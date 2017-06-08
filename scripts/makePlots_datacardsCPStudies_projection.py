#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import glob
import os
import shutil

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

import CombineHarvester.CombineTools.ch as ch

import Artus.Utility.jsonTools as jsonTools

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.datacards.datacardconfigs as datacardconfigs
import HiggsAnalysis.KITHiggsToTauTau.datacards.cpstudiesdatacards as cpstudiesdatacards
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples

def _str2bool(string):
	""" Parse string content to bool."""
	return string.lower() in ("yes", "true", "t", "1")

def poi_ranges_default(lumi):
	if lumi < 5000.0:
		return [-19.0, 21.0]
	elif lumi < 20000.0:
		return [-15.0, 16.0]
	elif lumi < 50000.0:
		return [-9.0, 11.0]
	else:
		return [-4.0, 6.0]

def poi_ranges_default_bbb(lumi):
	if lumi < 5000.0:
		return [-14.0, 16.0]
	elif lumi < 20000.0:
		return [-9.0, 11.0]
	elif lumi < 50000.0:
		return [-4.0, 6.0]
	else:
		return [-1.0, 3.0]

if __name__ == "__main__":
	
	models = {
		"default" : {
			"fit" : {
				"" : {
					"method" : "MultiDimFit",#"MaxLikelihoodFit",
					"options" : "--algo singles",
					"poi_ranges" : poi_ranges_default,
					"poi_ranges_bbb" : poi_ranges_default_bbb,
				},
			},
			"fit_plots" : {
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_mu_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_mu_split_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_mu_unc_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_mu_unc_split_over_lumi.json",
			},
		},
	}
	parser = argparse.ArgumentParser(description="Make Projections of the expected limits based on existing datacards.",
	                                 parents=[logger.loggingParser])
	parser.register("type", "bool", _str2bool)
	
	parser.add_argument("-d", "--datacards", nargs="+", required=True,
	                    help="Datacards.")
	parser.add_argument("-L", "--lumi-datacards", type=float, default=samples.default_lumi,
	                    help="Integrated luminosity / pb used for the datacards. [Default: %(default)s]")
	parser.add_argument("-l", "--lumis", nargs="+", type=int, default=range(1000, 10000, 1000)+range(10000, 100000, 10000)+[100000],#+range(100000, 300001, 100000),
	                    help="Projection values for integrated luminosities / pb. [Default: %(default)s]")
	parser.add_argument("-m", "--models", nargs="+", default=["default"],
	                    choices=models.keys(),
	                    help="Statistics models. [Default: %(default)s]")
	parser.add_argument("--freeze-syst-uncs", nargs="+", type="bool", default=[False],#, True],
	                    help="Freeze systematics (needs run without freezing first). [Default: %(default)s]")
	parser.add_argument("-r", "--ratio", default=False, action="store_true",
	                    help="Add ratio subplot. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int,
	                    help="Number of plots. [Default: all]")
	parser.add_argument("-o", "--output-dir", default=None,
	                    help="Output directory. [Default: relative to datacards]")
	parser.add_argument("--clear-output-dir", action="store_true", default=False,
	                    help="Delete/clear output directory before running this script. [Default: %(default)s]")
	parser.add_argument("--cp-mixings", nargs="+", type=float,
                        default=[mixing/100.0 for mixing in range(0, 101, 25)],
                        help="CP mixing angles alpha_tau (in units of pi/2) to be probed. [Default: %(default)s]")
	
	args = parser.parse_args()
	logger.initLogger(args)
		
	datacards_configs = datacardconfigs.DatacardConfigs()
	
	filename_templates= [
		"datacards/individual/${BINID}/${ANALYSIS}_${CHANNEL}_${BINID}_${ERA}.txt",
		"datacards/channel/${CHANNEL}/${ANALYSIS}_${CHANNEL}_${ERA}.txt",
		"datacards/category/${BINID}/${ANALYSIS}_${BINID}_${ERA}.txt",
		"datacards/combined/${ANALYSIS}_${ERA}.txt",
	]
	
	
	plot_configs = []
	for datacard in args.datacards:
		cb = ch.CombineHarvester()
		cb.SetFlag("workspaces-use-clone", True)
		for template in filename_templates:
			template_tag = template.split("$")[0]
						
			if template_tag in datacard:
				matched_template = os.path.join(datacard[:datacard.index(template_tag)], template).replace("{", "").replace("}", "")
				print datacard
				print matched_template
				cb.QuickParseDatacard(datacard, matched_template)
				break
			
		datacards = cpstudiesdatacards.CPStudiesDatacards(cb=cb)
		
		for model in args.models:
			model_settings = models.get(model, {})
			
			datacards_workspaces = {}
			for freeze_syst_uncs in args.freeze_syst_uncs:
				
				output_dir_base = args.output_dir
				if output_dir_base is None:
					output_dir_base = os.path.splitext(datacard)[0]
				sub_dir_base = os.path.join("projection", model, "statUnc" if freeze_syst_uncs else "totUnc")
				output_dir_base = os.path.abspath(os.path.expandvars(os.path.join(output_dir_base, sub_dir_base)))
				
				if args.clear_output_dir and os.path.exists(output_dir_base):
					logger.subprocessCall("rm -r " + output_dir_base, shell=True)				
				
				# scale datacards
				datacards_cbs = {}
				datacards_poi_ranges = {}
				for lumi in args.lumis:
					output_dir = os.path.join(output_dir_base, "{:06}".format(lumi))
					if not os.path.exists(output_dir):
						os.makedirs(output_dir)
					
					scaled_datacards = cpstudiesdatacards.CPStudiesDatacards(cb=datacards.cb.deep())
					
					lumi_scale_factor = lumi / args.lumi_datacards
					scaled_datacards.scale_expectation(lumi_scale_factor, no_norm_rate_sig=True)
					#scaled_datacards.replace_observation_by_asimov_dataset("125")
					scaled_datacards.cb.PrintAll()
					scaled_datacards_cbs = scaled_datacards.write_datacards(
							os.path.basename(datacard),
							os.path.splitext(os.path.basename(datacard))[0]+"_input.root",
							output_dir
					)
					#datacards_workspaces = datacards.text2workspace(datacards_cbs, n_processes=args.n_processes)
					datacards_cbs.update(scaled_datacards_cbs)
					for scaled_datacard, cb in scaled_datacards_cbs.iteritems():
						for fit_name, fit_settings in model_settings.get("fit", {"" : {}}).iteritems():
							if freeze_syst_uncs and (("CVCF" in fit_name) or ("RVRF" in fit_name)):
								continue #TODO syst errors
				if not freeze_syst_uncs:
					datacards_workspaces = datacards.text2workspace(datacards_cbs, args.n_processes)
					
					#continue
				json_configs = []
				
				
				# fits
				for fit_name, fit_options in model_settings.get("fit", {}).iteritems():
					tmp_datacards_workspaces = datacards_workspaces[fit_name] if freeze_syst_uncs else datacards_workspaces
	
					datacards.combine(
							datacards_cbs,
							datacards_workspaces,
							None,
							args.n_processes,
							"-M MaxLikelihoodFit --redefineSignalPOIs cpmixing --expectSignal=1 -t -1 --setPhysicsModelParameters cpmixing=0.0 {stable} -n \"\"".format(stable=datacards.stable_options)
					)
					
					datacards_postfit_shapes = datacards.postfit_shapes_fromworkspace(datacards_cbs, datacards_workspaces, False, args.n_processes, "--sampling" + (" --print" if args.n_processes <= 1 else ""))
					datacards.prefit_postfit_plots(datacards_cbs, datacards_postfit_shapes, plotting_args={"ratio" : args.ratio, "args" : args.args, "x_expressions" : "genPhiStarCP"}, n_processes=args.n_processes)
					
					datacards.pull_plots(datacards_postfit_shapes, s_fit_only=False, plotting_args={"fit_poi" : ["cpmixing"], "formats" : ["pdf", "png"]}, n_processes=args.n_processes)
					datacards.print_pulls(datacards_cbs, args.n_processes, "-A -p {POI}".format(POI="cpmixing"))
				
					datacards.combine(
							datacards_cbs,
							datacards_workspaces,
							None,
							args.n_processes,
							"-M MultiDimFit --algo grid --redefineSignalPOIs cpmixing --expectSignal=1 -t -1 --setPhysicsModelParameters cpmixing=0.0 --setPhysicsModelParameterRanges cpmixing={RANGE} --points {POINTS} {STABLE} -n \"\"".format(
									STABLE=datacards.stable_options,
									RANGE="{0:f},{1:f}".format(args.cp_mixings[0]-(args.cp_mixings[1]-args.cp_mixings[0])/2.0, args.cp_mixings[-1]+(args.cp_mixings[-1]-args.cp_mixings[-2])/2.0),
									POINTS=len(args.cp_mixings)
							)
					)
					
					datacards.combine(
							datacards_cbs,
							datacards_workspaces,
							None,
							args.n_processes,
							"--expectSignal=1 -t -1 -M Asymptotic --redefineSignalPOIs cpmixing --setPhysicsModelParameters cpmixing=0.0 --setPhysicsModelParameterRanges cpmixing=0,1 --rMin 0 --rMax 100 {STABLE} -n \"\"".format(STABLE=datacards.stable_options)
					)
					
					#getting limits of the tree:
					for lumi in args.lumis:
						limit_file=os.path.join(os.path.splitext(datacard)[0],"projection/default/totUnc/"+str("{:06}".format(lumi))+"/higgsCombine.Asymptotic.mH0.root")
						file = ROOT.TFile(limit_file)
						tree = file.Get("limit")
						quantile_expected_list = []
						limits_list = []
				
						for entry in range(0, tree.GetEntries()):
							tree.GetEntry(entry)
							quantile_expected_list.append(tree.quantileExpected)
							limits_list.append(tree.limit)
						log.debug("lumi")
						log.debug("limits_list")
						log.debug("quantile_expected_list")
						log.debug("****************************************************")
				datacards.annotate_trees(tmp_datacards_workspaces, "higgsCombine*{method}*mH*.root".format(method=fit_options.get("method", "MultiDimFit")), [os.path.join(sub_dir_base, "(\d*)/.*.root")], None, args.n_processes, None, "-t limit -b lumi")
				datacards.annotate_trees(tmp_datacards_workspaces, "higgsCombine.Asymptotic.mH0.root", [os.path.join(sub_dir_base, "(\d*)/.*.root")], None, args.n_processes, None, "-t limit -b lumi")
		
		#os.path.splitext(datacard)[0]
		file=os.path.join(os.path.splitext(datacard)[0],"projection/default/totUnc/*/higgsCombine.MultiDimFit.mH*.root")
		channel=["em","et","mt","tt"]
		
		lst=[(lumi/1000) for lumi in args.lumis]
		lst.extend([max(lst)+(max(lst)-min(lst))/len(lst)])		
		lst.sort()
		lst=[str(lst[i]) for i in range(len(lst))]
		xbins=" ".join(lst)
		print xbins
		plot_configs=[]
		for i in range(len(channel)):
			config={
				"folders": [
						"limit"
						],
				"x_label": "Integrated Luminosity / fb^{-1}",
				"y_label": "CP-mixing-angle #alpha_{#tau}",
				"files": [
						file
						],
				"filename": "lumivscpmixing_normal_"+channel[i],
				"x_bins":[xbins],
				"y_bins":["20,0,1.65"],
				"x_expressions":"lumi/1000",
				"y_expressions":"cpmixing*TMath::Pi()/2",
				"weights": "deltaNLL*(t_real<=0.00001)",
				"markers": "COLZ",
				"z_label": "-2 #Delta ln(L)",
				"output_dir": os.path.join(os.path.splitext(datacard)[0],"projection/")				
			}
			plot_configs.append(config)
		config_limitsoverlumi = jsonTools.JsonDict(os.path.expandvars("HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_limit_over_lumi.json"))
		dir_list=[os.path.join(output_dir_base, "{:06}".format(lumi)) for lumi in args.lumis]
		dir_list.sort()
		config_limitsoverlumi["directories"] = " ".join(dir_list)
		config_limitsoverlumi["y_label"]="95% CL Limit on CP-mixing-angle"
		config_limitsoverlumi["x_expressions"]= "lumi/1000","0:lumi/1000","0:lumi/1000","0:lumi/1000","0:lumi/1000"
		config_limitsoverlumi["y_expressions"]="limit*TMath::Pi()/2","0:limit*TMath::Pi()/2","0:limit*TMath::Pi()/2","0:limit*TMath::Pi()/2","0:limit*TMath::Pi()/2"
		config_limitsoverlumi["output_dir"]=os.path.join(os.path.splitext(datacard)[0],"projection/")
		plot_configs.append(config_limitsoverlumi)
		print os.path.join(os.path.splitext(datacard)[0])
	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)
		
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

