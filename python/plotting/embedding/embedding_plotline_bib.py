#!/usr/bin/env python

import HiggsAnalysis.KITHiggsToTauTau.plotting.embedding.embedding_plot_classes as pltcl
 
## Vertex Refitting Check for Muon Embedding
vtx_corrected_MM = pltcl.single_plotline(
	name = "vtx_corrected_MM",
	num_file = "/portal/ekpcms5/home/akhmet/CMSSW_7_4_7/src/EmbeddingVertexCorrection.root",
	num_folder = "histograms",
	den_folder = "histograms",
	num_tree = "",
	color = "kRed")

DYPrefitShape = pltcl.single_plotline(
	name = "DYPrefitShape",
	num_file = "/portal/ekpbms2/home/jbechtel/analysis/CMSSW_7_4_7/src/CombineHarvester/MSSMFull2016/shapes_160916.root",
	num_folder = "htt_mt_8_13TeV_prefit",
	#den_folder = "input_check",
	num_tree = "ZTT",
	label = "Monte Carlo",
	color = "kRed")
	
EmbeddingPrefitShape = pltcl.single_plotline(
	name = "EmbeddingPrefitShape",
	num_file = "/portal/ekpbms2/home/jbechtel/analysis/CMSSW_7_4_7/src/CombineHarvester/MSSMFull2016/emb/shapes_160916.root",
	num_folder = "htt_mt_8_13TeV_prefit",
	#den_folder = "input_check",
	num_tree = "ZTT",
	label = "Embedding",
	color = "kBlack")
## Embedding and Cleaning Input Check for Muon Embedding

DoubleMuonSelected = pltcl.single_plotline(
	name = "DoubleMuonSelected",
	num_file = "/portal/ekpbms1/home/akhmet/2016-10-11_23-45_analysis/merged/selected/selected.root",
	num_folder = "input_check",
	den_folder = "input_check",
	num_tree = "ntuple",
	label = "data ",
	color = "kBlack")

DoubleMuonEmbedded = DoubleMuonSelected.clone(
	name = "DoubleMuonEmbedded",
	num_file = "/portal/ekpbms1/home/akhmet/2016-10-11_23-36_analysis/merged/embedded/embedded.root",
	label = "#mu#rightarrow#mu embedded",
	color = "kRed")

DoubleMuonCleaned = DoubleMuonSelected.clone(
	name = "DoubleMuonCleaned",
	num_file = "/portal/ekpbms1/home/akhmet/2016-10-11_23-47_analysis/merged/cleaned/cleaned.root",
	label = "data (cleaned)",
	color = "kSpring-9")

DoubleMuonTrackcleaned = DoubleMuonSelected.clone(
	name = "DoubleMuonTrackcleaned",
	num_file = "/portal/ekpbms1/home/akhmet/2016-10-11_23-48_analysis/merged/trackcleaned/trackcleaned.root",
	label = "data (tracks cleaned)",
	color = "kCyan+3")

DoubleMuonMirrored= DoubleMuonSelected.clone(
	name = "DoubleMuonMirrored",
	num_file = "/portal/ekpbms1/home/akhmet/2016-10-11_23-46_analysis/merged/mirrored/mirrored.root",
	label = "#splitline{#mu#rightarrow#mu embedded}{w. mirroring}",
	color = "kBlue")

## Z->mumu selection check for Muon Embedding

DoubleMuonSelectedValidation = pltcl.single_plotline(
	name = "DoubleMuonSelectedValidation",
	num_file = "/portal/ekpbms1/home/akhmet/2016-10-11_23-45_analysis/merged/selected/selected.root",
	num_folder = "zmumu_selection_for_embedding",
	den_folder = "zmumu_selection_for_embedding",
	num_tree = "ntuple",
	label = "data ",
	color = "kBlack")

DoubleMuonEmbeddedValidation = DoubleMuonSelectedValidation.clone(
	name = "DoubleMuonEmbeddedValidation",
	num_file = "/portal/ekpbms1/home/akhmet/2016-10-11_23-36_analysis/merged/embedded/embedded.root",
	label = "#mu#rightarrow#mu embedded",
	color = "kRed")

DoubleMuonMirroredValidation = DoubleMuonSelectedValidation.clone(
	name = "DoubleMuonMirroredValidation",
	num_file = "/portal/ekpbms1/home/akhmet/2016-10-11_23-46_analysis/merged/mirrored/mirrored.root",
	label = "#splitline{#mu#rightarrow#mu embedded}{w. mirroring}",
	color = "kBlue")

DoubleMuonFSRrecoMuons = DoubleMuonSelectedValidation.clone(
	name = "DoubleMuonFSRrecoMuons",
	num_file = "/portal/ekpbms1/home/akhmet/2016-10-11_23-42_analysis/merged/mureco/mureco.root",
	label = "#mu_{reco}",
	color = "kGray+2")

DoubleMuonFSRsimMuons = DoubleMuonSelectedValidation.clone(
	name = "DoubleMuonFSRsimMuons",
	num_file = "/portal/ekpbms1/home/akhmet/2016-10-11_23-44_analysis/merged/musim/musim.root",
	label = "#mu_{sim}",
	color = "kRed")

DoubleMuonFSRfsrMuons = DoubleMuonSelectedValidation.clone(
	name = "DoubleMuonFSRfsrMuons",
	num_file = "/portal/ekpbms1/home/akhmet/2016-10-11_23-43_analysis/merged/mufsr/mufsr.root",
	label = "#mu_{FSR}",
	color = "kBlue")	

# corresponding pt flow histograms


DoubleMuonSelectedPtFlowHistograms = pltcl.single_plotline(
	name = "DoubleMuonSelectedPtFlowHistograms",
	num_file = "/portal/ekpbms2/home/jbechtel/inputfiles_embeddingplots/ptflow_photon_finebinning_10GeV/selected.root",
	num_folder = "zmumu_selection_for_embedding",
	den_folder = "zmumu_selection_for_embedding",
	num_tree = "",
	label = "data ",
	scale_factor = 1./2450930.,
	color = "kBlack")

DoubleMuonEmbeddedPtFlowHistograms = DoubleMuonSelectedPtFlowHistograms.clone(
	name = "DoubleMuonEmbeddedPtFlowHistograms",
	num_file = "/portal/ekpbms2/home/jbechtel/inputfiles_embeddingplots/ptflow_photon_finebinning_10GeV/embedded.root",
	label = "#mu#rightarrow#mu embedded",
	scale_factor = 1./2408535.,
	color = "kRed")

DoubleMuonMirroredPtFlowHistograms = DoubleMuonSelectedPtFlowHistograms.clone(
	name = "DoubleMuonMirroredPtFlowHistograms",
	num_file = "/portal/ekpbms2/home/jbechtel/inputfiles_embeddingplots/ptflow_photon_finebinning_10GeV/mirrored.root",
	label = "#splitline{#mu#rightarrow#mu embedded}{w. mirroring}",
	scale_factor = 1./2424583.,
	color = "kBlue")

DoubleMuonRandomPtFlowHistograms = DoubleMuonSelectedPtFlowHistograms.clone(
	name = "DoubleMuonMirroredPtFlowHistograms",
	num_file = "/portal/ekpbms2/home/jbechtel/inputfiles_embeddingplots/ptflow_photon_finebinning_10GeV/random.root",
	label = "random direction",
	color = "kGray+2")


DoubleMuonSelectedPtFlowDistribution = pltcl.single_plotline(
	name = "DoubleMuonSelectedPtFlowDistribution",
	num_file = "/portal/ekpbms2/home/jbechtel/inputfiles_embeddingplots/ptflow_histogram_photon_firstbin_10GeV/selected.root",
	num_folder = "zmumu_selection_for_embedding",
	den_folder = "zmumu_selection_for_embedding",
	num_tree = "",
	label = "data ",
	scale_factor = 1.,
	color = "kBlack")

DoubleMuonEmbeddedPtFlowDistribution = DoubleMuonSelectedPtFlowDistribution.clone(
	name = "DoubleMuonEmbeddedPtFlowDistribution",
	num_file = "/portal/ekpbms2/home/jbechtel/inputfiles_embeddingplots/ptflow_histogram_photon_firstbin_10GeV/embedded.root",
	label = "#mu#rightarrow#mu embedded",
	scale_factor = 1.,
	color = "kRed")

DoubleMuonMirroredPtFlowDistribution = DoubleMuonSelectedPtFlowDistribution.clone(
	name = "DoubleMuonMirroredPtFlowDistribution",
	num_file = "/portal/ekpbms2/home/jbechtel/inputfiles_embeddingplots/ptflow_histogram_photon_firstbin_10GeV/mirrored.root",
	label = "#splitline{#mu#rightarrow#mu embedded}{w. mirroring}",
	scale_factor = 1.,
	color = "kBlue")

DoubleMuonRandomPtFlowDistribution = DoubleMuonSelectedPtFlowDistribution.clone(
	name = "DoubleMuonMirroredPtFlowDistribution",
	num_file = "/portal/ekpbms2/home/jbechtel/inputfiles_embeddingplots/ptflow_histogram_photon_firstbin_10GeV/random.root", 
	label = "random direction",
	scale_factor = 1.,
	color = "kGray+2")

DoubleMuonSelectedPtFlowDistribution5GeV = pltcl.single_plotline(
	name = "DoubleMuonSelectedPtFlowDistribution",
	num_file = "/portal/ekpbms2/home/jbechtel/inputfiles_embeddingplots/ptflow_histogram_photon_firstbin_5GeV/selected.root",
	num_folder = "zmumu_selection_for_embedding",
	den_folder = "zmumu_selection_for_embedding",
	num_tree = "",
	label = "data ",
	scale_factor = 1.,
	color = "kBlack")

DoubleMuonEmbeddedPtFlowDistribution5GeV = DoubleMuonSelectedPtFlowDistribution5GeV.clone(
	name = "DoubleMuonEmbeddedPtFlowDistribution",
	num_file = "/portal/ekpbms2/home/jbechtel/inputfiles_embeddingplots/ptflow_histogram_photon_firstbin_5GeV/embedded.root",
	label = "#mu#rightarrow#mu embedded",
	scale_factor = 1.,
	color = "kRed")

DoubleMuonMirroredPtFlowDistribution5GeV = DoubleMuonSelectedPtFlowDistribution5GeV.clone(
	name = "DoubleMuonMirroredPtFlowDistribution",
	num_file = "/portal/ekpbms2/home/jbechtel/inputfiles_embeddingplots/ptflow_histogram_photon_firstbin_5GeV/mirrored.root",
	label = "#splitline{#mu#rightarrow#mu embedded}{w. mirroring}",
	scale_factor = 1.,
	color = "kBlue")

DoubleMuonRandomPtFlowDistribution5GeV = DoubleMuonSelectedPtFlowDistribution5GeV.clone(
	name = "DoubleMuonMirroredPtFlowDistribution",
	num_file = "/portal/ekpbms2/home/jbechtel/inputfiles_embeddingplots/ptflow_histogram_photon_firstbin_5GeV/random.root", 
	label = "random direction",
	scale_factor = 1.,
	color = "kGray+2")
	
	
DoubleMuonSelectedPtFlowDistributionMid = pltcl.single_plotline(
	name = "DoubleMuonSelectedPtFlowDistribution",
	num_file = "/portal/ekpbms2/home/jbechtel/inputfiles_embeddingplots/ptflow_histogram_photon_midbin_10GeV/selected.root",
	num_folder = "zmumu_selection_for_embedding",
	den_folder = "zmumu_selection_for_embedding",
	num_tree = "",
	label = "data ",
	scale_factor = 1.,
	color = "kBlack")

DoubleMuonEmbeddedPtFlowDistributionMid = DoubleMuonSelectedPtFlowDistribution.clone(
	name = "DoubleMuonEmbeddedPtFlowDistribution",
	num_file = "/portal/ekpbms2/home/jbechtel/inputfiles_embeddingplots/ptflow_histogram_photon_midbin_10GeV/embedded.root",
	label = "#mu#rightarrow#mu embedded",
	scale_factor = 1.,
	color = "kRed")

DoubleMuonMirroredPtFlowDistributionMid = DoubleMuonSelectedPtFlowDistribution.clone(
	name = "DoubleMuonMirroredPtFlowDistribution",
	num_file = "/portal/ekpbms2/home/jbechtel/inputfiles_embeddingplots/ptflow_histogram_photon_midbin_10GeV/mirrored.root",
	label = "#splitline{#mu#rightarrow#mu embedded}{w. mirroring}",
	scale_factor = 1.,
	color = "kBlue")

DoubleMuonRandomPtFlowDistributionMid = DoubleMuonSelectedPtFlowDistribution.clone(
	name = "DoubleMuonMirroredPtFlowDistribution",
	num_file = "/portal/ekpbms2/home/jbechtel/inputfiles_embeddingplots/ptflow_histogram_photon_midbin_10GeV/random.root", 
	label = "random direction",
	scale_factor = 1.,
	color = "kGray+2")


## Tau Embedding Studies

# Acceptance Efficiency 2D

AccEfficiency2D = pltcl.single_plotline(
	name = "AccEfficiency2D",
	num_file = "AccEfficiency.root",
	num_folder = "histograms",
	den_folder = "histograms",
	num_tree = "",
	marker = "COLZ",
	color = None)

NEntries2DMuTau = pltcl.single_plotline(
	name = "NEntries2DMuTau",
	num_file = "MuTauEmbedding.root",
	num_folder = "acc_eff",
	den_folder = "acc_eff",
	num_tree = "",
	scale_factor = 0.001,
	marker = "COLZ",
	color = None)

NEntries2DElTau = NEntries2DMuTau.clone(
	name = "NEntries2DElTau",
	num_file = "ElTauEmbedding.root")

NEntries2DTauTau = NEntries2DMuTau.clone(
	name = "NEntries2DTauTau",
	num_file = "TauTauEmbedding.root")

NEntries2DElMu = NEntries2DMuTau.clone(
	name = "NEntries2DElMu",
	num_file = "ElMuEmbedding.root")


# Acceptance Efficiency distributions

AccEfficiencyMuTauFile = pltcl.single_plotline(
	name = "AccEfficiencyMuTauFile",
	num_file = "MuTauEmbedding.root",
	num_folder = "acc_eff",
	den_folder = "acc_eff",
	num_tree = "ntuple",
	color = "kBlack")

AccEfficiencyElTauFile = AccEfficiencyMuTauFile.clone(
	name = "AccEfficiencyElTauFile",
	num_file = "ElTauEmbedding.root")

AccEfficiencyTauTauFile = AccEfficiencyMuTauFile.clone(
	name = "AccEfficiencyTauTauFile",
	num_file = "TauTauEmbedding.root")

AccEfficiencyElMuFile = AccEfficiencyMuTauFile.clone(
	name = "AccEfficiencyElMuFile",
	num_file = "ElMuEmbedding.root")

# visible Mass comparison

# TTbar files
TTFileMuTauFile = pltcl.single_plotline(
	name = "TTFileMuTauFile",
	scale_factor = 831.76/77229341.*12891.,
	num_file ="/portal/ekpbms1/home/jbechtel/plotting/2017-03-10_01-34_analysis/merged/TT_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8/TT_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",	#'/storage/a/akhmet/htautau/artus/2017-02-09_00-10_analysis/merged/DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1/DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root',	
	num_folder = "mt_jecUncNom_tauEsNom",
	den_folder = "mt_jecUncNom_tauEsNom",
	num_tree = "ntuple",
	label = "t#bar{t} simulation",
	color = "kMagenta-1",
	marker = "PE")
TTFileTauTauFile = TTFileMuTauFile.clone(
	name = "TTFileMuTauFile",
	num_folder = "tt_jecUncNom_tauEsNom",
	den_folder = "tt_jecUncNom_tauEsNom")
# DYJets files
DYFileMuTauFile = pltcl.single_plotline(
	name = "DYFileMuTauFile",
	#scale_factor = 1./5.234,
	num_file ="/home/jbechtel/plotting/dySmeared/dySmeared.root",	#'/storage/a/akhmet/htautau/artus/2017-02-09_00-10_analysis/merged/DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1/DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root',
	#~ num_folder = "mt_jecUncNom_tauEsNom",
	#~ den_folder = "mt_jecUncNom_tauEsNom",	
	num_folder = "mt_nominal",
	den_folder = "mt_nominal",
	num_tree = "ntuple",
	label = "Z#rightarrow#tau#tau simulation",
	color = "kRed",
	marker = "PE")

DYFileMuTauSmeared = DYFileMuTauFile.clone(
	name = "DYFileMuTauSmeared",
	#scale_factor = 1./1.7122,
	num_folder = "mt_ZDecayProductsSmeared",
	den_folder = "mt_ZDecayProductsSmeared",
	color = "kMagenta",
	label = "Z#rightarrow#tau#tau SMEARED",
	marker = "LINE"
)
DYFileElTauFile = DYFileMuTauFile.clone(
	name = "DYFileElTauFile",
	#scale_factor = 1./1.7122,
	num_folder = "et_nominal",
	den_folder = "et_nominal"
)

DYFileTauTauFile = DYFileMuTauFile.clone(
	name = "DYFileTauTauFile",
	#scale_factor = 1./0.273551,
	num_folder = "tt_jecUncNom_tauEsNom",
	den_folder = "tt_jecUncNom_tauEsNom"
)

DYFileElMuFile = DYFileMuTauFile.clone(
	name = "DYFileElMuFile",
	#scale_factor = 1./0.887674,
	num_folder = "em_jecUncNom",
	den_folder = "em_jecUncNom"
)
# DYISOJets files ISO
DYISOFileMuTauFile = pltcl.single_plotline(
	name = "DYFileMuTauFile",
	#scale_factor = 1./5.234,
	num_file = "/home/jbechtel/MVAcheck/DYToLLMCRunIISummer16DR80_AllFinalState_imputFlatPU28to62HcalNZSRAWAODSIM_13TeV_USER_unspecified/DYToLLMCRunIISummer16DR80_AllFinalState_imputFlatPU28to62HcalNZSRAWAODSIM_13TeV_USER_unspecified.root",
	num_folder = "mt_jecUncNom_tauEsNom",
	den_folder = "mt_jecUncNom_tauEsNom",
	num_tree = "ntuple",
	label = "Z#rightarrow#tau#tau simulation",
	color = "kRed",
	marker = "PE")

DYISOFileElTauFile = DYFileMuTauFile.clone(
	name = "DYFileElTauFile",
	#scale_factor = 1./1.7122,
	num_folder = "et_jecUncNom_tauEsNom",
	den_folder = "et_jecUncNom_tauEsNom"
)

DYISOFileTauTauFile = DYFileMuTauFile.clone(
	name = "DYFileTauTauFile",
	#scale_factor = 1./0.273551,
	num_folder = "tt_jecUncNom_tauEsNom",
	den_folder = "tt_jecUncNom_tauEsNom"
)

DYISOFileElMuFile = DYFileMuTauFile.clone(
	name = "DYFileElMuFile",
	#scale_factor = 1./0.887674,
	num_folder = "em_jecUncNom",
	den_folder = "em_jecUncNom"
)

# DiBoson files
VVFileMuTauFile = pltcl.single_plotline(
	name = "VVFileMuTauFile",
	#scale_factor = 1./5.234,
	num_file = "/home/jbechtel/MVAcheck/VVTo2L2Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8/VVTo2L2Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root",
	num_folder = "mt_jecUncNom_tauEsNom",
	den_folder = "mt_jecUncNom_tauEsNom",
	num_tree = "ntuple",
	label = "VV #rightarrow ll simulation",
	color = "kGreen",
	marker = "PE")

VVFileElTauFile = VVFileMuTauFile.clone(
	name = "VVFileElTauFile",
	#scale_factor = 1./1.7122,
	num_folder = "et_jecUncNom_tauEsNom",
	den_folder = "et_jecUncNom_tauEsNom"
)

VVFileTauTauFile = VVFileMuTauFile.clone(
	name = "VVFileTauTauFile",
	#scale_factor = 1./0.273551,
	num_folder = "tt_jecUncNom_tauEsNom",
	den_folder = "tt_jecUncNom_tauEsNom"
)

VVFileElMuFile = VVFileMuTauFile.clone(
	name = "VVFileElMuFile",
	#scale_factor = 1./0.887674,
	num_folder = "em_jecUncNom",
	den_folder = "em_jecUncNom"
)


# HToTauTau samples

HToTauTauMuTauFile = pltcl.single_plotline(
	name = "HToTauTauMuTauFile",
	scale_factor = 1./0.767714,
	num_file = "/portal/ekpbms1/home/akhmet/htautau_signal/*HToTauTauM125*.root",
	num_folder = "mt",
	den_folder = "mt",
	num_tree = "ntuple",
	label = "H(125)",
	color = "kBlack")

HToTauTauElTauFile = HToTauTauMuTauFile.clone(
	name = "HToTauTauElTauFile",
	scale_factor = 1./0.356839,
	num_folder = "et",
	den_folder = "et"
)

HToTauTauTauTauFile = HToTauTauMuTauFile.clone(
	name = "HToTauTauTauTauFile",
	scale_factor = 1./0.25,
	num_folder = "tt",
	den_folder = "tt"
)

HToTauTauElMuFile = HToTauTauMuTauFile.clone(
	name = "HToTauTauElMuFile",
	scale_factor = 1./0.164191,
	num_folder = "em",
	den_folder = "em"
)

#Embedding files for MuTau

EmbeddingMuTauFileNominal = DYFileMuTauFile.clone(
	name = "EmbeddingMuTauFileNominal",
	scale_factor = 1.04277308792,
	num_file = '/portal/ekpbms1/home/jbechtel/plotting/EmbeddingMETtest/EmbeddingMuTau.root',
	#num_file = "/home/jbechtel/plotting/0226/EmbeddingMCRunIISummer16DR80_MuTauFinalState_imputFlatPU28to62HcalNZSRAWAODSIM_13TeV_USER_pythia8/EmbeddingMCRunIISummer16DR80_MuTauFinalState_imputFlatPU28to62HcalNZSRAWAODSIM_13TeV_USER_pythia8.root",
	label = "#mu#rightarrow#tau embedded",
	color = "kBlue"
)

EmbeddingMuTauFileUp = EmbeddingMuTauFileNominal.clone(
	name = "EmbeddingMuTauFileUp",
	num_folder = "mt_jecUncNom_tauEsUp",
	den_folder = "mt_jecUncNom_tauEsUp",
	label = "w. #pm3% #tau_{h}-ES shifts",
	color = "kCyan+2",
	marker = "HISTO"
)

EmbeddingMuTauFileDown = EmbeddingMuTauFileNominal.clone(
	name = "EmbeddingMuTauFileDown",
	num_folder = "mt_jecUncNom_tauEsDown",
	den_folder = "mt_jecUncNom_tauEsDown",
	label = "",
	color = "kCyan+2",
	marker = "HISTO"
)


EmbeddingMuTauFileNominalMirrored = DYFileMuTauFile.clone(
	name = "EmbeddingMuTauFileNominalMirrored",
	#scale_factor = 1.62724193802,
	num_file = '/portal/ekpbms1/home/jbechtel/plotting/mirrored/RUNC/Embedding2016C_MuTauFinalState_imputSep16DoubleMumirrorminiAODv2_13TeV_USER/Embedding2016C_MuTauFinalState_imputSep16DoubleMumirrorminiAODv2_13TeV_USER.root',
	#num_file = "/home/jbechtel/plotting/0226/EmbeddingMCRunIISummer16DR80_MuTauFinalState_imputFlatPU28to62HcalNZSRAWAODSIM_13TeV_USER_pythia8/EmbeddingMCRunIISummer16DR80_MuTauFinalState_imputFlatPU28to62HcalNZSRAWAODSIM_13TeV_USER_pythia8.root",
	label = "#mu#rightarrow#tau emb mirrored",
	color = "kGreen"
)

EmbeddingMuTauFileUpMirrored = EmbeddingMuTauFileNominal.clone(
	name = "EmbeddingMuTauFileUpMirrored",
	num_folder = "mt_jecUncNom_tauEsUp",
	den_folder = "mt_jecUncNom_tauEsUp",
	label = "w. #pm3% #tau_{h}-ES shifts",
	color = "kCyan+2",
	marker = "HISTO"
)

EmbeddingMuTauFileDownMirrored = EmbeddingMuTauFileNominal.clone(
	name = "EmbeddingMuTauFileDownMirrored",
	num_folder = "mt_jecUncNom_tauEsDown",
	den_folder = "mt_jecUncNom_tauEsDown",
	label = "",
	color = "kCyan+2",
	marker = "HISTO"
)

#Embedding files for ElTau

EmbeddingElTauFileNominal = DYFileElTauFile.clone(
	name = "EmbeddingElTauFileNominal",
	scale_factor=1.00421186517,
	num_file ="/home/jbechtel/plotting/Jun17_EmbeddingFiles/EmbeddingElTau.root",	#'/storage/a/akhmet/htautau/artus/2017-02-09_00-10_analysis/merged/Embedding2016B_ElTauFinalState_imputSep16DoubleMumirrorminiAODv1_13TeV_USER/Embedding2016B_ElTauFinalState_imputSep16DoubleMumirrorminiAODv1_13TeV_USER.root',
	#num_file = "/home/jbechtel/plotting/output.root",
	label = "#mu#rightarrow#tau embedded",
	color = "kBlue"
)

EmbeddingElTauFileUp = EmbeddingElTauFileNominal.clone(
	name = "EmbeddingElTauFileUp",
	num_folder = "et_jecUncNom_tauEsUp",
	den_folder = "et_jecUncNom_tauEsUp",
	label = "w. #pm3% #tau_{h}-ES shifts",
	color = "kCyan+2"
)

EmbeddingElTauFileDown = EmbeddingElTauFileNominal.clone(
	name = "EmbeddingElTauFileDown",
	num_folder = "et_jecUncNom_tauEsDown",
	den_folder = "et_jecUncNom_tauEsDown",
	label = "",
	color = "kCyan+2"
)

#Embedding files for TauTau

EmbeddingTauTauFileNominal = DYFileTauTauFile.clone(
	scale_factor = 1./0.33,
	name = "EmbeddingTauTauFileNominal",
	num_file = "/home/jbechtel/plotting/tautau_controlplots/EmbeddingBCD.root",
	label = "#mu#rightarrow#tau embedded",
	color = "kBlue"
)

EmbeddingTauTauFileUp = EmbeddingTauTauFileNominal.clone(
	name = "EmbeddingTauTauFileUp",
	num_folder = "tt_jecUncNom_tauEsUp",
	den_folder = "tt_jecUncNom_tauEsUp",
	label = "w. #pm3% #tau_{h}-ES shifts",
	color = "kCyan+2"
)

EmbeddingTauTauFileDown = EmbeddingTauTauFileNominal.clone(
	name = "EmbeddingTauTauFileDown",
	num_folder = "tt_jecUncNom_tauEsDown",
	den_folder = "tt_jecUncNom_tauEsDown",
	label = "",
	color = "kCyan+2"
)

#Embedding files for ElMu

EmbeddingElMuFileNominal = DYFileElMuFile.clone(
	name = "EmbeddingElMuFileNominal",
	num_file = "/portal/ekpbms1/home/akhmet/elmuembedding/*.root",
	num_folder = "em_eleEsNom",
	den_folder = "em_eleEsNom",
	label = "#mu#rightarrow#tau embedded",
	color = "kBlue"
)

EmbeddingElMuFileUp = EmbeddingElMuFileNominal.clone(
	name = "EmbeddingElMuFileUp",
	num_folder = "em_eleEsUp",
	den_folder = "em_eleEsUp",
	label = "w. #pm2% e-ES shifts",
	color = "kCyan+2"
)

EmbeddingElMuFileDown = EmbeddingElMuFileNominal.clone(
	name = "EmbeddingElMuFileDown",
	num_folder = "em_eleEsDown",
	den_folder = "em_eleEsDown",
	label = "",
	color = "kCyan+2"
)

#EmbeddingISO files for MuTau including Iso_2 MVA Variables

EmbeddingISOMuTauFileNominal = DYFileMuTauFile.clone(
	#scale_factor = 1./4.32414,
	name = "EmbeddingMuTauFileNominal",
	num_file = "/home/jbechtel/MVAcheck/EmbeddingMCRunIISummer16DR80_MuTauFinalState_imputFlatPU28to62HcalNZSRAWAODSIM_13TeV_USER_pythia8/EmbeddingMCRunIISummer16DR80_MuTauFinalState_imputFlatPU28to62HcalNZSRAWAODSIM_13TeV_USER_pythia8.root",
	label = "#mu#rightarrow#tau embedded",
	color = "kBlue"
)

EmbeddingISOMuTauFileUp = EmbeddingMuTauFileNominal.clone(
	name = "EmbeddingMuTauFileUp",
	num_folder = "mt_jecUncNom_tauEsUp",
	den_folder = "mt_jecUncNom_tauEsUp",
	label = "w. #pm3% #tau_{h}-ES shifts",
	color = "kCyan+2"
)

EmbeddingISOMuTauFileDown = EmbeddingMuTauFileNominal.clone(
	name = "EmbeddingMuTauFileDown",
	num_folder = "mt_jecUncNom_tauEsDown",
	den_folder = "mt_jecUncNom_tauEsDown",
	label = "",
	color = "kCyan+2"
)


#EmbeddingISO files for ElTau including Iso_2 MVA Variables

EmbeddingISOElTauFileNominal = DYFileElTauFile.clone(
	name = "EmbeddingISOElTauFileNominal",
	num_file = "/storage/a/jbechtel/test/merged/merged/EmbeddingISO2016?_ElTau*/*.root",
	label = "#mu#rightarrow#tau embedded",
	color = "kBlue"
)

EmbeddingISOElTauFileUp = EmbeddingISOElTauFileNominal.clone(
	name = "EmbeddingISOElTauFileUp",
	num_folder = "et_jecUncNom_tauEsUp",
	den_folder = "et_jecUncNom_tauEsUp",
	label = "w. #pm3% #tau_{h}-ES shifts",
	color = "kCyan+2"
)

EmbeddingISOElTauFileDown = EmbeddingISOElTauFileNominal.clone(
	name = "EmbeddingISOElTauFileDown",
	num_folder = "et_jecUncNom_tauEsDown",
	den_folder = "et_jecUncNom_tauEsDown",
	label = "",
	color = "kCyan+2"
)

#EmbeddingISO files for TauTau including Iso_2 MVA Variables

EmbeddingISOTauTauFileNominal = DYFileTauTauFile.clone(
	scale_factor = 1./0.220103,
	name = "EmbeddingISOTauTauFileNominal",
	num_file = "/storage/a/jbechtel/janek/EmbeddingISO2016?_TauTau*/*.root",
	label = "#mu#rightarrow#tau embedded",
	color = "kBlue"
)

EmbeddingISOTauTauFileUp = EmbeddingISOTauTauFileNominal.clone(
	name = "EmbeddingISOTauTauFileUp",
	num_folder = "tt_jecUncNom_tauEsUp",
	den_folder = "tt_jecUncNom_tauEsUp",
	label = "w. #pm3% #tau_{h}-ES shifts",
	color = "kCyan+2"
)

EmbeddingISOTauTauFileDown = EmbeddingISOTauTauFileNominal.clone(
	name = "EmbeddingISOTauTauFileDown",
	num_folder = "tt_jecUncNom_tauEsDown",
	den_folder = "tt_jecUncNom_tauEsDown",
	label = "",
	color = "kCyan+2"
)

#EmbeddingISO files for ElMu including Iso_2 MVA Variables

EmbeddingISOElMuFileNominal = DYFileElMuFile.clone(
	scale_factor = 1./1.58934,
	name = "EmbeddingISOElMuFileNominal",
	num_file = "/portal/ekpbms1/home/akhmet/elmuEmbeddingISO/*.root",
	num_folder = "em_eleEsNom",
	den_folder = "em_eleEsNom",
	label = "#mu#rightarrow#tau embedded",
	color = "kBlue"
)

EmbeddingISOElMuFileUp = EmbeddingISOElMuFileNominal.clone(
	name = "EmbeddingISOElMuFileUp",
	num_folder = "em_eleEsUp",
	den_folder = "em_eleEsUp",
	label = "w. #pm2% e-ES shifts",
	color = "kCyan+2"
)

EmbeddingISOElMuFileDown = EmbeddingISOElMuFileNominal.clone(
	name = "EmbeddingISOElMuFileDown",
	num_folder = "em_eleEsDown",
	den_folder = "em_eleEsDown",
	label = "",
	color = "kCyan+2"
)


## Decay channel migration

#MuTau -> X
EmbeddingMuTauIntegralMuTauFile = pltcl.single_plotline(
	name = "EmbeddingMuTauIntegralMuTauFile",
	num_file = "/storage/a/jbechtel/test/merged/merged/Embedding2016?_MuTau*/*.root",
	num_folder = "mt_jecUncNom_tauEsNom",
	den_folder = "mt_jecUncNom_tauEsNom",
	num_tree = "ntuple")
	
EmbeddingMuTauIntegralElTauFile = EmbeddingMuTauIntegralMuTauFile.clone(
	name = "EmbeddingMuTauIntegralElTauFile",
	num_folder = "et_jecUncNom_tauEsNom",
	den_folder = "et_jecUncNom_tauEsNom")

EmbeddingMuTauIntegralTauTauFile = EmbeddingMuTauIntegralMuTauFile.clone(
	name = "EmbeddingMuTauIntegralTauTauFile",
	num_folder = "tt_jecUncNom_tauEsNom",
	den_folder = "tt_jecUncNom_tauEsNom")

EmbeddingMuTauIntegralElMuFile = EmbeddingMuTauIntegralMuTauFile.clone(
	name = "EmbeddingMuTauIntegralElMuFile",
	num_folder = "em_jecUncNom",
	den_folder = "em_jecUncNom")

#ElTau -> X

EmbeddingElTauIntegralElTauFile = pltcl.single_plotline(
	name = "EmbeddingElTauIntegralElTauFile",
	num_file = "/storage/a/jbechtel/test/merged/merged/Embedding2016?_ElTau*/*.root",
	num_folder = "et_jecUncNom_tauEsNom",
	den_folder = "et_jecUncNom_tauEsNom",
	num_tree = "ntuple")

EmbeddingElTauIntegralElMuFile = EmbeddingElTauIntegralElTauFile.clone(
	name = "EmbeddingElTauIntegralElMuFile",
	num_folder = "em_jecUncNom",
	den_folder = "em_jecUncNom")

EmbeddingElTauIntegralMuTauFile = EmbeddingElTauIntegralElTauFile.clone(
	name = "EmbeddingElTauIntegralMuTauFile",
	num_folder = "mt_jecUncNom_tauEsNom",
	den_folder = "mt_jecUncNom_tauEsNom")

EmbeddingElTauIntegralTauTauFile = EmbeddingElTauIntegralElTauFile.clone(
	name = "EmbeddingElTauIntegralTauTauFile",
	num_folder = "tt_jecUncNom_tauEsNom",
	den_folder = "tt_jecUncNom_tauEsNom")
	

#TauTau -> X

EmbeddingTauTauIntegralTauTauFile = pltcl.single_plotline(
	name = "EmbeddingTauTauIntegralTauTauFile",
	num_file = "/storage/a/jbechtel/test/merged/merged/Embedding2016?_TauTau*/*.root",
	num_folder = "tt_jecUncNom_tauEsNom",
	den_folder = "tt_jecUncNom_tauEsNom",
	num_tree = "ntuple")

EmbeddingTauTauIntegralMuTauFile = EmbeddingTauTauIntegralTauTauFile.clone(
	name = "EmbeddingTauTauIntegralMuTauFile",
	num_folder = "mt_jecUncNom_tauEsNom",
	den_folder = "mt_jecUncNom_tauEsNom")

EmbeddingTauTauIntegralElTauFile = EmbeddingTauTauIntegralTauTauFile.clone(
	name = "EmbeddingTauTauIntegralElTauFile",
	num_folder = "et_jecUncNom_tauEsNom",
	den_folder = "et_jecUncNom_tauEsNom")

EmbeddingTauTauIntegralElMuFile = EmbeddingTauTauIntegralTauTauFile.clone(
	name = "EmbeddingTauTauIntegralElMuFile",
	num_folder = "em_jecUncNom",
	den_folder = "em_jecUncNom")

#ElMu -> X

EmbeddingElMuIntegralElMuFile = pltcl.single_plotline(
	name = "EmbeddingElMuIntegralElMuFile",
	num_file = "/storage/a/jbechtel/test/merged/merged/Embedding2016?_ElMu*/*.root",
	num_folder = "em_jecUncNom",
	den_folder = "em_jecUncNom",
	num_tree = "ntuple")

EmbeddingElMuIntegralMuTauFile = EmbeddingElMuIntegralElMuFile.clone(
	name = "EmbeddingElMuIntegralMuTauFile",
	num_folder = "mt_jecUncNom_tauEsNom",
	den_folder = "mt_jecUncNom_tauEsNom")

EmbeddingElMuIntegralElTauFile = EmbeddingElMuIntegralElMuFile.clone(
	name = "EmbeddingElMuIntegralElTauFile",
	num_folder = "et_jecUncNom_tauEsNom",
	den_folder = "et_jecUncNom_tauEsNom")

EmbeddingElMuIntegralTauTauFile = EmbeddingElMuIntegralElTauFile.clone(
	name = "EmbeddingElMuIntegralTauTauFile",
	num_folder = "tt_jecUncNom_tauEsNom",
	den_folder = "tt_jecUncNom_tauEsNom")
