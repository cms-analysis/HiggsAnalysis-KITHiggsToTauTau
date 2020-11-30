# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import copy

class IdAndTriggerSF(dict):
	def __init__(self, nickname, channel, dcach=False):

		if dcach:
			if channel == "ET":
				if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
					self["TriggerEfficiencyData"] = [ "0:root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/ohlushch/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Electron_Ele23_fall15.root" ]
					self["TriggerEfficiencyMc"] = [ "0:root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/ohlushch/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele23_fall15.root"]

					self["IdentificationEfficiencyData"] = ["0:root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/ohlushch/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2015_Electron_IdIso0p1_fall15.root"]
					self["IdentificationEfficiencyMc"] = ["0:root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/ohlushch/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Electron_IdIso0p1_fall15.root"]

				elif re.search("Run2017|Summer17|Fall17|Embedding2017", nickname):
					self["TriggerEfficiencyData"] = ["0:root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/ohlushch/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2017_Electron_Ele32orEle35.root"]
					self["TriggerEfficiencyMc"] = ["0:root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/ohlushch/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MCFall2017_Electron_Ele32orEle35.root"]

					self["IdentificationEfficiencyData"] = ["0:root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/ohlushch/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2017_Electron_IdIso_IsoLt0.10_eff_RerecoFall17.root"]
					self["IdentificationEfficiencyMc"] = ["0:root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/ohlushch/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MCFall2017_Electron_IdIso_IsoLt0.10_eff_RerecoFall17.root"]

				else:
					self["TriggerEfficiencyData"] = ["0:root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/ohlushch/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Electron_Ele25WPTight_eff.root" ]
					self["TriggerEfficiencyMc"] = ["0:root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/ohlushch/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele25WPTight_eff.root" ]

					self["IdentificationEfficiencyData"] = ["0:root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/ohlushch/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Electron_IdIso_IsoLt0p1_eff.root"]
					self["IdentificationEfficiencyMc"] = ["0:root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/ohlushch/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Electron_IdIso_IsoLt0p1_eff.root"]
		else:
			if channel in ["ET", "MT", "TT"]:
				self["TauTrigger2017WorkingPoints"] = [
					"vloose",
					"loose",
					"medium",
					"tight",
					"vtight",
					"vvtight",
				]
				self["DeepTauIDWorkingPoints"] = [
					"VVVLOOSE",
					"VVLOOSE",
					"VLOOSE",
					"LOOSE",
					"MEDIUM",
					"TIGHT",
					"VTIGHT",
					"VVTIGHT",
				]
				if re.search("Run2016|Summer16|Embedding2016", nickname):
					self["DeepTauTriggerInput"] = "$CMSSW_BASE/src/TauAnalysisTools/TauTriggerSFs/data/2016_tauTriggerEff_DeepTau2017v2p1.root"
				elif re.search("Run2017|Fall17|Embedding2017", nickname):
					self["DeepTauTriggerInput"] = "$CMSSW_BASE/src/TauAnalysisTools/TauTriggerSFs/data/2017_tauTriggerEff_DeepTau2017v2p1.root"
				elif re.search("Run2018|Autumn18|Embedding2018", nickname):
					self["DeepTauTriggerInput"] = "$CMSSW_BASE/src/TauAnalysisTools/TauTriggerSFs/data/2018_tauTriggerEff_DeepTau2017v2p1.root"

			if channel == "ET":
				if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
					self["TriggerEfficiencyData"] = [ "0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Electron_Ele23_fall15.root" ]
					self["TriggerEfficiencyMc"] = [ "0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele23_fall15.root"]

					self["IdentificationEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2015_Electron_IdIso0p1_fall15.root"]
					self["IdentificationEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Electron_IdIso0p1_fall15.root"]

					self["TriggerEfficiencyMode"] = "multiply_weights"
					self["IdentificationEfficiencyMode"] = "multiply_weights"

				#TODO CHANGE TO HALES NEWEST COMMIT
				elif re.search("Run2017|Summer17|Fall17|Embedding2017", nickname):
					self["TriggerEfficiencyData"] = [
							"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2017_Electron_Ele35WPTight_IsoLt0.10_eff_RerecoFall17.root",
							"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2017_Electron_EleTau_Ele24.root"
					]

					self["TriggerEfficiencyMc"] = [
							"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MCFall2017_Electron_Ele35WPTight_IsoLt0.10_eff_RerecoFall17.root",
							"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MCFall2017_Electron_EleTau_Ele24.root"
					]

					self["IdentificationEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2017_Electron_IdIso_IsoLt0.10_eff_RerecoFall17.root"]
					self["IdentificationEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MCFall2017_Electron_IdIso_IsoLt0.10_eff_RerecoFall17.root"]

					self["TauTrigger2017Input"] = "$CMSSW_BASE/src/TauAnalysisTools/TauTriggerSFs/data/tauTriggerEfficiencies2017.root"
					# self["TauTrigger2017InputOLD"] = "$CMSSW_BASE/src/TauTriggerSFs2017/TauTriggerSFs2017/data/tauTriggerEfficiencies2017.root"
					# self["TauTrigger2017WorkingPoint"] = "tight"

					self["TriggerEfficiencyMode"] = "no_overlap_triggers"
					self["IdentificationEfficiencyMode"] = "multiply_weights"

				else:
					self["TriggerEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Electron_Ele25WPTight_eff.root" ]
					self["TriggerEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele25WPTight_eff.root" ]

					self["IdentificationEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Electron_IdIso_IsoLt0p1_eff.root"]
					self["IdentificationEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Electron_IdIso_IsoLt0p1_eff.root"]

					self["TriggerEfficiencyMode"] = "multiply_weights"
					self["IdentificationEfficiencyMode"] = "multiply_weights"

				if re.search("Spring16", nickname):
					self["TriggerEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_dummy.root" ]

			if channel == "MT":
				self["TriggerEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Muon_Mu22OR_eta2p1_eff.root"]
				self["TriggerEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu22OR_eta2p1_eff.root"]
				self["IdentificationEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Muon_IdIso_IsoLt0p15_2016BtoH_eff.root"]
				self["IdentificationEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Muon_IdIso_IsoLt0p15_2016BtoH_eff.root"]

				self["TriggerEfficiencyMode"] = "multiply_weights"
				self["IdentificationEfficiencyMode"] = "multiply_weights"

				if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
					self["TriggerEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Muon_IsoMu18_fall15.root"]
					self["TriggerEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_IsoMu18_fall15.root"]
					self["IdentificationEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2015_Muon_IdIso0p1_fall15.root"]
					self["IdentificationEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Muon_IdIso0p1_fall15.root"]

				elif re.search("Run2017|Summer17|Fall17", nickname):
					# triggerEfficiency_Run2017_Muon_IsoMu24orIsoMu27.root
					# triggerEfficiency_MCFall2017_Muon_IsoMu24orIsoMu27.root
					# triggerEfficiency_Run2017_Muon_IsoMu27.root
					# triggerEfficiency_MCFall2017_Muon_IsoMu27.root

					#or should 1 be 1:triggerEfficiency_Run2017_Muon_MuTau_IsoMu24.root? 				#TODO CHANGE TO HALES NEWEST COMMIT
					self["TriggerEfficiencyData"] = [
								"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2017_Muon_IsoMu27_IsoLt0.15_eff_RerecoFall17.root",
								"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2017_Muon_MuTau_IsoMu20.root",
					]
					self["TriggerEfficiencyMc"] = [
								"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MCFall2017_Muon_IsoMu27_IsoLt0.15_eff_RerecoFall17.root",
								"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MCFall2017_Muon_MuTau_IsoMu20.root",
					]
					self["TauTrigger2017Input"] = "$CMSSW_BASE/src/TauAnalysisTools/TauTriggerSFs/data/tauTriggerEfficiencies2017.root"
					# self["TauTrigger2017InputOLD"] = "$CMSSW_BASE/src/TauTriggerSFs2017/TauTriggerSFs2017/data/tauTriggerEfficiencies2017.root"
					self["TauTrigger2017WorkingPoint"] = "tight"

					# identificationEfficiency_Run2017_Muon_IdIso_IsoLt0p15_2017B_eff.root
					# identificationEfficiency_MCFall2017_Muon_IdIso_IsoLt0p15_2017B_eff.root
					self["IdentificationEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2017_Muon_IdIso_IsoLt0p15_2017B_eff.root"]
					self["IdentificationEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MCFall2017_Muon_IdIso_IsoLt0p15_2017B_eff.root"]

					self["TriggerEfficiencyMode"] = "no_overlap_triggers"

				elif re.search("Spring16", nickname):
					self["TriggerEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_dummy.root"]

			if channel == "TT":
				if re.search("Run2017|Summer17|Fall17", nickname):
					self["TauTrigger2017Input"] = "$CMSSW_BASE/src/TauAnalysisTools/TauTriggerSFs/data/tauTriggerEfficiencies2017.root"
					# self["TauTrigger2017InputOLD"] = "$CMSSW_BASE/src/TauTriggerSFs2017/TauTriggerSFs2017/data/tauTriggerEfficiencies2017.root"
					self["TauTrigger2017WorkingPoint"] = "tight" #TODO might change for 2017
					self["TriggerEfficiencyMode"] = "no_overlap_triggers"
					# self["TriggerEfficiencyMode"] = "multiply_tau2017_weights"
					self["IdentificationEfficiencyMode"] = "multiply_weights"


			if channel == "EM":
				self["TriggerEfficiencyMode"] = "correlate_triggers" #TODO might change for 2017
				self["IdentificationEfficiencyMode"] = "multiply_weights"

				if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
					self["TriggerEfficiencyData"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Electron_Ele12_fall15.root",         	 #2 times 0:... and 1:...
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Electron_Ele17_fall15.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Muon_Mu8_fall15.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Muon_Mu17_fall15.root"
					]

					self["TriggerEfficiencyMc"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele12_fall15.root",
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele17_fall15.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu8_fall15.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu17_fall15.root"
					]

					self["IdentificationEfficiencyData"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Electron_IdIso_IsoLt0p15_eff.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Muon_IdIso_IsoLt0p2_2016BtoH_eff.root"
					]
					self["IdentificationEfficiencyMc"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Electron_IdIso0p15_fall15.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Muon_IdIso0p15_fall15.root"
					]

				else:
					self["TriggerEfficiencyData"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Electron_Ele12leg_eff.root",      		 #2 times 0:... and 1:...
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Electron_Ele23leg_eff.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Muon_Mu8leg_2016BtoH_eff.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Muon_Mu23leg_2016BtoH_eff.root"
					]
					self["TriggerEfficiencyMc"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele12leg_eff.root",
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele23leg_eff.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu8leg_2016BtoH_eff.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu23leg_2016BtoH_eff.root"
					]

					self["IdentificationEfficiencyData"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Electron_IdIso_IsoLt0p15_eff.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Muon_IdIso_IsoLt0p2_2016BtoH_eff.root"
					]
					self["IdentificationEfficiencyMc"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Electron_IdIso_IsoLt0p15_eff.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Muon_IdIso_IsoLt0p2_2016BtoH_eff.root"
					]

			if channel == "MM":
				if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
					self["TriggerEfficiencyData"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Muon_Mu8_fall15.root",
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Muon_Mu17_fall15.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Muon_Mu8_fall15.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Muon_Mu17_fall15.root"
					]
					self["TriggerEfficiencyMc"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu8_fall15.root",
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu17_fall15.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu8_fall15.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu17_fall15.root"
					]

					self["IdentificationEfficiencyData"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2015_Muon_IdIso0p15_fall15.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2015_Muon_IdIso0p15_fall15.root"
					]
					self["IdentificationEfficiencyMc"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Muon_IdIso0p15_fall15.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Muon_IdIso0p15_fall15.root"
					]

				else:
					#self["TriggerEfficiencyData"] = not given

					self["TriggerEfficiencyMc"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_dummy.root",
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_dummy.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_dummy.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_dummy.root"
					]

					self["IdentificationEfficiencyData"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Muon_IdIso_IsoLt0p15_2016BtoH_eff.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Muon_IdIso_IsoLt0p15_2016BtoH_eff.root"
					]
					self["IdentificationEfficiencyMc"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Muon_IdIso_IsoLt0p15_2016BtoH_eff.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Muon_IdIso_IsoLt0p15_2016BtoH_eff.root"
					]

		# return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/ZZTo4L_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1.root"
		# log.warning("COULD NOT FIND THE SVFIT CACHE FILE")
