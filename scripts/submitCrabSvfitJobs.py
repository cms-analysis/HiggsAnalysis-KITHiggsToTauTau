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

def check_path(path):
	if os.path.exists(path):
		print(path + " already exists! Delete it now in order to re-initialize it by crab? [y/n]")
		yes = set(['yes','y', 'ye', ''])
		no = set(['no','n'])

		choice = raw_input().lower()
		if choice in yes:
			shutil.rmtree(path)
			return
		elif choice in no:
			return
		else:
			sys.stdout.write(path + " already exists! Delete it now in order to re-initialize it by crab?")


def submission(path):

	from CRABClient.UserUtilities import config
	config = config()

        today=datetime.date.today().strftime("%Y-%m-%d")

        # Crab submissions only allow for up to 10000 jobs per submission. For convienient (and stability reasons) limit the number to 8000 jobs per file
        files =0
        jobfile = open("svfit-%s.sh"%(today),"w+") 
        jobfile.write("#!/bin/bash\n")
        jobfile.write("declare -A arr\n")
	jobfile.write(CRAB_PREFIX)
        for index,file in enumerate(glob(path+"/*.root")):
            jobfile.write("arr[%s,0]=dcap://dcache-cms-dcap.desy.de/%s\n"%(index+1-8000*files,file))
            jobfile.write("arr[%s,1]=%s\n"%(index+1-8000*files,os.path.basename(file)))
            if index == 7999*(files+1):
                jobfile.write("if [ \"x$2\" != \"x\" ]; then\npushd %s\nSCRAM_ARCH=slc6_amd64_gcc493\nsource /cvmfs/cms.cern.ch/cmsset_default.sh\neval `scramv1 runtime -sh`\n"%(os.getcwd()))
                jobfile.write("ComputeSvfit -i ${arr[$1,0]} -o ${arr[$1,1]}\n")
                jobfile.write("else\n./ComputeSvfit -i ${arr[$1,0]} -o ${arr[$1,1]}\nfi\n")
                jobfile.write("if [ \"x$2\" == \"x\" ]; then\ntar -cf Svfit.tar ${arr[$1,1]}\nelse\ntar -cf Svfit_${1}.tar ${arr[$1,1]}\nfi\n")
                jobfile.write("rm ${arr[$1,1]}\n")
                jobfile.close()
                files += 1
                jobfile = open("svfit-%s-%s.sh"%(today,files),"w+") 
                jobfile.write("#!/bin/bash\n")
                jobfile.write("declare -A arr\n")
                jobfile.write(CRAB_PREFIX)
        jobfile.write("if [ \"x$2\" != \"x\" ]; then\npushd %s\nSCRAM_ARCH=slc6_amd64_gcc493\nsource /cvmfs/cms.cern.ch/cmsset_default.sh\neval `scramv1 runtime -sh`\n"%(os.getcwd()))
        jobfile.write("ComputeSvfit -i ${arr[$1,0]} -o ${arr[$1,1]}\n")
        jobfile.write("else\n./ComputeSvfit -i ${arr[$1,0]} -o ${arr[$1,1]}\nfi\n")
        jobfile.write("if [ \"x$2\" == \"x\" ]; then\ntar -cf Svfit.tar ${arr[$1,1]}\nelse\ntar -cf Svfit_${1}.tar ${arr[$1,1]}\nfi\n")
        jobfile.write("rm ${arr[$1,1]}\n")
        jobfile.close()

	config.General.workArea = '/nfs/dust/cms/user/%s/crab_svfit-%s'%(getUsernameFromSiteDB(),today)
	# check_path(config.General.workArea)
	config.General.transferOutputs = True
	config.General.transferLogs = True
	config.General.requestName = "SvFit-"+today

        config.Data.outputPrimaryDataset = 'Svfit'
        config.Data.splitting = 'EventBased'
        config.Data.unitsPerJob = 1
        config.Data.totalUnits = index if files == 0 else 8000
        config.Data.publication = False
        config.Data.outputDatasetTag = config.General.requestName
	config.Data.outLFNDirBase = '/store/user/%s/higgs-kit/Svfit/%s'%(getUsernameFromSiteDB(),today)
	config.Data.publication = False

	config.User.voGroup = 'dcms'
	
	config.JobType.pluginName = 'PrivateMC'
	config.JobType.psetName = os.environ['CMSSW_BASE']+'/src/CombineHarvester/CombineTools/scripts/do_nothing_cfg.py'
	config.JobType.inputFiles = ['Kappa/lib/libKappa.so','FrameworkJobReport.xml', os.environ['CMSSW_BASE']+'/bin/'+os.environ['SCRAM_ARCH']+'/ComputeSvfit', "svfit-%s.sh"%(today)]
	config.JobType.allowUndistributedCMSSW = True
	config.JobType.scriptExe = "svfit-%s.sh"%(today)
	config.JobType.outputFiles = ['Svfit.tar']
	
	config.Site.storageSite = "T2_DE_DESY"
	# config.Site.blacklist = ["T3_US_PuertoRico","T2_ES_CIEMAT","T2_DE_RWTH","T3_US_Colorado","T2_BR_UERJ","T2_ES_IFCA","T2_RU_JINR","T2_UA_KIPT","T2_EE_Estonia","T2_FR_GRIF_LLR","T2_CH_CERN","T2_FR_GRIF_LLR","T3_IT_Bologna","T2_US_Nebraska","T2_US_Nebraska","T3_TW_NTU_HEP","T2_US_Caltech","T3_US_Cornell","T2_IT_Legnaro","T2_HU_Budapest","T2_IT_Pisa","T2_US_Florida",'T2_IT_Bari',"T2_FR_GRIF_IRFU","T2_IT_Rome","T2_FR_GRIF_IRFU","T2_CH_CSCS","T3_TW_NCU"]
        p = Process(target=submit, args=(config,))
        p.start()
        p.join()

        for index2 in range(files):
            config.JobType.inputFiles = [os.environ['CMSSW_BASE']+'/src/Kappa/lib/libKappa.so',os.environ['CMSSW_BASE']+'/src/CombineHarvester/CombineTools/scripts/FrameworkJobReport.xml', os.environ['CMSSW_BASE']+'/bin/'+os.environ['SCRAM_ARCH']+'/ComputeSvfit', "svfit-%s-%s.sh"%(today,index2+1)]
            config.JobType.allowUndistributedCMSSW = True
            config.JobType.scriptExe = "svfit-%s_%s.sh"%(today,index2+1)
            config.General.requestName = "SvFit-%s_"%(index2+1)+today
            config.Data.totalUnits = 8000 if (index2 != files-1) else index-8000*files+1
            p = Process(target=submit, args=(config,))
            p.start()
            p.join()

if __name__ == "__main__":
	if len(sys.argv) == 1: 
		print "no setting provided"
		sys.exit()
	submission(sys.argv[1])
