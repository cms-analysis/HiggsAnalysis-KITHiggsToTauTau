#!/bin/bash

# set the environment
export KAPPAPATH=$CMSSW_BASE/src/Kappa
export KAPPATOOLSPATH=$CMSSW_BASE/KappaTools
export ARTUSPATH=$CMSSW_BASE/src/Artus
export KITHIGGSTOTAUTAUPATH=$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau

# configurations needed for compilation of C++ code
#export BOOSTPATH=$(ls /afs/cern.ch/cms/${SCRAM_ARCH}/external/boost/* -d | tail -n 1)/
export LD_LIBRARY_PATH="$CMSSW_BASE/src/KappaTools/lib/:$CMSSW_BASE/src/Kappa/lib/:$LD_LIBRARY_PATH"

# useful to rediect messages
export USERPC=`who am i | sed 's/.*(\([^]]*\)).*/\1/g'`

# activate pre-commit hooks
ln -sf $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/pre-commit  $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/.git/hooks/

