
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

void MadGraphReweightingProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);

	// parsing settings
	//std::map<std::string, std::vector<std::string> > madGraphProcessDirectoriesByName;
	std::map<int, std::vector<std::string> > madGraphProcessDirectoriesByIndex = Utility::ParseMapTypes<int, std::string>(
			Utility::ParseVectorToMap(settings.GetMadGraphProcessDirectories()),
			m_madGraphProcessDirectoriesByName
	);
	/*for (std::map<int, std::vector<std::string> >::const_iterator processDirectories = madGraphProcessDirectoriesByIndex.begin();
	     processDirectories != madGraphProcessDirectoriesByIndex.end(); ++processDirectories)
	{
		m_madGraphProcessDirectories[static_cast<HttEnumTypes::MadGraphProductionModeGGH>(processDirectories->first)] = processDirectories->second;
	}
	for (std::map<std::string, std::vector<std::string> >::const_iterator processDirectories = m_madGraphProcessDirectoriesByName.begin();
	     processDirectories != m_madGraphProcessDirectoriesByName.end(); ++processDirectories)
	{
		m_madGraphProcessDirectories[HttEnumTypes::ToMadGraphProductionModeGGH(processDirectories->first)] = processDirectories->second;
	}*/
	
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
		

		std::string directoryname = "";
		std::string initialname = "";
		std::string jetname = "";
		std::string higgsname = "";
		//std::map(<int>,<>);
		//Array to carry Directory Name consists of 
		//"incoming particle" "incoming particle" "higgs" "outgoing particle" "outgoing particle" "outgoing particle"
		std::string Names [6] = {"", "", "", "", "", ""};
		int Name_Index = 0;
		for (std::vector<KLHEParticle>::const_iterator lheParticle = event.m_lheParticles->particles.begin(); lheParticle != event.m_lheParticles->particles.end(); ++lheParticle)
		{
			ParticlesGroup* selectedParticles = nullptr;
			//construct name of events 
			TParticlePDG* pdgParticle = m_databasePDG->GetParticle(lheParticle->pdgId);
			if (pdgParticle)
			{
				//check if it's an Initial Particle, Higgsboson or Jet Particle
				if (lheParticle->status == -1)
				{
					//LOG(WARNING) << "InitalParticle: " << pdgParticle->GetName();
					selectedParticles = &initialParticles;
				}
	                        else if (Utility::Contains(settings.GetBosonPdgIds(), std::abs(lheParticle->pdgId)))
	                        {
	                                //LOG(WARNING) << "HiggsParticle: " << pdgParticle->GetName();
					selectedParticles = &higgsParticles;
	                                selectedParticles->nHiggsBosons += 1;
	
                                	if ((lheParticle->pdgId) == 25)
	                                {
	                                        selectedParticles = &higgsParticles;
	                                        selectedParticles->nHiggsBosons += 1;
	                                        higgsname += "_h0";
	                                }
	                        }
				else {
					selectedParticles = &jetParticles;
					//LOG(WARNING) << "JetParticle: " << pdgParticle->GetName();
				}
				//construct the name
				Names[Name_Index] = pdgParticle->GetName();
				if (Names[Name_Index]=="g"){
					numberGluons += 1;
					selectedParticles->nGluons += 1;
				}
				else if ((Names[Name_Index]=="b") || (Names[Name_Index]=="b_bar")){
					numberBottomQuarks += 1;
					selectedParticles->nHeavyQuarks += 1;
				}
				else if ((Names[Name_Index]=="u") || (Names[Name_Index]=="c") || (Names[Name_Index]=="d") || (Names[Name_Index]=="s") ||
					(Names[Name_Index]=="u_bar") || (Names[Name_Index]=="c_bar") || (Names[Name_Index]=="d_bar") || (Names[Name_Index]=="s_bar")){
					numberOtherQuarks += 1;
					selectedParticles->nLightQuarks += 1;
				}
				else if (Names[Name_Index]=="h0"){//do nothing, everything is fine
				}
				else{LOG(ERROR) << "This process contains a '" << Names[Name_Index] << "' which should not be here!";}
				Name_Index++;
			}

			selectedParticles->momenta.push_back(&(*lheParticle));

			//LOG(INFO) << lheParticle->pdgId << ", " << lheParticle->p4 << ", " << ", " << lheParticle->status << ", " << event.m_lheParticles->subprocessCode << ", " << lheParticle->colourLineIndices.first << ", " << lheParticle->colourLineIndices.second;
			if (product.m_lheParticlesSortedForMadGraph.size() < 7)
			{
				product.m_lheParticlesSortedForMadGraph.push_back(const_cast<KLHEParticle*>(&(*lheParticle)));
			}
		}
		//Names for incoming and outgoing particles
		initialname	= Names[0] + Names[1];
		jetname	= Names[3] + Names[4] + Names[5];
	        //print name of event
		//LOG(WARNING) << "Name: " << initialname << higgsname << jetname;
		/*std::cout << "Jetname: " << jetname << std::endl;
		std::cout << "Initalname: " << initialname << std::endl;
		std::cout << "Higgsname: " << higgsname << std::endl;*/
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
		//swapping four momenta
		//jet correction

		//pdgParticle->GetName() has no specific order 
		//madgraph sorts particle before antiparticle
		//puts gluons first
		//up type quarks second
		//downtype quarks third
		//heavy quarks last => the order is: g u c d s u_bar c_bar d_bar s_bar b b_bar
		if ((jetname=="u_baru") || (jetname=="b_barb") || (jetname=="c_barc") || (jetname=="d_bard") || (jetname=="s_bars") ||
			(jetname=="bs") || (jetname=="bd") || (jetname=="bc") || (jetname=="bu") ||
			(jetname=="sd") || (jetname=="sc") || (jetname=="su") || 
			(jetname=="dc") || (jetname=="du") ||
			(jetname=="cu") ||
			(jetname=="b_bars_bar") || (jetname=="b_bard_bar") || (jetname=="b_barc_bar") || (jetname=="b_baru_bar") ||
			(jetname=="s_bard_bar") || (jetname=="s_barc_bar") || (jetname=="s_baru_bar") ||
                        (jetname=="d_barc_bar") || (jetname=="d_baru_bar") ||
                        (jetname=="c_baru_bar") ||
                        (jetname=="b_bars") ||(jetname =="b_bard") ||(jetname =="b_barc") ||(jetname =="b_baru") ||
			(jetname=="bs_bar") || (jetname=="s_bard") || (jetname=="s_barc") || (jetname=="s_baru") ||
                        (jetname=="bd_bar") || (jetname=="d_bars") || (jetname=="d_barc") || (jetname=="d_baru") ||
                        (jetname=="bc_bar") || (jetname=="c_bars") || (jetname=="c_bard") || (jetname=="c_baru") ||
                        (jetname=="bu_bar") || (jetname=="u_bars") || (jetname=="u_bard") || (jetname=="u_barc") ||
			(initialname=="sg") || (initialname=="dg") || (initialname=="cg") || (initialname=="bg") || (initialname=="ug") ||
			(initialname=="sxg") || (initialname=="dxg") || (initialname=="cxg") || (initialname=="bxg") || (initialname=="uxg"))
		{
			std::swap(product.m_lheParticlesSortedForMadGraph[3], product.m_lheParticlesSortedForMadGraph[4]);
		}
		//3 Jets
		//3<->5, 4<->5
		//if ((jetname=="b_bardg") || (jetname=="dd_barg") || (jetname=="u_bars_barg") || (jetname=="sd_barg") ||
		//	(jetname=="cug") || (jetname=="u_bars_barg") || (jetname=="cdg") || (jetname=="cc_barg") ||
		//	(jetname=="ubg") || (jetname=="ds_barg") || (jetname=="uug") || (jetname=="ddg") || (jetname=="ucg") ||
		//	(jetname=="uu_barg") || (jetname=="uc_barg") || (jetname=="db_barg") || (jetname=="ss_barg") || (jetname=="cu_barg") ||
		//	(jetname=="ucg") || (jetname=="udg") || (jetname=="usg") || (jetname=="ubg") ||
		//	(jetname=="cdg") || (jetname=="csg") || (jetname=="cbg") ||
		//	(jetname=="dsg") || (jetname=="dbg") ||
		//	(jetname=="sbg") ||
		//	(jetname=="bbg"))
		//{
		//	std::swap(product.m_lheParticlesSortedForMadGraph[3], product.m_lheParticlesSortedForMadGraph[5]);
		//	std::swap(product.m_lheParticlesSortedForMadGraph[4], product.m_lheParticlesSortedForMadGraph[5]);
		//}
		////3<->5
		//if ((jetname=="bbg") ||(jetname=="bug") || (jetname=="bcg") || (jetname=="bdg") || (jetname=="bsg") ||
		//	(jetname=="ssg") || (jetname=="sdg") || (jetname=="scg") || (jetname=="sug") ||
		//	(jetname=="ddg") || (jetname=="dcg") || (jetname=="dug") ||
		//	(jetname=="ccg") || (jetname=="cug") ||
		//	(jetname=="uug") ||
		//	(jetname=="ugg") || (jetname=="cgg") || (jetname=="dgg") || (jetname=="sgg") || (jetname=="bgg") ||
		//	(jetname=="u_bargg") || (jetname=="c_bargg") || (jetname=="d_bargg") || (jetname=="s_bargg") || (jetname=="b_bargg"))
		//{
		//	std::swap(product.m_lheParticlesSortedForMadGraph[3], product.m_lheParticlesSortedForMadGraph[5]);
		//}
		//initialstate correction (basically the same as for jet)
                if ((initialname=="u_baru") || (initialname=="b_barb") || (initialname=="c_barc") || (initialname=="d_bard") || (initialname=="s_bars") ||
                        (initialname=="sd") || (initialname=="sc") || (initialname=="sb") || (initialname=="su") ||
                        (initialname=="dc") || (initialname=="bc") || (initialname=="du") ||
                        (initialname=="bc") || (initialname=="cu") ||
                        (initialname=="bu") ||
                        (initialname=="s_bard_bar") || (initialname=="s_barc_bar") || (initialname=="b_bars_bar") || (initialname=="s_baru_bar") ||
                        (initialname=="d_barc_bar") || (initialname=="b_bard_bar") || (initialname=="d_baru_bar") ||
                        (initialname=="b_barc_bar") || (initialname=="c_baru_bar") ||
                        (initialname=="b_baru_bar") ||
                        (initialname=="s_bard") || (initialname=="s_barc") || (initialname=="bs_bar") || (initialname=="s_baru") ||
                        (initialname=="d_barc") || (initialname=="bd_bar") || (initialname=="d_baru") ||
                        (initialname=="bc_bar") || (initialname=="c_baru") ||
                        (initialname=="b_baru") ||
                        (initialname=="d_bars") || (initialname=="c_bars") || (initialname=="b_bars") || (initialname=="u_bars") ||
                        (initialname=="c_bard") || (initialname=="b_bard") || (initialname=="u_bard") ||
                        (initialname=="b_barc") || (initialname=="u_barc") ||
                        (initialname=="bu_bar") ||
			(initialname=="sg") || (initialname=="dg") || (initialname=="cg") || (initialname=="bg") || (initialname=="ug"))
                {
                        std::swap(product.m_lheParticlesSortedForMadGraph[0], product.m_lheParticlesSortedForMadGraph[1]);
                }


		directoryname = initialname+higgsname+jetname;
		//std::cout << "Directory Name: " << directoryname << std::endl;
		
		//LOG(INFO) << productionMode << directoryname;
		//LOG(INFO) << event.m_lheParticles->particles->size() << ": " << numberGluons << ", " << numberBottomQuarks << ", " << numberOtherQuarks << ", " << Utility::ToUnderlyingValue(productionMode);

		//there are only gg->h0 and bb_bar->h0 events for 0 jets
		if ((jetParticles.nGluons==0)  &&
		    (jetParticles.nLightQuarks==0)  &&
		    (jetParticles.nHeavyQuarks==0) &&
		    (directoryname!="gg_h0"))
		{
			directoryname="bb_bar_h0";
		}

		if ((jetParticles.nGluons + jetParticles.nLightQuarks + jetParticles.nHeavyQuarks ==2) &&
		    (!(Utility::Contains(m_madGraphProcessDirectoriesByName, directoryname))))
		{
		
		}
		//if ((initialParticles.nLightQuarks==2) &&
		//    (jetParticles.nGluons==0))
		
		//this uses the reweighting json file
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
			//calculate the old matrix element for reweighting
			MadGraphTools* tmpMadGraphTools = SafeMap::Get(*tmpMadGraphToolsMap, -1);
                        product.m_optionalWeights["madGraphWeightSample"] = tmpMadGraphTools->GetMatrixElementSquared(particleFourMomenta);
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
