
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DecayChannelProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/Quantities.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/GeneratorInfo.h"


void DecayChannelProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);

	m_decayChannel = HttEnumTypes::ToDecayChannel(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetChannel())));

	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("decayChannelIndex", [](event_type const& event, product_type const& product) {
		return Utility::ToUnderlyingValue(product.m_decayChannel);
	});

	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("leadingLepLV", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(0)->p4;
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("lep1LV", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->p4;
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("posLepLV", [](event_type const& event, product_type const& product)
	{
		return product.m_chargeOrderedLeptons.at(0)->p4;
	});
	
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("trailingLepLV", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(1)->p4;
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("lep2LV", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->p4;
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("negLepLV", [](event_type const& event, product_type const& product)
	{
		return product.m_chargeOrderedLeptons.at(1)->p4;
	});
	
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("leadingGenLepLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_ptOrderedGenLeptonVisibleLVs.at(0) ? *(product.m_ptOrderedGenLeptonVisibleLVs.at(0)) : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("genLep1LV", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(0) ? *(product.m_flavourOrderedGenLeptonVisibleLVs.at(0)) : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("posGenLepLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_chargeOrderedGenLeptonVisibleLVs.at(0) ? *(product.m_chargeOrderedGenLeptonVisibleLVs.at(0)) : DefaultValues::UndefinedRMFLV);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("leadingGenLepFound", [](event_type const& event, product_type const& product)
	{
		return (product.m_ptOrderedGenLeptons.at(0) != nullptr);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("genLep1Found", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptons.at(0) != nullptr);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("posGenLepFound", [](event_type const& event, product_type const& product)
	{
		return (product.m_chargeOrderedGenLeptons.at(0) != nullptr);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("trailingGenLepLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_ptOrderedGenLeptonVisibleLVs.at(1) ? *(product.m_ptOrderedGenLeptonVisibleLVs.at(1)) : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("genLep2LV", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(1) ? *(product.m_flavourOrderedGenLeptonVisibleLVs.at(1)) : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("negGenLepLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_chargeOrderedGenLeptonVisibleLVs.at(1) ? *(product.m_chargeOrderedGenLeptonVisibleLVs.at(1)) : DefaultValues::UndefinedRMFLV);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("trailingGenLepFound", [](event_type const& event, product_type const& product)
	{
		return (product.m_ptOrderedGenLeptons.at(1) != nullptr);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("genLep2Found", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptons.at(1) != nullptr);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("negGenLepFound", [](event_type const& event, product_type const& product)
	{
		return (product.m_chargeOrderedGenLeptons.at(1) != nullptr);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("leadingLepCharge", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(0)->charge();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("leadingLepPt", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(0)->p4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("leadingLepEta", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(0)->p4.Eta();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("leadingLepPhi", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(0)->p4.Phi();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("leadingLepMass", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(0)->p4.mass();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("leadingLepMt", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(0)->p4.Mt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("leadingLepIso", [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolation, product.m_ptOrderedLeptons.at(0), DefaultValues::UndefinedDouble);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("leadingLepIsoOverPt", [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_ptOrderedLeptons.at(0), DefaultValues::UndefinedDouble);
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1Charge", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->charge();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1Dz", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->track.getDz(&event.m_vertexSummary->pv);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1D0", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->track.getDxy(&event.m_vertexSummary->pv);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1Pt", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->p4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1Eta", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->p4.Eta();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1Phi", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->p4.Phi();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1Mass", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->p4.mass();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1Mt", [](event_type const& event, product_type const& product)
	{
		return Quantities::CalculateMtH2Tau(product.m_flavourOrderedLeptons.at(0)->p4, product.m_met.p4);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1Iso", [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolation, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1IsoOverPt", [](event_type const& event, product_type const& product) {
		float iso = SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_flavourOrderedLeptons.at(0), std::numeric_limits<double>::max());
		return (product.m_flavourOrderedLeptons.at(0)->flavour() == KLeptonFlavour::TAU ? (iso * product.m_flavourOrderedLeptons.at(0)->p4.Pt()) : iso);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1MetPt", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedLeptons.at(0)->p4 + product.m_met.p4).Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1MetEta", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedLeptons.at(0)->p4 + product.m_met.p4).Eta();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1MetPhi", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedLeptons.at(0)->p4 + product.m_met.p4).Phi();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1MetMass", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedLeptons.at(0)->p4 + product.m_met.p4).mass();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1MetMt", [](event_type const& event, product_type const& product)
	{
		return Quantities::CalculateMt(product.m_flavourOrderedLeptons.at(0)->p4, product.m_met.p4);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genLep1Pt", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(0) ? product.m_flavourOrderedGenLeptonVisibleLVs.at(0)->Pt() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genLep1Eta", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(0) ? product.m_flavourOrderedGenLeptonVisibleLVs.at(0)->Eta() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genLep1Phi", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(0) ? product.m_flavourOrderedGenLeptonVisibleLVs.at(0)->Phi() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genLep1Mass", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(0) ? product.m_flavourOrderedGenLeptonVisibleLVs.at(0)->mass() : DefaultValues::UndefinedFloat);
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("trailingLepCharge", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(1)->charge();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("trailingLepPt", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(1)->p4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("trailingLepEta", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(1)->p4.Eta();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("trailingLepPhi", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(1)->p4.Phi();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("trailingLepMass", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(1)->p4.mass();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("trailingLepMt", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(1)->p4.Mt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("trailingLepIso", [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolation, product.m_ptOrderedLeptons.at(1), DefaultValues::UndefinedDouble);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("trailingLepIsoOverPt", [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_ptOrderedLeptons.at(1), DefaultValues::UndefinedDouble);
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2Charge", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->charge();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2Dz", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->track.getDz(&event.m_vertexSummary->pv);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2D0", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->track.getDxy(&event.m_vertexSummary->pv);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2Pt", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->p4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2Eta", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->p4.Eta();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2Phi", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->p4.Phi();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2Mass", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->p4.mass();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2Mt", [](event_type const& event, product_type const& product)
	{
		return Quantities::CalculateMtH2Tau(product.m_flavourOrderedLeptons.at(1)->p4, product.m_met.p4);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2Iso", [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolation, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2IsoOverPt", [](event_type const& event, product_type const& product) {
		float iso = SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_flavourOrderedLeptons.at(1), std::numeric_limits<double>::max());
		return (product.m_flavourOrderedLeptons.at(1)->flavour() == KLeptonFlavour::TAU ? (iso * product.m_flavourOrderedLeptons.at(1)->p4.Pt()) : iso);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2MetMt", [](event_type const& event, product_type const& product)
	{
		return Quantities::CalculateMt(product.m_flavourOrderedLeptons.at(1)->p4, product.m_met.p4);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genLep2Pt", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(1) ? product.m_flavourOrderedGenLeptonVisibleLVs.at(1)->Pt() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genLep2Eta", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(1) ? product.m_flavourOrderedGenLeptonVisibleLVs.at(1)->Eta() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genLep2Phi", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(1) ? product.m_flavourOrderedGenLeptonVisibleLVs.at(1)->Phi() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genLep2Mass", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(1) ? product.m_flavourOrderedGenLeptonVisibleLVs.at(1)->mass() : DefaultValues::UndefinedFloat);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("extraelec_veto", [](KappaEvent const& event, KappaProduct const& product)
	{
		return static_cast<HttProduct const&>(product).m_extraElecVeto;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("extramuon_veto", [](KappaEvent const& event, KappaProduct const& product)
	{
		return static_cast<HttProduct const&>(product).m_extraMuonVeto;
	});

	std::vector<std::string> tauDiscriminators;
	tauDiscriminators.push_back("byCombinedIsolationDeltaBetaCorrRaw3Hits");
	tauDiscriminators.push_back("byLooseCombinedIsolationDeltaBetaCorr3Hits");
	tauDiscriminators.push_back("byMediumCombinedIsolationDeltaBetaCorr3Hits");
	tauDiscriminators.push_back("byTightCombinedIsolationDeltaBetaCorr3Hits");
	tauDiscriminators.push_back("trigweight");
	tauDiscriminators.push_back("againstElectronLooseMVA5");
	tauDiscriminators.push_back("againstElectronMediumMVA5");
	tauDiscriminators.push_back("againstElectronTightMVA5");
	tauDiscriminators.push_back("againstElectronVLooseMVA5");
	tauDiscriminators.push_back("againstElectronVTightMVA5");
	tauDiscriminators.push_back("againstElectronLooseMVA6");
	tauDiscriminators.push_back("againstElectronMediumMVA6");
	tauDiscriminators.push_back("againstElectronTightMVA6");
	tauDiscriminators.push_back("againstElectronVLooseMVA6");
	tauDiscriminators.push_back("againstElectronVTightMVA6");
	tauDiscriminators.push_back("againstMuonLoose3");
	tauDiscriminators.push_back("againstMuonTight3");
	tauDiscriminators.push_back("byIsolationMVArun2v1DBoldDMwLTraw");
	tauDiscriminators.push_back("byLooseIsolationMVArun2v1DBoldDMwLT");
	tauDiscriminators.push_back("byMediumIsolationMVArun2v1DBoldDMwLT");
	tauDiscriminators.push_back("byTightIsolationMVArun2v1DBoldDMwLT");
	tauDiscriminators.push_back("byVTightIsolationMVArun2v1DBoldDMwLT");
	tauDiscriminators.push_back("chargedIsoPtSum");
	tauDiscriminators.push_back("decayModeFinding");
	tauDiscriminators.push_back("decayModeFindingNewDMs");
	tauDiscriminators.push_back("neutralIsoPtSum");
	tauDiscriminators.push_back("puCorrPtSum");

	for (size_t leptonIndex = 0; leptonIndex < 2; ++leptonIndex)
	{
		for (std::string tauDiscriminator : tauDiscriminators)
		{
			std::string quantity = tauDiscriminator + "_" + std::to_string(leptonIndex+1);
			LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(quantity, [tauDiscriminator, leptonIndex](event_type const& event, product_type const& product)
			{
				KLepton* lepton = product.m_flavourOrderedLeptons.at(leptonIndex);
				if (lepton->flavour() == KLeptonFlavour::TAU)
				{
					return static_cast<KTau*>(lepton)->getDiscriminator(tauDiscriminator, event.m_tauMetadata);
				}
				else
				{
					return DefaultValues::UndefinedFloat;
				}
			});
		}
		
		std::string decayModeQuantity = "decayMode_" + std::to_string(leptonIndex+1);
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity(decayModeQuantity, [leptonIndex](event_type const& event, product_type const& product)
		{
			KLepton* lepton = product.m_flavourOrderedLeptons.at(leptonIndex);
			if (lepton->flavour() == KLeptonFlavour::TAU)
			{
				return static_cast<KTau*>(lepton)->decayMode;
			}
			else
			{
				return DefaultValues::UndefinedInt;
			}
		});
		
		std::string genMatchQuantity = "gen_match_" + std::to_string(leptonIndex+1);
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity(genMatchQuantity, [leptonIndex](event_type const& event, product_type const& product)
		{
			KGenParticle* genParticle = product.m_flavourOrderedGenLeptons.at(leptonIndex);
			if (genParticle)
			{
				return Utility::ToUnderlyingValue(GeneratorInfo::GetGenMatchingCode(genParticle));
			}
			else
			{
				return Utility::ToUnderlyingValue(HttEnumTypes::GenMatchingCode::IS_FAKE);
			}
		});
		
		std::string hadGenMatchPtQuantity = "had_gen_match_pT_" + std::to_string(leptonIndex+1);
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(hadGenMatchPtQuantity, [leptonIndex](event_type const& event, product_type const& product)
		{
			KGenParticle* genParticle = product.m_flavourOrderedGenLeptons.at(leptonIndex);

			// Return pT in case it matches a hadronic tau
			if (genParticle && (GeneratorInfo::GetGenMatchingCode(genParticle) == HttEnumTypes::GenMatchingCode::IS_TAU_HAD_DECAY))
			{
				return genParticle->p4.Pt();
			}
			else
			{
				return 0.0f;
			}
		});
	}
}

void DecayChannelProducer::Produce(event_type const& event, product_type& product,
	                               setting_type const& settings) const
{

	product.m_decayChannel = HttEnumTypes::DecayChannel::NONE;

	KLepton* lepton1 = nullptr;
	KLepton* lepton2 = nullptr;

	size_t nElectrons = product.m_validElectrons.size();
	size_t nMuons = product.m_validMuons.size();
	size_t nTaus = product.m_validTaus.size();

	if (nElectrons == 2)
	{
		lepton1 = product.m_validElectrons[0];
		lepton2 = product.m_validElectrons[1];
		product.m_decayChannel = HttEnumTypes::DecayChannel::EE;
	}
	else if (nElectrons == 1)
	{
		if (nMuons == 1)
		{
			lepton1 = product.m_validElectrons[0];
			lepton2 = product.m_validMuons[0];

			// require that in the EM channel at least one of the leptons has a pT > 20 GeV
			if (lepton1->p4.Pt() > 20. || lepton2->p4.Pt() > 20.) {
				product.m_decayChannel = HttEnumTypes::DecayChannel::EM;
			}
		}
		else if (nTaus >= 1)
		{
			lepton1 = product.m_validElectrons[0];
			lepton2 = product.m_validTaus[0];
			product.m_decayChannel = HttEnumTypes::DecayChannel::ET;
		}
	}
	else if (nElectrons == 0)
	{
		if (nMuons == 2)
		{
			lepton1 = product.m_validMuons[0];
			lepton2 = product.m_validMuons[1];
			product.m_decayChannel = HttEnumTypes::DecayChannel::MM;
		}
		else if (nMuons == 1 && nTaus >= 1)
		{
			lepton1 = product.m_validMuons[0];
			lepton2 = product.m_validTaus[0];
			product.m_decayChannel = HttEnumTypes::DecayChannel::MT;
		}
		else if (nTaus >= 2)
		{
			lepton1 = product.m_validTaus[0];
			lepton2 = product.m_validTaus[1];
			product.m_decayChannel = HttEnumTypes::DecayChannel::TT;
		}
	}

	// fill tau energy scale weights
	if (! product.m_tauEnergyScaleWeight.empty())
	{
		if ((product.m_decayChannel == HttEnumTypes::DecayChannel::ET) ||
			(product.m_decayChannel == HttEnumTypes::DecayChannel::MT) ||
			(product.m_decayChannel == HttEnumTypes::DecayChannel::TT))
		{
			product.m_weights["tauEnergyScaleWeight"] = SafeMap::Get(product.m_tauEnergyScaleWeight, static_cast<KTau*>(lepton2));
			if (product.m_decayChannel == HttEnumTypes::DecayChannel::TT)
			{
				product.m_weights["tauEnergyScaleWeight"] *= SafeMap::Get(product.m_tauEnergyScaleWeight, static_cast<KTau*>(lepton1));
			}
		}
	}

	if (product.m_decayChannel != HttEnumTypes::DecayChannel::NONE)
	{

		// fill leptons ordered by pt (high pt first)
		if (lepton1->p4.Pt() >= lepton2->p4.Pt())
		{
			product.m_ptOrderedLeptons.push_back(lepton1);
			product.m_ptOrderedLeptons.push_back(lepton2);
		}
		else
		{
			product.m_ptOrderedLeptons.push_back(lepton2);
			product.m_ptOrderedLeptons.push_back(lepton1);
		}

		// fill leptons ordered by flavour (according to channel definition)
		product.m_flavourOrderedLeptons.push_back(lepton1);
		product.m_flavourOrderedLeptons.push_back(lepton2);

		// fill leptons ordered by charge (positive charges first)
		if (lepton1->charge() >= lepton2->charge())
		{
			product.m_chargeOrderedLeptons.push_back(lepton1);
			product.m_chargeOrderedLeptons.push_back(lepton2);
		}
		else
		{
			product.m_chargeOrderedLeptons.push_back(lepton2);
			product.m_chargeOrderedLeptons.push_back(lepton1);
		}
	}
	
	FillGenLeptonCollections(product);
}

void DecayChannelProducer::FillGenLeptonCollections(product_type& product) const
{
	product.m_ptOrderedGenLeptons.clear();
	for (std::vector<KLepton*>::iterator lepton = product.m_ptOrderedLeptons.begin();
	     lepton != product.m_ptOrderedLeptons.end(); ++lepton)
	{
		product.m_ptOrderedGenLeptons.push_back(GeneratorInfo::GetGenMatchedParticle(
				&(*(*lepton)), product.m_genParticleMatchedLeptons, product.m_genTauMatchedTaus
		));
		product.m_ptOrderedGenLeptonVisibleLVs.push_back(GeneratorInfo::GetVisibleLV(product.m_ptOrderedGenLeptons.back()));
	}
	
	product.m_flavourOrderedGenLeptons.clear();
	for (std::vector<KLepton*>::iterator lepton = product.m_flavourOrderedLeptons.begin();
	     lepton != product.m_flavourOrderedLeptons.end(); ++lepton)
	{
		product.m_flavourOrderedGenLeptons.push_back(GeneratorInfo::GetGenMatchedParticle(
				*lepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedTaus
		));
		product.m_flavourOrderedGenLeptonVisibleLVs.push_back(GeneratorInfo::GetVisibleLV(product.m_flavourOrderedGenLeptons.back()));
	}
	
	product.m_chargeOrderedGenLeptons.clear();
	for (std::vector<KLepton*>::iterator lepton = product.m_chargeOrderedLeptons.begin();
	     lepton != product.m_chargeOrderedLeptons.end(); ++lepton)
	{
		product.m_chargeOrderedGenLeptons.push_back(GeneratorInfo::GetGenMatchedParticle(
				*lepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedTaus
		));
		product.m_chargeOrderedGenLeptonVisibleLVs.push_back(GeneratorInfo::GetVisibleLV(product.m_chargeOrderedGenLeptons.back()));
	}
}


void TTHDecayChannelProducer::Produce(event_type const& event, product_type& product,
	                              setting_type const& settings) const
{

	product.m_decayChannel = HttEnumTypes::DecayChannel::NONE;

	KLepton* lepton1 = nullptr;
	KLepton* lepton2 = nullptr;
	KLepton* lepton3 = nullptr;

	size_t nElectrons = product.m_validElectrons.size();
	size_t nMuons = product.m_validMuons.size();
	size_t nTaus = product.m_validTTHTaus.size();

	if (nElectrons == 1)
	{
		if (nTaus == 2) {
			lepton1 = product.m_validTTHTaus[0];
			lepton2 = product.m_validTTHTaus[1];
			lepton3 = product.m_validElectrons[0];
			product.m_decayChannel = HttEnumTypes::DecayChannel::TTH_TTE;
		}
	}
	else if (nMuons == 1)
	{
		if (nTaus == 2) {
			lepton1 = product.m_validTTHTaus[0];
			lepton2 = product.m_validTTHTaus[1];
			lepton3 = product.m_validMuons[0];
			product.m_decayChannel = HttEnumTypes::DecayChannel::TTH_TTM;
		}
	}

	// fill tau energy scale weights
	if (! product.m_tauEnergyScaleWeight.empty())
	{
		if ((product.m_decayChannel == HttEnumTypes::DecayChannel::TTH_TTE) ||
		    (product.m_decayChannel == HttEnumTypes::DecayChannel::TTH_TTM))
		{
			product.m_weights["tauEnergyScaleWeight"] = SafeMap::Get(product.m_tauEnergyScaleWeight, static_cast<KTau*>(lepton1));
			product.m_weights["tauEnergyScaleWeight"] *= SafeMap::Get(product.m_tauEnergyScaleWeight, static_cast<KTau*>(lepton2));
		}
	}

	if (product.m_decayChannel != HttEnumTypes::DecayChannel::NONE)
	{
		// fill leptons ordered by pt (high pt first)
		product.m_ptOrderedLeptons.push_back(lepton1);
		product.m_ptOrderedLeptons.push_back(lepton2);
		product.m_ptOrderedLeptons.push_back(lepton3);

		std::sort(product.m_ptOrderedLeptons.begin(), product.m_ptOrderedLeptons.end(),
	          [](KLepton const* lepton1, KLepton const* lepton2) -> bool
	          { return lepton1->p4.Pt() > lepton2->p4.Pt(); });


		// fill leptons ordered by flavour (according to channel definition)
		product.m_flavourOrderedLeptons.push_back(lepton1);
		product.m_flavourOrderedLeptons.push_back(lepton2);
		product.m_flavourOrderedLeptons.push_back(lepton3);


		// fill leptons ordered by charge (positive charges first)
		product.m_chargeOrderedLeptons.push_back(lepton1);
		product.m_chargeOrderedLeptons.push_back(lepton2);
		product.m_chargeOrderedLeptons.push_back(lepton3);

		std::sort(product.m_chargeOrderedLeptons.begin(), product.m_chargeOrderedLeptons.end(),
	          [](KLepton const* lepton1, KLepton const* lepton2) -> bool
	          { return lepton1->charge() > lepton2->charge(); });
	}
	
	FillGenLeptonCollections(product);
}

void Run2DecayChannelProducer::Init(setting_type const& settings)
{
	DecayChannelProducer::Init(settings);

	// For taus in Run2 we use dz saved in the KTau
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1Dz", [](event_type const& event, product_type const& product)
	{
		if(product.m_flavourOrderedLeptons.at(0)->flavour() == KLeptonFlavour::TAU)
		{
			KTau* tau = dynamic_cast<KTau*>(product.m_flavourOrderedLeptons.at(0));
			return tau->dz;
		}
		return product.m_flavourOrderedLeptons.at(0)->track.getDz(&event.m_vertexSummary->pv);
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2Dz", [](event_type const& event, product_type const& product)
	{
		if(product.m_flavourOrderedLeptons.at(1)->flavour() == KLeptonFlavour::TAU)
		{
			KTau* tau = dynamic_cast<KTau*>(product.m_flavourOrderedLeptons.at(1));
			return tau->dz;
		}
		return product.m_flavourOrderedLeptons.at(1)->track.getDz(&event.m_vertexSummary->pv);
	});
}

void Run2DecayChannelProducer::Produce(event_type const& event, product_type& product,
	                              setting_type const& settings) const
{
	assert(product.m_validDiTauPairCandidates.size() > 0);

	product.m_decayChannel = m_decayChannel;

	// fill the lepton vectors
	DiTauPair diTauPair = product.m_validDiTauPairCandidates.at(0);
	KLepton* lepton1 = diTauPair.first;
	KLepton* lepton2 = diTauPair.second;

	// fill leptons ordered by pt (high pt first)
	if (lepton1->p4.Pt() >= lepton2->p4.Pt())
	{
		product.m_ptOrderedLeptons.push_back(lepton1);
		product.m_ptOrderedLeptons.push_back(lepton2);
	}
	else
	{
		product.m_ptOrderedLeptons.push_back(lepton2);
		product.m_ptOrderedLeptons.push_back(lepton1);
	}

	// fill leptons ordered by charge (positive charges first)
	if (lepton1->charge() >= lepton2->charge())
	{
		product.m_chargeOrderedLeptons.push_back(lepton1);
		product.m_chargeOrderedLeptons.push_back(lepton2);
	}
	else
	{
		product.m_chargeOrderedLeptons.push_back(lepton2);
		product.m_chargeOrderedLeptons.push_back(lepton1);
	}

	// fill leptons ordered by flavour (according to channel definition)
	if (m_decayChannel == HttEnumTypes::DecayChannel::EM)
	{
		product.m_flavourOrderedLeptons.push_back(lepton2);
		product.m_flavourOrderedLeptons.push_back(lepton1);
	}
	else if (m_decayChannel == HttEnumTypes::DecayChannel::TT || m_decayChannel == HttEnumTypes::DecayChannel::MM)
	{
		if (lepton1->p4.Pt() >= lepton2->p4.Pt())
		{
			product.m_flavourOrderedLeptons.push_back(lepton1);
			product.m_flavourOrderedLeptons.push_back(lepton2);
		}
		else
		{
			product.m_flavourOrderedLeptons.push_back(lepton2);
			product.m_flavourOrderedLeptons.push_back(lepton1);
		}
	}
	else
	{
		product.m_flavourOrderedLeptons.push_back(lepton1);
		product.m_flavourOrderedLeptons.push_back(lepton2);
	}

	// update valid leptons list with the leptons from the chosen pair: necessary for jet overlap removal
	product.m_validLeptons.clear();
	bool electronsCleared = false;
	bool muonsCleared = false;
	bool tausCleared = false;
	for (std::vector<KLepton*>::iterator lepton = product.m_ptOrderedLeptons.begin();
	     lepton != product.m_ptOrderedLeptons.end(); ++lepton)
	{
		product.m_validLeptons.push_back(*lepton);

		if ((*lepton)->flavour() == KLeptonFlavour::ELECTRON)
		{
			if (! electronsCleared)
			{
				product.m_validElectrons.clear();
				electronsCleared = true;
			}
			product.m_validElectrons.push_back(static_cast<KElectron*>(*lepton));
		}
		else if ((*lepton)->flavour() == KLeptonFlavour::MUON)
		{
			if (! muonsCleared)
			{
				product.m_validMuons.clear();
				muonsCleared = true;
			}
			product.m_validMuons.push_back(static_cast<KMuon*>(*lepton));
		}
		else if ((*lepton)->flavour() == KLeptonFlavour::TAU)
		{
			if (! tausCleared)
			{
				product.m_validTaus.clear();
				tausCleared = true;
			}
			product.m_validTaus.push_back(static_cast<KTau*>(*lepton));
		}
	}

	// set boolean veto variables
	product.m_extraElecVeto = (product.m_validLooseElectrons.size() > product.m_validElectrons.size());
	product.m_extraMuonVeto = (product.m_validLooseMuons.size() > product.m_validMuons.size());
	if ((m_decayChannel == HttEnumTypes::DecayChannel::TT) || (m_decayChannel == HttEnumTypes::DecayChannel::ET))
	{
		product.m_extraMuonVeto = (product.m_validLooseMuons.size() > 0);
	}
	if ((m_decayChannel == HttEnumTypes::DecayChannel::TT) || (m_decayChannel == HttEnumTypes::DecayChannel::MT))
	{
		product.m_extraElecVeto = (product.m_validLooseElectrons.size() > 0);
	}
	
	FillGenLeptonCollections(product);
}
