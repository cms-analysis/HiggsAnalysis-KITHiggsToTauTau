#!/bin/bash

HiggsToTauTauAnalysis.py @${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusWrapperConfigs/Run2CPStudies_Nominal.cfg -i ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/Samples/XROOTD_sample_DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1_recent.txt -f 1 -e 100
