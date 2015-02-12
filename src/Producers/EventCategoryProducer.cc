
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Calculations/Quantities.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/EventCategoryProducer.h"


bool EventCategoryProducer::EventInEventCategory(HttEnumTypes::EventCategory const& eventCategory,
                                                 product_type const& product)
{
	return (std::find(product.m_eventCategories.begin(), product.m_eventCategories.end(), eventCategory) !=
	        product.m_eventCategories.end());
}

void EventCategoryProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("exclusiveEventCategoryIndex", [](event_type const& event, product_type const& product) {
		return Utility::ToUnderlyingValue(product.m_exclusiveEventCategory);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("isCatInc", [](event_type const& event, product_type const& product) -> bool {
		return Utility::Contains(product.m_eventCategories, HttEnumTypes::EventCategory::INCLUSIVE);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("isCat0Jet", [](event_type const& event, product_type const& product) {
		return Utility::Contains(product.m_eventCategories, HttEnumTypes::EventCategory::ZERO_JET);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("isCat1Jet", [](event_type const& event, product_type const& product) {
		return Utility::Contains(product.m_eventCategories, HttEnumTypes::EventCategory::ONE_JET);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("isCat2Jet", [](event_type const& event, product_type const& product) {
		return Utility::Contains(product.m_eventCategories, HttEnumTypes::EventCategory::TWO_JET);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("isCat0JetLow", [](event_type const& event, product_type const& product) {
		return Utility::Contains(product.m_eventCategories, HttEnumTypes::EventCategory::ZERO_JET_LOW_PT);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("isCat0JetMedium", [](event_type const& event, product_type const& product) {
		return Utility::Contains(product.m_eventCategories, HttEnumTypes::EventCategory::ZERO_JET_MEDIUM_PT);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("isCat0JetHigh", [](event_type const& event, product_type const& product) {
		return Utility::Contains(product.m_eventCategories, HttEnumTypes::EventCategory::ZERO_JET_HIGH_PT);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("isCat1JetLow", [](event_type const& event, product_type const& product) {
		return Utility::Contains(product.m_eventCategories, HttEnumTypes::EventCategory::ONE_JET_LOW_PT);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("isCat1JetMedium", [](event_type const& event, product_type const& product) {
		return Utility::Contains(product.m_eventCategories, HttEnumTypes::EventCategory::ONE_JET_MEDIUM_PT);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("isCat1JetHigh", [](event_type const& event, product_type const& product) {
		return Utility::Contains(product.m_eventCategories, HttEnumTypes::EventCategory::ONE_JET_HIGH_PT);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("isCat1JetHighBoost", [](event_type const& event, product_type const& product) {
		return Utility::Contains(product.m_eventCategories, HttEnumTypes::EventCategory::ONE_JET_HIGH_PT_BOOST);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("isCat1JetHighLargeBoost", [](event_type const& event, product_type const& product) {
		return Utility::Contains(product.m_eventCategories, HttEnumTypes::EventCategory::ONE_JET_HIGH_PT_LARGE_BOOST);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("isCat2JetVbf", [](event_type const& event, product_type const& product) {
		return Utility::Contains(product.m_eventCategories, HttEnumTypes::EventCategory::TWO_JET_VBF);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("isCat2JetVbfLoose", [](event_type const& event, product_type const& product) {
		return Utility::Contains(product.m_eventCategories, HttEnumTypes::EventCategory::TWO_JET_VBF_LOOSE);
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("isCat2JetVbfTight", [](event_type const& event, product_type const& product) {
		return Utility::Contains(product.m_eventCategories, HttEnumTypes::EventCategory::TWO_JET_VBF_TIGHT);
	});
}

void EventCategoryProducer::Produce(event_type const& event, product_type& product,
                                    setting_type const& settings) const
{
	assert(product.m_flavourOrderedLeptons.size() >= 2);
	assert((product.m_decayChannel != HttEnumTypes::DecayChannel::EM) || (! product.m_antiTtbarDiscriminators.empty()));
	assert(((product.m_decayChannel != HttEnumTypes::DecayChannel::ET) && (product.m_decayChannel != HttEnumTypes::DecayChannel::MT)) || (product.m_met));
	
	// https://twiki.cern.ch/twiki/pub/CMSPublic/Hig13004TWikiUpdate/categories_2012.png
	// https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingSummer2013#Event_Categories_SM
	
	// inclusive category
	if ((product.m_decayChannel == HttEnumTypes::DecayChannel::ET) ||
		(product.m_decayChannel == HttEnumTypes::DecayChannel::MT))
	{
		if ((Quantities::CalculateMt(product.m_flavourOrderedLeptons[0]->p4, product.m_met->p4) < 30.0) &&
		    (product.m_bTaggedJets.size() == 0))
		{
			product.m_eventCategories.push_back(HttEnumTypes::EventCategory::INCLUSIVE);
		}
	}
	else
	{
		product.m_eventCategories.push_back(HttEnumTypes::EventCategory::INCLUSIVE);
	}
	
	// final categories
	if (Utility::Contains(product.m_eventCategories, HttEnumTypes::EventCategory::INCLUSIVE))
	{
		int nJets30 = KappaProduct::GetNJetsAbovePtThreshold(product.m_validJets, 30.0);
		
		float leptonHighPtCut = 45.0;
		if ((product.m_decayChannel == HttEnumTypes::DecayChannel::EM) ||
		    (product.m_decayChannel == HttEnumTypes::DecayChannel::MM) ||
		    (product.m_decayChannel == HttEnumTypes::DecayChannel::EE))
		{
			leptonHighPtCut = 35.0;
		}
		
		float leptonMediumPtCut = leptonHighPtCut;
		if ((product.m_decayChannel == HttEnumTypes::DecayChannel::ET) ||
		    (product.m_decayChannel == HttEnumTypes::DecayChannel::MT))
		{
			leptonMediumPtCut = 30.0;
		}
		
		int leptonPtCutIndex = 1;
		if ((product.m_decayChannel == HttEnumTypes::DecayChannel::MM) ||
		    (product.m_decayChannel == HttEnumTypes::DecayChannel::EE))
		{
			leptonPtCutIndex = 0;
		}
		
		// 2 Jet/VBF categories
		if ((product.m_decayChannel == HttEnumTypes::DecayChannel::MM) ||
		    (product.m_decayChannel == HttEnumTypes::DecayChannel::EE))
		{
			if ((nJets30 >= 2) &&
			    (! product.m_centralJet30Exists) &&
			    (product.m_validJets[0]->p4.Eta() * product.m_validJets[1]->p4.Eta() < 0.0))
			{
				product.m_eventCategories.push_back(HttEnumTypes::EventCategory::TWO_JET_VBF);
				product.m_eventCategories.push_back(HttEnumTypes::EventCategory::TWO_JET);
			}
		}
		else if ((product.m_decayChannel != HttEnumTypes::DecayChannel::EM) || (product.m_antiTtbarDiscriminators[0] > -0.15))
		{
			if ((nJets30 >= 2) &&
			    (product.m_diJetSystem.mass() > 700.0) &&
			    (std::abs(product.m_validJets[0]->p4.Eta() - product.m_validJets[1]->p4.Eta()) > 4.0) &&
			    (product.m_diLeptonPlusMetSystem.Pt() > 100.0))
			{
				product.m_eventCategories.push_back(HttEnumTypes::EventCategory::TWO_JET_VBF_TIGHT);
				product.m_eventCategories.push_back(HttEnumTypes::EventCategory::TWO_JET_VBF);
				product.m_eventCategories.push_back(HttEnumTypes::EventCategory::TWO_JET);
			}
			else if ((nJets30 >= 2) &&
			         (product.m_diJetSystem.mass() > 500.0) &&
			         (std::abs(product.m_validJets[0]->p4.Eta() - product.m_validJets[1]->p4.Eta()) > 3.5))
			{
				if (product.m_decayChannel != HttEnumTypes::DecayChannel::TT)
				{
					product.m_eventCategories.push_back(HttEnumTypes::EventCategory::TWO_JET_VBF_LOOSE);
					product.m_eventCategories.push_back(HttEnumTypes::EventCategory::TWO_JET_VBF);
					product.m_eventCategories.push_back(HttEnumTypes::EventCategory::TWO_JET);
				}
				else if (product.m_diLeptonPlusMetSystem.Pt() > 100.0)
				{
					product.m_eventCategories.push_back(HttEnumTypes::EventCategory::TWO_JET_VBF);
					product.m_eventCategories.push_back(HttEnumTypes::EventCategory::TWO_JET);
				}
			}
		}
		
		// 1 Jet categories
		if ((! Utility::Contains(product.m_eventCategories, HttEnumTypes::EventCategory::TWO_JET_VBF)) &&
		    ((product.m_decayChannel != HttEnumTypes::DecayChannel::EM) || (product.m_antiTtbarDiscriminators[0] > -0.5)))
		{
			if ((nJets30 >= 1) &&
		        ((product.m_decayChannel != HttEnumTypes::DecayChannel::ET) || (product.m_met->p4.Pt() > 30.0)))
			{
				if (product.m_flavourOrderedLeptons[leptonPtCutIndex]->p4.Pt() > leptonHighPtCut)
				{
					if ((product.m_decayChannel == HttEnumTypes::DecayChannel::TT) &&
					    (product.m_diLeptonPlusMetSystem.Pt() > 170.0))
					{
						product.m_eventCategories.push_back(HttEnumTypes::EventCategory::ONE_JET_HIGH_PT_LARGE_BOOST);
					}
					else if (((product.m_decayChannel == HttEnumTypes::DecayChannel::ET) ||
					          (product.m_decayChannel == HttEnumTypes::DecayChannel::MT) ||
					          (product.m_decayChannel == HttEnumTypes::DecayChannel::TT)) &&
					         (product.m_diLeptonPlusMetSystem.Pt() > 100.0))
					{
						product.m_eventCategories.push_back(HttEnumTypes::EventCategory::ONE_JET_HIGH_PT_BOOST);
					}
					else
					{
						product.m_eventCategories.push_back(HttEnumTypes::EventCategory::ONE_JET_HIGH_PT);
					}
				}
				else if (product.m_flavourOrderedLeptons[leptonPtCutIndex]->p4.Pt() > leptonMediumPtCut)
				{
					product.m_eventCategories.push_back(HttEnumTypes::EventCategory::ONE_JET_MEDIUM_PT);
				}
				else
				{
					product.m_eventCategories.push_back(HttEnumTypes::EventCategory::ONE_JET_LOW_PT);
				}
			
				product.m_eventCategories.push_back(HttEnumTypes::EventCategory::ONE_JET);
			}
		}
		
		// 0 Jet categories
		if ((! Utility::Contains(product.m_eventCategories, HttEnumTypes::EventCategory::ONE_JET)) &&
		    ((product.m_decayChannel != HttEnumTypes::DecayChannel::EM) || (product.m_antiTtbarDiscriminators[0] > -0.5)))
		{
			if (product.m_flavourOrderedLeptons[leptonPtCutIndex]->p4.Pt() > leptonHighPtCut)
			{
				product.m_eventCategories.push_back(HttEnumTypes::EventCategory::ZERO_JET_HIGH_PT);
				product.m_eventCategories.push_back(HttEnumTypes::EventCategory::ZERO_JET);
			}
			else if (product.m_flavourOrderedLeptons[leptonPtCutIndex]->p4.Pt() > leptonMediumPtCut)
			{
				product.m_eventCategories.push_back(HttEnumTypes::EventCategory::ZERO_JET_MEDIUM_PT);
				product.m_eventCategories.push_back(HttEnumTypes::EventCategory::ZERO_JET);
			}
			else
			{
				product.m_eventCategories.push_back(HttEnumTypes::EventCategory::ZERO_JET_LOW_PT);
				product.m_eventCategories.push_back(HttEnumTypes::EventCategory::ZERO_JET);
			}
		}
	}
	
	if (product.m_eventCategories.empty())
	{
		product.m_eventCategories.push_back(HttEnumTypes::EventCategory::NONE);
	}
	
	// exclusive category index is defined as the category with the max. enum value
	product.m_exclusiveEventCategory = *std::max_element(product.m_eventCategories.begin(), product.m_eventCategories.end());
}


void TTHEventCategoryProducer::Produce(event_type const& event, product_type& product,
	                               setting_type const& settings) const
{
	// define exclusive event categories
	product.m_exclusiveEventCategory = HttEnumTypes::EventCategory::NONE;
	
	// 1-tag categories
	if (product.m_bTaggedJets.size() == 1)
	{
		if (product.m_nonBTaggedJets.size() == 2)
		{
			product.m_exclusiveEventCategory = HttEnumTypes::EventCategory::TTH_1TAG_2JETS;
		}
		else if (product.m_nonBTaggedJets.size() == 3)
		{
			product.m_exclusiveEventCategory = HttEnumTypes::EventCategory::TTH_1TAG_3JETS;
		}
		else if (product.m_nonBTaggedJets.size() >= 4)
		{
			product.m_exclusiveEventCategory = HttEnumTypes::EventCategory::TTH_1TAG_4JETS;
		}
	}
	
	// 2-tags categories
	else if (product.m_bTaggedJets.size() == 2)
	{
		if (product.m_nonBTaggedJets.size() == 2)
		{
			product.m_exclusiveEventCategory = HttEnumTypes::EventCategory::TTH_2TAG_2JETS;
		}
		else if (product.m_nonBTaggedJets.size() == 3)
		{
			product.m_exclusiveEventCategory = HttEnumTypes::EventCategory::TTH_2TAG_3JETS;
		}
		else if (product.m_nonBTaggedJets.size() >= 4)
		{
			product.m_exclusiveEventCategory = HttEnumTypes::EventCategory::TTH_2TAG_4JETS;
		}
	}
}
