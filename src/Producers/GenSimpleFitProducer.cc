
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
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/GenSimpleFitProducer.h"

#include "TauPolSoftware/SimpleFits/interface/ErrorMatrixPropagator.h"
#include "TauPolSoftware/SimpleFits/interface/TPTRObject.h"
#include "TauPolSoftware/SimpleFits/interface/GEFObject.h"
#include "TauPolSoftware/SimpleFits/interface/GlobalEventFit.h"
#include "TauPolSoftware/SimpleFits/interface/LorentzVectorParticle.h"
#include "TauPolSoftware/SimpleFits/interface/TrackHelixVertexFitter.h"
#include "TauPolSoftware/SimpleFits/interface/PTObject.h"


std::string GenSimpleFitProducer::GetProducerId() const
{
	return "GenSimpleFitProducer";
}

void GenSimpleFitProducer::Init(setting_type const& settings, metadata_type& metadata)
{
    ProducerBase<HttTypes>::Init(settings, metadata);

	// m_massConstraint = settings.GetSimpleFitMassConstraint();

	// add possible quantities for the lambda ntuples consumers

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genSimpleFitIndex1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_genSimpleFitIndex1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genSimpleFitIndex2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_genSimpleFitIndex2;
	});

	// LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "genSimpleFitTau2PrefitPlusLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	// 	return product.m_genSimpleFitTau2PrefitPlus;
	// });
	// LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "genSimpleFitTau2PrefitMinusLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	// 	return product.m_genSimpleFitTau2PrefitMinus;
	// });
	// LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "genSimpleFitTau2PrefitZeroLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	// 	return product.m_genSimpleFitTau2PrefitZero;
	// });
	// LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "genSimpleFitResonancePrefitResolvedFitLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	// 	return product.m_genSimpleFitResonancePrefitResolvedFit;
	// });
	// LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "genSimpleFitTau1PrefitResolvedFitLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	// 	return product.m_genSimpleFitTau1PrefitResolvedFit;
	// });
	// LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "genSimpleFitTau2PrefitResolvedFitLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	// 	return product.m_genSimpleFitTau2PrefitResolvedFit;
	// });
	//
	// LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genSimpleFitChi2Sum", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	// 	return product.m_genSimpleFitChi2Sum;
	// });
	// LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genSimpleFitCsum", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	// 	return product.m_genSimpleFitCsum;
	// });
	// LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "genSimpleFitNiterations", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	// 	return product.m_genSimpleFitNiterations;
	// });
	// LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "genSimpleFitIndex", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	// 	return product.m_genSimpleFitIndex;
	// });
	// LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "genSimpleFitConverged", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	// 	return product.m_genSimpleFitConverged;
	// });
	//
	// for (int chi2index = 0; chi2index < 3; chi2index++) {
	// 	std::string quantity = "simpleFitChi2_" + std::to_string(chi2index+1);
	// 	// LOG(INFO) << quantity;
	// 	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, quantity, [chi2index](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	// 		if (product.m_genSimpleFitChi2.size() > 0)
	// 		{
	// 			return product.m_genSimpleFitChi2.at(chi2index);
	// 		}
	// 		else
	// 		{
	// 			return DefaultValues::UndefinedFloat;
	// 		}
	// 	});
	// }
	//
	// LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "genSimpleFitAvailable", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	// 	return (Utility::Contains(product.m_genSimpleFitTaus, product.m_flavourOrderedLeptons.at(0)) &&
	// 	        Utility::Contains(product.m_genSimpleFitTaus, product.m_flavourOrderedLeptons.at(1)));
	// });
	// LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "genSimpleFitLV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	// 	return product.m_genDiTauSystemSimpleFit;
	// });
	//
	// LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "genSimpleFitTau1Available", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	// 	return Utility::Contains(product.m_genSimpleFitTaus, product.m_flavourOrderedLeptons.at(0));
	// });
	// LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "genSimpleFitTau1LV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	// 	return SafeMap::GetWithDefault(product.m_genSimpleFitTaus, product.m_flavourOrderedLeptons.at(0), DefaultValues::UndefinedRMFLV);
	// });
	// LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genSimpleFitTau1ERatio", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	// 	if (Utility::Contains(product.m_genSimpleFitTaus, product.m_flavourOrderedLeptons.at(0)))
	// 	{
	// 		return product.m_flavourOrderedLeptons.at(0)->p4.E() / SafeMap::Get(product.m_genSimpleFitTaus, product.m_flavourOrderedLeptons.at(0)).E();
	// 	}
	// 	else
	// 	{
	// 		return DefaultValues::UndefinedFloat;
	// 	}
	// });
	//
	// LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "genSimpleFitTau2Available", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	// 	return Utility::Contains(product.m_genSimpleFitTaus, product.m_flavourOrderedLeptons.at(1));
	// });
	// LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "genSimpleFitTau2LV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	// 	return SafeMap::GetWithDefault(product.m_genSimpleFitTaus, product.m_flavourOrderedLeptons.at(1), DefaultValues::UndefinedRMFLV);
	// });
	// LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genSimpleFitTau2ERatio", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
	// 	if (Utility::Contains(product.m_genSimpleFitTaus, product.m_flavourOrderedLeptons.at(1)))
	// 	{
	// 		return product.m_flavourOrderedLeptons.at(1)->p4.E() / SafeMap::Get(product.m_genSimpleFitTaus, product.m_flavourOrderedLeptons.at(1)).E();
	// 	}
	// 	else
	// 	{
	// 		return DefaultValues::UndefinedFloat;
	// 	}
	// });
}

void GenSimpleFitProducer::Produce(event_type const& event, product_type& product,
                                setting_type const& settings, metadata_type const& metadata) const
{
	LOG(DEBUG) << "\t\t\t DEBUG 1: product.m_flavourOrderedGenLeptons.size(): " << product.m_flavourOrderedGenLeptons.size();
	LOG(DEBUG) << "\t\t\t DEBUG 1: product.m_flavourOrderedGenLeptons.at(0): " << product.m_flavourOrderedGenLeptons.at(0);
	LOG(DEBUG) << "\t\t\t DEBUG 1: product.m_flavourOrderedGenLeptons.at(1): " << product.m_flavourOrderedGenLeptons.at(1);
	if ( product.m_flavourOrderedGenLeptons.size() > 1
		&& product.m_flavourOrderedGenLeptons.at(0) != nullptr
		&& product.m_flavourOrderedGenLeptons.at(1) != nullptr )
		{
		if ( (std::abs(product.m_flavourOrderedGenLeptons.at(0)->pdgId) == DefaultValues::pdgIdTau)
			&& (std::abs(product.m_flavourOrderedGenLeptons.at(1)->pdgId) == DefaultValues::pdgIdTau) )
		{

		// genTauDecayTree1 is the positevely charged genBosonDaughter
		// GenParticleDecayTree* genTauDecayTree1 = nullptr;
		// GenParticleDecayTree* genTauDecayTree2 = nullptr;
		// KGenTau* genTau1 = nullptr;
		// KGenTau* genTau2 = nullptr;
		LOG(DEBUG) << "\t\t\t DEBUG 1";
		KGenTau* genTau1 = static_cast<KGenTau*>(product.m_flavourOrderedGenLeptons.at(0));
		KGenTau* genTau2 = static_cast<KGenTau*>(product.m_flavourOrderedGenLeptons.at(1));
		RMFLV genLeptonVis1LV = *(product.m_flavourOrderedGenLeptonVisibleLVs.at(0));
		RMFLV genLeptonVis2LV = *(product.m_flavourOrderedGenLeptonVisibleLVs.at(1));
		LOG(DEBUG) << "\t\t\t DEBUG 2";
		// if (product.m_genBosonTree.m_daughters.at(0).m_genParticle->charge() == +1){
		// 	genTauDecayTree1 = &(product.m_genBosonTree.m_daughters.at(0));
		// 	genTauDecayTree2 = &(product.m_genBosonTree.m_daughters.at(1));
		// }
		// else {
		// 	genTauDecayTree1 = &(product.m_genBosonTree.m_daughters.at(1));
		// 	genTauDecayTree2 = &(product.m_genBosonTree.m_daughters.at(0));
		// }
		// genTau1 = SafeMap::GetWithDefault(product.m_validGenTausMap, genTauDecayTree1->m_genParticle, static_cast<KGenTau*>(nullptr));
		// genTau2 = SafeMap::GetWithDefault(product.m_validGenTausMap, genTauDecayTree2->m_genParticle, static_cast<KGenTau*>(nullptr));

		// get the full decay tree of the taus
		// genTauDecayTree1->DetermineDecayMode(genTauDecayTree1);
		// genTauDecayTree2->DetermineDecayMode(genTauDecayTree2);
		//
		// genTauDecayTree1->CreateFinalStateProngs(genTauDecayTree1);
		// genTauDecayTree2->CreateFinalStateProngs(genTauDecayTree2);
		// std::vector<GenParticleDecayTree*> genTauDecayTree1OneProngs = genTauDecayTree1->m_finalStates;
		// std::vector<GenParticleDecayTree*> genTauDecayTree2OneProngs = genTauDecayTree2->m_finalStates;


		//Creating a boost matrix into the ZMF of the taus
		RMFLV genTau1LV = genTau1->p4;
		RMFLV::BetaVector boostVecGenTau1 = genTau1LV.BoostToCM();
		ROOT::Math::Boost MgenTau1(boostVecGenTau1);

		LOG(DEBUG) << "\t\t\t DEBUG 3";

		RMFLV genTau2LV = genTau2->p4;
		RMFLV::BetaVector boostVecGenTau2 = genTau2LV.BoostToCM();
		ROOT::Math::Boost MgenTau2(boostVecGenTau2);

		LOG(DEBUG) << "\t\t\t DEBUG 4";

		//and boosting 4-vectors of visible decay products to the respective tau ZMF
		genLeptonVis1LV = MgenTau1 * genLeptonVis1LV;
		genLeptonVis2LV = MgenTau2 * genLeptonVis2LV;

		LOG(DEBUG) << "\t\t\t DEBUG 5";
		double genDot1 = genTau1LV.Vect().Dot(genLeptonVis1LV.Vect());
		double genDot2 = genTau2LV.Vect().Dot(genLeptonVis2LV.Vect());
		product.m_genSimpleFitIndex1 = genDot1 == 0 ? 0 : (genDot1 > 0 ? 1 : -1);
		product.m_genSimpleFitIndex2 = genDot2 == 0 ? 0 : (genDot2 > 0 ? 1 : -1);
		LOG(DEBUG) << "product.m_genSimpleFitIndex1: " << product.m_genSimpleFitIndex1;
		LOG(DEBUG) << "product.m_genSimpleFitIndex2: " << product.m_genSimpleFitIndex2;
	}
	//
	// assert(product.m_flavourOrderedLeptons.size() >= 2);
	// assert(event.m_vertexSummary); // TODO: change to refitted PV
	//
	// KLepton* oneProng = nullptr;
	// KTau* a1 = nullptr;
	//
	// // LOG(INFO) << "GenSimpleFitProducer: START";
	//
	// for (std::vector<KLepton*>::iterator leptonIt = product.m_flavourOrderedLeptons.begin();
	//      leptonIt != product.m_flavourOrderedLeptons.end(); ++leptonIt)
	// {
	// 	if ((*leptonIt)->flavour() == KLeptonFlavour::TAU)
	// 	{
	// 		KTau* tau = static_cast<KTau*>(*leptonIt);
	// 		// LOG(INFO) << "tau->sv.valid: " << tau->sv.valid;
	//
	// 		if ((! a1) &&
	// 		    (tau->decayMode == reco::PFTau::hadronicDecayMode::kThreeProng0PiZero) &&
	// 		    (tau->chargedHadronCandidates.size() > 2) &&
	// 		    tau->sv.valid)
	// 		{
	// 			a1 = tau;
	// 		}
	// 		else if ((! oneProng) &&
	// 		         (tau->decayMode == reco::PFTau::hadronicDecayMode::kOneProng0PiZero))
	// 		{
	// 			oneProng = *leptonIt;
	// 		}
	// 	}
	// 	else if (! oneProng)
	// 	{
	// 		oneProng = *leptonIt;
	// 	}
	// }
	//
	// if ((oneProng != nullptr) && (a1 != nullptr))
	// {
	// 	// LOG(INFO) << "Found one prong and a1";
	// 	// one prong decay
	// 	std::vector<float> oneProngHelixParameters = oneProng->track.helixParameters();
	// 	TMatrixT<double> oneProngHelixParametersInput(TrackParticle::NHelixPar, 1);
	// 	for (unsigned int parameterIndex1 = 0; parameterIndex1 < TrackParticle::NHelixPar; ++parameterIndex1)
	// 	{
	// 		oneProngHelixParametersInput[parameterIndex1][0] = oneProngHelixParameters[parameterIndex1];
	// 	}
	// 	TMatrixTSym<double> oneProngHelixCovarianceInput = Utility::ConvertMatrixSym<ROOT::Math::SMatrix<float, reco::Track::dimension, reco::Track::dimension, ROOT::Math::MatRepSym<float, reco::Track::dimension> >, TMatrixTSym<double> >(oneProng->track.helixCovariance, TrackParticle::NHelixPar);
	//
	// 	// LOG(WARNING) << "\n\nSimpleFits inputs (oneProng):";
	// 	// LOG(INFO) << "\noneProngHelixParametersInput:";
	// 	// oneProngHelixParametersInput.Print();
	// 	// LOG(INFO) << "\noneProngHelixCovarianceInput:";
	// 	// oneProngHelixCovarianceInput.Print();
	// 	// LOG(INFO) << "\noneProng->pdgId(): " << oneProng->pdgId();
	// 	// LOG(INFO) << "oneProng->p4.mass(): " << oneProng->p4.mass();
	// 	// LOG(INFO) << "oneProng->charge(): " << oneProng->charge();
	// 	TrackParticle oneProngInput(oneProngHelixParametersInput, oneProngHelixCovarianceInput, oneProng->pdgId(), oneProng->p4.mass(), oneProng->charge(), oneProng->track.magneticField);
	//
	// 	// tau
	// 	// https://github.com/cherepan/LLRHiggsTauTau/blob/VladimirDev/NtupleProducer/plugins/TauFiller.cc#L483
	// 	// https://github.com/cherepan/LLRHiggsTauTau/blob/VladimirDev/NtupleProducer/plugins/TauFiller.cc#L464
	// 	// https://github.com/cherepan/LLRHiggsTauTau/blob/VladimirDev/NtupleProducer/src/ParticleBuilder.cc#L11-L40
	// 	unsigned int nLorentzAndVertexParameters = TrackHelixVertexFitter::NFreeTrackPar+TrackHelixVertexFitter::NExtraPar+TrackHelixVertexFitter::MassOffSet; // LorentzVectorParticle::NLorentzandVertexPar
	// 	TMatrixT<double> tauParameters(nLorentzAndVertexParameters, 1);
	// 	TMatrixTSym<double> tauCovariance(nLorentzAndVertexParameters);
	// 	for (int parameterIndex1 = 0; parameterIndex1 < 7; ++parameterIndex1)
	// 	{
	// 		tauParameters[parameterIndex1][0] = a1->refittedThreeProngParameters[parameterIndex1];
	// 		for (int parameterIndex2 = 0; parameterIndex2 < 7; ++parameterIndex2)
	// 		{
	// 			tauCovariance[parameterIndex1][parameterIndex1] = a1->refittedThreeProngCovariance[parameterIndex1][parameterIndex2];
	// 		}
	// 	}
	// 	tauParameters[TrackHelixVertexFitter::NFreeTrackPar+TrackHelixVertexFitter::BField0 + 1][0] = a1->track.magneticField; // was off by 1 and overwrote the a1 mass
	// 	TMatrixT<double> tauParametersInput = SimpleFitProducer::ComputeLorentzVectorPar(tauParameters);
	// 	TMatrixTSym<double> tauCovarianceInput = ErrorMatrixPropagator::PropagateError(&SimpleFitProducer::ComputeLorentzVectorPar, tauParameters, tauCovariance);
	//
	// 	// LOG(WARNING) << "\n\nSimpleFits inputs (a1):";
	// 	// LOG(INFO) << "\ntauParameters:";
	// 	// tauParameters.Print();
	// 	// LOG(INFO) << "\ntauCovariance:";
	// 	// tauCovariance.Print();
	// 	// LOG(INFO) << "\ntauParametersInput:";
	// 	// tauParametersInput.Print();
	// 	// LOG(INFO) << "\ntauCovarianceInput:";
	// 	// tauCovarianceInput.Print();
	// 	// LOG(INFO) << "\na1->pdgId(): " << a1->pdgId();
	// 	// LOG(INFO) << "a1->charge(): " << a1->charge();
	// 	// LOG(INFO) << "a1->track.magneticField: " << a1->track.magneticField;
	//
	// 	LorentzVectorParticle tauInput(tauParametersInput, tauCovarianceInput, a1->resonancePdgId(), a1->charge(), a1->track.magneticField);
	//
	// 	// LOG(INFO) << "LVP px: " << tauInput.LV().Px();
	// 	// LOG(INFO) << "LVP py: " << tauInput.LV().Py();
	// 	// LOG(INFO) << "LVP pz: " << tauInput.LV().Pz();
	// 	// LOG(INFO) << "LVP pt: " << tauInput.LV().Pt();
	// 	// LOG(INFO) << "LVP svx: " << tauInput.Vertex().X();
	// 	// LOG(INFO) << "LVP svy: " << tauInput.Vertex().Y();
	// 	// LOG(INFO) << "LVP svz: " << tauInput.Vertex().Z();
	//
	// 	// MET
	// 	unsigned int nMetComponents = 2;
	// 	TMatrixT<double> metVector(nMetComponents, 1);
	// 	metVector[0][0] = product.m_met.p4.Vect().X();
	// 	metVector[1][0] = product.m_met.p4.Vect().Y();
	//
	// 	TMatrixTSym<double> metCovariance = Utility::ConvertMatrixSym<ROOT::Math::SMatrix<double, 2, 2, ROOT::Math::MatRepSym<double, 2> >, TMatrixTSym<double> >(product.m_met.significance, nMetComponents);
	//
	// 	// LOG(WARNING) << "\n\nSimpleFits inputs (MET):";
	// 	// LOG(INFO) << "\nmetVector:";
	// 	// metVector.Print();
	// 	// LOG(INFO) << "\nmetCovariance:";
	// 	// metCovariance.Print();
	// 	PTObject metInput(metVector, metCovariance);
	//
	// 	// PV
	// 	// KVertex* pv = (product.m_refitPV ? product.m_refitPV : &(event.m_vertexSummary->pv));
	// 	KVertex* pv = (product.m_refitPVBS ? product.m_refitPVBS : &(event.m_vertexSummary->pv));
	// 	TVector3 pvInput = Utility::ConvertPxPyPzVector<RMPoint, TVector3>(pv->position);
	// 	TMatrixTSym<double> pvCovarianceInput = Utility::ConvertMatrixSym<ROOT::Math::SMatrix<double, 3, 3, ROOT::Math::MatRepSym<double, 3> >, TMatrixTSym<double> >(pv->covariance, 3);
	//
	// 	// LOG(WARNING) << "\nSimpleFits inputs (PV):";
	// 	// LOG(INFO) << "\npvInput:";
	// 	// pvInput.Print();
	// 	// LOG(INFO) << "\npvCovarianceInput:";
	// 	// pvCovarianceInput.Print();
	//
	//
	//
	// 	// Fit
	// 	GlobalEventFit globalEventFit(oneProngInput, tauInput, metInput, pvInput, pvCovarianceInput);
	// 	globalEventFit.setMassConstraint(125.0);
	// 	// globalEventFit.setMassConstraint(m_massConstraint);
	// 	TPTRObject tauReco = globalEventFit.getTPTRObject();
	// 	GEFObject fitResult = globalEventFit.Fit();
	// 	if (tauReco.isAmbiguous())
	// 	{
	// 		product.m_genSimpleFitTau2PrefitPlus = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(tauReco.getTauPlus().LV());
	// 		product.m_genSimpleFitTau2PrefitMinus = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(tauReco.getTauMinus().LV());
	// 	}
	// 	else
	// 	{
	// 		product.m_genSimpleFitTau2PrefitZero = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(tauReco.getTauZero().LV());
	// 	}
	// 	// LOG(ERROR) << "\n\nSimpleFits outputs:";
	// 	// LOG(INFO) << "fitResult.isValid(): " << fitResult.isValid();
	// 	if (fitResult.isValid())
	// 	{
	// 		product.m_genSimpleFitTaus[oneProng] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getTauMu().LV());
	// 		product.m_genSimpleFitTaus[a1] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getTauH().LV());
	// 		product.m_genDiTauSystemSimpleFit = product.m_genSimpleFitTaus[oneProng] + product.m_genSimpleFitTaus[a1];
	// 		// RMFLV resonance = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getResonance().LV());
	// 		product.m_genSimpleFitChi2Sum = fitResult.getChi2();
	// 		product.m_genSimpleFitCsum = fitResult.getCsum();
	// 		product.m_genSimpleFitNiterations = fitResult.getNiterations();
	// 		product.m_genSimpleFitResonancePrefitResolvedFit = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getInitResonance().LV());
	// 		product.m_genSimpleFitTau1PrefitResolvedFit = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getInitTauMu().LV());
	// 		product.m_genSimpleFitTau2PrefitResolvedFit = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(fitResult.getInitTauH().LV());
	// 		product.m_genSimpleFitIndex = fitResult.getIndex();
	// 		product.m_genSimpleFitConverged = fitResult.Fitconverged();
	// 		// m_chi2 = fitResult.getChi2Vectors().at(fitResult.getIndex());
	// 		TVectorD chi2vec(fitResult.getChi2Vector());
	// 		for (int chi2index = 0; chi2index < chi2vec.GetNrows(); chi2index++) {
	// 			product.m_genSimpleFitChi2.push_back(chi2vec[chi2index]);
	// 		}
	// 		// LOG(INFO) << "tauToOneProng: " << product.m_simpleFitTaus[oneProng];
	// 		// LOG(INFO) << "tauToA1: " << product.m_simpleFitTaus[a1];
	// 		// LOG(INFO) << "resonance: " << product.m_diTauSystemSimpleFit;
	// 		// LOG(INFO) << "resonance: " << resonance;
	// 	}
	// }
	}
}
