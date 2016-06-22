
#include <algorithm>
#include <math.h>

#include <boost/format.hpp>

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/SimpleFitProducer.h"

#include "SimpleFits/FitSoftware/interface/GlobalEventFit.h"
#include "Artus/KappaAnalysis/interface/KappaProduct.h"


void SimpleFitProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
    }


void SimpleFitProducer::Produce(event_type const& event, product_type& product,
								 setting_type const& settings) const
{
	assert(event.m_eventInfo);

     	// // consider only the first two leptons
        if(product.m_flavourOrderedLeptons.size() == 2){
            //    LOG(INFO) << "I am here!.. " << "TrackParticle::NHelixPar: "<<  TrackParticle::NHelixPar << " LorentzVectorParticle::NLorentzandVertexPar: " << LorentzVectorParticle::NLorentzandVertexPar ;	

         // Muon Track Properties
            TMatrixT<double> muonPar(TrackParticle::NHelixPar,1);
        double pt = product.m_flavourOrderedLeptons[0]->p4.Pt();
        muonPar[0] = 1/pt;   // kappa
        muonPar[1] = 0.8;   // lambda
        muonPar[2] = 0.8;   // phi
        muonPar[3] = product.m_flavourOrderedLeptons[0]->track.getDz(&event.m_vertexSummary->pv);   // dz
        muonPar[4] = product.m_flavourOrderedLeptons[0]->track.getDxy(&event.m_vertexSummary->pv);    // dxy

        TMatrixTSym<double> muonCov(TrackParticle::NHelixPar);
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
        
        muonCov[3][3] = 0.5;
        muonCov[3][4] = 0.5;
        
        muonCov[4][4] = 0.5;

        int muonPdgid = 13;
        double muonMass = product.m_flavourOrderedLeptons[0]->p4.mass(); //0.105; //GeV    
        double muonCharge = product.m_flavourOrderedLeptons[0]->charge();
        double muonB = 1; 


        // a1(3 prong pion) Vector Particle Properties *** for now it includes all hadronic decay products
        TMatrixT<double> tauhPar(LorentzVectorParticle::NLorentzandVertexPar,1);
        tauhPar[0] = product.m_flavourOrderedLeptons[1]->p4.Px(); // px
        tauhPar[1] = product.m_flavourOrderedLeptons[1]->p4.Py(); // py
        tauhPar[2] = product.m_flavourOrderedLeptons[1]->p4.Pz();  // pz
        tauhPar[3] = product.m_flavourOrderedLeptons[1]->p4.mass();  // m
        tauhPar[4] = 0.8;  // vx
        tauhPar[5] = 0.8;  // vy
        tauhPar[6] = 0.8;  // vz

        TMatrixTSym<double> tauhCov(LorentzVectorParticle::NLorentzandVertexPar);
        tauhCov[0][0] = 0.5;
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

        int tauhPdgid = 13;
        double tauhCharge =  product.m_flavourOrderedLeptons[1]->charge();
        double tauhB = 1;
        

        // MET info
        TMatrixT<double> metPar(2,1);
        metPar[0] = product.m_met.p4.Px();
        metPar[1] = product.m_met.p4.Py();

        TMatrixTSym<double> metCov(2);
        metCov[0][0] = 0.3;
        metCov[0][1] = 0.4;
        metCov[1][1] = 0.5;
        
        PTObject MET(metPar, metCov); //   // ????
           
        // Primary Vertex Info
        TVector3 PV(0.5, 0.4, 0.3);
	TMatrixTSym<double> PVCov(3);
	PVCov[0][0]= 0.5;
        PVCov[0][1]= 0.5;
        PVCov[0][2]= 0.5;
        PVCov[1][1]= 0.5;
        PVCov[1][2]= 0.5;
        PVCov[2][2]= 0.5;
	
        TrackParticle Muon(muonPar, muonCov, muonPdgid, muonMass, muonCharge, muonB);
        LorentzVectorParticle Tauh(tauhPar, tauhCov, tauhPdgid, tauhCharge, tauhB);

         GlobalEventFit GF(Muon, Tauh,  MET,  PV, PVCov);
         //GlobalEventFit::GlobalEventFit(TrackParticle Muon, LorentzVectorParticle A1, double Phi_Res, TVector3 PV, TMatrixTSym<double> PVCov){  }
        // GlobalEventFit::GlobalEventFit(TrackParticle Muon, LorentzVectorParticle A1, PTObject MET, TVector3 PV, TMatrixTSym<double> PVCov){  }
         
         //  GF.Fit();
         
        }
}


