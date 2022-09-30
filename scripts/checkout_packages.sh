#!/bin/sh
#set -e # exit on errors

ssh -vT git@github.com

read -e -p "Enter the CMMSW release you want to use (747, 810, 942, 10220 [default]) and press [ENTER] (747 is for SL6, 810, 942 and 10220 is for SL7): " -i "10220" cmssw_version
read -e -p "Enter the CombineHarvester developer branch you want to checkout (master, SM2016-dev, SMCP2016-dev, classicsvfit, HTTCPDecays18-dev [default]) and press [ENTER] : " -i "HTTCPDecays18-dev" ch_branch

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

elif [[ $cmssw_version = "810" ]]; then
	# set up CMSSW release area
	export SCRAM_ARCH=slc6_amd64_gcc530
	scramv1 project CMSSW CMSSW_8_1_0; cd CMSSW_8_1_0/src # slc6 # Combine requires this version
	eval `scramv1 runtime -sh`
	export BRANCH="master"

elif [[ $cmssw_version = "10220" ]]; then
	export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
	source $VO_CMS_SW_DIR/cmsset_default.sh
	read -e -p "Enter the Linux release you want to use (SL6, SL7 [default]) and press [ENTER]: " -i "SL7" sl_version
	if [[ $sl_version = "SL6" ]] || [[ $sl_version = "6" ]] || [[ $sl_version = "SLC6" ]]; then
	    export SCRAM_ARCH=slc6_amd64_gcc700
	    scramv1 project -n CMSSW_10_2_20 CMSSW CMSSW_10_2_20
	else
	    export SCRAM_ARCH=slc7_amd64_gcc700
	    scramv1 project -n CMSSW_10_2_20 CMSSW CMSSW_10_2_20_UL
	fi
	cd CMSSW_10_2_20/src
	eval `scramv1 runtime -sh`

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
git clone git@github.com:KappaAnalysis/Kappa.git -b dictchanges_CMSSW102X
cd Kappa
echo docs/ >> .git/info/sparse-checkout
echo DataFormats/ >> .git/info/sparse-checkout
echo Skimming/ >> .git/info/sparse-checkout
git config core.sparsecheckout true
git read-tree -mu HEAD
cd ..

git clone git@github.com:artus-analysis/Artus.git -b dictchanges_CMSSW102

# checkout KITHiggsToTauTau CMSSW analysis package
git clone --recursive git@github.com:cms-analysis/HiggsAnalysis-KITHiggsToTauTau HiggsAnalysis/KITHiggsToTauTau -b dictchanges_CMSSW102

# Di-tau system reconstruction
git clone git@github.com:SVfit/ClassicSVfit.git TauAnalysis/ClassicSVfit -b fastMTT_19_02_2019
git clone git@github.com:SVfit/SVfitTF.git TauAnalysis/SVfitTF
git clone git@github.com:CMSAachen3B/SVfit_standalone.git TauAnalysis/SVfitStandalone -b HIG-16-006
cd TauAnalysis/SVfitStandalone
cat <<EOF >> svFitStandalone.patch
--- a/src/SVfitStandaloneQuantities.cc
+++ b/src/SVfitStandaloneQuantities.cc
@@ -11,6 +11,7 @@
 #include <TMatrixDSym.h>
 #include <TMatrixDSymEigen.h>
 #include <TVectorD.h>
+#include <numeric>

 namespace svFitStandalone
 {
EOF
patch ./src/SVfitStandaloneQuantities.cc svFitStandalone.patch
cd $CMSSW_BASE/src/
git clone git@github.com:TauPolSoftware/SimpleFits.git TauPolSoftware/SimpleFits -b master

# polarisation
git clone git@github.com:TauPolSoftware/TauDecaysInterface.git TauPolSoftware/TauDecaysInterface
git clone git@github.com:TauPolSoftware/CalibrationCurve.git TauPolSoftware/CalibrationCurve

# MadGraph
git clone git@github.com:CMSAachen3B/MadGraphReweighting.git CMSAachen3B/MadGraphReweighting

# MELA/JHU
git clone --depth 1 --branch v2.3.7 git@github.com:JHUGen/JHUGenMELA.git JHUGenMELA
cd JHUGenMELA
./setup.sh -j `grep -c ^processor /proc/cpuinfo`
eval $(./setup.sh env)

cd $CMSSW_BASE/src/

# Jet2Tau Fakes as described here https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauJet2TauFakes
git clone --depth 1 --branch v0.2.2 git@github.com:CMS-HTT/Jet2TauFakes.git HTTutilities/Jet2TauFakes

# 2017 tau trigger efficiencies
mkdir TauAnalysisTools
if [[ $cmssw_version == "10220" ]]; then
	git clone -b run2_SFs git@github.com:cms-tau-pog/TauTriggerSFs $CMSSW_BASE/src/TauAnalysisTools/TauTriggerSFs
else
	git clone -b final_2017_MCv2 git@github.com:cms-tau-pog/TauTriggerSFs $CMSSW_BASE/src/TauAnalysisTools/TauTriggerSFs
fi

git clone --depth 1 https://github.com/cms-tau-pog/TauIDSFs.git $CMSSW_BASE/src/TauPOG/TauIDSFs

# EmuQCD Method
git clone --depth 1 git@github.com:CMS-HTT/QCDModelingEMu.git HTT-utilities/QCDModelingEMu

# MET Recoil Corrections for PF Met and Puppi Met
git clone --depth 1 https://github.com/KIT-CMS/RecoilCorrections.git HTT-utilities/RecoilCorrections

# needed for plotting and statistical inference
# recommendations found here: https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/#setting-up-the-environment-and-installation
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
	git checkout v7.0.13
	cd -
	git clone git@github.com:cms-analysis/CombineHarvester.git CombineHarvester

elif [[ $cmssw_version == "940" ]]; then
	echo "No valid CombineHarvester for 940. Compilation won't work. Checking out state of 810"
	if [[ $ch_branch == "HTTCPDecays18-dev" ]]; then
		git clone git@github.com:albertdow/CombineHarvester CombineHarvester
	else
		git clone git@github.com:cms-analysis/CombineHarvester.git CombineHarvester
	fi
	git clone git@github.com:cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
	cd HiggsAnalysis/CombinedLimit
	git fetch origin
	git checkout v7.0.13
	cd -

elif [[ $cmssw_version == "10220" ]]; then
	# needed for plotting and statistical inference
	if [[ $ch_branch == "HTTCPDecays18-dev" ]]; then
		git clone git@github.com:azotz/CombineHarvester CombineHarvester -b HTTCPDecays18-dev
	else
		git clone git@github.com:cms-analysis/CombineHarvester.git CombineHarvester -b SMCP2016-dev
		cd CombineHarvester/HTTSMCP2016
		git clone https://gitlab.cern.ch/cms-htt/SM-PAS-2016.git shapes
		cd -
	fi
	git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
	cd HiggsAnalysis/CombinedLimit
	git fetch origin
	git checkout v8.0.1
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
git clone git@github.com:artus-analysis/grid-control -b master

cd $CMSSW_BASE/src/

# HiggsCPinTauDecays
# Not all modules are needed here since the TauRefit is only used during skimming
git clone git@github.com:CMS-HTT/HiggsCPinTauDecays.git
cd HiggsCPinTauDecays
echo ImpactParameter/ >> .git/info/sparse-checkout
echo IpCorrection/ >> .git/info/sparse-checkout
git config core.sparsecheckout true
git read-tree -mu HEAD
cd ..

# source ini script, needs to be done in every new shell
source HiggsAnalysis/KITHiggsToTauTau/scripts/ini_KITHiggsToTauTauAnalysis.sh

# compile everything
scramv1 b -j `grep -c ^processor /proc/cpuinfo`
