
#pragma once

#include "Artus/KappaAnalysis/interface/KappaPipelineRunner.h"

#include "HttTypes.h"

#include "Producers/DecayChannelProducer.h"


class HttPipelineRunner : public KappaPipelineRunner<HttTypes, HttPipeline, HttGlobalProducerBase> {

public:

	HttPipelineRunner(HttGlobalSettings const& globalSettings) :
		KappaPipelineRunner(globalSettings)
	{

	}
	
	virtual void AddGlobalProducersById() ARTUS_CPP11_OVERRIDE {

		// call upper class function
		// TODO: current solution destroys order of producers
		KappaPipelineRunner::AddGlobalProducersById();
	
		BOOST_FOREACH(std::string producerId, m_globalSettings.GetGlobalProducers())
		{
			if(producerId == DecayChannelProducer().GetProducerId()) {
				this->AddGlobalProducer(new DecayChannelProducer());
			}
		}
	}

};

