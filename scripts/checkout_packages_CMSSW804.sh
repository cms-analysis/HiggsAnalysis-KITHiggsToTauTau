#!/bin/bash
set -e # exit on errors

export SCRAM_ARCH=slc6_amd64_gcc530
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh

# set up CMSSW release area
scramv1 project CMSSW CMSSW_8_0_4; cd CMSSW_8_0_4/src 
eval `scramv1 runtime -sh`

# JEC
git cms-addpkg CondFormats/JetMETObjects

# From Kappa, only the DataFormats are needed
# Mind that for certain skims, you need exactly the Kappa git tag that has been used for the production
git clone https://github.com/KappaAnalysis/Kappa.git -b CMSSW_7_6_X
cd Kappa
echo docs/ >> .git/info/sparse-checkout
echo DataFormats/ >> .git/info/sparse-checkout
echo Skimming/data/ >> .git/info/sparse-checkout
echo Skimming/python/ >> .git/info/sparse-checkout
git config core.sparsecheckout true
git read-tree -mu HEAD
cd $CMSSW_BASE/src
make -C Kappa/DataFormats/test/

git clone https://github.com/KappaAnalysis/KappaTools.git 

git clone https://github.com/artus-analysis/Artus.git
git clone https://github.com/artus-analysis/Artus.wiki.git Artus/Core/doc/wiki

# checkout KITHiggsToTauTau CMSSW analysis package
git clone https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau HiggsAnalysis/KITHiggsToTauTau
git clone https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau.wiki.git HiggsAnalysis/KITHiggsToTauTau/doc/wiki
#svn co https://ekptrac.physik.uni-karlsruhe.de/svn/KITHiggsToTauTau-auxiliaries/trunk HiggsAnalysis/KITHiggsToTauTau/auxiliaries

# Svfit and HHKinFit
git clone https://github.com/veelken/SVfit_standalone.git TauAnalysis/SVfitStandalone
cd TauAnalysis/SVfitStandalone
git checkout dd7cf43e3f930040959f7d700cef976307d7cec3 -b current
cd $CMSSW_BASE/src

# Jet2Tau Fakes
git clone https://github.com/CMS-HTT/Jet2TauFakes.git HTTutilities/Jet2TauFakes

# Fit Package for tau polarisation
git clone https://github.com/CMSAachen3B/SimpleFits.git -b artus_master

# checkout HHKinFit2 package - artus branch because of folder structure
git clone https://github.com/artus-analysis/HHKinFit2.git -b artus

# needed for plotting and statistical inference
#git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester # uncommented since not approved for ROOT6
#### --change to the recommendation of Combind Twiki 
##https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideHiggsAnalysisCombinedLimit#ROOT5_SLC6_release_CMSSW_7_1_X
##git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git -b slc6-root5.34.17 HiggsAnalysis/CombinedLimit

# git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit # does not compile in ROOT6
# cd HiggsAnalysis/CombinedLimit
#git fetch origin
#git checkout v5.0.3
#cd -
sed '/CombineHarvester/d' ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/BuildFile.xml -i

# needed for error propagation e.g. in the background estimations
git clone https://github.com/lebigot/uncertainties.git -b 2.4.6.1 HiggsAnalysis/KITHiggsToTauTau/python/uncertainties

sed 's/cms2/ikhhed3/g' ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/data/tauspinner.xml -i

# Grid-Control
git clone https://github.com/artus-analysis/grid-control.git

# source ini script, needs to be done in every new shell
source HiggsAnalysis/KITHiggsToTauTau/scripts/ini_KITHiggsToTauTauAnalysis.sh

# compile everything
scram b -j `grep -c ^processor /proc/cpuinfo`
cd HiggsAnalysis/KITHiggsToTauTau
cd -

