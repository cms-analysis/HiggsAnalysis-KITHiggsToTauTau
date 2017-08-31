
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

	std::string GetProducerId() const;

	virtual void Init(setting_type const& settings, metadata_type& metadata) override
	{
		ProducerBase<HttTypes>::Init(settings, metadata);
		TDirectory *savedir(gDirectory);
		TFile *savefile(gFile);
		m_qcdWeights = new QCDModelForEMu("HTT-utilities/QCDModelingEMu/data/QCD_weight_emu.root"); 
		gDirectory = savedir;
		gFile = savefile;
	}

	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings, metadata_type const& metadata) const override;
private:
	QCDModelForEMu* m_qcdWeights=0;

};
