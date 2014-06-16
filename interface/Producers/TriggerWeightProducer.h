
#pragma once

#include "../HttTypes.h"


/** Producer for the Trigger weights using the functions and paramters provided by the Htt group
 *      See: https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingSummer2013#Data_MC_correction_factors
 *
 *  Required config tags:
 *  - TriggerEfficiencyData (vector of ROOT files containing triggerEfficiencies histogram)
 *  - TriggerEfficiencyMc (vector of ROOT files containing triggerEfficiencies histogram)
 */
class TriggerWeightProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "trigger_weight";
	}
	
	virtual void Init(setting_type const& settings) ARTUS_CPP11_OVERRIDE;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const ARTUS_CPP11_OVERRIDE;


private:
	std::map<std::string, std::vector<TH2F*> > triggerEfficienciesDataByHltName;
	std::map<size_t, std::vector<TH2F*> > triggerEfficienciesDataByIndex;
	std::map<std::string, std::vector<TH2F*> > triggerEfficienciesMcByHltName;
	std::map<size_t, std::vector<TH2F*> > triggerEfficienciesMcByIndex;
	
	double GetTriggerEfficienciesFromHistograms(std::vector<TH2F*> const& histograms, KLepton* lepton) const;
	
	std::vector<double> GetTriggerEfficiencies(std::map<std::string, std::vector<TH2F*> > const& triggerEfficienciesByHltName,
		                                       std::map<size_t, std::vector<TH2F*> > const& triggerEfficienciesByIndex,
		                                       event_type const& event, product_type const& product,
	                                           setting_type const& settings) const;

};

