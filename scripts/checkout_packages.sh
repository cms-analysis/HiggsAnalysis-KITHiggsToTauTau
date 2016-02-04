#!/bin/bash
set -e # exit on errors

export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh

# set up CMSSW release area
cmsrel CMSSW_7_1_5; cd CMSSW_7_1_5/src # slc6 # Combine requires this version
cmsenv

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

git clone https://github.com/artus-analysis/Artus.git -b Kappa_2_1
git clone https://github.com/artus-analysis/Artus.wiki.git Artus/Core/doc/wiki

# checkout KITHiggsToTauTau CMSSW analysis package
git clone https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau HiggsAnalysis/KITHiggsToTauTau
git clone https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau.wiki.git HiggsAnalysis/KITHiggsToTauTau/doc/wiki
svn co https://ekptrac.physik.uni-karlsruhe.de/svn/KITHiggsToTauTau-auxiliaries/trunk HiggsAnalysis/KITHiggsToTauTau/auxiliaries
echo '<use   name="rootrflx"/>'>> TauAnalysis/SVfitStandalone/BuildFile.xml

# Svfit and HHKinFit
git clone https://github.com/veelken/SVfit_standalone.git TauAnalysis/SVfitStandalone
cd TauAnalysis/SVfitStandalone
git checkout dd7cf43e3f930040959f7d700cef976307d7cec3 -b current
cd $CMSSW_BASE/src
git clone https://github.com/thomas-mueller/HHKinFit2.git

# needed for plotting and statistical inference
git clone https://github.com/cms-analysis/HiggsAnalysis-HiggsToTauTau.git HiggsAnalysis/HiggsToTauTau
git clone https://github.com/roger-wolf/HiggsAnalysis-HiggsToTauTau-auxiliaries.git auxiliaries
git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git -b slc6-root5.34.17 HiggsAnalysis/CombinedLimit

# needed for error propagation e.g. in the background estimations
git clone https://github.com/lebigot/uncertainties.git -b 2.4.6.1 HiggsAnalysis/KITHiggsToTauTau/python/uncertainties

# install TauSpinner
git clone https://github.com/rfriese/TauSpinnerSetup
python TauSpinnerSetup/checkoutPackagesForTauSpinner.py --tauolaversion=1.1.5

# Grid-Control
svn co https://ekptrac.physik.uni-karlsruhe.de/svn/grid-control/trunk/grid-control -r 1501

# source ini script, needs to be done in every new shell
source HiggsAnalysis/KITHiggsToTauTau/scripts/ini_KITHiggsToTauTauAnalysis.sh

# compile everything
rm -r HiggsAnalysis/KITHiggsToTauTau/data/ArtusOutputs
scram b -j 4
cd HiggsAnalysis/KITHiggsToTauTau
git checkout -- data/ArtusOutputs
cd -

