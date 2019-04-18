#!/bin/sh
#set -e # exit on errors

ssh -vT git@github.com

echo -n "Enter the CMMSW release you want to use (747, 810 [default]) and press [ENTER] (747 is for SL6, 810 is for SL7): "
read cmssw_version

echo -n "Enter the CombineHarvester developer branch you want to checkout (master, SM2016-dev, SMCP2016-dev [default], classicsvfit) and press [ENTER] : "
read ch_branch

export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh

if [[ $cmssw_version = "747" ]]; then
	# set up CMSSW release area
	export SCRAM_ARCH=slc6_amd64_gcc491
	scramv1 project CMSSW CMSSW_7_4_7; cd CMSSW_7_4_7/src # slc6 # Combine requires this version
	eval `scramv1 runtime -sh`

	export BRANCH="CMSSW_747"
elif [[ $cmssw_version = "942" ]]; then
        export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
        source $VO_CMS_SW_DIR/cmsset_default.sh

        scramv1 project CMSSW CMSSW_9_4_2
        cd CMSSW_9_4_2/src
        eval `scramv1 runtime -sh`
else
        # set up CMSSW release area
        export SCRAM_ARCH=slc6_amd64_gcc530
        scramv1 project CMSSW CMSSW_8_1_0; cd CMSSW_8_1_0/src # slc6 # Combine requires this version
        eval `scramv1 runtime -sh`
	export BRANCH="master"
fi


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
git clone git@github.com:KappaAnalysis/Kappa.git -b dictchanges_CMSSW94X
cd Kappa
echo docs/ >> .git/info/sparse-checkout
echo DataFormats/ >> .git/info/sparse-checkout
echo Skimming/ >> .git/info/sparse-checkout
git config core.sparsecheckout true
git read-tree -mu HEAD
cd ..

git clone git@github.com:artus-analysis/Artus.git -b dictchanges_CMSSW94X

# checkout KITHiggsToTauTau CMSSW analysis package
git clone --recursive git@github.com:cms-analysis/HiggsAnalysis-KITHiggsToTauTau HiggsAnalysis/KITHiggsToTauTau -b dictchanges_CMSSW94

# Di-tau system reconstruction
git clone git@github.com:SVfit/ClassicSVfit.git TauAnalysis/ClassicSVfit -b release_2018Mar20
git clone git@github.com:SVfit/SVfitTF.git TauAnalysis/SVfitTF
git clone git@github.com:CMSAachen3B/SVfit_standalone.git TauAnalysis/SVfitStandalone -b HIG-16-006
git clone git@github.com:TauPolSoftware/SimpleFits.git TauPolSoftware/SimpleFits

# polarisation
git clone git@github.com:TauPolSoftware/TauDecaysInterface.git TauPolSoftware/TauDecaysInterface
git clone git@github.com:TauPolSoftware/CalibrationCurve.git TauPolSoftware/CalibrationCurve

# MadGraph
git clone git@github.com:CMSAachen3B/MadGraphReweighting.git CMSAachen3B/MadGraphReweighting

# MELA/JHU
git clone git@github.com:cms-analysis/HiggsAnalysis-ZZMatrixElement.git ZZMatrixElement -b v2.1.1 # see mail from Heshy Roskes sent on 15.11.2017 20:32
cd ZZMatrixElement
git checkout -b v2.1.1
#mkdir MELA/data/slc7_amd64_gcc530
#cp MELA/data/slc6_amd64_gcc530/download.url MELA/data/slc7_amd64_gcc530/
./setup.sh -j `grep -c ^processor /proc/cpuinfo`
cd $CMSSW_BASE/src/

# Jet2Tau Fakes as described here https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauJet2TauFakes
git clone git@github.com:CMS-HTT/Jet2TauFakes.git HTTutilities/Jet2TauFakes
cd $CMSSW_BASE/src/HTTutilities/Jet2TauFakes
git checkout -b v0.2.2

cd $CMSSW_BASE/src/

# 2017 tau trigger efficiencies
mkdir TauAnalysisTools
git clone -b final_2017_MCv2 git@github.com:cms-tau-pog/TauTriggerSFs $CMSSW_BASE/src/TauAnalysisTools/TauTriggerSFs

# EmuQCD Method
git clone git@github.com:CMS-HTT/QCDModelingEMu.git HTT-utilities/QCDModelingEMu

# needed for plotting and statistical inference
if [[ $ch_branch == "SM2016-dev" ]] && [[ $cmssw_version == "747" ]]; then
	git clone git@github.com:thomas-mueller/CombineHarvester.git CombineHarvester -b SM2016-dev
	cd CombineHarvester/HTTSM2016
	git clone https://gitlab.cern.ch/cms-htt/SM-PAS-2016.git shapes
	cd -
	git clone git@github.com:cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
	cd HiggsAnalysis/CombinedLimit
	git fetch origin
	git checkout v6.3.1
	cd -

elif [[ $ch_branch == "master" ]]  && [[ $cmssw_version == "747" ]]; then
	# needed for plotting and statistical inference
	git clone git@github.com:cms-analysis/CombineHarvester.git CombineHarvester
	#git clone git@github.com:TauPolSoftware/CombineHarvester.git CombineHarvester -b taupol2016
	git clone git@github.com:cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit -b 74x-root6
	cd HiggsAnalysis/CombinedLimit
	git checkout 3cb65246555d094734a81e20181e399714d22c7e
	cd -
	
elif [[ $ch_branch == "master" ]]  && [[ $cmssw_version == "810" ]]; then
	git clone git@github.com:cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
	cd HiggsAnalysis/CombinedLimit
	git fetch origin
	git checkout v7.0.10
	cd -
	git clone git@github.com:cms-analysis/CombineHarvester.git CombineHarvester


elif [[ $cmssw_version == "940" ]]; then
        echo "No valid CombineHarvester for 940. Compilation won't work. Checking out state of 810"
        # needed for plotting and statistical inference
        git clone git@github.com:cms-analysis/CombineHarvester.git CombineHarvester
        git clone git@github.com:cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
	cd HiggsAnalysis/CombinedLimit
        git fetch origin
        git checkout v7.0.4
        cd -
else
	git clone git@github.com:cms-analysis/CombineHarvester.git CombineHarvester -b SMCP2016-dev
    cd CombineHarvester/HTTSMCP2016
    git clone https://gitlab.cern.ch/cms-htt/SM-PAS-2016.git shapes
    cd -
    git clone git@github.com:cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
    cd HiggsAnalysis/CombinedLimit
    git fetch origin
    git checkout v7.0.4
    cd -

fi

# Grid-Control
git clone git@github.com:grid-control/grid-control.git -b testing
cd grid-control
git reset --hard 3f93692
cd $CMSSW_BASE/src/

# source ini script, needs to be done in every new shell
source HiggsAnalysis/KITHiggsToTauTau/scripts/ini_KITHiggsToTauTauAnalysis.sh

# compile everything
scramv1 b -j `grep -c ^processor /proc/cpuinfo`

