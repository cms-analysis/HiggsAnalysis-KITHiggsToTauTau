
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
			cuts["not2prong"] = "((decayMode_2<5)||(decayMode_2>6))"
			cuts["anti_e_tau_discriminators"] = "(againstElectronVLooseMVA5_2 > 0.5)"
			cuts["anti_mu_tau_discriminators"] = "(againstMuonTight3_2 > 0.5)"
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
			cuts["dilepton_veto"] = "(dilepton_veto < 0.5)"
			cuts["iso_1"] = "(iso_1 < 0.1)"
			cuts["iso_2"] = "(byMediumCombinedIsolationDeltaBetaCorr3Hits_2 > 0.5)"
		elif channel == "et":
			cuts["mt"] = "(mt_1<40.0)"
			cuts["not2prong"] = "((decayMode_2<5)||(decayMode_2>6))"
			cuts["anti_e_tau_discriminators"] = "(againstElectronTightMVA5_2 > 0.5)"
			cuts["anti_mu_tau_discriminators"] = "(againstMuonLoose3_2 > 0.5)"
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
			cuts["dilepton_veto"] = "(dilepton_veto < 0.5)"
			cuts["iso_1"] = "(iso_1 < 0.1)"
			cuts["iso_2"] = "(byMediumCombinedIsolationDeltaBetaCorr3Hits_2 > 0.5)"
		elif channel == "tt":
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
			cuts["anti_e_tau_discriminators"] = "(againstElectronVLooseMVA5_1 > 0.5)*(againstElectronVLooseMVA5_2 > 0.5)"
			cuts["anti_mu_tau_discriminators"] = "(againstMuonLoose3_1 > 0.5)*(againstMuonLoose3_2 > 0.5)"
			cuts["iso_1"] = "(byTightCombinedIsolationDeltaBetaCorr3Hits_1 > 0.5)"
			cuts["iso_2"] = "(byTightCombinedIsolationDeltaBetaCorr3Hits_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antieloosepass(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			#cuts["zpeak"] = "(m_vis > 60.0)*(m_vis < 120.0)"
			cuts["discriminator"] = "(againstElectronLooseMVA5_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antieloosefail(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			#cuts["zpeak"] = "(m_vis > 60.0)*(m_vis < 120.0)"
			cuts["discriminator"] = "(againstElectronLooseMVA5_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def tauidpass(channel, cut_type):
		if channel == "mt":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["discriminator"] = "(byMediumCombinedIsolationDeltaBetaCorr3Hits_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def tauidfail(channel, cut_type):
		if channel == "mt":
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
		elif cut_type=="antieloosepass":
			cuts = CutStringsDict.antieloosepass(channel, cut_type)
		elif cut_type=="antieloosefail":
			cuts = CutStringsDict.antieloosefail(channel, cut_type)
		elif cut_type=="tauidpass":
			cuts = CutStringsDict.tauidpass(channel, cut_type)
		elif cut_type=="tauidfail":
			cuts = CutStringsDict.tauidfail(channel, cut_type)
		else:
			log.fatal("No cut dictionary implemented for \"%s\"!" % cut_type)
			sys.exit(1)
		return cuts