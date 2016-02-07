
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/GenDiTauPairFilters.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


std::string GenDiTauPairCandidatesFilter::GetFilterId() const {
	return "GenDiTauPairCandidatesFilter";
}

void GenDiTauPairCandidatesFilter::Init(KappaSettings const& settings) {
	CutRangeFilterBase::Init(settings);
	
	this->m_cuts.push_back(std::pair<double_extractor_lambda, CutRange>(
			[](KappaEvent const& event, KappaProduct const& product) {
				return static_cast<double>(static_cast<HttProduct const&>(product).m_genDiTauPairCandidates.size());
			},
			CutRange::LowerThresholdCut(1.0)
	));
}


std::string GenDiTauPairAcceptanceFilter::GetFilterId() const {
	return "GenDiTauPairAcceptanceFilter";
}

void GenDiTauPairAcceptanceFilter::Init(KappaSettings const& settings) {
	CutRangeFilterBase::Init(settings);
	
	this->m_cuts.push_back(std::pair<double_extractor_lambda, CutRange>(
			[](KappaEvent const& event, KappaProduct const& product) {
				return static_cast<double>(static_cast<HttProduct const&>(product).m_genDiTauPairInAcceptance.size());
			},
			CutRange::LowerThresholdCut(1.0)
	));
}
