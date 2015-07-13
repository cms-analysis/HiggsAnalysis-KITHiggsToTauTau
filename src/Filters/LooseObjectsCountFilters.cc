
#include "Artus/KappaAnalysis/interface/KappaTypes.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/LooseObjectsCountFilters.h"


void LooseElectronsCountFilter::Init(setting_type const& settings) {
	CutRangeFilterBase<HttTypes>::Init(settings);
	
	this->m_cuts.push_back(std::pair<double_extractor_lambda, CutRange>(
			[](KappaEvent const& event, KappaProduct const& product) {
				return (static_cast<HttProduct const&>(product)).m_validLooseElectrons.size();
			},
			CutRange::EqualsCut(double(settings.GetNLooseElectrons()))
	));
}

void LooseMuonsCountFilter::Init(setting_type const& settings) {
	CutRangeFilterBase<HttTypes>::Init(settings);
	
	this->m_cuts.push_back(std::pair<double_extractor_lambda, CutRange>(
			[](KappaEvent const& event, KappaProduct const& product) {
				return (static_cast<HttProduct const&>(product)).m_validLooseMuons.size();
			},
			CutRange::EqualsCut(double(settings.GetNLooseMuons()))
	));
}

