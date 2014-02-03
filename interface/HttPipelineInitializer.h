
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"

#include "HttTypes.h"

#include "HttPipelineSettings.h"
#include "HttEvent.h"
#include "HttProduct.h"

#include "Filters/PreselectionFilter.h"
#include "Consumers/HttNtupleConsumer.h"

class HttPipelineInitializer: public PipelineInitilizerBase<HttTypes> {
public:

	virtual void InitPipeline(HttPipeline * pLine,  HttPipelineSettings const& pset) const ARTUS_CPP11_OVERRIDE {

		BOOST_FOREACH(std::string filterId, pset.GetFilters())
		{
			if(filterId == PreselectionFilter().GetFilterId()) {
				pLine->AddFilter(new PreselectionFilter());
			}
			else {
				LOG_FATAL("Filter \"" << filterId << "\" not found.");
			}
		}

		BOOST_FOREACH(std::string producerId, pset.GetProducers())
		{
			
		}

		BOOST_FOREACH(std::string consumerId, pset.GetConsumers())
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
