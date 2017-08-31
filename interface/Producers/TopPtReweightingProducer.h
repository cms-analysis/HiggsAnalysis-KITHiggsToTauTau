
#pragma once

#include "Artus/Core/interface/ProducerBase.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include <boost/regex.hpp>
#include <boost/algorithm/string.hpp>

/**
   \brief TopPtReweightingProducer
   Top Pt reweighting as suggested on:
   https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopPtReweighting
   Config tags:
   - TopPtReweightingStrategy: possible values: Run1, Run2. If something else is defined, then Run2 is taken.
     Both weigths are computed.

*/

class TopPtReweightingProducer: public ProducerBase<HttTypes> {
public:

	std::string GetProducerId() const override;

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
	void Produce( event_type const& event,
			product_type & product,
			setting_type const& settings, metadata_type const& metadata) const override;
private:
	bool m_isTTbar;
	bool m_oldStrategy = false; // old == true: Run1, new == false: Run2
	float ComputeWeight(float top1Pt, float top2Pt, float parameter_a, float parameter_b) const;
};
