
#include <algorithm>
#include <math.h>

#include <boost/format.hpp>

#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MadGraphReweightingProducer.h"


std::string MadGraphReweightingProducer::GetProducerId() const
{
	return "MadGraphReweightingProducer";
}

void MadGraphReweightingProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);


	m_madGraphProcessDirectoriesByIndex = Utility::ParseMapTypes<int, std::string>( Utility::ParseVectorToMap(settings.GetMadGraphProcessDirectories()),
		                                                          			m_madGraphProcessDirectoriesByName);
	
	for (std::map<int, std::vector<std::string> >::const_iterator processDirectories = m_madGraphProcessDirectoriesByIndex.begin();
	     processDirectories != m_madGraphProcessDirectoriesByIndex.end(); ++processDirectories)
	{
		m_madGraphTools[processDirectories->second.at(0)] = std::map<int, MadGraphTools*>();
		for (std::vector<float>::const_iterator mixingAngleOverPiHalf = settings.GetMadGraphMixingAnglesOverPiHalf().begin();
		     mixingAngleOverPiHalf != settings.GetMadGraphMixingAnglesOverPiHalf().end(); ++mixingAngleOverPiHalf)
		{
			MadGraphTools* madGraphTools = new MadGraphTools(*mixingAngleOverPiHalf, processDirectories->second.at(0), settings.GetMadGraphParamCard(), 0.118);
			m_madGraphTools[processDirectories->second.at(0)][GetMixingAngleKey(*mixingAngleOverPiHalf)] = madGraphTools;
		}
	}
	
	// quantities for LambdaNtupleConsumer
	for (std::vector<float>::const_iterator mixingAngleOverPiHalfIt = settings.GetMadGraphMixingAnglesOverPiHalf().begin();
	     mixingAngleOverPiHalfIt != settings.GetMadGraphMixingAnglesOverPiHalf().end();
	     ++mixingAngleOverPiHalfIt)
	{
		float mixingAngleOverPiHalf = *mixingAngleOverPiHalfIt;
		std::string mixingAngleOverPiHalfLabel = GetLabelForWeightsMap(mixingAngleOverPiHalf);
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(mixingAngleOverPiHalfLabel, [mixingAngleOverPiHalfLabel](event_type const& event, product_type const& product)
		{
			return SafeMap::GetWithDefault(product.m_optionalWeights, mixingAngleOverPiHalfLabel, 0.0);
		});
	}
	
	if (settings.GetMadGraphMixingAnglesOverPiHalfSample() >= 0.0)
	{
		float mixingAngleOverPiHalfSample = settings.GetMadGraphMixingAnglesOverPiHalfSample();
		
		// if mixing angle for curent sample is defined, it has to be in the list MadGraphMixingAnglesOverPiHalf
		assert(Utility::Contains(settings.GetMadGraphMixingAnglesOverPiHalf(), mixingAngleOverPiHalfSample));
		
		std::string mixingAngleOverPiHalfSampleLabel = GetLabelForWeightsMap(mixingAngleOverPiHalfSample);
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("madGraphWeightSample", [mixingAngleOverPiHalfSampleLabel](event_type const& event, product_type const& product)
		{
			return SafeMap::GetWithDefault(product.m_optionalWeights, mixingAngleOverPiHalfSampleLabel, 0.0);
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("madGraphWeightInvSample", [mixingAngleOverPiHalfSampleLabel](event_type const& event, product_type const& product)
		{
			double weight = SafeMap::GetWithDefault(product.m_optionalWeights, mixingAngleOverPiHalfSampleLabel, 0.0);
			//return std::min(((weight > 0.0) ? (1.0 / weight) : 0.0), 10.0);   // no physics reason for this
			return ((weight > 0.0) ? (1.0 / weight) : 0.0);
		});
	}
}


void MadGraphReweightingProducer::Produce(event_type const& event, product_type& product,
                                          setting_type const& settings) const
{
	// TODO: should this be an assertion?
	if (event.m_lheParticles != nullptr)
	{
		int productionMode=0;
		int numberGluons=0;
		int numberBottomQuarks=0;
		int numberOtherQuarks=0;

		std::vector<const RMFLV*> particleFourMomenta;
		for (KGenParticles::const_iterator lheParticle = event.m_lheParticles->begin(); lheParticle != event.m_lheParticles->end(); ++lheParticle)
		{
			if (particleFourMomenta.size() < 5)
			{
				particleFourMomenta.push_back(&(lheParticle->p4));
			}
		
			if (lheParticle->pdgId == DefaultValues::pdgIdGluon)
			{
				++numberGluons;
			}
			if (std::abs(lheParticle->pdgId) == 5)
			{
				++numberBottomQuarks;
			}
			if (std::abs(lheParticle->pdgId) < 5)
			{
				++numberOtherQuarks;
			}		
		}
	
		if ((numberGluons==2) &&
		    (numberBottomQuarks==0)&&
		    (numberOtherQuarks==0))
		{
			productionMode=0;
		}
		else if ((numberGluons==3) &&
		         (numberBottomQuarks==0)&&
		         (numberOtherQuarks==0))
		{
			productionMode=1;
		}
		else if ((numberGluons>3) &&
		         (numberBottomQuarks==0)&&
		         (numberOtherQuarks==0))
		{
			productionMode=2;
		}

		else if ((numberGluons>1) &&
		         (numberBottomQuarks>1)&&
		         (numberOtherQuarks==0))
		{
			productionMode=3;
		}
		else if ((numberGluons>1) &&
		         (numberBottomQuarks==0)&&
		         (numberOtherQuarks>1))
		{
			productionMode=4;
		}
		
		std::string madGraphProcessDirectory = SafeMap::Get(m_madGraphProcessDirectoriesByIndex, productionMode)[0];
		std::map<int, MadGraphTools*>* tmpMadGraphToolsMap = const_cast<std::map<int, MadGraphTools*>*>(&(SafeMap::Get(m_madGraphTools, madGraphProcessDirectory)));
		
		// calculate the matrix elements for different mixing angles
		for (std::vector<float>::const_iterator mixingAngleOverPiHalf = settings.GetMadGraphMixingAnglesOverPiHalf().begin();
		     mixingAngleOverPiHalf != settings.GetMadGraphMixingAnglesOverPiHalf().end(); ++mixingAngleOverPiHalf)
		{
			MadGraphTools* tmpMadGraphTools = SafeMap::Get(*tmpMadGraphToolsMap, GetMixingAngleKey(*mixingAngleOverPiHalf));
			product.m_optionalWeights[GetLabelForWeightsMap(*mixingAngleOverPiHalf)] = tmpMadGraphTools->GetMatrixElementSquared(particleFourMomenta);
			//LOG(DEBUG) << *mixingAngleOverPiHalf << " --> " << product.m_optionalWeights[GetLabelForWeightsMap(*mixingAngleOverPiHalf)];
		}
	}
}

int MadGraphReweightingProducer::GetMixingAngleKey(float mixingAngleOverPiHalf) const
{
	return int(mixingAngleOverPiHalf * 100.0);
}

std::string MadGraphReweightingProducer::GetLabelForWeightsMap(float mixingAngleOverPiHalf) const
{
	return ("madGraphWeight" + str(boost::format("%03d") % (mixingAngleOverPiHalf * 100.0)));
}

