for WORKSPACE in $1/cmb/125/htt_mt_2017_*_cpmixture.root; do
	echo combineTool.py -M FitDiagnostics --redefineSignalPOIs alpha --there -m 125 --parallel 8 --robustFit 1 --preFitValue 0.0 --cminDefaultMinimizerType Minuit2 --cminDefaultMinimizerAlgo Minuit2 --cminDefaultMinimizerStrategy 0 --cminFallbackAlgo Minuit2,0:1.0 \
		-d ${WORKSPACE} \
		-n `echo ${WORKSPACE} | sed -e "s@$1/cmb/125/htt_mt_2017_@.alpha@g"| sed -e "s@_13TeV_cpmixture.root@@g"`
done | runParallel.py -n 8

for WORKSPACE in $1/cmb/125/htt_et_2017_*_cpmixture.root; do
	echo combineTool.py -M FitDiagnostics --redefineSignalPOIs alpha --there -m 125 --parallel 8 --robustFit 1 --preFitValue 0.0 --cminDefaultMinimizerType Minuit2 --cminDefaultMinimizerAlgo Minuit2 --cminDefaultMinimizerStrategy 0 --cminFallbackAlgo Minuit2,0:1.0 \
		-d ${WORKSPACE} \
		-n `echo ${WORKSPACE} | sed -e "s@$1/cmb/125/htt_et_2017_@.alpha@g"| sed -e "s@_13TeV_cpmixture.root@@g"`
done | runParallel.py -n 8

echo "-------------------------------------------------------------------------"

for WORKSPACE in $1/cmb/125/htt_mt_2017_*_cpmixture.root; do
	echo PostFitShapesFromWorkspace --postfit -m 125 \
		-f `echo ${WORKSPACE}:fit_b | sed -e "s@htt_mt_2017_@fitDiagnostics.alpha@g"| sed -e "s@_13TeV_cpmixture.root@.root@g"` \
		-w ${WORKSPACE} \
		-d `echo ${WORKSPACE} | sed -e "s@_13TeV_cpmixture.root@_13TeV.txt@g"` \
		-o `echo ${WORKSPACE} | sed -e "s@htt_mt_2017_@htt_mt_2017_postFitShapesFromWorkspace.alpha@g"| sed -e "s@_13TeV_cpmixture.root@_fit_b.root@g"`

	echo PostFitShapesFromWorkspace --postfit -m 125 \
		-f `echo ${WORKSPACE}:fit_s | sed -e "s@htt_mt_2017_@fitDiagnostics.alpha@g"| sed -e "s@_13TeV_cpmixture.root@.root@g"` \
		-w ${WORKSPACE} \
		-d `echo ${WORKSPACE} | sed -e "s@_13TeV_cpmixture.root@_13TeV.txt@g"` \
		-o `echo ${WORKSPACE} | sed -e "s@htt_mt_2017_@htt_mt_2017_postFitShapesFromWorkspace.alpha@g"| sed -e "s@_13TeV_cpmixture.root@_fit_s.root@g"`
done | runParallel.py -n 8



for WORKSPACE in $1/cmb/125/htt_et_2017_*_cpmixture.root; do
	echo PostFitShapesFromWorkspace --postfit -m 125 \
		-f `echo ${WORKSPACE}:fit_b | sed -e "s@htt_et_2017_@fitDiagnostics.alpha@g"| sed -e "s@_13TeV_cpmixture.root@.root@g"` \
		-w ${WORKSPACE} \
		-d `echo ${WORKSPACE} | sed -e "s@_13TeV_cpmixture.root@_13TeV.txt@g"` \
		-o `echo ${WORKSPACE} | sed -e "s@htt_et_2017_@htt_et_2017_postFitShapesFromWorkspace.alpha@g"| sed -e "s@_13TeV_cpmixture.root@_fit_b.root@g"`

	echo PostFitShapesFromWorkspace --postfit -m 125 \
		-f `echo ${WORKSPACE}:fit_s | sed -e "s@htt_et_2017_@fitDiagnostics.alpha@g"| sed -e "s@_13TeV_cpmixture.root@.root@g"` \
		-w ${WORKSPACE} \
		-d `echo ${WORKSPACE} | sed -e "s@_13TeV_cpmixture.root@_13TeV.txt@g"` \
		-o `echo ${WORKSPACE} | sed -e "s@htt_et_2017_@htt_et_2017_postFitShapesFromWorkspace.alpha@g"| sed -e "s@_13TeV_cpmixture.root@_fit_s.root@g"`
done | runParallel.py -n 8
