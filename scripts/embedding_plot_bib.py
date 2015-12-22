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

higgs_plotter = higgsplot.HiggsPlotter(list_of_config_dicts=configs, list_of_args_strings=[""])
