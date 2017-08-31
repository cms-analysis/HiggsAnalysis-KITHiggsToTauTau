
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MetSelectors.h"


MetSelector::MetSelector() :
	MetSelectorBase<KMET>(&event_type::m_met, nullptr)
{
}


std::string MetSelector::GetProducerId() const
{
	return "MetSelector";
}


MetSelectorPuppi::MetSelectorPuppi() :
	MetSelectorBase<KMET>(&event_type::m_puppiMet, nullptr)
{
}

void MetSelectorPuppi::Produce(event_type const& event, product_type & product, 
                     setting_type const& settings, metadata_type const& metadata) const
{
	// temporary fix while PUPPI doesn't  have a significance matrix
	MetSelectorBase::Produce(event, product, settings, metadata);
	product.m_metUncorr->significance = event.m_met->significance;
}

std::string MetSelectorPuppi::GetProducerId() const
{
	return "MetSelectorPuppi";
}

MvaMetTTSelector::MvaMetTTSelector() :
	MetSelectorBase(&event_type::m_mvaMetTT, &event_type::m_mvaMetsTT)
{
}

std::string MvaMetTTSelector::GetProducerId() const
{
	return "MvaMetTTSelector";
}


MvaMetMTSelector::MvaMetMTSelector() :
	MetSelectorBase(&event_type::m_mvaMetMT, &event_type::m_mvaMetsMT)
{
}

std::string MvaMetMTSelector::GetProducerId() const
{
	return "MvaMetMTSelector";
}


MvaMetETSelector::MvaMetETSelector() :
	MetSelectorBase(&event_type::m_mvaMetET, &event_type::m_mvaMetsET)
{
}

std::string MvaMetETSelector::GetProducerId() const
{
	return "MvaMetETSelector";
}


MvaMetEMSelector::MvaMetEMSelector() :
	MetSelectorBase(&event_type::m_mvaMetEM, &event_type::m_mvaMetsEM)
{
}

std::string MvaMetEMSelector::GetProducerId() const
{
	return "MvaMetEMSelector";
}

MvaMetSelector::MvaMetSelector() :
	MetSelectorBase(&event_type::m_mvaMet, &event_type::m_mvaMets)
{
}

std::string MvaMetSelector::GetProducerId() const
{
	return "MvaMetSelector";
}
