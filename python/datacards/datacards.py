# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy
import glob
import os
import re
import shutil

import ROOT

# http://cms-analysis.github.io/CombineHarvester/python-interface.html
import CombineHarvester.CombineTools.ch as ch
import CombineHarvester.CombinePdfs.morphing as morphing

import Artus.Utility.tools as tools
import Artus.Utility.jsonTools as jsonTools
import Artus.HarryPlotter.utility.roottools as roottools
import Artus.Utility.tfilecontextmanager as tfilecontextmanager

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
	print command
	#log.debug(command)
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
		
		self.stable_options = r"--robustFit 1 --preFitValue 1.0 --minimizerAlgoForMinos Minuit2 --minimizerAlgo Minuit2 --minimizerStrategy 0 --minimizerTolerance 0.1 --cminFallbackAlgo Minuit2,0:1.0"

		path=os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/mva_configs/")
		self.mva_bdt_syst_uncs =[
			"mva_regular_BDT_shifts",
			"lnN"]
		mapster_1 = ch.SystMap("bin", "process")
		if os.path.exists(os.path.join(path, "Reg_BDT.cfg")):
			reg_bdt = jsonTools.JsonDict(os.path.join(path, "Reg_BDT.cfg"))
			for category in reg_bdt.keys():
				call = ([category], ["ZTT", "ZLL", "ZL", "ZJ", "TTJ", "TT", "VV", "WJ", "W", "ggH", "qqH", "WH", "ZH", "VH"], reg_bdt[category])
				mapster_1(*call)
		else:
			mapster_1(["dummy"], ["ZTT", "ZLL", "ZL", "ZJ", "TTJ", "TT", "VV", "WJ", "W", "ggH", "qqH", "WH", "ZH", "VH"], (1.0,1.0))
		self.mva_bdt_syst_uncs.append(mapster_1)
			#values without process mapping [3.734375, 3.609375, 3.640625]
		self.mva_vbf_bdt_syst_uncs =[
			"mva_vbftagger_BDT_shifts",
			"lnN"]
		mapster_2 = ch.SystMap("bin", "process")
		if os.path.exists(os.path.join(path, "VBF_BDT.cfg")):
			vbf_bdt = jsonTools.JsonDict(os.path.join(path, "VBF_BDT.cfg"))
			for category in vbf_bdt.keys():
				call = ([category], ["ZTT", "ZLL", "ZL", "ZJ", "TTJ", "TT", "VV", "WJ", "W", "ggH", "qqH", "WH", "ZH", "VH"], vbf_bdt[category])
				mapster_2(*call)
		else:
			mapster_2(["dummy"], ["ZTT", "ZLL", "ZL", "ZJ", "TTJ", "TT", "VV", "WJ", "W", "ggH", "qqH", "WH", "ZH", "VH"], (1.0,1.0))
		self.mva_vbf_bdt_syst_uncs.append(mapster_2)

	def add_processes(self, channel, categories, bkg_processes, sig_processes=["ztt"], add_data=True, *args, **kwargs):
		bin = [(self.configs.category2binid(category, channel), category) for category in categories]

		for key in ["channel", "procs", "bin", "signal"]:
			if key in kwargs:
				kwargs.pop(key)

		non_sig_kwargs = copy.deepcopy(kwargs)
		if "mass" in non_sig_kwargs:
			non_sig_kwargs.pop("mass")

		if add_data:		
			self.cb.AddObservations(channel=[channel], mass=["*"], bin=bin, *args, **non_sig_kwargs)
		self.cb.AddProcesses(channel=[channel], mass=["*"], procs=bkg_processes, bin=bin, signal=False, *args, **non_sig_kwargs)
		self.cb.AddProcesses(channel=[channel], procs=sig_processes, bin=bin, signal=True, *args, **kwargs)

	def get_samples_per_shape_systematic(self, channel=None, category=None):
		cb = self.cb
		if not channel is None:
			if isinstance(channel, basestring):
				cb = cb.cp().channel([channel])
			else:
				cb = cb.cp().channel(channel)
		if not category is None:
			if isinstance(category, basestring):
				cb = cb.cp().bin([category])
			else:
				cb = cb.cp().bin(category)
		
		samples_per_shape_systematic = {}
		samples_per_shape_systematic.setdefault("nominal", set([])).update(set(cb.process_set()))
		
		# Maybe not needed any more (updated by next block) but kept for safety
		for shape_systematic in cb.cp().syst_type(["shape"]).syst_name_set():
			samples_per_shape_systematic.setdefault(shape_systematic, set([])).update(set(cb.cp().syst_type(["shape"]).syst_name([shape_systematic]).SetFromSysts(ch.Systematic.process)))
		
		# There are systematics, which can have a mixed type of lnN/shape, where CH returns only lnN as type. Such which values 1.0 and 0.0 are assumed to be shape uncertainties.
		cbOnlyShapeUncs = cb.cp()
		cbOnlyShapeUncs.FilterSysts(lambda systematic : (systematic.value_u() != 1.0) or (systematic.value_d() != 0.0))
		for shape_systematic in cbOnlyShapeUncs.syst_name_set():
			samples_per_shape_systematic.setdefault(shape_systematic, set([])).update(set(cbOnlyShapeUncs.cp().syst_name([shape_systematic]).SetFromSysts(ch.Systematic.process)))
		
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
	
	def create_morphing_signals(self, morphing_variable_name, nominal_value, min_value, max_value):
		self.workspace = ROOT.RooWorkspace("workspace", "workspace")
		self.morphing_variable = ROOT.RooRealVar(morphing_variable_name, morphing_variable_name, nominal_value, min_value, max_value)
		
		cb_signals = self.cb.cp().signals()
		for category in cb_signals.bin_set():
			cb_signals_category = cb_signals.cp().bin([category])
			for signal_process in cb_signals_category.process_set():
				morphing.BuildRooMorphing(self.workspace, self.cb, category, signal_process, self.morphing_variable, "norm", True, log.isEnabledFor(logging.DEBUG))
		
		self.cb.AddWorkspace(self.workspace, False)
		self.cb.cp().signals().ExtractPdfs(self.cb, "workspace", "$BIN_$PROCESS_morph", "")

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
		
		self.cb.SetGroup("bbb", [".*_bin_\\d+"])
		self.cb.SetGroup("syst_plus_bbb", [".*"])

	def scale_expectation(self, scale_factor, no_norm_rate_bkg=False, no_norm_rate_sig=False):
		self.cb.cp().backgrounds().ForEachProc(lambda process: process.set_rate((process.no_norm_rate() if no_norm_rate_bkg else process.rate()) * scale_factor))
		self.cb.cp().signals().ForEachProc(lambda process: process.set_rate((process.no_norm_rate() if no_norm_rate_sig else process.rate()) * scale_factor))
	
	def scale_processes(self, scale_factor, processes, no_norm_rate=False):
		self.cb.cp().process(processes).ForEachProc(lambda process: process.set_rate((process.no_norm_rate() if no_norm_rate else process.rate()) * scale_factor))

	def replace_observation_by_asimov_dataset(self, signal_mass=None, signal_processes=None):
		def _replace_observation_by_asimov_dataset(observation):
			cb = self.cb.cp().analysis([observation.analysis()]).era([observation.era()]).channel([observation.channel()]).bin([observation.bin()])
			background = cb.cp().backgrounds()
			
			signal = cb.cp().signals()
			if signal_mass:
				if signal_processes:
					signal = cb.cp().signals().process(signal_processes).mass([signal_mass])
				else:
					signal = cb.cp().signals().mass([signal_mass])
			elif signal_processes:
				signal = cb.cp().signals().process(signal_processes)
			
			observation.set_shape(background.GetShape() + signal.GetShape(), True)
			observation.set_rate(background.GetRate() + signal.GetRate())

		self.cb.cp().ForEachObs(_replace_observation_by_asimov_dataset)

	def write_datacards(self, datacard_filename_template, root_filename_template, output_directory="."):
		writer = ch.CardWriter(os.path.join("$TAG", datacard_filename_template),
		                       os.path.join("$TAG", root_filename_template))
		if log.isEnabledFor(logging.DEBUG):
			writer.SetVerbosity(1)
		
		# enable writing datacards in cases where the mass does not have its original meaning
		if (len(self.cb.mass_set()) == 1) and (self.cb.mass_set()[0] == "*"):
			writer.SetWildcardMasses([])

		return writer.WriteCards(output_directory[:-1] if output_directory.endswith("/") else output_directory, self.cb)

	def text2workspace(self, datacards_cbs, n_processes=1, higgs_mass="0", *args):
		physics_model = re.search("(-P|--physics-model)[\s=\"\']*\S*:(?P<physics_model>\S*)[\"\']?\s", " ".join(args))
		if physics_model is None:
			physics_model = {}
		else:
			physics_model = physics_model.groupdict()
		commands = ["text2workspace.py -m {MASS} {ARGS} {DATACARD} -o {OUTPUT}".format(
				MASS=[mass for mass in cb.mass_set() if mass != "*"][0] if len(cb.mass_set()) > 1 else str(higgs_mass), # TODO: maybe there are more masses?
				ARGS=" ".join(args),
				DATACARD=datacard,
				OUTPUT=os.path.splitext(datacard)[0]+"_"+physics_model.get("physics_model", "default")+".root"
		) for datacard, cb in datacards_cbs.iteritems()]

		tools.parallelize(_call_command, commands, n_processes=n_processes, description="text2workspace.py")

		return {datacard : os.path.splitext(datacard)[0]+"_"+physics_model.get("physics_model", "default")+".root" for datacard in datacards_cbs.keys()}

	def combine(self, datacards_cbs, datacards_workspaces, datacards_poi_ranges=None, n_processes=1, higgs_mass="0", *args, **kwargs):
		if datacards_poi_ranges is None:
			datacards_poi_ranges = {}
		tmp_args = " ".join(args)

		chunks = [[None, None]]
		if "{CHUNK}" in tmp_args and "--points" in tmp_args:
			splited_args = tmp_args.split()
			n_points = int(splited_args[splited_args.index("--points") + 1])
			n_points_per_chunk = 199
			chunks = [[chunk*n_points_per_chunk, (chunk+1)*n_points_per_chunk-1] for chunk in xrange(n_points/n_points_per_chunk+1)]
		
		method = re.search("(-M|--method)[\s=\"\']*(?P<method>\w*)[\"\']?\s", tmp_args)
		if not method is None:
			method = method.groupdict()["method"]
		
		name = re.search("(-n|--name)[\s=\"\']*(?P<name>\w*)[\"\']?\s", tmp_args)
		if not name is None:
			name = name.groupdict()["name"]
		
		split_stat_syst_uncs = kwargs.get("split_stat_syst_uncs", False)
		if split_stat_syst_uncs and (method is None):
			log.error("Uncertainties are not split into stat. and syst. components, since the method for combine is unknown!")
			split_stat_syst_uncs = False
		if split_stat_syst_uncs and (not "MultiDimFit" in method):
			log.error("Uncertainties are not split into stat. and syst. components. This is only supported for the MultiDimFit method!")
			split_stat_syst_uncs = False
		
		split_stat_syst_uncs_options = [""]
		split_stat_syst_uncs_names = [""]
		if split_stat_syst_uncs:
			split_stat_syst_uncs_options = [
				"--saveWorkspace",
				"--snapshotName {method} -w w".format(method=method),
				"--snapshotName {method} -w w --freezeNuisances {uncs}".format(method=method, uncs="{uncs}"),
			]
			split_stat_syst_uncs_names = [
				"Workspace",
				"TotUnc",
				"StatUnc",
			]
		
		for split_stat_syst_uncs_index, (split_stat_syst_uncs_option, split_stat_syst_uncs_name) in enumerate(zip(split_stat_syst_uncs_options, split_stat_syst_uncs_names)):
			prepared_tmp_args = None
			new_name = None
			if split_stat_syst_uncs:
				new_name = ("" if name is None else name) + split_stat_syst_uncs_name
				if name is None:
					prepared_tmp_args = tmp_args + " -n " + new_name
				else:
					prepared_tmp_args = copy.deepcopy(tmp_args)
					prepared_tmp_args = re.sub("(--algo)([\s=\"\']*)(\w*)([\"\']?\s)", "\\1\\2 "+("none" if split_stat_syst_uncs_index == 0 else "\\3")+"\\4", prepared_tmp_args)
					prepared_tmp_args = re.sub("(-n|--name)([\s=\"\']*)(\w*)([\"\']?\s)", "\\1\\2"+new_name+"\\4", prepared_tmp_args)
			else:
				prepared_tmp_args = tmp_args
			
			commands = []
			for chunk_index, (chunk_min, chunk_max) in enumerate(chunks):
				commands.extend([[
						"combine -m {MASS} {POI_RANGE} {ARGS} {CHUNK_POINTS} {SPLIT_STAT_SYST_UNCS} {WORKSPACE}".format(
								MASS=[mass for mass in datacards_cbs[datacard].mass_set() if mass != "*"][0] if len(datacards_cbs[datacard].mass_set()) > 1 else higgs_mass, # TODO: maybe there are more masses?
								POI_RANGE="--rMin {RMIN} --rMax {RMAX}" if datacard in datacards_poi_ranges else "",
								ARGS=prepared_tmp_args.format(CHUNK=str(chunk_index), RMIN="{RMIN}", RMAX="{RMAX}"),
								CHUNK_POINTS = "" if (chunk_min is None) or (chunk_max is None) else "--firstPoint {CHUNK_MIN} --lastPoint {CHUNK_MAX}".format(
										CHUNK_MIN=chunk_min,
										CHUNK_MAX=chunk_max
								),
								SPLIT_STAT_SYST_UNCS=split_stat_syst_uncs_option.format(uncs=",".join(kwargs.get("additional_freeze_nuisances", [])+datacards_cbs[datacard].syst_name_set())),
								WORKSPACE="-d "+workspace
						).format(RMIN=datacards_poi_ranges.get(datacard, ["", ""])[0], RMAX=datacards_poi_ranges.get(datacard, ["", ""])[1]),
						os.path.dirname(workspace)
				] for datacard, workspace in datacards_workspaces.iteritems()])

			tools.parallelize(_call_command, commands, n_processes=n_processes, description="combine")
			
			if split_stat_syst_uncs and (split_stat_syst_uncs_index == 0):
				# replace workspaces by saved versions from the first fit including the postfit nuisance parameter values
				for datacard, workspace in datacards_workspaces.iteritems():
					datacards_workspaces[datacard] = glob.glob(os.path.join(os.path.dirname(workspace), "higgsCombine"+new_name+"."+method+".*.root"))[0]

	def annotate_trees(self, datacards_workspaces, root_filename, value_regex_list, value_replacements=None, n_processes=1, values_tree_files=None, *args):
		if value_replacements is None:
			value_replacements = {}

		if values_tree_files is None:
			values_tree_files = {}
		
		commands = []
		for datacard, workspace in datacards_workspaces.iteritems():
			float_values = []
			found_match = False
			for value_regex in value_regex_list:
				search_result = re.search(value_regex, workspace)
				if not search_result is None:
					value = search_result.groups()[0]
					float_values.append(float(value_replacements.get(value, value)))
					found_match = True
				else:
					float_values.append(-999.0)
			
			if found_match:
				files = os.path.join(os.path.dirname(workspace), root_filename)
				values_tree_files.setdefault(tuple(float_values), []).extend(glob.glob(files))

				commands.append("annotate-trees.py {FILES} --values {VALUES} {ARGS}".format(
						FILES=files,
						VALUES=" ".join([str(value) for value in float_values]),
						ARGS=" ".join(args)
				))
		
		tools.parallelize(_call_command, commands, n_processes=n_processes, description="annotate-trees.py")
		return values_tree_files

	def hypotestresulttree(self, datacards_cbs, n_processes=1, rvalue="1", poiname="x"):
		commands = []
		hypotestresulttree = {}
		
		

		#for fit_type in fit_type_list:
		commands.extend(["root -q -b \"HiggsAnalysis/KITHiggsToTauTau/scripts/hypoTestResultTree.cxx(\\\"{INPUT}\\\",\\\"{OUTPUT}\\\",{MASS},{RVALUE},\\\"{POINAME}\\\")\"".format(
				INPUT=os.path.join(os.path.dirname(datacard),"higgsCombine.HybridNew.mH{angle}.root".format(angle = [mass for mass in cb.mass_set() if mass != "*"][0] if len(cb.mass_set()) > 1 else "0")),
				OUTPUT=os.path.join(os.path.dirname(datacard), "higgsCombine.HybridNew.mH{angle}_qmu.root".format(angle =[mass for mass in cb.mass_set() if mass != "*"][0] if len(cb.mass_set()) > 1 else "0")),
				MASS=[mass for mass in cb.mass_set() if mass != "*"][0] if len(cb.mass_set()) > 1 else "0", # TODO: maybe there are more masses?
				RVALUE= str(rvalue),
				POINAME=str(poiname)
				
				#ARGS=", ".join(args)
			) for datacard, cb in datacards_cbs.iteritems()])

			#datacards_postfit_shapes.setdefault(fit_type, {}).update({
			#		datacard : os.path.splitext(datacard)[0]+"_"+fit_type+".root"
			#for datacard, cb in datacards_cbs.iteritems()})

		tools.parallelize(_call_command, commands, n_processes=n_processes, description="hypoTestResultTree.cxx")

		return {datacard : os.path.join(os.path.dirname(datacard), "higgsCombine.HybridNew.mH{angle}_qmu.root".format(angle =[mass for mass in cb.mass_set() if mass != "*"][0] if len(cb.mass_set()) > 1 else "0")) for datacard in datacards_cbs.keys()}
	
	def plot1DScan(self, datacards_cbs, datacards_workspaces, poi, n_processes=1, higgs_mass="0", *args):
		tmp_args = "".join(args)
		commandsPlot = []
		commandsPlot.extend([[
				"$CMSSW_BASE/src/CombineHarvester/CombineTools/scripts/plot1DScan.py --POI {POI} -o {OUTPUT} higgsCombine.MultiDimFit.mH{MASS}.root".format(
						MASS=[mass for mass in datacards_cbs[datacard].mass_set() if mass != "*"][0] if len(datacards_cbs[datacard].mass_set()) > 1 else higgs_mass,
						POI=poi,
						OUTPUT="plots/likelihoodscan",
						ARGS=tmp_args.format()				
				),
				os.path.dirname(workspace)
		] for datacard, workspace in datacards_workspaces.iteritems()])
		
		tools.parallelize(_call_command, commandsPlot, n_processes=n_processes, description="combineTool.py (plots)")	

	def postfit_shapes(self, datacards_cbs, s_fit_only=False, n_processes=1, higgs_mass="0", *args):
		commands = []
		datacards_postfit_shapes = {}
		fit_type_list = kwargs.get("fit_type_list", ["fit_s", "fit_b"])
		if s_fit_only:
			fit_type_list.remove("fit_b")

		for fit_type in fit_type_list:
			commands.extend(["PostFitShapes --postfit -d {DATACARD} -o {OUTPUT} -m {MASS} -f {FIT_RESULT} {ARGS}".format(
					DATACARD=datacard,
					OUTPUT=os.path.splitext(datacard)[0]+"_"+fit_type+".root",
					MASS=[mass for mass in cb.mass_set() if mass != "*"][0] if len(cb.mass_set()) > 1 else higgs_mass, # TODO: maybe there are more masses?
					FIT_RESULT=os.path.join(os.path.dirname(datacard), kwargs.get("fit_result", "mlfit.root")+":"+fit_type),
					ARGS=" ".join(args)
			) for datacard, cb in datacards_cbs.iteritems()])

			datacards_postfit_shapes.setdefault(fit_type, {}).update({
					datacard : os.path.splitext(datacard)[0]+"_"+fit_type+".root"
			for datacard, cb in datacards_cbs.iteritems()})

		tools.parallelize(_call_command, commands, n_processes=n_processes, description="PostFitShapes")

		return datacards_postfit_shapes

	def postfit_shapes_fromworkspace(self, datacards_cbs, datacards_workspaces, s_fit_only=False, n_processes=1, higgs_mass="0", *args, **kwargs):
		commands = []
		datacards_postfit_shapes = {}
		fit_type_list = kwargs.get("fit_type_list", ["fit_s", "fit_b"])
		if s_fit_only:
			fit_type_list.remove("fit_b")

		for fit_type in fit_type_list:
			commands.extend(["PostFitShapesFromWorkspace --postfit -w {WORKSPACE} -d {DATACARD} -o {OUTPUT} -m {MASS} -f {FIT_RESULT} {ARGS}".format(
					WORKSPACE=datacards_workspaces[datacard],
					DATACARD=datacard,
					OUTPUT=os.path.splitext(datacard)[0]+"_"+fit_type+".root",
					MASS=[mass for mass in cb.mass_set() if mass != "*"][0] if len(cb.mass_set()) > 1 else higgs_mass, # TODO: maybe there are more masses?
					FIT_RESULT=os.path.join(os.path.dirname(datacard), kwargs.get("fit_result", "mlfit.root")+":"+fit_type),
					ARGS=" ".join(args)
			) for datacard, cb in datacards_cbs.iteritems()])

			datacards_postfit_shapes.setdefault(fit_type, {}).update({
					datacard : os.path.splitext(datacard)[0]+"_"+fit_type+".root"
			for datacard, cb in datacards_cbs.iteritems()})

		tools.parallelize(_call_command, commands, n_processes=n_processes, description="PostFitShapesFromWorkspace")

		return datacards_postfit_shapes

	def prefit_postfit_plots(self, datacards_cbs, datacards_postfit_shapes, plotting_args=None, n_processes=1, signal_stacked_on_bkg=False, *args):
		if plotting_args is None:
			plotting_args = {}
		
		base_path = reduce(lambda datacard1, datacard2: tools.longest_common_substring(datacard1, datacard2), datacards_cbs.keys())
		
		plot_configs = []
		bkg_plotting_order = ["ZTTPOSPOL", "ZTTNEGPOL", "ZTT", "ZLL", "ZL", "ZJ", "EWKZ", "TTTAUTAU", "TTT", "TTJJ", "TTJ", "TT", "VVT", "VVJ", "VV", "WJ", "W", "hww_gg125", "hww_qq125", "EWK", "QCD"]
		for level in ["prefit", "postfit"]:
			for index, (fit_type, datacards_postfit_shapes_dict) in enumerate(datacards_postfit_shapes.iteritems()):
				if (index == 0) or (level == "postfit"):
					for datacard, postfit_shapes in datacards_postfit_shapes_dict.iteritems():
						for category in datacards_cbs[datacard].cp().bin_set():
							stacked_processes = []
							if signal_stacked_on_bkg:
								stacked_processes.extend(datacards_cbs[datacard].cp().bin([category]).signals().process_set())
							stacked_processes.extend(datacards_cbs[datacard].cp().bin([category]).backgrounds().process_set())
							stacked_processes.sort(key=lambda process: bkg_plotting_order.index(process) if process in bkg_plotting_order else len(bkg_plotting_order))
							stacked_processes = [process for process in bkg_plotting_order if datacards_cbs[datacard].cp().bin([category]).backgrounds().process([process]).GetRate() > 0.0]

							config = {}
							
							processes_to_plot = list(stacked_processes)
							# merge backgrounds from dictionary if provided
							if plotting_args.get("merge_backgrounds", False):
								if not "SumOfHistograms" in config.get("analysis_modules", []):
									config.setdefault("analysis_modules", []).append("SumOfHistograms")
								
								merge_backgrounds = plotting_args.get("merge_backgrounds", {})
								for new_background, backgrounds_to_merge in merge_backgrounds.iteritems():
									if new_background not in stacked_processes:
										backgrounds_to_remove = ""
										for background in backgrounds_to_merge:
											if background in stacked_processes:
												stacked_processes = [p + ("_noplot" if p == background else "") for p in stacked_processes]
												backgrounds_to_remove += background + "_noplot "
										config.setdefault("sum_nicks", []).append(backgrounds_to_remove)
										config.setdefault("sum_result_nicks", []).append(new_background)
								
								processes_to_plot = [p for p in stacked_processes if not "noplot" in p]
								
								for new_background in merge_backgrounds:
									if new_background not in stacked_processes:
										processes_to_plot.append(new_background)
								
								processes_to_plot.sort(key=lambda process: bkg_plotting_order.index(process) if process in bkg_plotting_order else len(bkg_plotting_order))
							
							config["files"] = [postfit_shapes]
							config["folders"] = [category+"_"+level]
							config["x_expressions"] = [p.strip("_noplot") for p in stacked_processes] + ["TotalSig"] + ["data_obs", "TotalBkg"]
							config["nicks"] = stacked_processes + ["TotalSig" + ("_noplot" if signal_stacked_on_bkg else "")] + ["data_obs", "TotalBkg" + ("_noplot" if signal_stacked_on_bkg else "")]
							config["stacks"] = (["stack"]*len(processes_to_plot)) + (["data"] if signal_stacked_on_bkg else ["sig", "data", "bkg_unc"])

							config["labels"] = [label.lower() for label in processes_to_plot + (["data_obs"] if signal_stacked_on_bkg else ["TotalSig", "data_obs", "TotalBkg"])]
							config["colors"] = [color.lower() for color in processes_to_plot + (["data_obs"] if signal_stacked_on_bkg else ["TotalSig", "data_obs", "TotalBkg"])]
							config["markers"] = (["HIST"]*len(processes_to_plot)) + (["E"] if signal_stacked_on_bkg else ["LINE", "E", "E2"])
							config["legend_markers"] = (["F"]*len(processes_to_plot)) + (["ELP"] if signal_stacked_on_bkg else ["L", "ELP", "F"])

							config["x_label"] = category.split("_")[0]+"_"+plotting_args.get("x_expressions", None)
							config["title"] = "channel_"+category.split("_")[0]
							config["energies"] = [13.0]
							config["lumis"] = [float("%.1f" % plotting_args.get("lumi", 1.0))]
							if plotting_args.get("era", False):
								config["year"] = plotting_args.get("era")
							config["legend"] = [0.7, 0.6, 0.9, 0.88]
							config["y_lims"] = [0.0]

							config["output_dir"] = os.path.join(os.path.dirname(datacard), "plots")
							config["filename"] = level+("_"+fit_type if level == "postfit" else "")+"_"+category
							if plotting_args.get("www", False):
								config["www"] = os.path.join(config["output_dir"].replace(base_path, plotting_args["www"]+"/"))

							if plotting_args.get("normalize", False):
								config.setdefault("analysis_modules", []).append("NormalizeByBinWidth")

							if plotting_args.get("ratio", False):
								if signal_stacked_on_bkg:
									if not "SumOfHistograms" in config.get("analysis_modules", []):
										config.setdefault("analysis_modules", []).append("SumOfHistograms")
									config.setdefault("sum_nicks", []).append("TotalBkg_noplot TotalSig_noplot")
									config.setdefault("sum_result_nicks", []).append("TotalBkg")
								
								if not "Ratio" in config.get("analysis_modules", []):
									config.setdefault("analysis_modules", []).append("Ratio")
								# add signal/bkg ratio first
								if plotting_args.get("add_soverb_ratio", False):
									if not "SumOfHistograms" in config.get("analysis_modules", []):
										config.setdefault("analysis_modules", []).append("SumOfHistograms")
									config.setdefault("sum_nicks", []).append("TotalBkg TotalSig")
									config.setdefault("sum_result_nicks", []).append("TotalSignalPlusBackground_noplot")
									config.setdefault("ratio_numerator_nicks", []).append("TotalSignalPlusBackground_noplot")
									config.setdefault("ratio_denominator_nicks", []).append("TotalBkg")
									config.setdefault("ratio_result_nicks", []).append("ratio_soverb")
								# now add data/bkg ratio
								config.setdefault("ratio_numerator_nicks", []).extend(["TotalBkg", "data_obs"])
								config.setdefault("ratio_denominator_nicks", []).extend(["TotalBkg"] * 2)
								config.setdefault("ratio_result_nicks", []).extend(["ratio_unc", "ratio"])
								config["ratio_denominator_no_errors"] = True
								
								if plotting_args.get("add_soverb_ratio", False):
									config.setdefault("colors", []).append("kRed")
									config.setdefault("markers", []).append("LINE")
									config.setdefault("legend_markers", []).append("L")
									config.setdefault("labels", []).append("")
									config.setdefault("stacks", []).append("ratio_soverb")
								config.setdefault("colors", []).extend(["totalbkg", "#000000"])
								config.setdefault("markers", []).extend(["E2", "E"])
								config.setdefault("legend_markers", []).extend(["F", "ELP"])
								config.setdefault("labels", []).extend([""] * 2)
								config.setdefault("stacks", []).extend(["unc", "ratio"])
								config["legend"] = [0.7, 0.4, 0.95, 0.83]
								config["subplot_grid"] = "True"
								config["y_subplot_lims"] = [0.5, 1.5]
								config["y_subplot_label"] = "Obs./Exp."
							
							# update ordering if backgrounds were merged
							if plotting_args.get("merge_backgrounds", False):
								config["nicks_whitelist"] = processes_to_plot + ["TotalSig" + ("_noplot" if signal_stacked_on_bkg else "")] + ["data_obs", "TotalBkg" + ("_noplot" if signal_stacked_on_bkg else "")]
								if plotting_args.get("ratio", False):
									if plotting_args.get("add_soverb_ratio", False):
										config["nicks_whitelist"].append("ratio_soverb")
									config["nicks_whitelist"].extend(["ratio_unc", "ratio"])

							plot_configs.append(config)

		if plotting_args.get("return_configs", False):
			return plot_configs
		else:
			# create result plots HarryPlotter
			return higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[plotting_args.get("args", "")], n_processes=n_processes)

	def print_pulls(self, datacards_cbs, n_processes=1, *args, **kwargs):
		commands = []
		for pulls_format, file_format in zip(["latex", "text"], ["tex", "txt"]):
			for all_nuissances in [False, True]:
				commands.extend([[
						"execute-command.py \"python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -f {FORMAT} {ALL} {PLOT} {ARGS} {FIT_RESULT}\" --log-file {LOG_FILE}".format(
								FORMAT=pulls_format,
								ALL=("-a" if all_nuissances else ""),
								PLOT="-g "+("" if all_nuissances else "largest_")+"pulls.root",
								ARGS=" ".join(args),
								FIT_RESULT=os.path.join(os.path.dirname(datacard), kwargs.get("fit_result", "mlfit.root")),
								LOG_FILE=("" if all_nuissances else "largest_")+"pulls."+file_format
						),
						os.path.dirname(datacard)
				] for datacard in datacards_cbs.keys()])

		tools.parallelize(_call_command, commands, n_processes=n_processes, description="diffNuisances.py")

	def pull_plots(self, datacards_postfit_shapes, s_fit_only=False, plotting_args=None, n_processes=1, *args):
		if plotting_args is None:
			plotting_args = {}
		
		datacards = []
		for fit_type, datacards_postfit_shapes_dict in datacards_postfit_shapes.iteritems():
			datacards.extend(datacards_postfit_shapes_dict.keys())
		base_path = reduce(lambda datacard1, datacard2: tools.longest_common_substring(datacard1, datacard2), datacards)

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

					config["left_pad_margin"] = 0.40
					config["labels"] = ["prefit", "S+B model"]
					config["markers"] = ["L2", "P"]
					config["fill_styles"] = [3001, 0]
					config["legend"] = [0.75, 0.8]
					config["legend_markers"] = ["LF", "LP"]
					config["x_lims"] = [-5.0, 5.0]
					config["x_label"] = "Pull values"

					config["output_dir"] = os.path.join(os.path.dirname(datacard), "plots")
					config["filename"] = "pulls"
					if plotting_args.get("www", False):
						config["www"] = os.path.join(config["output_dir"].replace(base_path, plotting_args["www"]+"/"))

					plot_configs.append(config)

		# create result plots HarryPlotter
		return higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[plotting_args.get("args", "")], n_processes=n_processes)		
	
	def nuisance_impacts(self, datacards_cbs, datacards_workspaces, n_processes=1, higgs_mass="0", *args):
		tmp_args = " ".join(args)
		
		commandsInitialFit = []
		commandsInitialFit.extend([[
				"combineTool.py -M Impacts -d {WORKSPACE} -m {MASS} --robustFit 1 --minimizerTolerance 0.1 --minimizerStrategy 0 --minimizerAlgoForMinos Minuit2,migrad --doInitialFit --allPars {ARGS}".format(
						MASS=[mass for mass in datacards_cbs[datacard].mass_set() if mass != "*"][0] if len(datacards_cbs[datacard].mass_set()) > 1 else higgs_mass,
						ARGS=tmp_args.format(),
						WORKSPACE=workspace
				),
				os.path.dirname(workspace)
		] for datacard, workspace in datacards_workspaces.iteritems()])
		
		commandsFits = []
		commandsFits.extend([[
				"combineTool.py -M Impacts -d {WORKSPACE} -m {MASS} --robustFit 1 --minimizerTolerance 0.1 --minimizerStrategy 0 --minimizerAlgoForMinos Minuit2,migrad --doFits --parallel {NPROCS} --allPars {ARGS}".format(
						MASS=[mass for mass in datacards_cbs[datacard].mass_set() if mass != "*"][0] if len(datacards_cbs[datacard].mass_set()) > 1 else higgs_mass,
						ARGS=tmp_args.format(),
						WORKSPACE=workspace,
						NPROCS=n_processes
				),
				os.path.dirname(workspace)
		] for datacard, workspace in datacards_workspaces.iteritems()])
		
		commandsOutput = []
		commandsOutput.extend([[
				"combineTool.py -M Impacts -d {WORKSPACE} -m {MASS} --robustFit 1 --minimizerTolerance 0.1 --minimizerStrategy 0 --minimizerAlgoForMinos Minuit2,migrad --output impacts.json --parallel {NPROCS} --allPars {ARGS}".format(
						MASS=[mass for mass in datacards_cbs[datacard].mass_set() if mass != "*"][0] if len(datacards_cbs[datacard].mass_set()) > 1 else higgs_mass,
						ARGS=tmp_args.format(),
						WORKSPACE=workspace,
						NPROCS=n_processes
				),
				os.path.dirname(workspace)
		] for datacard, workspace in datacards_workspaces.iteritems()])
		
		commandsPlot = []
		commandsPlot.extend([[
				"plotImpacts.py -i {INPUT} -o {OUTPUT}".format(
						INPUT="impacts.json",
						OUTPUT="plots/nuisance_impacts"
				),
				os.path.dirname(workspace)
		] for datacard, workspace in datacards_workspaces.iteritems()])

		tools.parallelize(_call_command, commandsInitialFit, n_processes=n_processes, description="combineTool.py (initial fits)")
		tools.parallelize(_call_command, commandsFits, n_processes=1, description="combineTool.py (fits)")
		tools.parallelize(_call_command, commandsOutput, n_processes=1, description="combineTool.py (outputs)")
		tools.parallelize(_call_command, commandsPlot, n_processes=n_processes, description="combineTool.py (plots)")

	def auto_rebin(self, bin_threshold = 1.0, rebin_mode = 0):
		rebin = ch.AutoRebin()
		rebin.SetBinThreshold(bin_threshold)
		rebin.SetRebinMode(rebin_mode)
		rebin.SetPerformRebin(True)
		rebin.SetVerbosity(0)
		rebin.Rebin(self.cb, self.cb)
