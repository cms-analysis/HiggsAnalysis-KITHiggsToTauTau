declare -A arr

$input_files
			
if [ \"x$2\" != \"x\" ]; then
	pushd $cwd
	SCRAM_ARCH=slc6_amd64_gcc493
	source /cvmfs/cms.cern.ch/cmsset_default.sh
	eval `scramv1 runtime -sh`
	ComputeSvfit -i ${arr[$1,0]} -o SvfitCache.root $args
else
	./ComputeSvfit -i ${arr[$1,0]} -o $(basename ${arr[$1,0]}) $args
	tar -cf SvfitCache.tar $(basename ${arr[$1,0]})
fi
