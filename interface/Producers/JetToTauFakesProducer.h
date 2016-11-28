
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
         TString cmsswBase = TString( getenv ("CMSSW_BASE") );

	 m_applyFakeFactors = false;
	 m_isSample = boost::regex_search(settings.GetNickname(), boost::regex("^(Single|MuonEG|Tau|Double|DY|TT|ST|WW|WZ|ZZ|VV)", boost::regex::icase | boost::regex::extended));
	 m_isET = boost::regex_search(settings.GetRootFileFolder(), boost::regex("et_jecUncNom_tauEsNom", boost::regex::icase | boost::regex::extended));
	 m_isMT = boost::regex_search(settings.GetRootFileFolder(), boost::regex("mt_jecUncNom_tauEsNom", boost::regex::icase | boost::regex::extended));

	//ET files
	if(m_isSample && m_isET)
	{
	 ff_file_et_incl = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_201610_test/et/incl/fakeFactors_201610_test.root");
	 ff_file_et_0jet = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_201610_test/et/_0jet/fakeFactors_201610_test.root");
	 ff_file_et_1jet = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_201610_test/et/_1jet/fakeFactors_201610_test.root");
	 ff_file_et_1jetZ050 = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_201610_test/et/_1jetZ050/fakeFactors_201610_test.root");
	 ff_file_et_1jetZ50100 = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_201610_test/et/_1jetZ50100/fakeFactors_201610_test.root");
	 ff_file_et_1jetZ100 = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_201610_test/et/_1jetZ100/fakeFactors_201610_test.root");
	 ff_file_et_2jet = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_201610_test/et/_2jet/fakeFactors_201610_test.root");
	 ff_file_et_2jetVBF = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_201610_test/et/_2jetVBF/fakeFactors_201610_test.root");
	 ff_file_et_anyb = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_201610_test/et/_anyb/fakeFactors_201610_test.root");
	 m_applyFakeFactors = true;
	}

	 // MT files
	if(m_isSample && m_isMT)
	{
	 ff_file_mt_incl = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_201610_test/mt/incl/fakeFactors_201610_test.root");
	 ff_file_mt_0jet = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_201610_test/mt/_0jet/fakeFactors_201610_test.root");
	 ff_file_mt_1jet = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_201610_test/mt/_1jet/fakeFactors_201610_test.root");
	 ff_file_mt_1jetZ050 = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_201610_test/mt/_1jetZ050/fakeFactors_201610_test.root");
	 ff_file_mt_1jetZ50100 = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_201610_test/mt/_1jetZ50100/fakeFactors_201610_test.root");
	 ff_file_mt_1jetZ100 = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_201610_test/mt/_1jetZ100/fakeFactors_201610_test.root");
	 ff_file_mt_2jet = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_201610_test/mt/_2jet/fakeFactors_201610_test.root");
	 ff_file_mt_2jetVBF = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_201610_test/mt/_2jetVBF/fakeFactors_201610_test.root");
	 ff_file_mt_anyb = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_201610_test/mt/_anyb/fakeFactors_201610_test.root");
	 m_applyFakeFactors = true;
	}

	/*
	 // TT files
	 ff_file_tt_incl = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_20160914/tt/incl/fakeFactors_20160914.root");
	 ff_file_tt_0jet = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_20160914/tt/_0jet/fakeFactors_20160914.root");
	 ff_file_tt_1jet = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_20160914/tt/_1jet/fakeFactors_20160914.root");
	 ff_file_tt_1jetZ050 = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_20160914/tt/_1jetZ050/fakeFactors_20160914.root");
	 ff_file_tt_1jetZ50100 = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_20160914/tt/_1jetZ50100/fakeFactors_20160914.root");
	 ff_file_tt_1jetZ100 = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_20160914/tt/_1jetZ100/fakeFactors_20160914.root");
	 ff_file_tt_2jet = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_20160914/tt/_2jet/fakeFactors_20160914.root");
	 ff_file_tt_2jetVBF = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_20160914/tt/_2jetVBF/fakeFactors_20160914.root");
	 ff_file_tt_anyb = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_20160914/tt/_anyb/fakeFactors_20160914.root");
	*/

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
    //if(m_isET)
    //{
    TFile* ff_file_et_incl;
    TFile* ff_file_et_0jet;
    TFile* ff_file_et_1jet;
    TFile* ff_file_et_1jetZ050;
    TFile* ff_file_et_1jetZ50100;
    TFile* ff_file_et_1jetZ100;
    TFile* ff_file_et_2jet;
    TFile* ff_file_et_2jetVBF;
    TFile* ff_file_et_anyb;
    //}
    //MT
    TFile* ff_file_mt_incl;
    TFile* ff_file_mt_0jet;
    TFile* ff_file_mt_1jet;
    TFile* ff_file_mt_1jetZ050;
    TFile* ff_file_mt_1jetZ50100;
    TFile* ff_file_mt_1jetZ100;
    TFile* ff_file_mt_2jet;
    TFile* ff_file_mt_2jetVBF;
    TFile* ff_file_mt_anyb;
/*
    //TT
    TFile* ff_file_tt_incl;
    TFile* ff_file_tt_0jet;
    TFile* ff_file_tt_1jet;
    TFile* ff_file_tt_1jetZ050;
    TFile* ff_file_tt_1jetZ50100;
    TFile* ff_file_tt_1jetZ100;
    TFile* ff_file_tt_2jet;
    TFile* ff_file_tt_2jetVBF;
    TFile* ff_file_tt_anyb;
*/
};
