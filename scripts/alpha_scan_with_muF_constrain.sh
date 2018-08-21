#!/bin/sh

# Creates the workspaces and likelihoodscans for consraining ggH rate to SM value.
# combineTool.py -M T2W -P CombineHarvester.CombinePdfs.CPMixture:CPMixture -i $CMSSW_BASE/src/CombineHarvester/HTTSMCP2016/output/$1/{cmb,em,et,mt,tt}/* -o ws.root --parallel 8 --PO constrain_ggHYield

# alpha scan
combineTool.py -m 125 -M MultiDimFit --setParameters muF=1,muV=1,alpha=0,f=0 --freezeParameters f,muF --setParameterRanges alpha=0,1 --points 20 --split-points 2 --parallel 10 --redefineSignalPOIs alpha -d $CMSSW_BASE/src/CombineHarvester/HTTSMCP2016/output/$1/cmb/125/ws.root --algo grid -t -1 --there -n .alpha_ggFconstrain
