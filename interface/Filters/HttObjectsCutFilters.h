
#include "Artus/Filter/interface/CutFilterBase.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

/** MET Pt Filter
 */
class MetLowerPtCutsFilter: public CutRangeFilterBase<HttTypes> {
public:
	
	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE;
	
	MetLowerPtCutsFilter() : CutRangeFilterBase<HttTypes>() {}
	
	virtual void Init(HttSettings const& settings) ARTUS_CPP11_OVERRIDE;
};


class MetUpperPtCutsFilter: public CutRangeFilterBase<HttTypes> {
public:
	
	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE;
	
	MetUpperPtCutsFilter() : CutRangeFilterBase<HttTypes>() {}
	
	virtual void Init(HttSettings const& settings) ARTUS_CPP11_OVERRIDE;
};
