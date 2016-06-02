
#pragma once

#include <TH2.h>
//#include "Artus/KappaAnalysis/interface/KappaProducerBase.h"
#include "Artus/Core/interface/ProducerBase.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HTT-utilities/QCDModelingEMu/interface/QCDModelForEMu.h"

/**
   \brief EmuQcdWeightProducer
   Config tags:
   - Fill me with something meaningful

*/

//class EmuQcdWeightProducer : public KappaProducerBase {
class EmuQcdWeightProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	std::string GetProducerId() const;

	virtual void Init(setting_type const& settings) override
	{
		ProducerBase<HttTypes>::Init(settings);
        TString cmsswBase = TString( getenv ("CMSSW_BASE") );
        m_qcdWeights = new QCDModelForEMu(cmsswBase+"/src/HTT-utilities/QCDModelingEMu/data/QCD_weight_emu.root"); 
	}

	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings) const override;
private:
    TH2D* m_zPtHist = 0;
    QCDModelForEMu* m_qcdWeights=0;

};
