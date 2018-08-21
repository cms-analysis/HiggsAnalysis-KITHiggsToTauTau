#!/bin/sh

# Creates the workspaces and likelihoodscans for consraining ggH rate to SM value.
combineTool.py -M T2W -P CombineHarvester.CombinePdfs.CPMixture:CPMixture -i $CMSSW_BASE/src/CombineHarvester/HTTSMCP2016/output/$1/{cmb,em,et,mt,tt}/* -o ws.root --parallel 8 --PO constrain_ggHYield

# alpha scan
combineTool.py -m 125 -M MultiDimFit --setParameters muF=1,muV=1,alpha=0,f=0 --freezeParameters f,muF --setParameterRanges alpha=0,1 --points 20 --split-points 2 --parallel 10 --redefineSignalPOIs alpha -d $CMSSW_BASE/src/CombineHarvester/HTTSMCP2016/output/$1/cmb/125/ws.root --algo grid -t -1 --there -n .alpha_ggFconstrain
# Add single points into one 
cd $CMSSW_BASE/src/CombineHarvester/HTTSMCP2016/output/$1/cmb/125/
hadd higgsCombine.alpha_ggFconstrain.MultiDimFit.mH125.root higgsCombine.alpha_ggFconstrain.POINTS.*.MultiDimFit.mH125.root
# plot the  
cd $CMSSW_BASE/src/
python $CMSSW_BASE/src/CombineHarvester/HTTSMCP2016/scripts/plot1DScan.py --main="$CMSSW_BASE/src/CombineHarvester/HTTSMCP2016/output/RWTH_dijet_mela3D_20180820_newOutputs_nocache/cmb/125/higgsCombine.alpha_ggFconstrain.MultiDimFit.mH125.root" --POI=alpha --output="CombineHarvester/HTTSMCP2016/output/RWTH_dijet_mela3D_20180820_newOutputs_nocache/cmb/125/alpha_ggFconstrain" --no-numbers  --no-box --x_title='#alpha_{t}(#frac{#pi}{2})' --y-max=17.0 --use-html-colors --title="#alpha_{t}(#mu_F=1)"
