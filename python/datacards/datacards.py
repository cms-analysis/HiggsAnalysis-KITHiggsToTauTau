# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy
import os
import re

# http://cms-analysis.github.io/HiggsAnalysis-HiggsToTauTau/python-interface.html
import combineharvester as ch

import Artus.Utility.tools as tools
import Artus.Utility.jsonTools as jsonTools
import Artus.HarryPlotter.utility.roottools as roottools
import Artus.HarryPlotter.utility.tfilecontextmanager as tfilecontextmanager

import HiggsAnalysis.KITHiggsToTauTau.datacards.datacardconfigs as datacardconfigs
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot


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
	
	log.debug(command)
	logger.subprocessCall(command, shell=True)
	
	if not cwd is None:
		os.chdir(old_cwd)


class Datacards(object):
	def __init__(self, cb=None):
		super(Datacards, self).__init__()
		
		self.cb = cb
		if self.cb is None:
			self.cb = ch.CombineHarvester()
		if log.isEnabledFor(logging.DEBUG):
			self.cb.SetVerbosity(1)
		
		self.configs = datacardconfigs.DatacardConfigs()
		
		# common systematics
		self.lumi_syst_args = [
			"lumi_$ERA",
			"lnN",
			ch.SystMap("era")
				(["7TeV", "8TeV"], 1.026)
				(       ["13TeV"], 1.10)
		]
		self.electron_efficieny_syst_args = [
			"CMS_eff_e",
			"lnN",
			ch.SystMap("era")
				(["7TeV", "8TeV"], 1.02)
				(       ["13TeV"], 1.02) # copied from 8TeV
		]
		self.muon_efficieny_syst_args = [
			"CMS_eff_m",
			"lnN",
			ch.SystMap("era")
				(["7TeV", "8TeV"], 1.02)
				(       ["13TeV"], 1.02) # copied from 8TeV
		]
		self.tau_efficieny_syst_args = [
			"CMS_eff_t_$CHANNEL_$ERA",
			"lnN",
			ch.SystMap("era", "channel")
				(["7TeV", "8TeV"], ["mt", "et"], 1.08)
				(["7TeV", "8TeV"], ["tt"],       1.19)
				(       ["13TeV"], ["mt", "et"], 1.08) # copied from 8TeV
				(       ["13TeV"], ["tt"],       1.19) # copied from 8TeV
		]
		self.btag_efficieny_syst_args = [
			"CMS_eff_b_$ERA",
			"lnN",
			ch.SystMap("era", "channel")
				(["13TeV"], ["mt"], 0.96) # copied from 8TeV
				(["13TeV"], ["et"], 0.96) # copied from 8TeV
				(["13TeV"], ["em"], 0.93) # copied from 8TeV
				(["13TeV"], ["tt"], 0.93) # copied from 8TeV
		]
		self.met_scale_syst_args = [
			"CMS_$ANALYSIS_scale_met_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(["13TeV"], ["ggH", "qqH", "WH", "ZH"], 0.98) # copied from 8TeV
				(["13TeV"], ["ZTT", "ZLL", "TTJ", "VV", "WJ"], 1.03) # copied from 8TeV
		]
		
		self.ztt_cross_section_syst_args = [
			"CMS_$ANALYSIS_zttNorm_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(["7TeV", "8TeV"], ["ZTT", "ZLL", "ZL", "ZJ"], 1.03)
				(       ["13TeV"], ["ZTT", "ZLL"], 1.03)
		]
		self.ttj_cross_section_syst_args = [
			"CMS_$ANALYSIS_ttjNorm_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				( ["7TeV"], ["TTJ"], 1.08)
				( ["8TeV"], ["TTJ"], 1.1)
				(["13TeV"], ["TTJ"], 1.1) # copied from 8TeV
		]
		self.vv_cross_section_syst_args = [
			"CMS_$ANALYSIS_vvNorm_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(["7TeV", "8TeV"], ["VV"], 1.15)
				(       ["13TeV"], ["VV"], 1.15) # copied from 8TeV
		]
		self.wj_cross_section_syst_args = [
			"CMS_$ANALYSIS_wjNorm_$CHANNEL_$ERA",
			"lnN",
			ch.SystMap("era", "process", "channel")
				(["7TeV", "8TeV"], ["WJ"], ["mt", "et"], 1.2)
				(       ["13TeV"], ["WJ"], ["mt", "et"], 1.2) # copied from 8TeV
		]
		
		self.qcd_syst_args = [
			"CMS_$ANALYSIS_qcdSyst_$BIN_$ERA",
			"lnN",
			ch.SystMap("era", "process", "bin")
				(["13TeV"], ["QCD"], ["mt_inclusive", "et_inclusive"], 1.06) # copied from 8TeV
				
				(["13TeV"], ["QCD"], ["mt_0jet_high"], 1.1) # copied from 8TeV
				(["13TeV"], ["QCD"], ["mt_0jet_low"], 1.1) # copied from 8TeV
				(["13TeV"], ["QCD"], ["mt_1jet_high"], 1.1) # copied from 8TeV
				(["13TeV"], ["QCD"], ["mt_1jet_low"], 1.1) # copied from 8TeV
				(["13TeV"], ["QCD"], ["mt_2jet_vbf"], 1.3) # copied from 8TeV
				
				(["13TeV"], ["QCD"], ["et_0jet_high"], 1.06) # copied from 8TeV
				(["13TeV"], ["QCD"], ["et_0jet_low"], 1.06) # copied from 8TeV
				(["13TeV"], ["QCD"], ["et_1jet_high"], 1.1) # copied from 8TeV
				(["13TeV"], ["QCD"], ["et_1jet_low"], 1.1) # copied from 8TeV
				(["13TeV"], ["QCD"], ["et_2jet_vbf"], 1.3) # copied from 8TeV
				
				(["13TeV"], ["QCD"], ["tt_inclusive"], 1.35) # copied from 8TeV
		]
		self.zllFakeTau_syst_args = [
			"CMS_$ANALYSIS_zllFakeTau_$CHANNEL_$ERA",
			"lnN",
			ch.SystMap("era", "process", "channel")
				(["7TeV", "8TeV"], ["ZLL"], ["mt", "et"], 1.30)
				(       ["13TeV"], ["ZLL"], ["mt", "et"], 1.30) # copied from 8TeV
		]
		
		self.jec_syst_args = [
			"CMS_scale_j_$ERA",
			"shape",
			ch.SystMap("era")
				(["13TeV"], 1.0)
		]
		self.tau_es_syst_args = [
			"CMS_scale_t_$CHANNEL_$ERA",
			"shape",
			ch.SystMap("era", "channel")
				(["13TeV"], ["mt"], 1.0)
				(["13TeV"], ["et"], 1.0)
				(["13TeV"], ["tt"], 1.0)
		]
		
		# https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV#s_13_0_TeV
		self.htt_qcd_scale_syst_args = [
			"QCD_scale_$PROCESS",
			"lnN",
			ch.SystMap("era", "process")
				(["13TeV"], ["ggH"], 1.079)
				(["13TeV"], ["qqH"], 1.007)
				(["13TeV"], ["WH"], 1.015)
				(["13TeV"], ["ZH"], 1.038)
		]
		self.htt_pdf_scale_syst_args = [
			"PDF_scale_$PROCESS",
			"lnN",
			ch.SystMap("era", "process")
				(["13TeV"], ["ggH"], 1.071)
				(["13TeV"], ["qqH"], 1.032)
				(["13TeV"], ["WH"], 1.022)
				(["13TeV"], ["ZH"], 1.022)
		]
		
		# CMS AN-13-262 (v8, table 3)
		self.htt_ueps_syst_args = [
			"UEPS",
			"lnN",
			ch.SystMap("era", "process", "bin")
				(["13TeV"], ["ggH"], ["mt_0jet_high"], 1.060) # copied from 8TeV
				(["13TeV"], ["ggH"], ["mt_0jet_low"], 1.073) # copied from 8TeV
				(["13TeV"], ["ggH"], ["mt_1jet_high"], 0.996) # copied from 8TeV
				(["13TeV"], ["ggH"], ["mt_1jet_low"], 1.007) # copied from 8TeV
				(["13TeV"], ["ggH"], ["mt_2jet_vbf"], 0.988) # copied from 8TeV
				
				(["13TeV"], ["ggH"], ["et_0jet_high"], 1.060) # copied from 8TeV
				(["13TeV"], ["ggH"], ["et_0jet_low"], 1.073) # copied from 8TeV
				(["13TeV"], ["ggH"], ["et_1jet_high"], 0.996) # copied from 8TeV
				(["13TeV"], ["ggH"], ["et_1jet_low"], 1.007) # copied from 8TeV
				(["13TeV"], ["ggH"], ["et_2jet_vbf"], 0.988) # copied from 8TeV
				
				(["13TeV"], ["ggH"], ["em_0jet_high"], 1.063) # copied from 8TeV
				(["13TeV"], ["ggH"], ["em_0jet_low"], 1.089) # copied from 8TeV
				(["13TeV"], ["ggH"], ["em_1jet_high"], 1.004) # copied from 8TeV
				(["13TeV"], ["ggH"], ["em_1jet_low"], 1.000) # copied from 8TeV
				(["13TeV"], ["ggH"], ["em_2jet_vbf"], 0.988) # copied from 8TeV
				
				(["13TeV"], ["ggH"], ["tt_inclusive"], 1.025) # copied from 8TeV
				
				(["13TeV"], ["qqH", "WH", "ZH"], ["mt_0jet_high"], 1.028) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH"], ["mt_0jet_low"], 1.018) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH"], ["mt_1jet_high"], 0.954) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH"], ["mt_1jet_low"], 0.946) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH"], ["mt_2jet_vbf"], 0.893) # copied from 8TeV
				
				(["13TeV"], ["qqH", "WH", "ZH"], ["et_0jet_high"], 1.028) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH"], ["et_0jet_low"], 1.018) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH"], ["et_1jet_high"], 0.954) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH"], ["et_1jet_low"], 0.946) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH"], ["et_2jet_vbf"], 0.893) # copied from 8TeV
				
				(["13TeV"], ["qqH", "WH", "ZH"], ["em_0jet_high"], 1.042) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH"], ["em_0jet_low"], 1.035) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH"], ["em_1jet_high"], 0.978) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH"], ["em_1jet_low"], 0.984) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH"], ["em_2jet_vbf"], 0.893) # copied from 8TeV
				
				(["13TeV"], ["qqH", "WH", "ZH"], ["tt_inclusive"], 1.025) # copied from 8TeV
		]
	
	def add_processes(self, channel, categories, bkg_processes, sig_processes=["ztt"], *args, **kwargs):
		bin = [(self.configs.category2binid(category, channel), category) for category in categories]
		
		for key in ["channel", "procs", "bin", "signal"]:
			if key in kwargs:
				kwargs.pop(key)
		
		non_sig_kwargs = copy.deepcopy(kwargs)
		if "mass" in non_sig_kwargs:
			non_sig_kwargs.pop("mass")
		
		self.cb.AddObservations(channel=[channel], mass=["*"], bin=bin, *args, **non_sig_kwargs)
		self.cb.AddProcesses(channel=[channel], mass=["*"], procs=bkg_processes, bin=bin, signal=False, *args, **non_sig_kwargs)
		self.cb.AddProcesses(channel=[channel], procs=sig_processes, bin=bin, signal=True, *args, **kwargs)
	
	def get_samples_per_shape_systematic(self):
		samples_per_shape_systematic = {}
		samples_per_shape_systematic["nominal"] = self.cb.process_set()
		for shape_systematic in self.cb.cp().syst_type(["shape"]).syst_name_set():
			samples_per_shape_systematic[shape_systematic] = self.cb.cp().syst_type(["shape"]).syst_name([shape_systematic]).SetFromSysts(ch.Systematic.process)
		return samples_per_shape_systematic
	
	def extract_shapes(self, root_filename_template,
	                   bkg_histogram_name_template, sig_histogram_name_template,
	                   bkg_syst_histogram_name_template, sig_syst_histogram_name_template,
	                   update_systematics=False):
		for analysis in self.cb.analysis_set():
			for era in self.cb.cp().analysis([analysis]).era_set():
				for channel in self.cb.cp().analysis([analysis]).era([era]).channel_set():
					for category in self.cb.cp().analysis([analysis]).era([era]).channel([channel]).bin_set():
						root_filename = root_filename_template.format(
								ANALYSIS=analysis,
								CHANNEL=channel,
								BIN=category,
								ERA=era
						)
						
						cb_backgrounds = self.cb.cp().analysis([analysis]).era([era]).channel([channel]).bin([category]).backgrounds()
						cb_backgrounds.ExtractShapes(
								root_filename,
								bkg_histogram_name_template.replace("{", "").replace("}", ""),
								bkg_syst_histogram_name_template.replace("{", "").replace("}", "")
						)
						
						cb_signals = self.cb.cp().analysis([analysis]).era([era]).channel([channel]).bin([category]).signals()
						cb_signals.ExtractShapes(
								root_filename,
								sig_histogram_name_template.replace("{", "").replace("}", ""),
								sig_syst_histogram_name_template.replace("{", "").replace("}", "")
						)
						
						# update/add systematics related to the estimation of backgrounds/signals
						# these uncertainties are stored in the input root files
						if update_systematics:
							with tfilecontextmanager.TFileContextManager(root_filename, "READ") as root_file:
								root_object_paths = [path for key, path in roottools.RootTools.walk_root_directory(root_file)]
								
								processes_histogram_names = []
								for process in cb_backgrounds.process_set():
									bkg_histogram_name = bkg_histogram_name_template.replace("$", "").format(
											ANALYSIS=analysis,
											CHANNEL=channel,
											BIN=category,
											ERA=era,
											PROCESS=process
									)
									yield_unc_rel = Datacards.get_yield_unc_rel(bkg_histogram_name, root_file, root_object_paths)
									if (not yield_unc_rel is None) and (yield_unc_rel != 0.0):
										cb_backgrounds.cp().process([process]).AddSyst(
												self.cb,
												"CMS_$ANALYSIS_$PROCESS_estimation_$ERA",
												"lnN",
												ch.SystMap("process")([process], 1.0+yield_unc_rel)
										)
								
								for process in cb_signals.process_set():
									for mass in cb_signals.mass_set():
										if mass != "*":
											sig_histogram_name = sig_histogram_name_template.replace("$", "").format(
													ANALYSIS=analysis,
													CHANNEL=channel,
													BIN=category,
													ERA=era,
													PROCESS=process,
													MASS=mass
											)
											yield_unc_rel = Datacards.get_yield_unc_rel(sig_histogram_name, root_file, root_object_paths)
											if (not yield_unc_rel is None) and (yield_unc_rel != 0.0):
												cb_backgrounds.cp().process([process]).mass([mass]).AddSyst(
														self.cb,
														"CMS_$ANALYSIS_$PROCESS$MASS_estimation_$ERA",
														"lnN",
														ch.SystMap("process", "mass")([process], [mass], 1.0+yield_unc_rel)
												)
		
		if log.isEnabledFor(logging.DEBUG):
			self.cb.PrintAll()
	
	@staticmethod
	def get_yield_unc_rel(histogram_path, root_file, root_object_paths):
		metadata_path = histogram_path+"_metadata"
		if metadata_path in root_object_paths:
			metadata = jsonTools.JsonDict(root_file.Get(metadata_path).GetString().Data())
			return metadata.get("yield_unc_rel", None)
		else:
			return None
	
	def add_bin_by_bin_uncertainties(self, processes, add_threshold=0.1, merge_threshold=0.5, fix_norm=True):
		bin_by_bin_factory = ch.BinByBinFactory()
		if log.isEnabledFor(logging.DEBUG):
			bin_by_bin_factory.SetVerbosity(100)
		
		bin_by_bin_factory.SetAddThreshold(add_threshold)
		bin_by_bin_factory.SetMergeThreshold(merge_threshold)
		bin_by_bin_factory.SetFixNorm(fix_norm)
		
		bin_by_bin_factory.MergeBinErrors(self.cb.cp().process(processes))
		bin_by_bin_factory.AddBinByBin(self.cb.cp().process(processes), self.cb)
		#ch.SetStandardBinNames(self.cb) # TODO: this line seems to mix up the categories
	
	def remove_systematics(self):
		def remove(systematic):
			systematic.set_type("lnN")
			systematic.set_value_u(0.0)
			systematic.set_value_d(0.0)
		
		self.cb.ForEachSyst(remove)
	
	def scale_expectation(self, scale_factor):
		self.cb.cp().backgrounds().ForEachProc(lambda process: process.set_rate(process.rate() * scale_factor))
		self.cb.cp().signals().ForEachProc(lambda process: process.set_rate(process.rate() * scale_factor))
	
	def replace_observation_by_asimov_dataset(self, signal_mass):
		log.warning("Asimov data sets need to be created with combine -t -1 --expectSignal 0 [--toysFrequentist], since CH (python) does not yet support modifying of shapes!")
		def _replace_observation_by_asimov_dataset(observation):
			cb = self.cb.cp().analysis([observation.analysis()]).era([observation.era()]).channel([observation.channel()]).bin([observation.bin()])
			#observation.set_shape(cb.cp().backgrounds().GetShape() + cb.cp().signals().mass([signal_mass]).GetShape(), True)
			observation.ShapeAsTH1F = cb.cp().backgrounds().GetShape() + cb.cp().signals().mass([signal_mass]).GetShape()
			observation.set_rate(cb.cp().backgrounds().GetRate() + cb.cp().signals().mass([signal_mass]).GetRate())
		
		self.cb.cp().ForEachObs(_replace_observation_by_asimov_dataset)
	
	def write_datacards(self, datacard_filename_template, root_filename_template, output_directory="."):
		writer = ch.CardWriter(os.path.join("$TAG", datacard_filename_template),
		                       os.path.join("$TAG", root_filename_template))
		if log.isEnabledFor(logging.DEBUG):
			writer.SetVerbosity(1)
		
		return writer.WriteCards(output_directory[:-1] if output_directory.endswith("/") else output_directory, self.cb)
	
	def text2workspace(self, datacards_cbs, n_processes=1, *args):
		commands = ["text2workspace.py -m {MASS} {ARGS} {DATACARD} -o {OUTPUT}".format(
				MASS=[mass for mass in cb.mass_set() if mass != "*"][0], # TODO: maybe there are more masses?
				ARGS=" ".join(args),
				DATACARD=datacard,
				OUTPUT=os.path.splitext(datacard)[0]+".root"
		) for datacard, cb in datacards_cbs.iteritems()]
		
		tools.parallelize(_call_command, commands, n_processes=n_processes)
		
		return {datacard : os.path.splitext(datacard)[0]+".root" for datacard in datacards_cbs.keys()}
	
	def combine(self, datacards_cbs, datacards_workspaces, datacards_poi_ranges=None, n_processes=1, *args):
		if datacards_poi_ranges is None:
			datacards_poi_ranges = {}
		tmp_args = " ".join(args)
		
		chunks = [[None, None]]
		if "{CHUNK}" in tmp_args and "--points" in tmp_args:
			splited_args = tmp_args.split()
			n_points = int(splited_args[splited_args.index("--points") + 1])
			n_points_per_chunk = 199
			chunks = [[chunk*n_points_per_chunk, (chunk+1)*n_points_per_chunk-1] for chunk in xrange(n_points/n_points_per_chunk+1)]
		
		commands = []
		for index, (chunk_min, chunk_max) in enumerate(chunks):
			commands.extend([[
					"combine -m {MASS} {POI_RANGE} {ARGS} {WORKSPACE} {CHUNK_POINTS}".format(
							MASS=[mass for mass in datacards_cbs[datacard].mass_set() if mass != "*"][0], # TODO: maybe there are more masses?
							POI_RANGE="--rMin {RMIN} --rMax {RMAX}" if datacard in datacards_poi_ranges else "",
							ARGS=tmp_args.format(CHUNK=str(index)),
							WORKSPACE=workspace,
							CHUNK_POINTS = "" if (chunk_min is None) or (chunk_max is None) else "--firstPoint {CHUNK_MIN} --lastPoint {CHUNK_MAX}".format(
									CHUNK_MIN=chunk_min,
									CHUNK_MAX=chunk_max
							)
					).format(RMIN=datacards_poi_ranges.get(datacard, ["", ""])[0], RMAX=datacards_poi_ranges.get(datacard, ["", ""])[1]),
					os.path.dirname(workspace)
			] for datacard, workspace in datacards_workspaces.iteritems()])
		
		tools.parallelize(_call_command, commands, n_processes=n_processes)
	
	def annotate_trees(self, datacards_workspaces, root_filename, value_regex, value_replacements=None, n_processes=1, *args):
		if value_replacements is None:
			value_replacements = {}
		
		commands = []
		for datacard, workspace in datacards_workspaces.iteritems():
			search_result = re.search(value_regex, workspace)
			if not search_result is None:
				value = search_result.groups()[0]
				float_value = float(value_replacements.get(value, value))
				
				commands.append("annotate-trees.py {FILES} --values {VALUE} {ARGS}".format(
						FILES=os.path.join(os.path.dirname(workspace), root_filename),
						VALUE=float_value,
						ARGS=" ".join(args)
				))
		
		tools.parallelize(_call_command, commands, n_processes=n_processes)
	
	def postfit_shapes(self, datacards_cbs, s_fit_only=False, n_processes=1, *args):
		commands = []
		datacards_postfit_shapes = {}
		fit_type_list = ["fit_s", "fit_b"]
		if s_fit_only:
			fit_type_list.remove("fit_b")

		for fit_type in fit_type_list:
			commands.extend(["PostFitShapes --postfit -d {DATACARD} -o {OUTPUT} -m {MASS} -f {FIT_RESULT} {ARGS}".format(
					DATACARD=datacard,
					OUTPUT=os.path.splitext(datacard)[0]+"_"+fit_type+".root",
					MASS=[mass for mass in cb.mass_set() if mass != "*"][0], # TODO: maybe there are more masses?
					FIT_RESULT=os.path.join(os.path.dirname(datacard), "mlfit.root:"+fit_type),
					ARGS=" ".join(args)
			) for datacard, cb in datacards_cbs.iteritems()])
			
			datacards_postfit_shapes.setdefault(fit_type, {}).update({
					datacard : os.path.splitext(datacard)[0]+"_"+fit_type+".root"
			for datacard, cb in datacards_cbs.iteritems()})
		
		tools.parallelize(_call_command, commands, n_processes=n_processes)
		
		return datacards_postfit_shapes
	
	def prefit_postfit_plots(self, datacards_cbs, datacards_postfit_shapes, plotting_args=None, n_processes=1, *args):
		if plotting_args is None:
			plotting_args = {}
		
		plot_configs = []
		bkg_plotting_order = ["ZTT", "ZLL", "TTJ", "VV", "WJ", "QCD"]
		for level in ["prefit", "postfit"]:
			for index, (fit_type, datacards_postfit_shapes_dict) in enumerate(datacards_postfit_shapes.iteritems()):
				if (index == 0) or (level == "postfit"):
					for datacard, postfit_shapes in datacards_postfit_shapes_dict.iteritems():
						for category in datacards_cbs[datacard].cp().bin_set():
							bkg_processes = datacards_cbs[datacard].cp().bin([category]).backgrounds().process_set()
							bkg_processes.sort(key=lambda process: bkg_plotting_order.index(process) if process in bkg_plotting_order else len(bkg_plotting_order))
							
							config = {}
							config["files"] = [postfit_shapes]
							config["folders"] = [category+"_"+level]
							config["x_expressions"] = ["TotalSig"] + bkg_processes + ["TotalBkg", "data_obs"]
							config["nicks"] = ["TotalSig"] + bkg_processes + ["TotalBkg", "data_obs"]
							config["stacks"] = ["sig_bkg"] + (["sig_bkg"]*len(bkg_processes)) + ["bkg_unc", "data"]
							
							config["labels"] = [label.lower() for label in ["TotalSig"] + bkg_processes + ["TotalBkg", "data_obs"]]
							config["colors"] = [color.lower() for color in ["TotalSig"] + bkg_processes + ["TotalBkg", "data_obs"]]
							config["markers"] = ["LINE"] + (["HIST"]*len(bkg_processes)) + ["E2", "E"]
							config["legend_markers"] = ["L"] + (["F"]*len(bkg_processes)) + ["F", "ELP"]
							
							config["rel_y_lims"] = [0.0, 1.4]
							config["legend"] = [0.23, 0.73, 0.9, 0.89]
							config["legend_cols"] = 3
							
							config["title"] = "channel_"+(category.split("_")[0])
							
							config["output_dir"] = os.path.join(os.path.dirname(datacard), "plots")
							config["filename"] = level+("_"+fit_type if level == "postfit" else "")+"_"+category
							
							if not "NormalizeByBinWidth" in config.get("analysis_modules", []):
								config.setdefault("analysis_modules", []).append("NormalizeByBinWidth")
							config["y_label"] = "Entries / bin"
							
							if plotting_args.get("ratio", False):
								if not "Ratio" in config.get("analysis_modules", []):
									config.setdefault("analysis_modules", []).append("Ratio")
								config.setdefault("ratio_numerator_nicks", []).extend(["noplot_TotalBkg", "noplot_TotalBkg TotalSig", "data_obs"])
								config.setdefault("ratio_denominator_nicks", []).extend(["noplot_TotalBkg"] * 3)
								config.setdefault("ratio_result_nicks", []).extend(["ratio_unc", "ratio_sig", "ratio"])
								config.setdefault("colors", []).extend(["totalbkg", "totalsig", "#000000"])
								config.setdefault("markers", []).extend(["E2", "LINE", "E"])
								config.setdefault("legend_markers", []).extend(["F", "L", "ELP"])
								config.setdefault("labels", []).extend([""] * 3)
								config["legend"] = [0.7, 0.5, 0.95, 0.92]
							
							plot_configs.append(config)
		
		# create result plots HarryPlotter
		return higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[plotting_args.get("args", "")], n_processes=n_processes)

	def print_pulls(self, datacards_cbs, n_processes=1, *args):
		commands = []
		for pulls_format, file_format in zip(["latex", "text"], ["tex", "txt"]):
			for all_nuissances in [False, True]:
				commands.extend([[
						"execute-command.py \"python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -f {FORMAT} {ALL} {PLOT} {ARGS} {FIT_RESULT}\" --log-file {LOG_FILE}".format(
								FORMAT=pulls_format,
								ALL=("-a" if all_nuissances else ""),
								PLOT="-g "+("" if all_nuissances else "largest_")+"pulls.root",
								ARGS=" ".join(args),
								FIT_RESULT=os.path.join(os.path.dirname(datacard), "mlfit.root"),
								LOG_FILE=("" if all_nuissances else "largest_")+"pulls."+file_format
						),
						os.path.dirname(datacard)
				] for datacard in datacards_cbs.keys()])
		
		tools.parallelize(_call_command, commands, n_processes=n_processes)

	def pull_plots(self, datacards_postfit_shapes, s_fit_only=False, plotting_args=None, n_processes=1):
		if plotting_args is None:
			plotting_args = {}
		
		plot_configs = []
		for index, (fit_type, datacards_postfit_shapes_dict) in enumerate(datacards_postfit_shapes.iteritems()):
			if (index == 0):
				for datacard, postfit_shapes in datacards_postfit_shapes_dict.iteritems():

					config = {}
					config["files"] = [os.path.join(os.path.dirname(datacard), "mlfit.root")]
					config["input_modules"] = ["InputRootSimple"]
					config["root_names"] = ["fit_s", "fit_b", "nuisances_prefit"]
					if s_fit_only:
						config["root_names"] = ["fit_s", "nuisances_prefit"]
						config["fit_s_only"] = [True]
					config["analysis_modules"] = ["ComputePullValues"]
					config["nicks_blacklist"] = ["graph_b"]
					config["fit_poi"] = plotting_args.get("fit_poi", "r")

					config["left_pad_margin"] = [0.40]
					config["labels"] = ["prefit", "S+B model"]
					config["markers"] = ["L2", "P"]
					config["fill_styles"] = [3001, 0]
					config["legend"] = [0.75, 0.8]
					config["legend_markers"] = ["LF", "LP"]
					config["x_lims"] = [-5.0, 5.0]
					config["x_label"] = "Pull values"

					config["output_dir"] = os.path.join(os.path.dirname(datacard), "plots")
					config["filename"] = "pulls"

					plot_configs.append(config)

		# create result plots HarryPlotter
		return higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[plotting_args.get("args", "")], n_processes=n_processes)
