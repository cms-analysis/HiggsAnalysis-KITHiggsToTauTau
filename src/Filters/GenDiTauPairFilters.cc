
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/GenDiTauPairFilters.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


std::string GenDiTauPairCandidatesFilter::GetFilterId() const {
	return "GenDiTauPairCandidatesFilter";
}

void GenDiTauPairCandidatesFilter::Init(setting_type const& settings, metadata_type& metadata) {
	CutRangeFilterBase::Init(settings, metadata);
	
	this->m_cuts.push_back(std::pair<double_extractor_lambda, CutRange>(
			[](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
				return static_cast<double>(static_cast<HttProduct const&>(product).m_genDiTauPairCandidates.size());
			},
			CutRange::LowerThresholdCut(1.0)
	));
}


std::string GenDiTauPairAcceptanceFilter::GetFilterId() const {
	return "GenDiTauPairAcceptanceFilter";
}

void GenDiTauPairAcceptanceFilter::Init(setting_type const& settings, metadata_type& metadata) {
	CutRangeFilterBase::Init(settings, metadata);
	
	this->m_cuts.push_back(std::pair<double_extractor_lambda, CutRange>(
			[](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
				return static_cast<double>(static_cast<HttProduct const&>(product).m_genDiTauPairInAcceptance.size());
			},
			CutRange::LowerThresholdCut(1.0)
	));
}
