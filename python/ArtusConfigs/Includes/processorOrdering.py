# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re

class ProcessorsOrdered(dict):

	def __init__(self, *args, **kwargs):
		self.create_sorting_keydict(self, *args, **kwargs)

	def create_sorting_keydict(self, *args, **kwargs):
		self["producer:HltProducer"] = 0
		self["filter:HltFilter"] = 1
		#leave some numbers inbetween so (missing) producers can be added lateron, it is also possible to use floats. example:
		#order = {"a" :10, k:"10.5", "d" :10.2, "e":11)
		#examplelist = ["a", "e" "k", "d"]
		#examplelist.sort(key =lambda val: order[val])
		#print examplelist => ["a", "d", "k", "e"]

		self["producer:MetSelector"] = 10
		self["producer:MetSelectorPuppi"] = 10.1
		self["producer:MetFilterProducer"] = 11

		if kwargs.get("channel", None) == "GEN":

			self["producer:GenParticleProducer"] = 21
			self["producer:GenBosonFromGenParticlesProducer"] = 22
			self["producer:GenBosonProductionProducer"] = 23
			self["producer:GenBosonDiLeptonDecayModeProducer"] = 24
			self["producer:GenDiLeptonDecayModeProducer"] = 25
			self["producer:GenTauDecayProducer"] = 26
			self["producer:GenTauCPProducer"] = 27

			self["TauSpinnerProducer"] = 31

		if kwargs.get("channel", None) == "MT":
			self["producer:ValidMuonsProducer"] = 21
			self["filter:ValidMuonsFilter"] = 22
			self["producer:MuonTriggerMatchingProducer"] = 23
			self["filter:MinMuonsCountFilter"] = 24

			self["producer:ValidElectronsProducer"] = 30

			self["producer:TauCorrectionsProducer"] = 40
			self["producer:ValidTausProducer"] = 41
			self["filter:ValidTausFilter"] = 42
			self["producer:TauTriggerMatchingProducer"] = 43
			self["filter:MinTausCountFilter"] = 44

			self["producer:MuonCorrectionsProducer"] = 49
			self["producer:ValidMTPairCandidatesProducer"] = 50
			self["producer:NewValidMTPairCandidatesProducer"] = 50.1
			self["filter:ValidDiTauPairCandidatesFilter"] = 51
			self["producer:HttValidVetoMuonsProducer"] = 60
			self["producer:HttValidLooseElectronsProducer"] = 70
			self["producer:HttValidLooseMuonsProducer"] = 80

		if kwargs.get("channel", None) == "TT":
			self["producer:TauCorrectionsProducer"] = 21
			self["producer:ValidTausProducer"] = 22
			self["filter:ValidTausFilter"] = 23
			self["producer:TauTriggerMatchingProducer"] = 24
			self["filter:MinTausCountFilter"] = 25

			self["producer:ValidElectronsProducer"] = 30

			self["producer:ValidMuonsProducer"] = 40

			self["producer:ValidTTPairCandidatesProducer"] = 50
			self["producer:NewValidTTPairCandidatesProducer"] = 51
			self["filter:ValidDiTauPairCandidatesFilter"] = 60
			self["producer:HttValidLooseElectronsProducer"] = 70
			self["producer:HttValidLooseMuonsProducer"] = 80

		if kwargs.get("channel", None) == "EM":
			self["producer:ElectronCorrectionsProducer"] = 21
			self["producer:ValidElectronsProducer"] = 22
			self["filter:ValidElectronsFilter"] = 23
			self["producer:ElectronTriggerMatchingProducer"] = 24
			self["filter:MinElectronsCountFilter"] = 25

			self["producer:RecoElectronGenParticleMatchingProducer"] = 27 #if you grep this, it is already in globalprocessors

			self["producer:ValidMuonsProducer"] = 31
			self["filter:ValidMuonsFilter"] = 32
			self["producer:MuonTriggerMatchingProducer"] = 33
			self["filter:MinMuonsCountFilter"] = 34

			self["producer:RecoMuonGenParticleMatchingProducer"] = 37
			self["producer:MatchedLeptonsProducer"] = 38

			self["producer:ValidTausProducer"] = 40

			self["producer:ValidEMPairCandidatesProducer"] = 50
			self["producer:NewValidEMPairCandidatesProducer"] = 51
			self["filter:ValidDiTauPairCandidatesFilter"] = 60
			self["producer:HttValidLooseElectronsProducer"] = 70
			self["producer:HttValidLooseMuonsProducer"] = 80

		if kwargs.get("channel", None) == "ET":
			self["producer:ElectronCorrectionsProducer"] = 21  # not in cp json
			self["producer:ValidElectronsProducer"] = 22
			self["filter:ValidElectronsFilter"] = 23
			self["producer:ElectronTriggerMatchingProducer"] = 24
			self["filter:MinElectronsCountFilter"] = 25

			self["producer:ValidMuonsProducer"] = 30

			self["producer:TauCorrectionsProducer"] = 40
			self["producer:ValidTausProducer"] = 41
			self["filter:ValidTausFilter"] = 42
			self["producer:TauTriggerMatchingProducer"] = 43
			self["filter:MinTausCountFilter"] = 44

			self["producer:ValidETPairCandidatesProducer"] = 50
			self["producer:NewValidETPairCandidatesProducer"] = 51
			self["filter:ValidDiTauPairCandidatesFilter"] = 60

			self["producer:HttValidVetoElectronsProducer"] = 70
			self["producer:HttValidLooseElectronsProducer"] = 80
			self["producer:HttValidLooseMuonsProducer"] = 90

		if kwargs.get("channel", None) == "MM":
			self["producer:ValidMuonsProducer"] = 21
			self["filter:ValidMuonsFilter"] = 22
			self["producer:MuonTriggerMatchingProducer"] = 23
			self["filter:MinMuonsCountFilter"] = 24

			self["producer:ValidElectronsProducer"] = 30
			self["producer:ValidTausProducer"] = 41

			self["producer:ValidMMPairCandidatesProducer"] = 50
			self["producer:NewValidMMPairCandidatesProducer"] = 50.1
			self["filter:ValidDiTauPairCandidatesFilter"] = 51
			self["producer:HttValidLooseElectronsProducer"] = 70
			self["producer:HttValidLooseMuonsProducer"] = 80



		self["producer:Run2DecayChannelProducer"] = 100

		self["producer:DiVetoMuonVetoProducer"] = 110
		self["producer:DiVetoElectronVetoProducer"] = 111

		self["producer:TaggedJetCorrectionsProducer"] = 120

		self["producer:SmearedTaggedJetProducer"] = 122

		self["producer:GroupedJetUncertaintyShiftProducer"] = 125 #Not together with TaggedJetUncertaintyShiftProducer, but before validtaggedjetsProducer and validBtaggedJetsProducer

		self["producer:ValidTaggedJetsProducer"] = 130

		self["producer:ValidBTaggedJetsProducer"] = 140

		self["producer:TaggedJetUncertaintyShiftProducer"] = 150

		self["producer:MetCorrector"] = 160
		self["producer:MvaMetCorrector"] = 161
		self["producer:PuppiMetCorrector"] = 162

		self["producer:TauTauRestFrameSelector"] = 170

		self["producer:DiLeptonQuantitiesProducer"] = 180

		self["producer:DiJetQuantitiesProducer"] = 190

		self["producer:SimpleEleTauFakeRateWeightProducer"] = 200

		self["producer:SimpleMuTauFakeRateWeightProducer"] = 210

		self["producer:ZPtReweightProducer"] = 220
		self["producer:TopPtReweightingProducer"] = 221

		self["filter:MinimalPlotlevelFilter"] = 230

		self["producer:MVATestMethodsProducer"] = 240

		self["producer:SvfitProducer"] = 250
		self["producer:SvfitM91Producer"] = 253
		self["producer:SvfitM125Producer"] = 256

		self["producer:FastMttProducer"] = 251

		self["producer:MELAProducer"] = 260
		self["producer:MELAM125Producer"] = 265

		self["producer:SimpleFitProducer"] = 270
		self["producer:GenSimpleFitProducer"] = 271

		self["producer:TauTriggerEfficiency2017Producer"] = 274
		self["producer:DeepTauTriggerScaleFactorProducer"] = 274.5
		self["producer:TriggerWeightProducer"] = 275
		self["producer:IdentificationWeightProducer"] = 276
		self["producer:EleTauFakeRateWeightProducer"] = 277

		self["producer:PileUpJetIDScaleFactorWeightProducer"] = 278

		self["producer:RooWorkspaceWeightProducer"] = 280

		self["producer:MuTauTriggerWeightProducer"] = 290
		self["producer:TauTauTriggerWeightProducer"] = 291
		self["producer:EmbeddingWeightProducer"] = 292

		self["producer:LeptonTauTrigger2017WeightProducer"] = 292

		self["producer:LegacyWeightProducer"] = 293
		self["producer:LegacyWeightUncProducer"] = 294


		self["producer:GenMatchedTauCPProducer"] = 295

		self["producer:RefitVertexSelector"] = 300

		#from here it "only" creates the quantities so I left some numbers inbetween
		self["producer:RecoTauCPProducer"] = 400
		self["producer:IsomorphicMappingProducer"] = 410
		self["producer:QuantileMappingProducer"] = 411

		self["producer:GenMatchedPolarisationQuantitiesProducer"] = 500

		self["producer:PolarisationQuantitiesSvfitProducer"] = 600
		self["producer:PolarisationQuantitiesSvfitM91Producer"] = 633
		self["producer:PolarisationQuantitiesSimpleFitProducer"] = 666 #Producer of the devil, I hope he approves this if I go to hell

		self["producer:TauPolarisationTmvaReader"] = 700

		self["producer:JetToTauFakesProducer"] = 800
		self["producer:LegacyJetToTauFakesProducer"] = 800.1

		self["producer:CPInitialStateQuantitiesProducer"] = 850
		self["producer:PrefiringWeightProducer"] = 900

		#left a lot of numbers since "producer:EventWeightProducer" is always the last one
		self["producer:LFVJetCorrection2016Producer"] = 1900
		self["producer:EventWeightProducer"] = 2000

	def order_processors(self, processorlist, *args, **kwargs):
		processornumber = 1000
		while True:
			try:
				processorlist.sort(key =lambda val: self[val])
				break

			except KeyError, e:
				log.warning("keyerror while sorting processors, missing processor='%s'" %str(e.args[0]))
				log.warning("appending it at the bottom with number '%s', is this intended?" %str(processornumber))
				self[e.args[0]] = processornumber
				processornumber += 1
				if processornumber > 1005:
					log.error("missing more then 5 keys in ordering dict, check HiggsAnalysis/KITHiggsToTauTau/python/ArtusConfigs/processorOrdering.py")
					break
			else:
				log.error("error in sorting processors, HiggsAnalysis/KITHiggsToTauTau/python/ArtusConfigs/processorOrdering.py")
				break
		return processorlist
