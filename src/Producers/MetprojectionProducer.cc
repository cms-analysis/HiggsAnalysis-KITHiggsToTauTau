
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MetprojectionProducer.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "TVector2.h"

void MetprojectionProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);


	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("metProjectionPar", [](event_type const& event, product_type const& product) {
		return product.m_metProjection.X();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("metProjectionPerp", [](event_type const& event, product_type const& product) {
		return product.m_metProjection.Y();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("metProjectionPhi", [](event_type const& event, product_type const& product) {
		return TVector2::Phi_mpi_pi(product.m_metProjection.Phi());
	});
}

void MetprojectionProducer::Produce(event_type const& event, product_type& product, setting_type const& settings) const
{
	assert(product.m_svfitResults.momentum);
	assert(product.m_met);

	//RMFLV::BetaVector proj, metP3;
	//proj.SetXYZ(product.m_svfitResults.momentum->X() - product.m_diLeptonSystem.X(),product.m_svfitResults.momentum->Y() - product.m_diLeptonSystem.Y(),product.m_svfitResults.momentum->Z() - product.m_diLeptonSystem.Z());
	
	//metP3.SetXYZ(product.m_met->p4.Vect().X(),product.m_met->p4.Vect().Y(),product.m_met->p4.Vect().Z());
	//product.m_metProjection = sqrt(metP3.Mag2())*sin(acos(metP3.Dot(proj)/sqrt(metP3.Mag2()*proj.Mag2())));



	TVector2 svFitMomentum(product.m_svfitResults.momentum->X(), product.m_svfitResults.momentum->Y());
	TVector2 diLeptonMomentum(product.m_diLeptonSystem.x(), product.m_diLeptonSystem.Y());
	TVector2 met(product.m_met->p4.Vect().X(), product.m_met->p4.Vect().Y());

	TVector2 neutrinoMomentum = svFitMomentum - diLeptonMomentum;

	product.m_metProjection = met.Rotate(- neutrinoMomentum.Phi());
}
