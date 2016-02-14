
#pragma once

#include "Artus/Filter/interface/CutFilterBase.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"



/** Filter checking for the existance of at least one valid di-tau pair.
 */
class ValidDiTauPairCandidatesFilter: public CutRangeFilterBase<KappaTypes> {
public:
	
	typedef typename std::function<double(KappaEvent const&, KappaProduct const&)> double_extractor_lambda;
	
	virtual std::string GetFilterId() const override;
	virtual void Init(KappaSettings const& settings) override;
};
