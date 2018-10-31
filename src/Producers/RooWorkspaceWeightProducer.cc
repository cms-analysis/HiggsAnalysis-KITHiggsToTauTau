
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/RooWorkspaceWeightProducer.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "Artus/KappaAnalysis/interface/Utility/GeneratorInfo.h"

RooWorkspaceWeightProducer::RooWorkspaceWeightProducer(
		bool (setting_type::*GetSaveRooWorkspaceTriggerWeightAsOptionalOnly)(void) const,
		std::string (setting_type::*GetRooWorkspace)(void) const,
		std::vector<std::string>& (setting_type::*GetRooWorkspaceWeightNames)(void) const,
		std::vector<std::string>& (setting_type::*GetRooWorkspaceObjectNames)(void) const,
		std::vector<std::string>& (setting_type::*GetRooWorkspaceObjectArguments)(void) const
):
	GetSaveRooWorkspaceTriggerWeightAsOptionalOnly(GetSaveRooWorkspaceTriggerWeightAsOptionalOnly),
	GetRooWorkspace(GetRooWorkspace),
	GetRooWorkspaceWeightNames(GetRooWorkspaceWeightNames),
	GetRooWorkspaceObjectNames(GetRooWorkspaceObjectNames),
	GetRooWorkspaceObjectArguments(GetRooWorkspaceObjectArguments)
{
}

RooWorkspaceWeightProducer::RooWorkspaceWeightProducer():
		RooWorkspaceWeightProducer(&setting_type::GetSaveRooWorkspaceTriggerWeightAsOptionalOnly,
								   &setting_type::GetRooWorkspace,
								   &setting_type::GetRooWorkspaceWeightNames,
								   &setting_type::GetRooWorkspaceObjectNames,
								   &setting_type::GetRooWorkspaceObjectArguments)
{
}

void RooWorkspaceWeightProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);

	m_saveTriggerWeightAsOptionalOnly = (settings.*GetSaveRooWorkspaceTriggerWeightAsOptionalOnly)();

	m_scaleFactorMode =  HttEnumTypes::ToDataMcScaleFactorProducerMode(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy((settings.GetTriggerEfficiencyMode)())));

	TDirectory *savedir(gDirectory);
	TFile *savefile(gFile);
	std::cout << settings.GetRooWorkspace().c_str() <<std::endl;
	TFile f(settings.GetRooWorkspace().c_str());
	gSystem->AddIncludePath("-I$ROOFITSYS/include");
	m_workspace = (RooWorkspace*)f.Get("w");
	f.Close();
	gDirectory = savedir;
	gFile = savefile;
	// Load the names of the weight to be included from the workspace 
	m_weightNames = Utility::ParseMapTypes<int,std::string>(Utility::ParseVectorToMap((settings.*GetRooWorkspaceWeightNames)()));
	// Load all functions which can be used to retreive weights
	std::map<int,std::vector<std::string>> objectNames = Utility::ParseMapTypes<int,std::string>(Utility::ParseVectorToMap((settings.*GetRooWorkspaceObjectNames)()));
	// Load the arguments to be passed to the functions
	m_functorArgs = Utility::ParseMapTypes<int,std::string>(Utility::ParseVectorToMap((settings.*GetRooWorkspaceObjectArguments)()));
	for(auto objectName:objectNames)
	{
		for(size_t index = 0; index < objectName.second.size(); index++)
		{
			std::vector<std::string> objects;
			boost::split(objects, objectName.second[index], boost::is_any_of(","));
			for(auto object:objects)
			{
				std::cout << objectName.first << "    " << object.c_str() << "   " << m_functorArgs[objectName.first][index].c_str() << std::endl; 
				m_functors[objectName.first].push_back(m_workspace->function(object.c_str())->functor(m_workspace->argSet(m_functorArgs[objectName.first][index].c_str())));
			}
		}
	}
}

void RooWorkspaceWeightProducer::Produce( event_type const& event, product_type & product, 
	                     setting_type const& settings, metadata_type const& metadata) const
{

	for(auto weightNames:m_weightNames)
	{
		KLepton* lepton = product.m_flavourOrderedLeptons[weightNames.first];
		for(size_t index = 0; index < weightNames.second.size(); index++)
		{
			auto args = std::vector<double>{};
			std::vector<std::string> arguments;
			boost::split(arguments,  m_functorArgs.at(weightNames.first).at(index) , boost::is_any_of(","));
			for(auto arg:arguments)
			{
				if(arg=="m_pt" || arg=="e_pt")
				{
					args.push_back(lepton->p4.Pt());
				}
				if(arg=="m_eta")
				{
					args.push_back(lepton->p4.Eta());
				}
				if(arg=="e_eta")
				{
					KElectron* electron = static_cast<KElectron*>(lepton);
					args.push_back(electron->superclusterPosition.Eta());
				}
				if(arg=="m_iso" || arg=="e_iso")
				{
					args.push_back(SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, lepton, std::numeric_limits<double>::max()));
				}
				else if(arg=="dR")
				{
					args.push_back(ROOT::Math::VectorUtil::DeltaR(product.m_flavourOrderedLeptons[0]->p4, product.m_flavourOrderedLeptons[1]->p4));
				}
				else if(arg=="njets")
				{
					args.push_back(1);
				}
			}
			if ((weightNames.second.at(index).find("triggerWeight") != std::string::npos && m_saveTriggerWeightAsOptionalOnly) ||
			    (weightNames.second.at(index).find("emuQcd") != std::string::npos))
			{
				product.m_optionalWeights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = m_functors.at(weightNames.first).at(index)->eval(args.data());
			}
			else
			{
				product.m_weights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = m_functors.at(weightNames.first).at(index)->eval(args.data());
			}
		}
	}
	if((product.m_weights.find("idweight_1") != product.m_weights.end()) && (product.m_weights.find("isoweight_1") != product.m_weights.end()))
	{
		product.m_weights["identificationWeight_1"] = product.m_weights["idweight_1"]*product.m_weights["isoweight_1"];
		product.m_weights["idweight_1"] = 1.0;
		product.m_weights["isoweight_1"] = 1.0;
	}
	if((product.m_weights.find("idweight_2") != product.m_weights.end()) && (product.m_weights.find("isoweight_2") != product.m_weights.end()))
	{
		product.m_weights["identificationWeight_2"] = product.m_weights["idweight_2"]*product.m_weights["isoweight_2"];
		product.m_weights["idweight_2"] = 1.0;
		product.m_weights["isoweight_2"] = 1.0;
	}
	if(product.m_weights.find("idIsoWeight_1") != product.m_weights.end())
	{
		product.m_weights["identificationWeight_1"] = product.m_weights["idIsoWeight_1"];
		product.m_weights["idIsoWeight_1"] = 1.0;
	}
	if(product.m_weights.find("idIsoWeight_2") != product.m_weights.end())
	{
		product.m_weights["identificationWeight_2"] = product.m_weights["idIsoWeight_2"];
		product.m_weights["idIsoWeight_2"] = 1.0;
	}
}

// ==========================================================================================

EETriggerWeightProducer::EETriggerWeightProducer() :
		RooWorkspaceWeightProducer(&setting_type::GetSaveEETriggerWeightAsOptionalOnly,
								   &setting_type::GetEETriggerWeightWorkspace,
								   &setting_type::GetEETriggerWeightWorkspaceWeightNames,
								   &setting_type::GetEETriggerWeightWorkspaceObjectNames,
								   &setting_type::GetEETriggerWeightWorkspaceObjectArguments)
{
}

void EETriggerWeightProducer::Produce( event_type const& event, product_type & product,
						   setting_type const& settings, metadata_type const& metadata) const
{
	double eTrigWeight = 1.0;

	for(auto weightNames:m_weightNames)
	{
		KLepton* lepton = product.m_flavourOrderedLeptons[weightNames.first];
		for(size_t index = 0; index < weightNames.second.size(); index++)
		{
			if(weightNames.second.at(index).find("triggerWeight") == std::string::npos)
				continue;
			auto args = std::vector<double>{};
			std::vector<std::string> arguments;
			boost::split(arguments,  m_functorArgs.at(weightNames.first).at(index) , boost::is_any_of(","));
			for(auto arg:arguments)
			{
				if(arg=="e_pt")
				{
					args.push_back(lepton->p4.Pt());
				}
				if(arg=="e_eta")
				{
					KElectron* electron = static_cast<KElectron*>(lepton);
					args.push_back(electron->superclusterPosition.Eta());
				}
				eTrigWeight *= (1.0 - m_functors.at(weightNames.first).at(index)->eval(args.data()));
			}
		}
	}
	if(m_saveTriggerWeightAsOptionalOnly)
	{
		product.m_optionalWeights["triggerWeight_1"] = 1-eTrigWeight;
	}
	else{
		product.m_weights["triggerWeight_1"] = 1-eTrigWeight;
	}
}

// ==========================================================================================

MuMuTriggerWeightProducer::MuMuTriggerWeightProducer() :
		RooWorkspaceWeightProducer(&setting_type::GetSaveMuMuTriggerWeightAsOptionalOnly,
								   &setting_type::GetMuMuTriggerWeightWorkspace,
								   &setting_type::GetMuMuTriggerWeightWorkspaceWeightNames,
								   &setting_type::GetMuMuTriggerWeightWorkspaceObjectNames,
								   &setting_type::GetMuMuTriggerWeightWorkspaceObjectArguments)
{
}

void MuMuTriggerWeightProducer::Produce( event_type const& event, product_type & product,
						   setting_type const& settings, metadata_type const& metadata) const
{
	double muTrigWeight = 1.0;

	for(auto weightNames:m_weightNames)
	{
		KLepton* lepton = product.m_flavourOrderedLeptons[weightNames.first];
		for(size_t index = 0; index < weightNames.second.size(); index++)
		{
			if(weightNames.second.at(index).find("triggerWeight") == std::string::npos)
				continue;
			auto args = std::vector<double>{};
			std::vector<std::string> arguments;
			boost::split(arguments,  m_functorArgs.at(weightNames.first).at(index) , boost::is_any_of(","));
			for(auto arg:arguments)
			{
				if(arg=="m_pt")
				{
					args.push_back(lepton->p4.Pt());
				}
				if(arg=="m_eta")
				{
					args.push_back(lepton->p4.Eta());
				}
			}
			muTrigWeight *= (1.0 - m_functors.at(weightNames.first).at(index)->eval(args.data()));
		}
	}
	if(m_saveTriggerWeightAsOptionalOnly)
	{
		product.m_optionalWeights["triggerWeight_1"] = 1-muTrigWeight;
	}
	else{
		product.m_weights["triggerWeight_1"] = 1-muTrigWeight;
	}
}

// ==========================================================================================

TauTauTriggerWeightProducer::TauTauTriggerWeightProducer() :
		RooWorkspaceWeightProducer(&setting_type::GetSaveTauTauTriggerWeightAsOptionalOnly,
								   &setting_type::GetTauTauTriggerWeightWorkspace,
								   &setting_type::GetTauTauTriggerWeightWorkspaceWeightNames,
								   &setting_type::GetTauTauTriggerWeightWorkspaceObjectNames,
								   &setting_type::GetTauTauTriggerWeightWorkspaceObjectArguments)
{
}

void TauTauTriggerWeightProducer::Produce( event_type const& event, product_type & product,
						   setting_type const& settings, metadata_type const& metadata) const
{
	double tauTrigWeight = 1.0;

	for(auto weightNames:m_weightNames)
	{
		KLepton* lepton = product.m_flavourOrderedLeptons[weightNames.first];
		KLepton* originalLepton = const_cast<KLepton*>(SafeMap::GetWithDefault(product.m_originalLeptons, const_cast<const KLepton*>(lepton), const_cast<const KLepton*>(lepton)));
		KappaEnumTypes::GenMatchingCode genMatchingCode = KappaEnumTypes::GenMatchingCode::NONE;
		if (settings.GetUseUWGenMatching())
		{
			genMatchingCode = GeneratorInfo::GetGenMatchingCodeUW(event, originalLepton);
		}
		else
		{
			KGenParticle* genParticle = product.m_flavourOrderedGenLeptons[weightNames.first];
			if (genParticle)
				genMatchingCode = GeneratorInfo::GetGenMatchingCode(genParticle);
			else
				genMatchingCode = KappaEnumTypes::GenMatchingCode::IS_FAKE;
		}
		for(size_t index = 0; index < weightNames.second.size(); index++)
		{
			if(weightNames.second.at(index).find("triggerWeight") == std::string::npos)
				continue;
			if(m_functors.at(weightNames.first).size() != 2)
			{
				LOG(WARNING) << "TauTauTriggerWeightProducer: two object names are required in json config file. Trigger weight will be set to 1.0!";
				break;
			}
			auto args = std::vector<double>{};
			std::vector<std::string> arguments;
			boost::split(arguments,  m_functorArgs.at(weightNames.first).at(index) , boost::is_any_of(","));
			for(auto arg:arguments)
			{
				if(arg=="t_pt")
				{
					args.push_back(lepton->p4.Pt());
				}
				if(arg=="t_eta")
				{
					args.push_back(lepton->p4.Eta());
				}
				if(arg=="t_dm")
				{
					KTau* tau = static_cast<KTau*>(lepton);
					args.push_back(tau->decayMode);
				}
			}
			if(genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_TAU_HAD_DECAY)
			{
				tauTrigWeight = m_functors.at(weightNames.first).at(index)->eval(args.data());
			}
			else
			{
				tauTrigWeight = m_functors.at(weightNames.first).at(index+1)->eval(args.data());
			}
			if(m_saveTriggerWeightAsOptionalOnly)
			{
				product.m_optionalWeights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = tauTrigWeight;
			}
			else{
				product.m_weights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = tauTrigWeight;
			}
		}
	}
}

// ==========================================================================================

MuTauTriggerWeightProducer::MuTauTriggerWeightProducer() :
		RooWorkspaceWeightProducer(&setting_type::GetSaveMuTauTriggerWeightAsOptionalOnly,
								   &setting_type::GetMuTauTriggerWeightWorkspace,
								   &setting_type::GetMuTauTriggerWeightWorkspaceWeightNames,
								   &setting_type::GetMuTauTriggerWeightWorkspaceObjectNames,
								   &setting_type::GetMuTauTriggerWeightWorkspaceObjectArguments)
{
}

void MuTauTriggerWeightProducer::Produce( event_type const& event, product_type & product,
						   setting_type const& settings, metadata_type const& metadata) const
{
	double muTrigWeight(1.0), tauTrigWeight(1.0);

	for(auto weightNames:m_weightNames)
	{
		// muon-tau cross trigger scale factors currently depend only on tau pt and eta
		KLepton* lepton = product.m_flavourOrderedLeptons[weightNames.first];
		KLepton* originalLepton = const_cast<KLepton*>(SafeMap::GetWithDefault(product.m_originalLeptons, const_cast<const KLepton*>(lepton), const_cast<const KLepton*>(lepton)));
		KappaEnumTypes::GenMatchingCode genMatchingCode = KappaEnumTypes::GenMatchingCode::NONE;
		if (settings.GetUseUWGenMatching())
		{
			genMatchingCode = GeneratorInfo::GetGenMatchingCodeUW(event, originalLepton);
		}
		else
		{
			KGenParticle* genParticle = product.m_flavourOrderedGenLeptons[weightNames.first];
			if (genParticle)
				genMatchingCode = GeneratorInfo::GetGenMatchingCode(genParticle);
			else
				genMatchingCode = KappaEnumTypes::GenMatchingCode::IS_FAKE;
		}
		for(size_t index = 0; index < weightNames.second.size(); index++)
		{
			if(weightNames.second.at(index).find("triggerWeight") == std::string::npos)
				continue;
			if(lepton->flavour() == KLeptonFlavour::TAU && m_functors.at(weightNames.first).size() != 2)
			{
				LOG(WARNING) << "MuTauTriggerWeightProducer: two object names are required for tau leg in json config file. Trigger weight for this leg will be set to 1.0!";
				if(m_saveTriggerWeightAsOptionalOnly)
				{
					product.m_optionalWeights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = 1.0;
				}
				else{
					product.m_weights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = 1.0;
				}
				break;
			}
			auto args = std::vector<double>{};
			std::vector<std::string> arguments;
			boost::split(arguments,  m_functorArgs.at(weightNames.first).at(index) , boost::is_any_of(","));
			for(auto arg:arguments)
			{
				if(arg=="m_pt" || arg=="t_pt")
				{
					args.push_back(lepton->p4.Pt());
				}
				if(arg=="m_eta" || arg=="t_eta")
				{
					args.push_back(lepton->p4.Eta());
				}
			}
			if(lepton->flavour() == KLeptonFlavour::TAU)
			{
				if(genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_TAU_HAD_DECAY)
				{
					tauTrigWeight = m_functors.at(weightNames.first).at(index)->eval(args.data());
				}
				else
				{
					tauTrigWeight = m_functors.at(weightNames.first).at(index+1)->eval(args.data());
				}
				if(m_saveTriggerWeightAsOptionalOnly)
				{
					product.m_optionalWeights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = tauTrigWeight;
				}
				else{
					product.m_weights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = tauTrigWeight;
				}
			}
			else
			{
				muTrigWeight = m_functors.at(weightNames.first).at(index)->eval(args.data());
				if(m_saveTriggerWeightAsOptionalOnly)
				{
					product.m_optionalWeights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = muTrigWeight;
				}
				else{
					product.m_weights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = muTrigWeight;
				}
			}
		}
	}
}

LeptonTauTrigger2017WeightProducer::LeptonTauTrigger2017WeightProducer() :
		RooWorkspaceWeightProducer(&setting_type::GetSaveLeptonTauTrigger2017WeightAsOptionalOnly,
								   &setting_type::GetLeptonTauTrigger2017WeightWorkspace,
								   &setting_type::GetLeptonTauTrigger2017WeightWorkspaceWeightNames,
								   &setting_type::GetLeptonTauTrigger2017WeightWorkspaceObjectNames,
								   &setting_type::GetLeptonTauTrigger2017WeightWorkspaceObjectArguments)
{
}

void LeptonTauTrigger2017WeightProducer::Produce( event_type const& event, product_type & product,
						   setting_type const& settings, metadata_type const& metadata) const
{
	double leptonTrigEffSingle_mc(1.0), leptonTrigEffSingle_data(1.0), leptonTrigEffCross_mc(1.0), leptonTrigEffCross_data(1.0);
	double leptonTauTrigWeight = 1.0;

	for(auto weightNames:m_weightNames)
	{
		// muon-tau cross trigger scale factors currently depend only on tau pt and eta
		KLepton* lepton = product.m_flavourOrderedLeptons[weightNames.first];
		KLepton* originalLepton = const_cast<KLepton*>(SafeMap::GetWithDefault(product.m_originalLeptons, const_cast<const KLepton*>(lepton), const_cast<const KLepton*>(lepton)));
		
		for(size_t index = 0; index < weightNames.second.size(); index++)
		{
			if(weightNames.second.at(index).find("triggerWeight") == std::string::npos && weightNames.second.at(index).find("_triggerEff") == std::string::npos)
			{
				continue;
			}

			auto args = std::vector<double>{};
			std::vector<std::string> arguments;
			boost::split(arguments,  m_functorArgs.at(weightNames.first).at(index) , boost::is_any_of(","));
			for(auto arg:arguments)
			{
				if(arg=="m_pt" || arg=="t_pt" || "e_pt")
				{
					args.push_back(lepton->p4.Pt());
				}
				if(arg=="m_eta" || arg=="t_eta" || "e_eta")
				{
					args.push_back(lepton->p4.Eta());
				}
				if(arg=="m_phi" || arg=="t_phi" || "e_phi")
				{
					args.push_back(lepton->p4.Phi());
				}
				if(arg=="m_iso"|| "e_iso")
				{
					args.push_back(SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, lepton, std::numeric_limits<double>::max()));
				}
			}
			if(m_scaleFactorMode == HttEnumTypes::DataMcScaleFactorProducerMode::CROSS_TRIGGERS) //For 2017 cross triggers
			{
				if (lepton->flavour() == KLeptonFlavour::MUON)
				{
					LOG(DEBUG) << weightNames.second.at(index) << std::endl;
					if(weightNames.second.at(index) == "m_triggerEffSingle_mc") 
					{
						leptonTrigEffSingle_mc = m_functors.at(weightNames.first).at(index)->eval(args.data());
						LOG(DEBUG) << "muTrigEffSingle_mc:  " << leptonTrigEffSingle_mc << std::endl;
					}
					else if (weightNames.second.at(index) == "m_triggerEffCross_mc")
					{
						leptonTrigEffCross_mc = m_functors.at(weightNames.first).at(index)->eval(args.data());
						LOG(DEBUG) << "muTrigEffCross_mc:  " << leptonTrigEffCross_mc << std::endl;
					}
					else if (weightNames.second.at(index) == "m_triggerEffSingle_data") 
					{
						leptonTrigEffSingle_data = m_functors.at(weightNames.first).at(index)->eval(args.data());
						LOG(DEBUG) << "muTrigEffSingle_data:  " << leptonTrigEffSingle_data << std::endl;
					}
					else if (weightNames.second.at(index) == "m_triggerEffCross_data")
					{
						leptonTrigEffCross_data = m_functors.at(weightNames.first).at(index)->eval(args.data());
						LOG(DEBUG) << "muTrigEffCross_data:  " << leptonTrigEffCross_data << std::endl;
					}
				}
				else if (lepton->flavour() == KLeptonFlavour::ELECTRON)
				{
					LOG(DEBUG) << weightNames.second.at(index) << std::endl;
					if(weightNames.second.at(index) == "e_triggerEffSingle_mc") 
					{
						leptonTrigEffSingle_mc = m_functors.at(weightNames.first).at(index)->eval(args.data());
						LOG(DEBUG) << "eleTrigEffSingle_mc:  " << leptonTrigEffSingle_mc << std::endl;
					}
					else if (weightNames.second.at(index) == "e_triggerEffCross_mc")
					{
						leptonTrigEffCross_mc = m_functors.at(weightNames.first).at(index)->eval(args.data());
						LOG(DEBUG) << "eleTrigEffCross_mc:  " << leptonTrigEffCross_mc << std::endl;
					}
					else if (weightNames.second.at(index) == "e_triggerEffSingle_data") 
					{
						leptonTrigEffSingle_data = m_functors.at(weightNames.first).at(index)->eval(args.data());
						LOG(DEBUG) << "eleTrigEffSingle_data:  " << leptonTrigEffSingle_data << std::endl;
					}
					else if (weightNames.second.at(index) == "e_triggerEffCross_data")
					{
						leptonTrigEffCross_data = m_functors.at(weightNames.first).at(index)->eval(args.data());
						LOG(DEBUG) << "eleTrigEffCross_data:  " << leptonTrigEffCross_data << std::endl;
					}
				}
			}
		}
	}
	//std::cout << "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" << std::endl;
	if(m_scaleFactorMode == HttEnumTypes::DataMcScaleFactorProducerMode::CROSS_TRIGGERS) //For 2017 cross triggers
	{
		assert((product.m_tautriggerefficienciesMC.size() == 1) &&
		(product.m_tautriggerefficienciesData.size() == 1));

		double efficiencyData = leptonTrigEffSingle_data*(1.0-product.m_tautriggerefficienciesData[0]) + leptonTrigEffCross_data*product.m_tautriggerefficienciesData[0];
		double efficiencyMc = leptonTrigEffSingle_mc*(1.0-product.m_tautriggerefficienciesMC[0])  + leptonTrigEffCross_mc*product.m_tautriggerefficienciesMC[0];
		leptonTauTrigWeight = ((efficiencyMc == 0.0) ? 1.0 : (efficiencyData / efficiencyMc));

		LOG(DEBUG) << "-------------------------------------------------------------------------------------------------------------------------" << std::endl;
		LOG(DEBUG) << "dataEff: " << efficiencyData << std::endl;
		LOG(DEBUG) << "MCEff: " << efficiencyMc << std::endl;
		LOG(DEBUG) << "weight: " << leptonTauTrigWeight << std::endl;
		LOG(DEBUG) << "-------------------------------------------------------------------------------------------------------------------------" << std::endl;
		product.m_weights[std::string("totalTriggerWeight")] = leptonTauTrigWeight;
	}
}
