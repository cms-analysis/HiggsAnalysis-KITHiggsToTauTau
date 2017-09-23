
#include "TMatrixT.h"
#include "TMatrixTSym.h"
#include "TVector3.h"

#include "DataFormats/TauReco/interface/PFTau.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/SimpleFitProducer.h"

#include "TauPolSoftware/SimpleFits/interface/ErrorMatrixPropagator.h"
#include "TauPolSoftware/SimpleFits/interface/GEFObject.h"
#include "TauPolSoftware/SimpleFits/interface/GlobalEventFit.h"
#include "TauPolSoftware/SimpleFits/interface/LorentzVectorParticle.h"
#include "TauPolSoftware/SimpleFits/interface/TrackHelixVertexFitter.h"
#include "TauPolSoftware/SimpleFits/interface/PTObject.h"


std::string SimpleFitProducer::GetProducerId() const
{
	return "SimpleFitProducer";
}

void SimpleFitProducer::Init(setting_type const& settings, metadata_type& metadata)
{
    ProducerBase<HttTypes>::Init(settings, metadata);
	
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "simpleFitAvailable", [](event_type const& event, product_type const& product) {
		return (Utility::Contains(product.m_simpleFitTaus, product.m_flavourOrderedLeptons.at(0)) &&
		        Utility::Contains(product.m_simpleFitTaus, product.m_flavourOrderedLeptons.at(1)));
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitLV", [](event_type const& event, product_type const& product) {
		return product.m_diTauSystemSimpleFit;
	});
	
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "simpleFitTau1Available", [](event_type const& event, product_type const& product) {
		return Utility::Contains(product.m_simpleFitTaus, product.m_flavourOrderedLeptons.at(0));
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitTau1LV", [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_simpleFitTaus, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "simpleFitTau1ERatio", [](event_type const& event, product_type const& product) {
		if (Utility::Contains(product.m_simpleFitTaus, product.m_flavourOrderedLeptons.at(0)))
		{
			return product.m_flavourOrderedLeptons.at(0)->p4.E() / SafeMap::Get(product.m_simpleFitTaus, product.m_flavourOrderedLeptons.at(0)).E();
		}
		else
		{
			return DefaultValues::UndefinedFloat;
		}
	});
	
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "simpleFitTau2Available", [](event_type const& event, product_type const& product) {
		return Utility::Contains(product.m_simpleFitTaus, product.m_flavourOrderedLeptons.at(1));
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitTau2LV", [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_simpleFitTaus, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "simpleFitTau2ERatio", [](event_type const& event, product_type const& product) {
		if (Utility::Contains(product.m_simpleFitTaus, product.m_flavourOrderedLeptons.at(1)))
		{
			return product.m_flavourOrderedLeptons.at(1)->p4.E() / SafeMap::Get(product.m_simpleFitTaus, product.m_flavourOrderedLeptons.at(1)).E();
		}
		else
		{
			return DefaultValues::UndefinedFloat;
		}
	});
}

void SimpleFitProducer::Produce(event_type const& event, product_type& product,
                                setting_type const& settings, metadata_type const& metadata) const
{
	assert(product.m_flavourOrderedLeptons.size() >= 2);
	assert(event.m_vertexSummary); // TODO: change to refitted PV
	
	KLepton* oneProng = nullptr;
	KTau* a1 = nullptr;
	
	for (std::vector<KLepton*>::iterator leptonIt = product.m_flavourOrderedLeptons.begin();
	     leptonIt != product.m_flavourOrderedLeptons.end(); ++leptonIt)
	{
		if ((*leptonIt)->flavour() == KLeptonFlavour::TAU)
		{
			KTau* tau = static_cast<KTau*>(*leptonIt);
			
			if ((! a1) &&
			    (tau->decayMode == reco::PFTau::hadronicDecayMode::kThreeProng0PiZero) &&
			    (tau->chargedHadronCandidates.size() > 2) &&
			    tau->sv.valid)
			{
				a1 = tau;
			}
			else if ((! oneProng) &&
			         (tau->decayMode == reco::PFTau::hadronicDecayMode::kOneProng0PiZero))
			{
				oneProng = *leptonIt;
			}
		}
		else if (! oneProng)
		{
			oneProng = *leptonIt;
		}
	}
	
	if ((oneProng != nullptr) && (a1 != nullptr))
	{
		// one prong decay
		std::vector<float> oneProngHelixParameters = oneProng->track.helixParameters();
		TMatrixT<double> oneProngHelixParametersInput(TrackParticle::NHelixPar, 1);
		for (unsigned int parameterIndex1 = 0; parameterIndex1 < TrackParticle::NHelixPar; ++parameterIndex1)
		{
			oneProngHelixParametersInput[parameterIndex1][0] = oneProngHelixParameters[parameterIndex1];
		}
		TMatrixTSym<double> oneProngHelixCovarianceInput = Utility::ConvertMatrixSym<ROOT::Math::SMatrix<float, reco::Track::dimension, reco::Track::dimension, ROOT::Math::MatRepSym<float, reco::Track::dimension> >, TMatrixTSym<double> >(oneProng->track.helixCovariance, TrackParticle::NHelixPar);
		
		// LOG(WARNING) << "\n\nSimpleFits inputs (oneProng):";
		// LOG(INFO) << "\noneProngHelixParametersInput:";
		// oneProngHelixParametersInput.Print();
		// LOG(INFO) << "\noneProngHelixCovarianceInput:";
		// oneProngHelixCovarianceInput.Print();
		// LOG(INFO) << "\noneProng->pdgId(): " << oneProng->pdgId();
		// LOG(INFO) << "oneProng->p4.mass(): " << oneProng->p4.mass();
		// LOG(INFO) << "oneProng->charge(): " << oneProng->charge();
		TrackParticle oneProngInput(oneProngHelixParametersInput, oneProngHelixCovarianceInput, oneProng->pdgId(), oneProng->p4.mass(), oneProng->charge(), oneProng->track.magneticField);
		
		// tau
		// https://github.com/cherepan/LLRHiggsTauTau/blob/VladimirDev/NtupleProducer/plugins/TauFiller.cc#L483
		// https://github.com/cherepan/LLRHiggsTauTau/blob/VladimirDev/NtupleProducer/plugins/TauFiller.cc#L464
		// https://github.com/cherepan/LLRHiggsTauTau/blob/VladimirDev/NtupleProducer/src/ParticleBuilder.cc#L11-L40
		unsigned int nLorentzAndVertexParameters = TrackHelixVertexFitter::NFreeTrackPar+TrackHelixVertexFitter::NExtraPar+TrackHelixVertexFitter::MassOffSet; // LorentzVectorParticle::NLorentzandVertexPar
		TMatrixT<double> tauParameters(nLorentzAndVertexParameters, 1);
		TMatrixTSym<double> tauCovariance(nLorentzAndVertexParameters);
		for (int parameterIndex1 = 0; parameterIndex1 < 7; ++parameterIndex1)
		{
			tauParameters[parameterIndex1][0] = a1->refittedThreeProngParameters[parameterIndex1];
			for (int parameterIndex2 = 0; parameterIndex2 < 7; ++parameterIndex2)
			{
				tauCovariance[parameterIndex1][parameterIndex1] = a1->refittedThreeProngCovariance[parameterIndex1][parameterIndex2];
			}
		}
		tauParameters[TrackHelixVertexFitter::NFreeTrackPar+TrackHelixVertexFitter::BField0][0] = a1->track.magneticField;
		TMatrixT<double> tauParametersInput = TrackHelixVertexFitter::ComputeLorentzVectorPar(tauParameters);
		TMatrixTSym<double> tauCovarianceInput = ErrorMatrixPropagator::PropagateError(&TrackHelixVertexFitter::ComputeLorentzVectorPar, tauParameters, tauCovariance);
		
		// LOG(WARNING) << "\n\nSimpleFits inputs (a1):";
		// LOG(INFO) << "\ntauParametersInput:";
		// tauParametersInput.Print();
		// LOG(INFO) << "\ntauCovarianceInput:";
		// tauCovarianceInput.Print();
		// LOG(INFO) << "\na1->pdgId(): " << a1->pdgId();
		// LOG(INFO) << "a1->charge(): " << a1->charge();
		// LOG(INFO) << "a1->track.magneticField: " << a1->track.magneticField;
		LorentzVectorParticle tauInput(tauParametersInput, tauCovarianceInput, a1->pdgId(), a1->charge(), a1->track.magneticField);
		
		// MET
		unsigned int nMetComponents = 2;
		TMatrixT<double> metVector(nMetComponents, 1);
		metVector[0][0] = product.m_met.p4.Vect().X();
		metVector[1][0] = product.m_met.p4.Vect().Y();
		
		TMatrixTSym<double> metCovariance = Utility::ConvertMatrixSym<ROOT::Math::SMatrix<double, 2, 2, ROOT::Math::MatRepSym<double, 2> >, TMatrixTSym<double> >(product.m_met.significance, nMetComponents);
		
		// LOG(WARNING) << "\n\nSimpleFits inputs (MET):";
		// LOG(INFO) << "\nmetVector:";
		// metVector.Print();
		// LOG(INFO) << "\nmetCovariance:";
		// metCovariance.Print();
		PTObject metInput(metVector, metCovariance);
		
		// PV
		KVertex* pv = (product.m_refitPV ? product.m_refitPV : &(event.m_vertexSummary->pv));
		TVector3 pvInput = Utility::ConvertPxPyPzVector<RMPoint, TVector3>(pv->position);
		TMatrixTSym<double> pvCovarianceInput = Utility::ConvertMatrixSym<ROOT::Math::SMatrix<double, 3, 3, ROOT::Math::MatRepSym<double, 3> >, TMatrixTSym<double> >(pv->covariance, 3);
		
		// LOG(WARNING) << "\nSimpleFits inputs (PV):";
		// LOG(INFO) << "\npvInput:";
		// pvInput.Print();
		// LOG(INFO) << "\npvCovarianceInput:";
		// pvCovarianceInput.Print();
		
		// Fit
		GlobalEventFit globalEventFit(oneProngInput, tauInput, metInput, pvInput, pvCovarianceInput);
		GEFObject fitResult = globalEventFit.Fit();
		// LOG(ERROR) << "\n\nSimpleFits outputs:";
		if (fitResult.isValid())
		{
			product.m_simpleFitTaus[oneProng] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getTauMu().LV());
			product.m_simpleFitTaus[a1] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getTauH().LV());
			product.m_diTauSystemSimpleFit = product.m_simpleFitTaus[oneProng] + product.m_simpleFitTaus[a1];
			// LOG(INFO) << "tauToOneProng: " << product.m_simpleFitTaus[oneProng];
			// LOG(INFO) << "tauToA1: " << product.m_simpleFitTaus[a1];
		}
	}
}

