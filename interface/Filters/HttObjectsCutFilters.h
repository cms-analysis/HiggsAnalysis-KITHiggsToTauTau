
#include "Artus/Filter/interface/CutFilterBase.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

/** MET Pt Filter
 */
class MetLowerPtCutsFilter: public CutRangeFilterBase<HttTypes> {
public:
	
	virtual std::string GetFilterId() const override;
	
	MetLowerPtCutsFilter() : CutRangeFilterBase<HttTypes>() {}
	
	virtual void Init(HttSettings const& settings) override;
};


class MetUpperPtCutsFilter: public CutRangeFilterBase<HttTypes> {
public:
	
	virtual std::string GetFilterId() const override;
	
	MetUpperPtCutsFilter() : CutRangeFilterBase<HttTypes>() {}
	
	virtual void Init(HttSettings const& settings) override;
};
