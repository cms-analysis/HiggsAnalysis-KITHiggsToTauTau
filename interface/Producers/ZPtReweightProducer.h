
#pragma once

#include <TH2.h>
//#include "Artus/KappaAnalysis/interface/KappaProducerBase.h"
#include "Artus/Core/interface/ProducerBase.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include <boost/regex.hpp>

/**
   \brief ZPtReweightProducer
   Config tags:
   - Fill me with something meaningful

*/

//class ZPtReweightProducer : public KappaProducerBase {
class ZPtReweightProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	std::string GetProducerId() const;

	virtual void Init(setting_type const& settings) override
	{
		ProducerBase<HttTypes>::Init(settings);
        TDirectory *savedir(gDirectory);
        TFile *savefile(gFile);
        TString cmsswBase = TString( getenv ("CMSSW_BASE") );
        TFile * zPtFile = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/zpt/zpt_weights.root");
        m_zPtHist = (TH2D*)zPtFile->Get("zptmass_histo");
        gDirectory = savedir;
        gFile = savefile;
	}

	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings) const override;
private:
    TH2D* m_zPtHist = 0;

};
