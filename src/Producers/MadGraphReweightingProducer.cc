
#include <algorithm>
#include <math.h>

#include <boost/format.hpp>

#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MadGraphReweightingProducer.h"
std::map<std::string, std::vector<std::string> > m_madGraphProcessDirectoriesByName;

std::string MadGraphReweightingProducer::GetProducerId() const
{
	return "MadGraphReweightingProducer";
}

void MadGraphReweightingProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);

	// parsing settings
	//std::map<std::string, std::vector<std::string> > madGraphProcessDirectoriesByName;
	std::map<int, std::vector<std::string> > madGraphProcessDirectoriesByIndex = Utility::ParseMapTypes<int, std::string>(
			Utility::ParseVectorToMap(settings.GetMadGraphProcessDirectories()),
			m_madGraphProcessDirectoriesByName
	);
	for (std::map<int, std::vector<std::string> >::const_iterator processDirectories = madGraphProcessDirectoriesByIndex.begin();
	     processDirectories != madGraphProcessDirectoriesByIndex.end(); ++processDirectories)
	{
		m_madGraphProcessDirectories[static_cast<HttEnumTypes::MadGraphProductionModeGGH>(processDirectories->first)] = processDirectories->second;
	}
	for (std::map<std::string, std::vector<std::string> >::const_iterator processDirectories = m_madGraphProcessDirectoriesByName.begin();
	     processDirectories != m_madGraphProcessDirectoriesByName.end(); ++processDirectories)
	{
		m_madGraphProcessDirectories[HttEnumTypes::ToMadGraphProductionModeGGH(processDirectories->first)] = processDirectories->second;
	}
	
	// preparations of MadGraphTools objects
	for (std::map<HttEnumTypes::MadGraphProductionModeGGH, std::vector<std::string> >::const_iterator processDirectories = m_madGraphProcessDirectories.begin();
	     processDirectories != m_madGraphProcessDirectories.end(); ++processDirectories)
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
	
	// add possible quantities for the lambda ntuples consumers
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
}


void MadGraphReweightingProducer::Produce(event_type const& event, product_type& product,
                                          setting_type const& settings) const
{
	product.m_lheParticlesSortedForMadGraph.clear();
	
	// TODO: should this be an assertion?
	if (event.m_lheParticles != nullptr)
	{
		//HttEnumTypes::MadGraphProductionModeGGH productionMode = HttEnumTypes::MadGraphProductionModeGGH::NONE;
		
		int numberGluons=0;
		int numberBottomQuarks=0;
		int numberOtherQuarks=0;
		
		/*std::vector<const KGenParticle*> selectedLheParticles;
		for (KGenParticles::const_iterator lheParticle1 = event.m_lheParticles->begin(); lheParticle1 != event.m_lheParticles->end(); ++lheParticle1)
		{
			if (std::abs(lheParticle1->pdgId) <= 6) // lheParticle1 is a quark
			{
				for (KGenParticles::const_iterator lheParticle2 = event.m_lheParticles->begin(); lheParticle2 != event.m_lheParticles->end(); ++lheParticle2)
				{
					if ((std::abs(lheParticle2->pdgId) <= 6) && (lheParticle1 != lheParticle2)) // lheParticle2 is a quark and different from lheParticle1
					{
						for (KGenParticles::const_iterator lheParticle3 = event.m_lheParticles->begin(); lheParticle3 != event.m_lheParticles->end(); ++lheParticle3)
						{
							if (std::abs(lheParticle3->pdgId) == DefaultValues::pdgIdGluon) // lheParticle3 is a gluon
							{
								if ((Utility::ApproxEqual(lheParticle1->p4 + lheParticle2->p4, lheParticle3->p4)) ||
								    (Utility::ApproxEqual(lheParticle1->p4 - lheParticle2->p4, lheParticle3->p4)) ||
								    (Utility::ApproxEqual(lheParticle2->p4 - lheParticle1->p4, lheParticle3->p4)))
								{
									LOG(ERROR) << lheParticle3->p4.mass();
								}
							}
						}
					}
				}
			}
		}*/
		
		struct ParticlesGroup
		{
			std::vector<const KLHEParticle*> momenta;
			int nLightQuarks = 0;
			int nHeavyQuarks = 0;
			int nGluons = 0;
			int nHiggsBosons = 0;
		} initialParticles, higgsParticles, jetParticles;
		
		std::vector<const CartesianRMFLV*> particleFourMomenta;
		std::string directoryname = "";
		std::string initialname = "";
		std::string jetname = "";
		std::string higgsname = "";
		//std::map(<int>,<>);

		for (std::vector<KLHEParticle>::const_iterator lheParticle = event.m_lheParticles->particles.begin(); lheParticle != event.m_lheParticles->particles.end(); ++lheParticle)
		{
			ParticlesGroup* selectedParticles = nullptr;
			
			if (lheParticle->status == -1)
			{
				selectedParticles = &initialParticles;



				if (lheParticle->pdgId == DefaultValues::pdgIdGluon)
				{
					selectedParticles->nGluons += 1;
					++numberGluons;
					initialname += "g";
				}
				

				else if ((lheParticle->pdgId) == 1)
				{
					selectedParticles->nLightQuarks += 1;
					++numberOtherQuarks;
					initialname += "d";
				}
			
				else if ((lheParticle->pdgId) == -1)
				{
					selectedParticles->nLightQuarks += 1;
					++numberOtherQuarks;
					initialname += "dx";
				}

				else if ((lheParticle->pdgId) == 2)
				{
					selectedParticles->nLightQuarks += 1;
					++numberOtherQuarks;
					initialname += "u";
				}
			
				else if ((lheParticle->pdgId) == -2)
				{
					selectedParticles->nLightQuarks += 1;
					++numberOtherQuarks;
					initialname += "ux";
				}

				else if ((lheParticle->pdgId) == 3)
				{
					selectedParticles->nLightQuarks += 1;
					++numberOtherQuarks;
					initialname += "s";
				}
			
				else if ((lheParticle->pdgId) == -3)
				{
					selectedParticles->nLightQuarks += 1;
					++numberOtherQuarks;
					initialname += "sx";
				}

				else if ((lheParticle->pdgId) == 4)
				{
					selectedParticles->nLightQuarks += 1;
					++numberOtherQuarks;
					initialname += "c";
				}
			
				else if ((lheParticle->pdgId) == -4)
				{
					selectedParticles->nLightQuarks += 1;
					++numberOtherQuarks;
					initialname += "cx";
				}

				else if ((lheParticle->pdgId) == 5)
				{
					selectedParticles->nHeavyQuarks += 1;
					++numberBottomQuarks;
					initialname += "b";
				}
			
				else if ((lheParticle->pdgId) == -5)
				{
					selectedParticles->nHeavyQuarks += 1;
					++numberBottomQuarks;
					initialname += "bx";
				}


			}
			else if (Utility::Contains(settings.GetBosonPdgIds(), std::abs(lheParticle->pdgId)))
			{
				selectedParticles = &higgsParticles;
				selectedParticles->nHiggsBosons += 1;

				if ((lheParticle->pdgId) == 25)
				{
					selectedParticles = &higgsParticles;
					selectedParticles->nHiggsBosons += 1;
					higgsname += "_x0";
				}

			}
			else
			{
				selectedParticles = &jetParticles;

				if (lheParticle->pdgId == DefaultValues::pdgIdGluon)
				{
					selectedParticles->nGluons += 1;
					++numberGluons;
					jetname += "g";
				}
				else if ((lheParticle->pdgId) == 25)
				{
					selectedParticles = &higgsParticles;
					selectedParticles->nHiggsBosons += 1;
					jetname += "_x0";
				}


				else if ((lheParticle->pdgId) == 1)
				{
					selectedParticles->nLightQuarks += 1;
					++numberOtherQuarks;
					jetname += "d";
				}
			
				else if ((lheParticle->pdgId) == -1)
				{
					selectedParticles->nLightQuarks += 1;
					++numberOtherQuarks;
					jetname += "dx";
				}

				else if ((lheParticle->pdgId) == 2)
				{
					selectedParticles->nLightQuarks += 1;
					++numberOtherQuarks;
					jetname += "u";
				}
			
				else if ((lheParticle->pdgId) == -2)
				{
					selectedParticles->nLightQuarks += 1;
					++numberOtherQuarks;
					jetname += "ux";
				}

				else if ((lheParticle->pdgId) == 3)
				{
					selectedParticles->nLightQuarks += 1;
					++numberOtherQuarks;
					jetname += "s";
				}
			
				else if ((lheParticle->pdgId) == -3)
				{
					selectedParticles->nLightQuarks += 1;
					++numberOtherQuarks;
					jetname += "sx";
				}

				else if ((lheParticle->pdgId) == 4)
				{
					selectedParticles->nLightQuarks += 1;
					++numberOtherQuarks;
					jetname += "c";
				}
			
				else if ((lheParticle->pdgId) == -4)
				{
					selectedParticles->nLightQuarks += 1;
					++numberOtherQuarks;
					jetname += "cx";
				}

				else if ((lheParticle->pdgId) == 5)
				{
					selectedParticles->nHeavyQuarks += 1;
					++numberBottomQuarks;
					jetname += "b";
				}
			
				else if ((lheParticle->pdgId) == -5)
				{
					selectedParticles->nHeavyQuarks += 1;
					++numberBottomQuarks;
					jetname += "bx";
				}
			}
			
			selectedParticles->momenta.push_back(&(*lheParticle));
			
			

			//LOG(INFO) << lheParticle->pdgId << ", " << lheParticle->p4 << ", " << ", " << lheParticle->status << ", " << event.m_lheParticles->subprocessCode << ", " << lheParticle->colourLineIndices.first << ", " << lheParticle->colourLineIndices.second;
			if (product.m_lheParticlesSortedForMadGraph.size() < 7)
			{
				product.m_lheParticlesSortedForMadGraph.push_back(const_cast<KLHEParticle*>(&(*lheParticle)));
			}
		}
		
		
		// checks and corrections for Higgs bosons
		if (higgsParticles.momenta.size() > 1)
		{
			//LOG(ERROR) << "Found " << higgsParticles.momenta.size() << " Higgs bosons, but expected 1! Take the first one.";
			higgsParticles.momenta.resize(1);
			higgsParticles.nHiggsBosons = 1;
		}
		else if (higgsParticles.momenta.size() > 1)
		{
			LOG(FATAL) << "Found no Higgs bosons, but expected 1!";
		}
		
//jetcorrections for naming
		
	//gluons
		//lighter quarks
		if ((jetname=="gc") ||
		    (jetname=="gd") ||
		    (jetname=="gs"))
		{
			jetname="gu";
		}
		else if ((jetname=="cg") ||
		         (jetname=="dg") ||
		         (jetname=="sg") ||
		         (jetname=="ug"))
		{
			jetname="gu";
			std::swap(product.m_lheParticlesSortedForMadGraph[3],product.m_lheParticlesSortedForMadGraph[4]);
		}
		//lighter antiquarks
		if ((jetname=="gcx") ||
		    (jetname=="gdx") ||
		    (jetname=="gsx"))
		{
			jetname="gux";
		}
		else if ((jetname=="cxg") ||
		         (jetname=="dxg") ||
		         (jetname=="sxg") ||
		         (jetname=="uxg"))
		{
			jetname="gux";
			std::swap(product.m_lheParticlesSortedForMadGraph[3],product.m_lheParticlesSortedForMadGraph[4]);
		}

		//bottom
		if (jetname=="bg")
		{
			jetname="gb";
			std::swap(product.m_lheParticlesSortedForMadGraph[3],product.m_lheParticlesSortedForMadGraph[4]);
		}

		if (jetname=="bxg")
		{
			jetname="gbx";
			std::swap(product.m_lheParticlesSortedForMadGraph[3],product.m_lheParticlesSortedForMadGraph[4]);
		}

	//uux ccx ddx ssx
		else if ((jetname=="ccx") ||
		    (jetname=="ddx") ||
		    (jetname=="ssx"))
		{
			jetname="uux";
		}
		else if ((jetname=="cxc") ||
		         (jetname=="dxd") ||
		         (jetname=="sxs") ||
		         (jetname=="uxu"))
		{
			jetname="uux";
			std::swap(product.m_lheParticlesSortedForMadGraph[3],product.m_lheParticlesSortedForMadGraph[4]);
		}
		
		
//initialcorrection for naming
	
	//gluons
		//lighter quarks
		if ((initialname=="gc") ||
		    (initialname=="gd") ||
		    (initialname=="gs"))
		{
			initialname="gu";
		}
		else if ((initialname=="cg") ||
		         (initialname=="dg") ||
		         (initialname=="sg") ||
		         (initialname=="ug"))
		{
			initialname="gu";
			std::swap(product.m_lheParticlesSortedForMadGraph[0],product.m_lheParticlesSortedForMadGraph[1]);
		}
		
		//lighter antiquarks
		if ((initialname=="gcx") ||
		    (initialname=="gdx") ||
		    (initialname=="gsx"))
		{
			initialname="gux";
		}
		else if ((initialname=="cxg") ||
		         (initialname=="dxg") ||
		         (initialname=="sxg") ||
		         (initialname=="uxg"))
		{
			initialname="gux";
			std::swap(product.m_lheParticlesSortedForMadGraph[0],product.m_lheParticlesSortedForMadGraph[1]);
		}
		//bottom
		if (initialname=="bg")
		{
			initialname="gb";
			std::swap(product.m_lheParticlesSortedForMadGraph[0],product.m_lheParticlesSortedForMadGraph[1]);
		}

		if (initialname=="bxg")
		{
			jetname="gbx";
			std::swap(product.m_lheParticlesSortedForMadGraph[0],product.m_lheParticlesSortedForMadGraph[1]);
		}


	//uux ccx ddx ssx
		else if ((initialname=="ccx") ||
		         (initialname=="ddx") ||
		         (initialname=="ssx"))
		{
			initialname="uux";
		}
		else if ((initialname=="cxc") ||
		         (initialname=="dxd") ||
		         (initialname=="sxs") ||
		         (initialname=="uxu"))
		{
			initialname="uux";
			std::swap(product.m_lheParticlesSortedForMadGraph[0],product.m_lheParticlesSortedForMadGraph[1]);
		}
		


		directoryname = initialname+higgsname+jetname;
		
		//LOG(INFO) << productionMode << directoryname;
		//LOG(INFO) << event.m_lheParticles->particles->size() << ": " << numberGluons << ", " << numberBottomQuarks << ", " << numberOtherQuarks << ", " << Utility::ToUnderlyingValue(productionMode);

		if ((jetParticles.nGluons==0)  &&
		    (jetParticles.nLightQuarks==0)  &&
		    (jetParticles.nHeavyQuarks==0) &&
		    (directoryname!="gg_x0"))
		{
			directoryname="bbx_x0";
		}

		if ((jetParticles.nGluons + jetParticles.nLightQuarks + jetParticles.nHeavyQuarks ==2) &&
		    (!(Utility::Contains(m_madGraphProcessDirectoriesByName, directoryname))))
		{
		
		}
		//if ((initialParticles.nLightQuarks==2) &&
		//    (jetParticles.nGluons==0))
		
		if (Utility::Contains(m_madGraphProcessDirectoriesByName, directoryname))
		{
			std::vector<CartesianRMFLV*> particleFourMomenta;
			for (std::vector<KLHEParticle*>::iterator madGraphLheParticle = product.m_lheParticlesSortedForMadGraph.begin();
			     madGraphLheParticle != product.m_lheParticlesSortedForMadGraph.end(); ++madGraphLheParticle)
			{
				particleFourMomenta.push_back(&((*madGraphLheParticle)->p4));
			}
		
			//std::string madGraphProcessDirectory = m_madGraphProcessDirectories.at(productionMode)[0];
			
			//std::string madGraphProcessDirectory = SafeMap::Get(madGraphProcessDirectoriesByName, directoryname)[0];
			std::string madGraphProcessDirectory = m_madGraphProcessDirectoriesByName.at(directoryname)[0];
			
			std::map<int, MadGraphTools*>* tmpMadGraphToolsMap = const_cast<std::map<int, MadGraphTools*>*>(&(SafeMap::Get(m_madGraphTools, madGraphProcessDirectory)));
			
			LOG(DEBUG) << "Processed event: run = " << event.m_eventInfo->nRun << ", lumi = " << event.m_eventInfo->nLumi << ", event = " << event.m_eventInfo->nEvent << ", pipeline = " << settings.GetName();
			LOG(DEBUG) << "Directory of matrixelement: " << madGraphProcessDirectory;
			
			// calculate the matrix elements for different mixing angles
			for (std::vector<float>::const_iterator mixingAngleOverPiHalf = settings.GetMadGraphMixingAnglesOverPiHalf().begin();
			     mixingAngleOverPiHalf != settings.GetMadGraphMixingAnglesOverPiHalf().end(); ++mixingAngleOverPiHalf)
			{
				MadGraphTools* tmpMadGraphTools = SafeMap::Get(*tmpMadGraphToolsMap, GetMixingAngleKey(*mixingAngleOverPiHalf));
				product.m_optionalWeights[GetLabelForWeightsMap(*mixingAngleOverPiHalf)] = tmpMadGraphTools->GetMatrixElementSquared(particleFourMomenta);
				//LOG(DEBUG) << *mixingAngleOverPiHalf << " --> " << product.m_optionalWeights[GetLabelForWeightsMap(*mixingAngleOverPiHalf)];
				//LOG(INFO) << "anlge " << *mixingAngleOverPiHalf;
			}
		}
		else
		{
			//LOG(ERROR) << "Process directory for production mode " << Utility::ToUnderlyingValue(productionMode) << " not found in settings with tag \"MadGraphProcessDirectories\"!";
			LOG(ERROR) << "Process directory for production mode " << directoryname << " not found in settings with tag \"MadGraphProcessDirectories\"!";
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

