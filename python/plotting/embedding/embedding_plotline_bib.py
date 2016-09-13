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
	num_file = "/nfs/dust/cms/user/aakhmets/for763/CMSSW_7_1_5/src/output_pythia_normal.root",
	num_folder = "acc_eff",
	den_folder = "acc_eff",
	num_tree = "ntuple",
	label = "pythia8",
	color = "kRed")

eMinusmuPlus_CP_spin_tauola = eMinusmuPlus_CP_spin_pythia.clone(
	num_file = "/nfs/dust/cms/user/aakhmets/for763/CMSSW_7_1_5/src/output_tauola_normal.root",
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


# bare vs. dressed (emu channel)

Bare_pythia = pltcl.single_plotline(
	name = "Bare_pythia",
	num_file = "/nfs/dust/cms/user/aakhmets/for763/CMSSW_7_1_5/src/output_pythia_bare.root",
	num_folder = "acc_eff",
	den_folder = "acc_eff",
	num_tree = "ntuple",
	label = "bare",
	color = "kRed")

Dressed_pythia = Bare_pythia.clone(
	name = "Dressed_pythia",
	num_file = "/nfs/dust/cms/user/aakhmets/for763/CMSSW_7_1_5/src/output_pythia_dressed.root",
	label = "dressed",
	color = "kBlue")


Normal_pythia = Bare_pythia.clone(
	name = "Dressed_pythia",
	num_file = "/nfs/dust/cms/user/aakhmets/for763/CMSSW_7_1_5/src/output_pythia_normal.root",
	label = "usual reco",
	color = "kBlack")


### Full Z->TauTau MC


# EM channel

FSRstudies_EM = pltcl.single_plotline(
	name = "FSRstudies_EM",
	num_file = "/nfs/dust/cms/user/aakhmets/htautau/artus/2016-04-13_14-39_analysis/merged/DYJetsToLLM50_RunIIFall15MiniAODv2_PU25nsData2015v1_13TeV_MINIAOD_madgraph-pythia8/DYJetsToLLM50_RunIIFall15MiniAODv2_PU25nsData2015v1_13TeV_MINIAOD_madgraph-pythia8.root",
	num_folder = "FSRstudies_EM_eleEsNom",
	den_folder = "FSRstudies_EM_eleEsNom",
	num_tree = "ntuple",
	label = "Z#rightarrow#tau#tau sim.",
	color = "kOrange+7")

FSRstudies_EM_emb_afterFSR = FSRstudies_EM.clone(
	name = "FSRstudies_EM_emb_afterFSR",
	num_file = "/nfs/dust/cms/user/aakhmets/htautau/artus/2016-04-13_14-17_analysis/merged/ZtoTauTauEmbedded_EM/ZtoTauTauEmbedded_EM.root",
	num_folder = "FSRstudies_EM_eleEsNom",
	den_folder = "FSRstudies_EM_eleEsNom",
	label = "#mu#rightarrow#tau emb. #pm 2% e-ES",
	color = "kBlue")

FSRstudies_EM_emb_afterFSR_up = FSRstudies_EM_emb_afterFSR.clone(
	name = "FSRstudies_EM_emb_afterFSR_up",
	num_folder = "FSRstudies_EM_eleEsUp",
	den_folder = "FSRstudies_EM_eleEsUp",
	label = "",
	color = "kCyan+1")

FSRstudies_EM_emb_afterFSR_down = FSRstudies_EM_emb_afterFSR.clone(
	name = "FSRstudies_EM_emb_afterFSR_down",
	num_folder = "FSRstudies_EM_eleEsDown",
	den_folder = "FSRstudies_EM_eleEsDown",
	label = "",
	color = "kCyan+2")


FSRstudies_EM_higgs = FSRstudies_EM.clone(
	name = "FSRstudies_EM_higgs",
	num_file = "/nfs/dust/cms/user/aakhmets/htautau/artus/2016-04-13_14-40_analysis/merged/GluGluHToTauTauM125_RunIIFall15MiniAODv2_PU25nsData2015v1_13TeV_MINIAOD_powheg-pythia8/GluGluHToTauTauM125_RunIIFall15MiniAODv2_PU25nsData2015v1_13TeV_MINIAOD_powheg-pythia8.root",
	label = "H(125)",
	color = "kBlack"
	)


# ET channel


FSRstudies_ET = FSRstudies_EM.clone(
	name = "FSRstudies_ET",
	num_folder = "FSRstudies_ET_tauEsNom",
	den_folder = "FSRstudies_ET_tauEsNom")

FSRstudies_ET_emb_afterFSR = FSRstudies_EM_emb_afterFSR.clone(
	name = "FSRstudies_ET_emb_afterFSR",
	num_file = "/nfs/dust/cms/user/aakhmets/htautau/artus/2016-04-13_14-13_analysis/merged/ZtoTauTauEmbedded_ET/ZtoTauTauEmbedded_ET.root",
	num_folder = "FSRstudies_ET_tauEsNom",
	den_folder = "FSRstudies_ET_tauEsNom",
	label = "#mu#rightarrow#tau emb. #pm 3% #tau_{h}-ES")

FSRstudies_ET_emb_afterFSR_up = FSRstudies_EM_emb_afterFSR_up.clone(
	name = "FSRstudies_ET_emb_afterFSR_up",
	num_file = "/nfs/dust/cms/user/aakhmets/htautau/artus/2016-04-13_14-13_analysis/merged/ZtoTauTauEmbedded_ET/ZtoTauTauEmbedded_ET.root",
	num_folder = "FSRstudies_ET_tauEsUp",
	den_folder = "FSRstudies_ET_tauEsUp")

FSRstudies_ET_emb_afterFSR_down = FSRstudies_EM_emb_afterFSR_down.clone(
	name = "FSRstudies_ET_emb_afterFSR_down",
	num_file = "/nfs/dust/cms/user/aakhmets/htautau/artus/2016-04-13_14-13_analysis/merged/ZtoTauTauEmbedded_ET/ZtoTauTauEmbedded_ET.root",
	num_folder = "FSRstudies_ET_tauEsDown",
	den_folder = "FSRstudies_ET_tauEsDown")

FSRstudies_ET_higgs = FSRstudies_EM_higgs.clone(
	name = "FSRstudies_ET_higgs",
	num_folder = "FSRstudies_ET_tauEsNom",
	den_folder = "FSRstudies_ET_tauEsNom"
	)

# MT channel

FSRstudies_MT = FSRstudies_EM.clone(
	name = "FSRstudies_MT",
	num_folder = "FSRstudies_MT_tauEsNom",
	den_folder = "FSRstudies_MT_tauEsNom")

FSRstudies_MT_emb_afterFSR = FSRstudies_EM_emb_afterFSR.clone(
	name = "FSRstudies_MT_emb_afterFSR",
	num_file = "/nfs/dust/cms/user/aakhmets/htautau/artus/2016-04-13_14-03_analysis/merged/ZtoTauTauEmbedded_MT/ZtoTauTauEmbedded_MT.root",
	num_folder = "FSRstudies_MT_tauEsNom",
	den_folder = "FSRstudies_MT_tauEsNom",
	label = "#mu#rightarrow#tau emb. #pm 3% #tau_{h}-ES")

FSRstudies_MT_emb_afterFSR_up = FSRstudies_EM_emb_afterFSR_up.clone(
	name = "FSRstudies_MT_emb_afterFSR_up",
	num_file = "/nfs/dust/cms/user/aakhmets/htautau/artus/2016-04-13_14-03_analysis/merged/ZtoTauTauEmbedded_MT/ZtoTauTauEmbedded_MT.root",
	num_folder = "FSRstudies_MT_tauEsUp",
	den_folder = "FSRstudies_MT_tauEsUp")

FSRstudies_MT_emb_afterFSR_down = FSRstudies_EM_emb_afterFSR_down.clone(
	name = "FSRstudies_MT_emb_afterFSR_down",
	num_file = "/nfs/dust/cms/user/aakhmets/htautau/artus/2016-04-13_14-03_analysis/merged/ZtoTauTauEmbedded_MT/ZtoTauTauEmbedded_MT.root",
	num_folder = "FSRstudies_MT_tauEsDown",
	den_folder = "FSRstudies_MT_tauEsDown")

FSRstudies_MT_higgs = FSRstudies_EM_higgs.clone(
	name = "FSRstudies_MT_higgs",
	num_folder = "FSRstudies_MT_tauEsNom",
	den_folder = "FSRstudies_MT_tauEsNom"
	)

# TT channel

FSRstudies_TT = FSRstudies_EM.clone(
	name = "FSRstudies_TT",
	num_folder = "FSRstudies_TT_tauEsNom",
	den_folder = "FSRstudies_TT_tauEsNom")

FSRstudies_TT_emb_afterFSR = FSRstudies_EM_emb_afterFSR.clone(
	name = "FSRstudies_TT_emb_afterFSR",
	num_file = "/nfs/dust/cms/user/aakhmets/htautau/artus/2016-04-13_14-16_analysis/merged/ZtoTauTauEmbedded_TT/ZtoTauTauEmbedded_TT.root",
	num_folder = "FSRstudies_TT_tauEsNom",
	den_folder = "FSRstudies_TT_tauEsNom",
	label = "#mu#rightarrow#tau emb. #pm 3% #tau_{h}-ES")

FSRstudies_TT_emb_afterFSR_up = FSRstudies_EM_emb_afterFSR_up.clone(
	name = "FSRstudies_TT_emb_afterFSR_up",
	num_file = "/nfs/dust/cms/user/aakhmets/htautau/artus/2016-04-13_14-16_analysis/merged/ZtoTauTauEmbedded_TT/ZtoTauTauEmbedded_TT.root",
	num_folder = "FSRstudies_TT_tauEsUp",
	den_folder = "FSRstudies_TT_tauEsUp")

FSRstudies_TT_emb_afterFSR_down = FSRstudies_EM_emb_afterFSR_down.clone(
	name = "FSRstudies_TT_emb_afterFSR_down",
	num_file = "/nfs/dust/cms/user/aakhmets/htautau/artus/2016-04-13_14-16_analysis/merged/ZtoTauTauEmbedded_TT/ZtoTauTauEmbedded_TT.root",
	num_folder = "FSRstudies_TT_tauEsDown",
	den_folder = "FSRstudies_TT_tauEsDown")

FSRstudies_TT_higgs = FSRstudies_EM_higgs.clone(
	name = "FSRstudies_TT_higgs",
	num_folder = "FSRstudies_TT_tauEsNom",
	den_folder = "FSRstudies_TT_tauEsNom"
	)

### Embedding Cleaning Check

DoubleMuonMINIAOD = pltcl.single_plotline(
	name = "DoubleMuonMINIAOD",
	num_file = "/portal/ekpcms5/home/akhmet/CMSSW_7_1_5/src/eventmatching.root",
	num_folder = "",
	den_folder = "",
	num_tree = "common3",
	label = "Run2015D",
	color = "kBlack")

DoubleMuonMINIAODonfly = DoubleMuonMINIAOD.clone(
	name = "DoubleMuonMINIAODonfly",
	num_file = "/portal/ekpcms5/home/akhmet/CMSSW_7_1_5/src/eventmatching.root",
	num_tree = "common2",
	label = "private",
	color = "kRed")

DoubleMuonCleaned = DoubleMuonMINIAOD.clone(
	name = "DoubleMuonCleaned",
	num_file = "/portal/ekpcms5/home/akhmet/CMSSW_7_1_5/src/eventmatching.root",
	num_tree = "common1",
	label = "track cleaning",
	color = "kGreen+2")

DoubleMuonCleanedCalo = DoubleMuonMINIAOD.clone(
name = "DoubleMuonCleanedCalo",
num_file = "/portal/ekpcms5/home/akhmet/CMSSW_7_1_5/src/eventmatching.root",
num_tree = "common4",
label = "cleaned (w. calo)",
color = "kOrange")

DoubleMuonFullyCleaned = DoubleMuonMINIAOD.clone(
name = "DoubleMuonFullyCleaned",
num_file = "/portal/ekpcms5/home/akhmet/CMSSW_7_1_5/src/eventmatching.root",
num_tree = "common4",
label = "full cleaning",
color = "kBlue")


## vertex correction check for Muon Embedding

vtx_corrected_MM = pltcl.single_plotline(
	name = "vtx_corrected_MM",
	num_file = "/portal/ekpcms5/home/akhmet/CMSSW_7_4_7/src/EmbeddingVertexCorrection.root",
	num_folder = "histograms",
	den_folder = "histograms",
	num_tree = "",
	color = "kBlack")

## Merging Input Check for Muon Embedding

DoubleMuonSelected = pltcl.single_plotline(
	name = "DoubleMuonSelected",
	num_file = "/portal/ekpcms5/home/akhmet/CMSSW_7_4_7/src/selected.root",
	num_folder = "input_check",
	den_folder = "input_check",
	num_tree = "ntuple",
	label = "Run2015D",
	color = "kBlack")

DoubleMuonMerged = DoubleMuonSelected.clone(
	name = "DoubleMuonMerged",
	num_file = "/portal/ekpcms5/home/akhmet/CMSSW_7_4_7/src/merged.root",
	label = "Embedded",
	color = "kRed")

DoubleMuonCleaned = DoubleMuonSelected.clone(
	name = "DoubleMuonCleaned",
	num_file = "/portal/ekpcms5/home/akhmet/CMSSW_7_4_7/src/cleaned.root",
	label = "Cleaned",
	color = "kGreen")

## Z->mumu selection check for Muon Embedding

DoubleMuonSelectedValidation = pltcl.single_plotline(
	name = "DoubleMuonSelectedValidation",
	num_file = "/portal/ekpcms5/home/akhmet/CMSSW_7_4_7/src/selected.root",
	num_folder = "zmumu_selection_for_embedding",
	den_folder = "zmumu_selection_for_embedding",
	num_tree = "ntuple",
	label = "Run2015D",
	color = "kBlack")

DoubleMuonMergedValidation = DoubleMuonSelectedValidation.clone(
	name = "DoubleMuonMergedValidation",
	num_file = "/portal/ekpcms5/home/akhmet/CMSSW_7_4_7/src/embedded.root",
	label = "#mu#rightarrow#mu embedded",
	color = "kRed")

DoubleMuonMirroredValidation = DoubleMuonSelectedValidation.clone(
	name = "DoubleMuonMirroredValidation",
	num_file = "/portal/ekpcms5/home/akhmet/CMSSW_7_4_7/src/mirrored.root",
	label = "#splitline{#mu#rightarrow#mu embedded}{w. mirroring}",
	color = "kBlue")
