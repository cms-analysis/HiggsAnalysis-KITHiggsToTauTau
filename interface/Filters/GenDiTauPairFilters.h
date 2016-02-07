
#pragma once

#include "Artus/Filter/interface/CutFilterBase.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"



/** Filter checking for the existance of at least one generator-level di-tau pair.
 */
class GenDiTauPairCandidatesFilter: public CutRangeFilterBase<KappaTypes> {
public:
	
	typedef typename std::function<double(KappaEvent const&, KappaProduct const&)> double_extractor_lambda;
	
	virtual std::string GetFilterId() const override;
	virtual void Init(KappaSettings const& settings) override;
};

/** Filter checking for the existance of at least one generator-level di-tau pair
 *  in the acceptance region of the detector.
 */
class GenDiTauPairAcceptanceFilter: public CutRangeFilterBase<KappaTypes> {
public:
	
	typedef typename std::function<double(KappaEvent const&, KappaProduct const&)> double_extractor_lambda;
	
	virtual std::string GetFilterId() const override;
	virtual void Init(KappaSettings const& settings) override;
};
