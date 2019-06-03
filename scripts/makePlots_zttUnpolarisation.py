#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os

import Artus.Utility.tools as tools
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Study unpolarisation of ZTT MC samples.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-c", "--channel", action = "append",
	                    default=["gen"],
	                    help="Channel. This agument can be set multiple times. [Default: %(default)s]")
	parser.add_argument("--categories", action="append", nargs="+",
	                    default=["inclusive"],
	                    help="Categories per channel. This agument needs to be set as often as --channels. [Default: %(default)s]")
	parser.add_argument("--alpha-s-weights", nargs="+",
	                    default=["NNPDF30_lo_as_0118_LHgrid__Member_0"],
	                    help="LHE weights for alpha_s uncertainty evaluation. [Default: %(default)s]")
	parser.add_argument("--pdf-weights", nargs="+",
	                    default=["NNPDF30_lo_as_0130_LHgrid__Member_0", "NNPDF30_lo_as_0130_LHgrid__Member_1", "NNPDF30_lo_as_0130_LHgrid__Member_2", "NNPDF30_lo_as_0130_LHgrid__Member_3", "NNPDF30_lo_as_0130_LHgrid__Member_4", "NNPDF30_lo_as_0130_LHgrid__Member_5", "NNPDF30_lo_as_0130_LHgrid__Member_6", "NNPDF30_lo_as_0130_LHgrid__Member_7", "NNPDF30_lo_as_0130_LHgrid__Member_8", "NNPDF30_lo_as_0130_LHgrid__Member_9", "NNPDF30_lo_as_0130_LHgrid__Member_10", "NNPDF30_lo_as_0130_LHgrid__Member_11", "NNPDF30_lo_as_0130_LHgrid__Member_12", "NNPDF30_lo_as_0130_LHgrid__Member_13", "NNPDF30_lo_as_0130_LHgrid__Member_14", "NNPDF30_lo_as_0130_LHgrid__Member_15", "NNPDF30_lo_as_0130_LHgrid__Member_16", "NNPDF30_lo_as_0130_LHgrid__Member_17", "NNPDF30_lo_as_0130_LHgrid__Member_18", "NNPDF30_lo_as_0130_LHgrid__Member_19", "NNPDF30_lo_as_0130_LHgrid__Member_20", "NNPDF30_lo_as_0130_LHgrid__Member_21", "NNPDF30_lo_as_0130_LHgrid__Member_22", "NNPDF30_lo_as_0130_LHgrid__Member_23", "NNPDF30_lo_as_0130_LHgrid__Member_24", "NNPDF30_lo_as_0130_LHgrid__Member_25", "NNPDF30_lo_as_0130_LHgrid__Member_26", "NNPDF30_lo_as_0130_LHgrid__Member_27", "NNPDF30_lo_as_0130_LHgrid__Member_28", "NNPDF30_lo_as_0130_LHgrid__Member_29", "NNPDF30_lo_as_0130_LHgrid__Member_30", "NNPDF30_lo_as_0130_LHgrid__Member_31", "NNPDF30_lo_as_0130_LHgrid__Member_32", "NNPDF30_lo_as_0130_LHgrid__Member_33", "NNPDF30_lo_as_0130_LHgrid__Member_34", "NNPDF30_lo_as_0130_LHgrid__Member_35", "NNPDF30_lo_as_0130_LHgrid__Member_36", "NNPDF30_lo_as_0130_LHgrid__Member_37", "NNPDF30_lo_as_0130_LHgrid__Member_38", "NNPDF30_lo_as_0130_LHgrid__Member_39", "NNPDF30_lo_as_0130_LHgrid__Member_40", "NNPDF30_lo_as_0130_LHgrid__Member_41", "NNPDF30_lo_as_0130_LHgrid__Member_42", "NNPDF30_lo_as_0130_LHgrid__Member_43", "NNPDF30_lo_as_0130_LHgrid__Member_44", "NNPDF30_lo_as_0130_LHgrid__Member_45", "NNPDF30_lo_as_0130_LHgrid__Member_46", "NNPDF30_lo_as_0130_LHgrid__Member_47", "NNPDF30_lo_as_0130_LHgrid__Member_48", "NNPDF30_lo_as_0130_LHgrid__Member_49", "NNPDF30_lo_as_0130_LHgrid__Member_50", "NNPDF30_lo_as_0130_LHgrid__Member_51", "NNPDF30_lo_as_0130_LHgrid__Member_52", "NNPDF30_lo_as_0130_LHgrid__Member_53", "NNPDF30_lo_as_0130_LHgrid__Member_54", "NNPDF30_lo_as_0130_LHgrid__Member_55", "NNPDF30_lo_as_0130_LHgrid__Member_56", "NNPDF30_lo_as_0130_LHgrid__Member_57", "NNPDF30_lo_as_0130_LHgrid__Member_58", "NNPDF30_lo_as_0130_LHgrid__Member_59", "NNPDF30_lo_as_0130_LHgrid__Member_60", "NNPDF30_lo_as_0130_LHgrid__Member_61", "NNPDF30_lo_as_0130_LHgrid__Member_62", "NNPDF30_lo_as_0130_LHgrid__Member_63", "NNPDF30_lo_as_0130_LHgrid__Member_64", "NNPDF30_lo_as_0130_LHgrid__Member_65", "NNPDF30_lo_as_0130_LHgrid__Member_66", "NNPDF30_lo_as_0130_LHgrid__Member_67", "NNPDF30_lo_as_0130_LHgrid__Member_68", "NNPDF30_lo_as_0130_LHgrid__Member_69", "NNPDF30_lo_as_0130_LHgrid__Member_70", "NNPDF30_lo_as_0130_LHgrid__Member_71", "NNPDF30_lo_as_0130_LHgrid__Member_72", "NNPDF30_lo_as_0130_LHgrid__Member_73", "NNPDF30_lo_as_0130_LHgrid__Member_74", "NNPDF30_lo_as_0130_LHgrid__Member_75", "NNPDF30_lo_as_0130_LHgrid__Member_76", "NNPDF30_lo_as_0130_LHgrid__Member_77", "NNPDF30_lo_as_0130_LHgrid__Member_78", "NNPDF30_lo_as_0130_LHgrid__Member_79", "NNPDF30_lo_as_0130_LHgrid__Member_80", "NNPDF30_lo_as_0130_LHgrid__Member_81", "NNPDF30_lo_as_0130_LHgrid__Member_82", "NNPDF30_lo_as_0130_LHgrid__Member_83", "NNPDF30_lo_as_0130_LHgrid__Member_84", "NNPDF30_lo_as_0130_LHgrid__Member_85", "NNPDF30_lo_as_0130_LHgrid__Member_86", "NNPDF30_lo_as_0130_LHgrid__Member_87", "NNPDF30_lo_as_0130_LHgrid__Member_88", "NNPDF30_lo_as_0130_LHgrid__Member_89", "NNPDF30_lo_as_0130_LHgrid__Member_90", "NNPDF30_lo_as_0130_LHgrid__Member_91", "NNPDF30_lo_as_0130_LHgrid__Member_92", "NNPDF30_lo_as_0130_LHgrid__Member_93", "NNPDF30_lo_as_0130_LHgrid__Member_94", "NNPDF30_lo_as_0130_LHgrid__Member_95", "NNPDF30_lo_as_0130_LHgrid__Member_96", "NNPDF30_lo_as_0130_LHgrid__Member_97", "NNPDF30_lo_as_0130_LHgrid__Member_98", "NNPDF30_lo_as_0130_LHgrid__Member_99", "NNPDF30_lo_as_0130_LHgrid__Member_100"],
	                    help="LHE weights for PDF uncertainty evaluation. [Default: %(default)s]")
	parser.add_argument("--qcd-scale-weights", nargs="+",
	                    default=["Central_scale_variation__mur_0_5_muf_0_5", "Central_scale_variation__mur_0_5_muf_1", "Central_scale_variation__mur_1_muf_0_5", "Central_scale_variation__mur_1_muf_1", "Central_scale_variation__mur_1_muf_2", "Central_scale_variation__mur_2_muf_1", "Central_scale_variation__mur_2_muf_2"],
	                    help="LHE weights for QCD scale (muR and muF) uncertainty evaluation. [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000.0,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int,
	                    help="Number of plots. [Default: all]")
	parser.add_argument("-o", "--output-dir",
	                    default="$CMSSW_BASE/src/TauPolSoftware/CalibrationCurve/data",
	                    help="Output directory. [Default: %(default)s]")
	parser.add_argument("--www", nargs="?", default=None, const="calibration_curve_inputs",
	                    help="Publish plots. [Default: %(default)s]")

	args = parser.parse_args()
	logger.initLogger(args)
	
	if args.channel != parser.get_default("channel"):
		args.channel = args.channel[len(parser.get_default("channel")):]

	if args.categories != parser.get_default("categories"):
		args.categories = args.categories[len(parser.get_default("categories")):]
	args.categories = (args.categories * len(args.channel))[:len(args.channel)]
	
	args.alpha_s_weights = [weight for weight in args.alpha_s_weights if weight != ""]
	args.pdf_weights = [weight for weight in args.pdf_weights if weight != ""]
	args.qcd_scale_weights = [weight for weight in args.qcd_scale_weights if weight != ""]
	
	args.output_dir = os.path.expandvars(args.output_dir)
	
	sample_settings = samples.Samples()
	
	quark_type_weights = {
		"up" : "(lheZfromUUbar+lheZfromCCbar)",
        "down" : "(lheZfromDDbar+lheZfromSSbar+lheZfromBBbar)",
	}
	
	plot_configs = []
	for channel, categories in zip(args.channel, args.categories):
		for category in categories:
			channel_category = channel+"_"+category
			
			for quark_type in ["up", "down"]:
			
				config = {}
				for index_weight, theo_unc_weight in enumerate(["1.0"] + args.alpha_s_weights + args.pdf_weights + args.qcd_scale_weights):
					weight_config = sample_settings.get_config(
							samples=[getattr(samples.Samples, sample) for sample in ["zttpospol", "zttnegpol"]],
							no_ewkz_as_dy=True,
							channel=channel,
							category="catZttPol13TeV_"+channel_category,
							weight=theo_unc_weight+"*"+quark_type_weights[quark_type],
							cut_type="low_mvis_smhtt2016",
							lumi = args.lumi * 1000,
							exclude_cuts=[],
							estimationMethod="new",
							polarisation_bias_correction=False, #True,
							polarisation_gen_ztt_plots=False,
							#forced_gen_polarisation=-0.2208,
							remove_bias_instead_unpolarisation=False, #True,
							nick_suffix = "" if index_weight == 0 else (theo_unc_weight+"_noplot") # ("" if index_weight == 0 else theo_unc_weight)+"_noplot"
					)
					config = samples.Samples.merge_configs(config, weight_config, additional_keys=[
							"ztt_pos_pol_gen_nicks", "ztt_pos_pol_reco_nicks", "ztt_pos_pol_reco_result_nicks",
							"ztt_neg_pol_gen_nicks", "ztt_neg_pol_reco_nicks", "ztt_neg_pol_reco_result_nicks",
							"ztt_forced_gen_polarisations"
					])
				
				for sample in ["zttpospol", "zttnegpol"]:
					"""
					if "AddHistograms" not in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("AddHistograms")
					config.setdefault("add_nicks", []).extend(["zttpospol{theo_unc_weight}_noplot zttnegpol{theo_unc_weight}_noplot".format(theo_unc_weight=theo_unc_weight) for theo_unc_weight in [""]+args.alpha_s_weights+args.pdf_weights+args.qcd_scale_weights])
					config.setdefault("add_result_nicks", []).extend([sample+theo_unc_weight+("" if index_weight == 0 else "_noplot") for index_weight, theo_unc_weight in enumerate([""]+args.alpha_s_weights+args.pdf_weights+args.qcd_scale_weights)])
					"""
					
					final_uncertainties = []
					if len(args.alpha_s_weights) > 0:
						if "UncertaintiesAlphaS" not in config.get("analysis_modules", []):
							config.setdefault("analysis_modules", []).append("UncertaintiesAlphaS")
						config.setdefault("uncertainties_alpha_s_reference_nicks", []).append(sample)
						config.setdefault("uncertainties_alpha_s_shifts_nicks", []).append(" ".join([sample+theo_unc_weight+"_noplot" for theo_unc_weight in args.alpha_s_weights]))
						config.setdefault("uncertainties_alpha_s_result_nicks", []).append(sample+"_alpha_s")
						final_uncertainties.append("alpha_s")
						
					if len(args.pdf_weights) > 0:
						if "UncertaintiesPdf" not in config.get("analysis_modules", []):
							config.setdefault("analysis_modules", []).append("UncertaintiesPdf")
						config.setdefault("uncertainties_pdf_reference_nicks", []).append(sample)
						config.setdefault("uncertainties_pdf_shifts_nicks", []).append(" ".join([sample+theo_unc_weight+"_noplot" for theo_unc_weight in args.pdf_weights]))
						config.setdefault("uncertainties_pdf_result_nicks", []).append(sample+"_pdf")
						config.setdefault("nicks_blacklist", []).append("_correlation")
						final_uncertainties.append("pdf")
						
					if len(args.qcd_scale_weights) > 0:
						if "UncertaintiesScale" not in config.get("analysis_modules", []):
							config.setdefault("analysis_modules", []).append("UncertaintiesScale")
						config.setdefault("uncertainties_scale_reference_nicks", []).append(sample)
						config.setdefault("uncertainties_scale_shifts_nicks", []).append(" ".join([sample+theo_unc_weight+"_noplot" for theo_unc_weight in args.qcd_scale_weights]))
						config.setdefault("uncertainties_scale_result_nicks", []).append(sample+"_qcd_scale")
						final_uncertainties.append("qcd_scale")
				
				if "Unpolarisation" not in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("Unpolarisation")
				config.setdefault("unpolarisation_nominal_pos_pol_nicks", []).append("zttpospol")
				config.setdefault("unpolarisation_nominal_neg_pol_nicks", []).append("zttnegpol")
				
				if len(final_uncertainties) > 0:
					config.setdefault("unpolarisation_shift_up_pos_pol_nicks", []).append(" ".join(["zttpospol_"+unc+"_up" for unc in final_uncertainties]))
					config.setdefault("unpolarisation_shift_down_pos_pol_nicks", []).append(" ".join(["zttpospol_"+unc+"_down" for unc in final_uncertainties]))
					config.setdefault("unpolarisation_shift_up_neg_pol_nicks", []).append(" ".join(["zttnegpol_"+unc+"_up" for unc in final_uncertainties]))
					config.setdefault("unpolarisation_shift_down_neg_pol_nicks", []).append(" ".join(["zttnegpol_"+unc+"_down" for unc in final_uncertainties]))
				else:
					config.setdefault("unpolarisation_shift_up_pos_pol_nicks", []).append(None)
					config.setdefault("unpolarisation_shift_down_pos_pol_nicks", []).append(None)
					config.setdefault("unpolarisation_shift_up_neg_pol_nicks", []).append(None)
					config.setdefault("unpolarisation_shift_down_neg_pol_nicks", []).append(None)
				
				config.setdefault("unpolarisation_scale_factor_pos_pol_nicks", []).append("unpol_pos")
				config.setdefault("unpolarisation_scale_factor_neg_pol_nicks", []).append("unpol_neg")
				config.setdefault("unpolarisation_polarisation_before_nicks", []).append("unpol_before")
				config.setdefault("unpolarisation_polarisation_after_nicks", []).append("unpol_after")
				
				config.setdefault("subplot_nicks", []).append("unpol")
				config.setdefault("nicks_blacklist", []).extend(["_up", "_down"])
				
				for key in ["stacks", "legend_markers"]:
					if key in config:
						config.pop(key)
				
				config["directories"] = [args.input_dir]
				
				config["x_expressions"] = [("0" if (("gen_zttpospol" in nick) or ("gen_zttnegpol" in nick)) else "genbosonmass") for nick in config["nicks"]]
				
				binning = " ".join(map(str, range(10, 40, 2)+range(40, 80, 4)+range(80, 120, 1)+range(120, 180, 5)+[180, 200, 300, 10000]))
				config["x_bins"] = [("1,-1,1" if (("gen_zttpospol" in nick) or ("gen_zttnegpol" in nick)) else [binning]) for nick in config["nicks"]]
				
				config["labels"] = [os.path.join(channel_category, unc_type) for unc_type in ["nominal", "alpha_s_up", "alpha_s_down", "pdf_up", "pdf_down", "qcd_scale_up", "qcd_scale_down"]]
				config["output_dir"] = os.path.join(args.output_dir, channel, category)
				config["filename"] = "energy_distribution_"+quark_type
				
				if not args.www is None:
					config["www"] = os.path.join(args.www, channel, category)
				
				plot_configs.append(config)
	
	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)

	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

