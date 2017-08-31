
#pragma once

#include "Artus/Filter/interface/CutFilterBase.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"



/** Filter checking for the existance of at least one valid di-tau pair.
 */
class ValidDiTauPairCandidatesFilter: public CutRangeFilterBase<HttTypes> {
public:
	
	typedef typename std::function<double(event_type const&, product_type const&)> double_extractor_lambda;
	
	virtual std::string GetFilterId() const override;
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
};
