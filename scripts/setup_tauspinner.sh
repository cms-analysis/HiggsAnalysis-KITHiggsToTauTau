#!/bin/sh
#set -e # exit on errors

rm -rf $CMSSW_BASE/src/TauSpinner
mkdir $CMSSW_BASE/src/TauSpinner

cd $CMSSW_BASE/src/TauSpinner
wget http://lcgapp.cern.ch/project/simu/HepMC/download/HepMC-2.06.05.tar.gz
tar -xzvf HepMC-2.06.05.tar.gz
rm HepMC-2.06.05.tar.gz
mkdir -p $CMSSW_BASE/src/TauSpinner/hepmc/build
mkdir -p $CMSSW_BASE/src/TauSpinner/hepmc/install

cd $CMSSW_BASE/src/TauSpinner
wget http://www.hepforge.org/archive/lhapdf/lhapdf-5.9.1.tar.gz

cd $CMSSW_BASE/src/TauSpinner
wget http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/pythia8/pythia8-176-src.tgz 
tar -xzvf pythia8-176-src.tgz
rm pythia8-176-src.tgz

cd $CMSSW_BASE/src/TauSpinner
#wget http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/tauola++/tauola++-1.1.5-src.tgz
#tar -xzvf tauola++-1.1.5-src.tgz
#rm tauola++-1.1.5-src.tgz
#wget http://tauolapp.web.cern.ch/tauolapp/resources/TAUOLA.1.1.5/TAUOLA.1.1.5-LHC.tar.gz
#tar -xzvf TAUOLA.1.1.5-LHC.tar.gz
#rm TAUOLA.1.1.5-LHC.tar.gz
wget http://tauolapp.web.cern.ch/tauolapp/resources/TAUOLA.1.1.6b/TAUOLA.1.1.6b-LHC.tar.gz
tar -xzvf TAUOLA.1.1.6b-LHC.tar.gz
rm TAUOLA.1.1.6b-LHC.tar.gz

cd $CMSSW_BASE/src/TauSpinner
sed -ie "s@SWSQ=0.23147@SWSQ=0.22224@g" $CMSSW_BASE/src/TauSpinner/TAUOLA/src/tauolaFortranInterfaces/tauola_extras.f
wget https://raw.githubusercontent.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/master/data/Make.TauSpinner.txt
#cp $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/Make.TauSpinner.txt ./
make -j 8 -f Make.TauSpinner.txt

#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CMSSW_BASE/src//TauSpiner/tauola++/1.1.5/lib/
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CMSSW_BASE/src//TauSpiner/pythia8/176/lib/
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CMSSW_BASE/src//TauSpiner/lhapdf/lib/
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CMSSW_BASE/src//TauSpiner/hepmc/install/lib/
