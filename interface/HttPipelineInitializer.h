
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"
#include "Artus/Consumer/interface/ValueModifier.h"

#include "Artus/Consumer/interface/DrawHist1dConsumer.h"
#include "Artus/Consumer/interface/ProfileConsumerBase.h"

#include "HttTypes.h"

#include "HttPipelineSettings.h"
#include "HttEvent.h"
#include "HttProduct.h"

// filter
#include "PtFilter.h"

// consumer
#include "MeanPtConsumer.h"
#include "HttNtupleConsumer.h"

class HttPipelineInitializer: public PipelineInitilizerBase<HttTypes> {
public:

	virtual void InitPipeline(HttPipeline * pLine,
			HttPipelineSettings const& pset) const ARTUS_CPP11_OVERRIDE
			{

		pLine->AddFilter(new PtFilter());
		pLine->AddConsumer(new MeanPtConsumer());

		typedef std::function<
				std::vector<float>(event_type const&, product_type const& )> ValueExtractLambda;
		typedef std::pair<ValueExtractLambda, ValueModifiers> ValueDesc;

		// define how to extract Pt and the range
		auto extractPtSim =
				[]( HttEvent const& ev, HttProduct const & prod )
				-> std::vector<float> {return {ev.m_floatPtSim};};
		auto PtSimValue = std::make_pair(extractPtSim,
				DefaultModifiers::getPtModifier(0.7, 1.3f));

		// extracts the value which has been corrected by a globalProducer
		auto extractPtSimCorrected =
				[]( HttEvent const& ev, HttProduct const & prod )
				-> std::vector<float> {return {prod.m_floatPtSim_corrected};};
		auto PtSimCorrectedValue = std::make_pair(extractPtSimCorrected,
				DefaultModifiers::getPtModifier(0.7, 1.3f));

		// define how to extract Theta and the range
		auto extractThetaSim =
				[]( HttEvent const& ev, HttProduct const & prod )
				-> std::vector<float> {return {ev.m_floatTheSim};};

		auto ThetaSimValue = std::make_pair(extractThetaSim,
				DefaultModifiers::getThetaModifier());


		BOOST_FOREACH(std::string id, pset.GetConsumer())
		{
			if (id == "quantities_all")
			{
				// plot Pt
				pLine->AddConsumer(
						new DrawHist1dConsumerBase<HttTypes>("pt", PtSimValue));

				// plot Pt - corrected, from the global product
				pLine->AddConsumer(
						new DrawHist1dConsumerBase<HttTypes>("pt_corr", PtSimCorrectedValue));


				// plot Theta
				pLine->AddConsumer(
						new DrawHist1dConsumerBase<HttTypes>("theta", ThetaSimValue));

				// profile Pt over Theta
				pLine->AddConsumer(
						new ProfileConsumerBase<HttTypes>("pt_over_theta",
							ThetaSimValue, PtSimValue));
			}
			else if (id == "ntuple")
				pLine->AddConsumer(new HttNtupleConsumer);
		}

	}
};
