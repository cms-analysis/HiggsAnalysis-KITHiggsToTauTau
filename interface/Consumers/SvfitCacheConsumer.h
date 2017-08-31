
#pragma once

#include <TTree.h>

#include "Artus/Core/interface/ConsumerBase.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/**
 */
class SvfitCacheConsumer: public ConsumerBase<HttTypes> {
public:

	virtual std::string GetConsumerId() const override
	{
		return "SvfitCacheConsumer";
	}

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void ProcessFilteredEvent(event_type const& event, product_type const& product,
	                                  setting_type const& settings, metadata_type const& metadata) override;

	virtual void Finish(setting_type const& settings, metadata_type const& metadata) override;


private:
	TTree* m_svfitCacheTree = 0;
	bool m_svfitCacheTreeInitialised = false;
	bool m_firstSvfitCacheFile = true;
	int m_fileIndex = 0;

};


