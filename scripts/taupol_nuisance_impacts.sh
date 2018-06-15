#!/bin/sh

# Mandatory options
# $1: datacards output base directory
# $2: www base directory

for WORKSPACE in `ls $1/best_choice/datacards/combined/workspace.root $1/workspace.root 2> /dev/null`
do
	pushd `dirname ${WORKSPACE}`
	
		# initial fit
		combineTool.py -M Impacts --doInitialFit --robustFit 1 -t -1 \
			--setParameters pol=-0.159,r=1 --setParameterRanges pol=-0.2,-0.1:r=0.5,1.5 \
			-m 0 -d `basename ${WORKSPACE}` --parallel 8
	
		# fits for all nuisance parameters
		combineTool.py -M Impacts --robustFit 1 -t -1 --doFits --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP \ #--minimizerAlgoForMinos Minuit2,Migrad \
			--setParameters pol=-0.159,r=1 --setParameterRanges pol=-0.2,-0.1:r=0.5,1.5 \
			-m 0 -d `basename ${WORKSPACE}` --parallel 8
		
		# collect and plot results
		combineTool.py -M Impacts -m 0 -d `basename ${WORKSPACE}` -o impacts.json
		plotImpacts.py -i impacts.json -o impacts
	
	popd
done

