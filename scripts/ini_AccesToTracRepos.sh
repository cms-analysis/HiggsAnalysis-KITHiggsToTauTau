#!/bin/bash

wget --no-check-certificate https://pki.pca.dfn.de/kit-ca/pub/cacert/chain.txt

cd $ANALYSIS_BASE/Artus/
git config --local --add http.sslCAinfo $ANALYSIS_BASE/KITHiggsToTauTau/Analysis/scripts/chain.txt
cd $ANALYSIS_BASE/Kappa
git config --local --add http.sslCAinfo $ANALYSIS_BASE/KITHiggsToTauTau/Analysis/scripts/chain.txt
cd $ANALYSIS_BASE/KappaTools
git config --local --add http.sslCAinfo $ANALYSIS_BASE/KITHiggsToTauTau/Analysis/scripts/chain.txt

git config --global --unset http.sslcainfo
