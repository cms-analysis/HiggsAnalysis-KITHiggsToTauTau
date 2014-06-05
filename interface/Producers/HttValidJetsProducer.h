
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
	typedef typename HttTypes::setting_type setting_type;


protected:

	// Htautau specific additional definitions
	virtual bool AdditionalCriteria(KDataPFJet* jet, event_type const& event,
	                                product_type& product, setting_type const& settings) const  ARTUS_CPP11_OVERRIDE;

};



/**
   \brief Producer for valid jets (tagged PF jets).
   
*/
class HttValidTaggedJetsProducer: public ValidTaggedJetsProducer<HttTypes>
{

public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;


protected:

	// Htautau specific additional definitions
	virtual bool AdditionalCriteria(KDataPFTaggedJet* jet, event_type const& event,
	                                product_type& product, setting_type const& settings) const  ARTUS_CPP11_OVERRIDE;

};
