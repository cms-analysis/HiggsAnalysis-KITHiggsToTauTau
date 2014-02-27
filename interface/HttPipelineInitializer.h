
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"
#include "Artus/KappaAnalysis/interface/KappaPipelineInitializer.h"

#include "HttTypes.h"

#include "HttPipelineSettings.h"
#include "HttEvent.h"
#include "HttProduct.h"

#include "Filters/PreselectionFilter.h"
#include "Consumers/HttNtupleConsumer.h"


class HttPipelineInitializer: public KappaPipelineInitializer<HttTypes> {
public:

	typedef std::function<float(HttEvent const&, HttProduct const&)> float_extractor_lambda;

	virtual void InitPipeline(HttPipeline * pLine,  HttPipelineSettings const& pset) const ARTUS_CPP11_OVERRIDE {
		
		// call upper class function
		// TODO: current solution destroys order of producers/filters/consumers
		KappaPipelineInitializer<HttTypes>::InitPipeline(pLine, pset);

		BOOST_FOREACH(std::string producerId, pset.GetLocalProducers())
		{
			// TODO
		}

		BOOST_FOREACH(std::string filterId, pset.GetFilters())
		{
			if(filterId == PreselectionFilter().GetFilterId()) {
				pLine->AddFilter(new PreselectionFilter());
			}
		}
		
		// TODO: move to dedicated class
		std::map<std::string, float_extractor_lambda> valueExtractorMap;
		valueExtractorMap["hardLepPt"] = [](HttEvent const& event, HttProduct const& product) { return product.m_validMuons.at(0)->p4.Pt(); };
		valueExtractorMap["hardLepEta"] = [](HttEvent const& event, HttProduct const& product) { return product.m_validMuons.at(0)->p4.Eta(); };
		valueExtractorMap["softLepPt"] = [](HttEvent const& event, HttProduct const& product) { return product.m_validMuons.at(1)->p4.Pt(); };
		valueExtractorMap["softLepEta"] = [](HttEvent const& event, HttProduct const& product) { return product.m_validMuons.at(1)->p4.Eta(); };
		valueExtractorMap["diLepMass"] = [](HttEvent const& event, HttProduct const& product) { return (product.m_validMuons.at(0)->p4 + product.m_validMuons.at(1)->p4).mass(); };

		BOOST_FOREACH(std::string consumerId, pset.GetConsumers())
		{
			if(consumerId == HttLambdaNtupleConsumer().GetConsumerId()) {
				pLine->AddConsumer(new HttLambdaNtupleConsumer(valueExtractorMap));
			}
			else if(consumerId == HttNtupleConsumer().GetConsumerId()) {
				pLine->AddConsumer(new HttNtupleConsumer);
			}
		}

	}
};
