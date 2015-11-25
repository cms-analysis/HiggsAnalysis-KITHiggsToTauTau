#!/usr/bin/env python

import HiggsAnalysis.KITHiggsToTauTau.plotting.embedding.embedding_plot_classes as pltcl

### Lines for comparison of efficiencies in different pipelines

# Mu Benjamin MC 
Mu_benjamin_MC = pltcl.single_plotline(
	name="Mu_benjamin_MC",
	num_file = "/nfs/dust/cms/user/swayand/embedd_save/muonembed/ar_muonembed_K2Skim_FullReco.root",
	num_folder = "Mu_Full",
	den_folder = "genMatched",
	num_tree = "ntuple",
	label = "CMSSW_7_0_7 Z#rightarrow#mu#mu MC",
	color = "kGray+1")
Mu_Full_benjamin_MC = Mu_benjamin_MC.clone(num_folder = "Mu_Full")
Mu_NoIso_benjamin_MC = Mu_benjamin_MC.clone(num_folder = "Mu_NoIso")
Mu_iso_onlyhadrons_benjamin_MC = Mu_benjamin_MC.clone(num_folder = "Mu_iso_onlyhadrons")
Mu_iso_onlyneutral_benjamin_MC = Mu_benjamin_MC.clone(num_folder = "Mu_iso_onlyneutral")
Mu_iso_onlyphotons_benjamin_MC = Mu_benjamin_MC.clone(num_folder = "Mu_iso_onlyphotons")
Mu_iso_onlypu_benjamin_MC = Mu_benjamin_MC.clone(num_folder = "Mu_iso_onlypu")

genMatched_benjamin_MC = Mu_benjamin_MC.clone(
    num_file = "/nfs/dust/cms/user/swayand/embedd_save/eventProfile_muonembed/ar_muonembed_eventprofile_K2Skim_FullReco.root",
    num_folder = "genMatched",
    den_folder = None,
    num_tree = "muons")

# Mu Benjamin RH
Mu_benjamin_RH = pltcl.single_plotline(
	name="Mu_benjamin_RH",
	num_file = "/nfs/dust/cms/user/swayand/embedd_save/muonembed/ar_muonembed_K2Skim_Embed_RH.root",
	num_folder = "Mu_Full",
	den_folder = "genMatched",
	num_tree = "ntuple",
	label = "CMSSW_7_0_7 Z#rightarrow#mu#mu RH",
	color = "kOrange+7")
Mu_Full_benjamin_RH = Mu_benjamin_RH.clone(num_folder = "Mu_Full")
Mu_NoIso_benjamin_RH = Mu_benjamin_RH.clone(num_folder = "Mu_NoIso")
Mu_iso_onlyhadrons_benjamin_RH = Mu_benjamin_RH.clone(num_folder = "Mu_iso_onlyhadrons")
Mu_iso_onlyneutral_benjamin_RH = Mu_benjamin_RH.clone(num_folder = "Mu_iso_onlyneutral")
Mu_iso_onlyphotons_benjamin_RH = Mu_benjamin_RH.clone(num_folder = "Mu_iso_onlyphotons")
Mu_iso_onlypu_benjamin_RH = Mu_benjamin_RH.clone(num_folder = "Mu_iso_onlypu")

genMatched_benjamin_RH = Mu_benjamin_RH.clone(
    num_file = "/nfs/dust/cms/user/swayand/embedd_save/eventProfile_muonembed/ar_muonembed_eventprofile_K2Skim_Embed_RH.root",
    num_folder = "genMatched",
    den_folder = None,
    num_tree = "muons")


# Mu Benjamin PF
Mu_benjamin_PF = pltcl.single_plotline(
	name="Mu_benjamin_PF",
	num_file = "/nfs/dust/cms/user/swayand/embedd_save/muonembed/ar_muonembed_K2Skim_Embed_PF.root",
	num_folder = "Mu_Full",
	den_folder = "genMatched",
	num_tree = "ntuple",
	label = "CMSSW_7_0_7 Z#rightarrow#mu#mu PF",
	color = "kCyan+3")
Mu_Full_benjamin_PF = Mu_benjamin_PF.clone(num_folder = "Mu_Full")
Mu_NoIso_benjamin_PF = Mu_benjamin_PF.clone(num_folder = "Mu_NoIso")
Mu_iso_onlyhadrons_benjamin_PF = Mu_benjamin_PF.clone(num_folder = "Mu_iso_onlyhadrons")
Mu_iso_onlyneutral_benjamin_PF = Mu_benjamin_PF.clone(num_folder = "Mu_iso_onlyneutral")
Mu_iso_onlyphotons_benjamin_PF = Mu_benjamin_PF.clone(num_folder = "Mu_iso_onlyphotons")
Mu_iso_onlypu_benjamin_PF = Mu_benjamin_PF.clone(num_folder = "Mu_iso_onlypu")

genMatched_benjamin_PF = Mu_benjamin_PF.clone(
    num_file = "/nfs/dust/cms/user/swayand/embedd_save/eventProfile_muonembed/ar_muonembed_eventprofile_K2Skim_Embed_PF.root",
    num_folder = "genMatched",
    den_folder = None,
    num_tree = "muons")



# Mu Run2 MC 
Mu_run2_MC = pltcl.single_plotline(
	name="Mu_run2_MC",
	num_file = "/nfs/dust/cms/user/swayand/DATA_NMSSM/artus_prod_v3/MC_ZMUMU/MC_ZMUMU_merged.root",
	num_folder = "muon_full",
	den_folder = "gen_matched",
	num_tree = "ntuple",
	label = "CMSSW_7_4_12p4 Z#rightarrow#mu#mu MC",
	color = "kBlack")
Mu_Full_run2_MC = Mu_run2_MC.clone(num_folder = "muon_full")
Mu_NoIso_run2_MC = Mu_run2_MC.clone(num_folder = "no_iso")
Mu_iso_onlyhadrons_run2_MC = Mu_run2_MC.clone(num_folder = "iso_onlyhadrons")
Mu_iso_onlyneutral_run2_MC = Mu_run2_MC.clone(num_folder = "iso_onlyneutral")
Mu_iso_onlyphotons_run2_MC = Mu_run2_MC.clone(num_folder = "iso_onlyphotons")
Mu_iso_onlypu_run2_MC = Mu_run2_MC.clone(num_folder = "iso_onlypu")

genMatched_run2_MC = Mu_run2_MC.clone(num_folder = "gen_matched",den_folder = None, num_tree = "muons")


# Run 2 RH
Mu_run2_RH = pltcl.single_plotline(
	name="Mu_run2_RH",
	num_file = "/nfs/dust/cms/user/swayand/DATA_NMSSM/artus_prod_v3/RH_MIRROR/RH_MIRROR_merged.root",
	num_folder = "muon_full",
	den_folder = "gen_matched",
	num_tree = "ntuple",
	label = "CMSSW_7_4_12p4 Z#rightarrow#mu#mu RH",
	color = "kRed+2")
Mu_Full_run2_RH = Mu_run2_RH.clone(num_folder = "muon_full")
Mu_NoIso_run2_RH = Mu_run2_RH.clone(num_folder = "no_iso")
Mu_iso_onlyhadrons_run2_RH = Mu_run2_RH.clone(num_folder = "iso_onlyhadrons")
Mu_iso_onlyneutral_run2_RH = Mu_run2_RH.clone(num_folder = "iso_onlyneutral")
Mu_iso_onlyphotons_run2_RH = Mu_run2_RH.clone(num_folder = "iso_onlyphotons")
Mu_iso_onlypu_run2_RH = Mu_run2_RH.clone(num_folder = "iso_onlypu")

genMatched_run2_RH = Mu_run2_RH.clone( num_folder = "gen_matched", den_folder = None, num_tree = "muons")


# Run 2 PF
Mu_run2_PF = pltcl.single_plotline(
	name="Mu_run2_PF",
	num_file = "/nfs/dust/cms/user/swayand/DATA_NMSSM/artus_prod_v3/PF_MIRROR/PF_MIRROR_merged.root",
	num_folder = "muon_Full",
	den_folder = "gen_matched",
	num_tree = "ntuple",
	label = "CMSSW_7_4_12p4 Z#rightarrow#mu#mu PF",
	color = "kBlue")
Mu_Full_run2_PF = Mu_run2_PF.clone(num_folder = "muon_full")
Mu_NoIso_run2_PF = Mu_run2_PF.clone(num_folder = "no_iso")
Mu_iso_onlyhadrons_run2_PF = Mu_run2_PF.clone(num_folder = "iso_onlyhadrons")
Mu_iso_onlyneutral_run2_PF = Mu_run2_PF.clone(num_folder = "iso_onlyneutral")
Mu_iso_onlyphotons_run2_PF = Mu_run2_PF.clone(num_folder = "iso_onlyphotons")
Mu_iso_onlypu_run2_PF = Mu_run2_PF.clone(num_folder = "iso_onlypu")

genMatched_run2_PF = Mu_run2_PF.clone( num_folder = "gen_matched", den_folder = None, num_tree = "muons")





