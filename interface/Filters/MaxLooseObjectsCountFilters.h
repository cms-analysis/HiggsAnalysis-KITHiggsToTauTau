
#pragma once

#include "Artus/Filter/interface/CutFilterBase.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/** Filter checking for the existance of exactly the given number of valid loose electrons.
 *  Required config tag: MaxNLooseElectrons
 */
class MaxLooseElectronsCountFilter: public CutRangeFilterBase<HttTypes> {
public:
	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	typedef typename std::function<double(event_type const&, product_type const&)> double_extractor_lambda;
	
	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE {
		return "max_n_loose_electrons";
	}
	
	virtual void Init(setting_type const& settings) ARTUS_CPP11_OVERRIDE;
};


/** Filter checking for the existance of exactly the given number of valid loose muons.
 *  Required config tag: MaxNLooseMuons
 */
class MaxLooseMuonsCountFilter: public CutRangeFilterBase<HttTypes> {
public:
	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	typedef typename std::function<double(event_type const&, product_type const&)> double_extractor_lambda;
	
	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE {
		return "max_n_loose_muons";
	}
	
	virtual void Init(setting_type const& settings) ARTUS_CPP11_OVERRIDE;
};

