
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MetprojectionProducer.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "TVector2.h"

#include "DataFormats/METReco/interface/MET.h"

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
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("metPullX", [](event_type const& event, product_type const& product) {
		return product.m_metPull.X();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("metPullY", [](event_type const& event, product_type const& product) {
		return product.m_metPull.Y();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("metPfPullX", [](event_type const& event, product_type const& product) {
		return product.m_metPfPull.X();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("metPfPullY", [](event_type const& event, product_type const& product) {
		return product.m_metPfPull.Y();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genMetSumEt", [](event_type const& event, product_type const& product) 
	{
		return event.m_genMet->sumEt;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genMetPt", [] (event_type const& event, product_type const& product)
	{
		return event.m_genMet->p4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genMetPhi", [](event_type const& event, product_type const& product)
	{
		return event.m_genMet->p4.Phi();
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
	TVector2 pfmet(product.m_pfmet->p4.Vect().X(), product.m_pfmet->p4.Vect().Y());

	TVector2 neutrinoMomentum = svFitMomentum - diLeptonMomentum;

	product.m_recoNeutrinoOnRecoMetProjection = neutrinoMomentum.Rotate(- met.Phi());
	// generator studies
	TVector2 genMet(event.m_genMet->p4.Vect().X(), event.m_genMet->p4.Vect().Y());
	product.m_recoNeutrinoOnGenMetProjection = neutrinoMomentum.Rotate( - genMet.Phi());

	product.m_recoMetOnGenMetProjection = met.Rotate( -genMet.Phi());

	// "pulls", recommended as crosscheck for covariance matrix, suggested by Christian Veelken
	if(product.m_genBoson.size() > 0)
	{
		TVector2 genBoson(product.m_genBoson[0].node->p4.X(), product.m_genBoson[0].node->p4.Y());
		TVector2 rotatedMet = met.Rotate( - genBoson.Phi());
		TVector2 rotatedGenMet = genMet.Rotate( -genBoson.Phi());
		ROOT::Math::SMatrix<double,2> rotationMatrix;
		rotationMatrix(0,0) = rotationMatrix(1,1) = std::cos( genBoson.Phi());
		rotationMatrix(0,1) =   std::sin( genBoson.Phi());
		rotationMatrix(1,0) = - std::sin( genBoson.Phi());

		ROOT::Math::SMatrix<double,2> rotatedMatrix = rotationMatrix * product.m_met->significance;
		product.m_metPull.Set( (rotatedGenMet.X() - rotatedMet.X()) / sqrt(rotatedMatrix(0,0)), 
	                       	   (rotatedGenMet.Y() - rotatedMet.Y()) / sqrt(rotatedMatrix(1,1)) );

		ROOT::Math::SMatrix<double,2> rotatedPfMatrix = rotationMatrix * product.m_pfmet->significance;
		product.m_metPfPull.Set( (rotatedGenMet.X() - rotatedMet.X()) / sqrt(rotatedPfMatrix(0,0)), 
	                         	 (rotatedGenMet.Y() - rotatedMet.Y()) / sqrt(rotatedPfMatrix(1,1)) );
	}
	else
	{
		product.m_metPull.Set(0.0,0.0);
		product.m_metPfPull.Set(0.0,0.0);
	}
}
