
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"
#include "Artus/Core/interface/ProducerBase.h"
#include "Artus/Core/interface/Pipeline.h"
#include "Artus/Core/interface/PipelineRunner.h"

#include "Artus/KappaAnalysis/interface/KappaPipelineInitializer.h"

#include "HttEvent.h"
#include "HttProduct.h"
#include "HttSettings.h"


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
	typedef HttSettings setting_type;
};

typedef Pipeline<HttTypes> HttPipeline;
typedef PipelineRunner<HttPipeline, HttTypes> HttPipelineRunner;
typedef KappaPipelineInitializer<HttTypes> HttPipelineInitializer;

typedef typename ROOT::Math::DisplacementVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag> RMDataV;
typedef typename ROOT::Math::SMatrix<double, 2, 2, ROOT::Math::MatRepSym<double, 2> > RMSM2x2;

