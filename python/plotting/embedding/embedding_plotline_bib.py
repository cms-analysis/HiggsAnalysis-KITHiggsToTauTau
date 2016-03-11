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
        num_file = "/nfs/dust/cms/user/aakhmets/DATA_EMBEDDING/hist2_merged.root",
        num_folder = "genfilter/all",
        den_folder = "genfilter/all",
        num_tree = "",
        label = "gen. filter",
        color = "kBlack")

zmumu_genfilter_MC_matched = zmumu_genfilter_all.clone(num_folder = "genfilter/MC_matched",
                                                       den_folder = "genfilter/MC_matched")
zmumu_genfilter_not_MC_matched = zmumu_genfilter_all.clone(num_folder = "genfilter/not_MC_matched",
                                                           den_folder = "genfilter/not_MC_matched")

zmumu_baseline_all = zmumu_genfilter_all.clone(num_folder = "baseline/all",
                                               color = "kRed",
                                               label = "baseline sel.")
zmumu_baseline_MC_matched = zmumu_genfilter_MC_matched.clone(num_folder = "baseline/MC_matched",
                                                             color = "kRed",
                                                             label = "baseline sel.")
zmumu_baseline_not_MC_matched = zmumu_genfilter_not_MC_matched.clone(num_folder = "baseline/not_MC_matched",
                                                                     color = "kRed",
                                                                     label = "baseline sel.")

zmumu_id_all = zmumu_genfilter_all.clone(num_folder = "id/all",
                                         color = "kBlue",
                                         label = "ID")
zmumu_id_MC_matched = zmumu_genfilter_MC_matched.clone(num_folder = "id/MC_matched",
                                                       color = "kBlue",
                                                       label = "ID")
zmumu_id_not_MC_matched = zmumu_genfilter_not_MC_matched.clone(num_folder = "id/not_MC_matched",
                                                               color = "kBlue",
                                                               label = "ID")

zmumu_id_and_trigger_all = zmumu_genfilter_all.clone(num_folder = "id_and_trigger/all",
                                                     color = "kGreen",
                                                     label = "ID & Trigger")
zmumu_id_and_trigger_MC_matched = zmumu_genfilter_MC_matched.clone(num_folder = "id_and_trigger/MC_matched",
                                                                   color = "kGreen",
                                                                   label = "ID & Trigger")
zmumu_id_and_trigger_not_MC_matched = zmumu_genfilter_not_MC_matched.clone(num_folder = "id_and_trigger/not_MC_matched",
                                                                           color = "kGreen",
                                                                           label = "ID & Trigger")

### Acceptance efficiency histograms

eMinusmuPlus_pythia = pltcl.single_plotline(
	name = "eMinusmuPlus",
	num_file = "/nfs/dust/cms/user/aakhmets/for763/CMSSW_7_1_5/src/output_pythia_em_mup.root",
	num_folder = "acc_eff",
	den_folder = "acc_eff",
	num_tree = "ntuple",
	label = "pythia8",
	color = "kRed")

eMinusmuPlus_tauola = eMinusmuPlus_pythia.clone(
	num_file = "/nfs/dust/cms/user/aakhmets/for763/CMSSW_7_1_5/src/output_tauola_em_mup.root",
	label = "tauola",
	color = "kBlue")

eMinusmuPlus_pythia_2D = eMinusmuPlus_pythia.clone(num_tree = "", marker = "COLZ", color = None)
eMinusmuPlus_tauola_2D = eMinusmuPlus_tauola.clone(num_tree = "", marker = "COLZ", color = None)



ePlusmuMinus_pythia = eMinusmuPlus_pythia.clone(
	name = "ePlusmuMinus",
	num_file = "/nfs/dust/cms/user/aakhmets/for763/CMSSW_7_1_5/src/output_pythia_ep_mum.root",
	num_folder = "acc_eff",
	den_folder = "acc_eff",
	num_tree = "ntuple")

ePlusmuMinus_tauola = ePlusmuMinus_pythia.clone(
	num_file = "/nfs/dust/cms/user/aakhmets/for763/CMSSW_7_1_5/src/output_tauola_ep_mum.root",
	label = "tauola",
	color = "kBlue")

ePlusmuMinus_pythia_2D = ePlusmuMinus_pythia.clone(num_tree = "", marker = "COLZ", color = None)
ePlusmuMinus_tauola_2D = ePlusmuMinus_tauola.clone(num_tree = "", marker = "COLZ", color = None)


ePlusmuMinus_tauola_path1 = ePlusmuMinus_tauola.clone(
	num_file = "/nfs/dust/cms/user/aakhmets/for763/CMSSW_7_1_5/src/output_tauola_ep_mum_path1.root")


### CP and Spin quantities

# for eMinusmuPlus

eMinusmuPlus_CP_spin_pythia = pltcl.single_plotline(
	name = "eMinusmuPlus_CP_spin",
	num_file = "/nfs/dust/cms/user/aakhmets/for763/CMSSW_7_1_5/src/output1_pythia.root",
	num_folder = "acc_eff",
	den_folder = "acc_eff",
	num_tree = "ntuple",
	label = "pythia8",
	color = "kRed")

eMinusmuPlus_CP_spin_tauola = eMinusmuPlus_CP_spin_pythia.clone(
	num_file = "/nfs/dust/cms/user/aakhmets/for763/CMSSW_7_1_5/src/output1_tauola.root",
	label = "tauola",
	color = "kBlue")
	
eMinusmuPlus_CP_spin_pythia_2D = eMinusmuPlus_CP_spin_pythia.clone(marker = "COLZ", color = None)
eMinusmuPlus_CP_spin_tauola_2D = eMinusmuPlus_CP_spin_tauola.clone(marker = "COLZ", color = None)

# for eMinusmuPlus (no cut)

eMinusmuPlus_CP_spin_pythia_nocut = pltcl.single_plotline(
	name = "eMinusmuPlus_CP_spin_nocut",
	num_file = "/nfs/dust/cms/user/aakhmets/for763/CMSSW_7_1_5/src/output_pythia_em_mup_nocut_polOn.root",
	num_folder = "acc_eff",
	den_folder = "acc_eff",
	num_tree = "ntuple",
	label = "pythia8",
	color = "kRed")

eMinusmuPlus_CP_spin_tauola_nocut = eMinusmuPlus_CP_spin_pythia_nocut.clone(
	num_file = "/nfs/dust/cms/user/aakhmets/for763/CMSSW_7_1_5/src/output_tauola_em_mup_nocut_polOn.root",
	label = "tauola",
	color = "kBlue")
	
eMinusmuPlus_CP_spin_pythia_2D_nocut = eMinusmuPlus_CP_spin_pythia_nocut.clone(marker = "COLZ", color = None)
eMinusmuPlus_CP_spin_tauola_2D_nocut = eMinusmuPlus_CP_spin_tauola_nocut.clone(marker = "COLZ", color = None)

# for PiPlusPiMinus

PiPlusPiMinus_CP_spin_pythia = pltcl.single_plotline(
	name = "PiPlusPiMinus_CP_spin",
	num_file = "/nfs/dust/cms/user/aakhmets/for763/CMSSW_7_1_5/src/output1_pythia_pipi.root",
	num_folder = "acc_eff",
	den_folder = "acc_eff",
	num_tree = "ntuple",
	label = "pythia8",
	color = "kRed")

PiPlusPiMinus_CP_spin_tauola = PiPlusPiMinus_CP_spin_pythia.clone(
	num_file = "/nfs/dust/cms/user/aakhmets/for763/CMSSW_7_1_5/src/output1_tauola_pipi.root",
	label = "tauola",
	color = "kBlue")
	
PiPlusPiMinus_CP_spin_pythia_2D = PiPlusPiMinus_CP_spin_pythia.clone(marker = "COLZ", color = None)
PiPlusPiMinus_CP_spin_tauola_2D = PiPlusPiMinus_CP_spin_tauola.clone(marker = "COLZ", color = None)

# for PiPlusPiMinus (no cut)

PiPlusPiMinus_CP_spin_pythia_nocut = pltcl.single_plotline(
	name = "PiPlusPiMinus_CP_spin_nocut",
	num_file = "/nfs/dust/cms/user/aakhmets/for763/CMSSW_7_1_5/src/output1_pythia_pipi_nocut.root",
	num_folder = "acc_eff",
	den_folder = "acc_eff",
	num_tree = "ntuple",
	label = "pythia8",
	color = "kRed")

PiPlusPiMinus_CP_spin_tauola_nocut = PiPlusPiMinus_CP_spin_pythia.clone(
	num_file = "/nfs/dust/cms/user/aakhmets/for763/CMSSW_7_1_5/src/output1_tauola_pipi_nocut_polOn.root",
	label = "tauola",
	color = "kBlue")
	
PiPlusPiMinus_CP_spin_pythia_2D_nocut = PiPlusPiMinus_CP_spin_pythia_nocut.clone(marker = "COLZ", color = None)
PiPlusPiMinus_CP_spin_tauola_2D_nocut = PiPlusPiMinus_CP_spin_tauola_nocut.clone(marker = "COLZ", color = None)

# for PiPlusPiMinus (no cut) long

PiPlusPiMinus_CP_spin_pythia_nocut_long = pltcl.single_plotline(
	name = "PiPlusPiMinus_CP_spin_nocut_long",
	num_file = "/nfs/dust/cms/user/aakhmets/for763/CMSSW_7_1_5/src/output1_pythia_pipi_nocut_long.root",
	num_folder = "acc_eff",
	den_folder = "acc_eff",
	num_tree = "ntuple",
	label = "pythia8",
	color = "kRed")

PiPlusPiMinus_CP_spin_tauola_nocut_long = PiPlusPiMinus_CP_spin_pythia.clone(
	num_file = "/nfs/dust/cms/user/aakhmets/for763/CMSSW_7_1_5/src/output1_tauola_pipi_nocut_long.root",
	label = "tauola",
	color = "kBlue")
	
PiPlusPiMinus_CP_spin_pythia_2D_nocut_long = PiPlusPiMinus_CP_spin_pythia_nocut_long.clone(marker = "COLZ", color = None)
PiPlusPiMinus_CP_spin_tauola_2D_nocut_long = PiPlusPiMinus_CP_spin_tauola_nocut_long.clone(marker = "COLZ", color = None)
