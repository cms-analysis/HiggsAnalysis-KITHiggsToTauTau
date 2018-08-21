#!/bin/sh

# Requires already performed likelihoodscan with grid 
combineTool.py -m 125 -M MultiDimFit --setParameters muF=1,muV=1,alpha=0,f=0 --freezeParameters f --setParameterRanges alpha=0,1 --points 20 --split-points 2 --redefineSignalPOIs alpha -d $CMSSW_BASE/src/CombineHarvester/HTTSMCP2016/output/$1/{{cmb,em,et,mt,tt}}/125/ws.root --algo grid -t -1 --there -n .alpha --parallel=10
# save best snapshot
combineTool.py -m 125 -M MultiDimFit --setParameters muF=1,muV=1,alpha=0,f=0 --freezeParameters f --setParameterRanges alpha=0,1 --points 20 --split-points 2 --redefineSignalPOIs alpha -d $CMSSW_BASE/src/CombineHarvester/HTTSMCP2016/output/$1/{{cmb,em,et,mt,tt}}/125/ws.root --algo none -t -1 --there -n .alpha_bestfit --parallel=10 --saveWorkspace
# Repeat first scan and load snapshot, freeze all nuisance parameters
# combineTool.py -m 125 -M MultiDimFit --setParameters muF=1,muV=1,alpha=0,f=0 --freezeParameters f --setParameterRanges alpha=0,1 --points 20 --split-points 2 --redefineSignalPOIs alpha higgsCombine --algo grid -t -1 --there -n .alpha_stat --parallel=10
