
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/ValidDiTauPairCandidatesFilter.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


std::string ValidDiTauPairCandidatesFilter::GetFilterId() const {
	return "ValidDiTauPairCandidatesFilter";
}

void ValidDiTauPairCandidatesFilter::Init(setting_type const& settings, metadata_type& metadata) {
	CutRangeFilterBase::Init(settings, metadata);
	
	this->m_cuts.push_back(std::pair<double_extractor_lambda, CutRange>(
			[](event_type const& event, product_type const& product) {
				return static_cast<double>(static_cast<HttProduct const&>(product).m_validDiTauPairCandidates.size());
			},
			CutRange::LowerThresholdCut(1.0)
	));
}

