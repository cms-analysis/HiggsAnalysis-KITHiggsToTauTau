
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
		std::string name = "";
		//std::map(<int>,<>);
		//Array to carry Directory Name consists of 
		//"incoming particle" "incoming particle" "higgs" "outgoing particle" "outgoing particle" "outgoing particle"
		std::string Names [6] = {"", "", "", "", "", ""};
		int Name_Index = 0;
		for (std::vector<KLHEParticle>::const_iterator lheParticle = event.m_lheParticles->particles.begin(); lheParticle != event.m_lheParticles->particles.end(); ++lheParticle)
		{
			ParticlesGroup* selectedParticles = nullptr;
			//construct name of events 
			//TODO update the jason file for ggh
			TParticlePDG* pdgParticle = m_databasePDG->GetParticle(lheParticle->pdgId);
			if (pdgParticle)
			{
				Names[Name_Index] = pdgParticle->GetName();
				Name_Index++;
			}

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
					higgsname += "_h0";
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
			
			

			LOG(INFO) << lheParticle->pdgId << ", " << lheParticle->p4 << ", " << ", " << lheParticle->status << ", " << event.m_lheParticles->subprocessCode << ", " << lheParticle->colourLineIndices.first << ", " << lheParticle->colourLineIndices.second;
			if (particleFourMomenta.size() < 7)
			{
				particleFourMomenta.push_back(&(lheParticle->p4));
			}






		}
		//Names for ingoing and outgoing particles
		initialname	= Names[0] + Names[1];
		jetname	= Names[3] + Names[4] + Names[5];
	        //print name of event
		/*std::cout << "Name: " << initialname << higgsname << jetname << std::endl;
		std::cout << "Jetname: " << jetname << std::endl;
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
			std::swap(particleFourMomenta[3],particleFourMomenta[4]);
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
			std::swap(particleFourMomenta[3],particleFourMomenta[4]);
		}

		//bottom
		if (jetname=="bg")
		{
			jetname="gb";
			std::swap(particleFourMomenta[3],particleFourMomenta[4]);
		}

		if (jetname=="bxg")
		{
			jetname="gbx";
			std::swap(particleFourMomenta[3],particleFourMomenta[4]);
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
			std::swap(particleFourMomenta[3],particleFourMomenta[4]);
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
			std::swap(particleFourMomenta[0],particleFourMomenta[1]);
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
			std::swap(particleFourMomenta[0],particleFourMomenta[1]);
		}
		//bottom
		if (initialname=="bg")
		{
			initialname="gb";
			std::swap(particleFourMomenta[0],particleFourMomenta[1]);
		}

		if (initialname=="bxg")
		{
			jetname="gbx";
			std::swap(particleFourMomenta[0],particleFourMomenta[1]);
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
			std::swap(particleFourMomenta[0],particleFourMomenta[1]);
		}

//vbf
	//jetname correction
	////GetName() has no specific order 
	//madgraph sorts particle before antiparticle in event names
	//puts gluons first
	//up type quarks second
	//downtype quarks third => gucdsb
		if ((jetname=="u_baru") || (jetname=="b_barb") || (jetname=="c_barc") || (jetname=="d_bard") || (jetname=="s_bars") ||
			(jetname=="sd") || (jetname=="sc") || (jetname=="bs") || (jetname=="su") || 
			(jetname=="dc") || (jetname=="du") ||
			(jetname=="bd") || (jetname=="cu") ||
			(jetname=="bu") ||
			(jetname=="s_bard_bar") || (jetname=="s_barc_bar") || (jetname=="b_bars_bar") || (jetname=="s_baru_bar") ||
                        (jetname=="d_barc_bar") || (jetname=="b_bard_bar") || (jetname=="d_baru_bar") ||
                        (jetname=="b_barc_bar") || (jetname=="c_baru_bar") ||
                        (jetname=="b_baru_bar") ||
                        (jetname=="s_bard") || (jetname=="s_barc") || (jetname=="s_barb") || (jetname=="s_baru") ||
                        (jetname=="d_barc") || (jetname=="d_barb") || (jetname=="d_baru") ||
                        (jetname=="c_barb") || (jetname=="c_baru") ||
                        (jetname=="b_baru") ||
                        (jetname=="d_bars") || (jetname=="c_bars") || (jetname=="b_bars") || (jetname=="u_bars") ||
                        (jetname=="c_bard") || (jetname=="b_bard") || (jetname=="u_bard") ||
                        (jetname=="b_barc") || (jetname=="u_barc") ||
                        (jetname=="u_barb"))
		{
			std::swap(particleFourMomenta[3], particleFourMomenta[4]);
		}
	//considering gluons (considered only the events that happen in the VBF sample)
	//3<->5, 4<->5
		if ((jetname=="b_bardg") || (jetname=="dd_barg") || (jetname=="u_bars_barg") || (jetname=="sd_barg") ||
			(jetname=="cug") || (jetname=="u_bars_barg") || (jetname=="cdg") || (jetname=="cc_barg") ||
			(jetname=="ubg") || (jetname=="ds_barg") || (jetname=="uug") || (jetname=="ddg") || (jetname=="ucg") ||
			(jetname=="uu_barg") || (jetname=="uc_barg") || (jetname=="db_barg") || (jetname=="ss_barg") || (jetname=="cu_barg"))
		{
			std::swap(particleFourMomenta[3], particleFourMomenta[5]);
			std::swap(particleFourMomenta[4], particleFourMomenta[5]);
		}
	//3<->5
		if ((jetname=="d_barc_barg") || (jetname=="cug") || (jetname=="d_baru_barg") || (jetname=="dug") || 
			(jetname=="c_bardg") || (jetname=="sug") || (jetname=="c_barug") || (jetname=="u_bardg"))
		{
			std::swap(particleFourMomenta[3], particleFourMomenta[5]);
		}
	//initialstate (basically the same as for jetname)
                if ((initialname=="u_baru") || (initialname=="b_barb") || (initialname=="c_barc") || (initialname=="d_bard") || (initialname=="s_bars") ||
                        (initialname=="sd") || (initialname=="sc") || (initialname=="sb") || (initialname=="su") ||
                        (initialname=="dc") || (initialname=="bc") || (initialname=="du") ||
                        (initialname=="bc") || (initialname=="cu") ||
                        (initialname=="bu") ||
                        (initialname=="s_bard_bar") || (initialname=="s_barc_bar") || (initialname=="b_bars_bar") || (initialname=="s_baru_bar") ||
                        (initialname=="d_barc_bar") || (initialname=="b_bard_bar") || (initialname=="d_baru_bar") ||
                        (initialname=="b_barc_bar") || (initialname=="c_baru_bar") ||
                        (initialname=="b_baru_bar") ||
                        (initialname=="s_bard") || (initialname=="s_barc") || (initialname=="s_barb") || (initialname=="s_baru") ||
                        (initialname=="d_barc") || (initialname=="d_barb") || (initialname=="d_baru") ||
                        (initialname=="c_barb") || (initialname=="c_baru") ||
                        (initialname=="b_baru") ||
                        (initialname=="d_bars") || (initialname=="c_bars") || (initialname=="b_bars") || (initialname=="u_bars") ||
                        (initialname=="c_bard") || (initialname=="b_bard") || (initialname=="u_bard") ||
                        (initialname=="b_barc") || (initialname=="u_barc") ||
                        (initialname=="u_barb") ||
			(initialname=="sg") || (initialname=="dg") || (initialname=="cg") || (initialname=="bg") || (initialname=="ug"))
                {
                        std::swap(particleFourMomenta[0], particleFourMomenta[1]);
                }


		directoryname = initialname+higgsname+jetname;
		//std::cout << "Directory Name: " << directoryname << std::endl;
		
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
		
		//this uses the reweighting json file
		if (Utility::Contains(m_madGraphProcessDirectoriesByName, directoryname))
		{
			//std::string madGraphProcessDirectory = m_madGraphProcessDirectories.at(productionMode)[0];
			
			//std::string madGraphProcessDirectory = SafeMap::Get(madGraphProcessDirectoriesByName, directoryname)[0];
			std::string madGraphProcessDirectory = m_madGraphProcessDirectoriesByName.at(directoryname)[0];
			std::cout << "testoutput LHS: " << madGraphProcessDirectory << std::endl;
			std::cout << "testoutput RHS: " << directoryname << std::endl;
			std::map<int, MadGraphTools*>* tmpMadGraphToolsMap = const_cast<std::map<int, MadGraphTools*>*>(&(SafeMap::Get(m_madGraphTools, madGraphProcessDirectory)));
			std::cout << "testoutput" << std::endl;
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
