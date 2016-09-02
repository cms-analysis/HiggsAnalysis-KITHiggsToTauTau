#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse, copy, os, re, sys
import glob
import ROOT
import matplotlib.pyplot as plt
import Artus.Utility.jsonTools as jsonTools
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.expressions as expressions
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2015 as samples

def plot_overlap(triple_list, names, file_path="Testfile", **kwargs):
	fig = plt.figure()
	ax = fig.add_subplot(111)
	c1_left=[]
	c1_width=[]
	c1_bottom=[]
	c1_height=[]
	c2_left=[]
	c2_width=[]
	c2_bottom=[]
	c2_height=[]
	c3_width=[]
	ax.set_xlim(-1, 3+max(map(sum, triple_list)))
	right_border = 2+max(map(sum, triple_list))
	#triples[0] = (cat1, cat2, overlap)
	for i,triple in enumerate(triple_list):
		c1_left.append(1)
		c1_width.append(triple[0]+triple[2])
		c1_bottom.append(2*i+0.5)
		c1_height.append(1)
		c2_left.append(1+triple[0])
		c2_width.append(triple[1]+triple[2])
		c3_width.append(triple[2])
		ax.annotate("%1.2f"%triple[0], xy=(0, 2*i+1), size="x-large")
		ax.annotate("%1.2f"%triple[1], xy=(1.5+sum(triple), 2*i+1), size="x-large")
		if not i == len(triple_list)-1:
			ax.annotate("%1.2f"%triple[2], xy=(1+triple[0]+0.5*triple[2], 2*i+1), size="x-large")

	ax.barh(left=c1_left, width=c1_width, bottom=c1_bottom, height=c1_height, edgecolor = "blue", facecolor="none", label=kwargs.get("labels", ["classic", "tagger"])[0])
	ax.barh(left=c2_left,width=c2_width, bottom=c1_bottom, height=c1_height, edgecolor = "red", facecolor="none", label=kwargs.get("labels", ["classic", "tagger"])[1])
	ax.barh(left=c2_left,width=c3_width, bottom=c1_bottom, height=c1_height, edgecolor = "none", facecolor="green", hatch="/", alpha=0.15, label="overlap", zorder=1)
	ax.set_yticks([2*x+1 for x in range(len(names))])
	ax.set_xticks([])
	ax.set_yticklabels(names, size='x-large', va='center', ha='right', rotation_mode='anchor')

	plt.title(kwargs.get("title", "Event Overlap: "))
	ax.set_ylim(0, 2*len(names))
	ax.set_ylabel("")
	ax.set_xlabel("")
	lgd = ax.legend(bbox_to_anchor=(0.75, 1), loc=2, borderaxespad=0.)
	#fig.tight_layout()
	plt.savefig("%s.png"%file_path, bbox_extra_artists=(lgd,), bbox_inches='tight')
	plt.savefig("%s.pdf"%file_path, bbox_extra_artists=(lgd,), bbox_inches='tight')
	plt.savefig("%s.eps"%file_path, bbox_extra_artists=(lgd,), bbox_inches='tight')
	log.info("create plot %s.png"%file_path)
	log.info("create plot %s.pdf"%file_path)
	log.info("create plot %s.eps"%file_path)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Plot overlapping signal events.",
									 parents=[logger.loggingParser])
	parser.add_argument("-i", "--input-dir",
						help="Path to ArtusOutput")
	parser.add_argument("-m", "--higgs-masses",nargs="+", default = ["125"],
						help="higgs mass [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-f", "--first-category", nargs="+", default=[],
	                    help="First Categories, can be specified multiple times. Several categories specified at once will be concatenated with or [Default: %(default)s]")
	parser.add_argument("-s", "--second-category", nargs="+", default=[],
						help="Second Categories, can be specified multiple times. Several categories specified at once will be concatenated with or[Default: %(default)s]")
	parser.add_argument("-S", "--Samples", nargs="+", default=["ggh", "qqh"],
	                    help="Samples to be compared [Default: %(default)s]")
	parser.add_argument("-o", "--output-dir",
						default="./",
						help="path to output file. [Default: %(default)s]")
	parser.add_argument("--filename",
						default="./",
						help="name of output file. [Default: %(default)s]")
	parser.add_argument("--labels", nargs="+",
						default=["classic", "VBF-tagger"],
						help="label names. [Default: %(default)s]")
	#parser.add_argument("-T", "--Ticklabels", nargs="+", default=["Category1", "Category2", "Overlap"],
	                    #help="Ticklabels, replace by first name in first and second [Default: %(default)s]")
	parser.add_argument("-c", "--channel",
						default="mt",
						help="Channel. [Default: %(default)s]")
	parser.add_argument("--title",
						default="Category Overlap",
						help="Title [Default: %(default)s]")
	parser.add_argument("-e", "--exclude-cuts", nargs="+", default=[],
						help="Exclude (default) selection cuts. [Default: %(default)s]")
	parser.add_argument("-r", "--ratio", nargs="+", default=["qqh"],
						help="List of Numerator samples. [Default: %(default)s]")
	parser.add_argument("--ratio-title",
						default="VBF/ggh",
						help="Title for ratio [Default: %(default)s]")

	args = parser.parse_args()
	logger.initLogger(args)

	exp_dict = expressions.ExpressionsDict()
	plot_configs = []
	list_of_samples = [getattr(samples.Samples, sample) for sample in args.Samples]
	sample_settings = samples.Samples()

	config = sample_settings.get_config(
	samples=list_of_samples,
	channel=args.channel,
	category="1.0",
	weight="1.0",
	higgs_masses=args.higgs_masses,
	normalise_signal_to_one_pb=False,
	exclude_cuts=args.exclude_cuts
	)
	firsts = [exp_dict.replace_expressions(s) for s in args.first_category]
	seconds = [exp_dict.replace_expressions(s) for s in args.second_category]
	config["x_expressions"] = ["1*({first})+2*({second})".format(first=" || ".join(firsts), second=" || ".join(seconds))]
	#config["x_expressions"] = ["m_sv"]

	#config["x_ticks"] = [1,2,3]
	config["x_bins"] = ["3,0.5,3.5"]
	#config["x_tick_labels"] = args.Ticklabels
	config["filename"] = args.filename
	config["output_dir"] = args.output_dir
	config["directories"] = [args.input_dir]
	args.args += " --plot-modules ExportRoot"
	#print config
	higgsplot.HiggsPlotter(list_of_config_dicts=[config],
							list_of_args_strings=[args.args])
	names = []
	ratio_names = []
	for nick in args.Samples:
		for mass in args.higgs_masses:
			add = nick
			if nick in ("ggh", "qqh", "vh"):
				add += "%s"%mass
			names.append(add)
			if nick in args.ratio:
				ratio_names.append(add)

	#sys.exit()
	tfile = ROOT.TFile(os.path.join(args.output_dir, args.filename+".root"), "READ")
	#ztt = tfile.Get("ztt")
	#zll = tfile.Get("zll")
	#wj = tfile.Get("wj")
	#qcd = tfile.Get("qcd")
	#vv = tfile.Get("vv")
	#data = tfile.Get("data")
	#ttj = tfile.Get("ttj")
	#qqh = tfile.Get("qqh125")
	#ggh = tfile.Get("ggh125")
	triples = []
	#triples[0] = (cat1, cat2, overlap)
	denominator = [0,0,0]
	numerator = [0,0,0]
	for i,name in enumerate(names):
		histogram = tfile.Get(name)
		triples.append([])
		for n in range(1, histogram.GetNbinsX()+1):
			#print histogram.GetBinContent(n)
			triples[-1].append(histogram.GetBinContent(n))
			if name in ratio_names:
				numerator[n-1]+=histogram.GetBinContent(n)
			else:
				denominator[n-1]+=histogram.GetBinContent(n)
		names[i] = names[i].replace("qqh", "VBF")
		names[i] = names[i].replace("h", "H")
	denominator[0] += denominator[2]
	denominator[1] += denominator[2]
	denominator[2] = 1
	numerator[0] += numerator[2]
	numerator[1] += numerator[2]
	numerator[2] = 0
	ratio = [numerator[x]/denominator[x] if denominator[x]>0 else 0 for x in range(3)]
	if len(args.ratio) > 0:
		names.append(args.ratio_title)
		triples.append(ratio)
	print triples
	print names
	#sys.exit()
	plot_overlap(triples, names, os.path.join(args.output_dir, args.filename), **vars(args))

