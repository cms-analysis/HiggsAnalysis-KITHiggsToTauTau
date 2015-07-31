
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DecayChannelProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/Quantities.h"


void DecayChannelProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);

	m_decayChannel = HttEnumTypes::ToDecayChannel(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetChannel())));
	HttEnumTypes::DecayChannel decayChannel = m_decayChannel; // for being captured in lambda functions
	
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("decayChannelIndex", [](event_type const& event, product_type const& product) {
		return Utility::ToUnderlyingValue(product.m_decayChannel);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("leadingLepCharge", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons[0]->charge();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("leadingLepPt", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons[0]->p4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("leadingLepEta", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons[0]->p4.Eta();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("leadingLepPhi", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons[0]->p4.Phi();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("leadingLepMass", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons[0]->p4.mass();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("leadingLepMt", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons[0]->p4.Mt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("leadingLepIso", [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolation, product.m_ptOrderedLeptons[0], DefaultValues::UndefinedDouble);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("leadingLepIsoOverPt", [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_ptOrderedLeptons[0], DefaultValues::UndefinedDouble);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1Charge", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[0]->charge();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1Dz", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[0]->track.getDz(&event.m_vertexSummary->pv);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1D0", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[0]->track.getDxy(&event.m_vertexSummary->pv);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1Pt", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[0]->p4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1Eta", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[0]->p4.Eta();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1Phi", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[0]->p4.Phi();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1Mass", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[0]->p4.mass();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1Mt", [](event_type const& event, product_type const& product)
	{
		return Quantities::CalculateMtH2Tau(product.m_flavourOrderedLeptons[0]->p4, product.m_met->p4); 
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1Iso", [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolation, product.m_flavourOrderedLeptons[0], DefaultValues::UndefinedDouble);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1IsoOverPt", [](event_type const& event, product_type const& product) {
		float iso = SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_flavourOrderedLeptons[0], std::numeric_limits<double>::max());
		return (product.m_flavourOrderedLeptons[0]->flavour() == KLeptonFlavour::TAU ? (iso * product.m_flavourOrderedLeptons[0]->p4.Pt()) : iso);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1MetPt", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedLeptons[0]->p4 + product.m_met->p4).Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1MetEta", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedLeptons[0]->p4 + product.m_met->p4).Eta();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1MetPhi", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedLeptons[0]->p4 + product.m_met->p4).Phi();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1MetMass", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedLeptons[0]->p4 + product.m_met->p4).mass();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1MetMt", [](event_type const& event, product_type const& product)
	{
		return Quantities::CalculateMt(product.m_flavourOrderedLeptons[0]->p4, product.m_met->p4);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("trailingLepCharge", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons[1]->charge();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("trailingLepPt", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons[1]->p4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("trailingLepEta", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons[1]->p4.Eta();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("trailingLepPhi", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons[1]->p4.Phi();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("trailingLepMass", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons[1]->p4.mass();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("trailingLepMt", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons[1]->p4.Mt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("trailingLepIso", [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolation, product.m_ptOrderedLeptons[1], DefaultValues::UndefinedDouble);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("trailingLepIsoOverPt", [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_ptOrderedLeptons[1], DefaultValues::UndefinedDouble);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2Charge", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[1]->charge();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2Dz", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[1]->track.getDz(&event.m_vertexSummary->pv);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2D0", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[1]->track.getDxy(&event.m_vertexSummary->pv);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2Pt", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[1]->p4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2Eta", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[1]->p4.Eta();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2Phi", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[1]->p4.Phi();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2Mass", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[1]->p4.mass();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2Mt", [](event_type const& event, product_type const& product)
	{
		return Quantities::CalculateMtH2Tau(product.m_flavourOrderedLeptons[1]->p4, product.m_met->p4); 
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2Iso", [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolation, product.m_flavourOrderedLeptons[1], DefaultValues::UndefinedDouble);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2IsoOverPt", [](event_type const& event, product_type const& product) {
		float iso = SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_flavourOrderedLeptons[1], std::numeric_limits<double>::max());
		return (product.m_flavourOrderedLeptons[1]->flavour() == KLeptonFlavour::TAU ? (iso * product.m_flavourOrderedLeptons[1]->p4.Pt()) : iso);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2MetMt", [](event_type const& event, product_type const& product)
	{
		return Quantities::CalculateMt(product.m_flavourOrderedLeptons[1]->p4, product.m_met->p4);
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("byCombinedIsolationDeltaBetaCorrRaw3Hits_1", [decayChannel](event_type const& event, product_type const& product)
	{
		return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[0]->getDiscriminator("byCombinedIsolationDeltaBetaCorrRaw3Hits", event.m_tauMetadata) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("byCombinedIsolationDeltaBetaCorrRaw3Hits_2", [decayChannel](event_type const& event, product_type const& product)
	{
		if (decayChannel == HttEnumTypes::DecayChannel::EM) return DefaultValues::UndefinedFloat;
		else return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[1]->getDiscriminator("byCombinedIsolationDeltaBetaCorrRaw3Hits", event.m_tauMetadata) :  product.m_validTaus[0]->getDiscriminator("byCombinedIsolationDeltaBetaCorrRaw3Hits", event.m_tauMetadata);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("trigweight_1", [decayChannel](event_type const& event, product_type const& product)
	{
		return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[0]->getDiscriminator("trigweight", event.m_tauMetadata) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("trigweight_2", [decayChannel](event_type const& event, product_type const& product)
	{
		if (decayChannel == HttEnumTypes::DecayChannel::EM) return DefaultValues::UndefinedFloat;
		else return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[1]->getDiscriminator("trigweight", event.m_tauMetadata) : product.m_validTaus[0]->getDiscriminator("trigweight", event.m_tauMetadata);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("againstElectronLooseMVA5_1", [decayChannel](event_type const& event, product_type const& product)
	{
		return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[0]->getDiscriminator("againstElectronLooseMVA5", event.m_tauMetadata) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("againstElectronLooseMVA5_2", [decayChannel](event_type const& event, product_type const& product)
	{
		if (decayChannel == HttEnumTypes::DecayChannel::EM) return DefaultValues::UndefinedFloat;
		else return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[1]->getDiscriminator("againstElectronLooseMVA5", event.m_tauMetadata) : product.m_validTaus[0]->getDiscriminator("againstElectronLooseMVA5", event.m_tauMetadata);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("againstElectronMediumMVA5_1", [decayChannel](event_type const& event, product_type const& product)
	{
		return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[0]->getDiscriminator("againstElectronMediumMVA5", event.m_tauMetadata) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("againstElectronMediumMVA5_2", [decayChannel](event_type const& event, product_type const& product)
	{
		if (decayChannel == HttEnumTypes::DecayChannel::EM) return DefaultValues::UndefinedFloat;
		else return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[1]->getDiscriminator("againstElectronMediumMVA5", event.m_tauMetadata) : product.m_validTaus[0]->getDiscriminator("againstElectronMediumMVA5", event.m_tauMetadata);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("againstElectronTightMVA5_1", [decayChannel](event_type const& event, product_type const& product)
	{
		return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[0]->getDiscriminator("againstElectronTightMVA5", event.m_tauMetadata) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("againstElectronTightMVA5_2", [decayChannel](event_type const& event, product_type const& product)
	{
		if (decayChannel == HttEnumTypes::DecayChannel::EM) return DefaultValues::UndefinedFloat;
		else return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[1]->getDiscriminator("againstElectronTightMVA5", event.m_tauMetadata) :  product.m_validTaus[0]->getDiscriminator("againstElectronTightMVA5", event.m_tauMetadata);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("againstElectronVLooseMVA5_1", [decayChannel](event_type const& event, product_type const& product)
	{
		return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[0]->getDiscriminator("againstElectronVLooseMVA5", event.m_tauMetadata) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("againstElectronVLooseMVA5_2", [decayChannel](event_type const& event, product_type const& product)
	{
		if (decayChannel == HttEnumTypes::DecayChannel::EM) return DefaultValues::UndefinedFloat;
		else return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[1]->getDiscriminator("againstElectronVLooseMVA5", event.m_tauMetadata) : product.m_validTaus[0]->getDiscriminator("againstElectronVLooseMVA5", event.m_tauMetadata);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("againstElectronVTightMVA5_1", [decayChannel](event_type const& event, product_type const& product)
	{
		return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[0]->getDiscriminator("againstElectronVTightMVA5", event.m_tauMetadata) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("againstElectronVTightMVA5_2", [decayChannel](event_type const& event, product_type const& product)
	{
		if (decayChannel == HttEnumTypes::DecayChannel::EM) return DefaultValues::UndefinedFloat;
		else return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[1]->getDiscriminator("againstElectronVTightMVA5", event.m_tauMetadata) : product.m_validTaus[0]->getDiscriminator("againstElectronVTightMVA5", event.m_tauMetadata);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("againstMuonLoose3_1", [decayChannel](event_type const& event, product_type const& product)
	{
		return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[0]->getDiscriminator("againstMuonLoose3", event.m_tauMetadata) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("againstMuonLoose3_2", [decayChannel](event_type const& event, product_type const& product)
	{
		if (decayChannel == HttEnumTypes::DecayChannel::EM) return DefaultValues::UndefinedFloat;
		else return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[1]->getDiscriminator("againstMuonLoose3", event.m_tauMetadata) :  product.m_validTaus[0]->getDiscriminator("againstMuonLoose3", event.m_tauMetadata);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("againstMuonTight3_1", [decayChannel](event_type const& event, product_type const& product)
	{
		return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[0]->getDiscriminator("againstMuonTight3", event.m_tauMetadata) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("againstMuonTight3_2", [decayChannel](event_type const& event, product_type const& product)
	{
		if (decayChannel == HttEnumTypes::DecayChannel::EM) return DefaultValues::UndefinedFloat;
		else return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[1]->getDiscriminator("againstMuonTight3", event.m_tauMetadata) : product.m_validTaus[0]->getDiscriminator("againstMuonTight3", event.m_tauMetadata);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("byIsolationMVA3newDMwoLTraw_1", [decayChannel](event_type const& event, product_type const& product)
	{
		return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[0]->getDiscriminator("byIsolationMVA3newDMwoLTraw", event.m_tauMetadata) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("byIsolationMVA3newDMwoLTraw_2", [decayChannel](event_type const& event, product_type const& product)
	{
		if (decayChannel == HttEnumTypes::DecayChannel::EM) return DefaultValues::UndefinedFloat;
		else return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[1]->getDiscriminator("byIsolationMVA3newDMwoLTraw", event.m_tauMetadata) : product.m_validTaus[0]->getDiscriminator("byIsolationMVA3newDMwoLTraw", event.m_tauMetadata);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("byIsolationMVA3oldDMwoLTraw_1", [decayChannel](event_type const& event, product_type const& product)
	{
		return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[0]->getDiscriminator("byIsolationMVA3oldDMwoLTraw", event.m_tauMetadata) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("byIsolationMVA3oldDMwoLTraw_2", [decayChannel](event_type const& event, product_type const& product)
	{
		if (decayChannel == HttEnumTypes::DecayChannel::EM) return DefaultValues::UndefinedFloat;
		else return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[1]->getDiscriminator("byIsolationMVA3oldDMwoLTraw", event.m_tauMetadata) : product.m_validTaus[0]->getDiscriminator("byIsolationMVA3oldDMwoLTraw", event.m_tauMetadata);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("byIsolationMVA3newDMwLTraw_1", [decayChannel](event_type const& event, product_type const& product)
	{
		return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[0]->getDiscriminator("byIsolationMVA3newDMwLTraw", event.m_tauMetadata) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("byIsolationMVA3newDMwLTraw_2", [decayChannel](event_type const& event, product_type const& product)
	{
		if (decayChannel == HttEnumTypes::DecayChannel::EM) return DefaultValues::UndefinedFloat;
		else return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[1]->getDiscriminator("byIsolationMVA3newDMwLTraw", event.m_tauMetadata) :  product.m_validTaus[0]->getDiscriminator("byIsolationMVA3newDMwLTraw", event.m_tauMetadata);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("byIsolationMVA3oldDMwLTraw_1", [decayChannel](event_type const& event, product_type const& product)
	{
		return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[0]->getDiscriminator("byIsolationMVA3oldDMwLTraw", event.m_tauMetadata) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("byIsolationMVA3oldDMwLTraw_2", [decayChannel](event_type const& event, product_type const& product)
	{
		if (decayChannel == HttEnumTypes::DecayChannel::EM) return DefaultValues::UndefinedFloat;
		else return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[1]->getDiscriminator("byIsolationMVA3oldDMwLTraw", event.m_tauMetadata) : product.m_validTaus[0]->getDiscriminator("byIsolationMVA3oldDMwLTraw", event.m_tauMetadata);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("chargedIsoPtSum_1", [decayChannel](event_type const& event, product_type const& product)
	{
		return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[0]->getDiscriminator("chargedIsoPtSum", event.m_tauMetadata) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("chargedIsoPtSum_2", [decayChannel](event_type const& event, product_type const& product)
	{
		if (decayChannel == HttEnumTypes::DecayChannel::EM) return DefaultValues::UndefinedFloat;
		else return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[1]->getDiscriminator("chargedIsoPtSum", event.m_tauMetadata) : product.m_validTaus[0]->getDiscriminator("chargedIsoPtSum", event.m_tauMetadata);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("decayModeFinding_1", [decayChannel](event_type const& event, product_type const& product)
	{
		return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[0]->getDiscriminator("decayModeFinding", event.m_tauMetadata) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("decayModeFinding_2", [decayChannel](event_type const& event, product_type const& product)
	{
		if (decayChannel == HttEnumTypes::DecayChannel::EM) return DefaultValues::UndefinedFloat;
		else return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[1]->getDiscriminator("decayModeFinding", event.m_tauMetadata) : product.m_validTaus[0]->getDiscriminator("decayModeFinding", event.m_tauMetadata);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("decayModeFindingNewDMs_1", [decayChannel](event_type const& event, product_type const& product)
	{
		return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[0]->getDiscriminator("decayModeFindingNewDMs", event.m_tauMetadata) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("decayModeFindingNewDMs_2", [decayChannel](event_type const& event, product_type const& product)
	{
		if (decayChannel == HttEnumTypes::DecayChannel::EM) return DefaultValues::UndefinedFloat;
		else return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[1]->getDiscriminator("decayModeFindingNewDMs", event.m_tauMetadata) : product.m_validTaus[0]->getDiscriminator("decayModeFindingNewDMs", event.m_tauMetadata);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("neutralIsoPtSum_1", [decayChannel](event_type const& event, product_type const& product)
	{
		return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[0]->getDiscriminator("neutralIsoPtSum", event.m_tauMetadata) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("neutralIsoPtSum_2", [decayChannel](event_type const& event, product_type const& product)
	{
		if (decayChannel == HttEnumTypes::DecayChannel::EM) return DefaultValues::UndefinedFloat;
		else return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[1]->getDiscriminator("neutralIsoPtSum", event.m_tauMetadata): product.m_validTaus[0]->getDiscriminator("neutralIsoPtSum", event.m_tauMetadata);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("puCorrPtSum_1", [decayChannel](event_type const& event, product_type const& product)
	{
		return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[0]->getDiscriminator("puCorrPtSum", event.m_tauMetadata) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("puCorrPtSum_2", [decayChannel](event_type const& event, product_type const& product)
	{
		if (decayChannel == HttEnumTypes::DecayChannel::EM) return DefaultValues::UndefinedFloat;
		else return (decayChannel == HttEnumTypes::DecayChannel::TT) ? product.m_validTaus[1]->getDiscriminator("puCorrPtSum", event.m_tauMetadata) : product.m_validTaus[0]->getDiscriminator("puCorrPtSum", event.m_tauMetadata);
	});
}

void DecayChannelProducer::Produce(event_type const& event, product_type& product,
	                               setting_type const& settings) const
{
	
	product.m_decayChannel = HttEnumTypes::DecayChannel::NONE;
	
	KLepton* lepton1 = 0;
	KLepton* lepton2 = 0;
	
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
}

void TTHDecayChannelProducer::Produce(event_type const& event, product_type& product,
	                              setting_type const& settings) const
{
	
	product.m_decayChannel = HttEnumTypes::DecayChannel::NONE;
	
	KLepton* lepton1 = 0;
	KLepton* lepton2 = 0;
	KLepton* lepton3 = 0;
	
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

	// validLeptons collection: necessary for jet overlap removal
	product.m_validLeptons.clear();
	product.m_validLeptons.push_back(lepton1);
	product.m_validLeptons.push_back(lepton2);
	
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
	product.m_flavourOrderedLeptons.push_back(lepton1);
	product.m_flavourOrderedLeptons.push_back(lepton2);

	// update valid leptons list with the leptons from the chosen pair
	if (m_decayChannel == HttEnumTypes::DecayChannel::TT)
	{
		product.m_validTaus.clear();
		product.m_validTaus.push_back(static_cast<KTau*>(diTauPair.first));
		product.m_validTaus.push_back(static_cast<KTau*>(diTauPair.second));
	}
	if (m_decayChannel == HttEnumTypes::DecayChannel::MT)
	{
		product.m_validMuons.clear();
		product.m_validTaus.clear();
		product.m_validMuons.push_back(static_cast<KMuon*>(diTauPair.first));
		product.m_validTaus.push_back(static_cast<KTau*>(diTauPair.second));	
	}
	if (m_decayChannel == HttEnumTypes::DecayChannel::ET)
	{
		product.m_validElectrons.clear();
		product.m_validTaus.clear();
		product.m_validElectrons.push_back(static_cast<KElectron*>(diTauPair.first));
		product.m_validTaus.push_back(static_cast<KTau*>(diTauPair.second));	
	}
	if (m_decayChannel == HttEnumTypes::DecayChannel::EM)
	{
		product.m_validElectrons.clear();
		product.m_validMuons.clear();
		product.m_validElectrons.push_back(static_cast<KElectron*>(diTauPair.first));
		product.m_validMuons.push_back(static_cast<KMuon*>(diTauPair.second));	
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
}
