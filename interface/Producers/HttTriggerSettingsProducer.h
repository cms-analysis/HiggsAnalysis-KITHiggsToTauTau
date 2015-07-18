
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"


/** Producer to overwrite settings for triggers (e.g. run-dependent settings)
 *  Config tags:
 *  - Channel
 *  - ElectronTriggerFilterNames
 *  - MuonTriggerFilterNames
 *  - TauTriggerFilterNames
 *  - JetTriggerFilterNames
 */
class HttTriggerSettingsProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	HttTriggerSettingsProducer();
	
	virtual std::string GetProducerId() const override;
	
	virtual void Init(setting_type const& settings) override;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const override;

private:
	HttEnumTypes::DecayChannel m_decayChannel;
	
	std::map<size_t, std::vector<std::string> > m_electronTriggerFiltersByIndex;
	std::map<size_t, std::vector<std::string> > m_muonTriggerFiltersByIndex;
	std::map<size_t, std::vector<std::string> > m_tauTriggerFiltersByIndex;
	std::map<size_t, std::vector<std::string> > m_jetTriggerFiltersByIndex;
	
	std::map<std::string, std::vector<std::string> > m_electronTriggerFiltersByHltName;
	std::map<std::string, std::vector<std::string> > m_muonTriggerFiltersByHltName;
	std::map<std::string, std::vector<std::string> > m_tauTriggerFiltersByHltName;
	std::map<std::string, std::vector<std::string> > m_jetTriggerFiltersByHltName;
};

