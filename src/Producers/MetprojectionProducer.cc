
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MetprojectionProducer.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/Quantities.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "TVector2.h"
#include "TVector.h"
#include "TMatrixTSym.h"

#include "DataFormats/METReco/interface/MET.h"

void MetprojectionProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	m_isData = settings.GetInputIsData();

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoMetPar", [](event_type const& event, product_type const& product) {
		return product.m_recoMetOnBoson.X();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoMetPerp", [](event_type const& event, product_type const& product) {
		return product.m_recoMetOnBoson.Y();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoMetPhi", [](event_type const& event, product_type const& product) {
		return product.m_recoMetOnBoson.Phi();
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoilPar", [](event_type const& event, product_type const& product) {
		return product.m_recoilOnBoson.X();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoilPerp", [](event_type const& event, product_type const& product) {
		return product.m_recoilOnBoson.Y();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoilPhi", [](event_type const& event, product_type const& product) {
		return product.m_recoilOnBoson.Phi();
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
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genMetSumEt", [](event_type const& event, product_type const& product) 
	{
		return (!(event.m_genMet) ? DefaultValues::UndefinedFloat : event.m_genMet->sumEt);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genMetPt", [] (event_type const& event, product_type const& product)
	{
		return (!(event.m_genMet) ? DefaultValues::UndefinedFloat : event.m_genMet->p4.Pt());
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genMetPhi", [](event_type const& event, product_type const& product)
	{
		return (!(event.m_genMet) ? DefaultValues::UndefinedFloat : event.m_genMet->p4.Phi());
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("chiSquare", [](event_type const& event, product_type const& product)
	{
		return product.chiSquare;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("probChiSquare", [](event_type const& event, product_type const& product)
	{
		return TMath::Prob(product.chiSquare, 2);
	});
}

void MetprojectionProducer::Produce(event_type const& event, product_type& product, setting_type const& settings) const
{
	assert(product.m_metUncorr);

	TVector2 diLeptonMomentum(product.m_diLeptonSystem.x(), product.m_diLeptonSystem.Y());
	TVector2 met(product.m_metUncorr->p4.Vect().X(), product.m_metUncorr->p4.Vect().Y());
	TVector2 recoil = diLeptonMomentum + met;
	recoil = recoil.Rotate(TMath::Pi()); 

	TVector2 genMet(0,0);
	if( !m_isData )
	{
		assert(event.m_genMet);
		genMet.Set(event.m_genMet->p4.Vect().X(), event.m_genMet->p4.Vect().Y());
		product.m_recoMetOnGenMetProjection = met.Rotate( -genMet.Phi());
	}
	else
	{
		product.m_recoMetOnGenMetProjection = TVector2(0,0);
	}

	product.m_recoMetOnBoson = met.Rotate(-diLeptonMomentum.Phi());
	product.m_recoilOnBoson = recoil.Rotate(-diLeptonMomentum.Phi());

	// "pulls", recommended as crosscheck for covariance matrix, suggested by Christian Veelken
	if(product.m_genBosonLVFound && (!m_isData))
	{
		TVector2 genBoson(product.m_genBosonLV.X(), product.m_genBosonLV.Y());
		TVector2 rotatedMet = met.Rotate( - genBoson.Phi());
		TVector2 rotatedGenMet = genMet.Rotate( -genBoson.Phi());
		ROOT::Math::SMatrix<double,2> rotationMatrix;
		rotationMatrix(0,0) = rotationMatrix(1,1) = std::cos( genBoson.Phi());
		rotationMatrix(0,1) =   std::sin( genBoson.Phi());
		rotationMatrix(1,0) = - std::sin( genBoson.Phi());

		ROOT::Math::SMatrix<double,2> rotatedMatrix = rotationMatrix * product.m_metUncorr->significance;
		product.m_metPull.Set( (rotatedGenMet.X() - rotatedMet.X()) / sqrt(rotatedMatrix(0,0)), 
	                       	   (rotatedGenMet.Y() - rotatedMet.Y()) / sqrt(rotatedMatrix(1,1)) );

		TVector2 dRecoGenMet = met - genMet;
		product.chiSquare = Quantities::MetChiSquare(dRecoGenMet, product.m_metUncorr->significance);
	}
	else
	{
		product.m_metPull.Set(DefaultValues::UndefinedFloat, DefaultValues::UndefinedFloat);
		product.m_metPfPull.Set(DefaultValues::UndefinedFloat, DefaultValues::UndefinedFloat);
		product.chiSquare = DefaultValues::UndefinedFloat;
	}
}
