
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"
#include "Artus/Consumer/interface/ValueModifier.h"

#include "Artus/Consumer/interface/DrawHist1dConsumer.h"
#include "Artus/Consumer/interface/ProfileConsumerBase.h"

#include "HttTypes.h"

#include "HttPipelineSettings.h"
#include "HttEvent.h"
#include "HttProduct.h"

#include "PreselectionFilter.h"
#include "HttNtupleConsumer.h"

class HttPipelineInitializer: public PipelineInitilizerBase<HttTypes> {
public:

	virtual void InitPipeline(HttPipeline * pLine,  HttPipelineSettings const& pset) const ARTUS_CPP11_OVERRIDE
			{

		BOOST_FOREACH(std::string filterId, pset.GetFilter())
		{
			if(filterId == PreselectionFilter().GetFilterId()) {
				pLine->AddFilter(new PreselectionFilter());
			}
			else {
				LOG_FATAL("Filter \"" << filterId << "\" not found.");
			}
		}

		BOOST_FOREACH(std::string consumerId, pset.GetConsumer())
		{
			if(consumerId == HttNtupleConsumer().GetConsumerId()) {
				pLine->AddConsumer(new HttNtupleConsumer);
			}
			else {
				LOG_FATAL("Consumer \"" << consumerId << "\" not found.");
			}
		}

	}
};
