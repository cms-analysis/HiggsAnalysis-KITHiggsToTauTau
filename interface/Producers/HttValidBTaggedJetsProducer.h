
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidJetsProducer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/**
   \brief Producer for valid b-tagged jets.

   Inherits from the HttValidTaggedJetsProducer class, adding further requirements
   which exploits the properties of b-tagged jets
*/
class HttValidBTaggedJetsProducer: public HttValidTaggedJetsProducer
{

public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::global_setting_type global_setting_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual void InitGlobal(global_setting_type const& globalSettings)  ARTUS_CPP11_OVERRIDE;
	virtual void InitLocal(setting_type const& settings)  ARTUS_CPP11_OVERRIDE;

	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "valid_btagged_jets";
	}

protected:

	// function that lets this producer work as both a global and a local producer
	virtual void Produce(event_type const& event, product_type& product) const ARTUS_CPP11_OVERRIDE;

	// Htautau specific additional definitions
	virtual bool AdditionalCriteria(KDataPFTaggedJet* jet, event_type const& event,
	                                product_type& product) const  ARTUS_CPP11_OVERRIDE;

private:

	float combinedSecondaryVertexMediumWP = 0.0;
	float absEtaCut = 0.0;
};
