
#pragma once

#include "Artus/KappaAnalysis/interface/Producers/ValidJetsProducer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/**
   \brief Producer for valid jets (simple PF jets).
   
*/
class HttValidJetsProducer: public ValidJetsProducer
{

public:

	typedef KappaEvent event_type;
	typedef KappaProduct product_type;
	typedef KappaSettings setting_type;
	typedef typename HttTypes::event_type spec_event_type;
	typedef typename HttTypes::product_type spec_product_type;
	typedef typename HttTypes::setting_type spec_setting_type;


protected:

	// Htautau specific additional definitions
	virtual bool AdditionalCriteria(KBasicJet* jet, event_type const& event,
	                                product_type& product, setting_type const& settings) const  override;

};



/**
   \brief Producer for valid jets (tagged PF jets).
   
*/
class HttValidTaggedJetsProducer: public ValidTaggedJetsProducer
{

public:

	typedef KappaEvent event_type;
	typedef KappaProduct product_type;
	typedef KappaSettings setting_type;
	typedef typename HttTypes::event_type spec_event_type;
	typedef typename HttTypes::product_type spec_product_type;
	typedef typename HttTypes::setting_type spec_setting_type;


protected:

	// Htautau specific additional definitions
	virtual bool AdditionalCriteria(KJet* jet, event_type const& event,
	                                product_type& product, setting_type const& settings) const  override;

};
