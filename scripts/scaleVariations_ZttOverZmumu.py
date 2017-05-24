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
parser.add_argument('--input-LO-DY',help="path to Artus files (wildcard notation possible) for leading order Drell-Yan MC. For now, stitching of 2 inclusive samples and 1 for each jet multiplicity is set up.",type=str)
parser.add_argument('--input-NLO-DY',help="path to Artus files (wildcard notation possible) for next to leading order Drell-Yan MC. For now only one should be specified (no stitching).",type=str)

args = parser.parse_args()

if args.input_LO_DY is None or args.input_NLO_DY is None:
	print "Please specify the inputs for Drell-Yan MC's (LO and NLO). Use --help for more information."
	exit()

sys.argv.append( '-b-' )
if not os.path.exists("./ztt_zmm_normalization/"):
    os.makedirs("./ztt_zmm_normalization/")
import ROOT as r

tautau_channels = ["mt","et","tt","em"]
categories = ["btag", "nobtag","inclusive"]
mtet_subcategories = ["loosemt","tight","inclusive"]
em_subcategories = ["highPzeta","mediumPzeta","lowPzeta","inclusive"]

scale_variation_weights = ["muR0p5_muF0p5_weight","muR1p0_muF0p5_weight","muR0p5_muF1p0_weight","muR1p0_muF2p0_weight","muR2p0_muF1p0_weight","muR2p0_muF2p0_weight","1"]

selection = {}
weights = {}
mm_weights = {}
ratios = {}
mm_yields = {}
tt_yields = {}

mm_hists = {}
tt_hists = {}

def ztt_stitching():
	mediummass = "(((genbosonmass >= 50.0 && genbosonmass < 150.0 && (npartons == 0 || npartons >= 5))*3.95423374e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 1)*1.27486147e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 2)*1.3012785e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 3)*1.33802133e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 4)*1.09698723e-5))"
	highmass = "(((genbosonmass >= 150.0 && (npartons == 0 || npartons >= 5))*3.95423374e-5) + ((genbosonmass >= 150.0 && npartons == 1)*1.27486147e-5) + ((genbosonmass >= 150.0 && npartons == 2)*1.3012785e-5) + ((genbosonmass >= 150.0 && npartons == 3)*1.33802133e-5) + ((genbosonmass >= 150.0 && npartons == 4)*1.09698723e-5))"
	normalization = "/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"
	return "("+highmass+"+"+mediummass+")"+normalization

# channel selection
selection["mt"] = "35870.0*eventWeight*(0.99)*(gen_match_1 == 4 && gen_match_2 == 5)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonTight3_2 > 0.5)*(dilepton_veto < 0.5)*(trg_singlemuon == 1)*(againstElectronVLooseMVA6_2 > 0.5)*(iso_1 < 0.15)*((q_1*q_2)<0.0)*(mt_1 < 70)*(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*zPtReweightWeight"
selection["et"] = "35870.0*eventWeight*(0.99)*(gen_match_1 == 3 && gen_match_2 == 5)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonLoose3_2 > 0.5)*(dilepton_veto < 0.5)*(trg_singleelectron == 1)*(againstElectronTightMVA6_2 > 0.5)*(iso_1 < 0.1)*((q_1*q_2)<0.0)*(mt_1 < 70)*(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*zPtReweightWeight"
selection["em"] = "35870*eventWeight*(gen_match_1 == 3 && gen_match_2 == 4)*(pt_1 > 24.0 || pt_2 > 24.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(trg_muonelectron == 1)*(iso_2 < 0.2)*(iso_1 < 0.15)*((q_1*q_2)<0.0)*(pZetaMissVis > -40)*zPtReweightWeight"
selection["tt"] = "35870*eventWeight*((0.9025))*(gen_match_1 == 5 && gen_match_2 == 5)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonLoose3_1 > 0.5)*(againstMuonLoose3_2 > 0.5)*(1.0)*(trg_doubletau == 1)*(againstElectronVLooseMVA6_1 > 0.5)*(againstElectronVLooseMVA6_2 > 0.5)*(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*(byTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5)*((q_1*q_2)<0.0)*zPtReweightWeight"
selection["mm"] = "35870.0*eventWeight*(gen_match_1 == 2 && gen_match_2 == 2)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(trg_singlemuon == 1)*(m_vis > 70.0)*(m_vis < 110.0)*(iso_2 < 0.15)*(iso_1 < 0.15)*((q_1*q_2)<0.0)*zPtReweightWeight"

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

for channel in tautau_channels:
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

for category in categories:
	name = "mm_"+category
	weight = "*".join([selection[k] for k in ["mm",category]])
	mm_weights[name] = weight
	
selection_weights = open("./ztt_zmm_normalization/selection_weights.json","w")
selection_weights.write(json.dumps(weights,sort_keys=True,indent=2))
selection_weights.close()


inputDYfiles = args.input_LO_DY

lo_dy_file_list = glob.glob(inputDYfiles)

inputDYNLOfile = args.input_NLO_DY

def scale_variation_mm(argument=("1","1")):
	mm = r.TChain()
	for f in lo_dy_file_list:
		mm.Add(f+"/mm_nominal/ntuple")
	hist_name = "mm_hist"+"_"+argument[0] + "_" + argument[1]
	mm_hist = r.TH1D(hist_name,hist_name,1,0,13000)
	mm.Project(hist_name,"m_vis",str(argument[0]+"*"+mm_weights[argument[1]]+"*"+ztt_stitching()),"GOFF")
	mm_hist = r.gDirectory.Get(hist_name)
	return (argument[0],mm_hist,mm_hist.Integral())

def scale_variation_tt(argument=("1","1","folder_string")):
	sel = r.TChain()
	category =  argument[1].split("_")[1]
	mm_weight = "mm_"+category
	for f in lo_dy_file_list:
		sel.Add(f+argument[2])
	hist_name = "sel_hist"+"_"+argument[0] + "_" + argument[1]
	sel_hist = r.TH1D(hist_name,hist_name,1,0,13000)
	sel.Project(hist_name,"m_vis",str(argument[0]+"*"+weights[argument[1]]+"*"+ztt_stitching()),"GOFF")
	sel_hist = r.gDirectory.Get(hist_name)
	ratio = sel_hist.Integral()/mm_yields[mm_weight][argument[0]]
	return (argument[0],sel_hist,sel_hist.Integral(),ratio)

### Perform scale variations

for weight in mm_weights:
	mm_hists[weight] = {}
	mm_yields[weight] = {}
	print "category:",weight
	pool = Pool(processes=7)
	results = pool.map(scale_variation_mm,[(svw,weight) for svw in scale_variation_weights])
	for result in results:
		mm_hists[weight][result[0]] = result[1]
		mm_yields[weight][result[0]] = result[2]

	nlo_mm = r.TChain()
	nlo_mm.Add(inputDYNLOfile+"/mm_nominal/ntuple")
	hist_name = "nlo_mm_hist_" + weight
	mm_hists[weight]["nlo"] = r.TH1D(hist_name,hist_name,1,0,13000)
	nlo_mm.Project(hist_name,"m_vis",str(mm_weights[weight].replace("*zPtReweightWeight","")),"GOFF")
	mm_hists[weight]["nlo"] = r.gDirectory.Get(hist_name)
	mm_yields[weight]["nlo"] = mm_hists[weight]["nlo"].Integral()

print "Scale variations for mm DONE"

for weight in weights:
	ratios[weight] = {}
	tt_yields[weight] = {}
	tt_hists[weight] = {}
	print "category:",weight
	channel,category,subcat = weight.split("_")
	mm_weight = "_".join(["mm",category])
	folder_string = "/"+channel+"_nominal/ntuple"
	pool = Pool(processes=7)
	results = pool.map(scale_variation_tt,[(svw,weight,folder_string) for svw in scale_variation_weights])
	for result in results:
		tt_hists[weight][result[0]] = result[1]
		tt_yields[weight][result[0]] = result[2]
		ratios[weight][result[0]] = result[3]
	nlo = r.TChain()
	nlo.Add(inputDYNLOfile+folder_string)
	hist_name = "nlo_hist" + "_" + weight
	tt_hists[weight]["nlo"] = r.TH1D(hist_name,hist_name,1,0,13000)
	nlo.Project(hist_name,"m_vis",str(weights[weight].replace("*zPtReweightWeight","")),"GOFF")
	tt_hists[weight]["nlo"] = r.gDirectory.Get(hist_name)
	ratios[weight]["nlo"] = tt_hists[weight]["nlo"].Integral()/mm_yields[mm_weight]["nlo"]
	tt_yields[weight]["nlo"] = tt_hists[weight]["nlo"].Integral()

	print weight,":",tt_yields[weight]["1"]
	print mm_weight,":",mm_yields[mm_weight]["1"]
	print "--------"

print "Scale variations for tt DONE"

ratios_file = open("./ztt_zmm_normalization/ratios.json","w")
ratios_file.write(json.dumps(ratios,sort_keys=True,indent=2))
ratios_file.close()

intervals = {}

for weight in sorted(weights):
	channel,category,subcat = weight.split("_")
	mm_weight = "_".join(["mm",category])
	if ratios[weight]["1"] != 0 and ratios[weight]["nlo"] != 0:
		intervals[weight] = {}
		ratio_variations = [ratios[weight][r_key] for r_key in ratios[weight] if not r_key in ["1","nlo"]]
		intervals[weight]["max"] = max(ratio_variations)
		intervals[weight]["min"] = min(ratio_variations)
		intervals[weight]["nominal"] = ratios[weight]["1"]
		intervals[weight]["nlo"] = ratios[weight]["nlo"]

		intervals[weight]["percentage_up"] = 100*(intervals[weight]["max"]/intervals[weight]["nominal"]-1)
		intervals[weight]["percentage_down"] = 100*(intervals[weight]["min"]/intervals[weight]["nominal"]-1)
		intervals[weight]["percentage_nlo"] = 100*(intervals[weight]["nlo"]/intervals[weight]["nominal"]-1)

		tt_hists[weight]["1"].Divide(mm_hists[mm_weight]["1"])
		intervals[weight]["percentage_stat_nominal"] = 100*(tt_hists[weight]["1"].GetBinError(1)/tt_hists[weight]["1"].GetBinContent(1))
		tt_hists[weight]["nlo"].Divide(mm_hists[mm_weight]["nlo"])
		intervals[weight]["percentage_stat_nlo"] = 100*(tt_hists[weight]["nlo"].GetBinError(1)/tt_hists[weight]["nlo"].GetBinContent(1))

intervals_file = open("./ztt_zmm_normalization/intervals.json","w")
intervals_file.write(json.dumps(intervals,sort_keys=True,indent=2))
intervals_file.close()
