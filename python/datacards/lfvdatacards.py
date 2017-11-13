# -*- coding: utf-8 -*-
import logging
import Artus.Utility.logger as logger
import Artus.Utility.tools as tools
log = logging.getLogger(__name__)

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.categories as Categories
import HiggsAnalysis.KITHiggsToTauTau.datacards.datacards as datacards
import CombineHarvester.CombineTools.ch as ch



class LFVDatacards(datacards.Datacards):
	def __init__(self, higgs_masses=["125"], useRateParam=False, year="", cb=None, signal_processes= []):
		super(LFVDatacards, self).__init__(cb)
		
		if cb is None:
			background_processes_mt = ["ZTT", "ZL", "ZJ", "EWKZ", "TTT", "TTJJ", "VV", "W", "QCD"]
			background_processes_et = ["ZTT", "ZL", "ZJ", "EWKZ", "TTT", "TTJJ", "VV", "W", "QCD"]
			background_processes_tt = ["ZTT", "ZL", "ZJ", "EWKZ", "TTT", "TTJJ", "VVT", "VVJ", "W", "QCD"]
			background_processes_em = ["ZTT", "ZLL", "EWKZ", "TT", "VV", "hww_gg125", "hww_qq125", "W", "QCD"]
			background_processes_mm = ["ZLL", "TT", "VV", "W"]
			background_processes_ttbar = ["ZTT", "ZLL", "EWKZ", "TT", "VV", "W", "QCD"]

			all_mc_bkgs = ["ZTT", "ZL", "ZJ", "ZLL", "EWKZ", "TT", "TTT", "TTJJ", "VV", "VVT", "VVJ", "W", "hww_gg125", "hww_qq125"]
			all_mc_bkgs_no_W = ["ZTT", "ZL", "ZJ", "ZLL", "EWKZ", "TT", "TTT", "TTJJ", "VV", "VVT", "VVJ", "hww_gg125", "hww_qq125"]
			all_mc_bkgs_no_TTJ = ["ZTT", "ZL", "ZJ", "ZLL", "EWKZ", "TT", "TTT", "VV", "VVT", "VVJ", "W", "hww_gg125", "hww_qq125"]

			# ======================================================================
			# MT channel
			self.add_processes(
					channel="mt",
					categories=Categories.CategoriesDict().getCategories(["mt"])["mt"],
					bkg_processes=background_processes_mt,
					sig_processes=signal_processes,
					analysis=["LFV"],
					era=["13TeV"],
					mass=higgs_masses
					
					
			)
			
			#efficencies
			self.cb.cp().channel(["mt"]).process(signal_processes+all_mc_bkgs_no_W).AddSyst(self.cb, *self.trigger_efficiency2016_syst_args)
			self.cb.cp().channel(["mt"]).process(signal_processes+all_mc_bkgs_no_W).AddSyst(self.cb, *self.muon_efficiency2016_syst_args)
			self.cb.cp().channel(["mt"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *self.tau_efficiency2016_syst_args)

			

			# ======================================================================
			# ET channel
			self.add_processes(
					channel="et",
					categories=Categories.CategoriesDict().getCategories(["et"])["et"],
					bkg_processes=background_processes_et,
					sig_processes=signal_processes,
					analysis=["LFV"],
					era=["13TeV"],
					mass=higgs_masses
					
			)

			# ======================================================================
			# EM channel
			self.add_processes(
					channel="em",
					categories=Categories.CategoriesDict().getCategories(["em"])["em"],
					bkg_processes=background_processes_em,
					sig_processes=signal_processes,
					analysis=["LFV"],
					era=["13TeV"],
					mass=higgs_masses
					
			)

			# ======================================================================
			# TT channel
			self.add_processes(
					channel="tt",
					categories=Categories.CategoriesDict().getCategories(["tt"])["tt"],
					bkg_processes=background_processes_tt,
					sig_processes=signal_processes,
					analysis=["LFV"],
					era=["13TeV"],
					mass=higgs_masses
					
			)

			# ======================================================================
			# MM channel
			self.add_processes(
					channel="mm",
					categories=Categories.CategoriesDict().getCategories(["mm"])["mm"],
					bkg_processes=background_processes_mm,
					sig_processes=signal_processes,
					analysis=["LFV"],
					era=["13TeV"],
					mass=higgs_masses
					
			)

			# ======================================================================
			# ttbar "channel" to extract normalization of ttbar process
			self.add_processes(
					channel="ttbar",
					categories=Categories.CategoriesDict().getCategories(["ttbar"])["ttbar"],
					bkg_processes=background_processes_ttbar,
					sig_processes=signal_processes,
					analysis=["LFV"],
					era=["13TeV"],
					mass=higgs_masses
			)

			if log.isEnabledFor(logging.DEBUG):
				self.cb.PrintAll()


	
