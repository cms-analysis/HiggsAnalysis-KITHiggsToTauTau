#!/bin/sh

# Creates the workspaces and likelihoodscans.
combineTool.py -M T2W -P CombineHarvester.CombinePdfs.CPMixture:CPMixture -i $CMSSW_BASE/src/CombineHarvester/HTTSMCP2016/output/$1/{cmb,em,et,mt,tt}/* -o ws.root --parallel 8

# alpha scan
combineTool.py -m 125 -M MultiDimFit --setParameters muF=1,muV=1,alpha=0,f=0 --freezeParameters f --setParameterRanges alpha=0,1 --points 20 --split-points 2 --redefineSignalPOIs alpha -d $CMSSW_BASE/src/CombineHarvester/HTTSMCP2016/output/$1/{cmb,em,et,mt,tt}/125/ws.root --algo grid -t -1 --there -n .alpha --parallel=10
cd $CMSSW_BASE/src/CombineHarvester/HTTSMCP2016/output/$1/cmb/125/
hadd higgsCombine.alpha.MultiDimFit.mH125.root higgsCombine.alpha.POINTS.*.MultiDimFit.mH125.root
cd $CMSSW_BASE/src
combineTool.py -m 125 -M MultiDimFit --setParameters muF=1,muV=1,alpha=0,f=0 --setParameterRanges alpha=0,1 --points 10 --split-points 1 --redefineSignalPOIs alpha -d $CMSSW_BASE/src/CombineHarvester/HTTSMCP2016/output/$1/{cmb,em,et,mt,tt}/125/ws.root --algo grid -t -1 --there -n .alpha_f_floating --parallel=10
cd $CMSSW_BASE/src/CombineHarvester/HTTSMCP2016/output/$1/cmb/125/
hadd higgsCombine.alpha_f_floating.MultiDimFit.mH125.root higgsCombine.alpha_f_floating.POINTS.*.MultiDimFit.mH125.root
cd $CMSSW_BASE/src
combineTool.py -m 125 -M MultiDimFit --setParameters muF=1,muV=1,alpha=0,f=0 --freezeParameters f --setParameterRanges muF=0,4 --points 20  --split-points 2 --redefineSignalPOIs muF -d $CMSSW_BASE/src/CombineHarvester/HTTSMCP2016/output/$1/{cmb,em,et,mt,tt}/125/ws.root --algo grid -t -1 --there -n .muF --parallel=10
cd $CMSSW_BASE/src/CombineHarvester/HTTSMCP2016/output/$1/cmb/125/
hadd higgsCombine.alpha.MultiDimFit.mH125.root higgsCombine.alpha.POINTS.*.MultiDimFit.mH125.root
cd $CMSSW_BASE/src
combineTool.py -m 125 -M MultiDimFit --setParameters muF=1,muV=1,alpha=0,f=0 --freezeParameters f --setParameterRanges alpha=0,1 --redefineSignalPOIs alpha,muF -d $CMSSW_BASE/src/CombineHarvester/HTTSMCP2016/output/$1/{cmb,em,et,mt,tt}/125/ws.root --points 500 --split-points 50 --algo grid -t -1 --there -n .2DScan --parallel=10
cd $CMSSW_BASE/src/CombineHarvester/HTTSMCP2016/output/$1/cmb/125/
hadd higgsCombine.2DScan.MultiDimFit.mH125.root higgsCombine.2DScan.POINTS.*.MultiDimFit.mH125.root
cd $CMSSW_BASE/src


# python $CMSSW_BASE/src/CombineHarvester/HTTSMCP2016/scripts/plot1DScan.py --main="$CMSSW_BASE/src/CombineHarvester/HTTSMCP2016/output/2018-08-25_FULL_mela3D_new_outputs_JECgroupings/cmb/125/higgsCombine.alpha.MultiDimFit.mH125.root" --POI=alpha --output="CombineHarvester/HTTSMCP2016/output/2018-08-25_FULL_mela3D_new_outputs_JECgroupings/cmb/125/alpha" --no-numbers  --no-box --x_title='#alpha_{t}(#frac{#pi}{2})' --y-max=3.0 --use-html-colors --title="#alpha_{t}"
# python $CMSSW_BASE/src/CombineHarvester/HTTSMCP2016/scripts/plot1DScan.py --main=CombineHarvester/HTTSMCP2016/output/2018-08-25_FULL_mela3D_new_outputs_JECgroupings/cmb/125/higgsCombine.alpha.MultiDimFit.mH125.root --POI=alpha --output=CombineHarvester/HTTSMCP2016/output/2018-08-25_FULL_mela3D_new_outputs_JECgroupings/cmb/125/alpha_channel --no-numbers --no-box --x_title='#alpha (#frac{#pi}{2})' --y-max=3.0 --others CombineHarvester/HTTSMCP2016/output/2018-08-25_FULL_mela3D_new_outputs_JECgroupings/tt/125/higgsCombine.alpha.MultiDimFit.mH125.root:#tau_{h}#tau_{h}:#FF4436 CombineHarvester/HTTSMCP2016/output/2018-08-25_FULL_mela3D_new_outputs_JECgroupings/mt/125/higgsCombine.alpha.MultiDimFit.mH125.root:#mu#tau_{h}:#4CAF50 CombineHarvester/HTTSMCP2016/output/2018-08-25_FULL_mela3D_new_outputs_JECgroupings/et/125/higgsCombine.alpha.MultiDimFit.mH125.root:e#tau_{h}:#CDDC39 CombineHarvester/HTTSMCP2016/output/2018-08-25_FULL_mela3D_new_outputs_JECgroupings/em/125/higgsCombine.alpha.MultiDimFit.mH125.root:e#mu:#FFC107 --use-html-colors
