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
					self["TriggerEfficiencyData"] = [ "0:root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/hlushchenko/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Electron_Ele23_fall15.root" ]
					self["TriggerEfficiencyMc"] = [ "0:root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/hlushchenko/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele23_fall15.root"]

					self["IdentificationEfficiencyData"] = ["0:root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/hlushchenko/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2015_Electron_IdIso0p1_fall15.root"]
					self["IdentificationEfficiencyMc"] = ["0:root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/hlushchenko/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Electron_IdIso0p1_fall15.root"]

				elif re.search("Run2017|Summer17|Fall17", nickname):
					self["TriggerEfficiencyData"] = ["0:root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/hlushchenko/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2017_Electron_Ele32orEle35.root"]
					self["TriggerEfficiencyMc"] = ["0:root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/hlushchenko/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MCFall2017_Electron_Ele32orEle35.root"]

					self["IdentificationEfficiencyData"] = ["0:root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/hlushchenko/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2017_Electron_IdIso_IsoLt0.10_eff_RerecoFall17.root"]
					self["IdentificationEfficiencyMc"] = ["0:root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/hlushchenko/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MCFall2017_Electron_IdIso_IsoLt0.10_eff_RerecoFall17.root"]

				else:
					self["TriggerEfficiencyData"] = ["0:root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/hlushchenko/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Electron_Ele25WPTight_eff.root" ]
					self["TriggerEfficiencyMc"] = ["0:root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/hlushchenko/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele25WPTight_eff.root" ]

					self["IdentificationEfficiencyData"] = ["0:root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/hlushchenko/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Electron_IdIso_IsoLt0p1_eff.root"]
					self["IdentificationEfficiencyMc"] = ["0:root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/hlushchenko/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Electron_IdIso_IsoLt0p1_eff.root"]
		else:
			if channel == "ET":
				if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
					self["TriggerEfficiencyData"] = [ "0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Electron_Ele23_fall15.root" ]
					self["TriggerEfficiencyMc"] = [ "0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele23_fall15.root"]

					self["IdentificationEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2015_Electron_IdIso0p1_fall15.root"]
					self["IdentificationEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Electron_IdIso0p1_fall15.root"]

				elif re.search("Run2017|Summer17|Fall17", nickname):
					self["TriggerEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2017_Electron_Ele32orEle35.root"]
					self["TriggerEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MCFall2017_Electron_Ele32orEle35.root"]

					self["IdentificationEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2017_Electron_IdIso_IsoLt0.10_eff_RerecoFall17.root"]
					self["IdentificationEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MCFall2017_Electron_IdIso_IsoLt0.10_eff_RerecoFall17.root"]

				else:
					self["TriggerEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Electron_Ele25WPTight_eff.root" ]
					self["TriggerEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele25WPTight_eff.root" ]

					self["IdentificationEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Electron_IdIso_IsoLt0p1_eff.root"]
					self["IdentificationEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Electron_IdIso_IsoLt0p1_eff.root"]

				if re.search("Spring16", nickname):
					self["TriggerEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_dummy.root" ]



		# return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/ZZTo4L_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1.root"
		# log.warning("COULD NOT FIND THE SVFIT CACHE FILE")
