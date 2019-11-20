
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MetprojectionProducer.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/Quantities.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "TVector2.h"
#include "TVector.h"
#include "TMatrixTSym.h"

#include "DataFormats/METReco/interface/MET.h"

void MetprojectionProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	m_isData = settings.GetInputIsData();

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoMetPar", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_recoMetOnBoson.X();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoMetPerp", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_recoMetOnBoson.Y();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoMetPhi", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_recoMetOnBoson.Phi();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPfMetPar", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_recoPfMetOnBoson.X();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPfMetPerp", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_recoPfMetOnBoson.Y();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPfMetPhi", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_recoPfMetOnBoson.Phi();
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoilPar", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_recoilOnBoson.X();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoilPerp", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_recoilOnBoson.Y();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoilPhi", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_recoilOnBoson.Phi();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pfrecoilPar", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_pfrecoilOnBoson.X();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pfrecoilPerp", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_pfrecoilOnBoson.Y();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pfrecoilPhi", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_pfrecoilOnBoson.Phi();
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoMetOnGenMetProjectionPar", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_recoMetOnGenMetProjection.X();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoMetOnGenMetProjectionPerp", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_recoMetOnGenMetProjection.Y();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoMetOnGenMetProjectionPhi", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return TVector2::Phi_mpi_pi(product.m_recoMetOnGenMetProjection.Phi());
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPfMetOnGenMetProjectionPar", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_recoPfMetOnGenMetProjection.X();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPfMetOnGenMetProjectionPerp", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_recoPfMetOnGenMetProjection.Y();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPfMetOnGenMetProjectionPhi", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return TVector2::Phi_mpi_pi(product.m_recoPfMetOnGenMetProjection.Phi());
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "metPlusVisLepsOnGenBosonPtOverGenBosonPt", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_metPlusVisLepsOnGenBosonPtOverGenBosonPt;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pfmetPlusVisLepsOnGenBosonPtOverGenBosonPt", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_pfmetPlusVisLepsOnGenBosonPtOverGenBosonPt;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "metPullX", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_metPull.X();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "metPullY", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_metPull.Y();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pfmetPullX", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_pfmetPull.X();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pfmetPullY", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_pfmetPull.Y();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMetSumEt", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) 
	{
		return (!(event.m_genMet) ? DefaultValues::UndefinedFloat : event.m_genMet->sumEt);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMetPt", [] (event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (!(event.m_genMet) ? DefaultValues::UndefinedFloat : event.m_genMet->p4.Pt());
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMetPhi", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (!(event.m_genMet) ? DefaultValues::UndefinedFloat : event.m_genMet->p4.Phi());
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genBosonPt", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genBosonPt;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genBosonPhi", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genBosonPhi;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "chiSquare", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_chiSquare;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "probChiSquare", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return TMath::Prob(product.m_chiSquare, 2);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "chiSquarePf", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_chiSquarePf;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "probChiSquarePf", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return TMath::Prob(product.m_chiSquarePf, 2);
	});
}

void MetprojectionProducer::Produce(event_type const& event, product_type& product, setting_type const& settings, metadata_type const& metadata) const
{
	TVector2 diLeptonMomentum(product.m_diLeptonSystem.x(), product.m_diLeptonSystem.Y());
	TVector2 met(product.m_met.p4.Vect().X(), product.m_met.p4.Vect().Y());
	TVector2 pfmet(product.m_pfmet.p4.Vect().X(), product.m_pfmet.p4.Vect().Y());
	TVector2 recoil = diLeptonMomentum + met;
	TVector2 pfrecoil = diLeptonMomentum + pfmet;
	recoil = recoil.Rotate(TMath::Pi()); 
	pfrecoil = pfrecoil.Rotate(TMath::Pi()); 

	TVector2 genMet(0,0);
	if( !m_isData )
	{
		assert(event.m_genMet);
		genMet.Set(event.m_genMet->p4.Vect().X(), event.m_genMet->p4.Vect().Y());
		product.m_recoMetOnGenMetProjection = met.Rotate( -genMet.Phi());
		product.m_recoPfMetOnGenMetProjection = pfmet.Rotate( -genMet.Phi());
	}
	else
	{
		product.m_recoMetOnGenMetProjection = TVector2(0,0);
		product.m_recoPfMetOnGenMetProjection = TVector2(0,0);
	}

	product.m_recoMetOnBoson = met.Rotate(-diLeptonMomentum.Phi());
	product.m_recoilOnBoson = recoil.Rotate(-diLeptonMomentum.Phi());
	product.m_recoPfMetOnBoson = pfmet.Rotate(-diLeptonMomentum.Phi());
	product.m_pfrecoilOnBoson = pfrecoil.Rotate(-diLeptonMomentum.Phi());

	// "pulls", recommended as crosscheck for covariance matrix, suggested by Christian Veelken
	if(product.m_genBosonLVFound && (!m_isData))
	{
		//quantity from MetCorrections
		TVector2 genBoson(product.m_pfmetCorrections[0],product.m_pfmetCorrections[1]);//product.m_genBosonLV.X(), product.m_genBosonLV.Y());
		TVector2 rotatedMet = met.Rotate( - genBoson.Phi());
		TVector2 rotatedPfMet = pfmet.Rotate( - genBoson.Phi());
		TVector2 rotatedGenMet = genMet.Rotate( -genBoson.Phi());
		TVector2 rotatedRecoil = recoil.Rotate( -genBoson.Phi());
		TVector2 rotatedPfRecoil = pfrecoil.Rotate( -genBoson.Phi());
        	//product.m_genMetMinusRecoRecoilOverGenBosonPt = DefaultValues::UndefinedFloat;// rotatedRecoil.X()/(Math::Sqrt(bosonLength));
        	//product.m_genMetMinusRecoPfRecoilOverGenBosonPt = DefaultValues::UndefinedFloat;//rotatedPfRecoil.X()/(ROOT::Math::Sqrt((genBoson*genBoson)));
        	TVector2 visibleLeps(product.m_mvametCorrections[2], product.m_mvametCorrections[3]);
		//should be the same
        	TVector2 visiblePfLeps(product.m_pfmetCorrections[2], product.m_pfmetCorrections[3]);
		
		TVector2 rotatedVisibleLeps = visiblePfLeps.Rotate( -genBoson.Phi());
		
            	product.m_metPlusVisLepsOnGenBosonPtOverGenBosonPt = (rotatedMet.X()+rotatedVisibleLeps.X())/(TMath::Sqrt(genBoson*genBoson));
            	product.m_pfmetPlusVisLepsOnGenBosonPtOverGenBosonPt = (rotatedPfMet.X()+rotatedVisibleLeps.X())/(TMath::Sqrt(genBoson*genBoson));
		ROOT::Math::SMatrix<double,2> rotationMatrix;
		rotationMatrix(0,0) = rotationMatrix(1,1) = std::cos( genBoson.Phi());
		rotationMatrix(0,1) =   std::sin( genBoson.Phi());
		rotationMatrix(1,0) = - std::sin( genBoson.Phi());

		ROOT::Math::SMatrix<double,2> rotatedMatrix = rotationMatrix * product.m_met.significance;
		ROOT::Math::SMatrix<double,2> rotatedPfMatrix = rotationMatrix * product.m_pfmet.significance;
		product.m_metPull.Set( (rotatedGenMet.X() - rotatedMet.X()) / sqrt(rotatedMatrix(0,0)), 
	                       	   (rotatedGenMet.Y() - rotatedMet.Y()) / sqrt(rotatedMatrix(1,1)) );
		product.m_pfmetPull.Set( (rotatedGenMet.X() - rotatedPfMet.X()) / sqrt(rotatedPfMatrix(0,0)), 
	                       	   (rotatedGenMet.Y() - rotatedPfMet.Y()) / sqrt(rotatedPfMatrix(1,1)) );

		TVector2 dRecoGenMet = met - genMet;
		TVector2 dPfRecoGenMet = pfmet - genMet;
		product.m_chiSquare = Quantities::MetChiSquare(dRecoGenMet, product.m_met.significance);
		product.m_chiSquarePf = Quantities::MetChiSquare(dPfRecoGenMet, product.m_pfmet.significance);
		product.m_genBosonPt = TMath::Sqrt(genBoson*genBoson);
		product.m_genBosonPhi = genBoson.Phi();
	}
	else
	{
		product.m_metPull.Set(DefaultValues::UndefinedFloat, DefaultValues::UndefinedFloat);
		product.m_pfmetPull.Set(DefaultValues::UndefinedFloat, DefaultValues::UndefinedFloat);
		product.m_chiSquare = DefaultValues::UndefinedFloat;
		product.m_chiSquarePf = DefaultValues::UndefinedFloat;
		product.m_metPlusVisLepsOnGenBosonPtOverGenBosonPt = DefaultValues::UndefinedFloat;
		product.m_pfmetPlusVisLepsOnGenBosonPtOverGenBosonPt = DefaultValues::UndefinedFloat;
		product.m_genBosonPt = DefaultValues::UndefinedFloat;
		product.m_genBosonPhi = DefaultValues::UndefinedFloat;
	}
}
