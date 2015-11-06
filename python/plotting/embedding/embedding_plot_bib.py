#!/usr/bin/env python

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot

import HiggsAnalysis.KITHiggsToTauTau.plotting.embedding.embedding_plot_classes as pltcl
#import HiggsAnalysis.KITHiggsToTauTau.plotting.embedding.embedding_plotline_bib as lbib
from HiggsAnalysis.KITHiggsToTauTau.plotting.embedding.embedding_plotline_bib import *

import copy

configs = []


nPU_Mu_Full_comparison = pltcl.single_plot(
	name = "Mu_Full_comparison",
	title = "Comparison Benjamin vs. Run2",
	x_expression = "nPU", 
	wwwfolder="Comparison",
	y_label = "Efficiency #scale[0.5]{#frac{#mu(genMatched & ID & Iso)}{#mu(genMatched))}}",
	plot_type = "efficiency",
        plotlines = [Mu_Full_benjamin_MC, Mu_Full_benjamin_RH, Mu_Full_run2_MC, Mu_Full_run2_RH]
        )
nPU_Mu_Full_comparison.fill_single_json()
#configs.append(nPU_Mu_Full_comparison.out_json)



nPU_Mu_NoIso_comparison = pltcl.single_plot(
	name = "Mu_NoIso_comparison",
	title = "Comparison Benjamin vs. Run2",
	x_expression = "nPU", 
	x_bins = "1 5 9 13 17 21 25 29 33 38 43 50 61",
	wwwfolder="Comparison",
	y_label = "Efficiency #scale[0.5]{#frac{#mu(genMatched & ID)}{#mu(genMatched))}}",
	plot_type = "efficiency",
        plotlines = [Mu_NoIso_benjamin_MC, Mu_NoIso_benjamin_RH, Mu_NoIso_run2_MC, Mu_NoIso_run2_RH]
        #plotlines = [Mu_NoIso_benjamin_MC, Mu_NoIso_benjamin_RH, Mu_NoIso_run2_RH]
        )
nPU_Mu_NoIso_comparison.fill_single_json()
#configs.append(nPU_Mu_NoIso_comparison.out_json)



#pfAllChargedParticlesNoPileupDeltaR_genMatched_comparison = pltcl.single_plot(
genMatched_comparison = pltcl.single_plot(
	name = "genMatched_comparison",
	title = "Comparison Benjamin vs. Run2",
	x_expression = "pfAllChargedParticlesNoPileupDeltaR", 
	x_bins = "40,0,0.4",
        x_label = "#Delta R",
	wwwfolder="DeltaR_Plots",
	y_label = "#Sigma p_{T} / #DeltaR ",
	plot_type = "absolute",
        normalized = True,
        legend =[0.25,0.55,0.55,0.9],
        plotlines = [genMatched_benjamin_MC, genMatched_benjamin_RH, genMatched_run2_MC, genMatched_run2_RH]
)
configs.extend(genMatched_comparison.return_json_from_x_expressions([
#  "pfAllChargedParticlesNoPileupDeltaR",
  "pfChargedHadronsPileUpDeltaR",
  "pfChargedHadronsNoPileUpDeltaR",
  "pfNeutralHadronsNoPileUpDeltaR",
  "pfPhotonsNoPileUpDeltaR"
  ])) 


genMatched_comparison_fine = genMatched_comparison.clone(
    name = "genMatched_comparison_fine",
    x_bins = "50,0,0.1"
)
configs.extend(genMatched_comparison_fine.return_json_from_x_expressions([
#  "pfAllChargedParticlesNoPileupDeltaR",
  "pfChargedHadronsPileUpDeltaR",
  "pfChargedHadronsNoPileUpDeltaR",
  "pfNeutralHadronsNoPileUpDeltaR",
  "pfPhotonsNoPileUpDeltaR"
  ])) 



#pfAllChargedParticlesNoPileupDeltaR_genMatched_comparison.fill_single_json()
#configs.append(pfAllChargedParticlesNoPileupDeltaR_genMatched_comparison.out_json)
#pfChargedHadronsPileUpDeltaR_genMatched_comparison = pfAllChargedParticlesNoPileupDeltaR_genMatched_comparison.clone(
 #                                                                       x_expression = "pfChargedHadronsPileUpDeltaR")


#pfChargedHadronsPileUpDeltaR_genMatched_comparison.fill_single_json()
#configs.append(pfChargedHadronsPileUpDeltaR_genMatched_comparison.out_json)
#pfChargedHadronsNoPileUpDeltaR_genMatched_comparison = pfAllChargedParticlesNoPileupDeltaR_genMatched_comparison.clone(
#                                                                        x_expression = "pfChargedHadronsNoPileUpDeltaR")

#pfChargedHadronsNoPileUpDeltaR_genMatched_comparison.fill_single_json()
#configs.append(pfChargedHadronsNoPileUpDeltaR_genMatched_comparison.out_json)
#pfChargedHadronsNoPileUpDeltaR_genMatched_comparison.name = "pfChargedHadronsPileUpDeltaR_genMatched_comparison"

#configs.append(pfChargedHadronsNoPileUpDeltaR_genMatched_comparison.out_json)
#pfNeutralHadronsNoPileUpDeltaR_genMatched_comparison = pfAllChargedParticlesNoPileupDeltaR_genMatched_comparison
#pfNeutralHadronsNoPileUpDeltaR_genMatched_comparison.x_expression = "pfNeutralHadronsNoPileUpDeltaR"
#pfNeutralHadronsNoPileUpDeltaR_genMatched_comparison.name = "pfNeutralHadronsNoPileUpDeltaR_genMatched_comparison"

#configs.append(pfNeutralHadronsNoPileUpDeltaR_genMatched_comparison.out_json)

#pfPhotonsNoPileUpDeltaR_genMatched_comparison = pfAllChargedParticlesNoPileupDeltaR_genMatched_comparison
#pfPhotonsNoPileUpDeltaR_genMatched_comparison.x_expression = "pfPhotonsNoPileUpDeltaR"
#pfPhotonsNoPileUpDeltaR_genMatched_comparison.name = "pfPhotonsNoPileUpDeltaR_genMatched_comparison"
#configs.append(pfPhotonsNoPileUpDeltaR_genMatched_comparison.out_json)



higgs_plotter = higgsplot.HiggsPlotter(list_of_config_dicts=configs, list_of_args_strings=[""])
