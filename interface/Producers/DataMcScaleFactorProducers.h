
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/** Abstract producer for scale factors effData/effMC
 */
class DataMcScaleFactorProducerBase: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	DataMcScaleFactorProducerBase(std::vector<std::string>& (setting_type::*GetEfficiencyData)(void) const,
	                              std::vector<std::string>& (setting_type::*GetEfficiencyMc)(void) const,
	                              std::string (setting_type::*GetEfficiencyHistogram)(void) const,
	                              std::string const& weightName);
	
	virtual void Init(setting_type const& settings) override;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const override;


private:
	std::vector<std::string>& (setting_type::*GetEfficiencyData)(void) const;
	std::vector<std::string>& (setting_type::*GetEfficiencyMc)(void) const;
	std::string (setting_type::*GetEfficiencyHistogram)(void) const;
	std::string m_weightName;
	
	std::map<std::string, std::vector<TH2F*> > efficienciesDataByHltName;
	std::map<size_t, std::vector<TH2F*> > efficienciesDataByIndex;
	std::map<std::string, std::vector<TH2F*> > efficienciesMcByHltName;
	std::map<size_t, std::vector<TH2F*> > efficienciesMcByIndex;
	
	double GetEfficienciesFromHistograms(std::vector<TH2F*> const& histograms, KLepton* lepton) const;
	
	std::vector<double> GetEfficiencies(std::map<std::string, std::vector<TH2F*> > const& efficienciesByHltName,
		                                std::map<size_t, std::vector<TH2F*> > const& efficienciesByIndex,
		                                event_type const& event, product_type const& product,
	                                    setting_type const& settings) const;

};


/** Producer for the Trigger weights using the functions and paramters provided by the Htt group
 *      See: https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingSummer2013#Data_MC_correction_factors
 *
 *  Required config tags:
 *  - TriggerEfficiencyData (vector of ROOT files containing triggerEfficiencies histogram)
 *  - TriggerEfficiencyMc (vector of ROOT files containing triggerEfficiencies histogram)
 *  - TriggerEfficiencyHistogram (default: triggerEfficiencies)
 */
class TriggerWeightProducer: public DataMcScaleFactorProducerBase {
public:

	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetProducerId() const override {
		return "TriggerWeightProducer";
	}
	
	TriggerWeightProducer();
	
};


/** Producer for the identification weights using the functions and paramters provided by the Htt group
 *
 *  Required config tags:
 *  - IdentificationEfficiencyData (vector of ROOT files containing identificationEfficiencies histogram)
 *  - IdentificationEfficiencyMc (vector of ROOT files containing identificationEfficiencies histogram)
 *  - IdentificationEfficiencyHistogram (default: identificationEfficiencies)
 */
class IdentificationWeightProducer: public DataMcScaleFactorProducerBase {
public:

	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetProducerId() const override {
		return "IdentificationWeightProducer";
	}
	
	IdentificationWeightProducer();
	
};

