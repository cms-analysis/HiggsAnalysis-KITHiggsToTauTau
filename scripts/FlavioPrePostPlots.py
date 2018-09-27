import ROOT

import os
import argparse

##Global constants
plot_dir = os.environ["CMSSW_BASE"] + "/src/FlavioOutput/Limits/{}/postfit_BDT_s.root"

try:
	out_dir = os.environ["THESIS_PLOTS"] + "/"

except KeyError:
	out_dir = os.environ["CMSSW_BASE"] + "/src/FlavioOutput/Limits/"

labels = {"ZTT": "Z#rightarrow#tau#tau", "ZLL": "Z#rightarrow ll", "ZL": "Z#rightarrow ll", "TT": "t#bar{t}", "TTJJ": "t#bar{t}", "W": "W + jets", "VV": "WW/ZZ/WZ", "QCD": "QCD", "ZEM": "Z#rightarrow e#mu", "ZET": "Z#rightarrow e#tau", "ZMT": "Z#rightarrow #mu#tau", "data_obs": "Data", "ZETM": "Z#rightarrow e#tau_{#mu}", "ZMTE": "Z#rightarrow #mu#tau_{e}"}
colors = {"ZTT": ROOT.kYellow, "ZLL": ROOT.kAzure+1, "ZL": ROOT.kAzure+1, "ZJ": ROOT.kAzure+1, "TT": ROOT.kViolet-3, "TTJJ": ROOT.kViolet-3, "TTT": ROOT.kViolet-3, "W": ROOT.kRed+1, "VV": ROOT.kOrange+5, "QCD": ROOT.kPink+1}
title = {"em": "e#mu", "etm": "e#mu", "mte": "e#mu", "et": "e#tau_{h}", "mt": "#mu#tau_{h}"}


processes = {
		"em": ["QCD", "TT", "VV", "W", "ZLL", "ZTT"],
		"et": ["QCD", "TTJJ", "TTT", "VV", "W", "ZL", "ZJ", "ZTT"],
		"mt": ["QCD", "TTJJ", "TTT", "VV", "W", "ZL", "ZJ", "ZTT"]
}


def parser():
	parser = argparse.ArgumentParser(description = "Script for calculating plotting in LFV analysis", formatter_class=argparse.RawTextHelpFormatter)

	parser.add_argument("--channel", nargs="+", required = True, choices = ["em", "et", "mt", "etm", "mte"] , help = "Channel which should be analyzed")

	return parser.parse_args()

def plot(channel, category, fit):
	##Get all hists
	hist_file = ROOT.TFile(plot_dir.format(channel) , "READ")

	##Legend
	ROOT.gStyle.SetLegendBorderSize(0)
	ROOT.gStyle.SetFillStyle(0)
	legend = ROOT.TLegend()
	legend.SetX1NDC(0.65)
	legend.SetX2NDC(0.95)
	legend.SetY1NDC(0.7)
	legend.SetY2NDC(0.9)
	
	hists = [hist_file.Get("{}_{}/{}".format(category, fit, process)) for process in processes[channel]]


	
	##Stacked background histogram
	stacked_hist = ROOT.THStack()
	bkgsum_hist = hists[0].Clone()

	for index, process in enumerate(processes[channel]):
		hists[index].SetFillColor(colors[process])
		hists[index].SetLineColor(colors[process])
		
		if index != 0:
			bkgsum_hist.Add(hists[index])

		if hists[index].GetName() not in ["ZJ", "TTT"]:
			legend.AddEntry(hists[index], labels[process], "F")

		stacked_hist.Add(hists[index])



	##Signal histogram
	sig_hist = hist = hist_file.Get("{}_{}/{}".format(category, fit, "Z{}".format(channel).upper()))
	sig_hist.SetLineColor(ROOT.kBlack)
	sig_hist.SetLineWidth(4)
	legend.AddEntry(sig_hist, labels["Z" + channel.upper()], "L")


	##Data histogram
	data_hist = hist_file.Get("{}_{}/{}".format(category, fit, "data_obs"))
		
	data_graph = ROOT.TGraphErrors()
	data_graph.SetMarkerStyle(20)
	
	legend.AddEntry(data_graph, labels["data_obs"], "LP")

	##Data/Bkg ratio histogram
	errorband = bkgsum_hist.Clone()
	errorband.Divide(bkgsum_hist)

	errorband.SetFillColor(ROOT.kGray +1)
	errorband.SetMarkerColor(ROOT.kWhite)
	errorband.SetFillStyle(3001)
	errorband.SetStats(0)

	ratio_graph = ROOT.TGraphErrors()
	ratio_graph.SetMarkerStyle(20)

	for index in range(data_hist.GetNbinsX()):
		data_graph.SetPoint(index, data_hist.GetBinCenter(index+1), data_hist.GetBinContent(index+1))
		data_graph.SetPointError(index, data_hist.GetBinWidth(index+1)/2., data_hist.GetBinError(index+1))

		try:
			ratio_graph.SetPoint(index, data_hist.GetBinCenter(index+1), data_hist.GetBinContent(index+1)/bkgsum_hist.GetBinContent(index+1))
			ratio_graph.SetPointError(index, data_hist.GetBinWidth(index+1)/2., data_hist.GetBinError(index+1)/bkgsum_hist.GetBinContent(index+1))

		except:
			pass

	##Erroband of background
	errorband_main = bkgsum_hist.Clone()
	errorband_main.SetFillColor(ROOT.kGray +1)
	errorband_main.SetMarkerColor(ROOT.kGray +1)
	errorband_main.SetLineColor(ROOT.kGray +1)
	errorband_main.SetFillStyle(3001)
	legend.AddEntry(errorband_main, "Uncertainty", "F")

	##CMS and lumi text
	channel_title = ROOT.TLatex()
	channel_title.SetTextFont(42)
	channel_title.SetTextSize(0.035)

	lumi = ROOT.TLatex()
	lumi.SetTextFont(42)
	lumi.SetTextSize(0.035)

	cms = ROOT.TLatex()
	cms.SetTextFont(62)
	cms.SetTextSize(0.0295)

	work = ROOT.TLatex()
	work.SetTextFont(52)
	work.SetTextSize(0.035)

	#Draw all things
	canvas = ROOT.TCanvas("c", "c", 800,800)
	canvas.SetLeftMargin(0.15)

	stacked_hist.Draw("HIST")
	sig_hist.Draw("SAME HIST")
	
	errorband_main.Draw("SAME E2")
	data_graph.Draw("SAME P")

	legend.Draw("SAME")

	channel_title.DrawLatexNDC(0.17, 0.905, title[channel])
	lumi.DrawLatexNDC(0.605, 0.905, "35.9 fb^{-1} (2016, 13 TeV)")
	cms.DrawLatexNDC(0.25, 0.905, "CMS")
	work.DrawLatexNDC(0.318, 0.905, "Work in progress")

	##Axis options
	stacked_hist.SetMinimum(0)
	stacked_hist.SetMaximum(1.3*bkgsum_hist.GetBinContent(bkgsum_hist.GetMaximumBin()))
	stacked_hist.GetXaxis().SetTitle("BDT score")
	stacked_hist.GetXaxis().SetTitleSize(0.04)
	stacked_hist.GetXaxis().SetLabelSize(0.035)
	stacked_hist.GetYaxis().SetTitle("Events")
	stacked_hist.GetYaxis().SetTitleOffset(1.9)
	stacked_hist.GetYaxis().SetLabelSize(0.035)
	ROOT.TGaxis().SetMaxDigits(3)

	
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
	stacked_hist.GetXaxis().SetTitleOffset(4.5)
	errorband.GetXaxis().SetLabelSize(0.17)
	errorband.SetAxisRange(0.6, 1.4, "Y")
	errorband.GetYaxis().SetTitle("#frac{Data}{MC}")
	errorband.GetYaxis().SetTitleSize(0.08)
	errorband.GetYaxis().SetLabelSize(0.1)
	errorband.GetYaxis().SetTitleOffset(0.5)


	##Save Histogram
	ROOT.gPad.RedrawAxis()
	ROOT.gPad.SetTicky()
	ROOT.TGaxis.SetExponentOffset(-0.05, 0.005, "y")

	canvas.SaveAs(out_dir + channel + "/{}_{}.pdf".format(category, fit))
	print "Saved plot: {}".format(out_dir + channel + "/{}_{}.pdf".format(category, fit))


def main():
	args = parser()

	for channel in args.channel:
		for category in ["ZeroJet", "OneJet", "MultiJet", "TT_CR", "DY_CR"]:
			for fit in ["prefit", "postfit"]:
				plot(channel, category, fit)


if __name__ == "__main__":
	main()

	
