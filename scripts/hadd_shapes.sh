#!/bin/bash

# script to properly 'hadd' the shapes needed to write the filled 
# datacards with the Morphing script.
cd $1
cd $2
rm htt_*.inputs-sm-13TeV-2D.root
hadd.py -t htt_$3.inputs-sm-13TeV-2D.root -n 1000 htt_$3_*.root
cd $CMSSW_BASE/src
