#!/bin/bash

echo "Run run-cvmfs.sh"
/etc/cvmfs/run-cvmfs.sh

if ! which wget; then
	echo "wget not found. Will install it.";
	yum install wget -y
	if ! which wget; then
		echo "Could not install wget."
		exit 1
	fi
fi

echo "Download and execute checkout script"
mkdir -p /home/build && cd /home/build
curl -O https://raw.githubusercontent.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/${TRAVIS_BRANCH}/scripts/checkout_packages.sh
chmod +x checkout_packages.sh
set -x
. ./checkout_packages.sh -b ${TRAVIS_BRANCH} -g 'greyxray' -e 'greyxray@gmail.com' -n 'test' || {
	echo "checkout_packages.sh could not be executed"
	exit 1
}

# TODO: find way to access files on dCache
#cd $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/ && scram b unittests || {
#	echo "run tests failed"
#	exit 1
#}

echo "Success!"
