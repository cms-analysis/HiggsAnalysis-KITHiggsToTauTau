
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "Kappa/DataFormats/interface/KTrack.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DecayChannelProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/Quantities.h"
#include "Artus/KappaAnalysis/interface/Utility/GeneratorInfo.h"


void DecayChannelProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);

	m_decayChannel = HttEnumTypes::ToDecayChannel(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetChannel())));

	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "decayChannelIndex", [](event_type const& event, product_type const& product) {
		return Utility::ToUnderlyingValue(product.m_decayChannel);
	});

	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "leadingLepLV", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(0)->p4;
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "lep1LV", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->p4;
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "posLepLV", [](event_type const& event, product_type const& product)
	{
		return product.m_chargeOrderedLeptons.at(0)->p4;
	});

	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "leadingLepSumChargedHadronsLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_ptOrderedLeptons.at(0)->flavour() == KLeptonFlavour::TAU ? static_cast<KTau*>(product.m_ptOrderedLeptons.at(0))->sumChargedHadronCandidates() : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "lep1SumChargedHadronsLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedLeptons.at(0)->flavour() == KLeptonFlavour::TAU ? static_cast<KTau*>(product.m_flavourOrderedLeptons.at(0))->sumChargedHadronCandidates() : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "posLepSumChargedHadronsLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_chargeOrderedLeptons.at(0)->flavour() == KLeptonFlavour::TAU ? static_cast<KTau*>(product.m_chargeOrderedLeptons.at(0))->sumChargedHadronCandidates() : DefaultValues::UndefinedRMFLV);
	});

	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "leadingLepSumNeutralHadronsLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_ptOrderedLeptons.at(0)->flavour() == KLeptonFlavour::TAU ? static_cast<KTau*>(product.m_ptOrderedLeptons.at(0))->piZeroMomentum() : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "lep1SumNeutralHadronsLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedLeptons.at(0)->flavour() == KLeptonFlavour::TAU ? static_cast<KTau*>(product.m_flavourOrderedLeptons.at(0))->piZeroMomentum() : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "posLepSumNeutralHadronsLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_chargeOrderedLeptons.at(0)->flavour() == KLeptonFlavour::TAU ? static_cast<KTau*>(product.m_chargeOrderedLeptons.at(0))->piZeroMomentum() : DefaultValues::UndefinedRMFLV);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "trailingLepLV", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(1)->p4;
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "lep2LV", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->p4;
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "negLepLV", [](event_type const& event, product_type const& product)
	{
		return product.m_chargeOrderedLeptons.at(1)->p4;
	});

	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "trailingLepSumChargedHadronsLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_ptOrderedLeptons.at(1)->flavour() == KLeptonFlavour::TAU ? static_cast<KTau*>(product.m_ptOrderedLeptons.at(1))->sumChargedHadronCandidates() : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "lep2SumChargedHadronsLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedLeptons.at(1)->flavour() == KLeptonFlavour::TAU ? static_cast<KTau*>(product.m_flavourOrderedLeptons.at(1))->sumChargedHadronCandidates() : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "negLepSumChargedHadronsLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_chargeOrderedLeptons.at(1)->flavour() == KLeptonFlavour::TAU ? static_cast<KTau*>(product.m_chargeOrderedLeptons.at(1))->sumChargedHadronCandidates() : DefaultValues::UndefinedRMFLV);
	});

	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "trailingLepSumNeutralHadronsLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_ptOrderedLeptons.at(1)->flavour() == KLeptonFlavour::TAU ? static_cast<KTau*>(product.m_ptOrderedLeptons.at(1))->piZeroMomentum() : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "lep2SumNeutralHadronsLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedLeptons.at(1)->flavour() == KLeptonFlavour::TAU ? static_cast<KTau*>(product.m_flavourOrderedLeptons.at(1))->piZeroMomentum() : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "negLepSumNeutralHadronsLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_chargeOrderedLeptons.at(1)->flavour() == KLeptonFlavour::TAU ? static_cast<KTau*>(product.m_chargeOrderedLeptons.at(1))->piZeroMomentum() : DefaultValues::UndefinedRMFLV);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "leadingGenMatchedLepLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_ptOrderedGenLeptonVisibleLVs.at(0) ? *(product.m_ptOrderedGenLeptonVisibleLVs.at(0)) : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "genMatchedLep1LV", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(0) ? *(product.m_flavourOrderedGenLeptonVisibleLVs.at(0)) : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "posGenMatchedLepLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_chargeOrderedGenLeptonVisibleLVs.at(0) ? *(product.m_chargeOrderedGenLeptonVisibleLVs.at(0)) : DefaultValues::UndefinedRMFLV);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "leadingGenMatchedLepFound", [](event_type const& event, product_type const& product)
	{
		return (product.m_ptOrderedGenLeptons.at(0) != nullptr);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "genMatchedLep1Found", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptons.at(0) != nullptr);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "posGenMatchedLepFound", [](event_type const& event, product_type const& product)
	{
		return (product.m_chargeOrderedGenLeptons.at(0) != nullptr);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "leadingGenMatchedTauLV", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_ptOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->p4 : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "genMatchedTau1LV", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->p4 : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "posGenMatchedTauLV", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_chargeOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->p4 : DefaultValues::UndefinedRMFLV);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "leadingGenMatchedTauVisibleLV", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_ptOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->visible.p4 : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "genMatchedTau1VisibleLV", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->visible.p4 : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "posGenMatchedTauVisibleLV", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_chargeOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->visible.p4 : DefaultValues::UndefinedRMFLV);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "leadingGenMatchedTauFound", [](event_type const& event, product_type const& product)
	{
		return Utility::Contains(product.m_genTauMatchedLeptons, product.m_ptOrderedLeptons.at(0));
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "genMatchedTau1Found", [](event_type const& event, product_type const& product)
	{
		return Utility::Contains(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(0));
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "posGenMatchedTauFound", [](event_type const& event, product_type const& product)
	{
		return Utility::Contains(product.m_genTauMatchedLeptons, product.m_chargeOrderedLeptons.at(0));
	});
	
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "trailingGenMatchedLepLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_ptOrderedGenLeptonVisibleLVs.at(1) ? *(product.m_ptOrderedGenLeptonVisibleLVs.at(1)) : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "genMatchedLep2LV", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(1) ? *(product.m_flavourOrderedGenLeptonVisibleLVs.at(1)) : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "negGenMatchedLepLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_chargeOrderedGenLeptonVisibleLVs.at(1) ? *(product.m_chargeOrderedGenLeptonVisibleLVs.at(1)) : DefaultValues::UndefinedRMFLV);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "trailingGenMatchedLepFound", [](event_type const& event, product_type const& product)
	{
		return (product.m_ptOrderedGenLeptons.at(1) != nullptr);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "genMatchedLep2Found", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptons.at(1) != nullptr);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "negGenMatchedLepFound", [](event_type const& event, product_type const& product)
	{
		return (product.m_chargeOrderedGenLeptons.at(1) != nullptr);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "trailingGenMatchedTauLV", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_ptOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->p4 : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "genMatchedTau2LV", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->p4 : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "negGenMatchedTauLV", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_chargeOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->p4 : DefaultValues::UndefinedRMFLV);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "trailingGenMatchedTauVisibleLV", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_ptOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->visible.p4 : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "genMatchedTau2VisibleLV", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->visible.p4 : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "negGenMatchedTauVisibleLV", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_chargeOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->visible.p4 : DefaultValues::UndefinedRMFLV);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "trailingGenMatchedTauFound", [](event_type const& event, product_type const& product)
	{
		return Utility::Contains(product.m_genTauMatchedLeptons, product.m_ptOrderedLeptons.at(1));
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "genMatchedTau2Found", [](event_type const& event, product_type const& product)
	{
		return Utility::Contains(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(1));
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "negGenMatchedTauFound", [](event_type const& event, product_type const& product)
	{
		return Utility::Contains(product.m_genTauMatchedLeptons, product.m_chargeOrderedLeptons.at(1));
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "leadingLepCharge", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(0)->charge();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "leadingLepPt", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(0)->p4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "leadingLepEta", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(0)->p4.Eta();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "leadingLepPhi", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(0)->p4.Phi();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "leadingLepMass", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(0)->p4.mass();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "leadingLepMt", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(0)->p4.Mt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "leadingLepIso", [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolation, product.m_ptOrderedLeptons.at(0), DefaultValues::UndefinedDouble);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "leadingLepIsoOverPt", [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_ptOrderedLeptons.at(0), DefaultValues::UndefinedDouble);
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep1Charge", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->charge();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep1Dz", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->dz;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep1ErrDz", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->track.errDz();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep1D0", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->dxy;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep1ErrD0", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->track.errDxy();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep1TrackNInnerHits", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->track.nInnerHits;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep1TrackChi2OverNdof", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedLeptons.at(0)->track.chi2 / product.m_flavourOrderedLeptons.at(0)->track.nDOF);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep1TrackIsLooseQuality", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->track.quality(KTrackQuality::KTrackQualityType::loose);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep1TrackIsTightQuality", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->track.quality(KTrackQuality::KTrackQualityType::tight);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep1TrackIsHighPurityQuality", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->track.quality(KTrackQuality::KTrackQualityType::highPurity);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep1Pt", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->p4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep1Eta", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->p4.Eta();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep1Phi", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->p4.Phi();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep1Mass", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->p4.mass();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep1Mt", [](event_type const& event, product_type const& product)
	{
		return Quantities::CalculateMtH2Tau(product.m_flavourOrderedLeptons.at(0)->p4, product.m_met.p4);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep1Iso", [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolation, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedDouble);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep1IsoOverPt", [](event_type const& event, product_type const& product) {
		float iso = SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_flavourOrderedLeptons.at(0), std::numeric_limits<double>::max());
		return (product.m_flavourOrderedLeptons.at(0)->flavour() == KLeptonFlavour::TAU ? (iso * product.m_flavourOrderedLeptons.at(0)->p4.Pt()) : iso);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep1MetPt", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedLeptons.at(0)->p4 + product.m_met.p4).Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep1MetEta", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedLeptons.at(0)->p4 + product.m_met.p4).Eta();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep1MetPhi", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedLeptons.at(0)->p4 + product.m_met.p4).Phi();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep1MetMass", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedLeptons.at(0)->p4 + product.m_met.p4).mass();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep1MetMt", [](event_type const& event, product_type const& product)
	{
		return Quantities::CalculateMt(product.m_flavourOrderedLeptons.at(0)->p4, product.m_met.p4);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedLep1Pt", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(0) ? product.m_flavourOrderedGenLeptonVisibleLVs.at(0)->Pt() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedLep1Eta", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(0) ? product.m_flavourOrderedGenLeptonVisibleLVs.at(0)->Eta() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedLep1Phi", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(0) ? product.m_flavourOrderedGenLeptonVisibleLVs.at(0)->Phi() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedLep1Mass", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(0) ? product.m_flavourOrderedGenLeptonVisibleLVs.at(0)->mass() : DefaultValues::UndefinedFloat);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "leadingGenMatchedTauDecayMode", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_ptOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->decayMode : DefaultValues::UndefinedInt);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "genMatchedTau1DecayMode", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->decayMode : DefaultValues::UndefinedInt);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "posGenMatchedTauDecayMode", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_chargeOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->decayMode : DefaultValues::UndefinedInt);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "leadingGenMatchedTauNProngs", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_ptOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->nProngs : DefaultValues::UndefinedInt);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "genMatchedTau1NProngs", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->nProngs : DefaultValues::UndefinedInt);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "posGenMatchedTauNProngs", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_chargeOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->nProngs : DefaultValues::UndefinedInt);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "leadingGenMatchedTauNPi0s", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_ptOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->nPi0s : DefaultValues::UndefinedInt);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "genMatchedTau1NPi0s", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->nPi0s : DefaultValues::UndefinedInt);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "posGenMatchedTauNPi0s", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_chargeOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->nPi0s : DefaultValues::UndefinedInt);
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "trailingLepCharge", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(1)->charge();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "trailingLepPt", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(1)->p4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "trailingLepEta", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(1)->p4.Eta();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "trailingLepPhi", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(1)->p4.Phi();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "trailingLepMass", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(1)->p4.mass();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "trailingLepMt", [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons.at(1)->p4.Mt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "trailingLepIso", [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolation, product.m_ptOrderedLeptons.at(1), DefaultValues::UndefinedDouble);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "trailingLepIsoOverPt", [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_ptOrderedLeptons.at(1), DefaultValues::UndefinedDouble);
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep2Charge", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->charge();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep2Dz", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->dz;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep2ErrDz", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->track.errDz();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep2D0", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->dxy;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep2ErrD0", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->track.errDxy();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep2TrackNInnerHits", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->track.nInnerHits;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep2TrackChi2OverNdof", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedLeptons.at(1)->track.chi2 / product.m_flavourOrderedLeptons.at(1)->track.nDOF);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep2TrackIsLooseQuality", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->track.quality(KTrackQuality::KTrackQualityType::loose);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep2TrackIsTightQuality", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->track.quality(KTrackQuality::KTrackQualityType::tight);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep2TrackIsHighPurityQuality", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->track.quality(KTrackQuality::KTrackQualityType::highPurity);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep2Pt", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->p4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep2Eta", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->p4.Eta();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep2Phi", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->p4.Phi();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep2Mass", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->p4.mass();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep2Mt", [](event_type const& event, product_type const& product)
	{
		return Quantities::CalculateMtH2Tau(product.m_flavourOrderedLeptons.at(1)->p4, product.m_met.p4);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep2Iso", [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolation, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedDouble);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep2IsoOverPt", [](event_type const& event, product_type const& product) {
		float iso = SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_flavourOrderedLeptons.at(1), std::numeric_limits<double>::max());
		return (product.m_flavourOrderedLeptons.at(1)->flavour() == KLeptonFlavour::TAU ? (iso * product.m_flavourOrderedLeptons.at(1)->p4.Pt()) : iso);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep2MetMt", [](event_type const& event, product_type const& product)
	{
		return Quantities::CalculateMt(product.m_flavourOrderedLeptons.at(1)->p4, product.m_met.p4);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedLep2Pt", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(1) ? product.m_flavourOrderedGenLeptonVisibleLVs.at(1)->Pt() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedLep2Eta", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(1) ? product.m_flavourOrderedGenLeptonVisibleLVs.at(1)->Eta() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedLep2Phi", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(1) ? product.m_flavourOrderedGenLeptonVisibleLVs.at(1)->Phi() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedLep2Mass", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(1) ? product.m_flavourOrderedGenLeptonVisibleLVs.at(1)->mass() : DefaultValues::UndefinedFloat);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "trailingGenMatchedTauDecayMode", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_ptOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->decayMode : DefaultValues::UndefinedInt);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "genMatchedTau2DecayMode", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->decayMode : DefaultValues::UndefinedInt);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "negGenMatchedTauDecayMode", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_chargeOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->decayMode : DefaultValues::UndefinedInt);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "trailingGenMatchedTauNProngs", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_ptOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->nProngs : DefaultValues::UndefinedInt);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "genMatchedTau2NProngs", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->nProngs : DefaultValues::UndefinedInt);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "negGenMatchedTauNProngs", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_chargeOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->nProngs : DefaultValues::UndefinedInt);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "trailingGenMatchedTauNPi0s", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_ptOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->nPi0s : DefaultValues::UndefinedInt);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "genMatchedTau2NPi0s", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->nPi0s : DefaultValues::UndefinedInt);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "negGenMatchedTauNPi0s", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_chargeOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->nPi0s : DefaultValues::UndefinedInt);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "extraelec_veto", [](event_type const& event, product_type const& product)
	{
		return static_cast<HttProduct const&>(product).m_extraElecVeto;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "extramuon_veto", [](event_type const& event, product_type const& product)
	{
		return static_cast<HttProduct const&>(product).m_extraMuonVeto;
	});
	

	std::vector<std::string> tauDiscriminators;
	tauDiscriminators.push_back("byCombinedIsolationDeltaBetaCorrRaw3Hits");
	tauDiscriminators.push_back("byLooseCombinedIsolationDeltaBetaCorr3Hits");
	tauDiscriminators.push_back("byMediumCombinedIsolationDeltaBetaCorr3Hits");
	tauDiscriminators.push_back("byTightCombinedIsolationDeltaBetaCorr3Hits");
	tauDiscriminators.push_back("trigweight");
	tauDiscriminators.push_back("againstElectronLooseMVA6");
	tauDiscriminators.push_back("againstElectronMediumMVA6");
	tauDiscriminators.push_back("againstElectronTightMVA6");
	tauDiscriminators.push_back("againstElectronVLooseMVA6");
	tauDiscriminators.push_back("againstElectronVTightMVA6");
	tauDiscriminators.push_back("againstMuonLoose3");
	tauDiscriminators.push_back("againstMuonTight3");
	// provided with files 2015 | 2017v1
	tauDiscriminators.push_back("byIsolationMVArun2v1DBoldDMwLTraw");
	tauDiscriminators.push_back("byVVLooseIsolationMVArun2v1DBoldDMwLT");
	tauDiscriminators.push_back("byVLooseIsolationMVArun2v1DBoldDMwLT");
	tauDiscriminators.push_back("byLooseIsolationMVArun2v1DBoldDMwLT");
	tauDiscriminators.push_back("byMediumIsolationMVArun2v1DBoldDMwLT");
	tauDiscriminators.push_back("byTightIsolationMVArun2v1DBoldDMwLT");
	tauDiscriminators.push_back("byVTightIsolationMVArun2v1DBoldDMwLT");
	tauDiscriminators.push_back("byVVTightIsolationMVArun2v1DBoldDMwLT");
	// 2017v1_oldDM training for Fall 17 skims after April 2018
	tauDiscriminators.push_back("byIsolationMVArun2017v1DBoldDMwLTraw2017");
	tauDiscriminators.push_back("byVVLooseIsolationMVArun2017v1DBoldDMwLT2017");
	tauDiscriminators.push_back("byVLooseIsolationMVArun2017v1DBoldDMwLT2017");
	tauDiscriminators.push_back("byLooseIsolationMVArun2017v1DBoldDMwLT2017");
	tauDiscriminators.push_back("byMediumIsolationMVArun2017v1DBoldDMwLT2017");
	tauDiscriminators.push_back("byTightIsolationMVArun2017v1DBoldDMwLT2017");
	tauDiscriminators.push_back("byVTightIsolationMVArun2017v1DBoldDMwLT2017");
	tauDiscriminators.push_back("byVVTightIsolationMVArun2017v1DBoldDMwLT2017");
	// 2017v2 training for Fall 17 skims after April 2018
	tauDiscriminators.push_back("byIsolationMVArun2017v2DBoldDMwLTraw2017");
	tauDiscriminators.push_back("byVVLooseIsolationMVArun2017v2DBoldDMwLT2017");
	tauDiscriminators.push_back("byVLooseIsolationMVArun2017v2DBoldDMwLT2017");
	tauDiscriminators.push_back("byLooseIsolationMVArun2017v2DBoldDMwLT2017");
	tauDiscriminators.push_back("byMediumIsolationMVArun2017v2DBoldDMwLT2017");
	tauDiscriminators.push_back("byTightIsolationMVArun2017v2DBoldDMwLT2017");
	tauDiscriminators.push_back("byVTightIsolationMVArun2017v2DBoldDMwLT2017");
	tauDiscriminators.push_back("byVVTightIsolationMVArun2017v2DBoldDMwLT2017");
	// newDM2017v2 training for Fall 17 skims after April 2018
	tauDiscriminators.push_back("byIsolationMVArun2017v2DBnewDMwLTraw2017");
	tauDiscriminators.push_back("byVVLooseIsolationMVArun2017v2DBnewDMwLT2017");
	tauDiscriminators.push_back("byVLooseIsolationMVArun2017v2DBnewDMwLT2017");
	tauDiscriminators.push_back("byLooseIsolationMVArun2017v2DBnewDMwLT2017");
	tauDiscriminators.push_back("byMediumIsolationMVArun2017v2DBnewDMwLT2017");
	tauDiscriminators.push_back("byTightIsolationMVArun2017v2DBnewDMwLT2017");
	tauDiscriminators.push_back("byVTightIsolationMVArun2017v2DBnewDMwLT2017");
	tauDiscriminators.push_back("byVVTightIsolationMVArun2017v2DBnewDMwLT2017");

		// 2017v1 training used in skim on 2018-02-13 - should NOT be used after full skim
		tauDiscriminators.push_back("rerunDiscriminationByIsolationMVArun2v1raw");
		tauDiscriminators.push_back("rerunDiscriminationByIsolationMVArun2v1VVLoose");
		tauDiscriminators.push_back("rerunDiscriminationByIsolationMVArun2v1VLoose");
		tauDiscriminators.push_back("rerunDiscriminationByIsolationMVArun2v1Loose");
		tauDiscriminators.push_back("rerunDiscriminationByIsolationMVArun2v1Medium");
		tauDiscriminators.push_back("rerunDiscriminationByIsolationMVArun2v1Tight");
		tauDiscriminators.push_back("rerunDiscriminationByIsolationMVArun2v1VTight");
		tauDiscriminators.push_back("rerunDiscriminationByIsolationMVArun2v1VVTight");
		tauDiscriminators.push_back("rerunDiscriminationByIsolationMVArun2v1VVTight");
		// 2016 training for skims of 2016 samples before April 2018 - should NOT be used after full skim
		tauDiscriminators.push_back("rerunDiscriminationByIsolationMVAOldDMrun2v1raw");
		tauDiscriminators.push_back("rerunDiscriminationByIsolationMVAOldDMrun2v1VLoose");
		tauDiscriminators.push_back("rerunDiscriminationByIsolationMVAOldDMrun2v1Loose");
		tauDiscriminators.push_back("rerunDiscriminationByIsolationMVAOldDMrun2v1Medium");
		tauDiscriminators.push_back("rerunDiscriminationByIsolationMVAOldDMrun2v1Tight");
		tauDiscriminators.push_back("rerunDiscriminationByIsolationMVAOldDMrun2v1VTight");
		tauDiscriminators.push_back("rerunDiscriminationByIsolationMVAOldDMrun2v1VVTight");

	// dR0p32017v2
	tauDiscriminators.push_back("byIsolationMVArun2017v2DBoldDMdR0p3wLTraw2017");
	tauDiscriminators.push_back("byVVLooseIsolationMVArun2017v2DBoldDMdR0p3wLT2017");
	tauDiscriminators.push_back("byVLooseIsolationMVArun2017v2DBoldDMdR0p3wLT2017");
	tauDiscriminators.push_back("byLooseIsolationMVArun2017v2DBoldDMdR0p3wLT2017");
	tauDiscriminators.push_back("byMediumIsolationMVArun2017v2DBoldDMdR0p3wLT2017");
	tauDiscriminators.push_back("byTightIsolationMVArun2017v2DBoldDMdR0p3wLT2017");
	tauDiscriminators.push_back("byVTightIsolationMVArun2017v2DBoldDMdR0p3wLT2017");
	tauDiscriminators.push_back("byVVTightIsolationMVArun2017v2DBoldDMdR0p3wLT2017");
	// 2016v1
	tauDiscriminators.push_back("byIsolationMVArun2v1DBoldDMwLTraw2016");
	tauDiscriminators.push_back("byVLooseIsolationMVArun2v1DBoldDMwLT2016");
	tauDiscriminators.push_back("byLooseIsolationMVArun2v1DBoldDMwLT2016");
	tauDiscriminators.push_back("byMediumIsolationMVArun2v1DBoldDMwLT2016");
	tauDiscriminators.push_back("byTightIsolationMVArun2v1DBoldDMwLT2016");
	tauDiscriminators.push_back("byVTightIsolationMVArun2v1DBoldDMwLT2016");
	tauDiscriminators.push_back("byVVTightIsolationMVArun2v1DBoldDMwLT2016");
	// newDM2016v1
	tauDiscriminators.push_back("byIsolationMVArun2v1DBnewDMwLTraw2016");
	tauDiscriminators.push_back("byVLooseIsolationMVArun2v1DBnewDMwLT2016");
	tauDiscriminators.push_back("byLooseIsolationMVArun2v1DBnewDMwLT2016");
	tauDiscriminators.push_back("byMediumIsolationMVArun2v1DBnewDMwLT2016");
	tauDiscriminators.push_back("byTightIsolationMVArun2v1DBnewDMwLT2016");
	tauDiscriminators.push_back("byVTightIsolationMVArun2v1DBnewDMwLT2016");
	tauDiscriminators.push_back("byVVTightIsolationMVArun2v1DBnewDMwLT2016");
	// -------
	tauDiscriminators.push_back("chargedIsoPtSum");
	tauDiscriminators.push_back("decayModeFinding");
	tauDiscriminators.push_back("decayModeFindingNewDMs");
	tauDiscriminators.push_back("neutralIsoPtSum");
	tauDiscriminators.push_back("puCorrPtSum");
	tauDiscriminators.push_back("footprintCorrection");
	tauDiscriminators.push_back("photonPtSumOutsideSignalCone");
	tauDiscriminators.push_back("decayDistX");
	tauDiscriminators.push_back("decayDistY");
	tauDiscriminators.push_back("decayDistZ");
	tauDiscriminators.push_back("decayDistM");
	tauDiscriminators.push_back("nPhoton");
	tauDiscriminators.push_back("ptWeightedDetaStrip");
	tauDiscriminators.push_back("ptWeightedDphiStrip");
	tauDiscriminators.push_back("ptWeightedDrSignal");
	tauDiscriminators.push_back("ptWeightedDrIsolation");
	tauDiscriminators.push_back("leadingTrackChi2");
	tauDiscriminators.push_back("eRatio");
	
	

	for (size_t leptonIndex = 0; leptonIndex < 2; ++leptonIndex)
	{
		for (std::string tauDiscriminator : tauDiscriminators)
		{
			std::string quantity = tauDiscriminator + "_" + std::to_string(leptonIndex+1);
			LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, quantity, [tauDiscriminator, leptonIndex](event_type const& event, product_type const& product)
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
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, decayModeQuantity, [leptonIndex](event_type const& event, product_type const& product)
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
		bool useUWGenMatching = settings.GetUseUWGenMatching();
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, genMatchQuantity, [leptonIndex, useUWGenMatching](event_type const& event, product_type const& product)
		{
			if (useUWGenMatching)
			{
				KLepton* lepton = product.m_flavourOrderedLeptons.at(leptonIndex);
				KLepton* originalLepton = const_cast<KLepton*>(SafeMap::GetWithDefault(product.m_originalLeptons, const_cast<const KLepton*>(lepton), const_cast<const KLepton*>(lepton)));
				return Utility::ToUnderlyingValue(GeneratorInfo::GetGenMatchingCodeUW(event, originalLepton));
			}
			else
			{
				KGenParticle* genParticle = product.m_flavourOrderedGenLeptons.at(leptonIndex);
				if (genParticle)
				{
					return Utility::ToUnderlyingValue(GeneratorInfo::GetGenMatchingCode(genParticle));
				}
				else
				{
					return Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_FAKE);
				}
			}
		});
		
		std::string hadGenMatchPtQuantity = "had_gen_match_pT_" + std::to_string(leptonIndex+1);
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, hadGenMatchPtQuantity, [leptonIndex](event_type const& event, product_type const& product)
		{
			KGenParticle* genParticle = product.m_flavourOrderedGenLeptons.at(leptonIndex);

			// Return pT in case it matches a hadronic tau
			if (genParticle && (GeneratorInfo::GetGenMatchingCode(genParticle) == KappaEnumTypes::GenMatchingCode::IS_TAU_HAD_DECAY))
			{
				KGenTau* genTau = static_cast<KGenTau*>(genParticle);
				return genTau->visible.p4.Pt();
			}
			else
			{
				return 0.0f;
			}
		});
	}
}

void DecayChannelProducer::Produce(event_type const& event, product_type& product,
	                               setting_type const& settings, metadata_type const& metadata) const
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
		KLepton* originalLepton = const_cast<KLepton*>(SafeMap::GetWithDefault(product.m_originalLeptons, const_cast<const KLepton*>(*lepton), const_cast<const KLepton*>(*lepton)));
		product.m_ptOrderedGenLeptons.push_back(GeneratorInfo::GetGenMatchedParticle(
				originalLepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedLeptons
		));
		product.m_ptOrderedGenLeptonVisibleLVs.push_back(GeneratorInfo::GetVisibleLV(product.m_ptOrderedGenLeptons.back()));
	}
	
	product.m_flavourOrderedGenLeptons.clear();
	for (std::vector<KLepton*>::iterator lepton = product.m_flavourOrderedLeptons.begin();
	     lepton != product.m_flavourOrderedLeptons.end(); ++lepton)
	{
		KLepton* originalLepton = const_cast<KLepton*>(SafeMap::GetWithDefault(product.m_originalLeptons, const_cast<const KLepton*>(*lepton), const_cast<const KLepton*>(*lepton)));
		product.m_flavourOrderedGenLeptons.push_back(GeneratorInfo::GetGenMatchedParticle(
				originalLepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedLeptons
		));
		product.m_flavourOrderedGenLeptonVisibleLVs.push_back(GeneratorInfo::GetVisibleLV(product.m_flavourOrderedGenLeptons.back()));
	}
	
	product.m_chargeOrderedGenLeptons.clear();
	for (std::vector<KLepton*>::iterator lepton = product.m_chargeOrderedLeptons.begin();
	     lepton != product.m_chargeOrderedLeptons.end(); ++lepton)
	{
		KLepton* originalLepton = const_cast<KLepton*>(SafeMap::GetWithDefault(product.m_originalLeptons, const_cast<const KLepton*>(*lepton), const_cast<const KLepton*>(*lepton)));
		product.m_chargeOrderedGenLeptons.push_back(GeneratorInfo::GetGenMatchedParticle(
				originalLepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedLeptons
		));
		product.m_chargeOrderedGenLeptonVisibleLVs.push_back(GeneratorInfo::GetVisibleLV(product.m_chargeOrderedGenLeptons.back()));
	}
}


void TTHDecayChannelProducer::Produce(event_type const& event, product_type& product,
	                              setting_type const& settings, metadata_type const& metadata) const
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

void Run2DecayChannelProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	DecayChannelProducer::Init(settings, metadata);

	// For taus in Run2 we use dz saved in the KTau
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep1Dz", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->dz;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "lep2Dz", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->dz;
	});
}

void Run2DecayChannelProducer::Produce(event_type const& event, product_type& product,
	                              setting_type const& settings, metadata_type const& metadata) const
{
	assert(product.m_validDiTauPairCandidates.size() > 0);

	product.m_decayChannel = m_decayChannel;

	// fill the lepton vectors
	DiTauPair diTauPair = product.m_validDiTauPairCandidates.at(0);
	KLepton* lepton1 = static_cast<KLepton*>(diTauPair.first);
	KLepton* lepton2 = static_cast<KLepton*>(diTauPair.second);

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

	// clean loose electrons/muons from signal electrons/muons
	std::vector<KElectron*> looseElectrons;
	for (std::vector<KElectron*>::iterator looseElectron = product.m_validLooseElectrons.begin();
		 looseElectron != product.m_validLooseElectrons.end(); ++looseElectron)
	{
		bool looseElectronAlsoSignalElectron = false;
		for (std::vector<KElectron*>::iterator electron = product.m_validElectrons.begin();
			 electron != product.m_validElectrons.end(); ++electron)
		{
			if ((*looseElectron)->p4 == (*electron)->p4)
			{
				looseElectronAlsoSignalElectron = true;
			}
		}
		if (!looseElectronAlsoSignalElectron)
			looseElectrons.push_back(*looseElectron);
	}
	std::vector<KMuon*> looseMuons;
	for (std::vector<KMuon*>::iterator looseMuon = product.m_validLooseMuons.begin();
		 looseMuon != product.m_validLooseMuons.end(); ++looseMuon)
	{
		bool looseMuonAlsoSignalMuon = false;
		for (std::vector<KMuon*>::iterator muon = product.m_validMuons.begin();
			 muon != product.m_validMuons.end(); ++muon)
		{
			if ((*looseMuon)->p4 == (*muon)->p4)
			{
				looseMuonAlsoSignalMuon = true;
			}
		}
		if (!looseMuonAlsoSignalMuon)
			looseMuons.push_back(*looseMuon);
	}
	// set boolean veto variables
	product.m_extraElecVeto = (looseElectrons.size() > 0);
	product.m_extraMuonVeto = (looseMuons.size() > 0);
	if ((m_decayChannel == HttEnumTypes::DecayChannel::TT) || (m_decayChannel == HttEnumTypes::DecayChannel::ET) || (m_decayChannel == HttEnumTypes::DecayChannel::EE))
	{
		product.m_extraMuonVeto = (product.m_validLooseMuons.size() > 0);
	}
	if ((m_decayChannel == HttEnumTypes::DecayChannel::TT) || (m_decayChannel == HttEnumTypes::DecayChannel::MT) || (m_decayChannel == HttEnumTypes::DecayChannel::MM))
	{
		product.m_extraElecVeto = (product.m_validLooseElectrons.size() > 0);
	}
	FillGenLeptonCollections(product);
}
