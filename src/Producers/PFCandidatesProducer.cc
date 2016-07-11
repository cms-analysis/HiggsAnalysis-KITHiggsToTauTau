
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/PFCandidatesProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/Quantities.h"

void PFCandidatesProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);


	LambdaNtupleConsumer<HttTypes>::AddVFloatQuantity("Pts", [](event_type const& event, product_type const& product)
	{
		std::vector<float> Pts;
		for(unsigned int i = 0; i < event.m_packedPFCandidates->size();i++)
		{
			Pts.push_back(event.m_packedPFCandidates->at(i).p4.Pt());//or .p4.fCoordinates.fPt()?
		}
		return Pts;
	});


}




void PFCandidatesProducer::Produce(event_type const& event, product_type& product,
	                                     setting_type const& settings) const
{


}
