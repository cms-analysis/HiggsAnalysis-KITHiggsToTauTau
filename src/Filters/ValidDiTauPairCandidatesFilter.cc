
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/ValidDiTauPairCandidatesFilter.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


std::string ValidDiTauPairCandidatesFilter::GetFilterId() const {
	return "ValidDiTauPairCandidatesFilter";
}

void ValidDiTauPairCandidatesFilter::Init(KappaSettings const& settings) {
	CutRangeFilterBase::Init(settings);
	
	this->m_cuts.push_back(std::pair<double_extractor_lambda, CutRange>(
			[](KappaEvent const& event, KappaProduct const& product) {
				return static_cast<double>(static_cast<HttProduct const&>(product).m_validDiTauPairCandidates.size());
			},
			CutRange::LowerThresholdCut(1.0)
	));
}

