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
				(       ["13TeV"], 1.026) # copied from 8TeV
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
			ch.SystMap("era")
				(["7TeV", "8TeV"], 1.08)
				(       ["13TeV"], 1.08) # copied from 8TeV
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
			"CMS_$ANALYSIS_wjNorm_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(["7TeV", "8TeV"], ["WJ"], 1.2)
				(       ["13TeV"], ["WJ"], 1.2) # copied from 8TeV
		]
		self.jec_syst_args = [
			"CMS_scale_j_$ERA",
			"shape",
			ch.SystMap("era")
				(["13TeV"], 1.0)
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
	                   bkg_syst_histogram_name_template, sig_syst_histogram_name_template):
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
						self.cb.cp().analysis([analysis]).era([era]).channel([channel]).bin([category]).backgrounds().ExtractShapes(root_filename, bkg_histogram_name_template, bkg_syst_histogram_name_template)
						self.cb.cp().analysis([analysis]).era([era]).channel([channel]).bin([category]).signals().ExtractShapes(root_filename, sig_histogram_name_template, sig_syst_histogram_name_template)
		
		if log.isEnabledFor(logging.DEBUG):
			self.cb.PrintAll()
	
	def add_bin_by_bin_uncertainties(self, processes, add_threshold=0.1, merge_threshold=0.5, fix_norm=True):
		bin_by_bin_factory = ch.BinByBinFactory()
		if log.isEnabledFor(logging.DEBUG):
			bin_by_bin_factory.SetVerbosity(1)
		
		bin_by_bin_factory.SetAddThreshold(add_threshold)
		bin_by_bin_factory.SetMergeThreshold(merge_threshold)
		bin_by_bin_factory.SetFixNorm(fix_norm)
		
		bin_by_bin_factory.AddBinByBin(self.cb.cp().process(processes), self.cb)
		ch.SetStandardBinNames(self.cb)
	
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
	
	def combine(self, datacards_cbs, datacards_workspaces, n_processes=1, *args):
		commands = [[
				"combine -m {MASS} {ARGS} {WORKSPACE}".format(
						MASS=[mass for mass in datacards_cbs[datacard].mass_set() if mass != "*"][0], # TODO: maybe there are more masses?
						ARGS=" ".join(args),
						WORKSPACE=workspace
				),
				os.path.dirname(workspace)
		] for datacard, workspace in datacards_workspaces.iteritems()]
		
		tools.parallelize(_call_command, commands, n_processes=n_processes)
	
	def annotate_trees(self, datacards_workspaces, root_filename, value_regex, n_processes=1, *args):
		commands = ["annotate-trees.py {FILES} --values {VALUE} {ARGS}".format(
				FILES=os.path.join(os.path.dirname(workspace), root_filename),
				VALUE=float(re.search(value_regex, workspace).groups()[0]),
				ARGS=" ".join(args)
		) for datacard, workspace in datacards_workspaces.iteritems()]
		
		tools.parallelize(_call_command, commands, n_processes=n_processes)
	
	def postfit_shapes(self, datacards_cbs, n_processes=1, *args):
		commands = []
		datacards_postfit_shapes = {}
		for fit_type in ["fit_s", "fit_b"]:
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
							config["x_expressions"] = ["TotalSig"] + bkg_processes + ["data_obs", "TotalBkg"]
							config["nicks"] = ["TotalSig"] + bkg_processes + ["data_obs", "noplot_TotalBkg"]
							config["stacks"] = ["sig_bkg"] + (["sig_bkg"]*len(bkg_processes)) + ["data"]
							
							config["labels"] = ["totalsig"] + [label.lower() for label in bkg_processes + ["data_obs"]]
							config["colors"] = ["totalsig"] + [color.lower() for color in bkg_processes + ["data_obs"]]
							config["markers"] = ["LINE"] + (["HIST"]*len(bkg_processes)) + ["E"]
							config["legend_markers"] = ["L"] + (["F"]*len(bkg_processes)) + ["ELP"]
							
							config["legend"] = [0.7, 0.6, 0.9, 0.88]
							
							config["output_dir"] = os.path.join(os.path.dirname(datacard), "plots")
							config["filename"] = level+("_"+fit_type if level == "postfit" else "")+"_"+category
							
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
		commands = [[
				"python $CMSSW_BASE//src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py {ARGS} {FIT_RESULT}".format(
						ARGS=" ".join(args),
						FIT_RESULT=os.path.join(os.path.dirname(datacard), "mlfit.root")
				)
		] for datacard in datacards_cbs.keys()]
		
		tools.parallelize(_call_command, commands, n_processes=n_processes)

