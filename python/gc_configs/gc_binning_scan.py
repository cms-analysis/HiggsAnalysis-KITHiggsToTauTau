#from gcSettings import Settings
#   this import is only needed to execute the script standalone
#   (<GCDIR>/packages needs to be in your PYTHONPATH - or grid-control was properly installed)

import time
import os
print(time.time())
project_name = "binning_scan"

cfg = Settings()
cfg.workflow.task = 'UserTask'
cfg.workflow.backend = 'local'

cfg.jobs.wall_time = '12:00:00'
cfg.jobs.set("memory", "14000")

cfg.usertask.executable = 'HiggsAnalysis/KITHiggsToTauTau/scripts/userjob_epilog.sh'
cmssw_base = os.getenv("CMSSW_BASE") + "/src/"
cfg.usertask.set("input files", [cmssw_base + "HiggsAnalysis/KITHiggsToTauTau/scripts/userjob_epilog.sh", cmssw_base + "HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsSMHtt.py"] )

executable = 'makePlots_datacardsSMHtt.py'
input_dataset = "-i /nfs/dust/cms/user/rfriese/htautau/artus/2016-05-31_11-32_FullAnalysis/merged/"
variable = "-x m_sv"
mass = "-m 125"
output_dir = "-o ."
channels= ["et", "mt", "tt", "em"]
extra=" --n-plots 1000 0 --auto-rebin --qcd-subtract-shape -n 1 --remote --use-asimov-dataset"
categories = "-c mt -c et -c tt -c em --categories ZeroJet30 1jet_120_40 i1jet_120_40 vbf_400_3.0 vbf_400_3.0"

cfg.parameters.set("parameters", ["NBINS", "MAX"])
cfg.parameters.set("repeat", 1)
cfg.parameters.set("NBINS", ["5", "10", "20", "40", "80", "160"])
cfg.parameters.set("MAX", ["150", "200", "250", "300", "350"])


arguments = " " .join([executable, variable, mass, output_dir, extra, input_dataset, categories])
arguments = arguments + " --x-bins @NBINS@,0,@MAX@ "

cfg.usertask.set('arguments', "%s"%arguments)
cfg.storage.set('se path', "/nfs/dust/cms/user/rfriese/" + project_name )
cfg.storage.set('se output files', "jobresult.tar")
cfg.storage.set('se output pattern', "@NBINS@_@MAX@/@X@")
getattr(cfg, 'global').set('workdir', "/nfs/dust/cms/user/rfriese/workdir_" + project_name)
print(cfg)
print('=' * 20)
