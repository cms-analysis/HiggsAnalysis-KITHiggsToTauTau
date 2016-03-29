
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MetSelectors.h"


MetSelector::MetSelector() :
	MetSelectorBase<KMET>(&HttTypes::event_type::m_met, nullptr)
{
}


std::string MetSelector::GetProducerId() const
{
	return "MetSelector";
}


MetSelectorPuppi::MetSelectorPuppi() :
	MetSelectorBase<KMET>(&HttTypes::event_type::m_puppiMet, nullptr)
{
}

void MetSelectorPuppi::Produce(event_type const& event, product_type & product, 
                     setting_type const& settings) const
{
	// temporary fix while PUPPI doesn't  have a significance matrix
	MetSelectorBase::Produce(event, product, settings);
	product.m_metUncorr->significance = event.m_met->significance;
}

std::string MetSelectorPuppi::GetProducerId() const
{
	return "MetSelectorPuppi";
}

MvaMetTTSelector::MvaMetTTSelector() :
	MetSelectorBase(&HttTypes::event_type::m_mvaMetTT, &HttTypes::event_type::m_mvaMetsTT)
{
}

std::string MvaMetTTSelector::GetProducerId() const
{
	return "MvaMetTTSelector";
}


MvaMetMTSelector::MvaMetMTSelector() :
	MetSelectorBase(&HttTypes::event_type::m_mvaMetMT, &HttTypes::event_type::m_mvaMetsMT)
{
}

std::string MvaMetMTSelector::GetProducerId() const
{
	return "MvaMetMTSelector";
}


MvaMetETSelector::MvaMetETSelector() :
	MetSelectorBase(&HttTypes::event_type::m_mvaMetET, &HttTypes::event_type::m_mvaMetsET)
{
}

std::string MvaMetETSelector::GetProducerId() const
{
	return "MvaMetETSelector";
}


MvaMetEMSelector::MvaMetEMSelector() :
	MetSelectorBase(&HttTypes::event_type::m_mvaMetEM, &HttTypes::event_type::m_mvaMetsEM)
{
}

std::string MvaMetEMSelector::GetProducerId() const
{
	return "MvaMetEMSelector";
}

MvaMetSelector::MvaMetSelector() :
	MetSelectorBase(&HttTypes::event_type::m_mvaMet, &HttTypes::event_type::m_mvaMets)
{
}

std::string MvaMetSelector::GetProducerId() const
{
	return "MvaMetSelector";
}
