
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/**
   Producer that modifies the event.m_electrons[..].p4.Eta()
   according to the Htt specifications to electron->superclusterposition.Eta()
   See: https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingSummer2013#Electron_ID
   
   It is recommendet to always run this producer globally and before any use of event.m_electrons.
*/
class ElectronEtaSelector: public ProducerBase<HttTypes>
{

public:

	virtual std::string GetProducerId() const override {
		return "ElectronEtaSelector";
	}

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;

};

