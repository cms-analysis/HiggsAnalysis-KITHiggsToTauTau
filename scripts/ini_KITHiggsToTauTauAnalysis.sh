#!/bin/bash

# source Artus ini script
source $CMSSW_BASE/src/Artus/Configuration/scripts/ini_ArtusAnalysis.sh

# source Harry ini script
source $CMSSW_BASE/src/Artus/HarryPlotter/scripts/ini_harry_cmssw.sh

# set the environment
export KITHIGGSTOTAUTAUPATH=$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau

# grid-control
export PATH=${CMSSW_BASE}/src/grid-control/:${CMSSW_BASE}/src/grid-control/scripts/:${PATH}

# setup TauSpinner
cp $KITHIGGSTOTAUTAUPATH/data/tauspinner.xml $CMSSW_BASE/config/toolbox/$SCRAM_ARCH/tools/selected/tauspinner.xml
scram setup tauspinner

#setup FastBDT
cp $KITHIGGSTOTAUTAUPATH/data/fastbdt.xml $CMSSW_BASE/config/toolbox/$SCRAM_ARCH/tools/selected/fastbdt.xml
scram setup fastbdt

if [ "$1" != "no-links" ]
then
	if [ command -v symlinks > /dev/null 2>&1 ]; then
		symlinks -c ${CMSSW_BASE}/external/${SCRAM_ARCH}/lib/ > /dev/null 2>&1
	else
		for FILE in ${CMSSW_BASE}/external/${SCRAM_ARCH}/lib/*; do
			if [ -L $FILE ]; then
				LINKPATH=$(readlink $FILE)
				rm -f $FILE
				ln -s ${LINKPATH/$CMSSW_BASE/..\/..\/..} $FILE
			fi
		done
	fi
else
	echo "Link creation deactivated"

fi
# FastBDT
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${CMSSW_BASE}/src/FastBDT/

# overwrite artus settings
if [[ `hostname` == *naf* ]]; then
	export ARTUS_WORK_BASE="/nfs/dust/cms/user/${USER}/htautau/artus/"
elif [[ `hostname` == *ekpbms* ]] && [ ${USER} == "wayand" ]; then
    echo "Hallo stefan auf der bms"
    export ARTUS_WORK_BASE="/portal/ekpbms2/home/wayand/htautau/artus"
elif [[ `hostname` == *ekp* ]]; then
	STORAGELIST=(a 5 6 7 8 9 jbod) #list of allowed storages ordered by priority (descending)
	for STORAGE in ${STORAGELIST[*]}
		do
			if [ -d /storage/${STORAGE}/${USER} ]; then
				export ARTUS_WORK_BASE="/storage/${STORAGE}/${USER}/htautau/artus/"
				break
			fi
	done
elif [[ `hostname` == *cern* ]]; then
	export ARTUS_WORK_BASE="/afs/cern.ch/work/${USER:0:1}/${USER}/htautau/artus/"
fi
