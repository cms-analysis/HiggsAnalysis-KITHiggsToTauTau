#!/bin/sh

# Mandatory options
# $1: datacards output base directory
# $2: www base directory


# ===== r floating ================================================================================

# combine

combineTool.py -M FitDiagnostics --redefineSignalPOIs pol --there -n .pol -m 0 -d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/workspace.root --parallel 8

for COMBINE_OUTPUT in $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/fitDiagnostics.pol.root; do

	echo PostFitShapesFromWorkspace --postfit -m 0 -f ${COMBINE_OUTPUT}:fit_s \
		-w `echo ${COMBINE_OUTPUT} | sed -e "s@/fitDiagnostics.pol.root@/workspace.root@g"` \
		-d `echo ${COMBINE_OUTPUT} | sed -e "s@/fitDiagnostics.pol.root@/ztt*_13TeV.txt@g"` \
		-o `echo ${COMBINE_OUTPUT} | sed -e "s@/fitDiagnostics.pol.root@/postFitShapesFromWorkspace.pol.root@g"`

done | runParallel.py -n 8

# plotting

for SHAPES in $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/postFitShapesFromWorkspace.pol.root; do

	echo ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_prefitPostfitPlots.py -i ${SHAPES} \
		-b ZTTPOSPOL ZTTNEGPOL "\"ZLL ZL ZJ\"" "\"TT TTT TTJ\"" W "\"VV VVT VVJ EWKZ\"" QCD \
		--polarisation -r -a "\" --x-label Discriminator --y-subplot-lims 0.5 1.5 --formats pdf png\"" \
		--www $2/`echo ${SHAPES} | sed -e "s@${1}/@@g" -e "s@postFitShapesFromWorkspace.pol.root@@g"`

done | runParallel.py -n 8


# ===== r=1 fixed =================================================================================

# combine

combineTool.py -M FitDiagnostics --redefineSignalPOIs pol --freezeParameters r --there -n .pol_r1 -m 0 -d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/workspace.root --parallel 8

for COMBINE_OUTPUT in $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/fitDiagnostics.pol_r1.root; do

	echo PostFitShapesFromWorkspace --postfit -m 0 -f ${COMBINE_OUTPUT}:fit_s \
		-w `echo ${COMBINE_OUTPUT} | sed -e "s@/fitDiagnostics.pol_r1.root@/workspace.root@g"` \
		-d `echo ${COMBINE_OUTPUT} | sed -e "s@/fitDiagnostics.pol_r1.root@/ztt*_13TeV.txt@g"` \
		-o `echo ${COMBINE_OUTPUT} | sed -e "s@/fitDiagnostics.pol_r1.root@/postFitShapesFromWorkspace.pol_r1.root@g"`

done | runParallel.py -n 8

# plotting

for SHAPES in $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/postFitShapesFromWorkspace.pol_r1.root; do

	echo ${CMSSW_BASE}/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_prefitPostfitPlots.py -i ${SHAPES} \
		-b ZTTPOSPOL ZTTNEGPOL "\"ZLL ZL ZJ\"" "\"TT TTT TTJ\"" W "\"VV VVT VVJ EWKZ\"" QCD \
		--polarisation -r -a "\" --x-label Discriminator --y-subplot-lims 0.5 1.5 --formats pdf png\"" \
		--www $2/`echo ${SHAPES} | sed -e "s@${1}/@@g" -e "s@postFitShapesFromWorkspace.pol_r1.root@@g"`

done | runParallel.py -n 8

