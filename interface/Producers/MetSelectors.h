
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/ProducerBase.h"

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
	typedef typename HttTypes::global_setting_type global_setting_type;
	
	MetSelectorBase(TMet* event_type::*met) :
		ProducerBase<HttTypes>(),
		m_metMember(met)
	{
	}
	
	// nothing to do here
	virtual void ProduceGlobal(event_type const& event, product_type& product,
	                           global_setting_type const& globalSettings) const ARTUS_CPP11_OVERRIDE
	{
		product.m_met = event.*m_metMember;
	}

	// nothing to do here
	virtual void ProduceLocal(event_type const& event, product_type & product, 
	                          setting_type const& pipelineSettings) const ARTUS_CPP11_OVERRIDE
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

