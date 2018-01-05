#!/bin/bash
echo "Test Artus:"
HiggsToTauTauAnalysis.py @${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusWrapperConfigs/Run2CPStudies_Nominal.cfg -i ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/Samples/XROOTD_sample_GluGluHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_recent.txt -f 1 -e 100
echo "Finished testing Artus."
echo "Begin producing control plots."
makePlots_controlPlots.py -i /net/scratch_cms3b/tmuller/artus//2017-12-08_23-24_Run2CPStudies_Nominal_Summer16_plusHToTauTauM110-140/merged/ -c tt -x "jdphi" -s ztt zll ttj vv wj qcd qqh gghjhusm gghjhups --categories Vbf3D_CP -a " --filename CP_initialstate_controlplot"
echo "Begin evaluating datacards script."
makePlots_datacardsCPInitialState.py -i /net/scratch_cms3b/tmuller/artus/2017-12-08_23-24_Run2CPStudies_Nominal_Summer16_plusHToTauTauM110-140/merged/ -n 3 -c tt --categories Vbf3D_CP -x "jdphi" --no-shape-uncs --use-asimov-dataset --use-shape-only --cp-study ggh -o "plots/htt_datacards/testing_CP_initialstate_datacardsscript/" --steps inputs likelihoodScan prefitpostfitplots
echo "Done."
