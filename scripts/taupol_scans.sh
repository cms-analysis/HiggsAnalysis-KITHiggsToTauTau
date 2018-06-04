#!/bin/sh

# Mandatory options
# $1: datacards output base directory
# $2: www base directory


# ===== r floating ================================================================================

# combine
combineTool.py -M MultiDimFit --points 200 --redefineSignalPOIs pol --algo grid --there -n .pol -m 0 -d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/workspace.root --parallel 8

# plotting

for COMBINE_OUTPUT in $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol.MultiDimFit.mH0.root; do
	
	# full range
	higgsplot.py -i ${COMBINE_OUTPUT} -f limit -x pol -y "2*deltaNLL" --tree-draw-options TGraph --analysis-modules LikelihoodScan --x-lims -1 1 --y-lims 0 100 \
		--x-label "Average Polarisation #LTP_{#tau}#GT" --y-label "Likelihood -2#Deltaln L" --title "r floating" -m LP L L L --marker-sizes 0.5 --line-styles 1 1 2 3 -C 2 1 1 1 \
		--www  $2/`echo ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g" -e "s@higgsCombine.pol.MultiDimFit.mH0.root@@g"` --filename higgsCombine.pol.MultiDimFit.mH0 --formats pdf png \
		--dry-run
	
	# zoomed
	higgsplot.py -i ${COMBINE_OUTPUT} -f limit -x pol -y "2*deltaNLL" --tree-draw-options TGraph --analysis-modules LikelihoodScan --x-lims -0.3 0 --y-lims 0 10 \
		--x-label "Average Polarisation #LTP_{#tau}#GT" --y-label "Likelihood -2#Deltaln L" --title "r floating" -m LP L L L --marker-sizes 0.5 --line-styles 1 1 2 3 -C 2 1 1 1 \
		--www  $2/`echo ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g" -e "s@higgsCombine.pol.MultiDimFit.mH0.root@@g"` --filename higgsCombine.pol.MultiDimFit.mH0_zoom --formats pdf png \
		--no-cache --dry-run
done
makePlots_jsonConfigs.py -j $(ls websync/`date +%Y_%m_%d`/$2/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol.MultiDimFit.mH0{,_zoom}.json) -n 8


# ===== r=1 fixed =================================================================================

# combine
combineTool.py -M MultiDimFit --points 200 --redefineSignalPOIs pol --freezeParameters r --algo grid --there -n .pol_r1 -m 0 -d $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/workspace.root --parallel 8

# plotting

for COMBINE_OUTPUT in $1/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol_r1.MultiDimFit.mH0.root; do
	
	# full range
	higgsplot.py -i ${COMBINE_OUTPUT} -f limit -x pol -y "2*deltaNLL" --tree-draw-options TGraph --analysis-modules LikelihoodScan --x-lims -1 1 --y-lims 0 100 \
		--x-label "Average Polarisation #LTP_{#tau}#GT" --y-label "Likelihood -2#Deltaln L" --title "r=1 fixed" -m LP L L L --marker-sizes 0.5 --line-styles 1 1 2 3 -C 4 1 1 1 \
		--www  $2/`echo ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g" -e "s@higgsCombine.pol_r1.MultiDimFit.mH0.root@@g"` --filename higgsCombine.pol_r1.MultiDimFit.mH0 --formats pdf png \
		--dry-run
	
	# zoomed
	higgsplot.py -i ${COMBINE_OUTPUT} -f limit -x pol -y "2*deltaNLL" --tree-draw-options TGraph --analysis-modules LikelihoodScan --x-lims -0.3 0 --y-lims 0 10 \
		--x-label "Average Polarisation #LTP_{#tau}#GT" --y-label "Likelihood -2#Deltaln L" --title "r=1 fixed" -m LP L L L --marker-sizes 0.5 --line-styles 1 1 2 3 -C 3 1 1 1 \
		--www  $2/`echo ${COMBINE_OUTPUT} | sed -e "s@${1}/@@g" -e "s@higgsCombine.pol_r1.MultiDimFit.mH0.root@@g"` --filename higgsCombine.pol_r1.MultiDimFit.mH0_zoom --formats pdf png \
		--no-cache --dry-run
done
makePlots_jsonConfigs.py -j $(ls websync/`date +%Y_%m_%d`/$2/*/datacards/{individual/*/*,category/*,channel/*,combined}/higgsCombine.pol_r1.MultiDimFit.mH0{,_zoom}.json) -n 8

