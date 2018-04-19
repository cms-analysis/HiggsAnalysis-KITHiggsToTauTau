# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import pprint


class processors_ordered(dict):

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

			self["producer:ValidMTPairCandidatesProducer"] = 50
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
			self["filter:ValidDiTauPairCandidatesFilter"] = 60
			self["producer:HttValidVetoElectronsProducer"] = 70
			self["producer:HttValidLooseElectronsProducer"] = 80
			self["producer:HttValidLooseMuonsProducer"] = 90
			

		self["producer:Run2DecayChannelProducer"] = 100

		self["producer:MvaMetSelector"] = 105
					
		self["producer:DiVetoMuonVetoProducer"] = 110
		self["producer:DiVetoElectronVetoProducer"] = 111

		self["producer:TaggedJetCorrectionsProducer"] = 120

		self["producer:ValidTaggedJetsProducer"] = 130

		self["producer:ValidBTaggedJetsProducer"] = 140

		self["producer:TaggedJetUncertaintyShiftProducer"] = 150

		self["producer:MetCorrector"] = 160 
		self["producer:MvaMetCorrector"] = 161 

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

		self["producer:MELAProducer"] = 260
		self["producer:MELAM125Producer"] = 265

		self["producer:SimpleFitProducer"] = 270

		self["producer:TriggerWeightProducer"] = 275
		self["producer:IdentificationWeightProducer"] = 276
		self["producer:EleTauFakeRateWeightProducer"] = 277

		self["producer:RooWorkspaceWeightProducer"] = 280
			
		self["producer:MuTauTriggerWeightProducer"] = 290
		self["producer:TauTauTriggerWeightProducer"] = 291

		self["producer:GenMatchedTauCPProducer"] = 295

		self["producer:RefitVertexSelector"] = 300

		#from here it "only" creates the quantities so I left some numbers inbetween
		self["producer:RecoTauCPProducer"] = 400

		self["producer:GenMatchedPolarisationQuantitiesProducer"] = 500

		self["producer:PolarisationQuantitiesSvfitProducer"] = 600
		self["producer:PolarisationQuantitiesSvfitM91Producer"] = 633
		self["producer:PolarisationQuantitiesSimpleFitProducer"] = 666 #Producer of the devil, I hope he approves this if I go to hell

		self["producer:TauPolarisationTmvaReader"] = 700
			
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
				
	def get_demon_processor(self, processorlist, *args, **kwargs):
		if "producer:PolarisationQuantitiesSimpleFitProducer" in processorlist:
			print "Your artus config is possessed by an evil spirit. what are you gonna do about this?"
			print "1) pray"
			print "2) run"
			print "3) fight"
			print "choose 1 2 or 3"
			s = raw_input()
			if s=="1":
				print "the evil demon laughs at you, and you die"
			elif s=="2":
				print "you escaped but the artus run is still haunted"
			elif s=="3":
				print "after you reach for your sword the demon attacks. you die instantly, seriously what where you thinking????"
		else:
			print "your artus run is not possessed"
		
