#!/bin/env python
# crab submission script
# usage: python crabConfig.py submit

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
	for path in glob(base_path+"/*"):
		dataset_nick = path.split('/')[-1]
		print "nick: " + dataset_nick
		print "path: " +path
		# Crab submissions only allow for up to 10000 jobs per submission. For convienient (and stability reasons) limit the number to 8000 jobs per file
		files =0
		jobfile_name = get_filename(today,dataset_nick)
		jobfile = open(jobfile_name,"w+") 
		jobfile.write("#!/bin/bash\n")
		jobfile.write("declare -A arr\n")
		jobfile.write(CRAB_PREFIX)
		cache_files = [f for f in glob(path+"/*.root") if("SvfitCache" in f)]
		cache_files = [f for f in cache_files if not ("em" in f)]
		for index,file in enumerate(cache_files):
			jobfile.write("arr[%s,0]=dcap://dcache-cms-dcap.desy.de/%s\n"%(index+1-8000*files,file))
			#jobfile.write("arr[%s,1]=%s\n"%(index+1-8000*files,os.path.basename(file)))
			jobfile.write("arr[%s,1]=%s\n"%(index+1-8000*files,"SvfitCache.root"))
			if index == 7999*(files+1):
				jobfile.write("if [ \"x$2\" != \"x\" ]; then\npushd %s\nSCRAM_ARCH=slc6_amd64_gcc493\nsource /cvmfs/cms.cern.ch/cmsset_default.sh\neval `scramv1 runtime -sh`\n"%(os.getcwd()))
				jobfile.write("ComputeSvfit -i ${arr[$1,0]} -o ${arr[$1,1]}\n")
				jobfile.write("else\n./ComputeSvfit -i ${arr[$1,0]} -o ${arr[$1,1]}\nfi\n")
				#jobfile.write("if [ \"x$2\" == \"x\" ]; then\ntar -cf Svfit.tar ${arr[$1,1]}\nelse\ntar -cf Svfit_${1}.tar ${arr[$1,1]}\nfi\n")
				#jobfile.write("rm ${arr[$1,1]}\n")
				jobfile.close()
				files += 1
				jobfile_i = get_filename( today,dataset_nick,files)
				jobfile = open(jobfile_i, "w+")
				jobfile.write("#!/bin/bash\n")
				jobfile.write("declare -A arr\n")
				jobfile.write(CRAB_PREFIX)
		jobfile.write("if [ \"x$2\" != \"x\" ]; then\npushd %s\nSCRAM_ARCH=slc6_amd64_gcc493\nsource /cvmfs/cms.cern.ch/cmsset_default.sh\neval `scramv1 runtime -sh`\n"%(os.getcwd()))
		jobfile.write("ComputeSvfit -i ${arr[$1,0]} -o ${arr[$1,1]}\n")
		jobfile.write("else\n./ComputeSvfit -i ${arr[$1,0]} -o ${arr[$1,1]}\nfi\n")
		#jobfile.write("if [ \"x$2\" == \"x\" ]; then\ntar -cf Svfit.tar ${arr[$1,1]}\nelse\ntar -cf Svfit_${1}.tar ${arr[$1,1]}\nfi\n")
		#jobfile.write("rm ${arr[$1,1]}\n")
		jobfile.close()
		
		config.General.workArea = '/nfs/dust/cms/user/%s/%s/crab_svfit-%s'%(getUsernameFromSiteDB(),today,dataset_nick)
		config.General.transferOutputs = True
		config.General.transferLogs = True
		config.General.requestName = "SvFit-"+today

		config.Data.outputPrimaryDataset = 'Svfit'
		config.Data.splitting = 'EventBased'
		config.Data.unitsPerJob = 1
		config.Data.totalUnits = index if files == 0 else 8000
		config.Data.publication = False
		config.Data.outputDatasetTag = config.General.requestName
		config.Data.outLFNDirBase = '/store/user/%s/higgs-kit/Svfit/%s/%s/'%(getUsernameFromSiteDB(),today,dataset_nick)
		print "outdir: " + config.Data.outLFNDirBase
		config.Data.publication = False
		
		config.User.voGroup = 'dcms'
		
		config.JobType.pluginName = 'PrivateMC'
		config.JobType.psetName = os.environ['CMSSW_BASE']+'/src/CombineHarvester/CombineTools/scripts/do_nothing_cfg.py'
		config.JobType.inputFiles = ['Kappa/lib/libKappa.so','FrameworkJobReport.xml', os.environ['CMSSW_BASE']+'/bin/'+os.environ['SCRAM_ARCH']+'/ComputeSvfit', jobfile_name]
		config.JobType.allowUndistributedCMSSW = True
		config.JobType.scriptExe = jobfile_name
		config.JobType.outputFiles = ['SvfitCache.root']
			
		config.Site.storageSite = "T2_DE_DESY"
			# config.Site.blacklist = ["T3_US_PuertoRico","T2_ES_CIEMAT","T2_DE_RWTH","T3_US_Colorado","T2_BR_UERJ","T2_ES_IFCA","T2_RU_JINR","T2_UA_KIPT","T2_EE_Estonia","T2_FR_GRIF_LLR","T2_CH_CERN","T2_FR_GRIF_LLR","T3_IT_Bologna","T2_US_Nebraska","T2_US_Nebraska","T3_TW_NTU_HEP","T2_US_Caltech","T3_US_Cornell","T2_IT_Legnaro","T2_HU_Budapest","T2_IT_Pisa","T2_US_Florida",'T2_IT_Bari',"T2_FR_GRIF_IRFU","T2_IT_Rome","T2_FR_GRIF_IRFU","T2_CH_CSCS","T3_TW_NCU"]
		p = Process(target=submit, args=(config,))
		p.start()
		p.join()
		sys.exit(0)
		for index2 in range(files):
			config.JobType.inputFiles = [os.environ['CMSSW_BASE']+'/src/Kappa/lib/libKappa.so',os.environ['CMSSW_BASE']+'/src/CombineHarvester/CombineTools/scripts/FrameworkJobReport.xml', os.environ['CMSSW_BASE']+'/bin/'+os.environ['SCRAM_ARCH']+'/ComputeSvfit', get_filename(today,dataset_nick,index2+1)]
			config.JobType.allowUndistributedCMSSW = True
			config.JobType.scriptExe = get_filename(today,dataset_nick,index2+1)
			config.General.requestName = "SvFit-%s_"%(index2+1)+today
			config.Data.totalUnits = 8000 if (index2 != files-1) else index-8000*files+1
			p = Process(target=submit, args=(config,))
			p.start()
			p.join()
			sys.exit(0)

if __name__ == "__main__":
	if len(sys.argv) == 1: 
		print "no setting provided"
		sys.exit()
	submission(sys.argv[1])
