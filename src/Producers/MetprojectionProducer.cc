
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MetprojectionProducer.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"

void MetprojectionProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);


	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("metProjection", [](event_type const& event, product_type const& product) {
		return product.m_metProjection;
	});
}

void MetprojectionProducer::Produce(event_type const& event, product_type& product, setting_type const& settings) const
{
	assert(product.m_svfitResults.momentum);
	assert(product.m_met);

	RMFLV::BetaVector proj, metP3;
	proj.SetXYZ(product.m_svfitResults.momentum->X() - product.m_diLeptonSystem.X(),product.m_svfitResults.momentum->Y() - product.m_diLeptonSystem.Y(),product.m_svfitResults.momentum->Z() - product.m_diLeptonSystem.Z());
	
	metP3.SetXYZ(product.m_met->p4.Vect().X(),product.m_met->p4.Vect().Y(),product.m_met->p4.Vect().Z());
	product.m_metProjection = sqrt(metP3.Mag2())*sin(acos(metP3.Dot(proj)/sqrt(metP3.Mag2()*proj.Mag2())));
}
