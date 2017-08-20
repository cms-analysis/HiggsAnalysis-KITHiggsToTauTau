
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

	// parsing settings
	std::map<int, std::vector<std::string> > madGraphProcessDirectoriesByIndex = Utility::ParseMapTypes<int, std::string>(
			Utility::ParseVectorToMap(settings.GetMadGraphProcessDirectories()),
			m_madGraphProcessDirectoriesByName
	);
	
	// preparations of MadGraphTools objects
	for (std::map<std::string, std::vector<std::string> >::const_iterator processDirectories = m_madGraphProcessDirectoriesByName.begin();
	     processDirectories != m_madGraphProcessDirectoriesByName.end(); ++processDirectories)
	{
		m_madGraphTools[processDirectories->second.at(0)] = std::map<int, MadGraphTools*>();
		
		//create map that stores a MadGraphTools element for every directory and every mixing angle
		for (std::vector<float>::const_iterator mixingAngleOverPiHalf = settings.GetMadGraphMixingAnglesOverPiHalf().begin();
		     mixingAngleOverPiHalf != settings.GetMadGraphMixingAnglesOverPiHalf().end(); ++mixingAngleOverPiHalf)
		{
			MadGraphTools* madGraphTools = new MadGraphTools(*mixingAngleOverPiHalf, processDirectories->second.at(0), settings.GetMadGraphParamCard(), 0.118);
			m_madGraphTools[processDirectories->second.at(0)][GetMixingAngleKey(*mixingAngleOverPiHalf)] = madGraphTools;
		}
		
		//add the MadGraphTools element needed for reweighting
		MadGraphTools* madGraphTools = new MadGraphTools(0, processDirectories->second.at(0), settings.GetMadGraphParamCardSample(), 0.118);
		m_madGraphTools[processDirectories->second.at(0)][-1] = madGraphTools;
	}
		
	std::string pdgDatabaseFilename = settings.GetDatabasePDG();
 	if (! pdgDatabaseFilename.empty())
	{
		if (m_databasePDG)
		{
			delete m_databasePDG;
			m_databasePDG = nullptr;
		}
		m_databasePDG = new TDatabasePDG();
		boost::algorithm::replace_first(pdgDatabaseFilename, "$ROOTSYS", getenv("ROOTSYS"));
		LOG(DEBUG) << "Read PDG database from \"" << pdgDatabaseFilename << "\"...";
		m_databasePDG->ReadPDGTable(pdgDatabaseFilename.c_str());
	}
	
	// add possible quantities for the lambda ntuples consumers
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
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(std::string("madGraphWeightSample"), [mixingAngleOverPiHalfSampleLabel](event_type const& event, product_type const& product)
		{
			return SafeMap::GetWithDefault(product.m_optionalWeights, std::string("madGraphWeightSample"), 0.0);
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(std::string("madGraphWeightInvSample"), [mixingAngleOverPiHalfSampleLabel](event_type const& event, product_type const& product)
		{
			double weight = SafeMap::GetWithDefault(product.m_optionalWeights, std::string("madGraphWeightSample"), 0.0);
			//return std::min(((weight > 0.0) ? (1.0 / weight) : 0.0), 10.0);   // no physics reason for this
			return ((weight > 0.0) ? (1.0 / weight) : 0.0);
		});
	}
	
	for (size_t particleIndex = 0; particleIndex < 6; ++particleIndex)
	{
		std::string particleIndexStr = std::to_string(particleIndex+1);
		
		LambdaNtupleConsumer<HttTypes>::AddCartesianRMFLVQuantity("madGraphLheParticle"+particleIndexStr+"LV", [this, particleIndex](event_type const& event, product_type const& product)
		{
			return product.m_lheParticlesSortedForMadGraph.size() > particleIndex ? product.m_lheParticlesSortedForMadGraph.at(particleIndex)->p4 : DefaultValues::UndefinedCartesianRMFLV;
		});
		
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity("madGraphLheParticle"+particleIndexStr+"PdgId", [this, particleIndex](event_type const& event, product_type const& product)
		{
			return product.m_lheParticlesSortedForMadGraph.size() > particleIndex ? product.m_lheParticlesSortedForMadGraph.at(particleIndex)->pdgId : DefaultValues::UndefinedInt;
		});
	}
	
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("subProcessCode", [](event_type const& event, product_type const& product)
	{
		return event.m_lheParticles->subprocessCode;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("lheParticleJetNumber", [](event_type const& event, product_type const& product)
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
	
	// sorting of LHE particles for MadGraph
	LOG(DEBUG) << "NOW SORTING!!!";
	std::sort(product.m_lheParticlesSortedForMadGraph.begin(), product.m_lheParticlesSortedForMadGraph.begin()+2, &MadGraphReweightingProducer::MadGraphParticleOrdering);
	std::sort(product.m_lheParticlesSortedForMadGraph.begin()+3, product.m_lheParticlesSortedForMadGraph.end(), &MadGraphReweightingProducer::MadGraphParticleOrdering);

	// preparations for MadGraph
	std::vector<CartesianRMFLV*> particleFourMomenta;
	std::string processDirectoryKey = "";
	for (std::vector<KLHEParticle*>::iterator madGraphLheParticle = product.m_lheParticlesSortedForMadGraph.begin();
	     madGraphLheParticle != product.m_lheParticlesSortedForMadGraph.end(); ++madGraphLheParticle)
	{
		particleFourMomenta.push_back(&((*madGraphLheParticle)->p4));
		processDirectoryKey += (std::string(Utility::Contains(settings.GetBosonPdgIds(), std::abs((*madGraphLheParticle)->pdgId)) ? "_" : "") +
		                        std::string(m_databasePDG->GetParticle((*madGraphLheParticle)->pdgId)->GetName()));
	}
	
	if (Utility::Contains(m_madGraphProcessDirectoriesByName, processDirectoryKey))
	{
		std::string madGraphProcessDirectory = m_madGraphProcessDirectoriesByName.at(processDirectoryKey)[0];
		LOG_N_TIMES(50, DEBUG) << "MadGraph process directory: " << madGraphProcessDirectory << " (" << processDirectoryKey << ")";
		
		std::map<int, MadGraphTools*>* tmpMadGraphToolsMap = const_cast<std::map<int, MadGraphTools*>*>(&(SafeMap::Get(m_madGraphTools, madGraphProcessDirectory)));
		
		// calculate the matrix elements for different mixing angles
		for (std::vector<float>::const_iterator mixingAngleOverPiHalf = settings.GetMadGraphMixingAnglesOverPiHalf().begin();
		     mixingAngleOverPiHalf != settings.GetMadGraphMixingAnglesOverPiHalf().end(); ++mixingAngleOverPiHalf)
		{
			MadGraphTools* tmpMadGraphTools = SafeMap::Get(*tmpMadGraphToolsMap, GetMixingAngleKey(*mixingAngleOverPiHalf));
			float matrixElementSquared = tmpMadGraphTools->GetMatrixElementSquared(particleFourMomenta);
			if (matrixElementSquared < 0.0)
			{
				LOG(ERROR) << "Error in calculation of matrix element for \"" << processDirectoryKey << ":" << madGraphProcessDirectory << "\"";
				LOG(ERROR) << "in event: run = " << event.m_eventInfo->nRun << ", lumi = " << event.m_eventInfo->nLumi << ", event = " << event.m_eventInfo->nEvent << ", pipeline = \"" << settings.GetName() << "\"!";
			}
			else
			{
				product.m_optionalWeights[GetLabelForWeightsMap(*mixingAngleOverPiHalf)] = matrixElementSquared;
			}
		}
		
		//calculate the old matrix element for reweighting
		MadGraphTools* tmpMadGraphTools = SafeMap::Get(*tmpMadGraphToolsMap, -1);
		float matrixElementSquared = tmpMadGraphTools->GetMatrixElementSquared(particleFourMomenta);
		if (matrixElementSquared < 0.0)
		{
			LOG(ERROR) << "Error in calculation of matrix element for \"" << processDirectoryKey << ":" << madGraphProcessDirectory << "\"";
			LOG(ERROR) << "in event: run = " << event.m_eventInfo->nRun << ", lumi = " << event.m_eventInfo->nLumi << ", event = " << event.m_eventInfo->nEvent << ", pipeline = \"" << settings.GetName() << "\"!";
		}
		else
		{
			product.m_optionalWeights["madGraphWeightSample"] = matrixElementSquared;
		}
	}
	else
	{
		LOG(ERROR) << "Process directory for production mode \"" << processDirectoryKey << "\" not found in settings with tag \"MadGraphProcessDirectories\"!";
		LOG(ERROR) << "in event: run = " << event.m_eventInfo->nRun << ", lumi = " << event.m_eventInfo->nLumi << ", event = " << event.m_eventInfo->nEvent << ", pipeline = \"" << settings.GetName() << "\"!";
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

// pdgParticle->GetName() has no specific order
// madgraph sorts particle before antiparticle
// puts gluons first
// up type quarks second
// downtype quarks third
// heavy quarks last => the order is: g u c d s u_bar c_bar d_bar s_bar b b_bar
bool MadGraphReweightingProducer::MadGraphParticleOrdering(KLHEParticle* lheParticle1, KLHEParticle* lheParticle2)
{
	int pdgId1 = std::abs(lheParticle1->pdgId);
	int pdgId2 = std::abs(lheParticle2->pdgId);
	
	if ((lheParticle1->pdgId < 0) && (lheParticle2->pdgId > 0))
	{
		if ((pdgId1 != DefaultValues::pdgIdBottom) && (pdgId2 == DefaultValues::pdgIdBottom))
		{
			return true;
		}
		else
		{
			return false;
		}
	}
	else if ((lheParticle1->pdgId > 0) && (lheParticle2->pdgId < 0))
	{
		if ((pdgId1 == DefaultValues::pdgIdBottom) && (pdgId2 != DefaultValues::pdgIdBottom))
		{
			return false;
		}
		else
		{
			return true;
		}
	}
	else
	{
		pdgId1 = std::abs(pdgId1);
		pdgId2 = std::abs(pdgId2);
		
		if (pdgId1 == DefaultValues::pdgIdGluon)
		{
			return true;
		}
		else if (pdgId2 == DefaultValues::pdgIdGluon)
		{
			return false;
		}
		else if (pdgId1 == DefaultValues::pdgIdUp)
		{
			return true;
		}
		else if (pdgId2 == DefaultValues::pdgIdUp)
		{
			return false;
		}
		else if (pdgId1 == DefaultValues::pdgIdCharm)
		{
			return true;
		}
		else if (pdgId2 == DefaultValues::pdgIdCharm)
		{
			return false;
		}
		else if (pdgId1 == DefaultValues::pdgIdDown)
		{
			return true;
		}
		else if (pdgId2 == DefaultValues::pdgIdDown)
		{
			return false;
		}
		else if (pdgId1 == DefaultValues::pdgIdStrange)
		{
			return true;
		}
		else if (pdgId2 == DefaultValues::pdgIdStrange)
		{
			return false;
		}
		else if (pdgId1 == DefaultValues::pdgIdBottom)
		{
			return true;
		}
		else if (pdgId2 == DefaultValues::pdgIdBottom)
		{
			return false;
		}
		else
		{
			return true;
		}
	}
}

