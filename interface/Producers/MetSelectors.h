
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/ProducerBase.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

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
		LambdaNtupleConsumer<HttTypes>::Quantities["pfMetSumEt"] = [](event_type const& event, product_type const& product)
		{
			return event.m_met->sumEt;
		};
		LambdaNtupleConsumer<HttTypes>::Quantities["pfMetPt"] = [](event_type const& event, product_type const& product)
		{
			return event.m_met->p4.Pt();
		};
		LambdaNtupleConsumer<HttTypes>::Quantities["pfMetPhi"] = [](event_type const& event, product_type const& product)
		{
			return event.m_met->p4.Phi();
		};
		LambdaNtupleConsumer<HttTypes>::Quantities["pfMetCov00"] = [](event_type const& event, product_type const& product)
		{
			return event.m_met->significance.At(0, 0);
		};
		LambdaNtupleConsumer<HttTypes>::Quantities["pfMetCov01"] = [](event_type const& event, product_type const& product)
		{
			return event.m_met->significance.At(0, 1);
		};
		LambdaNtupleConsumer<HttTypes>::Quantities["pfMetCov10"] = [](event_type const& event, product_type const& product)
		{
			return event.m_met->significance.At(1, 0);
		};
		LambdaNtupleConsumer<HttTypes>::Quantities["pfMetCov11"] = [](event_type const& event, product_type const& product)
		{
			return event.m_met->significance.At(1, 1);
		};
	
		LambdaNtupleConsumer<HttTypes>::Quantities["mvaMetSumEt"] = [](event_type const& event, product_type const& product)
		{
			return product.m_met->sumEt;
		};
		LambdaNtupleConsumer<HttTypes>::Quantities["mvaMetPt"] = [](event_type const& event, product_type const& product)
		{
			return product.m_met->p4.Pt();
		};
		LambdaNtupleConsumer<HttTypes>::Quantities["mvaMetPhi"] = [](event_type const& event, product_type const& product)
		{
			return product.m_met->p4.Phi();
		};
		LambdaNtupleConsumer<HttTypes>::Quantities["mvaMetCov00"] = [](event_type const& event, product_type const& product)
		{
			return product.m_met->significance.At(0, 0);
		};
		LambdaNtupleConsumer<HttTypes>::Quantities["mvaMetCov01"] = [](event_type const& event, product_type const& product)
		{
			return product.m_met->significance.At(0, 1);
		};
		LambdaNtupleConsumer<HttTypes>::Quantities["mvaMetCov10"] = [](event_type const& event, product_type const& product)
		{
			return product.m_met->significance.At(1, 0);
		};
		LambdaNtupleConsumer<HttTypes>::Quantities["mvaMetCov11"] = [](event_type const& event, product_type const& product)
		{
			return product.m_met->significance.At(1, 1);
		};
	}
	
	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings) const ARTUS_CPP11_OVERRIDE
	{
		product.m_met = event.*m_metMember;
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
		return "met_selector";
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
		return "mvamet_tt_selector";
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
		return "mvamet_mt_selector";
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
		return "mvamet_et_selector";
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
		return "mvamet_em_selector";
	}
};

