#!/bin/sh
#set -e # exit on errors

export SCRAM_ARCH=slc6_amd64_gcc491
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh

# set up CMSSW release area
scramv1 project CMSSW CMSSW_7_4_7; cd CMSSW_7_4_7/src # slc6 # Combine requires this version
eval `scramv1 runtime -sh`

export BRANCH="master"
while getopts :b:g:e:n: option
do
	case "${option}"
	in
	b) export BRANCH=${OPTARG};;
	g) git config --global user.github ${OPTARG};;
	e) git config --global user.email ${OPTARG};;
	n) git config --global user.name "\"${OPTARG}\"";;
	esac
done

# JEC
git cms-addpkg CondFormats/JetMETObjects

# From Kappa, only the DataFormats are needed
# Mind that for certain skims, you need exactly the Kappa git tag that has been used for the production
git clone https://github.com/KappaAnalysis/Kappa.git
cd Kappa
echo docs/ >> .git/info/sparse-checkout
echo DataFormats/ >> .git/info/sparse-checkout
echo Skimming/ >> .git/info/sparse-checkout
git config core.sparsecheckout true
git read-tree -mu HEAD
cd ..

git clone https://github.com/artus-analysis/Artus.git

# checkout KITHiggsToTauTau CMSSW analysis package
git clone https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau HiggsAnalysis/KITHiggsToTauTau -b $BRANCH

# Di-tau system reconstruction
# git clone https://github.com/veelken/SVfit_standalone.git TauAnalysis/SVfitStandalone -b HIG-16-006
git clone https://github.com/CMSAachen3B/SVfit_standalone.git TauAnalysis/SVfitStandalone -b HIG-16-006
git clone https://github.com/TauPolSoftware/SimpleFits.git TauPolSoftware/SimpleFits

# polarisation
git clone https://github.com/TauPolSoftware/TauDecaysInterface.git TauPolSoftware/TauDecaysInterface

# MadGraph
git clone https://github.com/CMSAachen3B/MadGraphReweighting.git CMSAachen3B/MadGraphReweighting

# MELA/JHU
git clone https://github.com/cms-analysis/HiggsAnalysis-ZZMatrixElement.git ZZMatrixElement -b v2.1.1 # see mail from Heshy Roskes sent on 15.11.2017 20:32
cd ZZMatrixElement
./setup.sh -j `grep -c ^processor /proc/cpuinfo`
cd $CMSSW_BASE/src/

# Jet2Tau Fakes
git clone https://github.com/CMS-HTT/Jet2TauFakes.git HTTutilities/Jet2TauFakes
cd $CMSSW_BASE/src/HTTutilities/Jet2TauFakes
git checkout v0.2.1
cd $CMSSW_BASE/src/

# EmuQCD Method
git clone https://github.com/CMS-HTT/QCDModelingEMu.git HTT-utilities/QCDModelingEMu

# needed for plotting and statistical inference
git clone https://github.com/thomas-mueller/CombineHarvester.git CombineHarvester -b SM2016-dev
cd CombineHarvester/HTTSM2016
git clone https://gitlab.cern.ch/cms-htt/SM-PAS-2016.git shapes
cd -
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v6.3.1
cd -

# needed for error propagation e.g. in the background estimations
git clone https://github.com/lebigot/uncertainties.git -b 2.4.6.1 HiggsAnalysis/KITHiggsToTauTau/python/uncertainties

# Grid-Control
git clone https://github.com/grid-control/grid-control.git -b testing
cd grid-control
git reset --hard 3f93692
cd $CMSSW_BASE/src/

# source ini script, needs to be done in every new shell
source HiggsAnalysis/KITHiggsToTauTau/scripts/ini_KITHiggsToTauTauAnalysis.sh

# compile everything
scramv1 b -j `grep -c ^processor /proc/cpuinfo`

