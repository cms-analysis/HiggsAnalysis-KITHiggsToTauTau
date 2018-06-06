#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os
import sys
import re

import Artus.Utility.jsonTools as jsonTools
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as binnings
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2015 as samples


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make gen-reco comparison plots. See also https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/wiki/Generator-Reconstruction-Matching.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-s", "--samples", nargs="+", default=["ztt"],
	                    help="Samples. [Default: %(default)s]")
	parser.add_argument("-c", "--channels", nargs="+",
	                    default=["tt", "mt", "et", "em", "mm"],
	                    help="Channels. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="+", default=[None],
	                    help="Categories. [Default: %(default)s]")
	parser.add_argument("-r", "--reco-quantities", nargs="+", action="append",
	                    default=[["svfitLV.mass()", "svfitLV.Pt()", "svfitLV.Eta()", "svfitLV.Phi()", "svfitLV.E()"]+
	                             ["svfitTau1LV.mass()", "svfitTau1LV.Pt()", "svfitTau1LV.Eta()", "svfitTau1LV.Phi()", "svfitTau1LV.E()"]+
	                             ["svfitTau2LV.mass()", "svfitTau2LV.Pt()", "svfitTau2LV.Eta()", "svfitTau2LV.Phi()", "svfitTau2LV.E()"]]+
	                            [["svfitM91LV.mass()", "svfitM91LV.Pt()", "svfitM91LV.Eta()", "svfitM91LV.Phi()", "svfitM91LV.E()"]+
	                             ["svfitM91Tau1LV.mass()", "svfitM91Tau1LV.Pt()", "svfitM91Tau1LV.Eta()", "svfitM91Tau1LV.Phi()", "svfitM91Tau1LV.E()"]+
	                             ["svfitM91Tau2LV.mass()", "svfitM91Tau2LV.Pt()", "svfitM91Tau2LV.Eta()", "svfitM91Tau2LV.Phi()", "svfitM91Tau2LV.E()"]],
	                    help="Reco-level quantities. Use this argument multiple times to compare different sets of reconstructions. [Default: %(default)s]")
	parser.add_argument("-g", "--gen-quantities", nargs="+",
	                    default=["genBosonLV.mass()", "genBosonLV.Pt()", "genBosonLV.Eta()", "genBosonLV.Phi()", "genBosonLV.E()"]+
	                            ["genBosonTau1LV.mass()", "genBosonTau1LV.Pt()", "genBosonTau1LV.Eta()", "genBosonTau1LV.Phi()", "genBosonTau1LV.E()"]+
	                            ["genBosonTau2LV.mass()", "genBosonTau2LV.Pt()", "genBosonTau2LV.Eta()", "genBosonTau2LV.Phi()", "genBosonTau2LV.E()"],
	                    help="Gen-level quantities. [Default: %(default)s]")
	parser.add_argument("-w", "--weights", nargs="+", action="append",
	                    default=[(["(svfitLV.mass()<8000)*(genBosonLV.mass()<9000)"]*5)+
	                             (["(svfitTau1LV.mass()<8000)*(genBosonTau1LV.mass()<9000)"]*5)+
	                             (["(svfitTau2LV.mass()<8000)*(genBosonTau2LV.mass()<9000)"]*5)]+
	                            [(["(svfitM91LV.mass()<8000)*(genBosonLV.mass()<9000)"]*5)+
	                             (["(svfitM91Tau1LV.mass()<8000)*(genBosonTau1LV.mass()<9000)"]*5)+
	                             (["(svfitM91Tau2LV.mass()<8000)*(genBosonTau2LV.mass()<9000)"]*5)],
	                    help="Weights/cuts to ensure proper fits and gen-reco matching. Use this argument multiple times to compare different sets of reconstructions. [Default: %(default)s]")
	parser.add_argument("--axis-labels", nargs="+",
	                    default=["m_{#tau#tau}", "p_{T, #tau#tau}", "#eta_{#tau#tau}", "#phi_{#tau#tau}", "E_{#tau#tau}"]+
	                            ["m_{#tau_{1}}", "p_{T, #tau_{1}}", "#eta_{#tau_{1}}", "#phi_{#tau_{1}}", "E_{#tau_{1}}"]+
	                            ["m_{#tau_{2}}", "p_{T, #tau_{2}}", "#eta_{#tau_{2}}", "#phi_{#tau_{2}}", "E_{#tau_{2}}"],
	                    help="Axis labels. [Default: %(default)s]")
	parser.add_argument("--legend-labels", nargs="+",
	                    default=["No mass constraint", "With m=m_{Z} constraint"],
	                    help="Legend labels. [Default: %(default)s]")
	parser.add_argument("--mssm", default=False, action="store_true",
	                    help="Produce the plots for the MSSM. [Default: %(default)s]")
	parser.add_argument("--mva", default=False, action="store_true",
	                    help="Produce plots for the mva studies. [Default: %(default)s]")
	parser.add_argument("--polarisation", default=False, action="store_true",
	                    help="Produce the plots for the polarisation analysis. [Default: %(default)s]")
	parser.add_argument("--smhtt", default=False, action="store_true",
	                    help="Produce the plots for the SM HTT analysis. [Default: %(default)s]")
	parser.add_argument("--cpggh", default=False, action="store_true",
			    help="Produce plots for the Higgs CP ggH analysis. [Default: %(default)s]")
	parser.add_argument("--cp", default=False, action="store_true",
	                    help="Produce the plots for the CP analysis. [Default: %(default)s]")  #TODO instead of 3 different boolean flag, change to option with 3 possible values
	parser.add_argument("--cprho", default=False, action="store_true",
	                    help="Produce the plots for the CP analysis. [Default: %(default)s]")
	parser.add_argument("--cpcomb", default=False, action="store_true",
	                    help="Produce the plots for the CP analysis. [Default: %(default)s]")
	parser.add_argument("--taues", default=False, action="store_true",
	                    help="Produce the plots for the tau energy scale analysis. [Default: %(default)s]")
	parser.add_argument("--etaufakerate", default=False, action="store_true",
	                    help="Produce the plots for the electron tau fake rate analysis. [Default: %(default)s]")
	parser.add_argument("--lfv", default=False, action="store_true",
	                    help="Produce the plots for the lepton flavour violation analysis. [Default: %(default)s]")
	parser.add_argument("--analysis-modules", default=[], nargs="+",
	                    help="Additional analysis Modules. [Default: %(default)s]")
	parser.add_argument("--era", default="2016",
	                    help="Era of samples to be used. [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000.0,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	parser.add_argument("--no-ewk-samples", default=False, action="store_true",
	                    help="Do not use EWK Z/W samples. [Default: %(default)s]")
	parser.add_argument("--no-ewkz-as-dy", default=False, action="store_true",
	                    help="Do not include EWKZ samples in inputs for DY. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int,
	                    help="Number of plots. [Default: all]")
	parser.add_argument("-o", "--output-dir",
	                    default="$CMSSW_BASE/src/plots/svfit_performance/",
	                    help="Output directory. [Default: %(default)s]")
	parser.add_argument("--www", nargs="?", default=None, const="svfit_performance",
	                    help="Publish plots. [Default: %(default)s]")
	
	args = parser.parse_args()
	logger.initLogger(args)

	if (args.era == "2015") or (args.era == "2015new"):
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2015 as samples
	elif args.era == "2016":
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
		if args.lumi == parser.get_default("lumi"):
			args.lumi = samples.default_lumi/1000.0
	elif args.era == "2017":
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2017 as samples
		if args.lumi == parser.get_default("lumi"):
			args.lumi = samples.default_lumi/1000.0
	else:
		log.critical("Invalid era string selected: " + args.era)
		sys.exit(1)
	
	sample_settings = samples.Samples()
	binnings_settings = binnings.BinningsDict()

	args.categories = [None if category == "None" else category for category in args.categories]

	# Category and Cut type assignment for respective studies
	global_category_string = "catHtt13TeV"
	global_cut_type = "baseline"
	if args.mssm:
		global_category_string = "catHttMSSM13TeV"
		global_cut_type = "mssm"
	elif args.mva:
		global_category_string = "catMVAStudies"
	elif args.lfv:
		global_category_string = "catLFV13TeV"
	elif args.polarisation:
		global_category_string = "catZttPol13TeV"
		global_cut_type = "low_mvis_smhtt"
	elif args.taues:
		global_cut_type = "tauescuts"
	elif args.cp:
		global_cut_type = "cp"
	elif args.cprho:
		global_cut_type = "cprho"
	elif args.cpcomb:
		global_cut_type = "cpcomb"
	elif args.etaufakerate:
		global_category_string = "catETauFakeRate13TeV"
		global_cut_type = "etaufake"
		if args.categories == [None]:
			args.categories = ["vloose_pass", "vloose_fail", "loose_pass", "loose_fail", "medium_pass", "medium_fail", "tight_pass", "tight_fail", "vtight_pass", "vtight_fail"]
		log.info("Use the following option to exclude the necessary cuts for etaufakerate studies: [ --exclude-cuts 'dilepton_veto' 'extra_lepton_veto' 'anti_e_tau_discriminators' ]")
	if args.era == "2016":
		if args.smhtt:
			global_cut_type = "smhtt"
		if args.cpggh:
			global_cut_type = "cpggh"
		global_cut_type += "2016"

	plot_configs = []
	for sample in args.samples:
		for channel in args.channels:
			for category in args.categories:
				category_string = None
				if category != None:
					category_string = (global_category_string + "_{channel}_{category}").format(channel = channel, category = category)
				
				for reco_quantities, gen_quantity, weights, axis_label in zip(zip(*args.reco_quantities), args.gen_quantities, zip(*args.weights), args.axis_labels):
					log.debug("Create comparison for sample={sample}, channel={channel}, category={category}...".format(sample=sample, channel=channel, category=category))
					log.debug("\tReco level: "+(", ".join(reco_quantities)))
					log.debug("\tGen level:  "+gen_quantity)
					log.debug("\tWeights:    "+(", ".join(weights)))
					
					config = {}
					for reco_index, (reco_quantity, weight, legend_label) in enumerate(zip(reco_quantities, weights, args.legend_labels)):
					
						tmp_config = sample_settings.get_config(
								samples = [getattr(samples.Samples, sample)],
								channel = channel,
								category = category_string,
								weight = "("+weight+")",
								lumi  =  args.lumi * 1000,
								estimationMethod = "new",
								mssm = args.mssm,
								cut_type = global_cut_type,
								no_ewk_samples = args.no_ewk_samples,
								no_ewkz_as_dy = args.no_ewkz_as_dy,
								nick_suffix = "_reco"+str(reco_index)
						)
						
						tmp_config["x_expressions"] = ["(({reco})-({gen}))/({gen})".format(reco=reco_quantity, gen=gen_quantity)] * len(tmp_config["nicks"])
						tmp_config["labels"] = [legend_label] * len(tmp_config["labels"])
						
						config = samples.Samples.merge_configs(config, tmp_config)
					
					config["directories"] = [args.input_dir]
					config["x_bins"] = ["101,-1,1"]
					
					if "stacks" in config:
						config.pop("stacks")
					
					if "colors" in config:
						config.pop("colors")
					config["markers"] = ["LINE"]
					config["line_widths"] = [3]
					config["legend_markers"] = ["L"]
					config["legend"] = [0.6, 0.6, 0.9, 0.85]
					
					reco_label = axis_label.replace("_", "^{reco}_", 1) if "_" in axis_label else (axis_label+"^{reco}")
					gen_label = axis_label.replace("_", "^{gen}_", 1) if "_" in axis_label else (axis_label+"^{gen}")
					config["x_label"] = "Resolution #left({reco} - {gen}#right) / {gen}".format(reco=reco_label, gen=gen_label)
					config["title"] = "channel_"+channel
					if args.polarisation:
						config["title"] = "channel_"+channel+"_"+category
			
					if args.lumi is not None:
						config["lumis"] = [float("%.1f" % args.lumi)]
					config["energies"] = [13]
					config["year"] = args.era
					
					output_dir = os.path.join(sample, channel, category, "resolution")
					config["output_dir"] = os.path.join(args.output_dir, output_dir)
					if not args.www is None:
						config["www"] = os.path.join(args.www, output_dir)
					
					plot_configs.append(config)
	
	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)
	
	import sys
	sys.exit(0)
	
	"""
		for quantity, weight in zip(args.quantities, args.weights):

			channels_background_methods = zip(args.channels, args.background_method)
			channel_config = {}
			for index, (channel, background_method) in enumerate(channels_background_methods):
				if args.mssm:
					cut_type = "mssm2016full"
					if args.era == "2016":
						cut_type = "mssm2016"
					elif "looseiso" in category:
						cut_type = "mssm2016looseiso"
					elif "loosemt" in category:
						cut_type = "mssm2016loosemt"
					elif "tight" in category:
						cut_type = "mssm2016tight"

				if args.etaufakerate:
					# TODO: add the default global_cut_type
					if "vloose_pass" in category:
						global_cut_type = "etaufake2016_antievloosepass"
					elif "vloose_fail" in category:
						global_cut_type = "etaufake2016_antievloosefail"
					elif "loose_pass" in category:
						global_cut_type = "etaufake2016_antieloosepass"
					elif "loose_fail" in category:
						global_cut_type = "etaufake2016_antieloosefail"
					elif "medium_pass" in category:
						global_cut_type = "etaufake2016_antiemediumpass"
					elif "medium_fail" in category:
						global_cut_type = "etaufake2016_antiemediumfail"
					elif "tight_pass" in category:
						global_cut_type = "etaufake2016_antietightpass"
					elif "tight_fail" in category:
						global_cut_type = "etaufake2016_antietightfail"
					elif "vtight_pass" in category:
						global_cut_type = "etaufake2016_antievtightpass"
					elif "vtight_fail" in category:
						global_cut_type = "etaufake2016_antievtightfail"

				last_loop = index == len(channels_background_methods) - 1

				category_string = None
				if category != None:
					category_string = (global_category_string + "_{channel}_{category}").format(channel = channel, category = category)

				json_config = {}
				json_filenames = [os.path.join(args.json_dir, "8TeV" if args.run1 else "13TeV", channel_dir, quantity + ".json") for channel_dir in [channel, "default"]]
				for json_filename in json_filenames:
					json_filename = os.path.expandvars(json_filename)
					if os.path.exists(json_filename):
						json_config = jsonTools.JsonDict(json_filename).doIncludes().doComments()
						break

				quantity = json_config.pop("x_expressions", [quantity])[0]
				config = sample_settings.get_config(
						samples = list_of_samples,
						channel = channel,
						category = category_string,
						higgs_masses = args.higgs_masses,
						normalise_signal_to_one_pb = False,
						ztt_from_mc = args.ztt_from_mc,
						weight = "((%s)*(%s))" % (json_config.pop("weights", ["1.0"])[0], weight),
						lumi  =  args.lumi * 1000,
						exclude_cuts = args.exclude_cuts + json_config.pop("exclude_cuts", []),
						blind_expression = channel + "_" + quantity,
						fakefactor_method = args.fakefactor_method,
						stack_signal = args.stack_signal,
						scale_signal = args.scale_signal,
						project_to_lumi = args.project_to_lumi,
						cut_mc_only = args.cut_mc_only,
						scale_mc_only = args.scale_mc_only,
						estimationMethod = background_method,
						mssm = args.mssm,
						controlregions = args.controlregions,
						cut_type = global_cut_type,
						no_ewk_samples = args.no_ewk_samples,
						no_ewkz_as_dy = args.no_ewkz_as_dy,
						useRelaxedIsolationForW = args.use_relaxed_isolation_for_W,
						useRelaxedIsolationForQCD = args.use_relaxed_isolation_for_QCD,
						nick_suffix = (channel if args.channel_comparison else ""),
						#polarisation_bias_correction=True,
						asimov_nicks = asimov_nicks
				)
				if (args.channel_comparison):
					channel_config = samples.Samples.merge_configs(channel_config, config)
					if last_loop:
						config = channel_config

				x_expression = json_config.pop("x_expressions", [quantity])
				config["x_expressions"] = [("0" if (("gen_zttpospol" in nick) or ("gen_zttnegpol" in nick)) else x_expression) for nick in config["nicks"]]
				config["category"] = category


				# Introduced due to missing samples in 2017 MCv1, can be removed when 2017 MCv2 samples are out, and samples_rnu2_2017.py script is updated correspondingly.
				if args.era == "2017":
					sub_conf_index = 0
					while (sub_conf_index < len(config["files"])):
						if config["files"][sub_conf_index] is None:
							config["files"].pop(sub_conf_index)
							config["x_expressions"].pop(sub_conf_index)
							config["scale_factors"].pop(sub_conf_index)
							config["folders"].pop(sub_conf_index)
							config["weights"].pop(sub_conf_index)
							config["nicks"].pop(sub_conf_index)
						else:
							sub_conf_index +=1

				if args.new_tau_id:
					for weight_index, weight in enumerate(config.get("weights", [])):
						config["weights"][weight_index] = weight.replace("byTightIsolationMVArun2v1DBoldDMwLT", "rerunDiscriminationByIsolationMVAOldDMrun2v1Medium").replace("byMediumIsolationMVArun2v1DBoldDMwLT", "rerunDiscriminationByIsolationMVAOldDMrun2v1Loose").replace("byLooseIsolationMVArun2v1DBoldDMwLT", "rerunDiscriminationByIsolationMVAOldDMrun2v1VLoose")

				binning_string = "binningHtt13TeV"
				if args.mssm:
					binning_string = "binningHttMSSM13TeV"
				elif args.mva:
					binning_string = "binningMVAStudies"
				elif args.polarisation:
					binning_string = "binningZttPol13TeV"

				binnings_key = "{binning_string}{channel}{category}_{quantity}".format(
						binning_string = binning_string + "_" if binning_string else "",
						channel = channel,
						category = "_" + category if category else "",
						quantity = quantity
				)
				if binnings_key not in binnings_settings.binnings_dict and channel + "_" + quantity in binnings_settings.binnings_dict and "--x-bins" not in args.args:
					binnings_key = channel + "_" + quantity
				if binnings_key not in binnings_settings.binnings_dict:
					binnings_key = None
				
				if binnings_key is not None and "--x-bins" not in args.args:
					x_bins = json_config.pop("x_bins", [binnings_key])
					config["x_bins"] = [("1,-1,1" if (("gen_zttpospol" in nick) or ("gen_zttnegpol" in nick)) else x_bins) for nick in config["nicks"]]
				elif "--x-bins" in args.args:
					x_binning = re.search("(--x-bins)[\s=\"\']*(?P<x_bins>\S*)[\"\']?\S", args.args)
					config["x_bins"] = [" ".join(x_binning.group(2))]
					
				config["x_label"] = json_config.pop("x_label", channel + "_" + quantity)

				if args.channel_comparison:
					config["labels"] = ["channel_" + channel for channel in args.channels]
					config["title"] = ", ".join(args.samples)
				elif args.polarisation:
					config["title"] = "channel_" + channel + ("" if category is None else ("_"+category))
				else:
					config["title"] = "channel_" + channel

				config["directories"] = [args.input_dir]

				if args.channel_comparison:
					if "stacks" in config: config.pop("stacks")
					if "colors" in config: config.pop("colors")
					config["markers"] = ["LINE"]
					config["legend_markers"] = ["L"]
					config["line_widths"] = [3]

				if args.shapes:
					if "stacks" in config: config.pop("stacks")
					if "NormalizeToUnity" not in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("NormalizeToUnity")
					config["y_label"] = "arb. u."
					config["markers"] = ["LINE"]
					config["legend_markers"] = ["L"]
					config["line_widths"] = [3]

				if args.ratio:
					bkg_samples_used = [nick for nick in bkg_samples if nick in config["nicks"]]
					if "Ratio" not in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("Ratio")
					config.setdefault("ratio_numerator_nicks", []).extend([" ".join(bkg_samples_used), "data"])
					config.setdefault("ratio_denominator_nicks", []).extend([" ".join(bkg_samples_used)] * 2)
					config.setdefault("ratio_result_nicks", []).extend(["ratio_MC", "ratio_Data"])
					config.setdefault("colors", []).extend(["#000000"] * 2)
					config.setdefault("markers", []).extend(["E2", "E"])
					config.setdefault("legend_markers", []).extend(["ELP"] * 2)
					config.setdefault("labels", []).extend([""] * 2)
					config.setdefault("stacks", []).extend(["unc", "ratio"])


				for analysis_module in args.analysis_modules:
					if analysis_module not in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append(analysis_module)

				if log.isEnabledFor(logging.DEBUG) and "PrintInfos" not in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("PrintInfos")

				if "--y-log" not in args.args:
					config["y_lims"] = [0.0]
				if args.cms:
					config["cms"] = True
					config["extra_text"] = "Preliminary"
					config["legend"] = [0.7, 0.4, 0.95, 0.83] if args.ratio or args.integrated_sob or args.sbratio or args.ratio_subplot else [0.7, 0.5, 0.9, 0.85]
				elif args.shapes:
					config["legend"] = [0.55, 0.65, 0.9, 0.88]
				else:
					config["y_rel_lims"] = [0.5, 10.0] if "--y-log" in args.args else [0.0, 1.5 if args.ratio or args.integrated_sob or args.sbratio else 1.4]
					config["legend"] = [0.23, 0.63, 0.9, 0.83] if args.ratio or args.integrated_sob or args.sbratio or args.ratio_subplot else [0.23, 0.73, 0.9, 0.89]
					config["legend_cols"] = 3
				if not args.shapes:
					if args.lumi is not None:
						config["lumis"] = [float("%.1f" % args.lumi)]
					config["energies"] = [8] if args.run1 else [13]
					if not args.run1:
						config["year"] = args.era

				#add integrated s/sqrt(b) subplot
				if args.integrated_sob:
					scale_nicks_temp = []
					scale_nicks = []
					replaced_sig_nicks = []
					replaced_bkg_nicks = []
					for sample in args.integration_nicks:
						if sample in sig_samples_raw and len(args.higgs_masses) > 1:
							log.fatal("found non specific signal nick %s while plotting more than 1 mass, please use [name][mass]_[scale_signal] as specifier"%(sample))
							sys.exit()
						elif sample in sig_samples_raw:
							replaced_sig_nicks += [nick for nick in sig_samples if sample in nick]
						elif sample in bkg_samples:
							replaced_sig_nicks.append(sample)

					for sample in args.integration_backgrounds:
						if sample in sig_samples_raw and len(args.higgs_masses) > 1:
							log.fatal("found non specific signal nick %s while plotting more than 1 mass, please use [name][mass]_[scale_signal] as specifier"%(sample))
							sys.exit()
						elif sample in sig_samples_raw:
							replaced_bkg_nicks += [nick for nick in sig_samples if sample in nick]
						elif sample in bkg_samples:
							replaced_bkg_nicks.append(sample)
						elif sample == "all":
							replaced_bkg_nicks += bkg_samples
					log.debug("replace bkg + signal nicks")
					log.debug(" ".join(replaced_bkg_nicks+replaced_sig_nicks))
					for sample in replaced_bkg_nicks+replaced_sig_nicks:
						nick = sample
						if sample in sig_samples_raw and len(args.higgs_masses) > 1:
							log.fatal("found non specific signal nick %s while plotting more than 1 mass, please use [name][mass]_[scale_signal] as specifier"%(sample))
							sys.exit()
						if nick in sig_samples and args.scale_signal != 1:
							scale_nicks_temp.append(sample)
					for nick in scale_nicks_temp:
						if nick not in scale_nicks:
							scale_nicks.append(nick)
					bkg_samples_used = [nick if nick not in scale_nicks else "%s_Scaled"%nick for nick in replaced_bkg_nicks]
					sig_samples_used = [nick if nick not in scale_nicks else "%s_Scaled"%nick for nick in replaced_sig_nicks]
					if not "scale_nicks" in config.keys():
						config["analysis_modules"].append("ScaleHistograms")
						config["scale_nicks"] = []
						config["scales"] = []
						config["scale_result_nicks"] = []
					for sample in scale_nicks:
						config["scale_nicks"].append(sample)
						config["scales"].append(1.0 / args.scale_signal)
						config["scale_result_nicks"].append(sample + "_Scaled")
					log.debug(config["scale_nicks"])
					log.debug(scale_nicks)
					log.debug(bkg_samples_used)
					log.debug(sig_samples_used)
					add_s_over_sqrtb_integral_subplot(config, args, bkg_samples_used, args.integrated_sob, sig_samples_used)

				#add FullIntegral
				if args.full_integral:
					bkg_samples_used = [nick for nick in bkg_samples if nick in config["nicks"]]
					bkg_samples_used.append('data')
					if args.emb:
						config["full_integral_outputs"] = './IntegralValues_Embedded.txt'
					config["full_integral_nicks"] = [" ".join(bkg_samples_used)]
					config["analysis_modules"].append("FullIntegral")

				# add s/sqrt(b) subplot
				if args.sbratio or args.blinding_threshold > 0:
					bkg_samples_used = [nick for nick in bkg_samples if nick in config["nicks"]]
					higgs_temp = "htt125"
					if len(args.higgs_masses) > 0 and "125" not in args.higgs_masses:
						higgs_temp = "htt%i"%int(args.higgs_masses[0])
					for sample in sig_samples:
						if higgs_temp in sample:
							higgs_temp = sample
							break
					add_s_over_sqrtb_subplot(config, args, bkg_samples_used, args.sbratio, higgs_temp)

				if args.blinding_threshold > 0:
					if args.blinding_variables[0] == "all" or quantity in args.blinding_variables:
						blind_signal(config, args.blinding_threshold, args.ratio)

				config["output_dir"] = os.path.expandvars(os.path.join(
						args.output_dir,
						channel if len(args.channels) > 1 and not args.channel_comparison else "",
						category if len(args.categories) > 1 else ""
				))
				if args.ratio_subplot:
					samples_used = [nick for nick in bkg_samples if nick in config["nicks"]]
					if "Ratio" not in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("Ratio")
					config.setdefault("ratio_numerator_nicks", []).extend([str(bkg) for bkg in samples_used])
					config.setdefault("ratio_denominator_nicks", []).extend([" ".join(samples_used)] *len(samples_used) )
					config.setdefault("ratio_result_nicks", []).extend([str(bkg)+"_subplot" for bkg in samples_used])
					config.setdefault("markers", []).extend(["HIST"]*len(samples_used))
					config.setdefault("legend_markers", []).extend(["ELP"]*len(samples_used))
					config.setdefault("stacks", []).extend(["ratio_subplot"]*len(samples_used))
					config.setdefault("subplot_nicks", []).extend([str(bkg)+"_subplot" for bkg in samples_used])
					config["y_subplot_lims"] = [0.0, 1.0]
					config["y_subplot_label"] = "a.u."			

				if not args.www is None:
					config["www"] = os.path.join(
							args.www,
							channel if len(args.channels) > 1 and not args.channel_comparison else "",
							"" if category is None else category
					)

				config.update(json_config)

				if (not args.channel_comparison) or last_loop:
					plot_configs.append(config)

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)
	higgsplot.HiggsPlotter(
			list_of_config_dicts=plot_configs, list_of_args_strings=[args.args],
			n_processes=args.n_processes, n_plots=args.n_plots, batch=args.batch
	)
	"""

