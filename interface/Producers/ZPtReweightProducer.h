
#pragma once

#include "Artus/Core/interface/ProducerBase.h"
#include "RooWorkspace.h"
#include "RooFunctor.h"
#include "TSystem.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include <boost/regex.hpp>

/**
   \brief ZPtReweightProducer
   Config tags:
   - Fill me with something meaningful

*/

class ZPtReweightProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	

	std::string GetProducerId() const;

	virtual void Init(setting_type const& settings) override;

	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings) const override;
private:
	RooFunctor* m_ZptWeightFunktor;
	std::map<std::string,RooFunctor*> m_ZptWeightUncertaintiesFunktor;
	RooWorkspace *m_workspace;
	bool m_applyReweighting;
};
