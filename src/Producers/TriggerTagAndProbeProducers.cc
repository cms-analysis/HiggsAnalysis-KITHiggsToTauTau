
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TriggerTagAndProbeProducers.h"


LeptonTriggerTagAndProbeProducer::LeptonTriggerTagAndProbeProducer() :
	TriggerTagAndProbeProducerBase<KLepton>(
			&HttTypes::product_type::m_ptOrderedLeptons,
			&HttTypes::product_type::m_detailedTriggerMatchedLeptons,
			&HttTypes::setting_type::GetTagLeptonHltPaths,
			&HttTypes::setting_type::GetProbeLeptonHltPaths,
			//&HttTypes::setting_type::GetTagLeptonTriggerFilterNames,
			//&HttTypes::setting_type::GetProbeLeptonTriggerFilterNames,
			&HttTypes::product_type::m_triggerTagLeptonAvailable,
			&HttTypes::product_type::m_triggerProbeLeptonAvailable,
			&HttTypes::product_type::m_triggerTagLepton,
			&HttTypes::product_type::m_triggerProbeLepton
	)
{
}

std::string LeptonTriggerTagAndProbeProducer::GetProducerId() const
{
	return "LeptonTriggerTagAndProbeProducer";
}

void LeptonTriggerTagAndProbeProducer::Init(setting_type const& settings)
{
	TriggerTagAndProbeProducerBase<KLepton>::Init(settings);
	
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("triggerTagLeptonAvailable", [](event_type const& event, product_type const& product)
	{
		return product.m_triggerTagLeptonAvailable;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("triggerTagLeptonPt", [](event_type const& event, product_type const& product)
	{
		return (product.m_triggerTagLeptonAvailable ? product.m_triggerTagLepton->p4.Pt() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("triggerTagLeptonEta", [](event_type const& event, product_type const& product)
	{
		return (product.m_triggerTagLeptonAvailable ? product.m_triggerTagLepton->p4.Eta() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("triggerTagLeptonPhi", [](event_type const& event, product_type const& product)
	{
		return (product.m_triggerTagLeptonAvailable ? product.m_triggerTagLepton->p4.Phi() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("triggerTagLeptonMass", [](event_type const& event, product_type const& product)
	{
		return (product.m_triggerTagLeptonAvailable ? product.m_triggerTagLepton->p4.mass() : DefaultValues::UndefinedFloat);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("triggerProbeLeptonAvailable", [](event_type const& event, product_type const& product)
	{
		return product.m_triggerProbeLeptonAvailable;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("triggerProbeLeptonPt", [](event_type const& event, product_type const& product)
	{
		return (product.m_triggerProbeLeptonAvailable ? product.m_triggerProbeLepton->p4.Pt() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("triggerProbeLeptonEta", [](event_type const& event, product_type const& product)
	{
		return (product.m_triggerProbeLeptonAvailable ? product.m_triggerProbeLepton->p4.Eta() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("triggerProbeLeptonPhi", [](event_type const& event, product_type const& product)
	{
		return (product.m_triggerProbeLeptonAvailable ? product.m_triggerProbeLepton->p4.Phi() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("triggerProbeLeptonMass", [](event_type const& event, product_type const& product)
	{
		return (product.m_triggerProbeLeptonAvailable ? product.m_triggerProbeLepton->p4.mass() : DefaultValues::UndefinedFloat);
	});
}
