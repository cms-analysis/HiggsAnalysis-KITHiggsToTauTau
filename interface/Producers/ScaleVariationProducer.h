
#pragma once

#include <TH2.h>
#include "Artus/Core/interface/ProducerBase.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include <boost/regex.hpp>

/**
   \brief ScaleVariationsProducer

   See https://indico.cern.ch/event/494682/contributions/1172505/attachments/1223578/1800218/mcaod-Feb15-2016.pdf for the motivation. This Producer copies event-by-event renormalization and factorization weights from the Kappa input file to the output. This can be used to calculate the migration of signal events between channels and categories.

*/

class ScaleVariationProducer: public ProducerBase<HttTypes> {
public:

	std::string GetProducerId() const;

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void OnLumi(event_type const& event,
	                    setting_type const& settings, metadata_type const& metadata) override;

	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings, metadata_type const& metadata) const override;

private:
	std::map<std::string, std::vector<std::string> > genEventInfoMetadataMap;
	std::vector<std::string> weightNames;

};
