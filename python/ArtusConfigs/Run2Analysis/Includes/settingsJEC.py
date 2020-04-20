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

		elif re.search("(Summer16)", nickname): # corresponding to MC GT 94X_mcRun2_asymptotic_v3
			self["JetEnergyCorrectionUncertaintyParameters"] =  "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_07Aug2017_V11_MC/Summer16_07Aug2017_V11_MC_UncertaintySources_AK4PFchs.txt"
			self["JetEnergyCorrectionParameters"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_07Aug2017_V11_MC/Summer16_07Aug2017_V11_MC_L1FastJet_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_07Aug2017_V11_MC/Summer16_07Aug2017_V11_MC_L2Relative_AK4PFchs.txt", "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_07Aug2017_V11_MC/Summer16_07Aug2017_V11_MC_L3Absolute_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_07Aug2017_V11_MC/Summer16_07Aug2017_V11_MC_L2L3Residual_AK4PFchs.txt"]
		elif re.search("((Run|Embedding2016)(A|B|C))", nickname): # corresponding to DATA GT 94X_dataRun2_v10
			self["JetEnergyCorrectionUncertaintyParameters"] =  "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_07Aug2017BCD_V11_DATA/Summer16_07Aug2017BCD_V11_DATA_UncertaintySources_AK4PFchs.txt"
			self["JetEnergyCorrectionParameters"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_07Aug2017BCD_V11_DATA/Summer16_07Aug2017BCD_V11_DATA_L1FastJet_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_07Aug2017BCD_V11_DATA/Summer16_07Aug2017BCD_V11_DATA_L2Relative_AK4PFchs.txt", "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_07Aug2017BCD_V11_DATA/Summer16_07Aug2017BCD_V11_DATA_L3Absolute_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_07Aug2017BCD_V11_DATA/Summer16_07Aug2017BCD_V11_DATA_L2L3Residual_AK4PFchs.txt"]
		elif re.search("((Run|Embedding2016)(E|F))", nickname): # corresponding to DATA GT 94X_dataRun2_v10
			self["JetEnergyCorrectionUncertaintyParameters"] =  "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_07Aug2017EF_V11_DATA/Summer16_07Aug2017EF_V11_DATA_UncertaintySources_AK4PFchs.txt"
			self["JetEnergyCorrectionParameters"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_07Aug2017EF_V11_DATA/Summer16_07Aug2017EF_V11_DATA_L1FastJet_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_07Aug2017EF_V11_DATA/Summer16_07Aug2017EF_V11_DATA_L2Relative_AK4PFchs.txt", "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_07Aug2017EF_V11_DATA/Summer16_07Aug2017EF_V11_DATA_L3Absolute_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_07Aug2017EF_V11_DATA/Summer16_07Aug2017EF_V11_DATA_L2L3Residual_AK4PFchs.txt"]
		elif re.search("((Run|Embedding2016)(G|H))", nickname): # corresponding to DATA GT 94X_dataRun2_v10
			self["JetEnergyCorrectionUncertaintyParameters"] =  "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_07Aug2017GH_V11_DATA/Summer16_07Aug2017GH_V11_DATA_UncertaintySources_AK4PFchs.txt"
			self["JetEnergyCorrectionParameters"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_07Aug2017GH_V11_DATA/Summer16_07Aug2017GH_V11_DATA_L1FastJet_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_07Aug2017GH_V11_DATA/Summer16_07Aug2017GH_V11_DATA_L2Relative_AK4PFchs.txt", "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_07Aug2017GH_V11_DATA/Summer16_07Aug2017GH_V11_DATA_L3Absolute_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_07Aug2017GH_V11_DATA/Summer16_07Aug2017GH_V11_DATA_L2L3Residual_AK4PFchs.txt"]

		elif re.search("(Autumn18)", nickname): # corresponding to MC GT 102X_upgrade2018_realistic_v20
			self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_V19_MC/Autumn18_V19_MC_UncertaintySources_AK4PFchs.txt"
			self["JetEnergyCorrectionParameters"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_V19_MC/Autumn18_V19_MC_L1FastJet_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_V19_MC/Autumn18_V19_MC_L2Relative_AK4PFchs.txt", "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_V19_MC/Autumn18_V19_MC_L3Absolute_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_V19_MC/Autumn18_V19_MC_L2L3Residual_AK4PFchs.txt"]

		elif re.search("((Run|Embedding)2018A)", nickname): # corresponding to DATA GT 102X_dataRun2_v12
			self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_RunA_V19_DATA/Autumn18_RunA_V19_DATA_UncertaintySources_AK4PFchs.txt"
			self["JetEnergyCorrectionParameters"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_RunA_V19_DATA/Autumn18_RunA_V19_DATA_L1FastJet_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_RunA_V19_DATA/Autumn18_RunA_V19_DATA_L2Relative_AK4PFchs.txt", "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_RunA_V19_DATA/Autumn18_RunA_V19_DATA_L3Absolute_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_RunA_V19_DATA/Autumn18_RunA_V19_DATA_L2L3Residual_AK4PFchs.txt"]

		elif re.search("((Run|Embedding)2018B)", nickname): # corresponding to DATA GT 102X_dataRun2_v12
			self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_RunB_V19_DATA/Autumn18_RunB_V19_DATA_UncertaintySources_AK4PFchs.txt"
			self["JetEnergyCorrectionParameters"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_RunB_V19_DATA/Autumn18_RunB_V19_DATA_L1FastJet_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_RunB_V19_DATA/Autumn18_RunB_V19_DATA_L2Relative_AK4PFchs.txt", "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_RunB_V19_DATA/Autumn18_RunB_V19_DATA_L3Absolute_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_RunB_V19_DATA/Autumn18_RunB_V19_DATA_L2L3Residual_AK4PFchs.txt"]

		elif re.search("((Run|Embedding)2018C)", nickname): # corresponding to DATA GT 102X_dataRun2_v12
			self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_RunC_V19_DATA/Autumn18_RunC_V19_DATA_UncertaintySources_AK4PFchs.txt"
			self["JetEnergyCorrectionParameters"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_RunC_V19_DATA/Autumn18_RunC_V19_DATA_L1FastJet_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_RunC_V19_DATA/Autumn18_RunC_V19_DATA_L2Relative_AK4PFchs.txt", "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_RunC_V19_DATA/Autumn18_RunC_V19_DATA_L3Absolute_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_RunC_V19_DATA/Autumn18_RunC_V19_DATA_L2L3Residual_AK4PFchs.txt"]

		elif re.search("((Run|Embedding)2018D)", nickname): # corresponding to DATA GT 102X_dataRun2_Prompt_v15
			self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_RunD_V19_DATA/Autumn18_RunD_V19_DATA_UncertaintySources_AK4PFchs.txt"
			self["JetEnergyCorrectionParameters"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_RunD_V19_DATA/Autumn18_RunD_V19_DATA_L1FastJet_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_RunD_V19_DATA/Autumn18_RunD_V19_DATA_L2Relative_AK4PFchs.txt", "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_RunD_V19_DATA/Autumn18_RunD_V19_DATA_L3Absolute_AK4PFchs.txt","$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Autumn18/Autumn18_RunD_V19_DATA/Autumn18_RunD_V19_DATA_L2L3Residual_AK4PFchs.txt"]

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
