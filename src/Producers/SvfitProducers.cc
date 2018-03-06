
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>
#include <boost/filesystem/convenience.hpp>
#include "boost/functional/hash.hpp"

#include "TauAnalysis/ClassicSVfit/interface/MeasuredTauLepton.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/SvfitProducers.h"


SvfitProducer::SvfitProducer(
		std::string name,
		float diTauMassConstraint,
		SvfitEventKey product_type::*svfitEventKeyMember,
		SvfitResults product_type::*svfitResultsMember,
		std::map<KLepton*, RMFLV> product_type::*svfitTausMember,
		std::string (setting_type::*GetSvfitCacheFileMember)(void) const,
		std::string (setting_type::*GetSvfitCacheFileFolderMember)(void) const,
		std::string (setting_type::*GetSvfitCacheTreeMember)(void) const
) :
	ProducerBase<HttTypes>(),
	m_name(name),
	m_diTauMassConstraint(diTauMassConstraint),
	m_svfitEventKeyMember(svfitEventKeyMember),
	m_svfitResultsMember(svfitResultsMember),
	m_svfitTausMember(svfitTausMember),
	GetSvfitCacheFileMember(GetSvfitCacheFileMember),
	GetSvfitCacheFileFolderMember(GetSvfitCacheFileFolderMember),
	GetSvfitCacheTreeMember(GetSvfitCacheTreeMember)
{
}

std::string SvfitProducer::GetProducerId() const
{
	return "SvfitProducer";
}

void SvfitProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	
	if (! (settings.*GetSvfitCacheFileMember)().empty())
	{
		svfitTools.Init(
				(settings.*GetSvfitCacheFileMember)(),
				boost::algorithm::to_lower_copy(settings.GetChannel())+"_"+(settings.*GetSvfitCacheFileFolderMember)()+"/"+(settings.*GetSvfitCacheTreeMember)()
		);
	}
	m_svfitCacheMissBehaviour = HttEnumTypes::ToSvfitCacheMissBehaviour(settings.GetSvfitCacheMissBehaviour());
	
	if (m_diTauMassConstraint <= 0.0)
	{
		m_diTauMassConstraint = settings.GetDiTauMassConstraint();
	}
	
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "svfit"+m_name+"Available", [this](event_type const& event, product_type const& product) {
		return ((product.*m_svfitResultsMember).fittedHiggsLV ? true : false);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "svfit"+m_name+"Pt", [this](event_type const& event, product_type const& product) {
		return ((product.*m_svfitResultsMember).fittedHiggsLV ? (product.*m_svfitResultsMember).fittedHiggsLV->Pt() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "svfit"+m_name+"Eta", [this](event_type const& event, product_type const& product) {
		return ((product.*m_svfitResultsMember).fittedHiggsLV ? (product.*m_svfitResultsMember).fittedHiggsLV->Eta() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "svfit"+m_name+"Phi", [this](event_type const& event, product_type const& product) {
		return ((product.*m_svfitResultsMember).fittedHiggsLV ? (product.*m_svfitResultsMember).fittedHiggsLV->Phi() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "svfit"+m_name+"Mass", [this](event_type const& event, product_type const& product) {
		return ((product.*m_svfitResultsMember).fittedHiggsLV ? (product.*m_svfitResultsMember).fittedHiggsLV->mass() : DefaultValues::UndefinedFloat);
	});

	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "svfit"+m_name+"LV", [this](event_type const& event, product_type const& product) {
		return ((product.*m_svfitResultsMember).fittedHiggsLV ? *((product.*m_svfitResultsMember).fittedHiggsLV) : DefaultValues::UndefinedRMFLV);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "svfit"+m_name+"TransverseMass", [this](event_type const& event, product_type const& product) {
		return ((product.*m_svfitResultsMember).fittedTransverseMass ? static_cast<float>((product.*m_svfitResultsMember).fittedTransverseMass) : DefaultValues::UndefinedFloat);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "svfit"+m_name+"Tau1Available", [this](event_type const& event, product_type const& product) {
		return ((product.*m_svfitResultsMember).fittedTau1LV ? true : false);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "svfit"+m_name+"Tau1LV", [this](event_type const& event, product_type const& product) {
		return ((product.*m_svfitResultsMember).fittedTau1LV ? *((product.*m_svfitResultsMember).fittedTau1LV) : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "svfit"+m_name+"Tau1ERatio", [this](event_type const& event, product_type const& product) {
		return (product.*m_svfitResultsMember).fittedTau1ERatio;
	});
	
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "svfit"+m_name+"Tau2Available", [this](event_type const& event, product_type const& product) {
		return ((product.*m_svfitResultsMember).fittedTau2LV ? true : false);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "svfit"+m_name+"Tau2LV", [this](event_type const& event, product_type const& product) {
		return ((product.*m_svfitResultsMember).fittedTau2LV ? *((product.*m_svfitResultsMember).fittedTau2LV) : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "svfit"+m_name+"Tau2ERatio", [this](event_type const& event, product_type const& product) {
		return (product.*m_svfitResultsMember).fittedTau2ERatio;
	});
}

void SvfitProducer::Produce(event_type const& event, product_type& product,
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
	
	// construct inputs
	product.m_svfitInputs.Set(lepton1->p4, lepton2->p4,
	                          product.m_met.p4.Vect(), product.m_met.significance);
	
	// construct event key
	size_t runLumiEvent = 0;
	boost::hash_combine(runLumiEvent, event.m_eventInfo->nRun);
	boost::hash_combine(runLumiEvent, event.m_eventInfo->nLumi);
	boost::hash_combine(runLumiEvent, event.m_eventInfo->nEvent);

	(product.*m_svfitEventKeyMember).Set(runLumiEvent, decayType1, decayType2, decayMode1, decayMode2,
	                                     product.m_systematicShift, product.m_systematicShiftSigma,
	                                     m_diTauMassConstraint, settings.GetSvfitKappaParameter());

	// calculate results
	(product.*m_svfitResultsMember) = svfitTools.GetResults((product.*m_svfitEventKeyMember), product.m_svfitInputs,
	                                                        m_svfitCacheMissBehaviour);
	
	if ((product.*m_svfitResultsMember).fittedTau1LV)
	{
		(product.*m_svfitTausMember)[lepton1] = *((product.*m_svfitResultsMember).fittedTau1LV);
	}
	if ((product.*m_svfitResultsMember).fittedTau2LV)
	{
		(product.*m_svfitTausMember)[lepton2] = *((product.*m_svfitResultsMember).fittedTau2LV);
	}
	
	// apply systematic shifts
	if((product.*m_svfitResultsMember).fittedHiggsLV)
	{
		(product.*m_svfitResultsMember).fittedHiggsLV->SetM((product.*m_svfitResultsMember).fittedHiggsLV->M() * settings.GetSvfitMassShift());
	}
}


SvfitM91Producer::SvfitM91Producer(
) :
	SvfitProducer(
			"M91",
			DefaultValues::ZBosonMassGeV,
			&product_type::m_svfitM91EventKey,
			&product_type::m_svfitM91Results,
			&product_type::m_svfitM91Taus,
			&setting_type::GetSvfitM91CacheFile,
			&setting_type::GetSvfitM91CacheFileFolder,
			&setting_type::GetSvfitM91CacheTree
	)
{
}

std::string SvfitM91Producer::GetProducerId() const
{
	return "SvfitM91Producer";
}


SvfitM125Producer::SvfitM125Producer(
) :
	SvfitProducer(
			"M125",
			125.0,
			&product_type::m_svfitM125EventKey,
			&product_type::m_svfitM125Results,
			&product_type::m_svfitM125Taus,
			&setting_type::GetSvfitM125CacheFile,
			&setting_type::GetSvfitM125CacheFileFolder,
			&setting_type::GetSvfitM125CacheTree
	)
{
}

std::string SvfitM125Producer::GetProducerId() const
{
	return "SvfitM125Producer";
}

