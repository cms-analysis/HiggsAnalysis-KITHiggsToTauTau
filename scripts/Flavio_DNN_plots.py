#! /usr/bin/env python

import ROOT
import os
import argparse


##Constants
old_limits = {"em": 7.6e-7, "et": 9.8e-6, "mt": 9.5e-6} #mt upper limit obtained by atlas group 2020

#UI: Please enter the path to the output of the statistical analysis
limit_path = os.environ["CMSSW_BASE"] + "/src/FlavioOutput/Limits/mt_bdtcontroll/{}"

try:
	output = os.environ["THESIS_PLOTS"] + "/{}/limits.pdf"

except KeyError:
	output = os.environ["CMSSW_BASE"] + "/src/FlavioOutput/Limits/{}_limits.pdf"

##Parser
def parser():
	parser = argparse.ArgumentParser(description = "Script for plotting limits in LFV analysis", formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("--channel", action = "store", choices = ["all", "em", "et", "mt"], default = "all", help = "Channel which should be analyzed")
	parser.add_argument("--method", action ="store" , choices = ["all", "cut_based", "DNN"],  default = "all", help = "Analysis method")
	parser.add_argument("--category", action="store",  choices = ["all", "ZeroJet", "OneJet", "MultiJet", "combined"], default = "all", help = "Analysis category")
	parser.add_argument("--print-limits", action = "store_true", help = "Plot values of limits")

	return parser.parse_args()


def plot_limit(channel, methods, categories, print_limits):
	##TGraph for storing limits
	exp_limits = ROOT.TGraph()
	old_limit = ROOT.TGraph()
	sigma1 = ROOT.TGraphAsymmErrors()
	sigma2 = ROOT.TGraphAsymmErrors()

	canvas = ROOT.TCanvas()

	##Read out limits
	index = 0
	for category in categories:
		for method in methods:
			limit_file = ROOT.TFile(os.environ["CMSSW_BASE"] + "/src/FlavioOutput/Limits/{}_bdtcontroll/limit_{}_{}.root".format(channel, category, method), "READ")
			tree = limit_file.Get("limit")

			limit = [event.limit*old_limits[channel] for event in tree]

			if category == "combined":
				old_limit.SetPoint(index, index+1, old_limits[channel])

			exp_limits.SetPoint(index, index+1, limit[2])
			sigma1.SetPoint(index, index+1, limit[2])
			sigma1.SetPointError(index, 0.15, 0.15, limit[2]-limit[1], limit[3]-limit[1])
			sigma2.SetPoint(index, index+1, limit[2])
			sigma2.SetPointError(index, 0.15, 0.15, limit[2]-limit[0], limit[4]-limit[1])

			if print_limits:
				print "Limit for category/method {}/{}: {}".format(category, "DNN", limit[2])


			index+=1


	##Marker styles
	canvas.SetBottomMargin(0.16)

	sigma2.SetFillColor(ROOT.kYellow)
	sigma2.SetFillStyle(1001)
	sigma2.Draw("AP2")

	sigma1.SetFillColor(ROOT.kGreen)
	sigma1.SetFillStyle(1001)
	sigma1.Draw("P2")

	exp_limits.SetMarkerStyle(20)
	exp_limits.Draw("P")

	old_limit.SetMarkerStyle(21)
	old_limit.Draw("P")

	##Alphanumeric labels
	index = 0
	for method in methods:
		for index2, category in enumerate(categories):
			sigma2.GetXaxis().SetBinLabel(sigma2.GetXaxis().FindBin(index+1), "#splitline" + "{" + method.replace("_", " ") + "}" + "{" + category + "}")
			#sigma2.GetXaxis().ChangeLabel(1 + index2, -1, -1, -1, -1, -1, "#splitline" + "{" + method.replace("_", " ") + "}" + "{" + category + "}")
			index+=1


	sigma2.GetXaxis().SetLabelSize(0.05)
	sigma2.GetYaxis().SetTitle("95% CL Limit on BR(Z#rightarrow {})".format({"em": "e#mu", "et": "e#tau", "mt": "#mu#tau"}[channel]))
	sigma2.SetMinimum(sigma2.GetMinimum())
	#sigma2.SetMaximum(1.5*bkgsum_hist.GetBinContent(bkgsum_hist.GetMaximumBin()))

	ROOT.gStyle.SetPalette(55)

	##Legend style
	ROOT.gStyle.SetLegendBorderSize(0)
	ROOT.gStyle.SetFillStyle(0)

	legend = ROOT.TLegend()
	legend.SetX1NDC(0.65)
	legend.SetX2NDC(0.9)
	legend.SetY1NDC(0.65)
	legend.SetY2NDC(0.9)
	legend.AddEntry(sigma1, "68% expected", "F")
	legend.AddEntry(sigma2, "95% expected", "F")
	legend.AddEntry(exp_limits, "Expected", "P")
	legend.AddEntry(old_limit, "Old observed limit", "P")
	legend.Draw("SAME")


	##CMS and lumi text
	lumi = ROOT.TLatex()
	lumi.SetTextFont(42)
	lumi.SetTextSize(0.04)
	lumi.DrawLatexNDC(0.55, 0.905, "41.5 fb^{-1} (2017, 13 TeV)")

	cms = ROOT.TLatex()
	cms.SetTextFont(62)
	cms.SetTextSize(0.048)
	cms.DrawLatexNDC(0.17, 0.905, "CMS")

	work = ROOT.TLatex()
	work.SetTextFont(52)
	work.SetTextSize(0.04)
	work.DrawLatexNDC(0.245, 0.905, "Work in progress")

	##Save as pdf
	canvas.SaveAs(output.format(channel))


def main():
	args = parser()

	if args.channel == "all":
		for channel in ["em", "et", "mt"]:
			plot_limit(channel, {"all": ["cut_based", "DNN"], "cut_based": ["cut_based"], "DNN": ["DNN"]}[args.method], {"all": ["ZeroJet", "OneJet", "MultiJet", "combined"], "ZeroJet": ["ZeroJet"], "OneJet": ["OneJet"], "MultiJet": ["MultiJet"], "combined": ["combined"]}[args.category], args.print_limits)

	else:
		plot_limit(args.channel, {"all": ["cut_based", "DNN"], "cut_based": ["cut_based"], "DNN": ["DNN"]}[args.method], {"all": ["ZeroJet", "OneJet", "MultiJet", "combined"], "ZeroJet": ["ZeroJet"], "OneJet": ["OneJet"], "MultiJet": ["MultiJet"], "combined": ["combined"]}[args.category], args.print_limits)


if __name__ == "__main__":
	main()
