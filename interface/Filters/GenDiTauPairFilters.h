
#pragma once

#include "Artus/Filter/interface/CutFilterBase.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"



/** Filter checking for the existance of at least one generator-level di-tau pair.
 */
class GenDiTauPairCandidatesFilter: public CutRangeFilterBase<HttTypes> {
public:

	typedef typename std::function<double(event_type const&, product_type const&, setting_type const&, metadata_type const&)> double_extractor_lambda;

	virtual std::string GetFilterId() const override;
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
};

/** Filter checking for the existance of at least one generator-level di-tau pair
 *  in the acceptance region of the detector.
 */
class GenDiTauPairAcceptanceFilter: public CutRangeFilterBase<HttTypes> {
public:

	typedef typename std::function<double(event_type const&, product_type const&, setting_type const&, metadata_type const&)> double_extractor_lambda;

	virtual std::string GetFilterId() const override;
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
};
