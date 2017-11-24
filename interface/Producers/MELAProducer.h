
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

// https://github.com/cms-analysis/HiggsAnalysis-ZZMatrixElement/tree/v2.1.1/MELA
// https://twiki.cern.ch/twiki/bin/viewauth/CMS/MELAProject
// http://hroskes.web.cern.ch/hroskes/JHUGen/manJHUGenerator.pdf
#include "ZZMatrixElement/MELA/interface/Mela.h"


class MELAProducer: public ProducerBase<HttTypes>
{
public:

	virtual std::string GetProducerId() const override;

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type& product,
						 setting_type const& settings, metadata_type const& metadata) const override;

};

