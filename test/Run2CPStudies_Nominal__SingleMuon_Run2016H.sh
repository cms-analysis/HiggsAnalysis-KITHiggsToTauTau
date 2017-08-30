#!/bin/bash

HiggsToTauTauAnalysis.py @${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusWrapperConfigs/Run2CPStudies_Nominal.cfg -i ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/Samples/XROOTD_sample_SingleMuon_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD_recent.txt -f 1 -e 100
