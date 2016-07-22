#from gcSettings import Settings
#   this import is only needed to execute the script standalone
#   (<GCDIR>/packages needs to be in your PYTHONPATH - or grid-control was properly installed)

import time
import os
print(time.time())
active = ["0jet", "1jet", "2jet"]

active = active[0]
project_name = "2ndscan"
print "doing stuff for " + active

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
extra=" --n-plots 1000 0 --auto-rebin --qcd-subtract-shape -n 1 --remote"

cfg.parameters.set("parameters", ["P1", "P2"])
cfg.parameters.set("repeat", 1)
if active == "2jet":
	cfg.parameters.set("P1", ["0", "100", "200", "300", "400", "500", "600", "700", "800"])
	cfg.parameters.set("P2", ["0.0", "0.5", "1.0", "1.5", "2.0", "2.5", "3.0", "4.0","4.5", "5.0", "5.5", "6.0"])
elif active == "1jet":
	cfg.parameters.set("P1", ["0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100", "110", "120", "130", "140", "150"])
	cfg.parameters.set("P2", ["0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"])
else:
	cfg.parameters.set("P1", ["0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"])
	cfg.parameters.set("P2", ["0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"])

arguments = executable + " " + variable +" "+ mass +" "+ output_dir+ " " + extra + " " + input_dataset
for channel in channels:
	arguments = arguments +" --channel " + channel + " --categories"
	if active == "0jet":
		arguments = arguments +" 0jet_@P1@_@P2@ i0jet_@P1@_@P2@ "
	else:
		#arguments = arguments +" ZeroJet30 "
		arguments = arguments +" 0jet_10_50 i0jet_10_50 "

	if active == "1jet":
		arguments = arguments +" 1jet_@P1@_@P2@ i1jet_@P1@_@P2@ "
	else:
		#arguments = arguments +" OneJet30 "
		arguments = arguments +" 1jet_120_40 i1jet_120_40 "

	if active == "2jet":
		arguments = arguments +" vbf_@P1@_@P2@ ivbf_@P1@_@P2@ "
	else:
		#arguments = arguments +" TwoJet30 "
		arguments = arguments +" vbf_400_3.0 ivbf_400_3.0 "

cfg.usertask.set('arguments', "%s"%arguments)
cfg.storage.set('se path', "/nfs/dust/cms/user/rfriese/" + project_name + "/" + active + "scan")
cfg.storage.set('se output files', "jobresult.tar")
cfg.storage.set('se output pattern', "@P1@_@P2@/@X@")
getattr(cfg, 'global').set('workdir', "/nfs/dust/cms/user/rfriese/workdir_" + project_name + "/" + active)
print(cfg)
print('=' * 20)
