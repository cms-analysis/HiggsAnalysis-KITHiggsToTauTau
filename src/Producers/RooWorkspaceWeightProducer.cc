
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
	TFile f((settings.*GetRooWorkspace)().c_str());
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
				else if(arg=="m_eta")
				{
					args.push_back(lepton->p4.Eta());
				}
				else if(arg=="e_eta")
				{
					KElectron* electron = static_cast<KElectron*>(lepton);
					args.push_back(electron->superclusterPosition.Eta());
				}
				else if(arg=="m_iso" || arg=="e_iso")
				{
					args.push_back(SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, lepton, std::numeric_limits<double>::max()));
				}
				else if(arg=="dR")
				{
					args.push_back(ROOT::Math::VectorUtil::DeltaR(product.m_flavourOrderedLeptons[0]->p4, product.m_flavourOrderedLeptons[1]->p4));
				}
				else if(arg=="njets")
				{
					args.push_back(1);//TODO this is wrong as fuck but not used
				}
				else if(arg=="HpT" || arg=="z_gen_pt")
				{
					args.push_back(product.m_genBosonLV.Pt());
				}
				else if(arg=="z_gen_mass")
				{
					args.push_back(product.m_genBosonLV.M());
				}
				else if(arg=="gt1_pt")
				{
					KGenTau leadingTau = event.m_genTaus->at(0);
					// std::cout << "leadingTau " << leadingTau.p4.Pt() << "\n";
					args.push_back(leadingTau.p4.Pt());
				}
				else if(arg=="gt1_eta")
				{
					KGenTau leadingTau = event.m_genTaus->at(0);
					// std::cout << "leadingTau " << leadingTau.p4.Eta() << "\n";
					args.push_back(leadingTau.p4.Eta());
				}
				else if(arg=="gt2_pt")
				{
					KGenTau trailingTau = event.m_genTaus->at(1);
					// std::cout << "trailingTau " << trailingTau.p4.Pt() << "\n";
					args.push_back(trailingTau.p4.Pt());
				}
				else if(arg=="gt2_eta")
				{
					KGenTau trailingTau = event.m_genTaus->at(1);
					// std::cout << "trailingTau " << trailingTau.p4.Eta() << "\n";
					args.push_back(trailingTau.p4.Eta());
				}
			}
			if ((weightNames.second.at(index).find("triggerWeight") != std::string::npos && m_saveTriggerWeightAsOptionalOnly) ||
			    (weightNames.second.at(index).find("emuQcd") != std::string::npos))
			{
				product.m_optionalWeights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = m_functors.at(weightNames.first).at(index)->eval(args.data());
			}
			else if (weightNames.second.at(index).find("quarkmassWeight") != std::string::npos)
			{
				//std::cout <<"quarkmassWeight:  " << product.m_genBosonLV.Pt() << " : " << m_functors.at(weightNames.first).at(index)->eval(args.data()) << std::endl;
				product.m_optionalWeights["quarkmassWeight"] = m_functors.at(weightNames.first).at(index)->eval(args.data());
			}
			else if (weightNames.second.at(index).find("quarkmassUpWeight") != std::string::npos)
			{
				//std::cout <<"quarkmassWeightup:  " << product.m_genBosonLV.Pt() << " : " << m_functors.at(weightNames.first).at(index)->eval(args.data()) << std::endl;
				product.m_optionalWeights["quarkmassUpWeight"] = m_functors.at(weightNames.first).at(index)->eval(args.data());
			}
			else if (weightNames.second.at(index).find("quarkmassDownWeight") != std::string::npos)
			{
				//std::cout <<"quarkmassWeightdown:  " << product.m_genBosonLV.Pt() << " : " << m_functors.at(weightNames.first).at(index)->eval(args.data()) << std::endl;
				product.m_optionalWeights["quarkmassDownWeight"] = m_functors.at(weightNames.first).at(index)->eval(args.data());
			}

			else if (weightNames.second.at(index).find("fullQuarkmassWeight") != std::string::npos)
			{
				//std::cout <<"fullQuarkmassWeight:  " <<product.m_genBosonLV.Pt() << " : " << m_functors.at(weightNames.first).at(index)->eval(args.data()) << std::endl;
				product.m_optionalWeights["fullQuarkmassWeight"] = m_functors.at(weightNames.first).at(index)->eval(args.data());
			}

			else if (weightNames.second.at(index).find("zPtReweightWeight") != std::string::npos)
			{
				product.m_optionalWeights["zPtReweightWeight"] = m_functors.at(weightNames.first).at(index)->eval(args.data());
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
				else if(arg=="gt1_pt")
				{
					KGenTau leadingTau = event.m_genTaus->at(0);
					// std::cout << "leadingTau " << leadingTau.p4.Pt() << "\n";
					args.push_back(leadingTau.p4.Pt());
				}
				else if(arg=="gt1_eta")
				{
					KGenTau leadingTau = event.m_genTaus->at(0);
					// std::cout << "leadingTau " << leadingTau.p4.Eta() << "\n";
					args.push_back(leadingTau.p4.Eta());
				}
				else if(arg=="gt2_pt")
				{
					KGenTau trailingTau = event.m_genTaus->at(1);
					// std::cout << "trailingTau " << trailingTau.p4.Pt() << "\n";
					args.push_back(trailingTau.p4.Pt());
				}
				else if(arg=="gt2_eta")
				{
					KGenTau trailingTau = event.m_genTaus->at(1);
					// std::cout << "trailingTau " << trailingTau.p4.Eta() << "\n";
					args.push_back(trailingTau.p4.Eta());
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

// ==========================================================================================

EmbeddingWeightProducer::EmbeddingWeightProducer() :
		RooWorkspaceWeightProducer(&setting_type::GetSaveEmbeddingWeightAsOptionalOnly,
								   &setting_type::GetEmbeddingWeightWorkspace,
								   &setting_type::GetEmbeddingWeightWorkspaceWeightNames,
								   &setting_type::GetEmbeddingWeightWorkspaceObjectNames,
								   &setting_type::GetEmbeddingWeightWorkspaceObjectArguments)
{
}

void EmbeddingWeightProducer::Produce( event_type const& event, product_type & product,
						   setting_type const& settings, metadata_type const& metadata) const
{
	for(auto weightNames:m_weightNames)
	{
		KLepton* lepton = product.m_flavourOrderedLeptons[weightNames.first];
		for(size_t index = 0; index < weightNames.second.size(); index++)
		{
			std::vector<double> args;
			std::vector<std::string> arguments;
			boost::split(arguments,  m_functorArgs.at(weightNames.first).at(index) , boost::is_any_of(","));
			for(auto arg:arguments)
			{
				if((arg=="m_pt") || (arg=="e_pt") || (arg=="t_pt"))
				{
					args.push_back(lepton->p4.Pt());
				}
				else if((arg=="m_eta") || (arg=="t_eta"))
				{
					args.push_back(lepton->p4.Eta());
				}
				else if(arg=="e_eta")
				{
					args.push_back(lepton->p4.Eta());
				}
				else if((arg=="m_iso") || (arg=="e_iso"))
				{
					args.push_back(SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, lepton, std::numeric_limits<double>::max()));
				}
				else if(arg=="t_dm")
				{
					KTau* tau = static_cast<KTau*>(lepton);
					args.push_back(tau->decayMode);
				}
				else if(arg=="gt_pt")
				{
					KGenTau genTau = event.m_genTaus->at(weightNames.first);
					args.push_back(genTau.p4.Pt());
					//LOG(INFO) << "weightNames.first" << weightNames.first;
					//LOG(INFO) << "genTau.p4.Pt(): "<< genTau.p4.Pt();
				}
				else if(arg=="gt_eta")
				{
					KGenTau genTau = event.m_genTaus->at(weightNames.first);
					args.push_back(genTau.p4.Eta());
					// LOG(INFO)<<"genTau.p4.Eta(): "<< genTau.p4.Eta();
				}
				else if(arg=="gt1_pt")
				{
					KGenTau leadingTau = event.m_genTaus->at(0);
					args.push_back(leadingTau.p4.Pt());
				}
				else if(arg=="gt1_eta")
				{
					KGenTau leadingTau = event.m_genTaus->at(0);
					args.push_back(leadingTau.p4.Eta());
				}
				else if(arg=="gt2_pt")
				{
					KGenTau trailingTau = event.m_genTaus->at(1);
					args.push_back(trailingTau.p4.Pt());
				}
				else if(arg=="gt2_eta")
				{
					KGenTau trailingTau = event.m_genTaus->at(1);
					args.push_back(trailingTau.p4.Eta());
				}
			}
			if(settings.GetLegacy()){
				if(m_saveTriggerWeightAsOptionalOnly)
				{
					product.m_optionalWeights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = m_functors.at(weightNames.first).at(index)->eval(args.data());
				}
				else{
					product.m_weights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = m_functors.at(weightNames.first).at(index)->eval(args.data());
				}
			}
			else{
				if((weightNames.second.at(index).find("triggerWeight") != std::string::npos && m_saveTriggerWeightAsOptionalOnly))
				{
					product.m_optionalWeights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = m_functors.at(weightNames.first).at(index)->eval(args.data());
				}
				else{
					product.m_weights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = m_functors.at(weightNames.first).at(index)->eval(args.data());
				}
				if((product.m_weights.find("MuTau_TauLeg_EmbeddedEfficiencyWeight_2") != product.m_weights.end()) && (product.m_weights.find("MuTau_TauLeg_DataEfficiencyWeight_2") != product.m_weights.end()))
				{
					product.m_weights["triggerWeight_muTauCross_2"] = product.m_weights["MuTau_TauLeg_DataEfficiencyWeight_2"]/product.m_weights["MuTau_TauLeg_EmbeddedEfficiencyWeight_2"];
					product.m_weights["MuTau_TauLeg_EmbeddedEfficiencyWeight_2"] = 1.0;
					product.m_weights["MuTau_TauLeg_DataEfficiencyWeight_2"] = 1.0;
				}
			}
		}
	}
}

// ==========================================================================================

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
		KLepton* lepton = product.m_flavourOrderedLeptons[weightNames.first];
		// KLepton* originalLepton = const_cast<KLepton*>(SafeMap::GetWithDefault(product.m_originalLeptons, const_cast<const KLepton*>(lepton), const_cast<const KLepton*>(lepton)));

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
				if(arg=="m_pt" || arg=="t_pt" || arg == "e_pt")
				{
					args.push_back(lepton->p4.Pt());
				}
				if(arg=="m_eta" || arg=="t_eta" || arg == "e_eta")
				{
					args.push_back(lepton->p4.Eta());
				}
				if(arg=="m_phi" || arg=="t_phi" || arg =="e_phi")
				{
					args.push_back(lepton->p4.Phi());
				}
				if(arg=="m_iso"|| arg == "e_iso")
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
			else if(m_scaleFactorMode == HttEnumTypes::DataMcScaleFactorProducerMode::NO_OVERLAP_TRIGGERS) //For 2017 cross triggers without overlap
			{
				if((weightNames.second.at(index).find("triggerWeight") != std::string::npos && m_saveTriggerWeightAsOptionalOnly))
				{
					product.m_optionalWeights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = m_functors.at(weightNames.first).at(index)->eval(args.data());
				}
				else{
					product.m_weights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = m_functors.at(weightNames.first).at(index)->eval(args.data());
				}
			}
		}
	}
	//std::cout << "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" << std::endl;
	if(m_scaleFactorMode == HttEnumTypes::DataMcScaleFactorProducerMode::CROSS_TRIGGERS) //For 2017 cross triggers
	{
		assert((product.m_tautriggerefficienciesMC.size() == 2) &&
		(product.m_tautriggerefficienciesData.size() == 2));
		LOG(DEBUG) << "tau cross-trigger efficiency DATA: " << product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::TIGHT).at(1) << std::endl;
		LOG(DEBUG) << "tau cross-trigger efficiency MC: " << product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::TIGHT).at(1) << std::endl;


		double efficiencyData = leptonTrigEffSingle_data*(1.0-product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::TIGHT).at(1)) + leptonTrigEffCross_data*product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::TIGHT).at(1);
		double efficiencyMc = leptonTrigEffSingle_mc*(1.0-product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::TIGHT).at(1))  + leptonTrigEffCross_mc*product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::TIGHT).at(1);
		leptonTauTrigWeight = ((efficiencyMc == 0.0) ? 1.0 : (efficiencyData / efficiencyMc));

		LOG(DEBUG) << "-------------------------------------------------------------------------------------------------------------------------" << std::endl;
		LOG(DEBUG) << "dataEff: " << efficiencyData << std::endl;
		LOG(DEBUG) << "MCEff: " << efficiencyMc << std::endl;
		LOG(DEBUG) << "weight: " << leptonTauTrigWeight << std::endl;
		LOG(DEBUG) << "-------------------------------------------------------------------------------------------------------------------------" << std::endl;
		product.m_weights[std::string("totalTriggerWeight")] = leptonTauTrigWeight;
	}
	else if(m_scaleFactorMode == HttEnumTypes::DataMcScaleFactorProducerMode::NO_OVERLAP_TRIGGERS) //For 2017 cross triggers without overlap
	{
		if (settings.GetChannel() == "MT")
		{
			assert((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::TIGHT).size() == 2) &&
			(product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::TIGHT).size() == 2));

			product.m_optionalWeights["triggerWeight_mutaucross_vloose_2"] = ((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::VLOOSE)[1] == 0.0) ? 1.0 : product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::VLOOSE)[1]/product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::VLOOSE)[1]);
			product.m_optionalWeights["triggerWeight_mutaucross_loose_2"] = ((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::LOOSE)[1] == 0.0) ? 1.0 : product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::LOOSE)[1]/product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::LOOSE)[1]);
			product.m_optionalWeights["triggerWeight_mutaucross_medium_2"] = ((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::MEDIUM)[1] == 0.0) ? 1.0 : product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::MEDIUM)[1]/product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::MEDIUM)[1]);
			product.m_optionalWeights["triggerWeight_mutaucross_tight_2"] = ((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::TIGHT)[1] == 0.0) ? 1.0 : product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::TIGHT)[1]/product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::TIGHT)[1]);
			product.m_optionalWeights["triggerWeight_mutaucross_vtight_2"] = ((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::VTIGHT)[1] == 0.0) ? 1.0 : product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::VTIGHT)[1]/product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::VTIGHT)[1]);
			product.m_optionalWeights["triggerWeight_mutaucross_vvtight_2"] = ((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::VVTIGHT)[1] == 0.0) ? 1.0 : product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::VVTIGHT)[1]/product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::VVTIGHT)[1]);

			KTau* tau = static_cast<KTau*>(product.m_flavourOrderedLeptons[1]);
			if(tau->getDiscriminator("byVVTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				product.m_optionalWeights["triggerWeight_mutaucross_2"] = product.m_optionalWeights["triggerWeight_mutaucross_vvtight_2"];
			}
			else if(tau->getDiscriminator("byVVTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) < 0.5 && tau->getDiscriminator("byVTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				product.m_optionalWeights["triggerWeight_mutaucross_2"] = product.m_optionalWeights["triggerWeight_mutaucross_vtight_2"];
			}
			else if(tau->getDiscriminator("byVTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) < 0.5 && tau->getDiscriminator("byTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				product.m_optionalWeights["triggerWeight_mutaucross_2"] = product.m_optionalWeights["triggerWeight_mutaucross_tight_2"];
			}
			else if(tau->getDiscriminator("byTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) < 0.5 && tau->getDiscriminator("byMediumIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				product.m_optionalWeights["triggerWeight_mutaucross_2"] = product.m_optionalWeights["triggerWeight_mutaucross_medium_2"];
			}
			else if(tau->getDiscriminator("byMediumIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) < 0.5 && tau->getDiscriminator("byLooseIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				product.m_optionalWeights["triggerWeight_mutaucross_2"] = product.m_optionalWeights["triggerWeight_mutaucross_loose_2"];
			}
			else if(tau->getDiscriminator("byLooseIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) < 0.5 && tau->getDiscriminator("byVLooseIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				product.m_optionalWeights["triggerWeight_mutaucross_2"] = product.m_optionalWeights["triggerWeight_mutaucross_vloose_2"];
			}
		}
		else if (settings.GetChannel() == "ET")
		{
			assert((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::TIGHT).size() == 2) &&
			(product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::TIGHT).size() == 2));

			product.m_optionalWeights["triggerWeight_etaucross_vloose_2"] = ((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::VLOOSE)[1] == 0.0) ? 1.0 : product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::VLOOSE)[1]/product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::VLOOSE)[1]);
			product.m_optionalWeights["triggerWeight_etaucross_loose_2"] = ((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::LOOSE)[1] == 0.0) ? 1.0 : product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::LOOSE)[1]/product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::LOOSE)[1]);
			product.m_optionalWeights["triggerWeight_etaucross_medium_2"] = ((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::MEDIUM)[1] == 0.0) ? 1.0 : product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::MEDIUM)[1]/product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::MEDIUM)[1]);
			product.m_optionalWeights["triggerWeight_etaucross_tight_2"] = ((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::TIGHT)[1] == 0.0) ? 1.0 : product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::TIGHT)[1]/product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::TIGHT)[1]);
			product.m_optionalWeights["triggerWeight_etaucross_vtight_2"] = ((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::VTIGHT)[1] == 0.0) ? 1.0 : product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::VTIGHT)[1]/product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::VTIGHT)[1]);
			product.m_optionalWeights["triggerWeight_etaucross_vvtight_2"] = ((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::VVTIGHT)[1] == 0.0) ? 1.0 : product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::VVTIGHT)[1]/product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::VVTIGHT)[1]);

			KTau* tau = static_cast<KTau*>(product.m_flavourOrderedLeptons[1]);
			if(tau->getDiscriminator("byVVTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				product.m_optionalWeights["triggerWeight_etaucross_2"] = product.m_optionalWeights["triggerWeight_etaucross_vvtight_2"];
			}
			else if(tau->getDiscriminator("byVVTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) < 0.5 && tau->getDiscriminator("byVTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				product.m_optionalWeights["triggerWeight_etaucross_2"] = product.m_optionalWeights["triggerWeight_etaucross_vtight_2"];
			}
			else if(tau->getDiscriminator("byVTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) < 0.5 && tau->getDiscriminator("byTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				product.m_optionalWeights["triggerWeight_etaucross_2"] = product.m_optionalWeights["triggerWeight_etaucross_tight_2"];
			}
			else if(tau->getDiscriminator("byTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) < 0.5 && tau->getDiscriminator("byMediumIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				product.m_optionalWeights["triggerWeight_etaucross_2"] = product.m_optionalWeights["triggerWeight_etaucross_medium_2"];
			}
			else if(tau->getDiscriminator("byMediumIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) < 0.5 && tau->getDiscriminator("byLooseIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				product.m_optionalWeights["triggerWeight_etaucross_2"] = product.m_optionalWeights["triggerWeight_etaucross_loose_2"];
			}
			else if(tau->getDiscriminator("byLooseIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) < 0.5 && tau->getDiscriminator("byVLooseIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				product.m_optionalWeights["triggerWeight_etaucross_2"] = product.m_optionalWeights["triggerWeight_etaucross_vloose_2"];
			}
		}
		else if (settings.GetChannel() == "TT")
		{
			assert((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::TIGHT).size() == 2) &&
			(product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::TIGHT).size() == 2));

			product.m_optionalWeights["triggerWeight_tautaucross_vloose_1"] = ((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::VLOOSE)[0] == 0.0) ? 1.0 : product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::VLOOSE)[0]/product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::VLOOSE)[0]);
			product.m_optionalWeights["triggerWeight_tautaucross_loose_1"] = ((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::LOOSE)[0] == 0.0) ? 1.0 : product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::LOOSE)[0]/product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::LOOSE)[0]);
			product.m_optionalWeights["triggerWeight_tautaucross_medium_1"] = ((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::MEDIUM)[0] == 0.0) ? 1.0 : product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::MEDIUM)[0]/product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::MEDIUM)[0]);
			product.m_optionalWeights["triggerWeight_tautaucross_tight_1"] = ((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::TIGHT)[0] == 0.0) ? 1.0 : product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::TIGHT)[0]/product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::TIGHT)[0]);
			product.m_optionalWeights["triggerWeight_tautaucross_vtight_1"] = ((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::VTIGHT)[0] == 0.0) ? 1.0 : product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::VTIGHT)[0]/product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::VTIGHT)[0]);
			product.m_optionalWeights["triggerWeight_tautaucross_vvtight_1"] = ((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::VVTIGHT)[0] == 0.0) ? 1.0 : product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::VVTIGHT)[0]/product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::VVTIGHT)[0]);

			product.m_optionalWeights["triggerWeight_tautaucross_vloose_2"] = ((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::VLOOSE)[1] == 0.0) ? 1.0 : product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::VLOOSE)[1]/product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::VLOOSE)[1]);
			product.m_optionalWeights["triggerWeight_tautaucross_loose_2"] = ((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::LOOSE)[1] == 0.0) ? 1.0 : product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::LOOSE)[1]/product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::LOOSE)[1]);
			product.m_optionalWeights["triggerWeight_tautaucross_medium_2"] = ((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::MEDIUM)[1] == 0.0) ? 1.0 : product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::MEDIUM)[1]/product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::MEDIUM)[1]);
			product.m_optionalWeights["triggerWeight_tautaucross_tight_2"] = ((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::TIGHT)[1] == 0.0) ? 1.0 : product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::TIGHT)[1]/product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::TIGHT)[1]);
			product.m_optionalWeights["triggerWeight_tautaucross_vtight_2"] = ((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::VTIGHT)[1] == 0.0) ? 1.0 : product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::VTIGHT)[1]/product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::VTIGHT)[1]);
			product.m_optionalWeights["triggerWeight_tautaucross_vvtight_2"] = ((product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::VVTIGHT)[1] == 0.0) ? 1.0 : product.m_tautriggerefficienciesData.at(HttEnumTypes::TauIDWP::VVTIGHT)[1]/product.m_tautriggerefficienciesMC.at(HttEnumTypes::TauIDWP::VVTIGHT)[1]);

			KTau* tau1 = static_cast<KTau*>(product.m_flavourOrderedLeptons[0]);
			KTau* tau2 = static_cast<KTau*>(product.m_flavourOrderedLeptons[1]);

			if(tau1->getDiscriminator("byVVTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				product.m_optionalWeights["triggerWeight_tautaucross_1"] = product.m_optionalWeights["triggerWeight_tautaucross_vvtight_1"];
			}
			else if(tau1->getDiscriminator("byVVTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) < 0.5 && tau1->getDiscriminator("byVTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				product.m_optionalWeights["triggerWeight_tautaucross_1"] = product.m_optionalWeights["triggerWeight_tautaucross_vtight_1"];
			}
			else if(tau1->getDiscriminator("byVTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) < 0.5 && tau1->getDiscriminator("byTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				product.m_optionalWeights["triggerWeight_tautaucross_1"] = product.m_optionalWeights["triggerWeight_tautaucross_tight_1"];
			}
			else if(tau1->getDiscriminator("byTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) < 0.5 && tau1->getDiscriminator("byMediumIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				product.m_optionalWeights["triggerWeight_tautaucross_1"] = product.m_optionalWeights["triggerWeight_tautaucross_medium_1"];
			}
			else if(tau1->getDiscriminator("byMediumIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) < 0.5 && tau1->getDiscriminator("byLooseIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				product.m_optionalWeights["triggerWeight_tautaucross_1"] = product.m_optionalWeights["triggerWeight_tautaucross_loose_1"];
			}
			else if(tau1->getDiscriminator("byLooseIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) < 0.5 && tau1->getDiscriminator("byVLooseIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				product.m_optionalWeights["triggerWeight_tautaucross_1"] = product.m_optionalWeights["triggerWeight_tautaucross_vloose_1"];
			}

			if(tau2->getDiscriminator("byVVTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				product.m_optionalWeights["triggerWeight_tautaucross_2"] = product.m_optionalWeights["triggerWeight_tautaucross_vvtight_2"];
			}
			else if(tau2->getDiscriminator("byVVTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) < 0.5 && tau2->getDiscriminator("byVTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				product.m_optionalWeights["triggerWeight_tautaucross_2"] = product.m_optionalWeights["triggerWeight_tautaucross_vtight_2"];
			}
			else if(tau2->getDiscriminator("byVTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) < 0.5 && tau2->getDiscriminator("byTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				product.m_optionalWeights["triggerWeight_tautaucross_2"] = product.m_optionalWeights["triggerWeight_tautaucross_tight_2"];
			}
			else if(tau2->getDiscriminator("byTightIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) < 0.5 && tau2->getDiscriminator("byMediumIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				product.m_optionalWeights["triggerWeight_tautaucross_2"] = product.m_optionalWeights["triggerWeight_tautaucross_medium_2"];
			}
			else if(tau2->getDiscriminator("byMediumIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) < 0.5 && tau2->getDiscriminator("byLooseIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				product.m_optionalWeights["triggerWeight_tautaucross_2"] = product.m_optionalWeights["triggerWeight_tautaucross_loose_2"];
			}
			else if(tau2->getDiscriminator("byLooseIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) < 0.5 && tau2->getDiscriminator("byVLooseIsolationMVArun2017v2DBoldDMwLT2017", event.m_tauMetadata) > 0.5)
			{
				product.m_optionalWeights["triggerWeight_tautaucross_2"] = product.m_optionalWeights["triggerWeight_tautaucross_vloose_2"];
			}
		}
	}
}

// ==========================================================================================

LegacyWeightProducer::LegacyWeightProducer() :
		RooWorkspaceWeightProducer(&setting_type::GetSaveLegacyWeightAsOptionalOnly,
								   &setting_type::GetLegacyWeightWorkspace,
								   &setting_type::GetLegacyWeightWorkspaceWeightNames,
								   &setting_type::GetLegacyWeightWorkspaceObjectNames,
								   &setting_type::GetLegacyWeightWorkspaceObjectArguments)
{
}

void LegacyWeightProducer::Produce( event_type const& event, product_type & product,
						   setting_type const& settings, metadata_type const& metadata) const
{
	for(auto weightNames:m_weightNames)
	{
		KLepton* lepton = product.m_flavourOrderedLeptons[weightNames.first];
		for(size_t index = 0; index < weightNames.second.size(); index++)
		{
			std::vector<double> args;
			std::vector<std::string> arguments;
			boost::split(arguments,  m_functorArgs.at(weightNames.first).at(index) , boost::is_any_of(","));
			for(auto arg:arguments)
			{
				if((arg=="m_pt") || (arg=="e_pt") || (arg=="t_pt"))
				{
					args.push_back(lepton->p4.Pt());
				}
				else if((arg=="m_eta") || (arg=="e_eta") || (arg=="t_eta"))
				{
					args.push_back(lepton->p4.Eta());
				}
				else if((arg=="m_phi") || (arg=="e_phi") || (arg =="t_phi"))
				{
					args.push_back(lepton->p4.Phi());
				}
				else if((arg=="m_iso") || (arg=="e_iso"))
				{
					args.push_back(SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, lepton, std::numeric_limits<double>::max()));
				}
				else if(arg=="t_dm")
				{
					KTau* tau = static_cast<KTau*>(lepton);
					args.push_back(tau->decayMode);
				}
				else if(arg=="gt_pt")
				{
					KGenTau genTau = event.m_genTaus->at(weightNames.first);
					args.push_back(genTau.p4.Pt());
				}
				else if(arg=="gt_eta")
				{
					KGenTau genTau = event.m_genTaus->at(weightNames.first);
					args.push_back(genTau.p4.Eta());
				}
				else if(arg=="gt1_pt")
				{
					KGenTau leadingTau = event.m_genTaus->at(0);
					args.push_back(leadingTau.p4.Pt());
				}
				else if(arg=="gt1_eta")
				{
					KGenTau leadingTau = event.m_genTaus->at(0);
					args.push_back(leadingTau.p4.Eta());
				}
				else if(arg=="gt2_pt")
				{
					KGenTau trailingTau = event.m_genTaus->at(1);
					args.push_back(trailingTau.p4.Pt());
				}
				else if(arg=="gt2_eta")
				{
					KGenTau trailingTau = event.m_genTaus->at(1);
					args.push_back(trailingTau.p4.Eta());
				}
			}
			bool legacy = settings.GetLegacy();
			if(legacy){
				if (settings.GetChannel() == "MM")
				{
					if((weightNames.second.at(index).find("trackWeight_2") != std::string::npos) || (weightNames.second.at(index).find("idisoWeight_2") != std::string::npos))
					{
						product.m_optionalWeights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = m_functors.at(weightNames.first).at(index)->eval(args.data());
					}
				}
				if(m_saveTriggerWeightAsOptionalOnly && weightNames.second.at(index).find("triggerEfficiency") != std::string::npos)
				{
					product.m_optionalWeights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = m_functors.at(weightNames.first).at(index)->eval(args.data());
				}
				else
				{
					product.m_weights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = m_functors.at(weightNames.first).at(index)->eval(args.data());
				}
			}
			else{
				LOG(WARNING) << "Using LegacyWeightProducer without Legacy setting! settings.GetLegacy(): " << legacy;
			}
		}
	}
	if ((settings.GetChannel() == "ET") || (settings.GetChannel() == "MT"))
	{
		double leptonTrigEffSingle_mcemb = product.m_optionalWeights["triggerEfficiency_singletrigger_MCEmb_1"];
		double leptonTrigEffSingle_data = product.m_optionalWeights["triggerEfficiency_singletrigger_data_1"];
		double leptonTrigEffCross_mcemb = product.m_optionalWeights["triggerEfficiency_crosstrigger_MCEmb_1"];
		double leptonTrigEffCross_data = product.m_optionalWeights["triggerEfficiency_crosstrigger_data_1"];
		double tauTrigEffCross_mcemb = product.m_optionalWeights["triggerEfficiency_crosstrigger_MCEmb_2"];
		double tauTrigEffCross_data = product.m_optionalWeights["triggerEfficiency_crosstrigger_data_2"];

		double efficiencyMCEmb = leptonTrigEffSingle_mcemb*(1.0-tauTrigEffCross_mcemb)  + leptonTrigEffCross_mcemb*tauTrigEffCross_mcemb;
		double efficiencyData = leptonTrigEffSingle_data*(1.0-tauTrigEffCross_data) + leptonTrigEffCross_data*tauTrigEffCross_data;

		// Trigger weights for "HttEnumTypes::DataMcScaleFactorProducerMode::NO_OVERLAP_TRIGGERS"
		product.m_optionalWeights["triggerWeight_single_1"] = ((leptonTrigEffSingle_mcemb == 0.0) ? 1.0 : leptonTrigEffSingle_data/leptonTrigEffSingle_mcemb);
		product.m_optionalWeights["triggerWeight_cross_1"] = ((leptonTrigEffCross_mcemb == 0.0) ? 1.0 : leptonTrigEffCross_data/leptonTrigEffCross_mcemb);
		product.m_optionalWeights["triggerWeight_cross_2"] = ((tauTrigEffCross_mcemb == 0.0) ? 1.0 : tauTrigEffCross_data/tauTrigEffCross_mcemb);

		// Trigger weights for "HttEnumTypes::DataMcScaleFactorProducerMode::CROSS_TRIGGERS"
		product.m_optionalWeights["triggerWeight_comb"] = ((efficiencyMCEmb == 0.0) ? 1.0 : (efficiencyData / efficiencyMCEmb));
	}
	else if (settings.GetChannel() == "MM")
	{
		double leptonTrigEffSingle_mcemb = product.m_optionalWeights["triggerEfficiency_singletrigger_MCEmb_1"];
		double leptonTrigEffSingle_data = product.m_optionalWeights["triggerEfficiency_singletrigger_data_1"];

		product.m_optionalWeights["triggerWeight_single_1"] = ((leptonTrigEffSingle_mcemb == 0.0) ? 1.0 : leptonTrigEffSingle_data/leptonTrigEffSingle_mcemb);
	}
	else if (settings.GetChannel() == "TT")
	{
		double leadingtauTrigEffCross_mcemb = product.m_optionalWeights["triggerEfficiency_crosstrigger_MCEmb_1"];
		double leadingtauTrigEffCross_data = product.m_optionalWeights["triggerEfficiency_crosstrigger_data_1"];
		double trailingtauTrigEffCross_mcemb = product.m_optionalWeights["triggerEfficiency_crosstrigger_MCEmb_2"];
		double trailingtauTrigEffCross_data = product.m_optionalWeights["triggerEfficiency_crosstrigger_data_2"];

		product.m_optionalWeights["triggerWeight_cross_1"] = ((leadingtauTrigEffCross_mcemb == 0.0) ? 1.0 : leadingtauTrigEffCross_data/leadingtauTrigEffCross_mcemb);
		product.m_optionalWeights["triggerWeight_cross_2"] = ((trailingtauTrigEffCross_mcemb == 0.0) ? 1.0 : trailingtauTrigEffCross_data/trailingtauTrigEffCross_mcemb);
		product.m_optionalWeights["triggerWeight_comb"] = product.m_optionalWeights["triggerWeight_cross_1"]*product.m_optionalWeights["triggerWeight_cross_2"];
	}
}
