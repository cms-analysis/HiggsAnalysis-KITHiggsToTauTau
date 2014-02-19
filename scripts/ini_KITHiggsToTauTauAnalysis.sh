#!/bin/bash

# set the environment
export BOOSTPATH=$(ls /afs/cern.ch/cms/${SCRAM_ARCH}/external/boost/* -d | tail -n 1)/
export ARTUS_BASE=$CMSSW_BASE/src/Artus
export KAPPAPATH=$CMSSW_BASE/src/Kappa
export KAPPATOOLSPATH=$CMSSW_BASE/KappaTools
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$EXCALIBUR_BASE:$EXCALIBUR_BASE/../Kappa/lib:$EXCALIBUR_BASE/../KappaTools/lib:$BOOSTPATH/lib
#export PATH=$EXCALIBUR_BASE/scripts:$PATH
#export PYTHONPATH=$EXCALIBUR_BASE/plotting:$EXCALIBUR_BASE/plotting/tools:$EXCALIBUR_BASE/cfg/artus:$PYTHONPATH
export USERPC=`who am i | sed 's/.*(\([^]]*\)).*/\1/g'`

# activate pre-commit hooks
ln -sf $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/pre-commit  $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/.git/hooks/


