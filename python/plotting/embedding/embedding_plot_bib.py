#!/usr/bin/env python

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot

import HiggsAnalysis.KITHiggsToTauTau.plotting.embedding.embedding_plot_classes as pltcl
import HiggsAnalysis.KITHiggsToTauTau.plotting.embedding.embedding_plotline_bib as lbib

import copy

configs = []


nPU_Mu_Full_comparison = pltcl.single_plot(
	name = "nPU_Mu_Full_comparison",
	title = "Comparison Benjamin vs. Run2",
	x_bins = "1 5 9 13 17 21 25 29 33 38 43 50 61",
	x_expression = "nPU", 
	wwwfolder="Comparison",
	y_label = "Efficiency #scale[0.5]{#frac{#mu(genMatched & ID & Iso)}{#mu(genMatched))}}",
	plot_type = "efficiency")

nPU_Mu_Full_comparison.add_plotline(lbib.Mu_Full_benjamin_MC)
nPU_Mu_Full_comparison.add_plotline(lbib.Mu_Full_benjamin_RH)
nPU_Mu_Full_comparison.add_plotline(lbib.Mu_Full_run2_MC)
nPU_Mu_Full_comparison.add_plotline(lbib.Mu_Full_run2_RH)

nPU_Mu_Full_comparison.fill_single_json()

#configs.append(nPU_Mu_Full_comparison.out_json)



nPU_Mu_NoIso_comparison = pltcl.single_plot(
	name = "nPU_Mu_NoIso_comparison",
	title = "Comparison Benjamin vs. Run2",
	x_bins = "1 5 9 13 17 21 25 29 33 38 43 50 61",
	x_expression = "nPU", 
	wwwfolder="Comparison",
	y_label = "Efficiency #scale[0.5]{#frac{#mu(genMatched & ID & Iso)}{#mu(genMatched))}}",
	plot_type = "efficiency")

nPU_Mu_NoIso_comparison.add_plotline(lbib.Mu_NoIso_benjamin_MC)
nPU_Mu_NoIso_comparison.add_plotline(lbib.Mu_NoIso_benjamin_RH)
nPU_Mu_NoIso_comparison.add_plotline(lbib.Mu_NoIso_run2_MC)
nPU_Mu_NoIso_comparison.add_plotline(lbib.Mu_NoIso_run2_RH)

nPU_Mu_NoIso_comparison.fill_single_json()

configs.append(nPU_Mu_NoIso_comparison.out_json)



pfAllChargedParticlesNoPileupDeltaR_genMatched_comparison = pltcl.single_plot(
	name = "pfAllChargedParticlesNoPileupDeltaR_genMatched_comparison",
	title = "Comparison Benjamin vs. Run2",
	x_expression = "pfAllChargedParticlesNoPileupDeltaR", 
	wwwfolder="Comparison",
	y_label = "Number of Events #scale[0.5]{#mu(genMatched & ID & Iso)}",
	plot_type = "absolute")

pfAllChargedParticlesNoPileupDeltaR_genMatched_comparison.add_plotline(lbib.genMatched_benjamin_MC)
pfAllChargedParticlesNoPileupDeltaR_genMatched_comparison.add_plotline(lbib.genMatched_benjamin_RH)
pfAllChargedParticlesNoPileupDeltaR_genMatched_comparison.add_plotline(lbib.genMatched_run2_MC)
pfAllChargedParticlesNoPileupDeltaR_genMatched_comparison.add_plotline(lbib.genMatched_run2_RH)

pfAllChargedParticlesNoPileupDeltaR_genMatched_comparison.fill_single_json()

#configs.append(pfAllChargedParticlesNoPileupDeltaR_genMatched_comparison.out_json)


pfChargedHadronsPileUpDeltaR_genMatched_comparison = copy.copy(pfAllChargedParticlesNoPileupDeltaR_genMatched_comparison)
pfChargedHadronsPileUpDeltaR_genMatched_comparison.x_expression = "pfChargedHadronsPileUpDeltaR"
pfChargedHadronsPileUpDeltaR_genMatched_comparison.name = "pfChargedHadronsPileUpDeltaR_genMatched_comparison"

#configs.append(pfChargedHadronsPileUpDeltaR_genMatched_comparison.out_json)


pfChargedHadronsNoPileUpDeltaR_genMatched_comparison = copy.copy(pfAllChargedParticlesNoPileupDeltaR_genMatched_comparison)
pfChargedHadronsNoPileUpDeltaR_genMatched_comparison.x_expression = "pfChargedHadronsNoPileUpDeltaR"
pfChargedHadronsNoPileUpDeltaR_genMatched_comparison.name = "pfChargedHadronsPileUpDeltaR_genMatched_comparison"

#configs.append(pfChargedHadronsNoPileUpDeltaR_genMatched_comparison.out_json)


pfNeutralHadronsNoPileUpDeltaR_genMatched_comparison = copy.copy(pfAllChargedParticlesNoPileupDeltaR_genMatched_comparison)
pfNeutralHadronsNoPileUpDeltaR_genMatched_comparison.x_expression = "pfNeutralHadronsNoPileUpDeltaR"
pfNeutralHadronsNoPileUpDeltaR_genMatched_comparison.name = "pfNeutralHadronsNoPileUpDeltaR_genMatched_comparison"

#configs.append(pfNeutralHadronsNoPileUpDeltaR_genMatched_comparison.out_json)

pfPhotonsNoPileUpDeltaR_genMatched_comparison = copy.copy(pfAllChargedParticlesNoPileupDeltaR_genMatched_comparison)
pfPhotonsNoPileUpDeltaR_genMatched_comparison.x_expression = "pfPhotonsNoPileUpDeltaR"
pfPhotonsNoPileUpDeltaR_genMatched_comparison.name = "pfPhotonsNoPileUpDeltaR_genMatched_comparison"

#configs.append(pfPhotonsNoPileUpDeltaR_genMatched_comparison.out_json)





higgs_plotter = higgsplot.HiggsPlotter(list_of_config_dicts=configs, list_of_args_strings=[""])
