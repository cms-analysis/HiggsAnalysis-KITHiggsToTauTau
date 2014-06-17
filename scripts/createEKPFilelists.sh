FILES=$(ls $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/Samples)

for NAFFILENAME in $FILES;
do

	if [[ $NAFFILENAME == NAF* ]]
	then
		EKPFILENAME=$(echo $NAFFILENAME | sed 's/NAF/EKP/')
		sed 's/\/nfs\/dust\/cms\/user\/rfriese/\/storage\/a\/friese/' ../data/Samples/$NAFFILENAME > "../data/Samples/${EKPFILENAME}_tmp"
	#	echo $EKPFILENAME
	#	echo $(sed 's/NAF/EKP/' ../data/Samples/${EKPFILENAME})
		sed 's/NAF/EKP/' ../data/Samples/${EKPFILENAME}_tmp > ../data/Samples/${EKPFILENAME}
	fi
done
	rm ../data/Samples/EKP*_tmp
