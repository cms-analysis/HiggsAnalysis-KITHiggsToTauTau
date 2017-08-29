#!/bin/bash

echo "Run run-cvmfs.sh"
/etc/cvmfs/run-cvmfs.sh

echo "Download and execute checkout script"
mkdir -p /home/build && cd /home/build
curl -O https://raw.githubusercontent.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/${TRAVIS_BRANCH}/scripts/checkout_packages.sh
chmod +x checkout_packages.sh
set -x
. ./checkout_packages.sh -b ${TRAVIS_BRANCH} -g 'greyxray' -e 'greyxray@gmail.com' -n 'test' || {
    echo "checkout_packages.sh could not be executed"
    exit 1
}

scram b unittests

echo "Success!"
