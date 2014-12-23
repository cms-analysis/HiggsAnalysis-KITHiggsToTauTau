
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/ProducerBase.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

/**
   \brief Producer for the MET
*/


template<class TMet>
class MetSelectorBase: public ProducerBase<HttTypes>
{
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	MetSelectorBase(TMet* event_type::*met) :
		ProducerBase<HttTypes>(),
		m_metMember(met)
	{
	}

	virtual void Init(setting_type const& settings) ARTUS_CPP11_OVERRIDE
	{
		ProducerBase<HttTypes>::Init(settings);
		
		// add possible quantities for the lambda ntuples consumers
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetSumEt", [](KappaEvent const& event, KappaProduct const& product)
		{
			return event.m_met->sumEt;
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetPt", [](KappaEvent const& event, KappaProduct const& product)
		{
			return event.m_met->p4.Pt();
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetPhi", [](KappaEvent const& event, KappaProduct const& product)
		{
			return event.m_met->p4.Phi();
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetCov00", [](KappaEvent const& event, KappaProduct const& product)
		{
			return event.m_met->significance.At(0, 0);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetCov01", [](KappaEvent const& event, KappaProduct const& product)
		{
			return event.m_met->significance.At(0, 1);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetCov10", [](KappaEvent const& event, KappaProduct const& product)
		{
			return event.m_met->significance.At(1, 0);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pfMetCov11", [](KappaEvent const& event, KappaProduct const& product)
		{
			return event.m_met->significance.At(1, 1);
		});
	
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvaMetSumEt", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met->sumEt;
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvaMetPt", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met->p4.Pt();
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvaMetPhi", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met->p4.Phi();
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvaMetCov00", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met->significance.At(0, 0);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvaMetCov01", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met->significance.At(0, 1);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvaMetCov10", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met->significance.At(1, 0);
		});
		LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvaMetCov11", [](KappaEvent const& event, KappaProduct const& product)
		{
			return (static_cast<HttProduct const&>(product)).m_met->significance.At(1, 1);
		});
	}
	
	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings) const ARTUS_CPP11_OVERRIDE
	{
		assert((event.*m_metMember));
		
		product.m_met = (event.*m_metMember);
	}

private:
	TMet* event_type::*m_metMember;
};



/**
   \brief Producer for MET (from event.m_met)
*/
class MetSelector: public MetSelectorBase<KDataPFMET>
{
public:
	MetSelector() : MetSelectorBase<KDataPFMET>(&HttTypes::event_type::m_met) {};
	
	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "MetSelector";
	}
};



/**
   \brief Producer for MVAMET (TT channel)
*/
class MvaMetTTSelector: public MetSelectorBase<KDataPFMET>
{
public:
	MvaMetTTSelector() : MetSelectorBase<KDataPFMET>(&HttTypes::event_type::m_mvaMetTT) {};
	
	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "MvaMetTTSelector";
	}
};



/**
   \brief Producer for MVAMET (MT channel)
*/
class MvaMetMTSelector: public MetSelectorBase<KDataPFMET>
{
public:
	MvaMetMTSelector() : MetSelectorBase<KDataPFMET>(&HttTypes::event_type::m_mvaMetMT) {};
	
	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "MvaMetMTSelector";
	}
};



/**
   \brief Producer for MVAMET (ET channel)
*/
class MvaMetETSelector: public MetSelectorBase<KDataPFMET>
{
public:
	MvaMetETSelector() : MetSelectorBase<KDataPFMET>(&HttTypes::event_type::m_mvaMetET) {};
	
	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "MvaMetETSelector";
	}
};



/**
   \brief Producer for MVAMET (EM channel)
*/
class MvaMetEMSelector: public MetSelectorBase<KDataPFMET>
{
public:
	MvaMetEMSelector() : MetSelectorBase<KDataPFMET>(&HttTypes::event_type::m_mvaMetEM) {};
	
	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "MvaMetEMSelector";
	}
};

