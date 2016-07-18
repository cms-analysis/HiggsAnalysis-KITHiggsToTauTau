#from gcSettings import Settings
#   this import is only needed to execute the script standalone
#   (<GCDIR>/packages needs to be in your PYTHONPATH - or grid-control was properly installed)

import time
print(time.time())
active = ["0jet", "1jet", "2jet"]

active = active[0]
print "doing stuff for " + active

cfg = Settings()
cfg.section('jobs').jobs = 2
cfg.workflow.task = 'UserTask'
cfg.workflow.backend = 'Host'

cfg.jobs.wall_time = '2:00'

cfg.usertask.executable = 'makePlots_datacardsSMHtt.py'

input_dataset = "-i /nfs/dust/cms/user/rfriese/htautau/artus/2016-05-31_11-32_FullAnalysis/merged/"
variable = "-x m_sv"
mass = "-m 125"
output_dir = "-o ."
channels= ["et", "mt", "tt", "em"]
extra=" --n-plots 1000 0 --auto-rebin --qcd-subtract-shape -n 3 --remote"

cfg.parameters.set("parameters", ["P1", "P2"])
cfg.parameters.set("repeat", 1)
if active == "2jet":
	cfg.parameters.set("P1", ["200", "300", "400", "500", "600", "700", "800", "900", "1000"])
	cfg.parameters.set("P2", ["1.0", "1.5", "2.0", "2.5", "3.0", "4.0","4.5", "5.0", "5.5", "6.0", "6.5"])
else:
	cfg.parameters.set("P1", ["20", "30", "40", "50", "60", "70", "80", "90", "100", "110", "120", "130", "140", "150"])
	cfg.parameters.set("P2", ["20", "30", "40", "50", "60", "70", "80", "90", "100"])

arguments = input_dataset + " " + variable +" "+ mass +" "+ output_dir+ " " + extra
for channel in channels:
	arguments = arguments +" -c " + channel + " --categories"
	if active == "0jet":
		arguments = arguments +" 0jet_@P1@_@P2@ i0jet_@P1@_@P2@ "
	else:
		arguments = arguments +" ZeroJet30 "

	if active == "1jet":
		arguments = arguments +" 1jet_@P1@_@P2@ i1jet_@P1@_@P2@ "
	else:
		arguments = arguments +" OneJet30 "

	if active == "2jet":
		arguments = arguments +" 2jet_@P1@_@P2@ i2jet_@P1@_@P2@ "
	else:
		arguments = arguments +" TwoJet30 "
#arguments = arguments + " -c mt --categories OneJet30"

cfg.usertask.set('arguments', arguments)
#cfg.usertask.set('output files', "jobresult.tar")
cfg.storage.set('se path', "/nfs/dust/cms/user/rfriese/scans/" + active + "scan")
cfg.storage.set('se output files', "jobresult.tar")
cfg.storage.set('se output pattern', "@P1@_@P2@/@X@")
getattr(cfg, 'global').set('workdir', "/nfs/dust/cms/user/rfriese/workdir/"+active)
print(cfg)
print('=' * 20)
