
#pragma once

#include <TLorentzVector.h>
#include <TVector2.h>
#include <TMatrixD.h>

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/** Producer for the HHKinFit
 *
 *  Required config tags:
 *  - ...
 *
 *  Required packages:
 *  git clone https://github.com/bvormwald/HHKinFit2
 *  cd HHKinFit2
 *  source compile.sh
 *
 *  Documentation:
 *  https://twiki.cern.ch/twiki/bin/viewauth/CMS/HHKinFit2
 */
class HHKinFitProducer: public ProducerBase<HttTypes> {
public:

	virtual std::string GetProducerId() const override;
	
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;

};

