#!/bin/sh

# Mandatory options
# $1: datacards output base directory
# $2: www base directory

# datacards
${CMSSW_BASE}/src/CombineHarvester/ZTTPOL2016/scripts/zttpol_projection.py \
	-d $1/best_choice/datacards/individual/*/*/ztt*13TeV.txt \
	--in-lumi 35.87 --out-lumis 300 600 900 1200 1500 1800 2100 2400 2700 3000 \
	--combinations combined	-o $1/best_choice/projection

# workspaces
combineTool.py -M T2W -o workspace.orig.root -P CombineHarvester.ZTTPOL2016.taupolarisationmodels:ztt_pol -m 0 -i $1/best_choice/projection/*/datacards/combined/ztt*13TeV.txt --parallel 8
	
# likelihood scans
combineTool.py -M MultiDimFit --points 100 --redefineSignalPOIs pol --freezeParameters r --algo grid --there -n .pol_r1.orig.scan -m 0 -d $1/best_choice/projection/*/datacards/combined/workspace.orig.root --parallel 8 \
	--setParameters pol=-0.159,r=1 --setParameterRanges pol=-0.17,-0.15:r=0.5,1.5

combineTool.py -M MultiDimFit --points 100 --redefineSignalPOIs pol --algo grid --there -n .pol.orig.scan -m 0 -d $1/best_choice/projection/*/datacards/combined/workspace.orig.root --parallel 8 \
	--setParameters pol=-0.159,r=1 --setParameterRanges pol=-0.17,-0.15:r=0.5,1.5

# plotting
for COMBINE_OUTPUT in $1/best_choice/projection/*/datacards/combined/higgsCombine*.root
do
	echo annotate-trees.py ${COMBINE_OUTPUT} -t limit -b lumi --values `echo ${COMBINE_OUTPUT} | sed -e "s@$1/best_choice/projection/@@g" -e "s@/datacards/combined/higgsCombine.*\.root@@g"`
done | runParallel.py -n 8
