#!/bin/bash

# 8 TeV analysis
HiggsToTauTauAnalysis.py @${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusWrapperConfigs/SM_Htautau.cfg -i ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/Samples/DCAP_sample_DYJetsToLL_M_50_madgraph_8TeV_recent.txt -f 1 && \

# 13 TeV sync analysis
HiggsToTauTauAnalysis.py @${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusWrapperConfigs/Sync13TeV.cfg -i ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/Samples/DCAP_sample_SUSYGluGluToHToTauTauM160_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD_pythia8_recent.txt -f 1 && \

# 13 TeV run2 analysis
HiggsToTauTauAnalysis.py @${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusWrapperConfigs/Run2Analysis.cfg -i ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/Samples/DCAP_sample_SUSYGluGluToHToTauTauM160_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM_recent.txt -f 1

