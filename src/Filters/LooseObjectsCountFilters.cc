
#include "Artus/KappaAnalysis/interface/KappaTypes.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/LooseObjectsCountFilters.h"


void LooseElectronsCountFilter::Init(setting_type const& settings, metadata_type& metadata) {
	CutRangeFilterBase<HttTypes>::Init(settings, metadata);
	
	this->m_cuts.push_back(std::pair<double_extractor_lambda, CutRange>(
			[](event_type const& event, product_type const& product) {
				return (static_cast<HttProduct const&>(product)).m_validLooseElectrons.size();
			},
			CutRange::EqualsCut(double(settings.GetNLooseElectrons()))
	));
}

void LooseMuonsCountFilter::Init(setting_type const& settings, metadata_type& metadata) {
	CutRangeFilterBase<HttTypes>::Init(settings, metadata);
	
	this->m_cuts.push_back(std::pair<double_extractor_lambda, CutRange>(
			[](event_type const& event, product_type const& product) {
				return (static_cast<HttProduct const&>(product)).m_validLooseMuons.size();
			},
			CutRange::EqualsCut(double(settings.GetNLooseMuons()))
	));
}

