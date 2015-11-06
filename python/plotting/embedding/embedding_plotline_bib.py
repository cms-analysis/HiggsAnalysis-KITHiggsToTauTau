#!/usr/bin/env python

import HiggsAnalysis.KITHiggsToTauTau.plotting.embedding.embedding_plot_classes as pltcl


Mu_Full_benjamin_MC = pltcl.single_plotline(
	name="Mu_Full_benjamin_MC",
	num_file = "/nfs/dust/cms/user/swayand/embedd_save/muonembed/ar_muonembed_K2Skim_FullReco.root",
	num_folder = "Mu_Full",
	den_folder = "genMatched",
	num_tree = "ntuple",
	label = "CMSSW_7_0_7 full MC",
	color = "kBlue")

Mu_Full_benjamin_RH = pltcl.single_plotline(
	name="Mu_Full_benjamin_RH",
	num_file = "/nfs/dust/cms/user/swayand/embedd_save/muonembed/ar_muonembed_K2Skim_Embed_RH.root",
	num_folder = "Mu_Full",
	den_folder = "genMatched",
	num_tree = "ntuple",
	label = "CMSSW_7_0_7 RH",
	color = "kCyan+1")

Mu_Full_run2_MC = pltcl.single_plotline(
	name="Mu_Full_run2_MC",
	num_file = "/nfs/dust/cms/user/swayand/DATA_NMSSM/artus_prod/MC_ZMUMU/MC_ZMUMU_merged.root",
	num_folder = "muon_full",
	den_folder = "gen_matched",
	num_tree = "ntuple",
	label = "CMSSW_7_4_12p4 full MC",
	color = "kRed+2")

Mu_Full_run2_RH = pltcl.single_plotline(
	name="Mu_Full_run2_RH",
	num_file = "/nfs/dust/cms/user/swayand/DATA_NMSSM/artus_prod/RH_MIRROR/RH_MIRROR_merged.root",
	num_folder = "muon_full",
	den_folder = "gen_matched",
	num_tree = "ntuple",
	label = "CMSSW_7_4_12p4 RH",
	color = "kOrange+7")



Mu_NoIso_benjamin_MC = pltcl.single_plotline(
	name="Mu_NoIso_benjamin_MC",
	num_file = "/nfs/dust/cms/user/swayand/embedd_save/muonembed/ar_muonembed_K2Skim_FullReco.root",
	num_folder = "Mu_NoIso",
	den_folder = "genMatched",
	num_tree = "ntuple",
	label = "CMSSW_7_0_7 full MC",
	color = "kBlue")

Mu_NoIso_benjamin_RH = pltcl.single_plotline(
	name="Mu_NoIso_benjamin_RH",
	num_file = "/nfs/dust/cms/user/swayand/embedd_save/muonembed/ar_muonembed_K2Skim_Embed_RH.root",
	num_folder = "Mu_NoIso",
	den_folder = "genMatched",
	num_tree = "ntuple",
	label = "CMSSW_7_0_7 RH",
	color = "kCyan+1")

Mu_NoIso_run2_MC = pltcl.single_plotline(
	name="Mu_NoIso_run2_MC",
	num_file = "/nfs/dust/cms/user/swayand/DATA_NMSSM/artus_prod_fix/MC_ZMUMU/MC_ZMUMU_merged.root",
	num_folder = "no_iso",
	den_folder = "gen_matched",
	num_tree = "ntuple",
	label = "CMSSW_7_4_12p4 full MC",
	color = "kRed+2")

Mu_NoIso_run2_RH = pltcl.single_plotline(
	name="Mu_NoIso_run2_RH",
	num_file = "/nfs/dust/cms/user/swayand/DATA_NMSSM/artus_prod_fix/RH_MIRROR/RH_MIRROR_merged.root",
	num_folder = "no_iso",
	den_folder = "gen_matched",
	num_tree = "ntuple",
	label = "CMSSW_7_4_12p4 RH",
	color = "kOrange+7")



genMatched_benjamin_MC = pltcl.single_plotline(
	name="genMatched_benjamin_MC",
	num_file = "/nfs/dust/cms/user/swayand/embedd_save/eventProfile_muonembed/ar_muonembed_eventprofile_K2Skim_FullReco.root",
	num_folder = "genMatched",
	den_folder = "genMatched",
	num_tree = "muons",
	label = "CMSSW_7_0_7 full MC",
	color = "kBlue")

genMatched_benjamin_RH = pltcl.single_plotline(
	name="genMatched_benjamin_RH",
	num_file = "/nfs/dust/cms/user/swayand/embedd_save/eventProfile_muonembed/ar_muonembed_eventprofile_K2Skim_Embed_RH.root",
	num_folder = "genMatched",
	den_folder = "genMatched",
	num_tree = "muons",
	label = "CMSSW_7_0_7 RH",
	color = "kCyan+1")

genMatched_run2_MC = pltcl.single_plotline(
	name="genMatched_run2_MC",
	num_file = "/nfs/dust/cms/user/swayand/DATA_NMSSM/artus_prod/MC_ZMUMU/MC_ZMUMU_merged.root",
	num_folder = "gen_matched",
	den_folder = "gen_matched",
	num_tree = "muons",
	label = "CMSSW_7_4_12p4 full MC",
	color = "kRed+2")

genMatched_run2_RH = pltcl.single_plotline(
	name="genMatched_run2_RH",
	num_file = "/nfs/dust/cms/user/swayand/DATA_NMSSM/artus_prod/RH_MIRROR/RH_MIRROR_merged.root",
	num_folder = "gen_matched",
	den_folder = "gen_matched",
	num_tree = "muons",
	label = "CMSSW_7_4_12p4 RH",
	color = "kOrange+7")



