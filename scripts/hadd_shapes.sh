#!/bin/bash

# script to properly 'hadd' the shapes needed to write the filled 
# datacards with the Morphing script.
cd $1
rm htt_*.inputs-sm-13TeV-2D.root
hadd.py -t htt_em.inputs-sm-13TeV-2D.root -n 1000 htt_em_*.root
hadd.py -t htt_et.inputs-sm-13TeV-2D.root -n 1000 htt_et_*.root
hadd.py -t htt_mt.inputs-sm-13TeV-2D.root -n 1000 htt_mt_*.root
hadd.py -t htt_tt.inputs-sm-13TeV-2D.root -n 1000 htt_tt_*.root
hadd.py -t htt_ttbar.inputs-sm-13TeV-2D.root -n 1000 htt_ttbar_*.root
cd $CMSSW_BASE/src
