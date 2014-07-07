
#pragma once

#include "../HttTypes.h"


/** Producer for 
 *
 *  Required config tags:
 *  - TauTauRestFrameReco
 *
 *  Required packages:
 *  git clone https://github.com:veelken/SVfit_standalone.git TauAnalysis/SVfitStandalone
 *
 *  Old version:
 *  http://cms-sw.github.io/faq.html#how-do-i-access-the-old-cvs-repository-to-check-what-was-really-there
 *  cvs co -r V00-02-03s TauAnalysis/CandidateTools
 *  https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingSummer2013#Di_Tau_Mass_Reconstruction
 */
class SvfitProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	static SvfitTools svfitTools;
	
	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "svfit";
	}
	
	virtual void Init(setting_type const& settings) ARTUS_CPP11_OVERRIDE;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const ARTUS_CPP11_OVERRIDE;

};

