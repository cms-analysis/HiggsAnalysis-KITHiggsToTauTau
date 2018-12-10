#include "Artus/Utility/interface/SafeMap.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/CPInitialStateQuantitiesProducer.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

CPInitialStateQuantitiesProducer::~CPInitialStateQuantitiesProducer()
{
}

std::string CPInitialStateQuantitiesProducer::GetProducerId() const
{
	return "CPInitialStateQuantitiesProducer";
}

void CPInitialStateQuantitiesProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);

	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "lhenpNLO", [](event_type const& event, product_type const& product)
	{
		return product.m_lhenpNLO;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "etaSep", [](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? std::min(std::abs(product.m_svfitResults.fittedHiggsLV->Eta() - product.m_validJets[0]->p4.Eta()),std::abs(product.m_svfitResults.fittedHiggsLV->Eta() - product.m_validJets[1]->p4.Eta())) : DefaultValues::UndefinedDouble;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "etaH_cut", [](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? (((product.m_validJets[0]->p4.Eta() < product.m_svfitResults.fittedHiggsLV->Eta()) && (product.m_validJets[1]->p4.Eta() > product.m_svfitResults.fittedHiggsLV->Eta())) || ((product.m_validJets[1]->p4.Eta() < product.m_svfitResults.fittedHiggsLV->Eta()) && (product.m_validJets[0]->p4.Eta() > product.m_svfitResults.fittedHiggsLV->Eta()))) : false;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "etaH_cut_CP", [](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? product.m_etaH_cut: false;
	});

	////////////////////////////////////////////
	//  method 1 sum all jets on either side  //
	////////////////////////////////////////////
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "diJetPt_CP1", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? product.m_diJetSystem_CP1.Pt(): DefaultValues::UndefinedFloat;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "diJetPhi_CP1", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? product.m_diJetSystem_CP1.Phi(): DefaultValues::UndefinedFloat;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "diJetEta_CP1", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? product.m_diJetSystem_CP1.Eta(): DefaultValues::UndefinedFloat;
	});
	//interesting variables
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mjj_CP1", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? product.m_diJetSystem_CP1.mass(): DefaultValues::UndefinedFloat;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jdphi_CP1", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? ROOT::Math::VectorUtil::DeltaPhi(product.m_jet_higher_CP1, product.m_jet_lower_CP1): DefaultValues::UndefinedFloat;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jdeta_CP1", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? (product.m_jet_higher_CP1.Eta() - product.m_jet_lower_CP1.Eta()): DefaultValues::UndefinedFloat;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jpt_1_CP1", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? (product.m_jet_higher_CP1.Pt()): DefaultValues::UndefinedFloat;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jpt_2_CP1", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? (product.m_jet_lower_CP1.Pt()): DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jeta_1_CP1", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? (product.m_jet_higher_CP1.Eta()): DefaultValues::UndefinedFloat;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jeta_2_CP1", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? (product.m_jet_lower_CP1.Eta()): DefaultValues::UndefinedFloat;
	});
LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jphi_1_CP1", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? (product.m_jet_higher_CP1.Phi()): DefaultValues::UndefinedFloat;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jphi_2_CP1", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? (product.m_jet_lower_CP1.Phi()): DefaultValues::UndefinedFloat;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "etasep_CP1", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? product.m_etasep_1 : DefaultValues::UndefinedFloat;
	});	

	///////////////////////////////////////////////////
	//  method 2 take highest pt jet on either side  //
	///////////////////////////////////////////////////
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "diJetPt_CP2", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? product.m_diJetSystem_CP2.Pt(): DefaultValues::UndefinedFloat;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "diJetPhi_CP2", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? product.m_diJetSystem_CP2.Phi(): DefaultValues::UndefinedFloat;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "diJetEta_CP2", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? product.m_diJetSystem_CP2.Eta(): DefaultValues::UndefinedFloat;
	});
	//interesting variables
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mjj_CP2", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? product.m_diJetSystem_CP2.mass(): DefaultValues::UndefinedFloat;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jdphi_CP2", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? ROOT::Math::VectorUtil::DeltaPhi(product.m_jet_higher_CP2, product.m_jet_lower_CP2): DefaultValues::UndefinedFloat;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jdeta_CP2", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? (product.m_jet_higher_CP2.Eta() - product.m_jet_lower_CP2.Eta()): DefaultValues::UndefinedFloat;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "etasep_CP2", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? product.m_etasep_2 : DefaultValues::UndefinedFloat;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jpt_1_CP2", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? (product.m_jet_higher_CP2.Pt()): DefaultValues::UndefinedFloat;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jpt_2_CP2", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? (product.m_jet_lower_CP2.Pt()): DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jeta_1_CP2", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? (product.m_jet_higher_CP2.Eta()): DefaultValues::UndefinedFloat;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jeta_2_CP2", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? (product.m_jet_lower_CP2.Eta()): DefaultValues::UndefinedFloat;
	});
LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jphi_1_CP2", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? (product.m_jet_higher_CP2.Phi()): DefaultValues::UndefinedFloat;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jphi_2_CP2", [this](event_type const& event, product_type const& product) {
		return product.m_etaH_cut ? (product.m_jet_lower_CP2.Phi()): DefaultValues::UndefinedFloat;
	});

}

void CPInitialStateQuantitiesProducer::Produce(event_type const& event, product_type& product,
                                    setting_type const& settings, metadata_type const& metadata) const
{
	int lhenpNLO = 0;
	if (settings.GetDoLhenpNLO()) //not in all skims yet, but quantities above/below I want to have in ntuple
	{
		lhenpNLO = (event.m_genEventInfo)->lhenpNLO;
	}
	product.m_lhenpNLO = lhenpNLO;

	float Higgs_eta = -999.;
	if (product.m_svfitResults.fittedHiggsLV)
	{
		Higgs_eta = product.m_svfitResults.fittedHiggsLV->Eta();
	}
	
	RMFLV CPSumJet_higher_eta;
	RMFLV CPSumJet_lower_eta;

	RMFLV CPJet_higher_eta;
	RMFLV CPJet_lower_eta;
	bool haslowerjeteta = false, hashigherjeteta = false;
	

	////////////////////////////////////////////////////
	//////  method 1 sum all jets on either side  //////
	////////////////////////////////////////////////////
	////////////////////////////////////////////////////
	////////////////////////////////////////////////////
	//  method 2 take highest pt jet on either side  ///
	////////////////////////////////////////////////////


	
	if ((KappaProduct::GetNJetsAbovePtThreshold(product.m_validJets, 30.0) >= 2) && (Higgs_eta>-900))
	{
		LOG(DEBUG) << "has at least 2 jets" << std::endl;
		// only sum over 3 highest pt jets, since NLO H+2jets only first 3 from Matrix Calc
		for (std::vector<KBasicJet*>::const_iterator jet = product.m_validJets.begin();
			     (jet != product.m_validJets.begin()+3) && (jet != product.m_validJets.end()); ++jet)
		{
			//std::cout << (*jet)->p4.Pt() << std::endl;
			//method 1 sum the jets to 1 "superjet" on each side
			//method 2 take the dijetsystem of the 2 hardest 2 jets on both sides
			if ((*jet)->p4.Pt() > 20.)  //TODO change this to 20?
			{
				if ((*jet)->p4.Eta() < Higgs_eta)
				{
					if (haslowerjeteta == false || CPJet_lower_eta.Pt()< (*jet)->p4.Pt())
					{
						CPJet_lower_eta = (*jet)->p4;
					}
					haslowerjeteta = true;
					CPSumJet_lower_eta = CPSumJet_lower_eta +  (*jet)->p4;
					LOG(DEBUG) << "CPJet with lower eta as Higgs:  " << std::endl;
					LOG(DEBUG) << "Eta" << CPSumJet_lower_eta.Eta() << std::endl;
					LOG(DEBUG) << "Pt" << CPSumJet_lower_eta.Pt() << std::endl;
					LOG(DEBUG) << "Phi" << CPSumJet_lower_eta.Phi() << std::endl;
				}
				else if ((*jet)->p4.Eta() > Higgs_eta)
				{
					if (hashigherjeteta == false || CPJet_higher_eta.Pt() < (*jet)->p4.Pt())
					{
						CPJet_higher_eta = (*jet)->p4;
					}

					hashigherjeteta = true;
					CPSumJet_higher_eta = CPSumJet_higher_eta +  (*jet)->p4;
					LOG(DEBUG) << "CPJet with lower eta as Higgs:  " << std::endl;
					LOG(DEBUG) << "Eta" << CPSumJet_higher_eta.Eta() << std::endl;
					LOG(DEBUG) << "Pt" << CPSumJet_higher_eta.Pt() << std::endl;
					LOG(DEBUG) << "Phi" << CPSumJet_higher_eta.Phi() << std::endl;
				}
			}
		}
		if (haslowerjeteta && hashigherjeteta)
		{
			product.m_diJetSystem_CP1 = CPSumJet_higher_eta + CPSumJet_lower_eta;
			product.m_diJetSystem_CP2 = CPJet_higher_eta + CPJet_lower_eta;

			product.m_jet_higher_CP1 = CPSumJet_higher_eta;
			product.m_jet_lower_CP1 = CPSumJet_lower_eta;

			product.m_jet_higher_CP2 = CPJet_higher_eta;
			product.m_jet_lower_CP2 = CPJet_lower_eta;

			product.m_etasep_1 = std::min(std::abs(CPSumJet_higher_eta.Eta()-Higgs_eta), std::abs(CPSumJet_lower_eta.Eta()-Higgs_eta));
			product.m_etasep_2 = std::min(std::abs(CPJet_higher_eta.Eta()-Higgs_eta), std::abs(CPJet_lower_eta.Eta()-Higgs_eta));

			product.m_etaH_cut = true;
		}
	}	
}
