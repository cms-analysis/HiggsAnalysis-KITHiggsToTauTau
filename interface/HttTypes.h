
#pragma once

#include "Artus/Core/interface/ProducerBase.h"
#include "Artus/Core/interface/Pipeline.h"
#include "Artus/Core/interface/PipelineRunner.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEvent.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttProduct.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttSettings.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttMetadata.h"


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
class HttTypes {

public:
	/// content of the kappa ntuple
	typedef HttEvent event_type;
	
	/// objects that have been produced for plotting within Artus (i.e. logic implemented at analysis level)
	typedef HttProduct product_type;
	
	/// configuration settings which are Htt specific? 
	typedef HttSettings setting_type;
	
	/// objects that exist once per pipeline and can be modified in Init functions of processors
	typedef HttMetadata metadata_type;
};

typedef Pipeline<HttTypes> HttPipeline;
typedef PipelineRunner<HttPipeline, HttTypes> HttPipelineRunner;
typedef PipelineInitilizerBase<HttTypes> HttPipelineInitializer;

