#!/bin/bash

# source Artus ini script
source $CMSSW_BASE/src/Artus/Configuration/scripts/ini_ArtusAnalysis.sh

# source Harry ini script
source $CMSSW_BASE/src/Artus/HarryPlotter/scripts/ini_harry_cmssw.sh

# set the environment
export KITHIGGSTOTAUTAUPATH=$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau

# setup TauSpinner
cp $KITHIGGSTOTAUTAUPATH/data/tauspinner.xml $CMSSW_BASE/config/toolbox/$SCRAM_ARCH/tools/selected/tauspinner.xml
scram setup tauspinner

# setup CombineHarvester
export LD_LIBRARY_PATH="$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/CombineHarvester/CombineTools/lib/:$LD_LIBRARY_PATH"
export PYTHONPATH="$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/CombineHarvester/CombineTools/python/:$PYTHONPATH"
export PATH="$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/CombineHarvester/CombineTools/bin/:$PATH"

# overwrite artus settings
if [[ `hostname` == *naf* ]]; then
	export ARTUS_WORK_BASE="/nfs/dust/cms/user/${USER}/htautau/artus/"
elif [[ `hostname` == *ekp* ]]; then
	export ARTUS_WORK_BASE="/storage/a/${USER}/htautau/artus/"
elif [[ `hostname` == *cern* ]]; then
	export ARTUS_WORK_BASE="/afs/cern.ch/work/${USER:0:1}/${USER}/htautau/artus/"
fi
