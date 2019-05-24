# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import os

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Includes.settingsKappa as sKappa
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Includes.settingsSampleStitchingWeights as sSSW
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJEC as sJEC
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsLheWeights as sLheWeights


class Baseconfig(dict):

	def __init__(self, nickname):

		"""
		"include" : [
		"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Includes/settingsKappa.json", #DONE
		"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsLheWeights.json", #DONE
		"#$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsJEC.json", #DONE
		"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Includes/settingsSampleStitchingWeights.json" #DONE
		"""


		Kappa_config = sKappa.Kappa(nickname)
		self.update(Kappa_config)

		LheWeights_config = sLheWeights.LheWeights(nickname)
		self.update(LheWeights_config)
		"""
		JEC_config = sJEC.JEC(nickname) # is commented out
		self.update(JEC_config)
		"""
		sampleStitchingWeight_config = sSSW.SampleStitchingWeights(nickname)
		self.update(sampleStitchingWeight_config)

		self["SkipEvents"] = 0
		self["EventCount"] = -1

		#self["OutputPath"] = "output.root"

		if re.search("Run201", nickname):
			self["InputIsData"] = "true" #string in json, possible to change to boolean?
		else:
			self["InputIsData"] = "false"

		if re.search("DY.?JetsToLL|EWKZ2Jets|Embedding(2016|MC)|LFV", nickname):
			self["BosonPdgIds"] = [23]
		elif re.search("^(GluGlu|GluGluTo|VBF|W|Wminus|Wplus|Z|JJ)(HToTauTau|H2JetsToTauTau|Higgs)", nickname):
			self["BosonPdgIds"] = [25]
		elif re.search("Pseudoscalar|Maxmix",nickname):
			self["BosonPdgIds"] = [25]
		elif re.search("W.?JetsToLN|EWKW", nickname):
			self["BosonPdgIds"] = [24]
		elif re.search("SUSY(BB|GluGlu|GluGluTo)(BB)?HToTauTau", nickname):
			self["BosonPdgIds"] = [25, 35 ,36]
		else:
			self["BosonPdgIds"] = [0]

		self["BosonStatuses"] = [11, 62]
		
		self["DeltaRMatchingRecoElectronGenParticle"] = 0.2
		self["DeltaRMatchingRecoElectronGenTau"] = 0.2
		self["DeltaRMatchingRecoMuonGenParticle"] = 0.2
		self["DeltaRMatchingRecoMuonGenTau"] = 0.2
		self["DeltaRMatchingRecoTauGenParticle"] = 0.2
		self["DeltaRMatchingRecoTauGenTau"] = 0.2
		self["RecoElectronMatchingGenParticlePdgIds"] = [ 11, 13 ]
		self["RecoMuonMatchingGenParticlePdgIds"] = [ 11, 13 ]
		self["RecoTauMatchingGenParticlePdgIds"] = [ 11, 13 ]
		self["RecoElectronMatchingGenParticleMatchAllElectrons"] = "true"
		self["RecoMuonMatchingGenParticleMatchAllMuons"] = "true"
		self["RecoTauMatchingGenParticleMatchAllTaus"] = "true"
		self["MatchAllElectronsGenTau"] = "true"
		self["MatchAllMuonsGenTau"] = "true"
		self["MatchAllTausGenTau"] = "true"
		self["MatchGenTauDecayMode"] = "true"
		self["UpdateMetWithCorrectedLeptons"] = "true"
		self["TopPtReweightingStrategy"] = "Run2"
		"""
		if re.search("(Run2016|Summer16|Spring16)", nickname):
			self["MetFilter"] = [
			#"Flag_HBHENoiseFilter",
			#"Flag_HBHENoiseIsoFilter",
			#"Flag_EcalDeadCellTriggerPrimitiveFilter",
			#"Flag_goodVertices",
			#"Flag_globalTightHalo2016Filter",
			"Flag_BadPFMuonFilter",
			"Flag_BadChargedCandidateFilter"
			]
		"""
		if re.search("Run2016", nickname):
			#self["MetFilter"].append("Flag_eeBadScFilter")
			self["MetFilter"] = [
			"!Flag_duplicateMuons",
			"!Flag_badMuons"
			]
		elif re.search("Summer16", nickname):
			self["MetFilter"] = [
			"!Flag_badGlobalMuonTaggerMAOD",
			"!Flag_cloneGlobalMuonTaggerMAOD"
			]

		if re.search("Run2017|Fall17", nickname):
			self["MetFilter"] = [  # suggested for MC and Data
				"Flag_goodVertices",
				"Flag_globalSuperTightHalo2016Filter",
				"Flag_HBHENoiseFilter",
				"Flag_HBHENoiseIsoFilter",
				"Flag_EcalDeadCellTriggerPrimitiveFilter",
				"Flag_BadPFMuonFilter",
				# "Flag_BadChargedCandidateFilter",   # not recommended, under review
				# "Flag_ecalBadCalibFilter",  # outdated; DO NOT USE (listed for completeness, updated version is the one below)
				# "ecalBadCalibReducedMINIAODFilter" TODO (still work in progress): https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#How_to_run_ecal_BadCalibReducedM
			]
			if re.search("Run2017", nickname):
				self["MetFilter"] += [
					"Flag_eeBadScFilter",
				]

		if re.search("Summer17", nickname):
			self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927-306462_RunBtoF_80bins_MC_Moriond17_PU25ns_V1_69p2MinBiasXS.root" 
			self["BTagScaleFactorFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/CSVv2_moriond17_BtoH.csv" 
			self["BTagEfficiencyFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/tagging_efficiencies_moriond2017.root" 

		elif re.search("Fall17", nickname) or re.search("adow", nickname):
			self["JetPrefireProbabilityFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/prefiring/L1prefiring_jetpt_2017BtoF.root"
			self["BTagScaleFactorFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/CSVv2_94XSF_V2_B_F.csv" #https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
			self["BTagEfficiencyFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/btagging_efficiency_2017/tagging_efficiencies_march2018_btageff-all_samp-inc-DeepCSV_medium.root" #TODO cant find this

			if re.search("Fall17", nickname) or re.search("adow", nickname): 
				pileupweightfile = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/SKIM_NOV2018_Fall17_CP/" + nickname +".root"
				if os.path.isfile(os.path.expandvars(pileupweightfile)):
					self["PileupWeightFile"] = pileupweightfile
				else:
					log.warning("automatic finding doesnt work,This is the inclusive pilupweight used for Fall17 are you sure you want to use this one?") #TODO create a new one?
					self["PileupWeightFile"] =  "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927-306462_13TeV_MC_94XFall17_99bins_69p2mbMinBiasXS.root"
			#elif re.search("Fall17", nickname): 
				"""
				log.warning("you are not using MiniAODv2, are you sure you want this")
				elif re.search("(DYJetsToLLM50).*(?=Fall17).*(?<!(ext1))$", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_DYJetsToLLM50_RunIIFall17MiniAOD_RECOSIMstep_13TeV_MINIAOD_madgraph-pythia8.root"
				elif re.search("(DYJetsToLLM50).*(?=Fall17).*(amcatnlo).*(?<!(ext1))$",nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_DYJetsToLLM50_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_amcatnlo-pythia8.root"
				elif re.search("(DYJetsToLLM50).*(?=Fall17).*(ext1)", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_DYJetsToLLM50_RunIIFall17MiniAOD_RECOSIMstep_13TeV_MINIAOD_madgraph-pythia8_ext1.root"

				elif re.search("(DY1JetsToLLM50).*(?=Fall17).*(?<!(ext1))$", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_DY1JetsToLLM50_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_madgraph-pythia8.root"
				elif re.search("(DY1JetsToLLM50).*(?=Fall17).*(ext1)", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_DY1JetsToLLM50_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_madgraph-pythia8_ext1.root"

				elif re.search("(DY2JetsToLLM50).*(?=Fall17).*(?<!(ext1))$", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_DY2JetsToLLM50_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_madgraph-pythia8.root"
				elif re.search("(DY2JetsToLLM50).*(?=Fall17).*(ext1)", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_DY2JetsToLLM50_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_madgraph-pythia8_ext1.root"

				elif re.search("(DY3JetsToLLM50).*(?=Fall17)", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_DY3JetsToLLM50_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_madgraph-pythia8.root"

				elif re.search("(DY4JetsToLLM50).*(?=Fall17)", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_DY4JetsToLLM50_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_madgraph-pythia8.root"

				elif re.search("(DYJetsToLLM10to50).*(?=Fall17)", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_DYJetsToLLM10to50_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_madgraph-pythia8.root"

				elif re.search("(STt-channelantitop).*(?=Fall17)", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_STt-channelantitop4finclusiveDecaysTuneCP5_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_powheg-pythia8.root"
				elif re.search("(STt-channeltop).*(?=Fall17)", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_STt-channeltop4finclusiveDecaysTuneCP5_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_powheg-pythia8.root"

				elif re.search("(STtWantitop5f).*(?=Fall17)", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_STtWantitop5finclusiveDecaysTuneCP5_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_powheg-pythia8.root"
				elif re.search("(STtWtop5f).*(?=Fall17).*(PSweights)", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_STtWtop5finclusiveDecaysTuneCP5PSweights_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_powheg-pythia8.root"
				elif re.search("(STtWtop5f).*(?=Fall17).*(?<!(PSweights))$", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_STtWtop5finclusiveDecaysTuneCP5_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_powheg-pythia8.root"

				elif re.search("(TTToHadronic).*(?=Fall17)", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_TTToHadronic_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_powheg-pythia8.root"
				elif re.search("(TTToSemiLeptonic).*(?=Fall17)", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_TTToSemiLeptonic_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_powheg-pythia8.root"
				elif re.search("(TTo2L2Nu).*(?=Fall17)", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_TTo2L2Nu_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_powheg-pythia8.root"

				elif re.search("(W1JetsToLNu).*(?=Fall17)", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_W1JetsToLNu_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_madgraph-pythia8.root"
				elif re.search("(W2JetsToLNu).*(?=Fall17)", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_W2JetsToLNu_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_madgraph-pythia8.root"
				elif re.search("(W3JetsToLNu).*(?=Fall17)", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_W3JetsToLNu_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_madgraph-pythia8.root"
				elif re.search("(W4JetsToLNu).*(?=Fall17)", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_W4JetsToLNu_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_madgraph-pythia8.root"
				elif re.search("(WJetsToLNu).*(?=Fall17)", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_WJetsToLNu_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_madgraph-pythia8.root"

				elif re.search("(WW_).*(?=Fall17)", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_WW_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_pythia8.root"
				elif re.search("(WZ_).*(?=Fall17)", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_WZ_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_pythia8.root"
				elif re.search("(ZZ_).*(?=Fall17)", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_ZZ_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_pythia8.root"
				elif re.search("(GluGluHToTauTauM).*(?=Fall17)", nickname): #might change if jhu/madgraph is added
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_GluGluHToTauTauM125_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_powheg-pythia8.root"
				elif re.search("(VBFHToTauTauM).*(?=Fall17)", nickname):
					self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927_306462_EOY2017ReReco_80bins_69p2MinBiasXS/puweights_VBFHToTauTauM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_powheg-pythia8.root"
				else:   #carefull should be filespecific but also new way in gitlab mssm cern
					log.warning("This is the incluse pilupweight used for summer2017 are you sure you want to use this one?")
					self["PileupWeightFile"] =  "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927-306462_13TeV_MC_94XFall17_99bins_69p2mbMinBiasXS.root"
		"""
		elif re.search("(Spring16|Summer16)", nickname):
			self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2016_271036-284044_13TeVMoriond17_23Sep2016ReReco_69p2mbMinBiasXS.root"
			self["BTagScaleFactorFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/CSVv2_moriond17_BtoH.csv"
			self["BTagEfficiencyFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/tagging_efficiencies_moriond2017.root"

		elif re.search("Run201", nickname):
			self["PileupWeightFile"] = "not needed"
			self["BTagScaleFactorFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/CSVv2_76X.csv"
			self["BTagEfficiencyFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/tagging_efficiencies.root"

		elif re.search("Embedding", nickname):
			self["PileupWeightFile"] = "not needed"
			self["BTagScaleFactorFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/CSVv2_76X.csv"
			self["BTagEfficiencyFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/tagging_efficiencies.root"
		else:
			self["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2015_246908-260627_13TeVFall15MiniAODv2_PromptReco_69mbMinBiasXS.root"
			self["BTagScaleFactorFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/CSVv2_76X.csv"
			self["BTagEfficiencyFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/tagging_efficiencies.root"

		if re.search("(Fall15MiniAODv2|Run2015D)", nickname):
			self["MetCorrectionMethod"] = "quantileMapping"
		else:
			self["MetCorrectionMethod"] = "meanResolution"

		if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
			self["MetRecoilCorrectorFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/recoilMet/recoilPFMEt_76X_MG5.root"
			self["MvaMetRecoilCorrectorFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/recoilMet/recoilMvaMEt_76X_newTraining_MG5.root"
			self["ZptReweightProducerWeights"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/zpt/zpt_weights.root"

		elif re.search("(Run2016|Spring16|Summer16)", nickname):
			self["MetRecoilCorrectorFile"] ="$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/recoilMet/TypeI-PFMet_Run2016BtoH.root"
			self["MvaMetRecoilCorrectorFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/recoilMet/MvaMET_2016BCD.root"
			self["ZptReweightProducerWeights"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/zpt/zpt_weights_2016_BtoH.root"



		elif re.search("(Run2017|Summer17|Fall17|Embedding2017)", nickname) or re.search("adow", nickname): #FIXME No files for 2017 yet
			self["MetCorrectionMethod"] = "meanResolution"
			self["MetRecoilCorrectorFile"] ="$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/recoilMet/Type1_PFMET_2017.root"
			self["MvaMetRecoilCorrectorFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/recoilMet/MvaMET_2016BCD.root" #not there
			self["ZptReweightProducerWeights"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/zpt/zpt_weights_2017.root" #TODO



		
		self["MetShiftCorrectorFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/recoilMet/MEtSys.root"
		self["MvaMetShiftCorrectorFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/recoilMet/MEtSys.root"

		if re.search("(Fall15MiniAODv2|Run2015D)", nickname):
			self["ChooseMvaMet"] = True
		else:
			self["ChooseMvaMet"] = False

		if re.search("Run2015B", nickname):
			self["JsonFiles"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/json/Cert_13TeV_16Dec2015ReReco_Collisions15_50ns_JSON_v2.txt"]
		elif re.search("Run2015(C|D)|Embedding2015", nickname):
			self["JsonFiles"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/json/Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_v2.txt"]
		elif re.search("Run2016|Embedding2016", nickname):
			self["JsonFiles"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/json/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt"]
		elif re.search("Run2017|Embedding2017", nickname):
			self["JsonFiles"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/json/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt"]

		if re.search("(Fall15MiniAODv2)", nickname):
			self["SimpleMuTauFakeRateWeightLoose"] = [1.0, 1.0, 1.0, 1.0, 1.0]
			self["SimpleMuTauFakeRateWeightTight"] = [1.0, 1.0, 1.0, 1.0, 1.0]
			self["SimpleEleTauFakeRateWeightVLoose"] = [1.02, 1.11]
			self["SimpleEleTauFakeRateWeightTight"] = [1.80, 1.30]

		elif re.search("(Spring16|Summer16)", nickname):
			self["SimpleMuTauFakeRateWeightLoose"]	= [1.22, 1.12, 1.26, 1.22, 2.39]
			self["SimpleMuTauFakeRateWeightTight"] = [1.47, 1.55, 1.33, 1.72, 2.50]
			self["SimpleEleTauFakeRateWeightVLoose"] = [1.213, 1.375]
			self["SimpleEleTauFakeRateWeightTight"] = [1.402, 1.90]

# https://indico.cern.ch/event/738043/contributions/3048471/attachments/1674773/2688351/TauId_26062018.pdf
		elif re.search("(Summer17|Fall17)", nickname) or re.search("adow", nickname):
			self["SimpleMuTauFakeRateWeightLoose"]	= [1.06, 1.02, 1.10, 1.03, 1.94]
			self["SimpleMuTauFakeRateWeightTight"] = [1.17, 1.29, 1.14, 0.93, 1.61]
			self["SimpleEleTauFakeRateWeightVLoose"] = [1.09, 1.19]
			self["SimpleEleTauFakeRateWeightTight"] = [1.80, 1.53] #also available are other wp

