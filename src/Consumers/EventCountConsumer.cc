
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/EventCountConsumer.h"
#include "Artus/Utility/interface/RootFileHelper.h"

void EventCountConsumer::Init(setting_type const& settings, metadata_type& metadata)
{
	ConsumerBase<HttTypes>::Init(settings, metadata);
	
	currentLumi = 0;
	m_totalEvents = new TH1I("totalEvents", "totalEvents", 2, -1, 1);
	m_totalEvents->SetBinContent(1, 0);
	m_totalEvents->SetBinContent(2, 0);
	m_filteredEvents = new TH1I("filteredEvents", "filteredEvents", 2, -1, 1);
	m_filteredEvents->SetBinContent(1, 0);
	m_filteredEvents->SetBinContent(2, 0);
}

std::string EventCountConsumer::GetConsumerId() const
{
	return "EventCountConsumer";
}

void EventCountConsumer::ProcessEvent(event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata, FilterResult & result)
{
	assert(event.m_eventInfo);
	assert(event.m_filterMetadata);
	if(currentLumi != event.m_eventInfo->nLumi)
	{
		currentLumi = event.m_eventInfo->nLumi;
		m_totalEvents->AddBinContent(1, event.m_filterMetadata->nNegEventsTotal);
		m_totalEvents->AddBinContent(2, event.m_filterMetadata->nEventsTotal - event.m_filterMetadata->nNegEventsTotal);
		m_filteredEvents->AddBinContent(1, event.m_filterMetadata->nNegEventsFiltered);
		m_filteredEvents->AddBinContent(2, event.m_filterMetadata->nEventsFiltered - event.m_filterMetadata->nNegEventsTotal);
	}
}

void EventCountConsumer::Finish(setting_type const& settings, metadata_type const& metadata)
{
	RootFileHelper::SafeCd(settings.GetRootOutFile(), "");
	m_totalEvents->Write(m_totalEvents->GetName());
	m_filteredEvents->Write(m_filteredEvents->GetName());
}

