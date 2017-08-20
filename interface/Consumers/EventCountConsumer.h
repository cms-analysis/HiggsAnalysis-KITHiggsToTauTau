
#pragma once

#include "Artus/Core/interface/ConsumerBase.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

#include "TH1.h"


class EventCountConsumer: public ConsumerBase<HttTypes>
{

public:

	virtual void Init(setting_type const& settings, metadata_type& metadata);
	virtual std::string GetConsumerId() const override;
	virtual void ProcessEvent(event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata, FilterResult & result) override;
	
	virtual void Finish(setting_type const& settings, metadata_type const& metadata);
	unsigned int currentLumi;

protected:
	TH1I* m_totalEvents;
	TH1I* m_filteredEvents;
};

