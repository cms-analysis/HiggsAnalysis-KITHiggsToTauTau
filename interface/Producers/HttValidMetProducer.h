
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/ProducerBase.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

/**
   \brief Producer for the MET
*/


template<class TMet>
class HttValidMetProducerBase: public ProducerBase<HttTypes>
{
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	typedef typename HttTypes::global_setting_type global_setting_type;
	
	HttValidMetProducerBase(TMet* event_type::*met) :
		ProducerBase<HttTypes>(),
		m_metMember(met)
	{
	}
	
	virtual void InitGlobal(global_setting_type const& globalSettings)  ARTUS_CPP11_OVERRIDE
	{
		ProducerBase<HttTypes>::InitGlobal(globalSettings);
	}
	
	virtual void InitLocal(setting_type const& settings)  ARTUS_CPP11_OVERRIDE
	{
		ProducerBase<HttTypes>::InitLocal(settings);
	}
	
	// nothing to do here
	virtual void ProduceGlobal(event_type const& event, product_type& product,
	                           global_setting_type const& globalSettings) const ARTUS_CPP11_OVERRIDE
	{
	}

	// nothing to do here
	virtual void ProduceLocal(event_type const& event, product_type & product, 
	                          setting_type const& pipelineSettings) const ARTUS_CPP11_OVERRIDE
	{
	}

private:
	TMet* event_type::*m_metMember;
};



/**
   \brief Producer for MVAMET (TT channel)
*/
class HttValidMvaMetTTProducer: public HttValidMetProducerBase<KDataPFMET>
{
public:
	HttValidMvaMetTTProducer() : HttValidMetProducerBase<KDataPFMET>(&HttTypes::event_type::m_mvaMetTT) {};
	
	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "valid_mvamet_tt";
	}
};



/**
   \brief Producer for MVAMET (MT channel)
*/
class HttValidMvaMetMTProducer: public HttValidMetProducerBase<KDataPFMET>
{
public:
	HttValidMvaMetMTProducer() : HttValidMetProducerBase<KDataPFMET>(&HttTypes::event_type::m_mvaMetMT) {};
	
	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "valid_mvamet_mt";
	}
};



/**
   \brief Producer for MVAMET (ET channel)
*/
class HttValidMvaMetETProducer: public HttValidMetProducerBase<KDataPFMET>
{
public:
	HttValidMvaMetETProducer() : HttValidMetProducerBase<KDataPFMET>(&HttTypes::event_type::m_mvaMetET) {};
	
	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "valid_mvamet_et";
	}
};



/**
   \brief Producer for MVAMET (EM channel)
*/
class HttValidMvaMetEMProducer: public HttValidMetProducerBase<KDataPFMET>
{
public:
	HttValidMvaMetEMProducer() : HttValidMetProducerBase<KDataPFMET>(&HttTypes::event_type::m_mvaMetEM) {};
	
	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "valid_mvamet_em";
	}
};
