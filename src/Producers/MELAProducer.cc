
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MELAProducer.h"

// https://github.com/cms-analysis/HiggsAnalysis-ZZMatrixElement
// https://twiki.cern.ch/twiki/bin/viewauth/CMS/MELAProject
#include "ZZMatrixElement/MELA/interface/Mela.h"


std::string MELAProducer::GetProducerId() const
{
	return "MELAProducer";
}

void MELAProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
}


void MELAProducer::Produce(event_type const& event, product_type& product,
                           setting_type const& settings, metadata_type const& metadata) const
{

}

