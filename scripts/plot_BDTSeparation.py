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
import ROOT
import Artus.Utility.jsonTools as jsonTools
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import matplotlib.pyplot as plt

'''Plot every combination in given folder
python plot_overtraining.py -i ../new_try/*.root -x BDT_all_all BDT_all_zll BDT_all_ztt BDT_glu_zll BDT_glu_ztt BDT_vbf_zll BDT_vbf_ztt -l "BDT_{all}^{all}" "BDT_{Z#rightarrow ll}^{all}" "BDT_{Z#rightarrow#tau#tau}^{all}" "BDT_{Z#rightarrow ll}^{ggh}" "BDT_{z#rightarrow#tau#tau}^{ggh}" "BDT_{Z#rightarrow ll}^{vbf}" "BDT_{z#rightarrow#tau#tau}^{vbf}" -f all_all all_zll all_ztt ggh_zll ggh_ztt vbf_zll vbf_ztt
basic plots
./HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -i /afs/desy.de/user/m/mschmitt/work-dir/htautau/artus/2016-02-03_22-40_analysis/merged -x all_vs_all all_vs_zll all_vs_ztt ggh_vs_zll ggh_vs_ztt vbf_vs_zll vbf_vs_ztt -a '--formats png eps --y-rel-lims 0.9 1.75 --y-subplot-label "S/#sqrt(B)" --y-subplot-lims 0.0 2.0' -s ztt zll ttj vv wj ggh qqh vh htt --sbratio -c mt -n 12 --scale-signal 250 -w '(TrainingSelectionValue>35)' -o plots/ --analysis-modules NormalizeByBinWidth
with qcd+data, all catagories
./HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -i /afs/desy.de/user/m/mschmitt/work-dir/htautau/artus/2016-02-03_22-40_analysis/merged -x all_vs_all all_vs_zll all_vs_ztt ggh_vs_zll ggh_vs_ztt vbf_vs_zll vbf_vs_ztt m_vis -a '--formats png eps --y-rel-lims 0.9 1.75 --y-subplot-label "S/#sqrt{B}" --y-subplot-lims 0.01 10.0 --y-subplot-log True' -s ztt zll ttj vv wj qcd ggh qqh vh htt data --sbratio -c mt -n 12 --scale-signal 250 -w '(TrainingSelectionValue>35)' -o plots/08_02_16/qcd_data --analysis-modules NormalizeByBinWidth --categories catMVA13TeV_mt_inclusive catMVA13TeV_mt_tight catMVA13TeV_mt_loose1 catMVA13TeV_mt_loose2 catMVA13TeV_mt_alt1 catMVA13TeV_mt_alt2 catMVA13TeV_mt_alt21 catMVA13TeV_mt_alt22 catMVA13TeV_mt_alt23 --blinding-threshold 0.5

./HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -i /afs/desy.de/user/m/mschmitt/work-dir/htautau/artus/2016-02-03_22-40_analysis/merged -x all_vs_all all_vs_zll all_vs_ztt ggh_vs_zll ggh_vs_ztt vbf_vs_zll vbf_vs_ztt m_vis -a '--formats png eps --y-rel-lims 0.9 1.75 --y-subplot-label "S/#sqrt{B}" --y-subplot-lims 0.01 10.0 --y-subplot-log True' -s ztt zll zl zj ttj vv wj qcd ggh qqh vh htt --sbratio -c mt -n 12 --scale-signal 250 -w '(TrainingSelectionValue>35)' -o plots/08_02_16/qcd_exct --analysis-modules NormalizeByBinWidth --categories catMVA13TeV_mt_ztt_low catMVA13TeV_mt_ztt_mid catMVA13TeV_mt_ztt_high catMVA13TeV_mt_inclusive -e "pZetaMiss" "pZetaVis" "iso_1" "iso_2" "mt_1" "mt_2" && ./HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -i /afs/desy.de/user/m/mschmitt/work-dir/htautau/artus/2016-02-03_22-40_analysis/merged -x all_vs_all all_vs_zll all_vs_ztt ggh_vs_zll ggh_vs_ztt vbf_vs_zll vbf_vs_ztt m_vis -a '--formats png eps --y-rel-lims 0.9 1.75 --y-subplot-label "S/#sqrt{B}" --y-subplot-lims 0.01 10.0 --y-subplot-log True' -s ztt zll zl zj ttj vv wj qcd ggh qqh vh htt --sbratio -c mt -n 12 --scale-signal 250 -w '(TrainingSelectionValue>35)' -o plots/08_02_16/qcd --analysis-modules NormalizeByBinWidth --categories catMVA13TeV_mt_ztt_low catMVA13TeV_mt_ztt_mid catMVA13TeV_mt_ztt_high catMVA13TeV_mt_inclusive
'''

def makePlot(x_vals, y_val_list, y_err_list, x_names, channel, category, bdt, output_dir):
	fig = plt.figure()
	ax = fig.add_subplot(111)
	nice_channel = {
		"em": "$e\\mathrm{\\mu}$",
		"mt": "$\\mathrm{\\mu\\tau}$",
		"et": "$e\\mathrm{\\tau}$",
		"tt": "$\\mathrm{\\tau\\tau}$"}

	for i,(yvals, y_errs) in enumerate(zip(y_val_list, y_err_list)):
		ax.plot(x_vals, yvals, label="CV-T%i"%(i+1), marker="x", markersize = 12.5, ls = "None", markeredgewidth=2)

	#ax.set_xticklabels(x_names)
	#ax.set_xticks(x_vals)
	ax.set_xlim(-0.2, 1.2*max(x_vals))
	lgd = ax.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0., numpoints=1)
	ax.set_xlabel("Iteration", size="x-large", ha='right', x=0.97)
	ax.set_ylabel("Separation", size="x-large", va='top', y=0.97)
	ans = ax.set_title("{channel}\t{category} - {bdt}".format(channel=nice_channel[channel], category=category, bdt=bdt), ha='left', x=0.01, y=1.01, size="x-large")
	plot_name = os.path.join(output_dir, "%s_%s_%s"%(channel,category,bdt))
	plt.savefig("%s.png"%plot_name, bbox_extra_artists=(lgd, ans), bbox_inches='tight')
	plt.savefig("%s.pdf"%plot_name, bbox_extra_artists=(lgd, ans), bbox_inches='tight')
	log.info("create plot %s.png"%plot_name)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Make overtraining control plots.",
											parents=[logger.loggingParser])
	parser.add_argument("-i", "--input_file", nargs="*", required= True,
						help="Input rootfiles")
	#parser.add_argument("-x", "--quantities", nargs="*",required = True,
	#                    help="Quantities.")
	#parser.add_argument("-l", "--label", nargs="*",required = False,
						#default = [], help="x-label.")
	parser.add_argument("-f", "--filename", nargs="*", required = False,
						default = [], help="output filename")
	parser.add_argument("-o", "--output-dir",
							default="$CMSSW_BASE/src/plots/",
							help="Output directory. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
							help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	#parser.add_argument("-n", "--n-processes", type=int, default=1,
							#help="Number of (parallel) processes. [Default: %(default)s]")
	#parser.add_argument("-p", "--n-plots", type=int,
							#help="Number of plots. [Default: all]")
	#parser.add_argument("--calculate-separation", action="store_true", default =False,
							#help="calculate separation using TestSample")
	#parser.add_argument("--no-plot", action="store_true", default =False,
							#help="skip plotting")
	args = parser.parse_args()
	logger.initLogger(args)
	if not os.path.exists(args.output_dir):
		os.makedirs(args.output_dir)
	bdt_name = {}
	for in_file in args.input_file:
		with open(in_file) as in_stream:
			begin = False
			for line in in_stream:

				if begin and ":" in line:
					cat, vals = line.split(": ")
					if not cat in bdt_name.keys():
						bdt_name[cat] = [vals]
					else:
						bdt_name[cat].append(vals)
					if args.args in line:
						print line, "store in %s"%cat
				elif '===Maxima===' in line:
					begin = True
	for cat in bdt_name.keys():
		if bdt_name[cat]:
			end_string = cat[-2:]
			cat = cat.replace(end_string, "")
			cat1 = cat + "T1"
			cat2 = cat + "T2"
			vars1 = bdt_name[cat1]
			vars2 = bdt_name[cat2]
			bdt_name[cat1] = False
			bdt_name[cat2] = False
			var1_names = []
			var2_names = []
			var1_y = []
			var2_y = []
			var1_err = []
			var2_err = []
			x_range = [x for x in range(len(vars1))]
			for var in vars1:
				(name, val, err) = var.split(" ")
				val = float(val)
				var1_names.append(name.replace("T1", ""))
				var1_y.append(val)
				var1_err.append(float(err))
			for var in vars2:
				(name, val, err) = var.split(" ")
				val = float(val)
				var2_names.append(name.replace("T2", ""))
				var2_y.append(val)
				var2_err.append(float(err))
			x_names = []
			for name1, name2 in zip(var1_names, var2_names):
				if name1 == name2:
					x_names.append('1')
				else:
					x_names.append('2')
			(trash, channel, category, bdt) = cat.split("_")
			makePlot(x_range, [var1_y, var2_y], [var1_err, var2_err], x_names, channel, category, bdt, args.output_dir)