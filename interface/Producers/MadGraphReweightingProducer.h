
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "CMSAachen3B/MadGraphReweighting/interface/MadGraphTools.h"


class MadGraphReweightingProducer: public ProducerBase<HttTypes>
{
public:

	virtual std::string GetProducerId() const override;

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type& product,
						 setting_type const& settings, metadata_type const& metadata) const override;

private:
	std::map<int, MadGraphTools*> m_madGraphTools;
	
	static int GetMixingAngleKey(float mixingAngleOverPiHalf);
	static std::string GetLabelForWeightsMap(float mixingAngleOverPiHalf);
};
