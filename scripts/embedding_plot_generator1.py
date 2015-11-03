#!/usr/bin/env python

command_template = '''python scripts/embedding_plot.py -plt-type "absolute" -plt-ttl "{CMSSW_VERSION}" -plt-fld "{CMSSW_VERSION}" -plt "{NAME}" -var "{VARIABLE}" -nfile "{NUMFILES}" -nfold "{NUMFOLDERS}" -nnick "{NUMNICKS}"'''

quantities = ["nPUMean","nPU","leadingLepPt", "leadingLepEta", "trailingLepPt","trailingLepEta"]

MC = {"name":"MC", "path":"/nfs/dust/cms/user/swayand/embedd_save/muonembed/ar_muonembed_K2Skim_FullReco.root"}
RH = {"name":"RH", "path":"/nfs/dust/cms/user/swayand/embedd_save/muonembed/ar_muonembed_K2Skim_Embed_RH.root"}
CMSSW_7_0_7 = {
	"name":"CMSSW_7_0_7",
	"files":[MC,RH],
	"folders":["genMatched", "Mu_Full", "Mu_iso_onlyall", "Mu_iso_onlyhadrons", "Mu_iso_onlyphotons", "Mu_iso_onlypu", "Mu_iso_onlyneutral"]
	}

MC_Run2 = {"name":"MC", "path":"/nfs/dust/cms/user/swayand/DATA_NMSSM/artus_prod/MC_ZMUMU/MC_ZMUMU_merged.root"}
RH_Run2 = {"name":"RH", "path":"/nfs/dust/cms/user/swayand/DATA_NMSSM/artus_prod/RH_MIRROR/RH_MIRROR_merged.root"}
CMSSW_7_4_12p4 = {
	"name":"CMSSW_7_4_12p4",
	"files":[MC_Run2,RH_Run2],
	"folders":["gen_matched", "muon_full", "iso_onlyall", "iso_onlyhadrons", "iso_onlyphotons", "iso_onlypu", "iso_onlyneutral"]
	}

CMSSW_list = [CMSSW_7_0_7, CMSSW_7_4_12p4]

shell_script = open("./plots.sh","w")
for version in CMSSW_list:
	for quantity in quantities:
		for folder in version["folders"]:
			name = quantity+"_"+folder
			numfolders = folder+";"+folder
			numfiles = ""
			numnicks = ""
			for rootfile in version["files"]:
				numfiles += rootfile["path"]+";"
				numnicks += (rootfile["name"]+"_"+folder+";")
			numfiles = numfiles.strip(";")
			numnicks = numnicks.strip(";")
			command = command_template.format(CMSSW_VERSION=version["name"], NAME=name, VARIABLE=quantity, NUMFILES=numfiles, NUMFOLDERS=numfolders, NUMNICKS=numnicks)
			shell_script.write(command+"\n")
shell_script.close()

