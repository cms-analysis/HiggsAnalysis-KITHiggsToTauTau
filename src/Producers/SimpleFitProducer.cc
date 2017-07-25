
#include "TMatrixT.h"
#include "TMatrixTSym.h"
#include "TVector3.h"

#include "DataFormats/TauReco/interface/PFTau.h"

#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/SimpleFitProducer.h"

#include "TauPolSoftware/SimpleFits/interface/ErrorMatrixPropagator.h"
#include "TauPolSoftware/SimpleFits/interface/GEFObject.h"
#include "TauPolSoftware/SimpleFits/interface/GlobalEventFit.h"
#include "TauPolSoftware/SimpleFits/interface/LorentzVectorParticle.h"
#include "TauPolSoftware/SimpleFits/interface/TrackHelixVertexFitter.h"
#include "TauPolSoftware/SimpleFits/interface/PTObject.h"


void SimpleFitProducer::Init(setting_type const& settings)
{
    ProducerBase<HttTypes>::Init(settings);
}


void SimpleFitProducer::Produce(event_type const& event, product_type& product,
                                setting_type const& settings) const
{
	assert(product.m_flavourOrderedLeptons.size() >= 2);
	assert(event.m_vertexSummary); // TODO: change to refitted PV
	
	KLepton* lepton = nullptr;
	KTau* tauToA1 = nullptr;
	
	for (std::vector<KLepton*>::iterator leptonIt = product.m_flavourOrderedLeptons.begin();
	     leptonIt != product.m_flavourOrderedLeptons.end(); ++leptonIt)
	{
		if ((! tauToA1) && ((*leptonIt)->flavour() == KLeptonFlavour::TAU))
		{
			KTau* tau = static_cast<KTau*>(*leptonIt);
			// https://github.com/cms-sw/cmssw/blob/09c3fce6626f70fd04223e7dacebf0b485f73f54/DataFormats/TauReco/interface/PFTau.h#L34-L54
			if ((tau->decayMode == reco::PFTau::hadronicDecayMode::kThreeProng0PiZero) &&
			    (tau->chargedHadronCandidates.size() > 2) &&
			    tau->sv.valid)
			{
				tauToA1 = tau;
			}
		}
		else if (! lepton)
		{
			lepton = *leptonIt;
		}
	}
	
	if ((lepton != nullptr) && (tauToA1 != nullptr))
	{
		// lepton
		std::vector<float> muonHelixParameters = lepton->track.helixParameters();
		TMatrixT<double> muonHelixParametersInput(TrackParticle::NHelixPar, 1);
		for (unsigned int parameterIndex1 = 0; parameterIndex1 < TrackParticle::NHelixPar; ++parameterIndex1)
		{
			muonHelixParametersInput[parameterIndex1][0] = muonHelixParameters[parameterIndex1];
		}
		TMatrixTSym<double> muonHelixCovarianceInput = Utility::ConvertMatrixSym<ROOT::Math::SMatrix<float, reco::Track::dimension, reco::Track::dimension, ROOT::Math::MatRepSym<float, reco::Track::dimension> >, TMatrixTSym<double> >(lepton->track.helixCovariance, TrackParticle::NHelixPar);
		int pdgIdMuon = static_cast<int>(DefaultValues::pdgIdMuon * lepton->charge() / std::abs(lepton->charge()));
		TrackParticle muonInput(muonHelixParametersInput, muonHelixCovarianceInput, pdgIdMuon, lepton->p4.mass(), lepton->charge(), lepton->track.magneticField);
		
		// tau
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
		TMatrixTSym<double> tauCovarianceInput = ErrorMatrixPropagator::PropagateError(&TrackHelixVertexFitter::ComputeLorentzVectorPar, tauParametersInput, tauCovariance);
		
		int pdgIdTau = static_cast<int>(DefaultValues::pdgIdTau * tauToA1->charge() / std::abs(tauToA1->charge()));
		LorentzVectorParticle tauInput(tauParametersInput, tauCovariance, pdgIdTau, tauToA1->charge(), tauToA1->track.magneticField);
		
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
		GlobalEventFit globalEventFit(muonInput, tauInput,  metInput, pvInput, pvCovarianceInput);
		GEFObject fitResult = globalEventFit.Fit();
		if (fitResult.isValid())
		{
			product.m_simpleFitTaus[lepton] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getTauMu().LV());
			product.m_simpleFitTaus[tauToA1] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getTauH().LV());
		}
	}
}

