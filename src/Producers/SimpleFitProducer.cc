
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
            LOG(INFO) << "I am here!.. ";	

         // Muon Track Properties
        TMatrixT<double> muonPar;
        double pt = product.m_flavourOrderedLeptons[0]->p4.Pt();
        muonPar[0] = 1/pt;   // kappa
        muonPar[1] = 0.8;   // lambda
        muonPar[2] = 0.8;   // phi
        muonPar[3] = product.m_flavourOrderedLeptons[0]->track.getDz(&event.m_vertexSummary->pv);   // dz
        muonPar[4] =  product.m_flavourOrderedLeptons[0]->track.getDxy(&event.m_vertexSummary->pv);    // dxy

        TMatrixTSym<double> muonCov;
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


        // a1(3 prong pion) Vector Particle Properties
        TMatrixT<double> tauhPar;
        tauhPar[0] = product.m_flavourOrderedLeptons[1]->p4.Px(); // px
        tauhPar[1] = product.m_flavourOrderedLeptons[1]->p4.Py(); // py
        tauhPar[2] = product.m_flavourOrderedLeptons[1]->p4.Pz();  // pz
        tauhPar[3] = product.m_flavourOrderedLeptons[1]->p4.mass();  // m
        tauhPar[4] = 0.8;  // vx
        tauhPar[5] = 0.8;  // vy
        tauhPar[6] = 0.8;  // vz

        TMatrixTSym<double> tauhCov;
        tauhCov[0][0] = 0.5;
        tauhCov[0][1] = 0.5;
        tauhCov[0][2] = 0.5;
        tauhCov[0][3] = 0.5;
        tauhCov[0][4] = 0.5;
        tauhCov[0][5] = 0.5;
        tauhCov[0][6] = 0.5;
        tauhCov[0][7] = 0.5;
        tauhCov[1][1] = 0.5;
        tauhCov[1][2] = 0.5;
        tauhCov[1][3] = 0.5;
        tauhCov[1][4] = 0.5;
        tauhCov[1][4] = 0.5;
        tauhCov[1][4] = 0.5;
        tauhCov[1][4] = 0.5;
        tauhCov[2][2] = 0.5;
        tauhCov[2][3] = 0.5;
        tauhCov[2][4] = 0.5;
        tauhCov[3][3] = 0.5;
        tauhCov[3][4] = 0.5;
        tauhCov[4][4] = 0.5;

        int tauhPdgid = 13;
        double tauhCharge =  product.m_flavourOrderedLeptons[1]->charge();
        double tauhB = 1; 


        // MET info
        double MET= product.m_met.p4.Pt();   // ????
           
        // Primary Vertex Info
        TVector3 PV(0.5, 0.4, 0.3);
	TMatrixTSym<double> PVCov;
	PVCov[0][0]= 0.5;
        PVCov[0][1]= 0.5;
        PVCov[0][2]= 0.5;
        PVCov[1][1]= 0.5;
        PVCov[1][2]= 0.5;
        PVCov[2][2]= 0.5;
	
        TrackParticle Muon(muonPar, muonCov, muonPdgid, muonMass, muonCharge, muonB);
        LorentzVectorParticle Tauh(tauhPar, tauhCov, tauhPdgid, tauhCharge, tauhB);

        GlobalEventFit GF(Muon, Tauh,  MET,  PV, PVCov);
        //GlobalEventFit GF(TrackParticle Muon, LorentzVectorParticle Tauh, double MET, TVector3 PV, TMatrixTSym<double> PVCov);

          GF.Fit();
     
        }


}


