#!/bin/bash

mg5_aMC $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/madgraph/HiggsCharacterisation/configs/ggh.txt

sed -i -e "s@\(F2PY.*\)\$@\1 --fcompiler=gnu95@g" $MADGRAPH_DIR/gg_X0/SubProcesses/makefile

echo "hallo"
for makefile in $MADGRAPH_DIR/gg_X0/SubProcesses/P*/makefile;
do
	echo `dirname $makefile`
	echo "before"
	cd `dirname $makefile` 
	echo "hi"	
	pwd
	echo "here starts matrix2py"
	make matrix2py.so 
	#|| (echo "Compilation failed"; exit)
done

