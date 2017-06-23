// -*- C++ -*-
//
// 
/**\class a1Helper.h a1Helper.cc
 Description: 
*/
//
// Original Author:  Vladimir Cherepanov 
//         Created:  Mon May 1 13:49:02 CET 2017
//
//

#ifndef a1Helper_h
#define a1Helper_h


#include <vector>
#include "TLorentzVector.h"
#include "TComplex.h"
#include "TMatrixT.h"
#include "TVectorT.h"
#include "TMatrixTSym.h"
#include <string.h>
#include <vector>
#include "TLorentzVector.h"
using namespace std;


class a1Helper {
 
 public:
  a1Helper();
  a1Helper(vector<TLorentzVector> TauA1andProd);
  a1Helper(vector<TLorentzVector> TauA1andProd, TLorentzVector RefernceFrame);
  ~a1Helper();
  void Configure(vector<TLorentzVector> TauA1andProd);
  void Configure(vector<TLorentzVector> TauA1andProd, TLorentzVector RefernceFrame);
  bool isConfigured();
  void Setup(vector<TLorentzVector> TauA1andProd, TLorentzVector ReferenceFrame );
  void subSetup(double s1, double s2, double s3, double Q);

  void Initialize(TLorentzVector t, TLorentzVector mu);
  bool OmegaIsValid(){return isValid_;}
  std::vector<TLorentzVector> getBoosted(){return TauA1andProd_RF;}


  void SetParametersReco(TLorentzVector tau, TLorentzVector mu );
  void SetFrame(TLorentzVector Vec );
  TLorentzVector Boost(TLorentzVector pB, TLorentzVector frame);

  /* double costheta(); */
  /* double costheta1(); */
  /* float CosBeta(); */
  /* double CosBeta1(); */
  /* std::vector<float> Sin2Cos2Gamma(TLorentzVector p1,TLorentzVector p2, TLorentzVector p3); */
  /* float CosPsi(); */

  //====================
  double costhetaLF(); 
  double sinthetaLF();

  double cosbetaLF();
  double cospsiLF();
  double sinpsiLF();
  double ultrarel_cospsiLF();
  double cosgammaLF();
  double singammaLF();
  double cosalpha();
  double sinalpha();
  double cos2gamma();
  double sin2gamma();
  double singamma();
  double cosgamma();
  double cosbeta();
  double sinbeta();
  //====================
  double getg();
  double getf();

 double vgetg(TString type="");
 double vgetf(TString type="");
 double vgetgscalar(TString type="");
 double vgetfscalar(TString type="");

 double vgetA1omega(TString type="");
 double vgetA1omegascalar(TString type="");

 double getA1omega();
 double getA1omegaBar();

//========== TRF  =======
 // double TRF_vgetf(TString type="");
 // double TRF_vgetg(TString type="");
 // double TRF_vgetA1omega(TString type="");
 double TRF_cosbeta();      double  TRF_cosalpha();   double  TRF_cosgamma();  
 double TRF_sinbeta();        double TRF_sinalpha();    double  TRF_singamma();  
//========== TRF  =======
  void debugger();
  double lambda(double x, double y, double z);
  double Scalar(TLorentzVector p1, TLorentzVector p2);

  double MomentSFunction(double s,string type="WA");

  //--------------------------- Hadronic current ---------------------
  //  only 9 structure fucbntions are non-zero in 3pions case

  double WA();
  double WC();
  double WD();
  double WE();
  double WSA();
  double WSB();
  double WSD();
  double WSC();
  double  WSE();


  double VV1();
  double VV2();
  double V1V2();
  double h0();
  double h();

  TVector3 nL();
  TVector3 nT();
  TVector3 nPerp();
  TVector3 ns();
  TLorentzVector sLV();



  TComplex  BreitWigner(double Q, string type="rho");
  TComplex  BRho(double Q);
  TComplex F1();
  TComplex F2();
  TComplex F4();
  TComplex   Conjugate(TComplex a);
  double  Widths(double Q, string type="rho");
  double ppi(double QQ);
  double ga1(double  Q);
  double Mass(string type="rho");


  TComplex  BWa1(float QQ);
  TComplex  BWrho(float QQ);
  TComplex  BWrhoPrime(float QQ);
  float GammaA1(float QQ);
  float gForGammaA1(float QQ);
  float GammaRho(float QQ);
  float  GammaRhoPrime(float QQ);



  double GetOmegaA1();



 private:
  double mpi;
  double mpi0;
  double mtau;
  double coscab;
  double mrho;
  double mrhoprime;
  double ma1;
  double mpiprime;
  double Gamma0rho; 
  double Gamma0rhoprime; 
  double Gamma0a1;
  double Gamma0piprime;
  double fpi;
  double fpiprime;
  double gpiprimerhopi;
  double grhopipi;
  double beta;

  const TLorentzVector a1pos;
  const TLorentzVector a1pss1;
  const TLorentzVector a1pss2;

  bool debug;

  vector<TLorentzVector> TauA1andProd_RF;
  TLorentzVector _osPionLV;
  TLorentzVector _ss1pionLV;
  TLorentzVector _ss2pionLV;
  TLorentzVector _a1LV;
  TLorentzVector _tauLV;
  TLorentzVector _s12;
  TLorentzVector _s13;
  TLorentzVector _s23;


  double _s1; 
  double _s2; 
  double _s3; 
  double _Q;


  double LFQ;
  TLorentzVector   LFosPionLV;
  TLorentzVector   LFss1pionLV;
  TLorentzVector   LFss2pionLV;
  TLorentzVector   LFa1LV;
  TLorentzVector   LFtauLV;

  TLorentzVector Boost_;

  TLorentzVector KFitTau_;
  TLorentzVector RecoMuon_;
  TLorentzVector Tau1_;
  TLorentzVector Tau2_;

  TLorentzVector TauMu1_;
  TLorentzVector TauMu2_;

  bool Flag_;

  TLorentzVector Z_;
  TLorentzVector TauA1_;
  TLorentzVector TauMu_;


  TLorentzVector A1ZFrame_;
  TLorentzVector OSPionZFrame_;
  TLorentzVector SSPion1ZFrame_;
  TLorentzVector SSPion2ZFrame_;
  bool isValid_;

  TMatrixT<double> convertToMatrix(TVectorT<double> V);


};
#endif
