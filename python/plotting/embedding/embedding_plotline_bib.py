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
	num_file = "selected.root",
	num_folder = "zmumu_selection_for_embedding",
	den_folder = "zmumu_selection_for_embedding",
	num_tree = "",
	label = "data ",
	scale_factor = 1.,
	color = "kBlack")

DoubleMuonEmbeddedPtFlowHistograms = DoubleMuonSelectedPtFlowHistograms.clone(
	name = "DoubleMuonEmbeddedPtFlowHistograms",
	#num_file = "/portal/ekpbms1/home/akhmet/2016-10-11_23-36_analysis/merged/embedded/embedded.root",
	num_file = "embedded.root",
	label = "#mu#rightarrow#mu embedded",
	#scale_factor = 1./2408535.,
	scale_factor = 1.,
	color = "kRed")

DoubleMuonMirroredPtFlowHistograms = DoubleMuonSelectedPtFlowHistograms.clone(
	name = "DoubleMuonMirroredPtFlowHistograms",
	num_file = "mirrored.root",
	label = "#splitline{#mu#rightarrow#mu embedded}{w. mirroring}",
	#scale_factor = 1./2424583.,
	scale_factor = 1.,
	color = "kBlue")

DoubleMuonRandomPtFlowHistograms = DoubleMuonSelectedPtFlowHistograms.clone(
	name = "DoubleMuonMirroredPtFlowHistograms",
	num_file = "random.root",
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

# DYJets files
DYFileMuTauFile = pltcl.single_plotline(
	name = "DYFileMuTauFile",
	scale_factor = 1./5.234,
	num_file = "/storage/a/jbechtel/test/merged/merged/DY*/*.root",
	num_folder = "mt_jecUncNom_tauEsNom",
	den_folder = "mt_jecUncNom_tauEsNom",
	num_tree = "ntuple",
	label = "Z#rightarrow#tau#tau simulation",
	color = "kRed")

DYFileElTauFile = DYFileMuTauFile.clone(
	name = "DYFileElTauFile",
	scale_factor = 1./1.7122,
	num_folder = "et_jecUncNom_tauEsNom",
	den_folder = "et_jecUncNom_tauEsNom"
)

DYFileTauTauFile = DYFileMuTauFile.clone(
	name = "DYFileTauTauFile",
	num_file = "/storage/a/jbechtel/janek/DY*/*.root",
	scale_factor = 1./0.273551,
	num_folder = "tt_jecUncNom_tauEsNom",
	den_folder = "tt_jecUncNom_tauEsNom"
)

DYFileElMuFile = DYFileMuTauFile.clone(
	name = "DYFileElMuFile",
	scale_factor = 1./0.887674,
	num_file = "/storage/a/jbechtel/janek/DY*/*.root",
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
	scale_factor = 1./4.32414,
	name = "EmbeddingMuTauFileNominal",
	num_file = "/storage/a/jbechtel/test/merged/merged/Embedding2016?_MuTau*/*.root",
	label = "#mu#rightarrow#tau embedded",
	color = "kBlue"
)

EmbeddingMuTauFileUp = EmbeddingMuTauFileNominal.clone(
	name = "EmbeddingMuTauFileUp",
	num_folder = "mt_jecUncNom_tauEsUp",
	den_folder = "mt_jecUncNom_tauEsUp",
	label = "w. #pm3% #tau_{h}-ES shifts",
	color = "kCyan+2"
)

EmbeddingMuTauFileDown = EmbeddingMuTauFileNominal.clone(
	name = "EmbeddingMuTauFileDown",
	num_folder = "mt_jecUncNom_tauEsDown",
	den_folder = "mt_jecUncNom_tauEsDown",
	label = "",
	color = "kCyan+2"
)


#Embedding files for ElTau

EmbeddingElTauFileNominal = DYFileElTauFile.clone(
	scale_factor = 1./1.90354,
	name = "EmbeddingElTauFileNominal",
	num_file = "/storage/a/jbechtel/test/merged/merged/Embedding2016?_ElTau*/*.root",
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
	scale_factor = 1./0.220103,
	name = "EmbeddingTauTauFileNominal",
	num_file = "/storage/a/jbechtel/janek/Embedding2016?_TauTau*/*.root",
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
	scale_factor = 1./1.58934,
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
