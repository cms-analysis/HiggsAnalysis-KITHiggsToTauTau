
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/HttObjectsCutFilters.h"

std::string MetLowerPtCutsFilter::GetFilterId() const {
	return "MetLowerPtCutsFilter";
}

void MetLowerPtCutsFilter::Init(setting_type const& settings, metadata_type& metadata)
{
	CutRangeFilterBase<HttTypes>::Init(settings, metadata);
	
	this->m_cuts.push_back(std::pair<double_extractor_lambda, CutRange>(
		[this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) -> double {
			return (product.m_met.p4.Pt());
			},
			CutRange::LowerThresholdCut(settings.GetMetLowerPtCuts())
		));
}


std::string MetUpperPtCutsFilter::GetFilterId() const {
	return "MetUpperPtCutsFilter";
}

void MetUpperPtCutsFilter::Init(setting_type const& settings, metadata_type& metadata)
{
	CutRangeFilterBase<HttTypes>::Init(settings, metadata);
	
	this->m_cuts.push_back(std::pair<double_extractor_lambda, CutRange>(
		[this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) -> double {
			return (product.m_met.p4.Pt());
			},
			CutRange::UpperThresholdCut(settings.GetMetUpperPtCuts())
		));
}
