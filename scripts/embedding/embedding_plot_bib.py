#!/usr/bin/env python

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot

import HiggsAnalysis.KITHiggsToTauTau.plotting.embedding.embedding_plot_classes as pltcl
#import HiggsAnalysis.KITHiggsToTauTau.plotting.embedding.embedding_plotline_bib as lbib
from HiggsAnalysis.KITHiggsToTauTau.plotting.embedding.embedding_plotline_bib import *

import copy

configs = []


Mu_Full_comparison = pltcl.single_plot(
	name = "Mu_Full_comparison",
	title = "Comparison Benjamin vs. Run2",
	x_expression = "nPU",
	x_bins = "1 5 9 13 17 21 25 29 33 38 43 50 61", 
	wwwfolder="Comparison",
	y_label = "Efficiency #scale[0.5]{#frac{#mu(genMatched & ID & Iso)}{#mu(genMatched))}}",
	plot_type = "efficiency",
	plotlines = [Mu_Full_benjamin_MC, Mu_Full_benjamin_RH, Mu_Full_run2_MC, Mu_Full_run2_RH]
)
configs.extend(Mu_Full_comparison.return_json_with_changed_x_and_weight(
	x_expressions=[
		"nPU",
		"nPUMean",
		"leadingLepPt",
		"leadingLepEta",
		"leadingLepPhi",
		"trailingLepPt",
		"trailingLepEta",
		"trailingLepPhi"
		]
))


Mu_NoIso_comparison = Mu_Full_comparison.clone(
	name = "Mu_NoIso_comparison",
	y_label = "Efficiency #scale[0.5]{#frac{#mu(genMatched & ID)}{#mu(genMatched))}}",
	plotlines = [Mu_NoIso_benjamin_MC, Mu_NoIso_benjamin_RH, Mu_NoIso_run2_MC, Mu_NoIso_run2_RH]
)
configs.extend(Mu_NoIso_comparison.return_json_with_changed_x_and_weight(
	x_expressions=[
		"nPU",
		"nPUMean",
		"leadingLepPt",
		"leadingLepEta",
		"leadingLepPhi",
		"trailingLepPt",
		"trailingLepEta",
		"trailingLepPhi"
		]
))




genMatched_comparison = pltcl.single_plot(
	name = "genMatched_comparison",
	title = "Comparison Benjamin vs. Run2",
	x_expression = "pfAllChargedParticlesNoPileupDeltaR", 
	x_bins = "40,0,0.4",
	x_label = "#Delta R",
	wwwfolder="DeltaR_Plots",
	y_label = "#Sigma p_{T} / #DeltaR ",
	weight = "pfAllChargedParticlesNoPileupPt",
	plot_type = "absolute",
	normalized = True,
	legend =[0.25,0.55,0.55,0.9],
	plotlines = [genMatched_benjamin_MC, genMatched_benjamin_RH, genMatched_run2_MC, genMatched_run2_RH]
)
configs.extend(genMatched_comparison.return_json_with_changed_x_and_weight(
	x_expressions=[
		"pfChargedHadronsPileUpDeltaR",
		"pfChargedHadronsNoPileUpDeltaR",
		"pfNeutralHadronsNoPileUpDeltaR",
		"pfPhotonsNoPileUpDeltaR"],
	weights=[
		"pfChargedHadronsPileUpPt",
		"pfChargedHadronsNoPileUpPt",
		"pfNeutralHadronsNoPileUpEt",
		"pfPhotonsNoPileUpEt"]
))


genMatched_comparison_fine = genMatched_comparison.clone(
    name = "genMatched_comparison_fine",
    x_bins = "50,0,0.1"
)
configs.extend(genMatched_comparison_fine.return_json_with_changed_x_and_weight(
	x_expressions=[
		"pfChargedHadronsPileUpDeltaR",
		"pfChargedHadronsNoPileUpDeltaR",
		"pfNeutralHadronsNoPileUpDeltaR",
		"pfPhotonsNoPileUpDeltaR"],
	weights=[
		"pfChargedHadronsPileUpPt",
		"pfChargedHadronsNoPileUpPt",
		"pfNeutralHadronsNoPileUpEt",
		"pfPhotonsNoPileUpEt"]
))



genMatched_comparison_run2 = pltcl.single_plot(
	name = "genMatched_comparison",
	title = "Run2",
	x_expression = "pfAllChargedParticlesNoPileupDeltaR", 
	x_bins = "40,0,0.4",
	x_label = "#Delta R",
	wwwfolder="DeltaR_Plots_run2",
	y_label = "#Sigma p_{T} / #DeltaR ",
	y_subplot_label = "Embedding/MC"
	weight = "pfAllChargedParticlesNoPileupPt",
	plot_type = "absolute",
	normalized = True,
	legend =[0.25,0.55,0.55,0.9],
	subplot_denominator = 0,
	subplot_numerators = [1],
	plotlines = [genMatched_run2_MC, genMatched_run2_RH]
)
configs.extend(genMatched_comparison_run2.return_json_with_changed_x_and_weight(
	x_expressions=[
		"pfChargedHadronsPileUpDeltaR",
		"pfChargedHadronsNoPileUpDeltaR",
		"pfNeutralHadronsNoPileUpDeltaR",
		"pfPhotonsNoPileUpDeltaR"
		],
	weights=[
		"pfChargedHadronsPileUpPt",
		"pfChargedHadronsNoPileUpPt",
		"pfNeutralHadronsNoPileUpEt",
		"pfPhotonsNoPileUpEt"
		]
))

higgs_plotter = higgsplot.HiggsPlotter(list_of_config_dicts=configs, list_of_args_strings=[""])
