
#pragma once

#include <TTree.h>

#include "Artus/Core/interface/ConsumerBase.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/**
 */
class SvfitCacheConsumer: public ConsumerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetConsumerId() const override
	{
		return "SvfitCacheConsumer";
	}

	virtual void Init(setting_type const& settings) override;

	virtual void ProcessFilteredEvent(event_type const& event, product_type const& product,
	                                  setting_type const& settings) override;

	virtual void Finish(setting_type const& settings) override;


private:
	TTree* m_svfitCacheTree = 0;
	bool m_svfitCacheTreeInitialised = false;
	int fileindex = 0;

};


