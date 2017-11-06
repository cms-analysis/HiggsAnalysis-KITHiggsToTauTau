# -*- coding: utf-8 -*-
import os
import logging
import Artus.Utility.logger as logger
import Artus.Utility.tools as tools
log = logging.getLogger(__name__)

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.categories as Categories
import HiggsAnalysis.KITHiggsToTauTau.datacards.datacards as datacards
import CombineHarvester.CombineTools.ch as ch

def _call_command(args):
	command = None
	cwd = None
	if isinstance(args, basestring):
		command = args
	else:
		command = args[0]
		if len(args) > 1:
			cwd = args[1]

	old_cwd = None
	if not cwd is None:
		old_cwd = os.getcwd()
		os.chdir(cwd)
	print command
	#log.debug(command)
	logger.subprocessCall(command, shell=True)

	if not cwd is None:
		os.chdir(old_cwd)



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

			# ======================================================================
			# MT channel
			self.add_processes(
					channel="mt",
					categories=Categories.CategoriesDict().getCategories(["mt"])["mt"],
					bkg_processes=background_processes_mt,
					sig_processes=signal_processes,
					analysis=["LFV"],
					era=["13TeV"],
					
			)

			# ======================================================================
			# ET channel
			self.add_processes(
					channel="et",
					categories=Categories.CategoriesDict().getCategories(["et"])["et"],
					bkg_processes=background_processes_et,
					sig_processes=signal_processes,
					analysis=["LFV"],
					era=["13TeV"],
					
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
			)

			if log.isEnabledFor(logging.DEBUG):
				self.cb.PrintAll()


	def texttoworkspace(self, datacards_cbs, n_processes=1, *args):
		commands = ["text2workspace.py -m {MASS} {ARGS} {DATACARD} -o {OUTPUT}".format(
				MASS="125",
				ARGS=" ".join(args),
				DATACARD=datacard,
				OUTPUT=os.path.splitext(datacard)[0]+".root"
		) for datacard, cb in datacards_cbs.iteritems()]

		tools.parallelize(_call_command, commands, n_processes=n_processes, description="text2workspace.py")

		return {datacard : os.path.splitext(datacard)[0]+".root" for datacard in datacards_cbs.keys()}
	
