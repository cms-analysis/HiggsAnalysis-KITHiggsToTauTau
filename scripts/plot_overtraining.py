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

'''Plot every combination in given folder
python plot_overtraining.py -i ../new_try/*.root -x BDT_all_all BDT_all_zll BDT_all_ztt BDT_glu_zll BDT_glu_ztt BDT_vbf_zll BDT_vbf_ztt -l "BDT_{all}^{all}" "BDT_{Z#rightarrow ll}^{all}" "BDT_{Z#rightarrow#tau#tau}^{all}" "BDT_{Z#rightarrow ll}^{ggh}" "BDT_{z#rightarrow#tau#tau}^{ggh}" "BDT_{Z#rightarrow ll}^{vbf}" "BDT_{z#rightarrow#tau#tau}^{vbf}" -f all_all all_zll all_ztt ggh_zll ggh_ztt vbf_zll vbf_ztt
basic plots
./HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -i /afs/desy.de/user/m/mschmitt/work-dir/htautau/artus/2016-02-03_22-40_analysis/merged -x all_vs_all all_vs_zll all_vs_ztt ggh_vs_zll ggh_vs_ztt vbf_vs_zll vbf_vs_ztt -a '--formats png eps --y-rel-lims 0.9 1.75 --y-subplot-label "S/#sqrt(B)" --y-subplot-lims 0.0 2.0' -s ztt zll ttj vv wj ggh qqh vh htt --sbratio -c mt -n 12 --scale-signal 250 -w '(TrainingSelectionValue>35)' -o plots/ --analysis-modules NormalizeByBinWidth
with qcd+data, all catagories
./HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -i /afs/desy.de/user/m/mschmitt/work-dir/htautau/artus/2016-02-03_22-40_analysis/merged -x all_vs_all all_vs_zll all_vs_ztt ggh_vs_zll ggh_vs_ztt vbf_vs_zll vbf_vs_ztt m_vis -a '--formats png eps --y-rel-lims 0.9 1.75 --y-subplot-label "S/#sqrt{B}" --y-subplot-lims 0.01 10.0 --y-subplot-log True' -s ztt zll ttj vv wj qcd ggh qqh vh htt data --sbratio -c mt -n 12 --scale-signal 250 -w '(TrainingSelectionValue>35)' -o plots/08_02_16/qcd_data --analysis-modules NormalizeByBinWidth --categories catMVA13TeV_mt_inclusive catMVA13TeV_mt_tight catMVA13TeV_mt_loose1 catMVA13TeV_mt_loose2 catMVA13TeV_mt_alt1 catMVA13TeV_mt_alt2 catMVA13TeV_mt_alt21 catMVA13TeV_mt_alt22 catMVA13TeV_mt_alt23 --blinding-threshold 0.5

./HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -i /afs/desy.de/user/m/mschmitt/work-dir/htautau/artus/2016-02-03_22-40_analysis/merged -x all_vs_all all_vs_zll all_vs_ztt ggh_vs_zll ggh_vs_ztt vbf_vs_zll vbf_vs_ztt m_vis -a '--formats png eps --y-rel-lims 0.9 1.75 --y-subplot-label "S/#sqrt{B}" --y-subplot-lims 0.01 10.0 --y-subplot-log True' -s ztt zll zl zj ttj vv wj qcd ggh qqh vh htt --sbratio -c mt -n 12 --scale-signal 250 -w '(TrainingSelectionValue>35)' -o plots/08_02_16/qcd_exct --analysis-modules NormalizeByBinWidth --categories catMVA13TeV_mt_ztt_low catMVA13TeV_mt_ztt_mid catMVA13TeV_mt_ztt_high catMVA13TeV_mt_inclusive -e "pZetaMiss" "pZetaVis" "iso_1" "iso_2" "mt_1" "mt_2" && ./HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -i /afs/desy.de/user/m/mschmitt/work-dir/htautau/artus/2016-02-03_22-40_analysis/merged -x all_vs_all all_vs_zll all_vs_ztt ggh_vs_zll ggh_vs_ztt vbf_vs_zll vbf_vs_ztt m_vis -a '--formats png eps --y-rel-lims 0.9 1.75 --y-subplot-label "S/#sqrt{B}" --y-subplot-lims 0.01 10.0 --y-subplot-log True' -s ztt zll zl zj ttj vv wj qcd ggh qqh vh htt --sbratio -c mt -n 12 --scale-signal 250 -w '(TrainingSelectionValue>35)' -o plots/08_02_16/qcd --analysis-modules NormalizeByBinWidth --categories catMVA13TeV_mt_ztt_low catMVA13TeV_mt_ztt_mid catMVA13TeV_mt_ztt_high catMVA13TeV_mt_inclusive
'''
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Make overtraining control plots.",
											parents=[logger.loggingParser])
	parser.add_argument("-i", "--input_file", nargs="*", required= True,
						help="Input rootfiles")
	#parser.add_argument("-x", "--quantities", nargs="*",required = True,
	#                    help="Quantities.")
	parser.add_argument("-l", "--label", nargs="*",required = False,
						default = [], help="x-label.")
	parser.add_argument("-f", "--filename", nargs="*", required = False,
						default = [], help="output filename")
	parser.add_argument("-o", "--output-dir",
							default="$CMSSW_BASE/src/plots/",
							help="Output directory. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
							help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
							help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-p", "--n-plots", type=int,
							help="Number of plots. [Default: all]")
	args = parser.parse_args()
	logger.initLogger(args)
	regex = re.compile(r"T[0-9]{1,}\.root", re.IGNORECASE)

	config_list = []
	for i,path in enumerate(args.input_file):
		if not os.path.isfile(path):
			continue
		if not ".root" in path:
			continue
		json_config = {}
		base_dict = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "BDT_overtraining.json")
		json_config = jsonTools.JsonDict(base_dict).doIncludes(
			).doComments()
		json_config["files"] = path
		trash, file_name = os.path.split(path)
		json_config["x_expressions"] = "BDT_"+regex.sub("", file_name)
		json_config["x_label"] = regex.sub("", file_name)
		json_config["filename"] = "Overtraining_"+ file_name.replace(".root", "")
		json_config["output_dir"] = os.path.join(os.path.expandvars(args.output_dir),regex.sub("", file_name))
		if len(args.label) > 0:
			json_config["x_label"] = args.label[i%len(args.label)]
		if len(args.filename) > 0:
			json_config["filename"] = args.filename[i%len(args.filename)]
		config_list.append(json_config)
	log.info("Plot all %i plots"%len(config_list))
	higgsplot.HiggsPlotter(list_of_config_dicts=config_list,
							list_of_args_strings=[args.args],
							n_processes=args.n_processes, n_plots=args.n_plots)
