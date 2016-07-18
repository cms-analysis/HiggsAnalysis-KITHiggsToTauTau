
#pragma once

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
		TDirectory *savedir(gDirectory);
		TFile *savefile(gFile);
		m_qcdWeights = new QCDModelForEMu("HTT-utilities/QCDModelingEMu/data/QCD_weight_emu.root"); 
		gDirectory = savedir;
		gFile = savefile;
	}

	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings) const override;
private:
	QCDModelForEMu* m_qcdWeights=0;

};
