
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DecayChannelProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/Quantities.h"
#include "Artus/KappaAnalysis/interface/Utility/GeneratorInfo.h"


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

	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("leadingLepSumChargedHadronsLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_ptOrderedLeptons.at(0)->flavour() == KLeptonFlavour::TAU ? static_cast<KTau*>(product.m_ptOrderedLeptons.at(0))->sumChargedHadronCandidates() : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("lep1SumChargedHadronsLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedLeptons.at(0)->flavour() == KLeptonFlavour::TAU ? static_cast<KTau*>(product.m_flavourOrderedLeptons.at(0))->sumChargedHadronCandidates() : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("posLepSumChargedHadronsLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_chargeOrderedLeptons.at(0)->flavour() == KLeptonFlavour::TAU ? static_cast<KTau*>(product.m_chargeOrderedLeptons.at(0))->sumChargedHadronCandidates() : DefaultValues::UndefinedRMFLV);
	});

	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("leadingLepSumNeutralHadronsLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_ptOrderedLeptons.at(0)->flavour() == KLeptonFlavour::TAU ? static_cast<KTau*>(product.m_ptOrderedLeptons.at(0))->piZeroMomentum() : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("lep1SumNeutralHadronsLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedLeptons.at(0)->flavour() == KLeptonFlavour::TAU ? static_cast<KTau*>(product.m_flavourOrderedLeptons.at(0))->piZeroMomentum() : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("posLepSumNeutralHadronsLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_chargeOrderedLeptons.at(0)->flavour() == KLeptonFlavour::TAU ? static_cast<KTau*>(product.m_chargeOrderedLeptons.at(0))->piZeroMomentum() : DefaultValues::UndefinedRMFLV);
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

	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("trailingLepSumChargedHadronsLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_ptOrderedLeptons.at(1)->flavour() == KLeptonFlavour::TAU ? static_cast<KTau*>(product.m_ptOrderedLeptons.at(1))->sumChargedHadronCandidates() : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("lep2SumChargedHadronsLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedLeptons.at(1)->flavour() == KLeptonFlavour::TAU ? static_cast<KTau*>(product.m_flavourOrderedLeptons.at(1))->sumChargedHadronCandidates() : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("negLepSumChargedHadronsLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_chargeOrderedLeptons.at(1)->flavour() == KLeptonFlavour::TAU ? static_cast<KTau*>(product.m_chargeOrderedLeptons.at(1))->sumChargedHadronCandidates() : DefaultValues::UndefinedRMFLV);
	});

	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("trailingLepSumNeutralHadronsLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_ptOrderedLeptons.at(1)->flavour() == KLeptonFlavour::TAU ? static_cast<KTau*>(product.m_ptOrderedLeptons.at(1))->piZeroMomentum() : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("lep2SumNeutralHadronsLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedLeptons.at(1)->flavour() == KLeptonFlavour::TAU ? static_cast<KTau*>(product.m_flavourOrderedLeptons.at(1))->piZeroMomentum() : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("negLepSumNeutralHadronsLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_chargeOrderedLeptons.at(1)->flavour() == KLeptonFlavour::TAU ? static_cast<KTau*>(product.m_chargeOrderedLeptons.at(1))->piZeroMomentum() : DefaultValues::UndefinedRMFLV);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("leadingGenMatchedLepLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_ptOrderedGenLeptonVisibleLVs.at(0) ? *(product.m_ptOrderedGenLeptonVisibleLVs.at(0)) : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("genMatchedLep1LV", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(0) ? *(product.m_flavourOrderedGenLeptonVisibleLVs.at(0)) : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("posGenMatchedLepLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_chargeOrderedGenLeptonVisibleLVs.at(0) ? *(product.m_chargeOrderedGenLeptonVisibleLVs.at(0)) : DefaultValues::UndefinedRMFLV);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("leadingGenMatchedLepFound", [](event_type const& event, product_type const& product)
	{
		return (product.m_ptOrderedGenLeptons.at(0) != nullptr);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("genMatchedLep1Found", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptons.at(0) != nullptr);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("posGenMatchedLepFound", [](event_type const& event, product_type const& product)
	{
		return (product.m_chargeOrderedGenLeptons.at(0) != nullptr);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("leadingGenMatchedTauLV", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_ptOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->p4 : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("genMatchedTau1LV", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->p4 : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("posGenMatchedTauLV", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_chargeOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->p4 : DefaultValues::UndefinedRMFLV);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("leadingGenMatchedTauVisibleLV", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_ptOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->visible.p4 : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("genMatchedTau1VisibleLV", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->visible.p4 : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("posGenMatchedTauVisibleLV", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_chargeOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->visible.p4 : DefaultValues::UndefinedRMFLV);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("leadingGenMatchedTauFound", [](event_type const& event, product_type const& product)
	{
		return Utility::Contains(product.m_genTauMatchedLeptons, product.m_ptOrderedLeptons.at(0));
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("genMatchedTau1Found", [](event_type const& event, product_type const& product)
	{
		return Utility::Contains(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(0));
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("posGenMatchedTauFound", [](event_type const& event, product_type const& product)
	{
		return Utility::Contains(product.m_genTauMatchedLeptons, product.m_chargeOrderedLeptons.at(0));
	});
	
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("trailingGenMatchedLepLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_ptOrderedGenLeptonVisibleLVs.at(1) ? *(product.m_ptOrderedGenLeptonVisibleLVs.at(1)) : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("genMatchedLep2LV", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(1) ? *(product.m_flavourOrderedGenLeptonVisibleLVs.at(1)) : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("negGenMatchedLepLV", [](event_type const& event, product_type const& product)
	{
		return (product.m_chargeOrderedGenLeptonVisibleLVs.at(1) ? *(product.m_chargeOrderedGenLeptonVisibleLVs.at(1)) : DefaultValues::UndefinedRMFLV);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("trailingGenMatchedLepFound", [](event_type const& event, product_type const& product)
	{
		return (product.m_ptOrderedGenLeptons.at(1) != nullptr);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("genMatchedLep2Found", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptons.at(1) != nullptr);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("negGenMatchedLepFound", [](event_type const& event, product_type const& product)
	{
		return (product.m_chargeOrderedGenLeptons.at(1) != nullptr);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("trailingGenMatchedTauLV", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_ptOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->p4 : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("genMatchedTau2LV", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->p4 : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("negGenMatchedTauLV", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_chargeOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->p4 : DefaultValues::UndefinedRMFLV);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("trailingGenMatchedTauVisibleLV", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_ptOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->visible.p4 : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("genMatchedTau2VisibleLV", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->visible.p4 : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("negGenMatchedTauVisibleLV", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_chargeOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->visible.p4 : DefaultValues::UndefinedRMFLV);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("trailingGenMatchedTauFound", [](event_type const& event, product_type const& product)
	{
		return Utility::Contains(product.m_genTauMatchedLeptons, product.m_ptOrderedLeptons.at(1));
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("genMatchedTau2Found", [](event_type const& event, product_type const& product)
	{
		return Utility::Contains(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(1));
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("negGenMatchedTauFound", [](event_type const& event, product_type const& product)
	{
		return Utility::Contains(product.m_genTauMatchedLeptons, product.m_chargeOrderedLeptons.at(1));
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
		return product.m_flavourOrderedLeptons.at(0)->dz;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1ErrDz", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->track.errDz;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1D0", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->dxy;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1ErrD0", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0)->track.errDxy;
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
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genMatchedLep1Pt", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(0) ? product.m_flavourOrderedGenLeptonVisibleLVs.at(0)->Pt() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genMatchedLep1Eta", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(0) ? product.m_flavourOrderedGenLeptonVisibleLVs.at(0)->Eta() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genMatchedLep1Phi", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(0) ? product.m_flavourOrderedGenLeptonVisibleLVs.at(0)->Phi() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genMatchedLep1Mass", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(0) ? product.m_flavourOrderedGenLeptonVisibleLVs.at(0)->mass() : DefaultValues::UndefinedFloat);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("leadingGenMatchedTauDecayMode", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_ptOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->decayMode : DefaultValues::UndefinedInt);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("genMatchedTau1DecayMode", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->decayMode : DefaultValues::UndefinedInt);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("posGenMatchedTauDecayMode", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_chargeOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->decayMode : DefaultValues::UndefinedInt);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("leadingGenMatchedTauNProngs", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_ptOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->nProngs : DefaultValues::UndefinedInt);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("genMatchedTau1NProngs", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->nProngs : DefaultValues::UndefinedInt);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("posGenMatchedTauNProngs", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_chargeOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->nProngs : DefaultValues::UndefinedInt);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("leadingGenMatchedTauNPi0s", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_ptOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->nPi0s : DefaultValues::UndefinedInt);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("genMatchedTau1NPi0s", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->nPi0s : DefaultValues::UndefinedInt);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("posGenMatchedTauNPi0s", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_chargeOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->nPi0s : DefaultValues::UndefinedInt);
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
		return product.m_flavourOrderedLeptons.at(1)->dz;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2ErrDz", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->track.errDz;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2D0", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->dxy;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2ErrD0", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->track.errDxy;
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
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genMatchedLep2Pt", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(1) ? product.m_flavourOrderedGenLeptonVisibleLVs.at(1)->Pt() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genMatchedLep2Eta", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(1) ? product.m_flavourOrderedGenLeptonVisibleLVs.at(1)->Eta() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genMatchedLep2Phi", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(1) ? product.m_flavourOrderedGenLeptonVisibleLVs.at(1)->Phi() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genMatchedLep2Mass", [](event_type const& event, product_type const& product)
	{
		return (product.m_flavourOrderedGenLeptonVisibleLVs.at(1) ? product.m_flavourOrderedGenLeptonVisibleLVs.at(1)->mass() : DefaultValues::UndefinedFloat);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("trailingGenMatchedTauDecayMode", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_ptOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->decayMode : DefaultValues::UndefinedInt);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("genMatchedTau2DecayMode", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->decayMode : DefaultValues::UndefinedInt);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("negGenMatchedTauDecayMode", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_chargeOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->decayMode : DefaultValues::UndefinedInt);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("trailingGenMatchedTauNProngs", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_ptOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->nProngs : DefaultValues::UndefinedInt);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("genMatchedTau2NProngs", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->nProngs : DefaultValues::UndefinedInt);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("negGenMatchedTauNProngs", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_chargeOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->nProngs : DefaultValues::UndefinedInt);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("trailingGenMatchedTauNPi0s", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_ptOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->nPi0s : DefaultValues::UndefinedInt);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("genMatchedTau2NPi0s", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->nPi0s : DefaultValues::UndefinedInt);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("negGenMatchedTauNPi0s", [](event_type const& event, product_type const& product)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_chargeOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));
		return (genTau ? genTau->nPi0s : DefaultValues::UndefinedInt);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("extraelec_veto", [](KappaEvent const& event, KappaProduct const& product)
	{
		return static_cast<HttProduct const&>(product).m_extraElecVeto;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("extramuon_veto", [](KappaEvent const& event, KappaProduct const& product)
	{
		return static_cast<HttProduct const&>(product).m_extraMuonVeto;
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pt_1", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["lep1Pt"]);

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pt_2", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["lep2Pt"]);

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
	tauDiscriminators.push_back("byIsolationMVArun2v1DBoldDMwLTraw");
	tauDiscriminators.push_back("byVLooseIsolationMVArun2v1DBoldDMwLT");
	tauDiscriminators.push_back("byLooseIsolationMVArun2v1DBoldDMwLT");
	tauDiscriminators.push_back("byMediumIsolationMVArun2v1DBoldDMwLT");
	tauDiscriminators.push_back("byTightIsolationMVArun2v1DBoldDMwLT");
	tauDiscriminators.push_back("byVTightIsolationMVArun2v1DBoldDMwLT");
	tauDiscriminators.push_back("byVVTightIsolationMVArun2v1DBoldDMwLT");
	tauDiscriminators.push_back("rerunDiscriminationByIsolationMVAOldDMrun2v1raw");
	tauDiscriminators.push_back("rerunDiscriminationByIsolationMVAOldDMrun2v1VLoose");
	tauDiscriminators.push_back("rerunDiscriminationByIsolationMVAOldDMrun2v1Loose");
	tauDiscriminators.push_back("rerunDiscriminationByIsolationMVAOldDMrun2v1Medium");
	tauDiscriminators.push_back("rerunDiscriminationByIsolationMVAOldDMrun2v1Tight");
	tauDiscriminators.push_back("rerunDiscriminationByIsolationMVAOldDMrun2v1VTight");
	tauDiscriminators.push_back("rerunDiscriminationByIsolationMVAOldDMrun2v1VVTight");
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
				return Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_FAKE);
			}
		});
		
		std::string hadGenMatchPtQuantity = "had_gen_match_pT_" + std::to_string(leptonIndex+1);
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(hadGenMatchPtQuantity, [leptonIndex](event_type const& event, product_type const& product)
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
				*lepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedLeptons
		));
		product.m_ptOrderedGenLeptonVisibleLVs.push_back(GeneratorInfo::GetVisibleLV(product.m_ptOrderedGenLeptons.back()));
	}
	
	product.m_flavourOrderedGenLeptons.clear();
	for (std::vector<KLepton*>::iterator lepton = product.m_flavourOrderedLeptons.begin();
	     lepton != product.m_flavourOrderedLeptons.end(); ++lepton)
	{
		product.m_flavourOrderedGenLeptons.push_back(GeneratorInfo::GetGenMatchedParticle(
				*lepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedLeptons
		));
		product.m_flavourOrderedGenLeptonVisibleLVs.push_back(GeneratorInfo::GetVisibleLV(product.m_flavourOrderedGenLeptons.back()));
	}
	
	product.m_chargeOrderedGenLeptons.clear();
	for (std::vector<KLepton*>::iterator lepton = product.m_chargeOrderedLeptons.begin();
	     lepton != product.m_chargeOrderedLeptons.end(); ++lepton)
	{
		product.m_chargeOrderedGenLeptons.push_back(GeneratorInfo::GetGenMatchedParticle(
				*lepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedLeptons
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
		return product.m_flavourOrderedLeptons.at(0)->dz;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2Dz", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1)->dz;
	});
}

void Run2DecayChannelProducer::Produce(event_type const& event, product_type& product,
	                              setting_type const& settings) const
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
