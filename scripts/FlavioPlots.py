#! /usr/bin/env python

import os
import string
import yaml
import argparse
from multiprocessing import Pool, cpu_count

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot

import ROOT

##Global Constants
parameter_yaml = os.environ["CMSSW_BASE"] + "/src/FlavioOutput/Configs/parameter.yaml"
plot_dir = os.environ["CMSSW_BASE"] + "/src/FlavioOutput/Plots/"

##ROOT plotting configuration
labels = {"ztt": "Z#rightarrow#tau#tau", "zll": "Z#rightarrow ll", "ttj": "t#bar{t}", "wj": "W + jets", "vv": "WW/ZZ/WZ", "qcd": "QCD", "zem": "Z#rightarrow e#mu", "zet": "Z#rightarrow e#tau", "zmt": "Z#rightarrow #mu#tau", "data": "Data", "zetm": "Z#rightarrow e#tau_{#mu}", "zmte": "Z#rightarrow #mu#tau_{e}"}
colors = {"ztt": ROOT.kYellow, "zll": ROOT.kAzure+1, "ttj": ROOT.kViolet-3, "wj": ROOT.kRed+1, "vv": ROOT.kOrange+5, "qcd": ROOT.kPink+1}
title = {"em": "e#mu", "etm": "e#mu", "mte": "e#mu", "et": "e#tau_{h}", "mt": "#mu#tau_{h}"}


def parser():
	parser = argparse.ArgumentParser(description = "Script for calculating plotting in LFV analysis", formatter_class=argparse.RawTextHelpFormatter)

	parser.add_argument("--channel", nargs="+", required = True, choices = ["em", "et", "mt", "etm", "mte"] , help = "Channel which should be analyzed")
	parser.add_argument("--parameter", nargs="+", required = True, help = "Parameter to plot")
	parser.add_argument("--shape", action = "store_true", help = "Draw shape histos for background/signal")
	parser.add_argument("--data", nargs='?', const="", help = "Plot with real data, to set region of blinding use --data 'start stop'")
	parser.add_argument("--weight", action = "store", default="1", help = "Weight applied while tree is read out")
	parser.add_argument("--name-suffix", action = "store", default = "", help = "Optional suffix for the output name of the plot")
	parser.add_argument("--www", action = "store", default = "", help = "Directory name of web plotting, in which plot should be safed if wished")
	return parser.parse_args()

def get_hists(parameter, base_config, binning, channel):
	##Get shapes for variables
	config = base_config + {
		"directories":	"/net/scratch_cms3b/{}/artus/AllSamples/merged/".format(os.environ["USER"]),
		"x_expressions": parameter,
		"plot_modules": ["ExportRoot"],
		"output_dir": plot_dir + channel,
		"x_bins": binning,
		"file_mode": "UPDATE",
		"filename": parameter,
	}
	config.pop("legend_markers")


	higgsplot.HiggsPlotter(list_of_config_dicts=[config])

def plot(parameter, channel, processes, plotname, x_label, data, name_suffix, www):
	##Get all hists
	hist_file = ROOT.TFile(plot_dir + channel + "/" + parameter + ".root", "READ")
	hists = [hist_file.Get(process) for process in processes]

	##Legend
	ROOT.gStyle.SetLegendBorderSize(0)
	ROOT.gStyle.SetFillStyle(0)
	legend = ROOT.TLegend()
	legend.SetX1NDC(0.65)
	legend.SetX2NDC(0.95)
	legend.SetY1NDC(0.7)
	legend.SetY2NDC(0.9)

	##Stacked background histogram
	stacked_hist = ROOT.THStack()
	bkgsum_hist = hists[0].Clone()

	for index, (hist, process) in enumerate(zip(hists[:-2], processes[:-2])):
		hist.SetFillColor(colors[process])
		hist.SetLineColor(colors[process])
		
		if index != 0:
			bkgsum_hist.Add(hist)

		legend.AddEntry(hist, labels[process], "F")
		stacked_hist.Add(hist)

	##Signal histogram
	sig_hist = hists[-2]
	sig_hist.SetLineColor(ROOT.kBlack)
	sig_hist.SetLineWidth(4)
	sig_hist.Scale(50)
	legend.AddEntry(sig_hist, labels[processes[-2]] + " x50", "L")

	if data != None:
		##Data histogram
		data_hist = hists[-1]
	
		data_graph = ROOT.TGraphErrors()
		data_graph.SetMarkerStyle(20)
	
		legend.AddEntry(data_graph, labels["data"], "LP")

		##Data/Bkg ratio histogram
		ratio_hist = data_hist.Clone()
		ratio_hist.Divide(bkgsum_hist)
	
		errorband = bkgsum_hist.Clone()
		errorband.Divide(bkgsum_hist)

		errorband.SetFillColor(ROOT.kGray)
		errorband.SetMarkerColor(ROOT.kWhite)
		errorband.SetFillStyle(4050)
		errorband.SetStats(0)

		ratio_graph = ROOT.TGraphErrors()
		ratio_graph.SetMarkerStyle(20)

		##Blind data in signal range
		start, stop = [0,0] if data == "" else [float(number) for number in data.split(" ")]

		for index in range(data_hist.GetNbinsX()):
			if sig_hist.GetBinContent(index+1) < 200 and data_hist.GetBinContent(index+1)!=0 and not start < data_hist.GetBinCenter(index+1) < stop:
				data_graph.SetPoint(index, data_hist.GetBinCenter(index+1), data_hist.GetBinContent(index+1))
				data_graph.SetPointError(index, data_hist.GetBinWidth(index+1)/2., data_hist.GetBinError(index+1))

				ratio_graph.SetPoint(index, ratio_hist.GetBinCenter(index+1), ratio_hist.GetBinContent(index+1))
				ratio_graph.SetPointError(index, ratio_hist.GetBinWidth(index+1)/2., ratio_hist.GetBinError(index+1))


	##CMS and lumi text
	channel_title = ROOT.TLatex()
	channel_title.SetTextFont(42)
	channel_title.SetTextSize(0.03)

	lumi = ROOT.TLatex()
	lumi.SetTextFont(42)
	lumi.SetTextSize(0.03)

	cms = ROOT.TLatex()
	cms.SetTextFont(62)
	cms.SetTextSize(0.029)

	work = ROOT.TLatex()
	work.SetTextFont(52)
	work.SetTextSize(0.03)

	#Draw all things
	canvas = ROOT.TCanvas("c", "c", 800,800)
	canvas.SetLeftMargin(0.15)

	stacked_hist.Draw("HIST")
	sig_hist.Draw("SAME HIST")
	
	if data != None:
		data_graph.Draw("SAME P")

	legend.Draw("SAME")

	channel_title.DrawLatexNDC(0.17, 0.905, title[channel])
	lumi.DrawLatexNDC(0.605, 0.905, "35.87 fb^{-1} (2016, 13 TeV)")
	cms.DrawLatexNDC(0.25, 0.905, "CMS")
	work.DrawLatexNDC(0.318, 0.905, "Work in progress")

	##Axis options
	stacked_hist.SetMinimum(0)
	stacked_hist.SetMaximum(1.5*bkgsum_hist.GetBinContent(bkgsum_hist.GetMaximumBin()))
	stacked_hist.GetXaxis().SetTitle(x_label)
	stacked_hist.GetXaxis().SetLabelSize(0.025)
	stacked_hist.GetYaxis().SetTitle("Events")
	stacked_hist.GetYaxis().SetTitleOffset(1.8)
	stacked_hist.GetYaxis().SetLabelSize(0.025)
	ROOT.TGaxis().SetMaxDigits(3)
	
	if data != None:
		##Draw pad for ratio plot
		canvas.SetBottomMargin(0.35)
		pad1 = ROOT.TPad("pad1", "pad1", 0, 0.08, 1, 0.31)
		pad1.SetLeftMargin(0.15)
		pad1.SetBottomMargin(0.21)
		pad1.Draw()
		pad1.cd()	
		
		##Draw ratio
		errorband.Draw("E5")
		ratio_graph.Draw("SAME P")

		##Axis options
		errorband.SetTitle("")
		stacked_hist.GetXaxis().SetTitleOffset(5.5)
		errorband.GetXaxis().SetLabelSize(0.1)
		errorband.SetAxisRange(0.6, 1.4, "Y")
		errorband.GetYaxis().SetTitle("#frac{Data}{MC}")
		errorband.GetYaxis().SetTitleSize(0.12)
		errorband.GetYaxis().SetLabelSize(0.1)
		errorband.GetYaxis().SetTitleOffset(0.5)

	##Save Histogram
	ROOT.gPad.RedrawAxis()
	ROOT.gPad.SetTicky()
	ROOT.TGaxis.SetExponentOffset(-0.05, 0.005, "y")

	canvas.SaveAs(plot_dir + channel + "/{}{}.pdf".format(plotname, name_suffix))
	print "Saved plot: {}".format(plot_dir + channel + "/{}{}.pdf".format(plotname, name_suffix))

	if www != "":
		os.system("mkdir -p " + os.environ["CMSSW_BASE"] + "/src/FlavioOutput/WebPlots/{}/{}".format(channel, www))
		canvas.SaveAs(os.environ["CMSSW_BASE"] + "/src/FlavioOutput/WebPlots/{}/{}".format(channel, www) + "/{}{}.png".format(plotname, name_suffix))

def shape_plot(parameter, channel, processes, plotname, x_label, name_suffix, www):
	##Get all hists without data hist
	hist_file = ROOT.TFile(plot_dir + channel + "/" + parameter + ".root", "READ")
	hists = [hist_file.Get(process) for process in processes[:-1]]

	##Legend
	ROOT.gStyle.SetLegendBorderSize(0)
	ROOT.gStyle.SetFillStyle(0)
	legend = ROOT.TLegend()
	legend.SetX1NDC(0.7)
	legend.SetX2NDC(0.9)
	legend.SetY1NDC(0.7)
	legend.SetY2NDC(0.9)

	##Hist for bkg sum
	bkgsum_hist = hists[0].Clone()
	bkgsum_hist.SetFillStyle(3353)
	bkgsum_hist.SetFillColor(ROOT.kRed)
	bkgsum_hist.SetLineColor(ROOT.kRed+1)
	bkgsum_hist.SetLineWidth(4)
	legend.AddEntry(bkgsum_hist, "Background", "F")
	
	for index, (hist, process) in enumerate(zip(hists[1:-1], processes[:-2])):
		bkgsum_hist.Add(hist)

	##signal hist
	sig_hist = hists[-1]
	sig_hist.SetFillStyle(3335)
	sig_hist.SetFillColor(ROOT.kBlue)
	sig_hist.SetLineColor(ROOT.kBlue+1)
	sig_hist.SetLineWidth(4)
	legend.AddEntry(sig_hist, "Signal", "F")

	##CMS and lumi text
	channel_title = ROOT.TLatex()
	channel_title.SetTextFont(42)
	channel_title.SetTextSize(0.03)

	lumi = ROOT.TLatex()
	lumi.SetTextFont(42)
	lumi.SetTextSize(0.03)

	cms = ROOT.TLatex()
	cms.SetTextFont(62)
	cms.SetTextSize(0.029)

	work = ROOT.TLatex()
	work.SetTextFont(52)
	work.SetTextSize(0.03)

	##Axis options
	sig_hist.SetMaximum(1.5*sig_hist.GetBinContent(sig_hist.GetMaximumBin()))
	sig_hist.GetXaxis().SetTitle(x_label)
	sig_hist.GetXaxis().SetLabelSize(0.025)
	sig_hist.GetYaxis().SetTitle("Events")
	sig_hist.GetYaxis().SetTitleOffset(1.8)
	sig_hist.GetYaxis().SetLabelSize(0.025)

	#Draw all things
	canvas = ROOT.TCanvas("c", "c", 800,800)
	canvas.SetLeftMargin(0.15)

	sig_hist.DrawNormalized("HIST")
	bkgsum_hist.DrawNormalized("SAME HIST")
	legend.Draw("SAME")

	channel_title.DrawLatexNDC(0.17, 0.905, title[channel])
	lumi.DrawLatexNDC(0.605, 0.905, "35.87 fb^{-1} (2016, 13 TeV)")
	cms.DrawLatexNDC(0.25, 0.905, "CMS")
	work.DrawLatexNDC(0.318, 0.905, "Work in progress")

	##Save Histogram
	ROOT.gStyle.SetOptStat(0)
	ROOT.gPad.SetTicky()	
	ROOT.gPad.RedrawAxis()

	canvas.SaveAs(plot_dir + channel + "/{}_Shape{}.pdf".format(plotname, name_suffix))
	print "Saved plot: {}".format(plot_dir + channel + "/{}_Shape{}.pdf".format(plotname, name_suffix))	

	if www != "":
		os.system("mkdir -p " + os.environ["CMSSW_BASE"] + "/src/FlavioOutput/WebPlots/{}/{}".format(channel, www))
		canvas.SaveAs(os.environ["CMSSW_BASE"] + "/src/FlavioOutput/WebPlots/{}/{}".format(channel, www) + "/{}{}.png".format(plotname, name_suffix))


def webplot(www, channel):
	html_texts = {}
	
	##Get html templates from Harry plotter
	for var in ["overview", "description", "subdir", "plot"]:
		with open(os.environ["ARTUSPATH"] + "/HarryPlotter/data/template_webplot_{}.html".format(var)) as htmlfile:
			html_texts[var] = string.Template(htmlfile.read())

	##Create channel directory web plotting space
	for chan in ["em", "et", "mt", "etm", "mte"]:
		os.system("xrdfs eosuser.cern.ch mkdir -p /eos/user/{}/{}/www/".format(os.environ["CERN_USER"][0], os.environ["CERN_USER"]) + chan)


	##Create index for main page
	with open(os.environ["CMSSW_BASE"] + "/src/FlavioOutput/WebPlots/index.html", "w") as file:
		file.write(html_texts["overview"].substitute(
		title="Overwiew", 
		description= "",
		plots= " ".join([html_texts["subdir"].substitute(subdir=chan) for chan in ["em", "et", "mt", "etm", "mte"]]))
	)
	
	##Create index channel directories
	sub_dirs = [sub_dir for sub_dir in set([name for name in os.listdir(os.environ["CMSSW_BASE"] + "/src/FlavioOutput/WebPlots/" + channel)]) if not "index" in sub_dir]

	with open(os.environ["CMSSW_BASE"] + "/src/FlavioOutput/WebPlots/{}/index.html".format(channel), "w") as file:
		file.write(html_texts["overview"].substitute(
		title="{}/".format(channel), 
		description= html_texts["description"].substitute(subdirs="").rsplit("<p>", 1)[0],
		plots= " ".join([html_texts["subdir"].substitute(subdir= sub_dir) for sub_dir in sub_dirs]))
	)

	##Create index for subdir
	parameters = [parameter for parameter in set([name[:-4] for name in os.listdir(os.environ["CMSSW_BASE"] + "/src/FlavioOutput/WebPlots/{}/{}".format(channel, www))]) if not "index" in parameter]

	with open(os.environ["CMSSW_BASE"] + "/src/FlavioOutput/WebPlots/{}/{}".format(channel, www) + "/index.html", "w") as file:
		file.write(html_texts["overview"].substitute(
		title="{}/{}".format(channel, www), 
		description= html_texts["description"].substitute(subdirs=""),
		plots= " ".join([html_texts["plot"].substitute(title=name, links ="", plot ="{}.png".format(name)) for name in parameters]))
	)
	
	os.system("xrdcp -r -s -f {} root://eosuser.cern.ch//eos/user/{}/{}/www/".format(os.environ["CMSSW_BASE"] + "/src/FlavioOutput/WebPlots/", os.environ["CERN_USER"][0], os.environ["CERN_USER"]))
	print "Web plots: https://{}.web.cern.ch/{}/{}/{}/index.html".format(os.environ["CERN_USER"], os.environ["CERN_USER"], channel, www)


def main():
	##parser 
	args = parser()
	
	##For zlt-leptonic there is just the em channel available with the addition of which lepton is first.
	functions = [get_hists] + ([shape_plot] if args.shape else [plot])

	for func in functions:
		
		pool = Pool(cpu_count())
		tasks = []
		
		for channel in args.channel:

			if not os.path.exists(plot_dir + channel):
				os.system("mkdir -p " + plot_dir + channel)
				
			##Procceses names 
			processes =  ["qcd", "ttj", "vv", "wj", "ztt", "zll"] + ["z{}".format(channel)] + ["data"]

			for param in args.parameter:
				##Check if parameter plotting configuration is saved in parameter.yaml
				param_config = 	yaml.load(open(parameter_yaml, "r"))

				if param in param_config.keys():
					parameter, binning, plotname, x_label = param_config[param][:4]

					if param in args.weight:
						args.weight = args.weight.replace(param, parameter)
	
				else:
					parameter, binning, plotname, x_label = (param, ["30"], param, param)

				
				if type(binning)==dict:
					binning = binning[channel]

				##Get histograms from of Ntuple with harry.py
				if func == get_hists:
					sample_settings = samples.Samples()
					base_config = sample_settings.get_config([getattr(samples.Samples, process) for process in processes], "em" if channel == "etm" or channel == "mte" else channel, category = None, estimationMethod = "new", weight = args.weight)
					task = pool.apply_async(get_hists, args = (parameter, base_config, binning, channel))
					tasks.append(task)

				##Plot all things
				if func == plot:
					task = pool.apply_async(plot, args = (parameter, channel, processes, plotname, x_label, args.data, args.name_suffix, args.www))
					tasks.append(task)
		
				##Plot shape histograms
				if func == shape_plot:
					task = pool.apply_async(shape_plot, args = (parameter, channel, processes, plotname, x_label, args.name_suffix, args.www))
					tasks.append(task)

		pool.close()
		pool.join()

		[task.get() for task in tasks]

	##Clean up
	for channel in ["em", "et", "mt", "etm", "mte"]:
		if os.path.exists(plot_dir + channel):
			os.system("rm --force " + plot_dir + channel + "/*.root")
			os.system("rm --force " + plot_dir + channel + "/*.json")

	##Web plotting
	if args.www != "":
		for channel in args.channel:
			webplot(args.www, channel)

if __name__ == "__main__":
	main()
