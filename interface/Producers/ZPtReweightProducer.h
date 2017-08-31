
#pragma once

#include <TH2.h>
#include "Artus/Core/interface/ProducerBase.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include <boost/regex.hpp>

/**
   \brief ZPtReweightProducer
   Config tags:
   - Fill me with something meaningful

*/

class ZPtReweightProducer: public ProducerBase<HttTypes> {
public:

	virtual ~ZPtReweightProducer();

	std::string GetProducerId() const;

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings, metadata_type const& metadata) const override;
private:
	TH2D* m_zPtHist = nullptr;
	bool m_applyReweighting;
};
