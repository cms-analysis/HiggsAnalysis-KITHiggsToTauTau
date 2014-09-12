
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
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
	LambdaNtupleConsumer<KappaTypes>::Quantities["exclusiveEventCategoryIndex"] = [](KappaEvent const& event, KappaProduct const& product) {
		return Utility::ToUnderlyingValue((static_cast<HttProduct const&>(product)).m_exclusiveEventCategory);
	};
}

void EventCategoryProducer::Produce(event_type const& event, product_type& product,
	                               setting_type const& settings) const
{
	// https://twiki.cern.ch/twiki/pub/CMSPublic/Hig13004TWikiUpdate/categories_2012.png

	// define exclusive event categories
	product.m_exclusiveEventCategory = HttEnumTypes::EventCategory::NONE;
	
	if (product.m_validJets.size() >= 2)
	{
		if ((product.m_decayChannel == HttEnumTypes::DecayChannel::TT) &&
		    (product.m_diLeptonPlusMetSystem.Pt() > 100.0) &&
		    (product.m_diJetSystem.M() > 500.0) &&
		    (std::abs(product.m_validJets[0]->p4.Eta() - product.m_validJets[1]->p4.Eta()) > 3.5))
		{
			product.m_exclusiveEventCategory = HttEnumTypes::EventCategory::TWO_JET_VBF;
		}
		else if ((product.m_decayChannel == HttEnumTypes::DecayChannel::ET) ||
		         (product.m_decayChannel == HttEnumTypes::DecayChannel::MT) ||
		         (product.m_decayChannel == HttEnumTypes::DecayChannel::EM))
		{
			if ((product.m_diLeptonPlusMetSystem.Pt() > 100.0) &&
			    (product.m_diJetSystem.M() > 700.0) &&
			    (std::abs(product.m_validJets[0]->p4.Eta() - product.m_validJets[1]->p4.Eta()) > 4.0))
			{
				product.m_exclusiveEventCategory = HttEnumTypes::EventCategory::TWO_JET_VBF_TIGHT;
			}
			else if ((product.m_diJetSystem.M() > 500.0) &&
			         (std::abs(product.m_validJets[0]->p4.Eta() - product.m_validJets[1]->p4.Eta()) > 3.5))
			{
				product.m_exclusiveEventCategory = HttEnumTypes::EventCategory::TWO_JET_VBF_LOOSE;
			}
		}
	}
	
	else
	{
		bool isHighPt = false;
		if ((product.m_decayChannel == HttEnumTypes::DecayChannel::ET) ||
		    (product.m_decayChannel == HttEnumTypes::DecayChannel::MT))
		{
			isHighPt = (product.m_flavourOrderedLeptons[1]->p4.Pt() > 45.0);
		}
		else if (product.m_decayChannel == HttEnumTypes::DecayChannel::EM)
		{
			isHighPt = (product.m_flavourOrderedLeptons[1]->p4.Pt() > 35.0);
		}
		else if ((product.m_decayChannel == HttEnumTypes::DecayChannel::EE) ||
		         (product.m_decayChannel == HttEnumTypes::DecayChannel::MM))
		{
			isHighPt = (product.m_ptOrderedLeptons[0]->p4.Pt() > 35.0);
		}
		
		if (product.m_validJets.size() == 1)
		{
			if (product.m_decayChannel == HttEnumTypes::DecayChannel::TT)
			{
				if (product.m_diLeptonPlusMetSystem.Pt() > 170.0)
				{
					product.m_exclusiveEventCategory = HttEnumTypes::EventCategory::ONE_JET_LARGE_BOOST;
				}
				else if (product.m_diLeptonPlusMetSystem.Pt() > 100.0)
				{
					product.m_exclusiveEventCategory = HttEnumTypes::EventCategory::ONE_JET_BOOST;
				}
			}
			else
			{
				float etMetCut = 30.0;
			
				if (isHighPt)
				{
					if (((product.m_decayChannel == HttEnumTypes::DecayChannel::ET) && (product.m_met->p4.Pt() > etMetCut)) ||
					    (product.m_decayChannel == HttEnumTypes::DecayChannel::MT))
					{
						if (product.m_diLeptonPlusMetSystem.Pt() > 100.0)
						{
							product.m_exclusiveEventCategory = HttEnumTypes::EventCategory::ONE_JET_HIGH_PT_BOOST;
						}
						else
						{
							product.m_exclusiveEventCategory = HttEnumTypes::EventCategory::ONE_JET_HIGH_PT;
						}
					}
					else
					{
						product.m_exclusiveEventCategory = HttEnumTypes::EventCategory::ONE_JET_HIGH_PT;
					}
				}
				else if ((product.m_decayChannel != HttEnumTypes::DecayChannel::ET) || (product.m_met->p4.Pt() > etMetCut))
				{
					product.m_exclusiveEventCategory = HttEnumTypes::EventCategory::ONE_JET_LOW_PT;
				}
			}
		}
		
		else
		{
			if (product.m_decayChannel != HttEnumTypes::DecayChannel::TT)
			{
				if (isHighPt)
				{
					product.m_exclusiveEventCategory = HttEnumTypes::EventCategory::ZERO_JET_HIGH_PT;
				}
				else
				{
					product.m_exclusiveEventCategory = HttEnumTypes::EventCategory::ZERO_JET_LOW_PT;
				}
			}
		}
	}
	
	// define non-exclusive event categories
	product.m_eventCategories.clear();
	
	product.m_eventCategories.push_back(product.m_exclusiveEventCategory);
	
	if (product.m_validJets.size() >= 2)
	{
		product.m_eventCategories.push_back(HttEnumTypes::EventCategory::TWO_JET);
	}
	else if (product.m_validJets.size() == 1)
	{
		product.m_eventCategories.push_back(HttEnumTypes::EventCategory::ONE_JET);
	}
	else
	{
		product.m_eventCategories.push_back(HttEnumTypes::EventCategory::ZERO_JET);
	}
	
	if (product.m_exclusiveEventCategory != HttEnumTypes::EventCategory::NONE)
	{
		product.m_eventCategories.push_back(HttEnumTypes::EventCategory::INCLUSIVE);
	}
		
}
