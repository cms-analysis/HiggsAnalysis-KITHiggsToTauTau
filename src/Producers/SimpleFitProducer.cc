
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
	
	KLepton* tauToOneProng = nullptr;
	KTau* tauToA1 = nullptr;
	
	for (std::vector<KLepton*>::iterator leptonIt = product.m_flavourOrderedLeptons.begin();
	     leptonIt != product.m_flavourOrderedLeptons.end(); ++leptonIt)
	{
		if ((*leptonIt)->flavour() == KLeptonFlavour::TAU)
		{
			KTau* tau = static_cast<KTau*>(*leptonIt);
			
			if ((! tauToA1) &&
			    (tau->decayMode == reco::PFTau::hadronicDecayMode::kThreeProng0PiZero) &&
			    (tau->chargedHadronCandidates.size() > 2) &&
			    tau->sv.valid)
			{
				tauToA1 = tau;
			}
			else if ((! tauToOneProng) &&
			         (tau->decayMode == reco::PFTau::hadronicDecayMode::kOneProng0PiZero))
			{
				tauToOneProng = *leptonIt;
			}
		}
		else if (! tauToOneProng)
		{
			tauToOneProng = *leptonIt;
		}
	}
	
	if ((tauToOneProng != nullptr) && (tauToA1 != nullptr))
	{
		// one prong decay
		std::vector<float> muonHelixParameters = tauToOneProng->track.helixParameters();
		TMatrixT<double> muonHelixParametersInput(TrackParticle::NHelixPar, 1);
		for (unsigned int parameterIndex1 = 0; parameterIndex1 < TrackParticle::NHelixPar; ++parameterIndex1)
		{
			muonHelixParametersInput[parameterIndex1][0] = muonHelixParameters[parameterIndex1];
		}
		TMatrixTSym<double> muonHelixCovarianceInput = Utility::ConvertMatrixSym<ROOT::Math::SMatrix<float, reco::Track::dimension, reco::Track::dimension, ROOT::Math::MatRepSym<float, reco::Track::dimension> >, TMatrixTSym<double> >(tauToOneProng->track.helixCovariance, TrackParticle::NHelixPar);
		int pdgIdMuon = static_cast<int>(DefaultValues::pdgIdMuon * tauToOneProng->charge() / std::abs(tauToOneProng->charge()));
		TrackParticle muonInput(muonHelixParametersInput, muonHelixCovarianceInput, pdgIdMuon, tauToOneProng->p4.mass(), tauToOneProng->charge(), tauToOneProng->track.magneticField);
		
		// tau
		// https://github.com/cherepan/LLRHiggsTauTau/blob/VladimirDev/NtupleProducer/plugins/TauFiller.cc#L483
		// https://github.com/cherepan/LLRHiggsTauTau/blob/VladimirDev/NtupleProducer/plugins/TauFiller.cc#L464
		// https://github.com/cherepan/LLRHiggsTauTau/blob/VladimirDev/NtupleProducer/src/ParticleBuilder.cc#L11-L40
		unsigned int nLorentzAndVertexParameters = TrackHelixVertexFitter::NFreeTrackPar+TrackHelixVertexFitter::NExtraPar+TrackHelixVertexFitter::MassOffSet; // LorentzVectorParticle::NLorentzandVertexPar
		TMatrixT<double> tauParameters(nLorentzAndVertexParameters, 1);
		tauParameters[TrackHelixVertexFitter::x0][0] = tauToA1->sv.position.X();
		tauParameters[TrackHelixVertexFitter::y0][0] = tauToA1->sv.position.Y();
		tauParameters[TrackHelixVertexFitter::z0][0] = tauToA1->sv.position.Z();
		tauParameters[TrackHelixVertexFitter::kappa0][0] = tauToA1->track.qOverP();
		tauParameters[TrackHelixVertexFitter::lambda0][0] = tauToA1->track.lambda();
		tauParameters[TrackHelixVertexFitter::phi0][0] = tauToA1->track.phi();
		tauParameters[TrackHelixVertexFitter::NFreeTrackPar+TrackHelixVertexFitter::MassOffSet][0] = DefaultValues::ChargedPionMass;
		tauParameters[TrackHelixVertexFitter::NFreeTrackPar+TrackHelixVertexFitter::BField0][0] = tauToA1->track.magneticField;
		TMatrixT<double> tauParametersInput = TrackHelixVertexFitter::ComputeLorentzVectorPar(tauParameters);
		
		TMatrixTSym<double> tauCovariance(nLorentzAndVertexParameters);
		for (unsigned int parameterIndex1 = 0; parameterIndex1 < TrackHelixVertexFitter::NFreeVertexPar; ++parameterIndex1)
		{
			for (unsigned int parameterIndex2 = 0; parameterIndex2 < TrackHelixVertexFitter::NFreeVertexPar; ++parameterIndex2)
			{
				tauCovariance[parameterIndex1][parameterIndex2] = tauToA1->sv.covariance[parameterIndex1][parameterIndex2];
			}
		}
		tauCovariance[TrackHelixVertexFitter::kappa0][TrackHelixVertexFitter::kappa0] = tauToA1->track.helixCovariance(reco::Track::i_qoverp, reco::Track::i_qoverp);
		tauCovariance[TrackHelixVertexFitter::lambda0][TrackHelixVertexFitter::lambda0] = tauToA1->track.helixCovariance(reco::Track::i_lambda, reco::Track::i_lambda);
		tauCovariance[TrackHelixVertexFitter::phi0][TrackHelixVertexFitter::phi0] = tauToA1->track.helixCovariance(reco::Track::i_phi, reco::Track::i_phi);
		tauCovariance(nLorentzAndVertexParameters-1, nLorentzAndVertexParameters-1) = 1e-10;
		tauCovariance(nLorentzAndVertexParameters-2, nLorentzAndVertexParameters-2) = 1e-10;
		TMatrixTSym<double> tauCovarianceInput = ErrorMatrixPropagator::PropagateError(&TrackHelixVertexFitter::ComputeLorentzVectorPar, tauParameters, tauCovariance);
		
		int pdgIdTau = static_cast<int>(DefaultValues::pdgIdTau * tauToA1->charge() / std::abs(tauToA1->charge()));
		LorentzVectorParticle tauInput(tauParametersInput, tauCovarianceInput, pdgIdTau, tauToA1->charge(), tauToA1->track.magneticField);
		
		// MET
		unsigned int nMetComponents = 2;
		TMatrixT<double> metVector(nMetComponents, 1);
		metVector[0][0] = product.m_met.p4.Vect().X();
		metVector[1][0] = product.m_met.p4.Vect().Y();
		
		TMatrixTSym<double> metCovariance = Utility::ConvertMatrixSym<ROOT::Math::SMatrix<double, 2, 2, ROOT::Math::MatRepSym<double, 2> >, TMatrixTSym<double> >(product.m_met.significance, nMetComponents);
		PTObject metInput(metVector, metCovariance);
		
		// PV
		// TODO: change to refitted PV
		TVector3 pvInput = Utility::ConvertPxPyPzVector<RMPoint, TVector3>(event.m_vertexSummary->pv.position);
		TMatrixTSym<double> pvCovarianceInput = Utility::ConvertMatrixSym<ROOT::Math::SMatrix<double, 3, 3, ROOT::Math::MatRepSym<double, 3> >, TMatrixTSym<double> >(event.m_vertexSummary->pv.covariance, 3);
		
		// Fit
		GlobalEventFit globalEventFit(muonInput, tauInput, metInput, pvInput, pvCovarianceInput);
		GEFObject fitResult = globalEventFit.Fit();
		if (fitResult.isValid())
		{
			product.m_simpleFitTaus[tauToOneProng] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getTauMu().LV());
			product.m_simpleFitTaus[tauToA1] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getTauH().LV());
			product.m_diTauSystemSimpleFit = product.m_simpleFitTaus[tauToOneProng] + product.m_simpleFitTaus[tauToA1];
		}
	}
}

