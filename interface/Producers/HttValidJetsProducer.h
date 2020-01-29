
#pragma once

#include "Artus/KappaAnalysis/interface/Producers/ValidJetsProducer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/**
   \brief Producer for valid jets (simple PF jets).
   
*/
class HttValidJetsProducer: public ValidJetsProducer
{

public:

	typedef typename KappaTypes::event_type event_type;
	typedef typename KappaTypes::product_type product_type;
	typedef typename KappaTypes::setting_type setting_type;
	typedef typename KappaTypes::metadata_type metadata_type;
	typedef typename HttTypes::event_type spec_event_type;
	typedef typename HttTypes::product_type spec_product_type;
	typedef typename HttTypes::setting_type spec_setting_type;
	typedef typename HttTypes::metadata_type spec_metadata_type;

	static bool AdditionalCriteriaStatic(KBasicJet* jet, event_type const& event, product_type& product,
	                                     setting_type const& settings, metadata_type const& metadata);

protected:

	// Htautau specific additional definitions
	virtual bool AdditionalCriteria(KBasicJet* jet, event_type const& event, product_type& product,
	                                setting_type const& settings, metadata_type const& metadata) const override;

};



/**
   \brief Producer for valid jets (tagged PF jets).
   
*/
class HttValidTaggedJetsProducer: public ValidTaggedJetsProducer
{

public:

	typedef typename KappaTypes::event_type event_type;
	typedef typename KappaTypes::product_type product_type;
	typedef typename KappaTypes::setting_type setting_type;
	typedef typename KappaTypes::metadata_type metadata_type;
	typedef typename HttTypes::event_type spec_event_type;
	typedef typename HttTypes::product_type spec_product_type;
	typedef typename HttTypes::setting_type spec_setting_type;
	typedef typename HttTypes::metadata_type spec_metadata_type;

	static bool AdditionalCriteriaStatic(KJet* jet,
	                                     std::map<size_t, std::vector<std::string> > const& puJetIdsByIndex,
	                                     std::map<std::string, std::vector<std::string> > const& puJetIdsByHltName,
	                                     std::map<std::string, std::vector<float> > const& jetTaggerLowerCutsByTaggerName,
	                                     std::map<std::string, std::vector<float> > const& jetTaggerUpperCutsByTaggerName,
	                                     std::string const& jetPuJetIDName,
	                                     KappaEnumTypes::JetID const& pujetID,
	                                     KappaEnumTypes::JetIDVersion const& pujetIDVersion,
	                                     event_type const& event, product_type& product,
	                                     setting_type const& settings, metadata_type const& metadata);

protected:

	// Htautau specific additional definitions
	virtual bool AdditionalCriteria(KJet* jet, event_type const& event, product_type& product,
	                                setting_type const& settings, metadata_type const& metadata) const override;

};
