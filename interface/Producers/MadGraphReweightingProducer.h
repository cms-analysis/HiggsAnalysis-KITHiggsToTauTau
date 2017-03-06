
#pragma once

#include <Python.h>

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


class MadGraphReweightingProducer: public ProducerBase<HttTypes>
{
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	virtual ~MadGraphReweightingProducer();
	
	virtual std::string GetProducerId() const override;

	virtual void Init(setting_type const& settings) override;

	virtual void Produce(event_type const& event, product_type& product,
						 setting_type const& settings) const override;


private:
	std::string GetLabelForWeightsMap(float mixingAngleOverPiHalf) const;
	
	std::vector<float> mixingAnglesOverPiHalf;
	
	PyObject *m_functionMadGraphWeightGGH = nullptr;
	bool m_initialised = false;
};

