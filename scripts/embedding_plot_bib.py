#!/usr/bin/env python

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot

import HiggsAnalysis.KITHiggsToTauTau.plotting.embedding.embedding_plot_classes as pltcl
from HiggsAnalysis.KITHiggsToTauTau.plotting.embedding.embedding_plotline_bib import *

configs = []

# npu efficiency plots
muon_full_run2 = pltcl.single_plot(
	name = "muon_full_run2",
	title = "Run II",
	x_expression = "npv",
	x_bins = "1 5 9 13 17 21 25 29 33 38 43 50 61", 
	wwwfolder="Efficiencies",
	y_label = "Efficiency #scale[0.5]{#frac{#mu(genMatched & ID & Iso)}{#mu(genMatched))}}",
	plot_type = "efficiency",
	subplot_denominator = 0,
	subplot_numerators = [1],
	plotlines = [run2_MC_full,run2_RH_full]
)
configs.extend(muon_full_run2.return_json_with_changed_x_and_weight(
	x_expressions=[
#		"npv"
		]
))


muon_iso_run2 = muon_full_run2.clone(
	plotlines = [run2_MC_iso,run2_RH_iso],
	y_label = "Efficiency #scale[0.5]{#frac{#mu(genMatched & Iso)}{#mu(genMatched))}}"
)
configs.extend(muon_iso_run2.return_json_with_changed_x_and_weight(
	x_expressions=[
#		"npv"
		]
))

muon_id_run2 = muon_full_run2.clone(
	plotlines = [run2_MC_id,run2_RH_id],
	y_label = "Efficiency #scale[0.5]{#frac{#mu(genMatched & ID)}{#mu(genMatched))}}"
)
configs.extend(muon_id_run2.return_json_with_changed_x_and_weight(
	x_expressions=[
#		"npv"
		]
))



# PtFlow plots

ptFlow_run2 = pltcl.single_plot(
	name = "ptFlow_run2",
	title = "Run II",
	x_expression = "leadingMuon_NeutralNoPUPtFlow",
	x_label = "#Delta R",
	y_label = "#Sigma p_{T} / #DeltaR ",
	y_subplot_label = "Embedding/MC",
	plot_type = "absolute",
	legend =[0.25,0.55,0.55,0.9],
	normalized_to_nevents = True,
	wwwfolder = "PtFlow",
	subplot_denominator = 0,
	subplot_numerators = [1],
	plotlines = [run2_MC_PtFlow,run2_RH_PtFlow]
)
configs.extend(ptFlow_run2.return_json_with_changed_x_and_weight(
	x_expressions=[
#		"leadingMuon_NeutralNoPUPtFlow",
#		"leadingMuon_ChargedNoPUPtFlow",
#		"leadingMuon_ChargedPUPtFlow",
#		"leadingMuon_PhotonsNoPUPtFlow",

#		"trailingMuon_NeutralNoPUPtFlow",
#		"trailingMuon_ChargedNoPUPtFlow",
#		"trailingMuon_ChargedPUPtFlow",
#		"trailingMuon_PhotonsNoPUPtFlow"
		]
))



### Plots for Zmumu selection of CMSSW skim

#Pt
zmumu_all_pt = pltcl.single_plot(
        name = "zmumu_all_pt",
        title = "Z#rightarrow#mu#mu MC (Run II): all Muons",
        x_expression = "ptMuons",
        x_label = "p^{#mu}_{T}",
        y_label = "Muons / bin width [GeV^{-1}]",
        y_subplot_label = "#frac{selection}{gen. filter}",
        wwwfolder = "",
        plot_type = "absolute",
        legend =[0.6,0.5,0.9,0.9],
        subplot_denominator = 0,
        subplot_numerators = [1,2,3],
        y_subplot_lims = [0.8,1.1],
        plotlines = [zmumu_genfilter_all,zmumu_baseline_all,zmumu_id_all,zmumu_id_and_trigger_all]
)
configs.extend(zmumu_all_pt.return_json_with_changed_x_and_weight(
        x_expressions=["ptMuons"]
))

zmumu_MC_matched_pt = zmumu_all_pt.clone(name = "zmumu_MC_matched_pt",
                                       title = "Z#rightarrow#mu#mu MC (Run II): MC matched Muons",
                                      plotlines = [zmumu_genfilter_MC_matched,
                                                   zmumu_baseline_MC_matched,
                                                   zmumu_id_MC_matched,
                                                   zmumu_id_and_trigger_MC_matched])
configs.extend(zmumu_MC_matched_pt.return_json_with_changed_x_and_weight(
        x_expressions=["ptMuons"]
))

zmumu_not_MC_matched_pt = zmumu_all_pt.clone(name = "zmumu_not_MC_matched_pt",
                                       title = "Z#rightarrow#mu#mu MC (Run II): not MC matched Muons",
                                          plotlines = [zmumu_genfilter_not_MC_matched,
                                                       zmumu_baseline_not_MC_matched,
                                                       zmumu_id_not_MC_matched,
                                                       zmumu_id_and_trigger_not_MC_matched])
configs.extend(zmumu_not_MC_matched_pt.return_json_with_changed_x_and_weight(
        x_expressions=["ptMuons"]
))

#Eta
zmumu_all_eta = pltcl.single_plot(
        name = "zmumu_all_eta",
        title = "Z#rightarrow#mu#mu MC (Run II): all Muons",
        x_expression = "etaMuons",
        x_label = "#eta^{#mu}",
        y_label = "Muons",
        y_subplot_label = "#frac{selection}{gen. filter}",
        wwwfolder = "",
        plot_type = "absolute",
        legend =[0.4,0.15,0.7,0.55],
        subplot_denominator = 0,
        subplot_numerators = [1,2,3],
        y_subplot_lims = [0.8,1.1],
        plotlines = [zmumu_genfilter_all,zmumu_baseline_all,zmumu_id_all,zmumu_id_and_trigger_all]
)
configs.extend(zmumu_all_eta.return_json_with_changed_x_and_weight(
        x_expressions=["etaMuons"]
))

zmumu_MC_matched_eta = zmumu_all_eta.clone(name = "zmumu_MC_matched_eta",
                                       title = "Z#rightarrow#mu#mu MC (Run II): MC matched Muons",
                                       plotlines = [zmumu_genfilter_MC_matched,
                                                    zmumu_baseline_MC_matched,
                                                    zmumu_id_MC_matched,
                                                    zmumu_id_and_trigger_MC_matched])
configs.extend(zmumu_MC_matched_eta.return_json_with_changed_x_and_weight(
        x_expressions=["etaMuons"]
))

zmumu_not_MC_matched_eta = zmumu_all_eta.clone(name = "zmumu_not_MC_matched_eta",
                                       title = "Z#rightarrow#mu#mu MC (Run II): not MC matched Muons",
                                           plotlines = [zmumu_genfilter_not_MC_matched,
                                                        zmumu_baseline_not_MC_matched,
                                                        zmumu_id_not_MC_matched,
                                                        zmumu_id_and_trigger_not_MC_matched],
                                           legend = [0.4,0.45,0.7,0.85])
configs.extend(zmumu_not_MC_matched_eta.return_json_with_changed_x_and_weight(
        x_expressions=["etaMuons"]
))


#nMuons
zmumu_all_n = pltcl.single_plot(
        name = "zmumu_all_n",
        title = "Z#rightarrow#mu#mu MC (Run II): all Muons",
        x_expression = "nMuons",
        x_label = "N^{#mu}",
        y_label = "Events",
        y_log = True,
        wwwfolder = "",
        plot_type = "absolute",
        legend =[0.65,0.75,0.95,0.9],
        plotlines = [zmumu_genfilter_all,zmumu_id_and_trigger_all]
)
configs.extend(zmumu_all_n.return_json_with_changed_x_and_weight(
        x_expressions=["nMuons"]
))


zmumu_MC_matched_n = zmumu_all_n.clone(name = "zmumu_MC_matched_n",
                                       title = "Z#rightarrow#mu#mu MC (Run II): MC matched Muons",
                                       plotlines = [zmumu_genfilter_MC_matched,
                                                    zmumu_id_and_trigger_MC_matched])
configs.extend(zmumu_MC_matched_n.return_json_with_changed_x_and_weight(
        x_expressions=["nMuons"]
))

zmumu_not_MC_matched_n = zmumu_all_n.clone(name = "zmumu_not_MC_matched_n",
                                       title = "Z#rightarrow#mu#mu MC (Run II): not MC matched Muons",
                                           plotlines = [zmumu_genfilter_not_MC_matched,
                                                        zmumu_id_and_trigger_not_MC_matched])
configs.extend(zmumu_not_MC_matched_n.return_json_with_changed_x_and_weight(
        x_expressions=["nMuons"]
))

higgs_plotter = higgsplot.HiggsPlotter(list_of_config_dicts=configs, list_of_args_strings=[""])
