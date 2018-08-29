#!/bin/sh

# Requires already performed likelihoodscan with grid 
combineTool.py -m 125 -M MultiDimFit --setParameters muF=1,muV=1,alpha=0,f=0 --freezeParameters f --setParameterRanges alpha=0,1 --points 20 --split-points 2 --redefineSignalPOIs alpha -d $CMSSW_BASE/src/CombineHarvester/HTTSMCP2016/output/$1/cmb/125/ws.root --algo grid -t -1 --there -n .alpha --parallel=10
# save best snapshot
combineTool.py -m 125 -M MultiDimFit --setParameters muF=1,muV=1,alpha=0,f=0 --freezeParameters f --setParameterRanges alpha=0,1 --points 20 --split-points 1 --redefineSignalPOIs alpha -d $CMSSW_BASE/src/CombineHarvester/HTTSMCP2016/output/$1/cmb/125/ws.root --algo none -t -1 --there -n .alpha_bestfit --parallel=20 --saveWorkspace
# Repeat first scan and load snapshot, freeze all nuisance parameters
combineTool.py -m 125 -M MultiDimFit --setParameters muF=1,muV=1,alpha=0,f=0 --setParameterRanges alpha=0,1 --points 20  --redefineSignalPOIs alpha -d /afs/desy.de/user/d/dwolfsch/cms_analysis/CMSSW_8_1_0/src/CombineHarvester/HTTSMCP2016/output/2018-08-25_FULL_mela3D_new_outputs_JECgroupings/cmb/125/higgsCombine.alpha_bestfit.MultiDimFit.mH125.root --algo grid -t -1 --there -n .alpha_stat --parallel=20 --freezeParameters="all"   --snapshotName MultiDimFit --robustFit  1
