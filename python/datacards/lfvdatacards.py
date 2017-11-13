# -*- coding: utf-8 -*-
import logging
import Artus.Utility.logger as logger
import Artus.Utility.tools as tools
log = logging.getLogger(__name__)

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.categories as Categories
import HiggsAnalysis.KITHiggsToTauTau.datacards.datacards as datacards
import CombineHarvester.CombineTools.ch as ch



class LFVDatacards(datacards.Datacards):
	def __init__(self, higgs_masses=["125"], useRateParam=False, year="", cb=None, signal_processes= [], categories = []):
		super(LFVDatacards, self).__init__(cb)
		
		print Categories.CategoriesDict().getCategories(["em"])["em"]
		if cb is None:
			background_processes_mt = ["ZTT", "ZL", "ZJ", "EWKZ", "TTT", "TTJJ", "VV", "W", "QCD"]
			background_processes_et = ["ZTT", "ZL", "ZJ", "EWKZ", "TTT", "TTJJ", "VV", "W", "QCD"]
			background_processes_em = ["ZTT", "ZLL", "EWKZ", "TT", "VV", "hww_gg125", "hww_qq125", "W", "QCD"]

			all_mc_bkgs = ["ZTT", "ZL", "ZJ", "ZLL", "EWKZ", "TT", "TTT", "TTJJ", "VV", "VVT", "VVJ", "W", "hww_gg125", "hww_qq125"]
			all_mc_bkgs_no_W = ["ZTT", "ZL", "ZJ", "ZLL", "EWKZ", "TT", "TTT", "TTJJ", "VV", "VVT", "VVJ", "hww_gg125", "hww_qq125"]
			all_mc_bkgs_no_TTJ = ["ZTT", "ZL", "ZJ", "ZLL", "EWKZ", "TT", "TTT", "VV", "VVT", "VVJ", "W", "hww_gg125", "hww_qq125"]

			# ===========================Channels===========================================
			# MT channel
			self.add_processes(
					channel="mt",
					categories=categories,
					bkg_processes=background_processes_mt,
					sig_processes=signal_processes,
					analysis=["LFV"],
					era=["13TeV"],
					mass=higgs_masses
					
					
			)

			# ET channel
			self.add_processes(
					channel="et",
					categories=categories,
					bkg_processes=background_processes_et,
					sig_processes=signal_processes,
					analysis=["LFV"],
					era=["13TeV"],
					mass=higgs_masses
					
			)

			# EM channel
			self.add_processes(
					channel="em",
					categories=categories,
					bkg_processes=background_processes_em,
					sig_processes=signal_processes,
					analysis=["LFV"],
					era=["13TeV"],
					mass=higgs_masses
					
			)


			# ttbar "channel" to extract normalization of ttbar process
			self.add_processes(
					channel="ttbar",
					categories=categories,
					bkg_processes=background_processes_ttbar,
					sig_processes=signal_processes,
					analysis=["LFV"],
					era=["13TeV"],
					mass=higgs_masses
			)
			
			# =============================Uncertanties=========================================
			# Efficiencies
			
			self.cb.cp().channel(["em"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *self.trigger_efficiency2016_em_syst_args)
			self.cb.cp().channel(["em"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *self.electron_efficiency2016_syst_args)
			self.cb.cp().channel(["em"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *self.muon_efficiency2016_syst_args)

			self.cb.cp().channel(["et"]).process(signal_processes+all_mc_bkgs_no_W).AddSyst(self.cb, *self.trigger_efficiency2016_syst_args)
			self.cb.cp().channel(["et"]).process(signal_processes+all_mc_bkgs_no_W).AddSyst(self.cb, *self.electron_efficiency2016_syst_args)
			self.cb.cp().channel(["et"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *self.tau_efficiency2016_syst_args)

			self.cb.cp().channel(["mt"]).process(signal_processes+all_mc_bkgs_no_W).AddSyst(self.cb, *self.trigger_efficiency2016_syst_args)
			self.cb.cp().channel(["mt"]).process(signal_processes+all_mc_bkgs_no_W).AddSyst(self.cb, *self.muon_efficiency2016_syst_args)
			self.cb.cp().channel(["mt"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *self.tau_efficiency2016_syst_args)


			#fake ES

			

			

			if log.isEnabledFor(logging.DEBUG):
				self.cb.PrintAll()


	
