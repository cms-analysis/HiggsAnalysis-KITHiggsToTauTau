
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"
#include "Artus/Core/interface/GlobalProducerBase.h"
#include "Artus/Core/interface/PipelineRunner.h"

#include "Artus/KappaAnalysis/interface/Producers/PhysicsObjectsProducer.h"
#include "Artus/KappaAnalysis/interface/KappaPipelineRunner.h"

#include "HttEvent.h"
#include "HttProduct.h"
#include "HttPipelineSettings.h"

// all data types which are used for this analysis
struct HttTypes {
	typedef HttEvent event_type;
	typedef HttProduct product_type;
	typedef HttPipelineSettings setting_type;
	typedef HttGlobalSettings global_setting_type;
};

// Pass the template parameters for the Producers
typedef GlobalProducerBase<HttTypes> HttGlobalProducerBase;
typedef LocalProducerBase<HttTypes> HttLocalProducerBase;

typedef ValidMuonsProducer<HttTypes> HttValidMuonsProducer;

// Pass the template parameters for the Consumer
typedef ConsumerBase<HttTypes> HttConsumerBase;

// Pass the template parameters for the Filter
typedef FilterBase<HttTypes> HttFilterBase;

//Pass the template parameters for the Pipeline
typedef Pipeline<HttTypes> HttPipeline;

//Setup our custom pipeline runner
//typedef PipelineRunner<HttPipeline, HttGlobalProducerBase> HttPipelineRunner;
typedef KappaPipelineRunner<HttTypes, HttPipeline, HttGlobalProducerBase> HttPipelineRunner;
