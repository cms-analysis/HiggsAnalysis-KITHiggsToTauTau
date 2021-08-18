
#include "TMatrixT.h"
#include "TMatrixTSym.h"
#include "TVector3.h"
#include "TVectorT.h"

#include "DataFormats/TauReco/interface/PFTau.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/SimpleFitProducer.h"

#include "TauPolSoftware/SimpleFits/interface/ErrorMatrixPropagator.h"
#include "TauPolSoftware/SimpleFits/interface/TPTRObject.h"
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

	m_massConstraint = settings.GetGEFMassConstraint();
	m_useCollinearityTauMu = settings.GetGEFUseCollinearityTauMu();
	m_useMVADecayModes = settings.GetGEFUseMVADecayModes();

	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "simpleFitTauRecoIsAmbiguous", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_simpleFitTauRecoIsAmbiguous;
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitTauA1PrefitPlusLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_simpleFitTauA1PrefitPlus;
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitTauA1PrefitMinusLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_simpleFitTauA1PrefitMinus;
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitTauA1PrefitZeroLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_simpleFitTauA1PrefitZero;
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitResonancePrefitResolvedFitLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_simpleFitResonancePrefitResolvedFit;
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitTau1PrefitResolvedFitLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return SafeMap::GetWithDefault(product.m_simpleFitTausPrefitResolvedFit, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitTau2PrefitResolvedFitLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return SafeMap::GetWithDefault(product.m_simpleFitTausPrefitResolvedFit, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitResonancePrefitResolvedGenLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_simpleFitResonancePrefitResolvedGen;
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitTau1PrefitResolvedGenLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return SafeMap::GetWithDefault(product.m_simpleFitTausPrefitResolvedGen, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitTau2PrefitResolvedGenLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return SafeMap::GetWithDefault(product.m_simpleFitTausPrefitResolvedGen, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedRMFLV);
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "simpleFitRotationSignificance", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_simpleFitRotationSignificance;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "simpleFitChi2Sum", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_simpleFitChi2Sum;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "simpleFitCsum", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_simpleFitCsum;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "simpleFitNiterations", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_simpleFitNiterations;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "simpleFitIndex", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_simpleFitIndex;
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "simpleFitConverged", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_simpleFitConverged;
	});

	for (int chi2index = 0; chi2index < 3; chi2index++) {
		std::string quantity = "simpleFitChi2_" + std::to_string(chi2index+1);
		// LOG(INFO) << quantity;
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, quantity, [chi2index](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
			if (product.m_simpleFitChi2.size() > 0)
			{
				return product.m_simpleFitChi2.at(chi2index);
			}
			else
			{
				return DefaultValues::UndefinedFloat;
			}
		});
	}

	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "simpleFitAvailable", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return (Utility::Contains(product.m_simpleFitTaus, product.m_flavourOrderedLeptons.at(0)) &&
		        Utility::Contains(product.m_simpleFitTaus, product.m_flavourOrderedLeptons.at(1)));
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_diTauSystemSimpleFit;
	});

	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "simpleFitTau1Available", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return Utility::Contains(product.m_simpleFitTaus, product.m_flavourOrderedLeptons.at(0));
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitTau1LV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return SafeMap::GetWithDefault(product.m_simpleFitTaus, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "simpleFitTau1ERatio", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		if (Utility::Contains(product.m_simpleFitTaus, product.m_flavourOrderedLeptons.at(0)))
		{
			return product.m_flavourOrderedLeptons.at(0)->p4.E() / SafeMap::Get(product.m_simpleFitTaus, product.m_flavourOrderedLeptons.at(0)).E();
		}
		else
		{
			return DefaultValues::UndefinedFloat;
		}
	});

	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "simpleFitTau2Available", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return Utility::Contains(product.m_simpleFitTaus, product.m_flavourOrderedLeptons.at(1));
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitTau2LV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return SafeMap::GetWithDefault(product.m_simpleFitTaus, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "simpleFitTau2ERatio", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		if (Utility::Contains(product.m_simpleFitTaus, product.m_flavourOrderedLeptons.at(1)))
		{
			return product.m_flavourOrderedLeptons.at(1)->p4.E() / SafeMap::Get(product.m_simpleFitTaus, product.m_flavourOrderedLeptons.at(1)).E();
		}
		else
		{
			return DefaultValues::UndefinedFloat;
		}
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitTau1ResolvedGenLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return SafeMap::GetWithDefault(product.m_simpleFitTausResolvedGen, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitTau2ResolvedGenLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return SafeMap::GetWithDefault(product.m_simpleFitTausResolvedGen, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedRMFLV);
	});
	// LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitTauA1PlusLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	// 	return product.m_simpleFitTauA1Plus;
	// });
	// LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitTauA1MinusLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	// 	return product.m_simpleFitTauA1Minus;
	// });
	// LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitTauA1ZeroLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	// 	return product.m_simpleFitTauA1Zero;
	// });


}

void SimpleFitProducer::Produce(event_type const& event, product_type& product,
                                setting_type const& settings, metadata_type const& metadata) const
{
	assert(product.m_flavourOrderedLeptons.size() >= 2);
	assert(event.m_vertexSummary); // TODO: change to refitted PV

	KLepton* oneProng = nullptr;
	KTau* a1 = nullptr;

	// LOG(INFO) << "SimpleFitProducer: START";

	for (std::vector<KLepton*>::iterator leptonIt = product.m_flavourOrderedLeptons.begin();
	     leptonIt != product.m_flavourOrderedLeptons.end(); ++leptonIt)
	{
		if ((*leptonIt)->flavour() == KLeptonFlavour::TAU)
		{
			KTau* tau = static_cast<KTau*>(*leptonIt);
			int decaymode = m_useMVADecayModes ? (int)tau->getDiscriminator("MVADM2017v1", event.m_tauMetadata) : tau->decayMode;
			// LOG(INFO) << "tau->sv.valid: " << tau->sv.valid;

			if ((! a1) &&
			    (decaymode == reco::PFTau::hadronicDecayMode::kThreeProng0PiZero) &&
			    (tau->chargedHadronCandidates.size() > 2) &&
			    tau->sv.valid)
			{
				a1 = tau;
			}
			else if ((! oneProng) &&
			         (decaymode == reco::PFTau::hadronicDecayMode::kOneProng0PiZero))
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
		// LOG(INFO) << "Found one prong and a1";
		// one prong decay
		std::vector<float> threeProngOneHelixParameters = oneProng->track.helixParameters();
		TMatrixT<double> threeProngOneHelixParametersInput(TrackParticle::NHelixPar, 1);
		for (unsigned int parameterIndex1 = 0; parameterIndex1 < TrackParticle::NHelixPar; ++parameterIndex1)
		{
			threeProngOneHelixParametersInput[parameterIndex1][0] = threeProngOneHelixParameters[parameterIndex1];
		}
		TMatrixTSym<double> oneProngHelixCovarianceInput = Utility::ConvertMatrixSym<ROOT::Math::SMatrix<float, reco::Track::dimension, reco::Track::dimension, ROOT::Math::MatRepSym<float, reco::Track::dimension> >, TMatrixTSym<double> >(oneProng->track.helixCovariance, TrackParticle::NHelixPar);

		// LOG(WARNING) << "\n\nSimpleFits inputs (oneProng):";
		// LOG(INFO) << "\nthreeProngOneHelixParametersInput:";
		// threeProngOneHelixParametersInput.Print();
		// LOG(INFO) << "\noneProngHelixCovarianceInput:";
		// oneProngHelixCovarianceInput.Print();

		threeProngOneHelixParametersInput[TrackParticle::kappa][0] = -threeProngOneHelixParametersInput[TrackParticle::kappa][0]*oneProng->track.magneticField/cos(threeProngOneHelixParametersInput[TrackParticle::lambda][0]);
		TMatrixTSym<double> Jacobi(TrackParticle::NHelixPar);
		// make unit matrix first
		for (size_t i_row = 0; i_row < TrackParticle::NHelixPar; i_row++)
		{
			Jacobi[i_row][i_row] = 1.0;
		}
		Jacobi[TrackParticle::kappa][reco::Track::i_qoverp] = (-1.0)*oneProng->track.magneticField/cos(oneProng->track.lambda());
		Jacobi[TrackParticle::kappa][reco::Track::i_lambda] = (-1.0)*oneProng->track.magneticField*oneProng->track.qOverP()*tan(oneProng->track.lambda())/cos(oneProng->track.lambda());

		// LOG(INFO) << "\nJacobi Matrix:";
		// Jacobi.Print();

		oneProngHelixCovarianceInput.Similarity(Jacobi);
		TrackParticle oneProngInput(threeProngOneHelixParametersInput, oneProngHelixCovarianceInput, oneProng->pdgId(), oneProng->p4.mass(), oneProng->charge(), oneProng->track.magneticField);

		// LOG(WARNING) << "\n\nSimpleFits inputs (oneProng) after change from qoverp->kappa:";
		// LOG(INFO) << "\nthreeProngOneHelixParametersInput:";
		// threeProngOneHelixParametersInput.Print();
		// LOG(INFO) << "\noneProngHelixCovarianceInput:";
		// oneProngHelixCovarianceInput.Print();
		// LOG(INFO) << "\noneProng->pdgId(): " << oneProng->pdgId();
		// LOG(INFO) << "oneProng->p4.mass(): " << oneProng->p4.mass();
		// LOG(INFO) << "oneProng->charge(): " << oneProng->charge();
		// LOG(INFO) << "threeProngOneHelixParametersInput[0][0]: " << threeProngOneHelixParametersInput[0][0];
		// LOG(INFO) << "oneProngInput.Parameter(TrackParticle::kappa): " << oneProngInput.Parameter(TrackParticle::kappa);
		// LOG(INFO) << "-q*oneProng->track.magneticField/oneProngInput.Parameter(TrackParticle::kappa): " << (-1)*oneProng->charge()*oneProng->track.magneticField/oneProngInput.Parameter(TrackParticle::kappa);
		// LOG(INFO) << "oneProng->track.qOverP(): " << oneProng->track.qOverP();
		// LOG(INFO) << "oneProng->p4.pt(): " << oneProng->p4.pt();
		// LOG(INFO) << "oneProng->p4.px(): " << oneProng->p4.px();
		// LOG(INFO) << "oneProng->p4.py(): " << oneProng->p4.py();
		// LOG(INFO) << "cos(oneProng->track.lambda())/fabs(oneProng->track.qOverP()): " << cos(oneProng->track.lambda())/fabs(oneProng->track.qOverP());

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
				tauCovariance[parameterIndex1][parameterIndex2] = a1->refittedThreeProngCovariance[parameterIndex1][parameterIndex2];
			}
		}
		tauParameters[TrackHelixVertexFitter::NFreeTrackPar+TrackHelixVertexFitter::BField0 + 1][0] = a1->track.magneticField; // was off by 1 and overwrote the a1 mass
		TMatrixT<double> tauParametersInput = SimpleFitProducer::ComputeLorentzVectorPar(tauParameters);
		TMatrixTSym<double> tauCovarianceInput = ErrorMatrixPropagator::PropagateError(&SimpleFitProducer::ComputeLorentzVectorPar, tauParameters, tauCovariance);

		// LOG(WARNING) << "\n\nSimpleFits inputs (a1):";
		// LOG(INFO) << "\ntauParameters:";
		// tauParameters.Print();
		// LOG(INFO) << "\ntauCovariance:";
		// tauCovariance.Print();
		// LOG(INFO) << "\ntauParametersInput:";
		// tauParametersInput.Print();
		// LOG(INFO) << "\ntauCovarianceInput:";
		// tauCovarianceInput.Print();
		// LOG(INFO) << "\na1->pdgId(): " << a1->pdgId();
		// LOG(INFO) << "a1->charge(): " << a1->charge();
		// LOG(INFO) << "a1->track.magneticField: " << a1->track.magneticField;

		LorentzVectorParticle tauInput(tauParametersInput, tauCovarianceInput, a1->resonancePdgId(), a1->charge(), a1->track.magneticField);

		// LOG(INFO) << "LVP px: " << tauInput.LV().Px();
		// LOG(INFO) << "LVP py: " << tauInput.LV().Py();
		// LOG(INFO) << "LVP pz: " << tauInput.LV().Pz();
		// LOG(INFO) << "LVP pt: " << tauInput.LV().Pt();
		// LOG(INFO) << "LVP svx: " << tauInput.Vertex().X();
		// LOG(INFO) << "LVP svy: " << tauInput.Vertex().Y();
		// LOG(INFO) << "LVP svz: " << tauInput.Vertex().Z();

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
		// KVertex* pv = (product.m_refitPV ? product.m_refitPV : &(event.m_vertexSummary->pv));
		KVertex* pv = (product.m_refitPVBS ? product.m_refitPVBS : &(event.m_vertexSummary->pv));
		TVector3 pvInput = Utility::ConvertPxPyPzVector<RMPoint, TVector3>(pv->position);
		TMatrixTSym<double> pvCovarianceInput = Utility::ConvertMatrixSym<ROOT::Math::SMatrix<double, 3, 3, ROOT::Math::MatRepSym<double, 3> >, TMatrixTSym<double> >(pv->covariance, 3);

		// LOG(WARNING) << "\nSimpleFits inputs (PV):";
		// LOG(INFO) << "\npvInput:";
		// pvInput.Print();
		// LOG(INFO) << "\npvCovarianceInput:";
		// pvCovarianceInput.Print();

		// Fit
		GlobalEventFit globalEventFit(oneProngInput, tauInput, metInput, pvInput, pvCovarianceInput);
		if (m_massConstraint > 0) globalEventFit.setMassConstraint(m_massConstraint);
		globalEventFit.setMinimizer(LagrangeMultipliersFitter::FittingProc::Standard);
		globalEventFit.setUseCollinearityTauMu(m_useCollinearityTauMu);
		TPTRObject tauReco = globalEventFit.getTPTRObject();
		GEFObject fitResult = globalEventFit.Fit();
		product.m_simpleFitTauRecoIsAmbiguous = tauReco.isAmbiguous();
		// LOG(INFO) << "product.m_simpleFitTauRecoIsAmbiguous: " << product.m_simpleFitTauRecoIsAmbiguous;
		if (product.m_simpleFitTauRecoIsAmbiguous)
		{
			product.m_simpleFitTauA1PrefitPlus = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(tauReco.getTauPlus().LV());
			product.m_simpleFitTauA1PrefitMinus = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(tauReco.getTauMinus().LV());
			// LOG(INFO) << "tauReco.getTauPlus().LV(): (px,py,pz,M)=(" << product.m_simpleFitTauA1PrefitPlus.px() << "," << product.m_simpleFitTauA1PrefitPlus.py() << "," << product.m_simpleFitTauA1PrefitPlus.pz() << "," << product.m_simpleFitTauA1PrefitPlus.M() << ")";
			// LOG(INFO) << "tauReco.getTauMinus().LV(): (px,py,pz,M)=(" << product.m_simpleFitTauA1PrefitMinus.px() << "," << product.m_simpleFitTauA1PrefitMinus.py() << "," << product.m_simpleFitTauA1PrefitMinus.pz() << "," << product.m_simpleFitTauA1PrefitMinus.M() << ")";
		}
		else
		{
			product.m_simpleFitTauA1PrefitZero = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(tauReco.getTauZero().LV());
			product.m_simpleFitRotationSignificance = tauReco.getRotationSignificance();
			// LOG(INFO) << "tauReco.getTauZero().LV(): (px,py,pz,M)=(" << product.m_simpleFitTauA1PrefitZero.px() << "," << product.m_simpleFitTauA1PrefitZero.py() << "," << product.m_simpleFitTauA1PrefitZero.pz() << "," << product.m_simpleFitTauA1PrefitZero.M() << ")";
			// LOG(INFO) << "product.m_simpleFitRotationSignificance: " << product.m_simpleFitRotationSignificance;
		}
		// LOG(ERROR) << "\n\nSimpleFits outputs:";
		// LOG(INFO) << "fitResult.isValid(): " << fitResult.isValid();
		if(product.m_genSimpleFitIndex1 != DefaultValues::UndefinedInt && product.m_genSimpleFitIndex2 != DefaultValues::UndefinedInt)
		{
			// fitResult.getInitTauHs().at(0).LV().Print();
			// fitResult.getInitTauMus().at(0).LV().Print();
			// fitResult.getInitTauHs().at(1).LV().Print();
			// fitResult.getInitTauMus().at(1).LV().Print();
			// fitResult.getInitTauHs().at(2).LV().Print();
			// fitResult.getInitTauMus().at(2).LV().Print();
			if(product.m_simpleFitTauRecoIsAmbiguous)
			{
				product.m_simpleFitResonancePrefitResolvedGen = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getInitResonances().at(product.m_genSimpleFitIndexMap[a1]).LV());
				product.m_simpleFitTausPrefitResolvedGen[oneProng] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getInitTauMus().at(product.m_genSimpleFitIndexMap[a1]).LV());
				product.m_simpleFitTausPrefitResolvedGen[a1] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getInitTauHs().at(product.m_genSimpleFitIndexMap[a1]).LV());
				// LOG(INFO) << "product.m_genSimpleFitIndexMap[a1]: " << product.m_genSimpleFitIndexMap[a1];
				// LOG(INFO) << "m_simpleFitResonancePrefitResolvedGen: (px,py,pz,M)=(" << product.m_simpleFitResonancePrefitResolvedGen.px() << "," << product.m_simpleFitResonancePrefitResolvedGen.py() << "," << product.m_simpleFitResonancePrefitResolvedGen.pz() << "," << product.m_simpleFitResonancePrefitResolvedGen.M() << ")";
				// LOG(INFO) << "m_simpleFitTausPrefitResolvedGen[oneProng]: (px,py,pz,M)=(" << product.m_simpleFitTausPrefitResolvedGen[oneProng].px() << "," << product.m_simpleFitTausPrefitResolvedGen[oneProng].py() << "," << product.m_simpleFitTausPrefitResolvedGen[oneProng].pz() << "," << product.m_simpleFitTausPrefitResolvedGen[oneProng].M() << ")";
				// LOG(INFO) << "m_simpleFitTausPrefitResolvedGen[a1]: (px,py,pz,M)=(" << product.m_simpleFitTausPrefitResolvedGen[a1].px() << "," << product.m_simpleFitTausPrefitResolvedGen[a1].py() << "," << product.m_simpleFitTausPrefitResolvedGen[a1].pz() << "," << product.m_simpleFitTausPrefitResolvedGen[a1].M() << ")";
			}
			else
			{
				product.m_simpleFitResonancePrefitResolvedGen = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getInitResonances().at(0).LV());
				product.m_simpleFitTausPrefitResolvedGen[oneProng] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getInitTauMus().at(0).LV());
				product.m_simpleFitTausPrefitResolvedGen[a1] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getInitTauHs().at(0).LV());
				// LOG(INFO) << "m_simpleFitResonancePrefitResolvedGen: (px,py,pz,M)=(" << product.m_simpleFitResonancePrefitResolvedGen.px() << "," << product.m_simpleFitResonancePrefitResolvedGen.py() << "," << product.m_simpleFitResonancePrefitResolvedGen.pz() << "," << product.m_simpleFitResonancePrefitResolvedGen.M() << ")";
				// LOG(INFO) << "m_simpleFitTausPrefitResolvedGen[oneProng]: (px,py,pz,M)=(" << product.m_simpleFitTausPrefitResolvedGen[oneProng].px() << "," << product.m_simpleFitTausPrefitResolvedGen[oneProng].py() << "," << product.m_simpleFitTausPrefitResolvedGen[oneProng].pz() << "," << product.m_simpleFitTausPrefitResolvedGen[oneProng].M() << ")";
				// LOG(INFO) << "m_simpleFitTausPrefitResolvedGen[a1]: (px,py,pz,M)=(" << product.m_simpleFitTausPrefitResolvedGen[a1].px() << "," << product.m_simpleFitTausPrefitResolvedGen[a1].py() << "," << product.m_simpleFitTausPrefitResolvedGen[a1].pz() << "," << product.m_simpleFitTausPrefitResolvedGen[a1].M() << ")";
			}
		}
		if (fitResult.isValid())
		{
			product.m_simpleFitTaus[oneProng] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getTauMu().LV());
			product.m_simpleFitTaus[a1] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getTauH().LV());
			product.m_diTauSystemSimpleFit = product.m_simpleFitTaus[oneProng] + product.m_simpleFitTaus[a1];
			// RMFLV resonance = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getResonance().LV());
			product.m_simpleFitChi2Sum = fitResult.getChi2();
			product.m_simpleFitCsum = fitResult.getCsum();
			product.m_simpleFitNiterations = fitResult.getNiterations();
			product.m_simpleFitResonancePrefitResolvedFit = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getInitResonance().LV());
			product.m_simpleFitTausPrefitResolvedFit[oneProng] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getInitTauMu().LV());
			product.m_simpleFitTausPrefitResolvedFit[a1] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getInitTauH().LV());
			product.m_simpleFitIndex = fitResult.getIndex();
			product.m_simpleFitConverged = fitResult.Fitconverged();
			// m_chi2 = fitResult.getChi2Vectors().at(fitResult.getIndex());
			TVectorD chi2vec(fitResult.getChi2Vector());
			for (int chi2index = 0; chi2index < chi2vec.GetNrows(); chi2index++) {
				product.m_simpleFitChi2.push_back(chi2vec[chi2index]);
			}
			if(product.m_simpleFitTauRecoIsAmbiguous)
			{
				product.m_simpleFitTausResolvedGen[oneProng] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getTauMus().at(product.m_genSimpleFitIndexMap[a1]).LV());
				product.m_simpleFitTausResolvedGen[a1] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getTauHs().at(product.m_genSimpleFitIndexMap[a1]).LV());
			}
			else
			{
				product.m_simpleFitTausResolvedGen[oneProng] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getTauMu().LV());
				product.m_simpleFitTausResolvedGen[a1] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getTauH().LV());
			}
			// LOG(INFO) << "tauToOneProng: " << product.m_simpleFitTaus[oneProng];
			// LOG(INFO) << "tauToA1: " << product.m_simpleFitTaus[a1];
			// LOG(INFO) << "resonance: " << product.m_diTauSystemSimpleFit;
			// LOG(INFO) << "resonance: " << resonance;
		}
	}
}


void SimpleFitThreeProngThreeProngProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	SimpleFitProducer::Init(settings, metadata);

	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "simpleFitTau1RecoIsAmbiguous", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_simpleFitTau1RecoIsAmbiguous;
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitTau1PrefitPlusLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_simpleFitTau1PrefitPlus;
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitTau1PrefitMinusLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_simpleFitTau1PrefitMinus;
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitTau1PrefitZeroLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_simpleFitTau1PrefitZero;
	});

	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "simpleFitTau2RecoIsAmbiguous", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_simpleFitTau2RecoIsAmbiguous;
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitTau2PrefitPlusLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_simpleFitTau2PrefitPlus;
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitTau2PrefitMinusLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_simpleFitTau2PrefitMinus;
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "simpleFitTau2PrefitZeroLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_simpleFitTau2PrefitZero;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "simpleFitTau1RotationSignificance", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_simpleFitTau1RotationSignificance;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "simpleFitTau2RotationSignificance", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_simpleFitTau2RotationSignificance;
	});

}

void SimpleFitThreeProngThreeProngProducer::Produce(event_type const& event, product_type& product,
                                setting_type const& settings, metadata_type const& metadata) const
{
	assert(product.m_flavourOrderedLeptons.size() >= 2);
	assert(event.m_vertexSummary); // TODO: change to refitted PV

	bool twoThreeprongs(true);

	// LOG(INFO) << "SimpleFitProducer: START";

	for (std::vector<KLepton*>::iterator leptonIt = product.m_flavourOrderedLeptons.begin();
	     leptonIt != product.m_flavourOrderedLeptons.end(); ++leptonIt)
	{
		if ((*leptonIt)->flavour() == KLeptonFlavour::TAU)
		{
			KTau* tau = static_cast<KTau*>(*leptonIt);
			int decaymode = m_useMVADecayModes ? (int)tau->getDiscriminator("MVADM2017v1", event.m_tauMetadata) : tau->decayMode;
			// LOG(INFO) << "tau->sv.valid: " << tau->sv.valid;

			if (!((decaymode == reco::PFTau::hadronicDecayMode::kThreeProng0PiZero) &&
			    (tau->chargedHadronCandidates.size() > 2) &&
			    tau->sv.valid))
			{
				twoThreeprongs = false;
			}
		}
	}

	if (twoThreeprongs)
	{
		// tau 1
		unsigned int nLorentzAndVertexParameters = TrackHelixVertexFitter::NFreeTrackPar+TrackHelixVertexFitter::NExtraPar+TrackHelixVertexFitter::MassOffSet; // LorentzVectorParticle::NLorentzandVertexPar
		TMatrixT<double> tauOneParameters(nLorentzAndVertexParameters, 1);
		TMatrixTSym<double> tauOneCovariance(nLorentzAndVertexParameters);
		KTau* tauOne = static_cast<KTau*>(product.m_flavourOrderedLeptons.at(0));
		for (int parameterIndex1 = 0; parameterIndex1 < 7; ++parameterIndex1)
		{
			tauOneParameters[parameterIndex1][0] = tauOne->refittedThreeProngParameters[parameterIndex1];
			for (int parameterIndex2 = 0; parameterIndex2 < 7; ++parameterIndex2)
			{
				tauOneCovariance[parameterIndex1][parameterIndex2] = tauOne->refittedThreeProngCovariance[parameterIndex1][parameterIndex2];
			}
		}
		tauOneParameters[TrackHelixVertexFitter::NFreeTrackPar+TrackHelixVertexFitter::BField0 + 1][0] = tauOne->track.magneticField; // was off by 1 and overwrote the a1 mass
		TMatrixT<double> tauOneParametersInput = SimpleFitProducer::ComputeLorentzVectorPar(tauOneParameters);
		TMatrixTSym<double> tauOneCovarianceInput = ErrorMatrixPropagator::PropagateError(&SimpleFitProducer::ComputeLorentzVectorPar, tauOneParameters, tauOneCovariance);

		// LOG(WARNING) << "\n\nSimpleFits inputs (a1):";
		// LOG(INFO) << "\ntauOneParameters:";
		// tauOneParameters.Print();
		// LOG(INFO) << "\ntauOneCovariance:";
		// tauOneCovariance.Print();
		// LOG(INFO) << "\ntauOneParametersInput:";
		// tauOneParametersInput.Print();
		// LOG(INFO) << "\ntauOneCovarianceInput:";
		// tauOneCovarianceInput.Print();
		// LOG(INFO) << "\na1->pdgId(): " << a1->pdgId();
		// LOG(INFO) << "a1->charge(): " << a1->charge();
		// LOG(INFO) << "a1->track.magneticField: " << a1->track.magneticField;

		LorentzVectorParticle tauOneInput(tauOneParametersInput, tauOneCovarianceInput, tauOne->resonancePdgId(), tauOne->charge(), tauOne->track.magneticField);

		// LOG(INFO) << "LVP px: " << tauOneInput.LV().Px();
		// LOG(INFO) << "LVP py: " << tauOneInput.LV().Py();
		// LOG(INFO) << "LVP pz: " << tauOneInput.LV().Pz();
		// LOG(INFO) << "LVP pt: " << tauOneInput.LV().Pt();
		// LOG(INFO) << "LVP svx: " << tauOneInput.Vertex().X();
		// LOG(INFO) << "LVP svy: " << tauOneInput.Vertex().Y();
		// LOG(INFO) << "LVP svz: " << tauOneInput.Vertex().Z();

		// tau 2
		// https://github.com/cherepan/LLRHiggsTauTau/blob/VladimirDev/NtupleProducer/plugins/TauFiller.cc#L483
		// https://github.com/cherepan/LLRHiggsTauTau/blob/VladimirDev/NtupleProducer/plugins/TauFiller.cc#L464
		// https://github.com/cherepan/LLRHiggsTauTau/blob/VladimirDev/NtupleProducer/src/ParticleBuilder.cc#L11-L40
		TMatrixT<double> tauTwoParameters(nLorentzAndVertexParameters, 1);
		TMatrixTSym<double> tauTwoCovariance(nLorentzAndVertexParameters);
		KTau* tauTwo = static_cast<KTau*>(product.m_flavourOrderedLeptons.at(1));
		for (int parameterIndex1 = 0; parameterIndex1 < 7; ++parameterIndex1)
		{
			tauTwoParameters[parameterIndex1][0] = tauTwo->refittedThreeProngParameters[parameterIndex1];
			for (int parameterIndex2 = 0; parameterIndex2 < 7; ++parameterIndex2)
			{
				tauTwoCovariance[parameterIndex1][parameterIndex2] = tauTwo->refittedThreeProngCovariance[parameterIndex1][parameterIndex2];
			}
		}
		tauTwoParameters[TrackHelixVertexFitter::NFreeTrackPar+TrackHelixVertexFitter::BField0 + 1][0] = tauTwo->track.magneticField; // was off by 1 and overwrote the a1 mass
		TMatrixT<double> tauTwoParametersInput = SimpleFitProducer::ComputeLorentzVectorPar(tauTwoParameters);
		TMatrixTSym<double> tauTwoCovarianceInput = ErrorMatrixPropagator::PropagateError(&SimpleFitProducer::ComputeLorentzVectorPar, tauTwoParameters, tauTwoCovariance);

		// LOG(WARNING) << "\n\nSimpleFits inputs (a1):";
		// LOG(INFO) << "\ntauTwoParameters:";
		// tauTwoParameters.Print();
		// LOG(INFO) << "\ntauTwoCovariance:";
		// tauTwoCovariance.Print();
		// LOG(INFO) << "\ntauTwoParametersInput:";
		// tauTwoParametersInput.Print();
		// LOG(INFO) << "\ntauTwoCovarianceInput:";
		// tauTwoCovarianceInput.Print();
		// LOG(INFO) << "\na1->pdgId(): " << a1->pdgId();
		// LOG(INFO) << "a1->charge(): " << a1->charge();
		// LOG(INFO) << "a1->track.magneticField: " << a1->track.magneticField;

		LorentzVectorParticle tauTwoInput(tauTwoParametersInput, tauTwoCovarianceInput, tauTwo->resonancePdgId(), tauTwo->charge(), tauTwo->track.magneticField);
		std::vector<LorentzVectorParticle> tauInputs {tauOneInput, tauTwoInput};
		// LOG(INFO) << "LVP px: " << tauTwoInput.LV().Px();
		// LOG(INFO) << "LVP py: " << tauTwoInput.LV().Py();
		// LOG(INFO) << "LVP pz: " << tauTwoInput.LV().Pz();
		// LOG(INFO) << "LVP pt: " << tauTwoInput.LV().Pt();
		// LOG(INFO) << "LVP svx: " << tauTwoInput.Vertex().X();
		// LOG(INFO) << "LVP svy: " << tauTwoInput.Vertex().Y();
		// LOG(INFO) << "LVP svz: " << tauTwoInput.Vertex().Z();

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
		// KVertex* pv = (product.m_refitPV ? product.m_refitPV : &(event.m_vertexSummary->pv));
		KVertex* pv = (product.m_refitPVBS ? product.m_refitPVBS : &(event.m_vertexSummary->pv));
		TVector3 pvInput = Utility::ConvertPxPyPzVector<RMPoint, TVector3>(pv->position);
		TMatrixTSym<double> pvCovarianceInput = Utility::ConvertMatrixSym<ROOT::Math::SMatrix<double, 3, 3, ROOT::Math::MatRepSym<double, 3> >, TMatrixTSym<double> >(pv->covariance, 3);

		// LOG(WARNING) << "\nSimpleFits inputs (PV):";
		// LOG(INFO) << "\npvInput:";
		// pvInput.Print();
		// LOG(INFO) << "\npvCovarianceInput:";
		// pvCovarianceInput.Print();

		// Fit
		GlobalEventFit globalEventFit(tauInputs, metInput, pvInput, pvCovarianceInput);
		if (m_massConstraint > 0) globalEventFit.setMassConstraint(m_massConstraint);
		globalEventFit.setMinimizer(LagrangeMultipliersFitter::FittingProc::Standard);
		globalEventFit.setUseCollinearityTauMu(m_useCollinearityTauMu);
		std::vector<TPTRObject> tauReco = globalEventFit.getTPTRObjects();
		GEFObject fitResult = globalEventFit.Fit();
		product.m_simpleFitTau1RecoIsAmbiguous = tauReco.at(0).isAmbiguous();
		product.m_simpleFitTau2RecoIsAmbiguous = tauReco.at(1).isAmbiguous();
		// LOG(INFO) << "product.m_simpleFitTau1RecoIsAmbiguous: " << product.m_simpleFitTau1RecoIsAmbiguous;
		// LOG(INFO) << "product.m_simpleFitTau2RecoIsAmbiguous: " << product.m_simpleFitTau2RecoIsAmbiguous;
		if (product.m_simpleFitTau1RecoIsAmbiguous)
		{
			product.m_simpleFitTauA1PrefitPlus = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(tauReco.at(0).getTauPlus().LV());
			product.m_simpleFitTauA1PrefitMinus = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(tauReco.at(0).getTauMinus().LV());
			product.m_simpleFitTau1PrefitPlus = product.m_simpleFitTauA1PrefitPlus;
			product.m_simpleFitTau1PrefitMinus = product.m_simpleFitTauA1PrefitMinus;
			// LOG(INFO) << "tauReco.at(0).getTauPlus().LV(): (px,py,pz,M)=(" << product.m_simpleFitTauA1PrefitPlus.px() << "," << product.m_simpleFitTauA1PrefitPlus.py() << "," << product.m_simpleFitTauA1PrefitPlus.pz() << "," << product.m_simpleFitTauA1PrefitPlus.M() << ")";
			// LOG(INFO) << "tauReco.at(0).getTauMinus().LV(): (px,py,pz,M)=(" << product.m_simpleFitTauA1PrefitMinus.px() << "," << product.m_simpleFitTauA1PrefitMinus.py() << "," << product.m_simpleFitTauA1PrefitMinus.pz() << "," << product.m_simpleFitTauA1PrefitMinus.M() << ")";
		}
		else
		{
			product.m_simpleFitTauA1PrefitZero = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(tauReco.at(0).getTauZero().LV());
			product.m_simpleFitTau1PrefitZero = product.m_simpleFitTauA1PrefitZero;
			product.m_simpleFitRotationSignificance = tauReco.at(0).getRotationSignificance();
			product.m_simpleFitTau1RotationSignificance = product.m_simpleFitRotationSignificance;
			// LOG(INFO) << "tauReco.getTauZero().LV(): (px,py,pz,M)=(" << product.m_simpleFitTauA1PrefitZero.px() << "," << product.m_simpleFitTauA1PrefitZero.py() << "," << product.m_simpleFitTauA1PrefitZero.pz() << "," << product.m_simpleFitTauA1PrefitZero.M() << ")";
			// LOG(INFO) << "product.m_simpleFitRotationSignificance: " << product.m_simpleFitTau1RotationSignificance;
		}
		if (product.m_simpleFitTau2RecoIsAmbiguous)
		{
			product.m_simpleFitTau2PrefitPlus = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(tauReco.at(1).getTauPlus().LV());
			product.m_simpleFitTau2PrefitMinus = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(tauReco.at(1).getTauMinus().LV());
			// LOG(INFO) << "tauReco.at(1).getTauPlus().LV(): (px,py,pz,M)=(" << product.m_simpleFitTau2PrefitPlus.px() << "," << product.m_simpleFitTau2PrefitPlus.py() << "," << product.m_simpleFitTau2PrefitPlus.pz() << "," << product.m_simpleFitTau2PrefitPlus.M() << ")";
			// LOG(INFO) << "tauReco.at(1).getTauMinus().LV(): (px,py,pz,M)=(" << product.m_simpleFitTau2PrefitMinus.px() << "," << product.m_simpleFitTau2PrefitMinus.py() << "," << product.m_simpleFitTau2PrefitMinus.pz() << "," << product.m_simpleFitTau2PrefitMinus.M() << ")";
		}
		else
		{
			product.m_simpleFitTau2PrefitZero = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(tauReco.at(1).getTauZero().LV());
			product.m_simpleFitTau2RotationSignificance = tauReco.at(1).getRotationSignificance();
			// LOG(INFO) << "tauReco.getTauZero().LV(): (px,py,pz,M)=(" << product.m_simpleFitTau2PrefitZero.px() << "," << product.m_simpleFitTau2PrefitZero.py() << "," << product.m_simpleFitTau2PrefitZero.pz() << "," << product.m_simpleFitTau2PrefitZero.M() << ")";
			// LOG(INFO) << "product.m_simpleFitRotationSignificance: " << product.m_simpleFitTau2RotationSignificance;
		}
		// LOG(INFO) << "\n\nSimpleFits outputs:";
		// LOG(INFO) << "fitResult.isValid(): " << fitResult.isValid();
		// LOG(INFO) << "genSimpleFitIndex1: " << product.m_genSimpleFitIndex1;
		// LOG(INFO) << "genSimpleFitIndex2: " << product.m_genSimpleFitIndex2;
		int genSimpleFitIndex1(DefaultValues::UndefinedInt), genSimpleFitIndex2(DefaultValues::UndefinedInt), genSimpleFitIndex(DefaultValues::UndefinedInt);
		if(product.m_genSimpleFitIndex1 != DefaultValues::UndefinedInt && product.m_genSimpleFitIndex2 != DefaultValues::UndefinedInt)
		{
			// for (size_t i = 0; i < fitResult.getInitTauHs().size(); i++)
			// {
				// fitResult.getInitTauHs().at(i).LV().Print();
				// fitResult.getInitTauMus().at(i).LV().Print();
			// }
			// fitResult.getInitTauHs().at(0).LV().Print();
			// fitResult.getInitTauMus().at(0).LV().Print();
			// fitResult.getInitTauHs().at(1).LV().Print();
			// fitResult.getInitTauMus().at(1).LV().Print();
			// fitResult.getInitTauHs().at(2).LV().Print();
			// fitResult.getInitTauMus().at(2).LV().Print();
			genSimpleFitIndex1 = product.m_simpleFitTau1RecoIsAmbiguous ? product.m_genSimpleFitIndex1 : 0;
			genSimpleFitIndex2 = product.m_simpleFitTau2RecoIsAmbiguous ? product.m_genSimpleFitIndex2 : 0;
			genSimpleFitIndex = genSimpleFitIndex1*3 + genSimpleFitIndex2;

			product.m_simpleFitResonancePrefitResolvedGen = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getInitResonances().at(genSimpleFitIndex).LV());
			product.m_simpleFitTausPrefitResolvedGen[product.m_flavourOrderedLeptons.at(0)] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getInitTauMus().at(genSimpleFitIndex).LV());
			product.m_simpleFitTausPrefitResolvedGen[product.m_flavourOrderedLeptons.at(1)] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getInitTauHs().at(genSimpleFitIndex).LV());
			// LOG(INFO) << "genSimpleFitIndex1: " << genSimpleFitIndex1;
			// LOG(INFO) << "genSimpleFitIndex2: " << genSimpleFitIndex2;
			// LOG(INFO) << "genSimpleFitIndex: " << genSimpleFitIndex;
			// LOG(INFO) << "m_simpleFitResonancePrefitResolvedGen: (px,py,pz,M)=(" << product.m_simpleFitResonancePrefitResolvedGen.px() << "," << product.m_simpleFitResonancePrefitResolvedGen.py() << "," << product.m_simpleFitResonancePrefitResolvedGen.pz() << "," << product.m_simpleFitResonancePrefitResolvedGen.M() << ")";
			// LOG(INFO) << "product.m_simpleFitTausPrefitResolvedGen[product.m_flavourOrderedLeptons.at(0)]: (px,py,pz,M)=(" << product.m_simpleFitTausPrefitResolvedGen[product.m_flavourOrderedLeptons.at(0)].px() << "," << product.m_simpleFitTausPrefitResolvedGen[product.m_flavourOrderedLeptons.at(0)].py() << "," << product.m_simpleFitTausPrefitResolvedGen[product.m_flavourOrderedLeptons.at(0)].pz() << "," << product.m_simpleFitTausPrefitResolvedGen[product.m_flavourOrderedLeptons.at(0)].M() << ")";
			// LOG(INFO) << "product.m_simpleFitTausPrefitResolvedGen[product.m_flavourOrderedLeptons.at(1)]: (px,py,pz,M)=(" << product.m_simpleFitTausPrefitResolvedGen[product.m_flavourOrderedLeptons.at(1)].px() << "," << product.m_simpleFitTausPrefitResolvedGen[product.m_flavourOrderedLeptons.at(1)].py() << "," << product.m_simpleFitTausPrefitResolvedGen[product.m_flavourOrderedLeptons.at(1)].pz() << "," << product.m_simpleFitTausPrefitResolvedGen[product.m_flavourOrderedLeptons.at(1)].M() << ")";
		}
		if (fitResult.isValid())
		{
			product.m_simpleFitTaus[product.m_flavourOrderedLeptons.at(0)] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getTaus().at(0).LV());
			product.m_simpleFitTaus[product.m_flavourOrderedLeptons.at(1)] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getTaus().at(1).LV());
			product.m_diTauSystemSimpleFit = product.m_simpleFitTaus[product.m_flavourOrderedLeptons.at(0)] + product.m_simpleFitTaus[product.m_flavourOrderedLeptons.at(1)];
			// RMFLV resonance = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getResonance().LV());
			product.m_simpleFitChi2Sum = fitResult.getChi2();
			product.m_simpleFitCsum = fitResult.getCsum();
			product.m_simpleFitNiterations = fitResult.getNiterations();
			product.m_simpleFitResonancePrefitResolvedFit = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getInitResonance().LV());
			product.m_simpleFitTausPrefitResolvedFit[product.m_flavourOrderedLeptons.at(0)] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getInitTauMu().LV());
			product.m_simpleFitTausPrefitResolvedFit[product.m_flavourOrderedLeptons.at(1)] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getInitTauH().LV());
			product.m_simpleFitIndex = fitResult.getIndex();
			product.m_simpleFitConverged = fitResult.Fitconverged();
			// m_chi2 = fitResult.getChi2Vectors().at(fitResult.getIndex());
			TVectorD chi2vec(fitResult.getChi2Vector());
			for (int chi2index = 0; chi2index < chi2vec.GetNrows(); chi2index++) {
				product.m_simpleFitChi2.push_back(chi2vec[chi2index]);
			}
			if(genSimpleFitIndex != DefaultValues::UndefinedInt)
			{
				product.m_simpleFitTausResolvedGen[product.m_flavourOrderedLeptons.at(0)] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getTauMus().at(genSimpleFitIndex).LV());
				product.m_simpleFitTausResolvedGen[product.m_flavourOrderedLeptons.at(1)] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getTauHs().at(genSimpleFitIndex).LV());
			}
			// LOG(INFO) << "tauOne: " << product.m_simpleFitTaus[product.m_flavourOrderedLeptons.at(0)];
			// LOG(INFO) << "tauTwo: " << product.m_simpleFitTaus[product.m_flavourOrderedLeptons.at(1)];
			// LOG(INFO) << "resonance: " << product.m_diTauSystemSimpleFit;
		}
	}
}



TMatrixT<double> SimpleFitProducer::ComputeLorentzVectorPar(TMatrixT<double> &inpar){
  TMatrixT<double> LV(LorentzVectorParticle::NLorentzandVertexPar,1);
	LV(LorentzVectorParticle::vx,0)=inpar[0][0];
	LV(LorentzVectorParticle::vy,0)=inpar[1][0];
	LV(LorentzVectorParticle::vz,0)=inpar[2][0];
  LV(LorentzVectorParticle::px,0)=inpar[3][0];
  LV(LorentzVectorParticle::py,0)=inpar[4][0];
  LV(LorentzVectorParticle::pz,0)=inpar[5][0];
  LV(LorentzVectorParticle::m,0) =inpar[6][0];
  return LV;
}
