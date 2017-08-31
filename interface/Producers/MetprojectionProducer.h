

#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/SvfitTools.h"

/**
   \brief GlobalProducer for MET studies
   
*/
class MetprojectionProducer: public ProducerBase<HttTypes> {
private:
	bool m_isData;
public:

	virtual std::string GetProducerId() const override {
		return "MetprojectionProducer";
	}

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
	virtual void Produce(event_type const& event, product_type& product, setting_type const& settings, metadata_type const& metadata) const override;
};

