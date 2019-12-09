
//#include <boost/algorithm/string.hpp>
//#include <boost/algorithm/string/trim.hpp>
//#include <boost/filesystem/convenience.hpp>

#include "TauAnalysis/ClassicSVfit/interface/MeasuredTauLepton.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/FastMttProducer.h"


FastMttProducer::FastMttProducer(
		std::string name,
		FastMttResults product_type::*fastmttResultsMember,
		std::map<KLepton*, RMFLV> product_type::*fastmttTausMember
) :
	ProducerBase<HttTypes>(),
	m_name(name),
	m_fastmttResultsMember(fastmttResultsMember),
	m_fastmttTausMember(fastmttTausMember)
{
}

std::string FastMttProducer::GetProducerId() const
{
	return "FastMttProducer";
}

void FastMttProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "fastmtt"+m_name+"Available", [this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return ((product.*m_fastmttResultsMember).fittedHiggsLV ? true : false);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "fastmtt"+m_name+"Pt", [this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return ((product.*m_fastmttResultsMember).fittedHiggsLV ? (product.*m_fastmttResultsMember).fittedHiggsLV->Pt() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "fastmtt"+m_name+"Eta", [this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return ((product.*m_fastmttResultsMember).fittedHiggsLV ? (product.*m_fastmttResultsMember).fittedHiggsLV->Eta() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "fastmtt"+m_name+"Phi", [this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return ((product.*m_fastmttResultsMember).fittedHiggsLV ? (product.*m_fastmttResultsMember).fittedHiggsLV->Phi() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "fastmtt"+m_name+"Mass", [this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return ((product.*m_fastmttResultsMember).fittedHiggsLV ? (product.*m_fastmttResultsMember).fittedHiggsLV->mass() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "fastmtt"+m_name+"LV", [this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return ((product.*m_fastmttResultsMember).fittedHiggsLV ? *((product.*m_fastmttResultsMember).fittedHiggsLV) : DefaultValues::UndefinedRMFLV);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "fastmtt"+m_name+"Tau1Available", [this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	        return ((product.*m_fastmttResultsMember).fittedTau1LV ? true : false);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "fastmtt"+m_name+"Tau1LV", [this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	        return ((product.*m_fastmttResultsMember).fittedTau1LV ? *((product.*m_fastmttResultsMember).fittedTau1LV) : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "fastmtt"+m_name+"Tau1ERatio", [this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	        return (product.*m_fastmttResultsMember).fittedTau1ERatio;
	});

	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "fastmtt"+m_name+"Tau2Available", [this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	        return ((product.*m_fastmttResultsMember).fittedTau2LV ? true : false);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "fastmtt"+m_name+"Tau2LV", [this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	        return ((product.*m_fastmttResultsMember).fittedTau2LV ? *((product.*m_fastmttResultsMember).fittedTau2LV) : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "fastmtt"+m_name+"Tau2ERatio", [this](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	        return (product.*m_fastmttResultsMember).fittedTau2ERatio;
	});
}

void FastMttProducer::Produce(event_type const& event, product_type& product,
			      setting_type const& settings, metadata_type const& metadata) const
{
	assert(event.m_eventInfo);

	// consider only the first two leptons
	assert(product.m_flavourOrderedLeptons.size() >= 2);
	KLepton* lepton1 = product.m_flavourOrderedLeptons[0];
	KLepton* lepton2 = product.m_flavourOrderedLeptons[1];
	
	// construct decay types/modes
	classic_svFit::MeasuredTauLepton::kDecayType decayType1 = classic_svFit::MeasuredTauLepton::kTauToHadDecay;
	int decayMode1 = -1;
	if (lepton1->flavour() == KLeptonFlavour::ELECTRON)
	{
		decayType1 = classic_svFit::MeasuredTauLepton::kTauToElecDecay;
		decayMode1 = -1;
	}
	else if (lepton1->flavour() == KLeptonFlavour::MUON)
	{
		decayType1 = classic_svFit::MeasuredTauLepton::kTauToMuDecay;
		decayMode1 = -1;
	}
	else if (lepton1->flavour() == KLeptonFlavour::TAU)
	{
		decayType1 = classic_svFit::MeasuredTauLepton::kTauToHadDecay;
		decayMode1 = static_cast<KTau*>(lepton1)->decayMode;
	}
	
	classic_svFit::MeasuredTauLepton::kDecayType decayType2 = classic_svFit::MeasuredTauLepton::kTauToHadDecay;
	int decayMode2 = -1;
	if (lepton2->flavour() == KLeptonFlavour::ELECTRON)
	{
		decayType2 = classic_svFit::MeasuredTauLepton::kTauToElecDecay;
		decayMode2 = -1;
	}
	else if (lepton2->flavour() == KLeptonFlavour::MUON)
	{
		decayType2 = classic_svFit::MeasuredTauLepton::kTauToMuDecay;
		decayMode2 = -1;
	}
	else if (lepton2->flavour() == KLeptonFlavour::TAU)
	{
		decayType2 = classic_svFit::MeasuredTauLepton::kTauToHadDecay;
		decayMode2 = static_cast<KTau*>(lepton2)->decayMode;
	}
	
	// set inputs
	FastMttInputs fastmttInputs(lepton1->p4, decayType1, decayMode1,
				    lepton2->p4, decayType2, decayMode2,
				    product.m_met.p4.Vect(), product.m_met.significance);

	// calculate results
	(product.*m_fastmttResultsMember) = fastmttTools.GetResults(fastmttInputs);

	if ((product.*m_fastmttResultsMember).fittedTau1LV)
	{
		(product.*m_fastmttTausMember)[lepton1] = *((product.*m_fastmttResultsMember).fittedTau1LV);
	}
	if ((product.*m_fastmttResultsMember).fittedTau2LV)
	{
		(product.*m_fastmttTausMember)[lepton2] = *((product.*m_fastmttResultsMember).fittedTau2LV);
	}

	// apply systematic shifts
	if((product.*m_fastmttResultsMember).fittedHiggsLV)
	{
		(product.*m_fastmttResultsMember).fittedHiggsLV->SetM((product.*m_fastmttResultsMember).fittedHiggsLV->M() * settings.GetFastMttMassShift());
	}
}
