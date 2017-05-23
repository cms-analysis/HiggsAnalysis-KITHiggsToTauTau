# Example command:
# python HiggsAnalysis/KITHiggsToTauTau/scripts/scaleVariations_ZttOverZmumu.py --input-LO-DY "/nfs/dust/cms/user/rcaspart/htautau/artus/2017-05-15_22-22_incBadMuons/merged/DY[Jets,1Jets,2Jets,3Jets,4Jets]*ToLLM50*madgraph*/*.root" --input-NLO-DY "/nfs/dust/cms/user/rcaspart/htautau/artus/2017-05-15_22-22_incBadMuons/merged/DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext2/DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext2.root"
# Adapt it to your purposes, e.g. change the input files


import sys
import json
import math
import os
import glob
import argparse
from multiprocessing import Pool

parser = argparse.ArgumentParser(description='Script to calculate Z->tautau over Z->mumu ratios under mu_F and mu_R scale variations.')
parser.add_argument('--input-LO-TTbar',help="path to Artus files (wildcard notation possible) for leading order TTbar. For now only one should be specified (no stitching).",type=str)
parser.add_argument('--input-NLO-TTbar',help="path to Artus files (wildcard notation possible) for next to leading order TTba. For now only one should be specified (no stitching).",type=str)

args = parser.parse_args()

if args.input_LO_TTbar is None or args.input_NLO_TTbar is None:
	print "Please specify the inputs for TTbar MC's (LO and NLO). Use --help for more information."
	exit()

sys.argv.append( '-b' )
if not os.path.exists("./ttbar_cr_normalization/"):
    os.makedirs("./ttbar_cr_normalization/")
import ROOT as r

signal_channels = ["mt","et","tt","em"]
categories = ["btag", "nobtag","inclusive"]
mtet_subcategories = ["loosemt","tight","inclusive"]
em_subcategories = ["highPzeta","mediumPzeta","lowPzeta","inclusive"]

scale_variation_weights = ["muR0p5_muF0p5_weight","muR1p0_muF0p5_weight","muR0p5_muF1p0_weight","muR1p0_muF2p0_weight","muR2p0_muF1p0_weight","muR2p0_muF2p0_weight","1"]

selection = {}
weights = {}
ttbar_cr_weights = {}
ratios = {}
ttbar_cr_yields = {}
ttbar_yields = {}

ttbar_cr_hists = {}
ttbar_hists = {}

# channel selection
selection["mt"] = "35870.0*eventWeight*(0.99)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonTight3_2 > 0.5)*(dilepton_veto < 0.5)*(trg_singlemuon == 1)*(againstElectronVLooseMVA6_2 > 0.5)*(iso_1 < 0.15)*((q_1*q_2)<0.0)*(mt_1 < 70)*(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*topPtReweightWeight"
selection["et"] = "35870.0*eventWeight*(0.99)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonLoose3_2 > 0.5)*(dilepton_veto < 0.5)*(trg_singleelectron == 1)*(againstElectronTightMVA6_2 > 0.5)*(iso_1 < 0.1)*((q_1*q_2)<0.0)*(mt_1 < 70)*(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*topPtReweightWeight"
selection["em"] = "35870*eventWeight*(pt_1 > 24.0 || pt_2 > 24.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(trg_muonelectron == 1)*(iso_2 < 0.2)*(iso_1 < 0.15)*((q_1*q_2)<0.0)*(pZetaMissVis > -50)*topPtReweightWeight"
selection["tt"] = "35870*eventWeight*((0.9409))*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonLoose3_1 > 0.5)*(againstMuonLoose3_2 > 0.5)*(1.0)*(trg_doubletau == 1)*(againstElectronVLooseMVA6_1 > 0.5)*(againstElectronVLooseMVA6_2 > 0.5)*(byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*(byMediumIsolationMVArun2v1DBoldDMwLT_1 > 0.5)*((q_1*q_2)<0.0)*topPtReweightWeight"
selection["ttbar_cr"] = "35870*eventWeight*(pt_1 > 24.0 || pt_2 > 24.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(trg_muonelectron == 1)*(iso_2 < 0.2)*(iso_1 < 0.15)*((q_1*q_2)<0.0)*(pZetaMissVis < -50)*(met > 80.0)*topPtReweightWeight"

# main categorisation
selection["btag"] = "(nbtag > 0)"
selection["nobtag"] = "(nbtag == 0)"

# mt et channel subcategories
selection["loosemt"] = "(0.95/0.99)*(mt_1 > 40 && mt_1 < 70 && byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
selection["tight"] = "(0.95/0.99)*(mt_1 < 40 && byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"

# em channel subcategories
selection["highPzeta"] = "(pZetaMissVis > 30)"
selection["mediumPzeta"] = "((pZetaMissVis > -10)*(pZetaMissVis < 30))"
selection["lowPzeta"] = "((pZetaMissVis > -50)*(pZetaMissVis < -10))"

selection["inclusive"] = "(1)"

for channel in signal_channels:
	name = ""
	weight = ""
	for category in categories:
			if channel in ["mt","et"]:
				for subcat in mtet_subcategories:
					name = "_".join([channel,category,subcat])
					weight = "*".join([selection[k] for k in [channel,category,subcat]])
					weights[name] = weight
			elif channel == "em":
				for subcat in em_subcategories:
					name = "_".join([channel,category,subcat])
					weight = "*".join([selection[k] for k in [channel,category,subcat]])
					weights[name] = weight
			elif channel == "tt":
				name = "_".join([channel,category,"inclusive"])
				weight = "*".join([selection[k] for k in [channel,category]])
				weights[name] = weight

for category in ["inclusive"]:
	name = "ttbar_cr_"+category
	weight = "*".join([selection[k] for k in ["ttbar_cr",category]])
	ttbar_cr_weights[name] = weight
	
selection_weights = open("./ttbar_cr_normalization/selection_weights.json","w")
selection_weights.write(json.dumps(weights,sort_keys=True,indent=2))
selection_weights.close()


inputDYfiles = args.input_LO_TTbar

lo_ttbar_file = glob.glob(inputDYfiles)[0]

inputttbarNLOfile = glob.glob(args.input_NLO_TTbar)[0]

def scale_variation_ttbar_cr(argument=("1","1")):
	mm = r.TChain()
	f = inputttbarNLOfile
	mm.Add(f+"/em_nominal/ntuple")
	hist_name = "ttbar_cr_hist"+"_"+argument[0] + "_" + argument[1]
	ttbar_cr_hist = r.TH1D(hist_name,hist_name,1,0,13000)
	mm.Project(hist_name,"m_vis",str(argument[0]+"*"+ttbar_cr_weights[argument[1]]),"GOFF")
	ttbar_cr_hist = r.gDirectory.Get(hist_name)
	return (argument[0],ttbar_cr_hist,ttbar_cr_hist.Integral())

def scale_variation_tt(argument=("1","1","folder_string")):
	sel = r.TChain()
	category =  argument[1].split("_")[1]
	ttbar_cr_weight = "ttbar_cr_"+"inclusive"
	f = inputttbarNLOfile
	sel.Add(f+argument[2])
	hist_name = "sel_hist"+"_"+argument[0] + "_" + argument[1]
	sel_hist = r.TH1D(hist_name,hist_name,1,0,13000)
	sel.Project(hist_name,"m_vis",str(argument[0]+"*"+weights[argument[1]]),"GOFF")
	sel_hist = r.gDirectory.Get(hist_name)
	ratio = sel_hist.Integral()/ttbar_cr_yields[ttbar_cr_weight][argument[0]]
	return (argument[0],sel_hist,sel_hist.Integral(),ratio)

### Perform scale variations

for weight in ttbar_cr_weights:
	ttbar_cr_hists[weight] = {}
	ttbar_cr_yields[weight] = {}
	print "category:",weight
	pool = Pool(processes=7)
	results = pool.map(scale_variation_ttbar_cr,[(svw,weight) for svw in scale_variation_weights])
	for result in results:
		ttbar_cr_hists[weight][result[0]] = result[1]
		ttbar_cr_yields[weight][result[0]] = result[2]
		print "NLO yield: ",weight,result[0],result[2]

	nlo_mm = r.TChain()
	nlo_mm.Add(lo_ttbar_file+"/em_nominal/ntuple")
	hist_name = "lo_ttbar_cr_hist_" + weight
	ttbar_cr_hists[weight]["lo"] = r.TH1D(hist_name,hist_name,1,0,13000)
	nlo_mm.Project(hist_name,"m_vis",str(ttbar_cr_weights[weight]),"GOFF")
	ttbar_cr_hists[weight]["lo"] = r.gDirectory.Get(hist_name)
	ttbar_cr_yields[weight]["lo"] = ttbar_cr_hists[weight]["lo"].Integral()
	print "LO yield: ",weight,ttbar_cr_yields[weight]["lo"]

print "Scale variations for ttbar_cr DONE"

for weight in weights:
	ratios[weight] = {}
	ttbar_yields[weight] = {}
	ttbar_hists[weight] = {}
	print "category:",weight
	channel,category,subcat = weight.split("_")
	ttbar_cr_weight = "_".join(["ttbar_cr","inclusive"])
	folder_string = "/"+channel+"_nominal/ntuple"
	pool = Pool(processes=7)
	results = pool.map(scale_variation_tt,[(svw,weight,folder_string) for svw in scale_variation_weights])
	for result in results:
		ttbar_hists[weight][result[0]] = result[1]
		ttbar_yields[weight][result[0]] = result[2]
		ratios[weight][result[0]] = result[3]
	nlo = r.TChain()
	nlo.Add(lo_ttbar_file+folder_string)
	hist_name = "lo_hist" + "_" + weight
	ttbar_hists[weight]["lo"] = r.TH1D(hist_name,hist_name,1,0,13000)
	nlo.Project(hist_name,"m_vis",str(weights[weight]),"GOFF")
	ttbar_hists[weight]["lo"] = r.gDirectory.Get(hist_name)
	ratios[weight]["lo"] = ttbar_hists[weight]["lo"].Integral()/ttbar_cr_yields[ttbar_cr_weight]["lo"]
	ttbar_yields[weight]["lo"] = ttbar_hists[weight]["lo"].Integral()

	print weight,":","yield =",ttbar_yields[weight]["1"], 
	print ttbar_cr_weight,":","yield =",ttbar_cr_yields[ttbar_cr_weight]["1"]
	print "ratio =",ratios[weight]["1"]
	print "--------"

print "Scale variations for tt DONE"

ratios_file = open("./ttbar_cr_normalization/ratios.json","w")
ratios_file.write(json.dumps(ratios,sort_keys=True,indent=2))
ratios_file.close()

intervals = {}

for weight in sorted(weights):
	channel,category,subcat = weight.split("_")
	ttbar_cr_weight = "_".join(["ttbar_cr","inclusive"])
	if ratios[weight]["1"] != 0 and ratios[weight]["lo"] != 0:
		intervals[weight] = {}
		ratio_variations = [ratios[weight][r_key] for r_key in ratios[weight] if not r_key in ["1","lo"]]
		intervals[weight]["max"] = max(ratio_variations)
		intervals[weight]["min"] = min(ratio_variations)
		intervals[weight]["nominal"] = ratios[weight]["1"]
		intervals[weight]["lo"] = ratios[weight]["lo"]

		intervals[weight]["percentage_up"] = 100*(intervals[weight]["max"]/intervals[weight]["nominal"]-1)
		intervals[weight]["percentage_down"] = 100*(intervals[weight]["min"]/intervals[weight]["nominal"]-1)
		intervals[weight]["percentage_lo"] = 100*(intervals[weight]["lo"]/intervals[weight]["nominal"]-1)

		ttbar_hists[weight]["1"].Divide(ttbar_cr_hists[ttbar_cr_weight]["1"])
		intervals[weight]["percentage_stat_nominal"] = 100*(ttbar_hists[weight]["1"].GetBinError(1)/ttbar_hists[weight]["1"].GetBinContent(1))
		ttbar_hists[weight]["lo"].Divide(ttbar_cr_hists[ttbar_cr_weight]["lo"])
		intervals[weight]["percentage_stat_lo"] = 100*(ttbar_hists[weight]["lo"].GetBinError(1)/ttbar_hists[weight]["lo"].GetBinContent(1))

intervals_file = open("./ttbar_cr_normalization/intervals.json","w")
intervals_file.write(json.dumps(intervals,sort_keys=True,indent=2))
intervals_file.close()
