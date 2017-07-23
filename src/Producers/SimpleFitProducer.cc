
#include <algorithm>
#include <math.h>

#include "DataFormats/TauReco/interface/PFTau.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/SimpleFitProducer.h"

#include "SimpleFits/FitSoftware/interface/ErrorMatrixPropagator.h"
#include "SimpleFits/FitSoftware/interface/GlobalEventFit.h"
#include "SimpleFits/FitSoftware/interface/LorentzVectorParticle.h"
#include "SimpleFits/FitSoftware/interface/TrackHelixVertexFitter.h"
#include "SimpleFits/FitSoftware/interface/PTObject.h"
//#include "SimpleFits/FitSoftware/interface/GEFObject.h"


void SimpleFitProducer::Init(setting_type const& settings)
{
    ProducerBase<HttTypes>::Init(settings);
}


void SimpleFitProducer::Produce(event_type const& event, product_type& product,
                                setting_type const& settings) const
{
	assert(product.m_flavourOrderedLeptons.size() >= 2);
	assert(event.m_vertexSummary); // TODO: change to refitted PV
	
	KMuon* muon = nullptr;
	KTau* tauToA1 = nullptr;
	
	for (std::vector<KLepton*>::iterator lepton = product.m_flavourOrderedLeptons.begin();
	     lepton != product.m_flavourOrderedLeptons.end(); ++lepton)
	{
		if ((! muon) && ((*lepton)->flavour() == KLeptonFlavour::MUON))
		{
			muon = static_cast<KMuon*>(*lepton);
		}
		else if ((! tauToA1) && ((*lepton)->flavour() == KLeptonFlavour::TAU))
		{
			KTau* tau = static_cast<KTau*>(*lepton);
			// https://github.com/cms-sw/cmssw/blob/09c3fce6626f70fd04223e7dacebf0b485f73f54/DataFormats/TauReco/interface/PFTau.h#L34-L54
			if ((tau->decayMode >= reco::PFTau::hadronicDecayMode::kThreeProng0PiZero) &&
			    (tau->chargedHadronCandidates.size() > 2) &&
			    tau->sv.valid)
			{
				tauToA1 = tau;
			}
		}
	}
	
	if ((muon != nullptr) && (tauToA1 != nullptr))
	{
		// muon
		std::vector<float> muonHelixParameters = muon->globalTrack.helixParameters();
		TMatrixT<double> muonHelixParametersInput(TrackParticle::NHelixPar, 1);
		for (unsigned int parameterIndex1 = 0; parameterIndex1 < TrackParticle::NHelixPar; ++parameterIndex1)
		{
			muonHelixParametersInput[parameterIndex1][0] = muonHelixParameters[parameterIndex1];
		}
		TMatrixTSym<double> muonHelixCovarianceInput = Utility::ConvertMatrixSym<ROOT::Math::SMatrix<float, reco::Track::dimension, reco::Track::dimension, ROOT::Math::MatRepSym<float, reco::Track::dimension> >, TMatrixTSym<double> >(muon->globalTrack.helixCovariance, TrackParticle::NHelixPar);
		int pdgIdMuon = static_cast<int>(DefaultValues::pdgIdMuon * muon->charge() / std::abs(muon->charge()));
		TrackParticle muonInput(muonHelixParametersInput, muonHelixCovarianceInput, pdgIdMuon, muon->p4.mass(), muon->charge(), muon->globalTrack.magneticField);
		
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
		LOG(INFO) << &globalEventFit;
	}

	int muonPdgid = 0;
	double muonMass = 0; 
	double muonCharge = 0;
	double muonB = 0;

	// Muon Track Properties
	TMatrixT<double> muonPar(TrackParticle::NHelixPar,1);
	double pt;
	double pz;

	TMatrixTSym<double> muonCov(TrackParticle::NHelixPar);

	bool muonFound = false;
	bool tauFound = false;

	for (std::vector<KLepton*>::iterator lepton = product.m_flavourOrderedLeptons.begin();
	     lepton != product.m_flavourOrderedLeptons.end(); ++lepton)
	{
		if (! muonFound)
		{
			if ((*lepton)->flavour() == KLeptonFlavour::MUON)
			{
				//LOG(INFO) << "Type of Lepton: "<< (*lepton)->flavour()  << " Is it a muon: " << KLeptonFlavour::MUON << ", or electron: "<< KLeptonFlavour::ELECTRON << ", or tau: "<< KLeptonFlavour::TAU ;
				muonFound = true;
				//LOG(INFO) << "This is a MUON!.. " << "TrackParticle::NHelixPar: "<<  TrackParticle::NHelixPar << " LorentzVectorParticle::NLorentzandVertexPar: " << LorentzVectorParticle::NLorentzandVertexPar ;

				//LOG(INFO) << "Inside leptons list if it is MUON: " << product.m_flavourOrderedLeptons[0]->p4.mass() << ", and: "<< product.m_flavourOrderedLeptons[1]->p4.mass() ;
				muonPdgid = 13;
				muonMass = (*lepton)->p4.mass(); //0.105; //GeV
				muonCharge = (*lepton)->charge();
				muonB = 1; 

				// Muon Track Properties
				pt = (*lepton)->p4.Pt();
				pz = (*lepton)->p4.Pz();
				muonPar[0] = muonCharge/pt;   // kappa
				muonPar[1] = std::atan(pz/pt);   // lambda
				muonPar[2] = (*lepton)->p4.Phi(); // phi
				muonPar[3] = (*lepton)->track.getDz(&event.m_vertexSummary->pv);   // dz
				muonPar[4] = (*lepton)->track.getDxy(&event.m_vertexSummary->pv);    // dxy


				muonCov[0][0] = 0.5;
				muonCov[0][1] = 0.5;
				muonCov[0][2] = 0.5;
				muonCov[0][3] = 0.5;
				muonCov[0][4] = 0.5;

				muonCov[1][1] = 0.5;
				muonCov[1][2] = 0.5;
				muonCov[1][3] = 0.5;
				muonCov[1][4] = 0.5;

				muonCov[2][2] = 0.5;
				muonCov[2][3] = 0.5;
				muonCov[2][4] = 0.5;

				muonCov[3][3] = (*lepton)->track.errDxy();
				muonCov[3][4] = (*lepton)->track.errDxy();

				muonCov[4][4] = 0.5;
			}
		}
	}

	//LOG(INFO) <<  "muonMass: " << muonMass ;
	TMatrixT<double> tauhPar(LorentzVectorParticle::NLorentzandVertexPar,1);
	TMatrixTSym<double> tauhCov(LorentzVectorParticle::NLorentzandVertexPar);
	int tauhPdgid = 0;
	double tauhCharge = 0;
	double tauhB = 0;

	for (std::vector<KTau*>::iterator tau = product.m_validTaus.begin(); tau != product.m_validTaus.end(); ++tau)
	{
		if (! tauFound)
		{
			//LOG(INFO) << "NchargedPart: "<< (*tau)->chargedHadronCandidates.size() << ", decaymode: " << (*tau)->decayMode;
			if (((*tau)->decayMode >= reco::PFTau::hadronicDecayMode::kThreeProng0PiZero) &&
			    ((*tau)->chargedHadronCandidates.size() > 2))
			{
				// a1(3 prong pion) Vector Particle Properties *** for now it includes all hadronic decay products
				tauFound = true;
				tauhPar[0] = (*tau)->p4.Px(); // px
				tauhPar[1] = (*tau)->p4.Py(); // py
				tauhPar[2] = (*tau)->p4.Pz();  // pz
				tauhPar[3] = (*tau)->p4.mass();  // m
				tauhPar[4] = (*tau)->p4.x();  // vx   #TODO this is momentums
				tauhPar[5] = (*tau)->p4.y();  // vy
				tauhPar[6] = (*tau)->p4.z();  // vz

				//sLOG(INFO) << "tau_vx " <<  product.m_flavourOrderedLeptons[0]->vertex.x(); << ", tau_px:" << product.m_flavourOrderedLeptons[0]->p4.Px() << std::endl;

				tauhCov[0][0] = (*tau)->track.errDxy(); //0.5;
				tauhCov[0][1] = 0.5;
				tauhCov[0][2] = 0.5;
				tauhCov[0][3] = 0.5;
				tauhCov[0][4] = 0.5;
				tauhCov[0][5] = 0.5;
				tauhCov[0][6] = 0.5;
				tauhCov[1][1] = 0.5;
				tauhCov[1][2] = 0.5;
				tauhCov[1][3] = 0.5;
				tauhCov[1][4] = 0.5;
				tauhCov[1][5] = 0.5;
				tauhCov[1][6] = 0.5;
				tauhCov[2][2] = 0.5;
				tauhCov[2][3] = 0.5;
				tauhCov[2][4] = 0.5;
				tauhCov[2][5] = 0.5;
				tauhCov[2][6] = 0.5;
				tauhCov[3][3] = 0.5;
				tauhCov[3][4] = 0.5;
				tauhCov[3][5] = 0.5;
				tauhCov[3][6] = 0.5;
				tauhCov[4][4] = 0.5;
				tauhCov[4][5] = 0.5;
				tauhCov[4][6] = 0.5;

				// LOG(INFO) << "tracK_Dxy " <<  product.m_flavourOrderedLeptons[0]->track.getDxy(&event.m_vertexSummary->pv) << ", tracK_errDxy() " <<  product.m_flavourOrderedLeptons[0]->track.errDxy() << std::endl;
				tauhPdgid = 13;
				tauhCharge =  (*tau)->charge();
				tauhB = 1;
			}
		}
	}

	// ====== MET info =======
	TMatrixT<double> metPar(2,1);
	metPar[0] = product.m_met.p4.Px();
	metPar[1] = product.m_met.p4.Py();

	TMatrixTSym<double> metCov(2);
	metCov[0][0] = product.m_met.significance[0][0];
	metCov[0][1] = product.m_met.significance[0][1];
	metCov[1][1] = product.m_met.significance[1][1];

	// TMatrixD metCov = Utility::ConvertMatrixSym<ROOT::Math::SMatrix<double, 2, 2, ROOT::Math::MatRepSym<double, 2> >,   TMatrixTSym<double>>(product.m_met.significance, 2, 4);
	//LOG(INFO) << "MtCov: " << metCov[0][0] << std::endl;

	PTObject MET(metPar, metCov); //   // ????
	// ====== Primary Vertex Info ======
	TVector3 PV(0.5, 0.4, 0.3);  // pv->position.x()   in KTrack.h
	TMatrixTSym<double> PVCov(3);  // pv->covariance  in KTrack.h
	PVCov[0][0]= 0.5;
	PVCov[0][1]= 0.5;
	PVCov[0][2]= 0.5;
	PVCov[1][1]= 0.5;
	PVCov[1][2]= 0.5;
	PVCov[2][2]= 0.5;

	if( muonFound && tauFound)
	{
		//LOG(INFO) << "PER EVENT: this a new event with one muon and one tau_h";
		TrackParticle Muon(muonPar, muonCov, muonPdgid, muonMass, muonCharge, muonB);
		LorentzVectorParticle Tauh(tauhPar, tauhCov, tauhPdgid, tauhCharge, tauhB);
		GlobalEventFit SimpleFit(Muon, Tauh,  MET,  PV, PVCov);
		//GlobalEventFit::GlobalEventFit(TrackParticle Muon, LorentzVectorParticle A1, double Phi_Res, TVector3 PV, TMatrixTSym<double> PVCov){  }
		// GlobalEventFit::GlobalEventFit(TrackParticle Muon, LorentzVectorParticle A1, PTObject MET, TVector3 PV, TMatrixTSym<double> PVCov){  }

		GEFObject GEF = SimpleFit.Fit();
		if( GEF.isValid() )
		{
			//TLorentzVector EventFitTauA1 =GEF.getTauH().LV();
			//product.m_simpleFitTaus[product.m_flavourOrderedLeptons[0]] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(GEF.getTauH().LV());
			product.m_simpleFitTaus[product.m_flavourOrderedLeptons[1]] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(GEF.getTauH().LV());
			//LOG(INFO) << " I am hereQ" << GEF.getTauH().LV().M() << "  " << product.m_simpleFitTaus[product.m_flavourOrderedLeptons[0]].M();
			//LOG(INFO) << "Fit is valid and implemented\n\n" ;
		}
	}
}

