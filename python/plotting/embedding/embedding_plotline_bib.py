#!/usr/bin/env python

import HiggsAnalysis.KITHiggsToTauTau.plotting.embedding.embedding_plot_classes as pltcl



### Default line difinition

# Run 2 MC
run2_MC_def = pltcl.single_plotline(
	name="run2_MC_def",
	num_file = "/nfs/dust/cms/user/swayand/DATA_NMSSM/merged_files/MC.root",
	num_folder = "gen_matched",
	den_folder = "gen_matched",
	num_tree = "ntuple",
	label = "Z#rightarrow#mu#mu MC",
	color = "kBlack")

# Run 2 RH
run2_RH_def = pltcl.single_plotline(
	name="run2_RH_def",
	num_file = "/nfs/dust/cms/user/swayand/DATA_NMSSM/merged_files/RH_Mirror.root",
	num_folder = "gen_matched",
	den_folder = "gen_matched",
	num_tree = "ntuple",
	label = "Z#rightarrow#mu#mu RH",
	color = "kRed+2")


### Lines for efficiencies in different pipelines

# Run 2 MC
run2_MC_full = run2_MC_def.clone(num_folder = "muon_full")
run2_MC_id = run2_MC_def.clone(num_folder = "muon_medium")
run2_MC_iso = run2_MC_def.clone(num_folder = "muon_iso")

# Run 2 RH
run2_RH_full = run2_RH_def.clone(num_folder = "muon_full")
run2_RH_id = run2_RH_def.clone(num_folder = "muon_medium")
run2_RH_iso = run2_RH_def.clone(num_folder = "muon_iso")


### Lines for Pt-Flow in different pipelines

run2_MC_PtFlow = run2_MC_def.clone(num_tree = "")
run2_RH_PtFlow = run2_RH_def.clone(num_tree = "")


