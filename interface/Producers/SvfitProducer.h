
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/SvfitTools.h"


/** Producer for SVfit
 *
 *  Required config tags:
 *  - SvfitIntegrationMethod (possible values: markovchain, vegas)
 *  - GetSvfitCacheFile (need to be implemented as global setting, default: empty)
 *  - GetSvfitCacheTree (need to be implemented as global setting, default: svfitCache)
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
		return "SvfitProducer";
	}
	
	virtual void Init(setting_type const& settings) ARTUS_CPP11_OVERRIDE;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const ARTUS_CPP11_OVERRIDE;


private:
	SvfitEventKey::IntegrationMethod integrationMethod;
};

