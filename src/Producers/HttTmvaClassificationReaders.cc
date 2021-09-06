
#include <Math/VectorUtil.h>

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttTmvaClassificationReaders.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/Quantities.h"
#include "Artus/Utility/interface/DefaultValues.h"

	
AntiTtbarDiscriminatorTmvaReader::AntiTtbarDiscriminatorTmvaReader() :
	TmvaClassificationReaderBase<HttTypes>(&setting_type::GetAntiTtbarTmvaInputQuantities,
	                                       &setting_type::GetAntiTtbarTmvaMethods,
	                                       &setting_type::GetAntiTtbarTmvaWeights,
	                                       &product_type::m_antiTtbarDiscriminators)
{
}

void AntiTtbarDiscriminatorTmvaReader::Init(setting_type const& settings, metadata_type& metadata)
{
	// register variables needed for the MVA evaluation
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "emAntiTTbarMva_pzetavis", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.pZetaVis;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "emAntiTTbarMva_pzetamiss", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.pZetaMissVis;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "emAntiTTbarMva_dphi", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return std::abs(ROOT::Math::VectorUtil::DeltaPhi(product.m_flavourOrderedLeptons[0]->p4,
		                                                 product.m_flavourOrderedLeptons[1]->p4));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "emAntiTTbarMva_mvamet", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_met.p4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "emAntiTTbarMva_mtll", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return Quantities::CalculateMt(product.m_flavourOrderedLeptons[0]->p4,
		                               product.m_flavourOrderedLeptons[1]->p4);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "emAntiTTbarMva_csv", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		float csv = -1.0;
		for (std::vector<KBasicJet*>::const_iterator jet = product.m_validJets.begin();
		     ((jet != product.m_validJets.end()) && ((*jet)->p4.Pt() > 20.0)); ++jet)
		{
			if (((*jet)->p4.Pt() > 20.0) && (std::abs((*jet)->p4.Eta()) < 2.4))
			{
				csv = static_cast<KJet const*>(*jet)->getTag("CombinedSecondaryVertexBJetTags", event.m_jetMetadata);
				csv = ((csv > 0.244) ? csv : -1.0);
				break;
			}
		}
		return csv;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "emAntiTTbarMva_d01", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_flavourOrderedLeptons[0]->track.getDxy(&(event.m_vertexSummary->pv));
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "emAntiTTbarMva", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((product.m_antiTtbarDiscriminators.size() > 0) ? product.m_antiTtbarDiscriminators[0] : DefaultValues::UndefinedFloat);
	});
	
	// has to be called at the end of the subclass function
	TmvaClassificationReaderBase<HttTypes>::Init(settings, metadata);
}

void AntiTtbarDiscriminatorTmvaReader::Produce(event_type const& event,
                                               product_type& product,
                                               setting_type const& settings, metadata_type const& metadata) const
{
	assert(product.m_flavourOrderedLeptons.size() >= 2);
	assert(event.m_tjets);
	assert(event.m_jetMetadata);
	assert(product.m_metUncorr);
	
	// has to be called at the end of the subclass function
	TmvaClassificationReaderBase<HttTypes>::Produce(event, product, settings, metadata);
}

// Tau polarisation MVA class:

TauPolarisationTmvaReader::TauPolarisationTmvaReader() :
	TmvaClassificationReaderBase<HttTypes>(&setting_type::GetTauPolarisationTmvaInputQuantities,
	                                       &setting_type::GetTauPolarisationTmvaMethods,
	                                       &setting_type::GetTauPolarisationTmvaWeights,
	                                       &product_type::m_tauPolarisationDiscriminators)
{
}

void TauPolarisationTmvaReader::Init(setting_type const& settings, metadata_type& metadata)
{
	// register variables needed for the MVA evaluation
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "tauPolarisationTMVA", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((product.m_tauPolarisationDiscriminators.size() > 0) ? product.m_tauPolarisationDiscriminators[0] : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "tauPolarisationSKLEARN", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((product.m_tauPolarisationDiscriminators.size() > 0) ? product.m_tauPolarisationDiscriminators[1] : DefaultValues::UndefinedFloat);
	});
	
	// has to be called at the end of the subclass function
	TmvaClassificationReaderBase<HttTypes>::Init(settings, metadata);
}

void TauPolarisationTmvaReader::Produce(event_type const& event,
                                               product_type& product,
                                               setting_type const& settings, metadata_type const& metadata) const
{
	assert(product.m_flavourOrderedLeptons.size() >= 2);
	assert(event.m_tjets);
	assert(event.m_jetMetadata);
	assert(product.m_metUncorr);

	// has to be called at the end of the subclass function
	TmvaClassificationReaderBase<HttTypes>::Produce(event, product, settings, metadata);
}


// HTT Event Classifier MVA class for the tt channel:

HttEventClassifierTmvaReader::HttEventClassifierTmvaReader() :
	TmvaClassificationReaderBase<HttTypes>(&setting_type::GetAntiTtbarTmvaInputQuantities,
	                                       &setting_type::GetAntiTtbarTmvaMethods,
	                                       &setting_type::GetAntiTtbarTmvaWeights,
	                                       &product_type::m_antiTtbarDiscriminators)
{
}

void HttEventClassifierTmvaReader::Init(setting_type const& settings, metadata_type& metadata)
{
	// register variables needed for the MVA evaluation

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "higgs_score", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((product.m_httEventClassifierScores.size() > 0) ? (float)product.m_httEventClassifierScores[0] : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jetFakes_score", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((product.m_httEventClassifierScores.size() > 0) ? (float)product.m_httEventClassifierScores[1] : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "zttEmbed_score", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((product.m_httEventClassifierScores.size() > 0) ? (float)product.m_httEventClassifierScores[2] : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IC_BDT_max_score", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		if (product.m_httEventClassifierScores.size() > 0)
		{
			std::vector<double>::const_iterator max_index_it = std::max_element(product.m_httEventClassifierScores.begin(), product.m_httEventClassifierScores.end());
			return (float)*max_index_it;
		}
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "IC_BDT_max_index", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		if (product.m_httEventClassifierScores.size() > 0)
		{
			std::vector<double>::const_iterator max_index_it = std::max_element(product.m_httEventClassifierScores.begin(), product.m_httEventClassifierScores.end());
			return (int)(max_index_it - product.m_httEventClassifierScores.begin());
		}
		return DefaultValues::UndefinedInt;
	});

	// LOG(INFO) << "-------------------------------------" << std::endl;
	// LOG(INFO) << "HTTEventClassifier" << std::endl;
	// LOG(INFO) << boost::format(param_fmt()) % "channel"             % Channel2String(channel_);
	// LOG(INFO) << boost::format(param_fmt()) % "era"                 % Era2String(era_);
	// LOG(INFO) << "-------------------------------------" << std::endl;

	reader_even_ = new TMVA::Reader();
	reader_odd_ = new TMVA::Reader();

	TString m_year = std::to_string(settings.GetYear());

	// fold0 is trained on even, so apply on odd, and vice versa

	TString filename_even = (std::string)getenv("CMSSW_BASE") + "/src/HiggsAnalysis/KITHiggsToTauTau/data/BDT/01Jun2020/" + TString(m_year) + "/multi_fold1_sm_tt_tauspinner_" + TString(m_year) + "_xgb.xml"; // apply to even here
	TString filename_odd  = (std::string)getenv("CMSSW_BASE") + "/src/HiggsAnalysis/KITHiggsToTauTau/data/BDT/01Jun2020/" + TString(m_year) + "/multi_fold0_sm_tt_tauspinner_" + TString(m_year) + "_xgb.xml"; // apply to odd

	std::vector<TString> var_names = {"jdeta",
																				 "jpt_1",
																				 "m_vis",
																				 "met",
																				 "mjj",
																				 "n_jets",
																				 "pt_1",
																				 "pt_tt",
																				 "pt_vis",
																				 "svfit_mass",};

	for (size_t i_var = 0; i_var < var_names.size(); i_var++)
	{
		m_vars.push_back(new float(0));
		reader_even_->AddVariable(var_names.at(i_var), m_vars.back());
		reader_odd_->AddVariable(var_names.at(i_var), m_vars.back());
	}

	// reader_even_->AddVariable( "jdeta",      & var0_ );
	// reader_even_->AddVariable( "jpt_1",      & var1_ );
	// reader_even_->AddVariable( "m_vis",      & var2_ );
	// reader_even_->AddVariable( "met",        & var3_ );
	// reader_even_->AddVariable( "mjj",        & var4_ );
	// reader_even_->AddVariable( "n_jets",     & var5_ );
	// reader_even_->AddVariable( "pt_1",       & var6_ );
	// reader_even_->AddVariable( "pt_tt",      & var7_ );
	// reader_even_->AddVariable( "pt_vis",     & var8_ );
	// reader_even_->AddVariable( "svfit_mass", & var9_ );
	//
	// reader_odd_->AddVariable( "jdeta",      & var0_ );
	// reader_odd_->AddVariable( "jpt_1",      & var1_ );
	// reader_odd_->AddVariable( "m_vis",      & var2_ );
	// reader_odd_->AddVariable( "met",        & var3_ );
	// reader_odd_->AddVariable( "mjj",        & var4_ );
	// reader_odd_->AddVariable( "n_jets",     & var5_ );
	// reader_odd_->AddVariable( "pt_1",       & var6_ );
	// reader_odd_->AddVariable( "pt_tt",      & var7_ );
	// reader_odd_->AddVariable( "pt_vis",     & var8_ );
	// reader_odd_->AddVariable( "svfit_mass", & var9_ );

	reader_even_->BookMVA( "Multi", filename_even );
	reader_odd_->BookMVA( "Multi", filename_odd );

}

void HttEventClassifierTmvaReader::Produce(event_type const& event,
                                               product_type& product,
                                               setting_type const& settings, metadata_type const& metadata) const
{
	// assert(product.m_flavourOrderedLeptons.size() >= 2);
	// assert(event.m_tjets);
	// assert(event.m_jetMetadata);
	// assert(product.m_metUncorr);


	uint64_t evt_ = event.m_eventInfo->nEvent;
	unsigned isEven_ = evt_ % 2 == 0; // if even then event_ = 1, odd = 0
	// float event_ = (float)isEven_;

	// Initialise variables
	double jdeta_ = -9999.;
	double jpt_1_ = -9999.;
	double m_vis_ = -9999.;
	double met_ = -9999.;
	double mjj_ = -9999.;
	unsigned n_jets_ = 0;
	double pt_1_ = -9999.;
	double pt_tt_ = -9999.;
	double pt_vis_ = -9999.;
	double svfit_mass_ = -9999.;

	RMFLV lep1 = product.m_flavourOrderedLeptons.at(0)->p4;
	RMFLV ditau = product.m_flavourOrderedLeptons.at(0)->p4 + product.m_flavourOrderedLeptons.at(1)->p4;

	// std::vector<PFJet*> jets = event->GetPtrVec<PFJet>(jets_label_);
	// std::sort(jets.begin(), jets.end(), bind(&Candidate::pt, _1) > bind(&Candidate::pt, _2));
	// ic::erase_if(jets,!boost::bind(MinPtMaxEta, _1, 30.0, 4.7));
	std::vector<KBasicJet*> validJets;
	for (std::vector<KBasicJet*>::const_iterator jet = product.m_validJets.begin(); jet != product.m_validJets.end(); ++jet)
	{
		if ((*jet)->p4.Pt() > 30.0 && abs((*jet)->p4.Eta()) < 4.7)
		{
			validJets.push_back(*jet);
		}
	}
	n_jets_ = validJets.size();

	pt_1_ = lep1.Pt();
	if (product.m_svfitResults.fittedHiggsLV->mass() > DefaultValues::UndefinedFloat) {
		svfit_mass_ = product.m_svfitResults.fittedHiggsLV->mass();
	  // svfit_mass_ = event->Get<double>("svfitMass");
	} else {
	  svfit_mass_ = -1;
	}
	m_vis_ = ditau.M();
	pt_tt_ = isnan(product.m_met.p4.Pt()) ? -1 : (ditau + product.m_met.p4).Pt();
	pt_vis_ = ditau.pt();
	met_ = isnan(product.m_met.p4.Pt()) ? -1 : product.m_met.p4.Pt();

	if (n_jets_ >= 1) jpt_1_ = validJets.at(0)->p4.Pt();
	if (n_jets_ >= 2) {
	  jdeta_ = fabs(validJets.at(0)->p4.Eta() - validJets.at(1)->p4.Eta());
	  mjj_ = (validJets.at(0)->p4 + validJets.at(1)->p4).M();
	}

	std::vector<float> inputs = {};
	if (product.m_decayChannel == HttEnumTypes::DecayChannel::TT) {
		inputs.resize(12);
		inputs[0]  = float(jdeta_);
		inputs[1]  = float(jpt_1_);
		inputs[2]  = float(m_vis_);
		inputs[3]  = float(met_);
		inputs[4]  = float(mjj_);
		inputs[5]  = unsigned(n_jets_);
		inputs[6]  = float(pt_1_);
		inputs[7] = float(pt_tt_);
		inputs[8] = float(pt_vis_);
		inputs[9] = float(svfit_mass_);
	}

	// std::vector<float> scores = read_mva_scores(isEven_,inputs);

	std::vector<float> scores = {};

	// LOG(INFO) << "m_vars.size()" << m_vars.size();
	// LOG(INFO) << "inputs.size()" << inputs.size();

	for (size_t i_var = 0; i_var < m_vars.size(); i_var++)
	{
		*(m_vars[i_var]) = inputs[i_var];
	}

	if(isEven_) scores = reader_even_->EvaluateMulticlass("Multi");
	else       scores = reader_odd_->EvaluateMulticlass("Multi");

	// LOG(INFO) << "scores.size()" << scores.size();

	for (size_t i_score = 0; i_score < scores.size(); i_score++) {
		product.m_httEventClassifierScores.push_back(scores[i_score]);
	}

	// event->Add("higgs_score",    scores[0]);
	// event->Add("jetFakes_score", scores[1]);
	// event->Add("zttEmbed_score", scores[2]);
	//
	// std::pair<float, int> max_pair = getMaxScoreWithIndex(scores);
	// event->Add("IC_BDT_max_score", max_pair.first);
	// event->Add("IC_BDT_max_index", max_pair.second);


	// has to be called at the end of the subclass function
	// TmvaClassificationReaderBase<HttTypes>::Produce(event, product, settings, metadata);
}

// std::vector<float> HttEventClassifierTmvaReader::read_mva_scores(unsigned isEven, std::vector<float> vars)
// {
// 	std::vector<float> scores = {};
//
// 	var0_=vars[0], var1_=vars[1], var2_=vars[2], var3_=vars[3], var4_=vars[4], var5_=vars[5], var6_=vars[6], var7_=vars[7], var8_=vars[8], var9_=vars[9];
//
// 	if(isEven) scores = reader_even_->EvaluateMulticlass("Multi");
// 	else       scores = reader_odd_->EvaluateMulticlass("Multi");
//
// 	return scores;
// }

