#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/A1Helper.h"
#include <iostream>

a1Helper::a1Helper(){
}

a1Helper::a1Helper(vector<TLorentzVector> TauA1andProd){
  if(TauA1andProd.size()!=4){
    std::cout<<" Warning!! Size of input vector != 4 !! "<<std::endl;
  }
  TLorentzVector fakeboost(0,0,0,0);
  Setup(TauA1andProd,fakeboost);
}


a1Helper::a1Helper(vector<TLorentzVector> TauA1andProd, TLorentzVector RefernceFrame){
  if(TauA1andProd.size()!=4){
    std::cout<<" Warning!! Size of input vector != 4 !! "<<std::endl;
  }
  Setup(TauA1andProd,RefernceFrame);
}


void 
a1Helper::Setup(vector<TLorentzVector> TauA1andProd, TLorentzVector ReferenceFrame){
   mpi   = 0.13957018; // GeV 
   mpi0 = 0.1349766;   // GeV
   mtau = 1.776; // GeV
   coscab = 0.975; 
   mrho = 0.773; // GeV
   mrhoprime = 1.370; // GeV
   ma1 = 1.251; // GeV
   mpiprime = 1.300; // GeV
   Gamma0rho  =0.145; // GeV
   Gamma0rhoprime = 0.510; // GeV
   Gamma0a1 = 0.599; // GeV
   Gamma0piprime = 0.3; // GeV
   fpi= 0.093; // GeV
   fpiprime = 0.08; //GeV
   gpiprimerhopi = 5.8; //GeV
   grhopipi = 6.08;  //GeV
   beta = -0.145;
   debug  = false;
   for(unsigned int i=0; i<TauA1andProd.size(); i++){
     TauA1andProd_RF.push_back(Boost(TauA1andProd.at(i),ReferenceFrame));
   }
   LFosPionLV  = TauA1andProd.at(1);
   LFss1pionLV =TauA1andProd.at(2);
   LFss2pionLV =TauA1andProd.at(3);
   LFa1LV = LFosPionLV+LFss1pionLV+LFss2pionLV;
   LFtauLV = TauA1andProd.at(0);
   LFQ= LFa1LV.M();

   _osPionLV   = TauA1andProd_RF.at(1);
   _ss1pionLV =TauA1andProd_RF.at(2);
   _ss2pionLV =TauA1andProd_RF.at(3);
   _a1LV = _osPionLV+_ss1pionLV+_ss2pionLV;
   _tauLV = TauA1andProd_RF.at(0);
   _s12 = _ss1pionLV +_ss2pionLV;
   _s13 = _ss1pionLV + _osPionLV;
   _s23 = _ss2pionLV + _osPionLV;
   _s1  =  _s23.M2(); 
   _s2  =  _s13.M2();
   _s3  =  _s12.M2();
   _Q = _a1LV.M();
}

void 
a1Helper::subSetup(double s1, double s2, double s3, double Q){
   _s1  =   s1;
   _s2  =   s2;
   _s3  =   s3;
   _Q = Q;
}



void 
a1Helper::Configure(vector<TLorentzVector> TauA1andProd){

  if(TauA1andProd.size()!=4){
    std::cout<<" Warning!! Size of input vector != 4 !! "<<std::endl;
  }
  TLorentzVector fakeboost(0,0,0,0);
  Setup(TauA1andProd,fakeboost);

}

void 
a1Helper::Configure(vector<TLorentzVector> TauA1andProd, TLorentzVector RefernceFrame){
  if(TauA1andProd.size()!=4){
    std::cout<<" a1 helper:  Warning!! Size of input vector != 4!   Size = "<< TauA1andProd.size()<<std::endl;
  }
  Setup(TauA1andProd,RefernceFrame);

}
bool
a1Helper::isConfigured(){
  if(TauA1andProd_RF.size()!=4){ std::cout<<"Error:   a1Helper is not Configured! Check  the size of input vector!  Size =  "<< TauA1andProd_RF.size() <<std::endl; return false;} return true;
}



void 
a1Helper::SetParametersReco(TLorentzVector tau, TLorentzVector mu ){//not used at the moment
 Initialize(tau,mu);
}
void 
a1Helper::SetFrame(TLorentzVector vec){//not used at the moment
  Boost_ = vec;
}



a1Helper::~a1Helper(){
}



void 
a1Helper::Initialize(TLorentzVector t, TLorentzVector mu){ //not used at the moment
  RecoMuon_=mu;
  KFitTau_=t;
}





double 
a1Helper::lambda(double x, double y, double z){
    return x*x +y*y +z*z - 2*x*y - 2*x*z - 2*z*y;
}
TLorentzVector 
a1Helper::Boost(TLorentzVector pB, TLorentzVector frame){
   TMatrixT<double> transform(4,4);
   TMatrixT<double> result(4,1);
   TVectorT<double> vec(4); 
   TVector3 b;
   if(frame.Vect().Mag()==0){ std::cout<<" Boost is not set, perfrom calculation in the Lab Frame   "<<std::endl; return pB;}
    if(frame.E()==0){ std::cout<<" Caution: Please check that you perform boost correctly!  " <<std::endl; return pB;} 
   else   b=frame.Vect()*(1/frame.E());
   vec(0)  = pB.E();    vec(1)  = pB.Px();
   vec(2)  = pB.Py();  vec(3)  = pB.Pz();
   double gamma  = 1/sqrt( 1 - b.Mag2());
   transform(0,0)=gamma; transform(0,1) =- gamma*b.X() ;  transform(0,2) =  - gamma*b.Y();  transform(0,3) = - gamma*b.Z(); 
   transform(1,0)=-gamma*b.X(); transform(1,1) =(1+ (gamma-1)*b.X()*b.X()/b.Mag2()) ;  transform(1,2) = ((gamma-1)*b.X()*b.Y()/b.Mag2());  transform(1,3) = ((gamma-1)*b.X()*b.Z()/b.Mag2());
   transform(2,0)=-gamma*b.Y(); transform(2,1) = ((gamma-1)*b.Y()*b.X()/b.Mag2());  transform(2,2) = (1 + (gamma-1)*b.Y()*b.Y()/b.Mag2());  transform(2,3) =  ((gamma-1)*b.Y()*b.Z()/b.Mag2()); 
   transform(3,0)=-gamma*b.Z(); transform(3,1) =((gamma-1)*b.Z()*b.X()/b.Mag2()) ;  transform(3,2) = ((gamma-1)*b.Z()*b.Y()/b.Mag2());  transform(3,3) = (1 + (gamma-1)*b.Z()*b.Z()/b.Mag2()); 
   result=transform*convertToMatrix(vec);
   return TLorentzVector(result(1,0), result(2,0) ,result(3,0), result(0,0));
}
double 
a1Helper::Scalar(TLorentzVector p1, TLorentzVector p2){
    return p1.Vect()*p2.Vect();
}
double 
a1Helper::MomentSFunction(double s, string type){
  int cells(50);
  //  double s = Q*Q;
  double intx(0);
  double m1 = mpi;
  double m2 = mpi;
  double m3 = mpi;

  double m13(0);
  double integral(0);

  double da1(0), db1(0);
  vector<double> set;
  set.push_back(_s1);
  set.push_back(_s2);
  set.push_back(_s3);
  set.push_back(_Q);
  double  stepx  = (pow(sqrt(s)-m2,2) - pow( m1+m3,2) ) / cells;
  for(int i=1;i<cells + 1;i++){ 
    da1 = pow(m1+m3,2) + stepx*(i-1);
    db1 = pow(m1+m3,2) + stepx*i;
    m13 = 0.5*(da1 + db1);
    double  E3s = (m13 - m1*m1 + m3*m3)/(2*sqrt(m13));  
    double  E2s = (s   - m13  -m2*m2)/(2*sqrt(m13));  
    double  m23max =pow (E2s+E3s,2) - pow( sqrt(E2s*E2s - m2*m2) - sqrt(E3s*E3s - m3*m3),2);
    double  m23min =  pow(E2s+E3s,2) - pow( sqrt(E2s*E2s - m2*m2) + sqrt(E3s*E3s - m3*m3),2);
    double  stepy = (m23max - m23min)/cells;
    double da2(0), db2(0);
    double inty(0);
    double m23(0);
    double m12(0);
    for(int j=1;j<cells + 1;j++){ 
      da2 = m23min + stepy*(j-1);
      db2 = m23min + stepy*j;
      m23 = 0.5*(da2 + db2);
      m12 = s +m1*m1 + m2*m2 + m3*m3 - m13 - m23;
      subSetup(m23,m13,m12,sqrt(s)); 
      // if(s >1.88 && s < 1.90)    std::cout<<"  WD=    "<< WD() << "        m23 = "<< m23 << "       m13= " << m13 <<    "     m12=   "<< m12 << "    sqrts=  " << sqrt(s) <<std::endl;
      // if(s >1.88 && s < 1.90)    std::cout<<"  F1  "<< F1() << "  F2 "<< F2() << " h0 " << h0()<<    "  VV1()-h()=   "<< VV1()-h() << " VV2() -h()=  " <<VV2()-h() <<std::endl;
      double SFunction(0);
      if(type=="WA")SFunction=WA();
      if(type=="WC")SFunction=WC();
      if(type=="WSA")SFunction=WSA();
      if(type=="WSB")SFunction=WSB();
      if(type=="WD"  ){
	if(m23 > m13)SFunction=WD();
	else SFunction=-WD();
      }
      if(type=="WE"){
	if(m23 > m13)SFunction=WE();
	else SFunction=-WE();
      }
      if(type=="WSD"){
	if(m23 > m13)SFunction=WSD();
	else SFunction=-WSD();
      }
      //      std::cout<<"SFunction  "<< SFunction<< std::endl;
      inty+=stepx*stepy*SFunction;
    }
    intx+=inty;
  }
  integral = intx;
  subSetup(set.at(0),set.at(1),set.at(2),set.at(3));



  return integral;
}
 

//---------------------------------------  hadronic current ---------------------------
double 
a1Helper::WA(){
   return  VV1()*F1().Rho2() + VV2()*F2().Rho2()  + 2*V1V2()*( F1()*Conjugate(F2()) ).Re();

 }

 double 
a1Helper::WC(){
   return  -(-VV1() + 2*h() )*F1().Rho2() - (-VV2() + 2*h())*F2().Rho2()   -   (-2*V1V2() - 4*h())*( F1()*Conjugate(F2()) ).Re();
 } 

 double
 a1Helper::WD(){
   double QQ = _Q*_Q;
   double undersqrt1 = VV1()  -h();
   double undersqrt2 = VV2()  -h();

   return  -sqrt(h()) * ( 2 * sqrt(undersqrt1) * F1().Rho2() - 2*sqrt(undersqrt2)*F2().Rho2()  
			  + (QQ - mpi*mpi + _s3)*(_s1 - _s2 )*( F1()*Conjugate(F2()) ).Re()/QQ/sqrt(h0() ) );


 }

 double
 a1Helper::WE(){
  return  3*sqrt(h()*h0())*( F1()*Conjugate(F2()) ).Im();
 }

double
 a1Helper::WSA(){
  double QQ = _Q*_Q;
  return  QQ*F4().Rho2();
 }
double
 a1Helper::WSB(){
  //  double QQ = _Q*_Q;
   double undersqrt1 = VV1()  -h();
   double undersqrt2 = VV2()  -h();
   return  -2*_Q* (sqrt(undersqrt1) * (F1()*Conjugate(F4())).Re() +   sqrt(undersqrt2)*(F2()*Conjugate(F4())).Re()  );
 }
double
 a1Helper::WSD(){
  double QQ = _Q*_Q;
  return  2*sqrt(QQ*h())* ( (F1()*Conjugate(F4())).Re() - (F2()*Conjugate(F4())).Re()   );
 }
double
 a1Helper::WSC(){
  //  double QQ = _Q*_Q;
   double undersqrt1 = VV1()  -h();
   double undersqrt2 = VV2()  -h();
   return  2*_Q* (sqrt(undersqrt1) * (F1()*Conjugate(F4())).Im() +   sqrt(undersqrt2)*(F2()*Conjugate(F4())).Im()  );
 }
double
 a1Helper::WSE(){
  double QQ = _Q*_Q;
   return  -2*sqrt(QQ*h())* ( (F1()*Conjugate(F4())).Im() - (F2()*Conjugate(F4())).Im()   );
 }



double
a1Helper::cosgammaLF(){
  double QQ=LFQ*LFQ;
  // double B1 = (pow(_ss1pionLV.E()*_tauLV.E()   - _ss1pionLV.Vect().Dot(_a1LV.Vect()),2 ) - QQ*mpi*mpi)/QQ;
  // double B2 = (pow(_ss2pionLV.E()*_tauLV.E()   - _ss2pionLV.Vect().Dot(_a1LV.Vect()),2 ) - QQ*mpi*mpi)/QQ;
  double B3 = (pow(LFosPionLV.E()*LFtauLV.E()   - LFosPionLV.Vect().Dot(LFa1LV.Vect()),2 ) - QQ*mpi*mpi)/QQ;

  // double T = 0.5*sqrt(-lambda(B1,B2,B3));
  // double A1=(_a1LV.E()*_a1LV.Vect().Dot(_ss1pionLV.Vect()) - _ss1pionLV.E()*_a1LV.P()*_a1LV.P())/QQ;
  // double A2=(_a1LV.E()*_a1LV.Vect().Dot(_ss2pionLV.Vect()) - _ss2pionLV.E()*_a1LV.P()*_a1LV.P())/QQ;
  double A3=(LFa1LV.E() * LFa1LV.Vect().Dot(LFosPionLV.Vect()) - LFosPionLV.E()*LFa1LV.P()*LFa1LV.P()) / LFQ;
  // std::cout<<"sqrt B3 "<< sqrt(B3)<<std::endl;
  // std::cout<<"A3 "<< A3<<std::endl;

  // std::cout<< "fuck 1  "   <<LFosPionLV.E()*LFtauLV.E()   - LFosPionLV.Vect().Dot(LFa1LV.Vect())<<std::endl;
  // std::cout<< "fuck 2  "   <<LFa1LV.E() * LFa1LV.Vect().Dot(LFosPionLV.Vect()) - LFosPionLV.E()*LFa1LV.P()*LFa1LV.P()<<std::endl;
                                         
  // std::cout<< "QQ "   << LFQ*LFQ<< "  _Q_Q  "<< _Q*_Q << std::endl;

  if(B3<=0 || cosbetaLF() >=1){std::cout<<"Warning! In a1Helper::cosgamma square root <=0! return 0"<<std::endl; return 0;}
  return A3/LFa1LV.P()/sqrt(B3)/sqrt(1 - cosbetaLF()*cosbetaLF());
}

double
a1Helper::singammaLF(){
  double QQ=LFQ*LFQ;
   double B1 = (pow(LFss1pionLV.E()*LFa1LV.E()   - LFss1pionLV.Vect().Dot(LFa1LV.Vect()),2 ) - QQ*mpi*mpi)/QQ;
  double B2 = (pow(LFss2pionLV.E()*LFa1LV.E()   - LFss2pionLV.Vect().Dot(LFa1LV.Vect()),2 ) - QQ*mpi*mpi)/QQ;
   double B3 = (pow(LFosPionLV.E()*LFa1LV.E()   - LFosPionLV.Vect().Dot(LFa1LV.Vect()),2 ) - QQ*mpi*mpi)/QQ;

  double T = 0.5*sqrt(-lambda(B1,B2,B3));

  double A1=(LFa1LV.E()*LFa1LV.Vect().Dot(LFss1pionLV.Vect()) - LFss1pionLV.E()*LFa1LV.P()*LFa1LV.P())/QQ;
  //  double A2=(_a1LV.E()*_a1LV.Vect().Dot(_ss2pionLV.Vect()) - _ss2pionLV.E()*_a1LV.P()*_a1LV.P())/QQ;
  double A3=(LFa1LV.E()*LFa1LV.Vect().Dot(LFosPionLV.Vect()) - LFosPionLV.E()*LFa1LV.P()*LFa1LV.P())/QQ;

  if(A3==0 || T==0){std::cout<<"Warning! In a1Helper::singamma denominator ==0! return 0"<<std::endl; return 0;}
  double scale = -(B3*A1/A3 - 0.5*(B2 - B1 - B3))/T;
  //  std::cout<<"scale  " << scale <<std::endl;
  return cosgammaLF()*scale;
}
double
a1Helper::cos2gamma(){
   return singamma()*singamma()   -     cosgamma()*cosgamma();
}

double
a1Helper::sin2gamma(){
  return 2*singamma()*cosgamma();
}
double 
a1Helper::cospsiLF(){
  double QQ = LFQ*LFQ;
  double s = 4*LFtauLV.E()*LFtauLV.E();
  double x = 2*LFa1LV.E()/sqrt(s);
  if(x*x  - 4*QQ/s <= 0 ){if(debug){std::cout<<"Warning! In a1Helper::cospsi root square <=0! return 0"<<std::endl;} return 0;}
  return    ( x*(mtau*mtau + QQ)  - 2*QQ  )   /   ( mtau*mtau  - QQ   ) / sqrt(x*x  - 4*QQ/s); 
}
double 
a1Helper::sinpsiLF(){
  if(cospsiLF()*cospsiLF() > 1  ){if(debug){std::cout<<"Warning! In a1Helper::sinpsi root square <=0! return nan"<<std::endl;}}
  return    sqrt(1 - cospsiLF()*cospsiLF());
}

double 
a1Helper::ultrarel_cospsiLF(){
  double QQ = LFQ*LFQ;
  double cos = (costhetaLF()*(mtau*mtau  + QQ)   + (mtau*mtau  - QQ))/(costhetaLF()*(mtau*mtau  - QQ)   + (mtau*mtau  + QQ));
  return cos;
}

double 
a1Helper::costhetaLF(){
  double QQ = LFQ*LFQ;
  double x = LFa1LV.E()/LFtauLV.E();
  double s = 4*LFtauLV.E()*LFtauLV.E();
  if( 1 - 4*mtau*mtau/s  <= 0 ){if(debug){std::cout<<"Warning! In a1Helper::costheta root square <=0! return 0"<<std::endl;} return 0;}
  return (2*x*mtau*mtau - mtau*mtau - QQ)/( (mtau*mtau - QQ)*sqrt(1 - 4*mtau*mtau/s) );
}
double 
a1Helper::sinthetaLF(){
  if( costhetaLF()*costhetaLF() > 1 ) {if(debug){std::cout<<"Warning! In a1Helper::sin theta root square <=0! return nan;   costheta = "<< costhetaLF()<<std::endl; }}
  return sqrt(1- costhetaLF()*costhetaLF());
}

double 
a1Helper::cosbetaLF(){
  double QQ = LFQ*LFQ;
  double B1 = (pow(LFss1pionLV.E()*LFa1LV.E()   - Scalar(LFss1pionLV,LFa1LV),2 ) - QQ*mpi*mpi)/QQ;
  double B2 = (pow(LFss2pionLV.E()*LFa1LV.E()   - Scalar(LFss2pionLV,LFa1LV),2 ) - QQ*mpi*mpi)/QQ;
  double B3 = (pow(LFosPionLV.E()*LFa1LV.E()   -   Scalar(LFosPionLV,LFa1LV),2 ) - QQ*mpi*mpi)/QQ;

  TVector3 ss1pionVect = LFss1pionLV.Vect();
  TVector3 ss2pionVect = LFss2pionLV.Vect();
  TVector3 ospionVect = LFosPionLV.Vect();
  float T = 0.5*sqrt(-lambda(B1,B2,B3));

  if(T==0 || LFa1LV.P()==0){if(debug){std::cout<<" Warning!  Can not compute cosbetaLF, denominator =0; return 0; "<<std::endl;} return 0;}
  return ospionVect.Dot(ss1pionVect.Cross(ss2pionVect)) /LFa1LV.P()/T;
}

double
a1Helper::VV1(){ //  this is -V1^{2}
  double QQ = _Q*_Q;
  return  _s2 - 4*mpi*mpi + pow(_s3 - _s1,2)/4/QQ;
}

double
a1Helper::VV2(){ //  this is -V2^{2}
  double QQ = _Q*_Q;
  return  _s1 - 4*mpi*mpi + pow(_s3 - _s2,2)/4/QQ;
}

double
a1Helper::V1V2(){  // this is -V1V2
  double QQ = _Q*_Q;
  return  (QQ/2 - _s3 - 0.5*mpi*mpi) + (_s3 - _s1)*(_s3 - _s2)/4/QQ;
}


double
a1Helper::h0(){ // this is -3sqrt{h0}/2
  double QQ = _Q*_Q;
  return -4*mpi*mpi + pow(2*mpi*mpi - _s1 - _s2,2)/QQ;
}

double
a1Helper::h(){
  double QQ = _Q*_Q;
  return (_s1*_s2*_s3 - mpi*mpi*pow(QQ - mpi*mpi,2))/h0()/QQ;  // this is sqrt{h}
}



TComplex 
a1Helper::F1(){
  TComplex scale(0, -2*sqrt(2)/3/fpi);
  TComplex res = scale*BreitWigner(_Q,"a1")*BRho(sqrt(_s2));
  //  std::cout<<"  BreitWigner(_Q,a1)  " << BreitWigner(_Q,"a1") << " BRho(_s2)  " << BRho(sqrt(_s2))<< std::endl;
  return res;
}


TComplex 
a1Helper::F2(){
  TComplex scale(0, -2*sqrt(2)/3/fpi);
  TComplex res = scale*BreitWigner(_Q,"a1")*BRho(sqrt(_s1));
  return res;
}

TComplex 
a1Helper::F4(){
  TComplex scale(0, -gpiprimerhopi*grhopipi*fpiprime/2/pow(mrho,4)/pow(mpiprime,3));
  TComplex res = scale*BreitWigner(_Q,"piprime")*(_s1*(_s2-_s3)*BRho(sqrt(_s1)) + _s2*(_s1-_s3)*BRho(sqrt(_s2)));
  return res;
}


TComplex 
a1Helper::BRho(double Q){
  //  std::cout<<"BRho:      BreitWigner(Q) " << BreitWigner(Q) << " BreitWigner(Q,rhoprime) " << BreitWigner(Q,"rhoprime")<< std::endl;
  return (BreitWigner(Q) + beta*BreitWigner(Q,"rhoprime"))/(1+beta);
}

TComplex 
a1Helper::BreitWigner(double Q, string type){
  double QQ=Q*Q;
  double re,im;
  double m = Mass(type);
  double g  = Widths(Q,type);
  re = (m*m*pow(m*m - QQ,2))/(pow(m*m - QQ,2) + m*m*g*g);
  im = m*m*m*g/(pow(m*m - QQ,2) + m*m*g*g);
  TComplex out(re,im);
  return out;
}

double
a1Helper::Widths(double Q, string type){
  double QQ = Q*Q;
  double Gamma;
  Gamma = Gamma0rho*mrho*pow( ppi(QQ)  / ppi(mrho*mrho), 3) /sqrt(QQ);
  if(type == "rhoprime"){
    Gamma=Gamma0rhoprime*QQ/mrhoprime/mrhoprime;
 }
  if(type == "a1"){
    Gamma=Gamma0a1*ga1(Q)/ga1(ma1);
 }
  if(type == "piprime"){
    Gamma = Gamma0piprime*pow( sqrt(QQ)/mpiprime  ,5)*pow( (1-mrho*mrho/QQ)/(1-mrho*mrho/mpiprime/mpiprime) ,3);
  }
  //  std::cout<< " Widths :   type   " << type << " Gamma  " << Gamma << "  QQ  "<< QQ <<std::endl;
  return Gamma;
}
double a1Helper::ga1(double  Q){
  double QQ = Q*Q;
  return (QQ > pow(mrho + mpi,2)) ?  QQ*(1.623 + 10.38/QQ - 9.32/QQ/QQ   + 0.65/QQ/QQ/QQ)  : 4.1*pow(QQ - 9*mpi*mpi,3)*(  1 - 3.3*(QQ - 9*mpi*mpi)  + 5.8*pow(QQ - 9*mpi*mpi,2)  );
}
double
a1Helper::Mass(string type){
  double m = mrho;
  if(type == "rhoprime") return mrhoprime; 
  if(type == "a1") return ma1;
  if(type == "piprime") return mpiprime;
  //std::cout<< "  type   " << type << " Mass  " << std::endl;
  return m;
}


double a1Helper::ppi(double QQ){  if(QQ < 4*mpi*mpi) std::cout<<"Warning! Can not compute ppi(Q); root square <0 ; return nan  "; return 0.5*sqrt(QQ - 4*mpi*mpi);}


 double a1Helper::getf(){
   double QQ=_Q*_Q;
   double l  = 0.5*(mtau*mtau + QQ)/sqrt(QQ);
   double line1 =   -2*l   *   ( 2*WA()/3   + 0.5*(3*cospsiLF()*cospsiLF()   -1)  *  ( WA()*(3*cosbeta()*cosbeta() -1 )/6    - 0.5*WC()*sinbeta()*sinbeta()*cos2gamma()   + 0.5*WD()* sinbeta()*sinbeta()* sin2gamma() )   )/sqrt(QQ);
   double line2 = mtau*mtau*WA()/QQ + mtau*mtau  *  (  WSA() +  cospsiLF()*sinbeta()*(   WSB() *cosgamma()      - WSD() * singamma())     )/QQ + WE()*cosbeta()*cospsiLF();
   double res = line1+ line2;

   return res;
 }
 double a1Helper::getg(){
   double QQ=_Q*_Q;
   //  double l  = 0.5*(mtau*mtau + QQ)/sqrt(QQ);
   double l0= 0.5*(mtau*mtau - QQ)/sqrt(QQ);
   double line1 =   -2*l0   * costhetaLF()*  ( 2*WA()/3   + 0.5*(3*cospsiLF()*cospsiLF()   -1)  *  ( WA()*(3*cosbeta()*cosbeta() -1 )/6    -  0.5*WC()*sinbeta()*sinbeta()*cos2gamma()   + 0.5*WD()* sinbeta()*sinbeta()* sin2gamma() )   )/sqrt(QQ);
   double line2 = mtau*mtau*WA()*costhetaLF()/QQ  +    sqrt(mtau*mtau/QQ )  * sinthetaLF()* ( 0.5*WA()*2* sinbeta()*cosbeta()* cosalpha() -  
                                              WC()*sinbeta()* (sinalpha()* sin2gamma() + cos2gamma()* cosalpha()*    cosbeta() )    -    WD()*sinbeta()*( sinalpha()*cos2gamma() + sin2gamma()* cosalpha()*cosbeta()  )- 2*cospsiLF()*sinpsiLF()  *
 				            (WA()*(3*cosbeta() *cosbeta() -1 )/6   -    0.5*WC()*sinbeta()* sinbeta()* cos2gamma()+ 0.5*WD()*sinbeta()* sinbeta()* cos2gamma() + WD()*sinbeta()* sinbeta()* sin2gamma())/3   );

   double line3  =  sqrt(mtau*mtau/QQ ) *sinthetaLF()* (WE()*(cosbeta()*sinpsiLF() + sinbeta()*cosalpha()) +cosbeta()*sinalpha()*(WSC()*cosgamma() - WSE()*singamma()) + cosalpha()*(WSC()*singamma() + WSE()*cosgamma()));
   double line4  =  -WE()*costhetaLF()*cosbeta()*cospsiLF() + mtau*mtau*costhetaLF()*(WSA() + cospsiLF()*sinbeta()  * (WSB()*cosgamma() - WSD()* singamma()  ) )/QQ;
   double line5  =  sqrt(mtau*mtau/QQ)*sinthetaLF() *  ( sinpsiLF()*sinbeta()*( WSB()* cosgamma() - WSD()* singamma()) + cosbeta()*cosalpha()*(WSD()*singamma() - WSB()*cosgamma()  ) + 
 							sinalpha()*(WSD()*cosgamma() + WSB()*singamma())          );
   double res = line1+ line2 + line3 + line4 + line5;
   return res;
 }


 double a1Helper::vgetf(TString type){
   double QQ=_Q*_Q;
   double RR  = mtau*mtau/QQ;
   //double R = sqrt(RR);
   float U = 0.5*(3*cospsiLF()*cospsiLF() - 1)*(1 - RR);
   double B = 0.5*(3*cosbeta()*cosbeta() - 1);

   double fA =  WA()*(2+RR + B*U)/3;
   double fC = -WC()*0.5*U*sinbeta()*sinbeta()* cos2gamma();
   double fD = WD()*0.5*U*sinbeta()*sinbeta()* sin2gamma();
   double fE =  WE()*cospsiLF()*cosbeta();

   double res = fA+fC+fD+fE;

   return res;
 }


 double a1Helper::vgetg(TString type){
   double QQ=_Q*_Q;
   double RR  = mtau*mtau/QQ; double R = sqrt(RR);
   //float U = 0.5*(3*cospsiLF()*cospsiLF() - 1)*(1 - RR);
   float V = 0.5*(3*cospsiLF()*cospsiLF() - 1)*(1 + RR)*costhetaLF() + 0.5*3*2*cospsiLF()* sinpsiLF()*sinthetaLF()*R;
   double B = 0.5*(3*cosbeta()*cosbeta() - 1);
   double fact =0;
   if(type == "bar") fact =1;
   double gA =  WA()*(costhetaLF()*(RR - 2)   - B*V)/3                                                               +     fact*WA()*0.5*R*sinthetaLF()*cosalpha()*2*sinbeta()*cosbeta();
   double gC =  WC()*0.5*V*sinbeta()*sinbeta()* cos2gamma()                                                 -      fact*WC()*R*sinthetaLF()*sinbeta()*(sinalpha()*sin2gamma()  -  cos2gamma()*cosalpha()*cosbeta() ) ;
   double gD = -WD()*0.5*V*sinbeta()*sinbeta()* sin2gamma()                                                 -      fact*WD()*R*sinthetaLF()*sinbeta()*(sinalpha()*cos2gamma() + sin2gamma()* cosalpha()*cosbeta()  );
   double gE = - WE()*cosbeta()*( costhetaLF()*cospsiLF() + R*sinthetaLF()*sinpsiLF())             +     fact*WE()*R*sinthetaLF()*sinbeta()*cosalpha();


   double res = gA+gC+gD+gE;
   return res;
 }

 double a1Helper::vgetfscalar(TString type){
   double QQ=_Q*_Q;
   double RR  = mtau*mtau/QQ;
   //double R = sqrt(RR);
   float U = 0.5*(3*cospsiLF()*cospsiLF() - 1)*(1 - RR);
   //float V = 0.5*(3*cospsiLF()*cospsiLF() - 1)*(1 + RR)*costhetaLF() + 0.5*3*2*cospsiLF()* sinpsiLF()*sinthetaLF()*R;
   double B = 0.5*(3*cosbeta()*cosbeta() - 1);

   double fA =  WA()*(2+RR + B*U)/3;
   double fC = -WC()*0.5*U*sinbeta()*sinbeta()* cos2gamma();
   double fD = WD()*0.5*U*sinbeta()*sinbeta()* sin2gamma();
   double fE =  WE()*cospsiLF()*cosbeta();
   double fSA = WSA()*RR;
   double fSB = WSB()*RR*cospsiLF()*sinbeta()*cosgamma();
   double fSC = 0;
   double fSD = -WSD()*RR*cospsiLF()*sinbeta()*singamma();
   double fSE =0;

   double res = fA+fC+fD+fE  + fSA + fSB + fSC  + fSD + fSE;

   return res;
 }
 double a1Helper::vgetgscalar(TString type){
   double QQ=_Q*_Q;
   double RR  = mtau*mtau/QQ; double R = sqrt(RR);
   //float U = 0.5*(3*cospsiLF()*cospsiLF() - 1)*(1 - RR);
   float V = 0.5*(3*cospsiLF()*cospsiLF() - 1)*(1 + RR)*costhetaLF() + 0.5*3*2*cospsiLF()* sinpsiLF()*sinthetaLF()*R;
   double B = 0.5*(3*cosbeta()*cosbeta() - 1);
   double fact =0;
   if(type == "bar") fact =1;

  
   double gA =  WA()*(costhetaLF()*(RR - 2)   - B*V)/3                                                               +     fact*WA()*0.5*R*sinthetaLF()*cosalpha()*2*sinbeta()*cosbeta();
   double gC =  WC()*0.5*V*sinbeta()*sinbeta()* cos2gamma()                                                 -      fact*WC()*R*sinthetaLF()*sinbeta()*(sinalpha()*sin2gamma()  -  cos2gamma()*cosalpha()*cosbeta() ) ;
   double gD = -WD()*0.5*V*sinbeta()*sinbeta()* sin2gamma()                                                 -      fact*WD()*R*sinthetaLF()*sinbeta()*(sinalpha()*cos2gamma() + sin2gamma()* cosalpha()*cosbeta()  );
   double gE = - WE()*cosbeta()*( costhetaLF()*cospsiLF() + R*sinthetaLF()*sinpsiLF())             +     fact*WE()*R*sinthetaLF()*sinbeta()*cosalpha();
   //double gSA =WSA()*RR*costhetaLF();
   //double gSB =WSB()*R*(R*cospsiLF()*costhetaLF()*sinbeta()*cosgamma() + sinthetaLF()* ( sinpsiLF()*sinbeta()*cosgamma()  -  cosbeta()* cosalpha()* cosgamma() + sinalpha()*singamma())   );
   //double gSC = WSC()*R*sinthetaLF()*(cosbeta()*sinalpha()*cosgamma() + cosalpha()*singamma());
   //double gSD = WSD()*R*(sinthetaLF()*(cosbeta()*cosalpha()*singamma() + sinalpha()*cosgamma() - sinpsiLF()*sinbeta()*singamma()  )      - R*costhetaLF()*cospsiLF()*sinbeta()*singamma() );
   //double gSE = -WSE()*R*sinthetaLF()*(cosbeta()*sinalpha()*singamma() -  cosalpha()*cosgamma());
   double res = gA+gC+gD+gE;

   return res;
 }

void a1Helper::debugger(){
   double QQ=_Q*_Q;
   double RR  = mtau*mtau/QQ; double R = sqrt(RR);

   double cb = TRF_cosbeta();     double ct = costhetaLF();    double ca = TRF_cosalpha();   double cg = TRF_cosgamma();  
   double sb = TRF_sinbeta();     double st =  sinthetaLF();    double sa = TRF_sinalpha();   double sg = TRF_singamma();  
   double s2g  = 2*sg*cg; double c2g = cg*cg - sg*sg;
   double Bb = 0.5*(cb*cb + 1);

   double fA =  WA()*(Bb*(1 - RR) + RR);
   double fC = -WC()*0.5*sb*sb*c2g*(1- RR);
   double fD = WD()*0.5*(1-RR)*sb*sb*s2g;
   double fE =  WE()*cb;
   //double fSA = WSA()*RR;
   //double fSB = WSB()*RR*sb*cg;
   //double fSC = 0;
   //double fSD = -WSD()*RR*sb*sg;
   //double fSE = 0;
   double s2b  = 2*sb*cb;
   //double c2b = cb*cb - sb*sb;

 
   double gA =  WA()*(RR*ct - Bb*ct*(1+RR)) + WA()*0.5*R*st*s2b*ca ;
   double gC = WC()*(ct*(1+RR)  *s2b*c2g)  - WC()*R*st*sb*( sa*s2g - c2g*ca*cb    );
   double gD = -WD()*(ct*(1+RR)*sb*sb*s2g) +WD()* R*st*sb*( sa*c2g + s2g*ca*cb  );
   double gE =  WE()*(R*st*sb*ca) - WE()*ct*cb;

   //double gSA = WSA()*RR*ct;
   //double gSB = WSB()*(RR*ct*sb*sg - R*st*(cb*ca*cg - sa*sg  ));
   //double gSC = WSC()*R*st*(cb*sa*cg + ca*sg);
   //double gSD = WSD()*(R*st*(cb*ca*sg + sa*cg) - RR*ct*sb*sg);
   //double gSE = -WSE()*st*(cb*sa*sg - ca*cg);

   std::cout<<"  TRF_f"<<std::endl; 
   std::cout<<" fa + fc + fd + fe   "<< fA+fC+fD+fE;  std::cout<<"   TRF g non alpha   "<< WA()*(RR*ct - Bb*ct*(1+RR))+  WC()*(ct*(1+RR)  *s2b*c2g) -WD()*(ct*(1+RR)*sb*sb*s2g)- WE()*ct*cb <<std::endl;
   std::cout<<" fA   "<<  fA   << "    gA  + gAa  " << WA()*(RR*ct - Bb*ct*(1+RR)) <<"  +  " << WA()*0.5*R*st*s2b*ca<<std::endl;
   std::cout<<" fC  "<<  fC   << "     gC  + gCa  " <<  WC()*(ct*(1+RR)  *s2b*c2g) <<"  +  " << - WC()*R*st*sb*( sa*s2g - c2g*ca*cb    )<<std::endl;
   std::cout<<" fD    "<<  fD   << "    gD  + gDa " << -WD()*(ct*(1+RR)*sb*sb*s2g)<<"  +  " << WD()* R*st*sb*( sa*c2g + s2g*ca*cb  )<<std::endl;
   std::cout<<" fE    "<<  fE   << "    gE  + gEa  " << - WE()*ct*cb<<"  +  " << WE()*(R*st*sb*ca)<<std::endl;

   std::cout<<"  TRF_g"<<std::endl; 
   std::cout<<" ga + gc + gd + ge   "<< gA+gC+gD+gE<<std::endl;
}


double a1Helper::vgetA1omegascalar(TString type){
  if(vgetfscalar(type)==0){ if(debug){std::cout<<"Warning!  Can not return vomegascalar; f(0)=0; return -5;  "<<std::endl;} return -999;}
  return vgetgscalar(type)/vgetfscalar(type);
}
double a1Helper::vgetA1omega(TString type){
  if(vgetf(type)==0){ if(debug){std::cout<<"Warning!  Can not return vomega; f(0)=0; return -5;  "<<std::endl; }return -999;}
  return vgetg(type)/vgetf(type);
}
double a1Helper::getA1omegaBar(){
  if(getf()==0){ if(debug){std::cout<<"Warning!  Can not return omega; f(0)=0; return -5;  "<<std::endl;} return -999;}
  return getg()/getf();
}
double
a1Helper::getA1omega(){
  double QQ=_Q*_Q;
  double RR  = mtau*mtau/QQ;
  float U = 0.5*(3*cospsiLF()*cospsiLF() - 1)*(1 - RR);
  float V = 0.5*(3*cospsiLF()*cospsiLF() - 1)*(1 + RR)*costhetaLF() + 0.5*3*2*cospsiLF()* sinpsiLF()*sinthetaLF()*sqrt(RR);
  
  float fa1 = (2  + RR + 0.5*(3*cosbeta()*cosbeta()- 1)*U)*WA()/3 - 0.5*sinbeta()*sinbeta()*cos2gamma()*U*WC() + 0.5*sinbeta()*sinbeta()*sin2gamma()*U*WD() + cospsiLF()*cosbeta()*WE();
  float ga1 = (costhetaLF()*(RR -2) - 0.5*(3*cosbeta()*cosbeta() - 1)*V)*WA()/3 + 0.5*sinbeta()*sinbeta()*cos2gamma()*V*WC() - 0.5*sinbeta()*sinbeta()*sin2gamma()*V*WD() -cosbeta()*(costhetaLF()*cospsiLF() + sinthetaLF()*sinpsiLF()*sqrt(RR))*WE();

  double omega = ga1/fa1;
  if(!std::isnan(omega)) 	return omega;
  return -999;
}
TLorentzVector
a1Helper::sLV(){
  double QQ = _Q*_Q;
  double l0 = 0.5*(mtau*mtau + QQ)/sqrt(QQ);
  double l   = 0.5*(mtau*mtau  - QQ)/sqrt(QQ);
  return TLorentzVector(sinthetaLF(),0,-l0*costhetaLF()/mtau,-l*costhetaLF()/mtau);
}


TVector3
a1Helper::nPerp(){
  if(_ss1pionLV.Vect().Cross(_ss2pionLV.Vect()).Mag()==0){if(debug){ std::cout<<"  Can not return nPerp, same sign pions seem to be parallel in a1 rest frame, return 0,0,0  "<<std::endl;} return TVector3(0,0,0);}

  TVector3 nss1= _ss1pionLV.Vect()*(1/_ss1pionLV.Vect().Mag());
  TVector3 nss2= _ss2pionLV.Vect()*(1/_ss2pionLV.Vect().Mag());
  return   (nss1.Cross(nss2))*(1/(nss1.Cross(nss2)).Mag());
}

TVector3
a1Helper::ns(){
  return   sLV().Vect()*(1/sLV().Vect().Mag());
}
TVector3
a1Helper::nL(){
  return   -LFa1LV.Vect()*(1/LFa1LV.Vect().Mag());
}
TVector3
a1Helper::nT(){
  return   _tauLV.Vect()*(1/_tauLV.Vect().Mag());
}


double  
a1Helper::TRF_cosalpha(){
   TVector3 nTCrossns  = nT().Cross(ns());
   TVector3 nTCrossnPerp  = nT().Cross(nPerp());

   if(nTCrossns.Mag() ==0 || nTCrossnPerp.Mag() ==0){if(debug){std::cout<<" Can not compute cos alpha, one denominator is 0, return TRF cos alpha =0  "<< std::endl; }return 0;}
  return nTCrossns.Dot(nTCrossnPerp)/nTCrossns.Mag()/nTCrossnPerp.Mag();
}
double  
a1Helper::TRF_sinalpha(){
   TVector3 nTCrossns  = nT().Cross(ns());
   TVector3 nTCrossnPerp  = nT().Cross(nPerp());

   if(nTCrossns.Mag() ==0 || nTCrossnPerp.Mag() ==0){if(debug){std::cout<<" Can not compute sin alpha, one denominator is 0, return TRF sin alpha =0  "<< std::endl; }return 0;}
  return -ns().Dot(nTCrossnPerp)/nTCrossns.Mag()/nTCrossnPerp.Mag();

}


double a1Helper::TRF_cosbeta(){
  return nT().Dot(nPerp());
}
double a1Helper::TRF_sinbeta(){
  if(TRF_cosbeta()*TRF_cosbeta() > 1 ){if(debug){std::cout<<"Warning! Can not compute TRF sin beta! return 0"<<std::endl;} return 0;}
  return sqrt(1 - TRF_cosbeta()*TRF_cosbeta());
}

double a1Helper::TRF_cosgamma(){
  TVector3 nTCrossnPerp  = nT().Cross(nPerp());

  TVector3 qvect = _osPionLV.Vect()*(1/_osPionLV.Vect().Mag());
  //  qvect.Print();
  if(nTCrossnPerp.Mag()==0) { if(debug){std::cout<<"Warning! Can not compute TRF cos gamma, denominator =0, return 0  "<< std::endl;} return 0; }
  return -nT()*qvect/nTCrossnPerp.Mag();
}

double a1Helper::TRF_singamma(){
  TVector3 nTCrossnPerp  = nT().Cross(nPerp());
  TVector3 qvect = _osPionLV.Vect()*(1/_osPionLV.Vect().Mag());

  if(nTCrossnPerp.Mag()==0) { if(debug){std::cout<<"Warning! Can not compute TRF  sin gamma, denominator =0, return 0  "<< std::endl;} return 0; }
  return qvect*nTCrossnPerp/nTCrossnPerp.Mag();
}


 // double  TRF_cosbeta();      double  TRF_cosalpha();   double  TRF_cosgamma();  
 // double TRF_sinbeta();        double TRF_sinalpha();    double  TRF_singamma();  

double a1Helper::cosalpha(){
   TVector3 nLCrossnT  = nL().Cross(nT());
   TVector3 nLCrossnPerp  = nL().Cross(nPerp());

   if(nLCrossnPerp.Mag() ==0 || nLCrossnT.Mag() ==0){if(debug){std::cout<<" Can not compute cos alpha, one denominator is 0, return cos alpha =0  "<< std::endl;} return 0;}
  return nLCrossnT.Dot(nLCrossnPerp)/nLCrossnT.Mag()/nLCrossnPerp.Mag();
}
double a1Helper::sinalpha(){
  TVector3 nLCrossnT  = nL().Cross(nT());
  TVector3 nLCrossnPerp  = nL().Cross(nPerp());
  if(nLCrossnPerp.Mag() ==0 || nLCrossnT.Mag() ==0){if(debug){std::cout<<" Can not compute sin alpha, one denominator is 0, return sin alpha =0  "<< std::endl; }return 0;}
  return -nT().Dot(nLCrossnPerp)/nLCrossnT.Mag()/nLCrossnPerp.Mag();
}
double a1Helper::cosbeta(){
  return nL().Dot(nPerp());
}
double a1Helper::sinbeta(){
  if(cosbeta()*cosbeta() > 1 ){if(debug){std::cout<<"Warning! Can not compute sin beta! return 0"<<std::endl;} return 0;}
  return sqrt(1 - cosbeta()*cosbeta());
}

double a1Helper::cosgamma(){
  TVector3 nLCrossnPerp  = nL().Cross(nPerp());

  TVector3 qvect = _osPionLV.Vect()*(1/_osPionLV.Vect().Mag());
  //  qvect.Print();
  if(nLCrossnPerp.Mag()==0) { if(debug){std::cout<<"Warning! Can not compute cos gamma, denominator =0, return 0  "<< std::endl; }return 0; }
  return -nL()*qvect/nLCrossnPerp.Mag();
}

double a1Helper::singamma(){
  TVector3 nLCrossnPerp  = nL().Cross(nPerp());
  TVector3 qvect = _osPionLV.Vect()*(1/_osPionLV.Vect().Mag());

  if(nLCrossnPerp.Mag()==0) { if(debug){std::cout<<"Warning! Can not compute cos gamma, denominator =0, return 0  "<< std::endl;} return 0; }
  return qvect*nLCrossnPerp/nLCrossnPerp.Mag();
}



TComplex 
a1Helper::Conjugate(TComplex a){
  return TComplex(a.Re(), -a.Im());
}
TMatrixT<double> a1Helper::convertToMatrix(TVectorT<double> V){
  TMatrixT<double> M(V.GetNrows(),1);
  for(int i=0; i < M.GetNrows(); i++){
    M(i,0)=V(i);
  } return M;
}
