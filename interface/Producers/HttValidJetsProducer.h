
#pragma once

#include "Artus/KappaAnalysis/interface/Producers/ValidJetsProducer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/**
   \brief Producer for valid jets (simple PF jets).
   
*/
class HttValidJetsProducer: public ValidJetsProducer<HttTypes>
{

public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::global_setting_type global_setting_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual void InitGlobal(global_setting_type const& globalSettings)  ARTUS_CPP11_OVERRIDE
	{
		ValidJetsProducer::InitGlobal(globalSettings);
	}
	
	virtual void InitLocal(setting_type const& settings)  ARTUS_CPP11_OVERRIDE
	{
		ValidJetsProducer::InitLocal(settings);
	}

protected:

	// Htautau specific additional definitions
	virtual bool AdditionalCriteria(KDataPFJet* jet, event_type const& event,
	                                product_type& product) const  ARTUS_CPP11_OVERRIDE;

// private:
// 	HttProduct::DecayChannel decayChannel;
};



/**
   \brief Producer for valid jets (tagged PF jets).
   
*/
class HttValidTaggedJetsProducer: public ValidTaggedJetsProducer<HttTypes>
{

public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::global_setting_type global_setting_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual void InitGlobal(global_setting_type const& globalSettings)  ARTUS_CPP11_OVERRIDE
	{
		ValidTaggedJetsProducer::InitGlobal(globalSettings);
	}
	
	virtual void InitLocal(setting_type const& settings)  ARTUS_CPP11_OVERRIDE
	{
		ValidTaggedJetsProducer::InitLocal(settings);
	}

protected:

	// Htautau specific additional definitions
	virtual bool AdditionalCriteria(KDataPFTaggedJet* jet, event_type const& event,
	                                product_type& product) const  ARTUS_CPP11_OVERRIDE;

// private:
// 	HttProduct::DecayChannel decayChannel;
};
