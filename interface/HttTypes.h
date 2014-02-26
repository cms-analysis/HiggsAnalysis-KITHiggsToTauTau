
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"
#include "Artus/Core/interface/GlobalProducerBase.h"
#include "Artus/Core/interface/PipelineRunner.h"

#include "Artus/KappaAnalysis/interface/KappaPipelineRunner.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

#include "HttEvent.h"
#include "HttProduct.h"
#include "HttPipelineSettings.h"

/**
   HttTypes HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h

   Adjusts common Artus tools to the data formats used for Htt specific analyses. These types are 
   defined in HttTypes. Corresponding Artus templates are then expanded to use the specific types. 

   The final analysis workflow is organized by Producers, Filters and Consumers. Common philosophy 
   is to keep Consumers free of the analysis logic, which should be implemented in form of Filters 
   and Producers. Several Consumers could be defined to detemrine what quantities will be available 
   for plotting after Artus is run.
*/

/// all data types which are used for Htt analyses
struct HttTypes {
        /// content of the kappa ntuple
	typedef HttEvent event_type;
        /// objects that have been produced for plotting within Artus (i.e. logic implemented at analysis level)
	typedef HttProduct product_type;
        /// configuration settings which are Htt specific? 
	typedef HttPipelineSettings setting_type;
        /// global configration settings (which could also be Htt specific?)
	typedef HttGlobalSettings global_setting_type;
};

/// producers of global analysis objects
typedef GlobalProducerBase<HttTypes> HttGlobalProducerBase;
/// producers of local analysis objects
typedef LocalProducerBase<HttTypes> HttLocalProducerBase;
/// event filters at final analysis level
typedef FilterBase<HttTypes> HttFilterBase;
/// base class for a consumer (for final plotting)
typedef ConsumerBase<HttTypes> HttConsumerBase;
/// custom class for a consumer (for final plotting)
typedef LambdaNtupleConsumer<HttTypes> HttLambdaNtupleConsumer;
/// custom pipeline (several pipeline of this format could exist)
typedef Pipeline<HttTypes> HttPipeline;
/// custom pipeline runner (to manage running of pipelines in parallel)
typedef KappaPipelineRunner<HttTypes, HttPipeline, HttGlobalProducerBase> HttPipelineRunner;


