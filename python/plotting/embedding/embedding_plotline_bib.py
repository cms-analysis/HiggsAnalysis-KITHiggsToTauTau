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


### Lines for CMSSW Zmumu selection


zmumu_genfilter_all = pltcl.single_plotline(
        name="zmumu",
        num_file = "/nfs/dust/cms/user/aakhmets/DATA_EMBEDDING/hist_merged.root",
        num_folder = "genfilter/all",
        den_folder = "genfilter/all",
        num_tree = "",
        label = "Z#rightarrow#mu#mu MC (genfilter)",
        color = "kGrey")

zmumu_genfilter_MC_matched = zmumu_genfilter_all.clone(num_folder = "genfilter/MC_matched",
                                                       den_folder = "genfilter/MC_matched")
zmumu_genfilter_not_MC_matched = zmumu_genfilter_all.clone(num_folder = "genfilter/not_MC_matched",
                                                           den_folder = "genfilter/not_MC_matched")

zmumu_baseline_all = zmumu_genfilter_all.clone(num_folder = "baseline/all",
                                               color = "kRed",
                                               label = "Z#rightarrow#mu#mu MC (baseline)")
zmumu_baseline_MC_matched = zmumu_genfilter_MC_matched.clone(num_folder = "baseline/MC_matched",
                                                             color = "kRed",
                                                             label = "Z#rightarrow#mu#mu MC (baseline)")
zmumu_baseline_not_MC_matched = zmumu_genfilter_not_MC_matched.clone(num_folder = "baseline/not_MC_matched",
                                                                     color = "kRed",
                                                                     label = "Z#rightarrow#mu#mu MC (baseline)")

zmumu_id_all = zmumu_genfilter_all.clone(num_folder = "id/all",
                                         color = "kBlue",
                                         label = "Z#rightarrow#mu#mu MC (id)")
zmumu_id_MC_matched = zmumu_genfilter_MC_matched.clone(num_folder = "id/MC_matched",
                                                       color = "kBlue",
                                                       label = "Z#rightarrow#mu#mu MC (id)")
zmumu_id_not_MC_matched = zmumu_genfilter_not_MC_matched.clone(num_folder = "id/not_MC_matched",
                                                               color = "kBlue",
                                                               label = "Z#rightarrow#mu#mu MC (id)")

zmumu_id_and_trigger_all = zmumu_genfilter_all.clone(num_folder = "id_and_trigger/all",
                                                     color = "kGreen",
                                                     label = "Z#rightarrow#mu#mu MC (trigger_and_id)")
zmumu_id_and_trigger_MC_matched = zmumu_genfilter_MC_matched.clone(num_folder = "id_and_trigger/MC_matched",
                                                                   color = "kGreen",
                                                                   label = "Z#rightarrow#mu#mu MC (trigger_and_id)")
zmumu_id_and_trigger_not_MC_matched = zmumu_genfilter_not_MC_matched.clone(num_folder = "id_and_trigger/not_MC_matched",
                                                                           color = "kGreen",
                                                                           label = "Z#rightarrow#mu#mu MC (trigger_and_id)")



