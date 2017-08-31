#!/bin/bash

HiggsToTauTauAnalysis.py @${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusWrapperConfigs/Run2Analysis_Nominal.cfg -i ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/Samples/XROOTD_sample_GluGluHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_recent.txt -f 1 -e 100
