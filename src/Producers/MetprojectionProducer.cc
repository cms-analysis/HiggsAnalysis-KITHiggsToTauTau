
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MetprojectionProducer.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "TVector2.h"

void MetprojectionProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);


	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoNeutrinoOnRecoMetProjectionPar", [](event_type const& event, product_type const& product) {
		return product.m_recoNeutrinoOnRecoMetProjection.X();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoNeutrinoOnRecoMetProjectionPerp", [](event_type const& event, product_type const& product) {
		return product.m_recoNeutrinoOnRecoMetProjection.Y();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoNeutrinoOnRecoMetProjectionPhi", [](event_type const& event, product_type const& product) {
		return TVector2::Phi_mpi_pi(product.m_recoNeutrinoOnRecoMetProjection.Phi());
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoNeutrinoOnGenMetProjectionPar", [](event_type const& event, product_type const& product) {
		return product.m_recoNeutrinoOnGenMetProjection.X();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoNeutrinoOnGenMetProjectionPerp", [](event_type const& event, product_type const& product) {
		return product.m_recoNeutrinoOnGenMetProjection.Y();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoNeutrinoOnGenMetProjectionPhi", [](event_type const& event, product_type const& product) {
		return TVector2::Phi_mpi_pi(product.m_recoNeutrinoOnGenMetProjection.Phi());
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoMetOnGenMetProjectionPar", [](event_type const& event, product_type const& product) {
		return product.m_recoMetOnGenMetProjection.X();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoMetOnGenMetProjectionPerp", [](event_type const& event, product_type const& product) {
		return product.m_recoMetOnGenMetProjection.Y();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoMetOnGenMetProjectionPhi", [](event_type const& event, product_type const& product) {
		return TVector2::Phi_mpi_pi(product.m_recoMetOnGenMetProjection.Phi());
	});
}

void MetprojectionProducer::Produce(event_type const& event, product_type& product, setting_type const& settings) const
{
	assert(product.m_svfitResults.momentum);
	assert(product.m_met);
	assert(event.m_genMet);

	// comparisons with SVFit, purely on reco level
	TVector2 svFitMomentum(product.m_svfitResults.momentum->X(), product.m_svfitResults.momentum->Y());
	TVector2 diLeptonMomentum(product.m_diLeptonSystem.x(), product.m_diLeptonSystem.Y());
	TVector2 met(product.m_met->p4.Vect().X(), product.m_met->p4.Vect().Y());

	TVector2 neutrinoMomentum = svFitMomentum - diLeptonMomentum;

	product.m_recoNeutrinoOnRecoMetProjection = neutrinoMomentum.Rotate(- met.Phi());
	// generator studies
	TVector2 genMet(event.m_genMet->p4.Vect().X(), event.m_genMet->p4.Vect().Y());
	product.m_recoNeutrinoOnGenMetProjection = neutrinoMomentum.Rotate( - genMet.Phi());

	product.m_recoMetOnGenMetProjection = met.Rotate( -genMet.Phi());
}
