
#include "Artus/KappaAnalysis/interface/KappaTypes.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/MaxLooseObjectsCountFilters.h"


void MaxLooseElectronsCountFilter::Init(setting_type const& settings, metadata_type& metadata) {
	CutRangeFilterBase<HttTypes>::Init(settings, metadata);
	
	this->m_cuts.push_back(std::pair<double_extractor_lambda, CutRange>(
			[](event_type const& event, product_type const& product) {
				return (static_cast<HttProduct const&>(product)).m_validLooseElectrons.size();
			},
			CutRange::UpperThresholdCut(double(settings.GetMaxNLooseElectrons()))
	));
}

void MaxLooseMuonsCountFilter::Init(setting_type const& settings, metadata_type& metadata) {
	CutRangeFilterBase<HttTypes>::Init(settings, metadata);
	
	this->m_cuts.push_back(std::pair<double_extractor_lambda, CutRange>(
			[](event_type const& event, product_type const& product) {
				return (static_cast<HttProduct const&>(product)).m_validLooseMuons.size();
			},
			CutRange::UpperThresholdCut(double(settings.GetMaxNLooseMuons()))
	));
}

