
#include <algorithm>
#include <math.h>

#include <boost/format.hpp>

#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

#include <boost/algorithm/string/replace.hpp>

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MadGraphReweightingProducer.h"


std::string MadGraphReweightingProducer::GetProducerId() const
{
	return "MadGraphReweightingProducer";
}

void MadGraphReweightingProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	
	//create map that stores a MadGraphTools element for every mixing angle
	for (std::vector<float>::const_iterator mixingAngleOverPiHalf = settings.GetMadGraphMixingAnglesOverPiHalf().begin();
	     mixingAngleOverPiHalf != settings.GetMadGraphMixingAnglesOverPiHalf().end(); ++mixingAngleOverPiHalf)
	{
		MadGraphTools* madGraphTools = new MadGraphTools(*mixingAngleOverPiHalf, settings.GetMadGraphProcessDirectories(), settings.GetMadGraphParamCard(), 0.118, settings.GetMadGraphSortingHeavyBQuark());
		m_madGraphTools[MadGraphReweightingProducer::GetMixingAngleKey(*mixingAngleOverPiHalf)] = madGraphTools;
	}
	
	//add the MadGraphTools element needed for reweighting
	MadGraphTools* madGraphTools = new MadGraphTools(0, settings.GetMadGraphProcessDirectories(), settings.GetMadGraphParamCard(), 0.118, settings.GetMadGraphSortingHeavyBQuark());
	m_madGraphTools[-1] = madGraphTools;
	
	// add possible quantities for the lambda ntuples consumers
	for (std::vector<float>::const_iterator mixingAngleOverPiHalfIt = settings.GetMadGraphMixingAnglesOverPiHalf().begin();
	     mixingAngleOverPiHalfIt != settings.GetMadGraphMixingAnglesOverPiHalf().end();
	     ++mixingAngleOverPiHalfIt)
	{
		float mixingAngleOverPiHalf = *mixingAngleOverPiHalfIt;
		std::string mixingAngleOverPiHalfLabel = MadGraphReweightingProducer::GetLabelForWeightsMap(mixingAngleOverPiHalf);
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, mixingAngleOverPiHalfLabel, [mixingAngleOverPiHalfLabel](event_type const& event, product_type const& product)
		{
			return SafeMap::GetWithDefault(product.m_optionalWeights, mixingAngleOverPiHalfLabel, 0.0);
		});
	}
	
	if (settings.GetMadGraphMixingAnglesOverPiHalfSample() >= 0.0)
	{
		float mixingAngleOverPiHalfSample = settings.GetMadGraphMixingAnglesOverPiHalfSample();
		
		// if mixing angle for curent sample is defined, it has to be in the list MadGraphMixingAnglesOverPiHalf
		assert(Utility::Contains(settings.GetMadGraphMixingAnglesOverPiHalf(), mixingAngleOverPiHalfSample));
		
		std::string mixingAngleOverPiHalfSampleLabel = MadGraphReweightingProducer::GetLabelForWeightsMap(mixingAngleOverPiHalfSample);
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, std::string("madGraphWeightSample"), [mixingAngleOverPiHalfSampleLabel](event_type const& event, product_type const& product)
		{
			return SafeMap::GetWithDefault(product.m_optionalWeights, std::string("madGraphWeightSample"), 0.0);
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, std::string("madGraphWeightInvSample"), [mixingAngleOverPiHalfSampleLabel](event_type const& event, product_type const& product)
		{
			double weight = SafeMap::GetWithDefault(product.m_optionalWeights, std::string("madGraphWeightSample"), 0.0);
			//return std::min(((weight > 0.0) ? (1.0 / weight) : 0.0), 10.0);   // no physics reason for this
			return ((weight > 0.0) ? (1.0 / weight) : 0.0);
		});
	}
	
	for (size_t particleIndex = 0; particleIndex < 6; ++particleIndex)
	{
		std::string particleIndexStr = std::to_string(particleIndex+1);
		
		LambdaNtupleConsumer<HttTypes>::AddCartesianRMFLVQuantity(metadata, "madGraphLheParticle"+particleIndexStr+"LV", [this, particleIndex](event_type const& event, product_type const& product)
		{
			return product.m_lheParticlesSortedForMadGraph.size() > particleIndex ? product.m_lheParticlesSortedForMadGraph.at(particleIndex)->p4 : DefaultValues::UndefinedCartesianRMFLV;
		});
		
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "madGraphLheParticle"+particleIndexStr+"PdgId", [this, particleIndex](event_type const& event, product_type const& product)
		{
			return product.m_lheParticlesSortedForMadGraph.size() > particleIndex ? product.m_lheParticlesSortedForMadGraph.at(particleIndex)->pdgId : DefaultValues::UndefinedInt;
		});
	}
	
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "subProcessCode", [](event_type const& event, product_type const& product)
	{
		return event.m_lheParticles->subprocessCode;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "lheParticleJetNumber", [](event_type const& event, product_type const& product)
	{
		return static_cast<int>(product.m_lheParticlesSortedForMadGraph.size()) - 3;
	});
}


void MadGraphReweightingProducer::Produce(event_type const& event, product_type& product,
                                          setting_type const& settings, metadata_type const& metadata) const
{
	assert(event.m_lheParticles);
	
	// copy LHE particles to new vector which can be sorted
	product.m_lheParticlesSortedForMadGraph.clear();
	for (std::vector<KLHEParticle>::const_iterator lheParticle = event.m_lheParticles->particles.begin(); lheParticle != event.m_lheParticles->particles.end(); ++lheParticle)
	{
		product.m_lheParticlesSortedForMadGraph.push_back(const_cast<KLHEParticle*>(&(*lheParticle)));
		
	}
	
	LOG_N_TIMES(50, DEBUG) << "MadGraph process directory: " << settings.GetMadGraphProcessDirectories();
	
	// calculate the matrix elements for different mixing angles
	for (std::vector<float>::const_iterator mixingAngleOverPiHalf = settings.GetMadGraphMixingAnglesOverPiHalf().begin();
	     mixingAngleOverPiHalf != settings.GetMadGraphMixingAnglesOverPiHalf().end(); ++mixingAngleOverPiHalf)
	{
		MadGraphTools* tmpMadGraphTools = SafeMap::Get(m_madGraphTools, MadGraphReweightingProducer::GetMixingAngleKey(*mixingAngleOverPiHalf));
		float matrixElementSquared = tmpMadGraphTools->GetMatrixElementSquared(product.m_lheParticlesSortedForMadGraph);
		if (matrixElementSquared < 0.0)
		{
			LOG(ERROR) << "Error in calculation of matrix element for \"" << ":" << settings.GetMadGraphProcessDirectories() <<  "\"";
			LOG(ERROR) << "in event: run = " << event.m_eventInfo->nRun << ", lumi = " << event.m_eventInfo->nLumi << ", event = " << event.m_eventInfo->nEvent << ", pipeline = \"" << settings.GetName() << "\"!";
			product.m_optionalWeights[MadGraphReweightingProducer::GetLabelForWeightsMap(*mixingAngleOverPiHalf)] = 0.0;
			}
		else
		{
			product.m_optionalWeights[MadGraphReweightingProducer::GetLabelForWeightsMap(*mixingAngleOverPiHalf)] = matrixElementSquared;
		}
	}
		
	//calculate the old matrix element for reweighting
	MadGraphTools* tmpMadGraphTools = SafeMap::Get(m_madGraphTools, -1);
	float matrixElementSquared = tmpMadGraphTools->GetMatrixElementSquared(product.m_lheParticlesSortedForMadGraph);
	if (matrixElementSquared < 0.0)
	{
		LOG(ERROR) << "Error in calculation of matrix element for \""<< ":" << settings.GetMadGraphProcessDirectories() << "\"";
		LOG(ERROR) << "in event: run = " << event.m_eventInfo->nRun << ", lumi = " << event.m_eventInfo->nLumi << ", event = " << event.m_eventInfo->nEvent << ", pipeline = \"" << settings.GetName() << "\"!";
		product.m_optionalWeights["madGraphWeightSample"] = 0.0;
	}
	else
	{
		product.m_optionalWeights["madGraphWeightSample"] = matrixElementSquared;
	}
	
}

int MadGraphReweightingProducer::GetMixingAngleKey(float mixingAngleOverPiHalf)
{
	return int(mixingAngleOverPiHalf * 100.0);
}

std::string MadGraphReweightingProducer::GetLabelForWeightsMap(float mixingAngleOverPiHalf)
{
	return ("madGraphWeight" + str(boost::format("%03d") % (mixingAngleOverPiHalf * 100.0)));
}




