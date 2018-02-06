#!/bin/bash
set -e # exit on errors

if [ "x$1" = "x" ]; then
    MODE="artus"
else
    MODE=$1
fi

if [ "$MODE" = "artus" -o "$MODE" = "both" ]; then
    export SCRAM_ARCH=slc6_amd64_gcc630
    export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
    source $VO_CMS_SW_DIR/cmsset_default.sh

    # set up CMSSW release area
    scramv1 project CMSSW CMSSW_9_2_4; pushd CMSSW_9_2_4/src 
    eval `scramv1 runtime -sh`

    # JEC
    git cms-addpkg CondFormats/JetMETObjects

    # From Kappa, only the DataFormats are needed
    # Mind that for certain skims, you need exactly the Kappa git tag that has been used for the production
    git clone https://github.com/KappaAnalysis/Kappa.git
    pushd Kappa
    echo docs/ >> .git/info/sparse-checkout
    echo DataFormats/ >> .git/info/sparse-checkout
    echo Skimming/ >> .git/info/sparse-checkout
    git config core.sparsecheckout true
    git read-tree -mu HEAD
    popd

    git clone https://github.com/KappaAnalysis/KappaTools.git 

    git clone https://github.com/artus-analysis/Artus.git
    git clone https://github.com/artus-analysis/Artus.wiki.git Artus/Core/doc/wiki

    # checkout KITHiggsToTauTau CMSSW analysis package
    git clone https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau HiggsAnalysis/KITHiggsToTauTau
    git clone https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau.wiki.git HiggsAnalysis/KITHiggsToTauTau/doc/wiki

    # Svfit and HHKinFit
    git clone https://github.com/CMSAachen3B/SVfit_standalone.git TauAnalysis/SVfitStandalone -b HIG-16-006
    git clone https://github.com/artus-analysis/HHKinFit2.git -b artus

    # Jet2Tau Fakes
    git clone https://github.com/CMS-HTT/Jet2TauFakes.git HTTutilities/Jet2TauFakes

    # EmuQCD Method
    git clone https://github.com/CMS-HTT/QCDModelingEMu.git HTT-utilities/QCDModelingEMu

    # Fit Package for tau polarisation
    git clone https://github.com/CMSAachen3B/SimpleFits.git -b artus_master

    sed '/CombineHarvester/d' ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/BuildFile.xml -i

    # needed for error propagation e.g. in the background estimations
    git clone https://github.com/lebigot/uncertainties.git -b 2.4.6.1 HiggsAnalysis/KITHiggsToTauTau/python/uncertainties

    sed 's/\-cms2//g' ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/tauspinner.xml -i

    # Grid-Control
    git clone https://github.com/grid-control/grid-control.git -b r1941

    # source ini script, needs to be done in every new shell
    source HiggsAnalysis/KITHiggsToTauTau/scripts/ini_KITHiggsToTauTauAnalysis.sh

    # compile everything
    scram b -j `grep -c ^processor /proc/cpuinfo`
    popd
fi

if [ "$MODE" = "limit" -o "$MODE" = "both" ]; then
    export SCRAM_ARCH=slc6_amd64_gcc493
    export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
    source $VO_CMS_SW_DIR/cmsset_default.sh

    # set up CMSSW release area
    scramv1 project CMSSW CMSSW_7_4_7; pushd CMSSW_7_4_7/src 
    eval `scramv1 runtime -sh`

    git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
    git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
    scram b -j `grep -c ^processor /proc/cpuinfo`
    popd
fi
