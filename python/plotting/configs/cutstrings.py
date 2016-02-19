
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import sys

class CutStringsDict:
	
	@staticmethod
	def baseline(channel, cut_type):
		cuts = {}
		cuts["blind"] = "{blind}"
		cuts["os"] = "((q_1*q_2)<0.0)"
		
		if channel == "mm":
			pass
		elif channel == "ee":
			pass
		elif channel == "em":
			cuts["pzeta"] = "(pZetaMissVis > -20.0)"
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
			cuts["iso_1"] = "(iso_1 < 0.15)"
			cuts["iso_2"] = "(iso_2 < 0.15)"
		elif channel == "mt":
			cuts["mt"] = "(mt_1<40.0)"
			cuts["anti_e_tau_discriminators"] = "(againstElectronVLooseMVA6_2 > 0.5)"
			cuts["anti_mu_tau_discriminators"] = "(againstMuonTight3_2 > 0.5)"
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
			cuts["dilepton_veto"] = "(dilepton_veto < 0.5)"
			cuts["iso_1"] = "(iso_1 < 0.1)"
			cuts["iso_2"] = "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
		elif channel == "et":
			cuts["mt"] = "(mt_1<40.0)"
			cuts["anti_e_tau_discriminators"] = "(againstElectronTightMVA6_2 > 0.5)"
			cuts["anti_mu_tau_discriminators"] = "(againstMuonLoose3_2 > 0.5)"
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
			cuts["dilepton_veto"] = "(dilepton_veto < 0.5)"
			cuts["iso_1"] = "(iso_1 < 0.1)"
			cuts["iso_2"] = "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
		elif channel == "tt":
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
			cuts["anti_e_tau_discriminators"] = "(againstElectronVLooseMVA6_1 > 0.5)*(againstElectronVLooseMVA6_2 > 0.5)"
			cuts["anti_mu_tau_discriminators"] = "(againstMuonLoose3_1 > 0.5)*(againstMuonLoose3_2 > 0.5)"
			cuts["iso_1"] = "(byVTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5)"
			cuts["iso_2"] = "(byVTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antievloosepass(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 25.0)"
			cuts["iso_2"] = "(byLooseCombinedIsolationDeltaBetaCorr3Hits_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronVLooseMVA6_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antievloosefail(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 25.0)"
			cuts["iso_2"] = "(byLooseCombinedIsolationDeltaBetaCorr3Hits_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronVLooseMVA6_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antieloosepass(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 25.0)"
			cuts["iso_2"] = "(byLooseCombinedIsolationDeltaBetaCorr3Hits_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronLooseMVA6_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antieloosefail(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 25.0)"
			cuts["iso_2"] = "(byLooseCombinedIsolationDeltaBetaCorr3Hits_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronLooseMVA6_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antiemediumpass(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 25.0)"
			cuts["iso_2"] = "(byLooseCombinedIsolationDeltaBetaCorr3Hits_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronMediumMVA6_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antiemediumfail(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 25.0)"
			cuts["iso_2"] = "(byLooseCombinedIsolationDeltaBetaCorr3Hits_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronMediumMVA6_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antietightpass(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 25.0)"
			cuts["iso_2"] = "(byLooseCombinedIsolationDeltaBetaCorr3Hits_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronTightMVA6_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antietightfail(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 25.0)"
			cuts["iso_2"] = "(byLooseCombinedIsolationDeltaBetaCorr3Hits_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronTightMVA6_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antievtightpass(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 25.0)"
			cuts["iso_2"] = "(byLooseCombinedIsolationDeltaBetaCorr3Hits_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronVTightMVA6_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antievtightfail(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 25.0)"
			cuts["iso_2"] = "(byLooseCombinedIsolationDeltaBetaCorr3Hits_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronVTightMVA6_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antimuloosepass(channel, cut_type):
		if channel == "mt":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["pzeta"] = "(pZetaMissVis > -20.0)"
			cuts["discriminator"] = "(againstMuonLoose3_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antimuloosefail(channel, cut_type):
		if channel == "mt":
			cuts = CutStringsDict.baseline(channel, cut_type)
			#cuts["pzeta"] = "(pZetaMissVis > -20.0)"
			cuts["discriminator"] = "(againstMuonLoose3_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antimutightpass(channel, cut_type):
		if channel == "mt":
			cuts = CutStringsDict.baseline(channel, cut_type)
			#cuts["pzeta"] = "(pZetaMissVis > -20.0)"
			cuts["discriminator"] = "(againstMuonTight3_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antimutightfail(channel, cut_type):
		if channel == "mt":
			cuts = CutStringsDict.baseline(channel, cut_type)
			#cuts["pzeta"] = "(pZetaMissVis > -20.0)"
			cuts["discriminator"] = "(againstMuonTight3_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def tauidpass(channel, cut_type):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["discriminator"] = "(byMediumCombinedIsolationDeltaBetaCorr3Hits_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def tauidfail(channel, cut_type):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["discriminator"] = "(byMediumCombinedIsolationDeltaBetaCorr3Hits_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	
	def _get_cutdict(self, channel, cut_type):
		cuts = {}
		if cut_type=="baseline":
			cuts = CutStringsDict.baseline(channel, cut_type)
		elif cut_type=="antievloosepass":
			cuts = CutStringsDict.antievloosepass(channel, cut_type)
		elif cut_type=="antievloosefail":
			cuts = CutStringsDict.antievloosefail(channel, cut_type)
		elif cut_type=="antieloosepass":
			cuts = CutStringsDict.antieloosepass(channel, cut_type)
		elif cut_type=="antieloosefail":
			cuts = CutStringsDict.antieloosefail(channel, cut_type)
		elif cut_type=="antiemediumpass":
			cuts = CutStringsDict.antiemediumpass(channel, cut_type)
		elif cut_type=="antiemediumfail":
			cuts = CutStringsDict.antiemediumfail(channel, cut_type)
		elif cut_type=="antietightpass":
			cuts = CutStringsDict.antietightpass(channel, cut_type)
		elif cut_type=="antietightfail":
			cuts = CutStringsDict.antietightfail(channel, cut_type)
		elif cut_type=="antievtightpass":
			cuts = CutStringsDict.antievtightpass(channel, cut_type)
		elif cut_type=="antievtightfail":
			cuts = CutStringsDict.antievtightfail(channel, cut_type)
		
		elif cut_type=="antimuloosepass":
			cuts = CutStringsDict.antimuloosepass(channel, cut_type)
		elif cut_type=="antimuloosefail":
			cuts = CutStringsDict.antimuloosefail(channel, cut_type)
		elif cut_type=="antimutightpass":
			cuts = CutStringsDict.antimutightpass(channel, cut_type)
		elif cut_type=="antimutightfail":
			cuts = CutStringsDict.antimutightfail(channel, cut_type)
		
		elif cut_type=="tauidpass":
			cuts = CutStringsDict.tauidpass(channel, cut_type)
		elif cut_type=="tauidfail":
			cuts = CutStringsDict.tauidfail(channel, cut_type)
		else:
			log.fatal("No cut dictionary implemented for \"%s\"!" % cut_type)
			sys.exit(1)
		return cuts