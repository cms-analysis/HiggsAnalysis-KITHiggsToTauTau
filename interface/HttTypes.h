
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"
#include "Artus/Core/interface/GlobalProducerBase.h"
#include "Artus/Core/interface/PipelineRunner.h"

#include "Artus/KappaAnalysis/interface/KappaPipelineRunner.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

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

// Pass the template parameters for the Consumer
typedef ConsumerBase<HttTypes> HttConsumerBase;

// Pass the template parameters for the Filter
typedef FilterBase<HttTypes> HttFilterBase;

//Pass the template parameters for the Pipeline
typedef Pipeline<HttTypes> HttPipeline;

//Setup our custom ntuple producer
typedef LambdaNtupleConsumer<HttTypes> HttLambdaNtupleConsumer;

