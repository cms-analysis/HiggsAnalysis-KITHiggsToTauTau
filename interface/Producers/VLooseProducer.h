
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "Artus/KappaAnalysis/interface/KappaProducerBase.h"
#include <boost/regex.hpp>
#include <TGraph.h>
#include <TFormula.h>

#if ROOT_VERSION_CODE < ROOT_VERSION(6,0,0)
#include <TROOT.h>
#endif

/**
   \brief VLoose MVA Isolation Discriminator Producer
   Config tags:
   
    Run this producer after the Run2DecayModeProducer

*/

class VLooseProducer : public ProducerBase<HttTypes> {
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

	 m_isSample = boost::regex_search(settings.GetNickname(), boost::regex("^(Single|MuonEG|Tau|Double|DY|TT|ST|WW|WZ|ZZ|VV)", boost::regex::icase | boost::regex::extended));

	 if(m_isSample)
	 {
	 tauIdMVArun2DB_wpFile = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/VLooseIsoMVA/wpDiscriminationByIsolationMVARun2v1_DBoldDMwLT.root");
	 DBoldDMwLTvLoose = dynamic_cast<TGraph*>(tauIdMVArun2DB_wpFile->Get("DBoldDMwLTEff90"));
	 DBoldDMwLTLoose = dynamic_cast<TGraph*>(tauIdMVArun2DB_wpFile->Get("DBoldDMwLTEff80"));
	 mvaOutput_normalization_DBoldDMwLT = dynamic_cast<TFormula*>(tauIdMVArun2DB_wpFile->Get("mvaOutput_normalization_DBoldDMwLT"));
	 }

         gDirectory = savedir;
         gFile = savefile;
 	 
	}


    void Produce(event_type const& event, product_type& product,
                 setting_type const& settings) const override;
private:

    bool m_isSample; 

    TFile* tauIdMVArun2DB_wpFile;
    TGraph* DBoldDMwLTvLoose;
    TGraph* DBoldDMwLTLoose;
    TFormula* mvaOutput_normalization_DBoldDMwLT;
};
