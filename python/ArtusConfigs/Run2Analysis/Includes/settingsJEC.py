# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re


class JEC(dict):
	def __init__(self, nickname):

		# from https://twiki.cern.ch/twiki/bin/viewauth/CMS/JECDataMC
		if re.search("(Summer17)",nickname):
			self["JetEnergyCorrectionUncertaintyParameters"] = ""

		elif re.search("(Fall17)", nickname): # corresponding to MC GT 94X_mc2017_realistic_v17
			self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/Fall17_17Nov2017_V32_MC_UncertaintySources_AK4PFchs.txt"
			self["JetEnergyCorrectionParameters"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/Fall17_17Nov2017_V32_MC_L1FastJet_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/Fall17_17Nov2017_V32_MC_L2Relative_AK4PFchs.txt", "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/Fall17_17Nov2017_V32_MC_L3Absolute_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/Fall17_17Nov2017_V32_MC_L2L3Residual_AK4PFchs.txt"]

		elif re.search("((Run|Embedding)2017B)", nickname): # corresponding to DATA GT 94X_dataRun2_v11
			self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/Fall17_17Nov2017B_V32_DATA_UncertaintySources_AK4PFchs.txt"
			self["JetEnergyCorrectionParameters"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/Fall17_17Nov2017B_V32_DATA_L1FastJet_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/Fall17_17Nov2017B_V32_DATA_L2Relative_AK4PFchs.txt", "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/Fall17_17Nov2017B_V32_DATA_L3Absolute_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/Fall17_17Nov2017B_V32_DATA_L2L3Residual_AK4PFchs.txt"]

		elif re.search("((Run|Embedding)2017C)", nickname):
			self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/Fall17_17Nov2017C_V32_DATA_UncertaintySources_AK4PFchs.txt"
			self["JetEnergyCorrectionParameters"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/Fall17_17Nov2017C_V32_DATA_L1FastJet_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/Fall17_17Nov2017C_V32_DATA_L2Relative_AK4PFchs.txt", "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/Fall17_17Nov2017C_V32_DATA_L3Absolute_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/Fall17_17Nov2017C_V32_DATA_L2L3Residual_AK4PFchs.txt"]

		elif re.search("((Run|Embedding)2017D)", nickname):
			self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/Fall17_17Nov2017DE_V32_DATA_UncertaintySources_AK4PFchs.txt"
			self["JetEnergyCorrectionParameters"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/Fall17_17Nov2017DE_V32_DATA_L1FastJet_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/Fall17_17Nov2017DE_V32_DATA_L2Relative_AK4PFchs.txt", "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/Fall17_17Nov2017DE_V32_DATA_L3Absolute_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/Fall17_17Nov2017DE_V32_DATA_L2L3Residual_AK4PFchs.txt"]

		elif re.search("((Run|Embedding)2017E)", nickname):
			self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/Fall17_17Nov2017DE_V32_DATA_UncertaintySources_AK4PFchs.txt"
			self["JetEnergyCorrectionParameters"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/Fall17_17Nov2017DE_V32_DATA_L1FastJet_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/Fall17_17Nov2017DE_V32_DATA_L2Relative_AK4PFchs.txt", "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/Fall17_17Nov2017DE_V32_DATA_L3Absolute_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/Fall17_17Nov2017DE_V32_DATA_L2L3Residual_AK4PFchs.txt"]

		elif re.search("((Run|Embedding)2017F)", nickname):
			self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/Fall17_17Nov2017F_V32_DATA_UncertaintySources_AK4PFchs.txt"
			self["JetEnergyCorrectionParameters"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/Fall17_17Nov2017F_V32_DATA_L1FastJet_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/Fall17_17Nov2017F_V32_DATA_L2Relative_AK4PFchs.txt", "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/Fall17_17Nov2017F_V32_DATA_L3Absolute_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/Fall17_17Nov2017F_V32_DATA_L2L3Residual_AK4PFchs.txt"]

		# # NOTE: old
		# if re.search("(Summer17)",nickname):
		# 	self["JetEnergyCorrectionUncertaintyParameters"] = ""
		# elif re.search("(Fall17|Run2017|Embedding2017)", nickname): #this is recomended in https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2017#%20Jet/MET%20uncertainty%20treatment
		# 	self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/Fall17_17Nov2017F_V6_DATA_UncertaintySources_AK4PFchs.txt"
		# 	if re.search("(Run2017|Embedding2017)", nickname):
		# 		self["JetEnergyCorrectionParameters"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/94X_dataRun2_v10_L1FastJet_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/94X_dataRun2_v10_L2Relative_AK4PFchs.txt", "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/94X_dataRun2_v10_L3Absolute_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/94X_dataRun2_v10_L2L3Residual_AK4PFchs.txt"]
		#
		# 	elif re.search("(Fall17)", nickname):
		# 		self["JetEnergyCorrectionParameters"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/94X_mc2017_realistic_v15_L1FastJet_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/94X_mc2017_realistic_v15_L2Relative_AK4PFchs.txt", "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/94X_mc2017_realistic_v15_L3Absolute_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/correctionfiles/94X_mc2017_realistic_v15_L2L3Residual_AK4PFchs.txt"]

		elif re.search("(Run2016|Spring16|Summer16|Embedding2016)", nickname):
			self["JetEnergyCorrectionUncertaintyParameters"] =  "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_23Sep2016V4_DATA_UncertaintySources_AK4PFchs.txt"
		#elif re.search("Run2016|Embedding2016", nickname):
		#	self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_23Sep2016V4_DATA_Uncertainty_AK4PFchs.txt"
		elif re.search("(Fall15MiniAODv2)", nickname):
			self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_MC_Uncertainty_AK4PFchs.txt"
		elif re.search("(Run2015|Embedding2015)", nickname):
			self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_DATA_Uncertainty_AK4PFchs.txt"

		self["JetEnergyCorrectionUncertaintySource"] = "Total"
		#self["JetEnergyCorrectionUncertaintyShift"] = 0.0

		#All commented out

		if re.search("Run2015", nickname):
			self["JetEnergyCorrectionParameters"] = [
				"#$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_DATA_L1FastJet_AK4PFchs.txt",
				"#$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_DATA_L2Relative_AK4PFchs.txt",
				"#$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_DATA_L3Absolute_AK4PFchs.txt",
				"#$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_DATA_L2L3Residual_AK4PFchs.txt"
			]
		"""
		else:
			self["JetEnergyCorrectionParameters"] = [
				"#$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_MC_L1FastJet_AK4PFchs.txt",
				"#$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_MC_L2Relative_AK4PFchs.txt",
				"#$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_MC_L3Absolute_AK4PFchs.txt"
			]
		"""
