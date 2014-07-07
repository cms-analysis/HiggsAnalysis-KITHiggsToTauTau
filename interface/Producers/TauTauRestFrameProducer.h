
#pragma once

#include <unordered_map>

#include <TFile.h>
#include <TTree.h>

#include "Kappa/DataFormats/interface/Kappa.h"

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
class TauTauRestFrameProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	static SvfitTools svfitTools;
	
	enum class TauTauRestFrameReco : int
	{
		NONE  = -1,
		VISIBLE_LEPTONS = 0,
		VISIBLE_LEPTONS_MET = 1,
		COLLINEAR_APPROXIMATION  = 2,
		SVFIT  = 3,
	};
	static TauTauRestFrameReco ToTauTauRestFrameReco(std::string const& tauTauRestFrameReco)
	{
		if (tauTauRestFrameReco == "visible_leptons") return TauTauRestFrameReco::VISIBLE_LEPTONS;
		else if (tauTauRestFrameReco == "visible_leptons_met") return TauTauRestFrameReco::VISIBLE_LEPTONS_MET;
		else if (tauTauRestFrameReco == "collinear_approximation") return TauTauRestFrameReco::COLLINEAR_APPROXIMATION;
		else if (tauTauRestFrameReco == "svfit") return TauTauRestFrameReco::SVFIT;
		else return TauTauRestFrameReco::NONE;
	}
	
	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "tautau_restframe";
	}
	
	~TauTauRestFrameProducer();
	
	virtual void Init(setting_type const& settings) ARTUS_CPP11_OVERRIDE;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const ARTUS_CPP11_OVERRIDE;


private:
	TauTauRestFrameReco tauTauRestFrameReco;

	std::vector<RMDataLV> ProduceVisibleLeptonsRestFrame(event_type const& event,
	                                                     product_type& product,
	                                                     setting_type const& settings) const;
	
	std::vector<RMDataLV> ProduceVisibleLeptonsMetRestFrame(event_type const& event,
	                                                        product_type& product,
	                                                        setting_type const& settings) const;
	
	std::vector<RMDataLV> ProduceCollinearApproximationRestFrame(event_type const& event,
	                                                             product_type& product,
	                                                             setting_type const& settings) const;
	
	std::vector<RMDataLV> ProduceSvfitRestFrame(event_type const& event,
	                                            product_type& product,
	                                            setting_type const& settings) const;

};

