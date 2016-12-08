
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "Artus/KappaAnalysis/interface/KappaProducerBase.h"
#include "HTTutilities/Jet2TauFakes/interface/FakeFactor.h"
#include <boost/regex.hpp>

#if ROOT_VERSION_CODE < ROOT_VERSION(6,0,0)
#include <TROOT.h>
#endif

/**
   \brief JetToTauFakesProducer
   Config tags:
   
    Run this producer after the Run2DecayModeProducer

*/

class JetToTauFakesProducer : public ProducerBase<HttTypes> {
public:

    typedef typename HttTypes::event_type event_type;
    typedef typename HttTypes::product_type product_type;
    typedef typename HttTypes::setting_type setting_type;
    
    std::string GetProducerId() const override;

    virtual void Init(setting_type const& settings) override
 	{
	
         #if ROOT_VERSION_CODE < ROOT_VERSION(6,0,0)
         gROOT->ProcessLine("#include <map>");
         #endif

         ProducerBase<HttTypes>::Init(settings);
         TDirectory *savedir(gDirectory);
         TFile *savefile(gFile);

	 m_applyFakeFactors = false;
	 m_isSample = boost::regex_search(settings.GetNickname(), boost::regex("^(Single|MuonEG|Tau|Double|DY|TT|ST|WW|WZ|ZZ|VV)", boost::regex::icase | boost::regex::extended));
	 m_isET = boost::regex_search(settings.GetRootFileFolder(), boost::regex("et_jecUncNom_tauEsNom", boost::regex::icase | boost::regex::extended));
	 m_isMT = boost::regex_search(settings.GetRootFileFolder(), boost::regex("mt_jecUncNom_tauEsNom", boost::regex::icase | boost::regex::extended));

	 TFile::SetCacheFileDir(("/tmp/" + settings.GetUser() +"/").c_str());

	//ET files
	if(m_isSample && m_isET)
	{
	 ff_file_et_incl = TFile::Open("dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/et/incl/fakeFactors_201610_test.root", "CACHEREAD", "dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/et/incl/fakeFactors_201610_test.root");
	 ff_file_et_incl_SS = TFile::Open("dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/et/incl_SS/fakeFactors_201610_test.root", "CACHEREAD", "dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/et/incl_SS/fakeFactors_201610_test.root");
	 ff_file_et_0jet = TFile::Open("dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/et/_0jet/fakeFactors_201610_test.root", "CACHEREAD", "dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/et/_0jet/fakeFactors_201610_test.root");
	 ff_file_et_1jet = TFile::Open("dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/et/_1jet/fakeFactors_201610_test.root", "CACHEREAD", "dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/et/_1jet/fakeFactors_201610_test.root");
	 ff_file_et_1jetZ050 = TFile::Open("dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/et/_1jetZ050/fakeFactors_201610_test.root", "CACHEREAD", "dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/et/_1jetZ050/fakeFactors_201610_test.root");
	 ff_file_et_1jetZ50100 = TFile::Open("dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/et/_1jetZ50100/fakeFactors_201610_test.root", "CACHEREAD", "dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/et/_1jetZ50100/fakeFactors_201610_test.root");
	 ff_file_et_1jetZ100 = TFile::Open("dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/et/_1jetZ100/fakeFactors_201610_test.root", "CACHEREAD", "dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/et/_1jetZ100/fakeFactors_201610_test.root");
	 ff_file_et_2jet = TFile::Open("dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/et/_2jet/fakeFactors_201610_test.root", "CACHEREAD", "dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/et/_2jet/fakeFactors_201610_test.root");
	 ff_file_et_2jetVBF = TFile::Open("dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/et/_2jetVBF/fakeFactors_201610_test.root", "CACHEREAD", "dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/et/_2jetVBF/fakeFactors_201610_test.root");
	 ff_file_et_anyb = TFile::Open("dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/et/_anyb/fakeFactors_201610_test.root", "CACHEREAD", "dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/et/_anyb/fakeFactors_201610_test.root");
	 m_applyFakeFactors = true;
	}

	 // MT files
	if(m_isSample && m_isMT)
	{
	 ff_file_mt_incl = TFile::Open("dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/mt/incl/fakeFactors_201610_test.root", "CACHEREAD", "dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/mt/incl/fakeFactors_201610_test.root");
	 ff_file_mt_incl_SS = TFile::Open("dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/mt/incl_SS/fakeFactors_201610_test.root", "CACHEREAD", "dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/mt/incl_SS/fakeFactors_201610_test.root");
	 ff_file_mt_0jet = TFile::Open("dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/mt/_0jet/fakeFactors_201610_test.root", "CACHEREAD", "dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/mt/_0jet/fakeFactors_201610_test.root");
	 ff_file_mt_1jet = TFile::Open("dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/mt/_1jet/fakeFactors_201610_test.root", "CACHEREAD", "dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/mt/_1jet/fakeFactors_201610_test.root");
	 ff_file_mt_1jetZ050 = TFile::Open("dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/mt/_1jetZ050/fakeFactors_201610_test.root", "CACHEREAD", "dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/mt/_1jetZ050/fakeFactors_201610_test.root");
	 ff_file_mt_1jetZ50100 = TFile::Open("dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/mt/_1jetZ50100/fakeFactors_201610_test.root", "CACHEREAD", "dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/mt/_1jetZ50100/fakeFactors_201610_test.root");
	 ff_file_mt_1jetZ100 = TFile::Open("dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/mt/_1jetZ100/fakeFactors_201610_test.root", "CACHEREAD", "dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/mt/_1jetZ100/fakeFactors_201610_test.root");
	 ff_file_mt_2jet = TFile::Open("dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/mt/_2jet/fakeFactors_201610_test.root", "CACHEREAD", "dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/mt/_2jet/fakeFactors_201610_test.root");
	 ff_file_mt_2jetVBF = TFile::Open("dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/mt/_2jetVBF/fakeFactors_201610_test.root", "CACHEREAD", "dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/mt/_2jetVBF/fakeFactors_201610_test.root");
	 ff_file_mt_anyb = TFile::Open("dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/mt/_anyb/fakeFactors_201610_test.root", "CACHEREAD", "dcap://dcache-cms-dcap.desy.de//pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/artus/fakeFactorWeights/mt/_anyb/fakeFactors_201610_test.root");
	 m_applyFakeFactors = true;
	}

         gDirectory = savedir;
         gFile = savefile;
 	
	}


    void Produce(event_type const& event, product_type& product,
                 setting_type const& settings) const override;
private:

    bool m_isSample; 
    bool m_isET; 
    bool m_isMT; 
    bool m_applyFakeFactors;

    //ET
    TFile* ff_file_et_incl;
    TFile* ff_file_et_incl_SS;
    TFile* ff_file_et_0jet;
    TFile* ff_file_et_1jet;
    TFile* ff_file_et_1jetZ050;
    TFile* ff_file_et_1jetZ50100;
    TFile* ff_file_et_1jetZ100;
    TFile* ff_file_et_2jet;
    TFile* ff_file_et_2jetVBF;
    TFile* ff_file_et_anyb;
    
    //MT
    TFile* ff_file_mt_incl;
    TFile* ff_file_mt_incl_SS;
    TFile* ff_file_mt_0jet;
    TFile* ff_file_mt_1jet;
    TFile* ff_file_mt_1jetZ050;
    TFile* ff_file_mt_1jetZ50100;
    TFile* ff_file_mt_1jetZ100;
    TFile* ff_file_mt_2jet;
    TFile* ff_file_mt_2jetVBF;
    TFile* ff_file_mt_anyb;
};
