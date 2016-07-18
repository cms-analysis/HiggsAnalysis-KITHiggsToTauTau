#!/bin/env python
# crab submission script for standalone Svfit calculation
# usage: python submitCrabSvfitJobs.py /pnfs/[path to storage element with SvfitCache input files]

from CRABClient.UserUtilities import getUsernameFromSiteDB
from httplib import HTTPException
from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from multiprocessing import Process
import sys
from glob import glob
import os, shutil
import datetime

CRAB_PREFIX = """
set -x
set -e
ulimit -s unlimited
ulimit -c 0



echo "<FrameworkJobReport>
  <ReadBranches>
  </ReadBranches>
  <PerformanceReport>
    <PerformanceSummary Metric=\\"StorageStatistics\\">
      <Metric Name=\\"Parameter-untracked-bool-enabled\\" Value=\\"true\\"/>
      <Metric Name=\\"Parameter-untracked-bool-stats\\" Value=\\"true\\"/>
      <Metric Name=\\"Parameter-untracked-string-cacheHint\\" Value=\\"application-only\\"/>
      <Metric Name=\\"Parameter-untracked-string-readHint\\" Value=\\"auto-detect\\"/>
      <Metric Name=\\"ROOT-tfile-read-totalMegabytes\\" Value=\\"0\\"/>
      <Metric Name=\\"ROOT-tfile-write-totalMegabytes\\" Value=\\"0\\"/>
    </PerformanceSummary>
  </PerformanceReport>

  <GeneratorInfo>
  </GeneratorInfo>
</FrameworkJobReport>" >FrameworkJobReport.xml

function error_exit
{
  if [ $1 -ne 0 ]; then
    echo "Error with exit code ${1}"
    if [ -e FrameworkJobReport.xml ]
    then
      cat << EOF > FrameworkJobReport.xml.tmp
      <FrameworkJobReport>
      <FrameworkError ExitStatus="${1}" Type="" >
      Error with exit code ${1}
      </FrameworkError>
EOF
      tail -n+2 FrameworkJobReport.xml >> FrameworkJobReport.xml.tmp
      mv FrameworkJobReport.xml.tmp FrameworkJobReport.xml
    else
      cat << EOF > FrameworkJobReport.xml
      <FrameworkJobReport>
      <FrameworkError ExitStatus="${1}" Type="" >
      Error with exit code ${1}
      </FrameworkError>
      </FrameworkJobReport>
EOF
    fi
    exit 0
  fi
}
trap 'error_exit $?' ERR


"""

def submit(config):
	try:
		crabCommand('submit', config = config)
	except HTTPException as hte:
		print "Failed submitting task: %s" % (hte.headers)
	except ClientException as cle:
		print "Failed submitting task: %s" % (cle)

def get_filename(date, nick, index=None):
	if(index==None):
		return "svfit-%s-%s.sh"%(date, nick)
	else:
		return "svfit-%s-%s-%s.sh"%(date, nick, index)

def submission(base_path):

	from CRABClient.UserUtilities import config
	config = config()
	today=datetime.date.today().strftime("%Y-%m-%d")
	files =0
	cache_files = [f for f in glob(base_path+"/*/*.root") if("SvfitCache" in f)]
	if len(cache_files) == 0:
		return
	if len(cache_files) > 8000:
            cache_files = [cache_files[i:i+8000] for i in xrange(0,len(cache_files),8000)]
        else:
            cache_files = [cache_files]
        for index,cache_file in enumerate(cache_files):
            jobfile_name = get_filename(today,index)
            jobfile = open(jobfile_name,"w+")
            jobfile.write("#!/bin/bash\n")
            jobfile.write("declare -A arr\n")
            jobfile.write(CRAB_PREFIX)
            for index2,file in enumerate(cache_file):
                    jobfile.write("arr[%s,0]=dcap://dcache-cms-dcap.desy.de/%s\n"%(index2+1,file))
            jobfile.write("if [ \"x$2\" != \"x\" ]; then\npushd %s\nSCRAM_ARCH=slc6_amd64_gcc493\nsource /cvmfs/cms.cern.ch/cmsset_default.sh\neval `scramv1 runtime -sh`\n"%(os.getcwd()))
            jobfile.write("ComputeSvfit -i ${arr[$1,0]} -o SvfitCache.root\n")
            jobfile.write("else\n./ComputeSvfit -i ${arr[$1,0]} -o $(basename ${arr[$1,0]})\ntar -cf SvfitCache.tar $(basename ${arr[$1,0]})\nfi\n")
            jobfile.close()
			
            config.General.workArea = '/nfs/dust/cms/user/%s/%s/'%(getUsernameFromSiteDB(),today)
            config.General.transferOutputs = True
            config.General.transferLogs = True
            jobname = "SvFit_"+today+"_"+str(index)
            config.General.requestName = jobname
            print jobname
            config.Data.outputPrimaryDataset = 'Svfit'
            config.Data.splitting = 'EventBased'
            config.Data.unitsPerJob = 1
            config.Data.totalUnits = len(cache_file)
            config.Data.publication = False
            config.Data.outputDatasetTag = config.General.requestName
            config.Data.outLFNDirBase = '/store/user/%s/higgs-kit/Svfit/%s/'%(getUsernameFromSiteDB(),today)
            print "outdir: " + config.Data.outLFNDirBase
            config.Data.publication = False
			
            config.User.voGroup = 'dcms'
			
            config.JobType.pluginName = 'PrivateMC'
            config.JobType.psetName = os.environ['CMSSW_BASE']+'/src/CombineHarvester/CombineTools/scripts/do_nothing_cfg.py'
            config.JobType.inputFiles = ['Kappa/lib/libKappa.so', os.environ['CMSSW_BASE']+'/bin/'+os.environ['SCRAM_ARCH']+'/ComputeSvfit', jobfile_name]
            config.JobType.allowUndistributedCMSSW = True
            config.JobType.scriptExe = jobfile_name
            config.JobType.outputFiles = ['SvfitCache.tar']
			
            config.Site.storageSite = "T2_DE_DESY"
                    # config.Site.blacklist = ["T3_US_PuertoRico","T2_ES_CIEMAT","T2_DE_RWTH","T3_US_Colorado","T2_BR_UERJ","T2_ES_IFCA","T2_RU_JINR","T2_UA_KIPT","T2_EE_Estonia","T2_FR_GRIF_LLR","T2_CH_CERN","T2_FR_GRIF_LLR","T3_IT_Bologna","T2_US_Nebraska","T2_US_Nebraska","T3_TW_NTU_HEP","T2_US_Caltech","T3_US_Cornell","T2_IT_Legnaro","T2_HU_Budapest","T2_IT_Pisa","T2_US_Florida",'T2_IT_Bari',"T2_FR_GRIF_IRFU","T2_IT_Rome","T2_FR_GRIF_IRFU","T2_CH_CSCS","T3_TW_NCU"]
            p = Process(target=submit, args=(config,))
            p.start()
            p.join()

if __name__ == "__main__":
	if len(sys.argv) == 1: 
		print "no setting provided"
		sys.exit()
	submission(sys.argv[1])
