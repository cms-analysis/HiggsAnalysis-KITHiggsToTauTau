
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/CPQuantities.h"
#include "Artus/Utility/interface/UnitConverter.h"

#include "TMatrix.h"
#include "Math/SVector.h"
#include "TFitter.h"
//#include "TF1.h"
//#include "TCanvas.h"
#include "Math/Functor.h"
#include "Math/BrentMinimizer1D.h"
#include "Math/Minimizer.h"
#include "Math/Factory.h"

#include <fstream>

typedef ROOT::Math::PositionVector3D<ROOT::Math::Cartesian3D<float> > RMPoint;

// this version uses tau 4-momenta to calculate decay planes (useful for GenTauCPProducer)
double CPQuantities::CalculatePhiStarCP(RMFLV tau1, RMFLV tau2, RMFLV chargPart1, RMFLV chargPart2)
{
	//Momentum vectors of the Taus
	RMFLV::BetaVector k1, k2;
	k1.SetXYZ(tau1.Px(), tau1.Py() , tau1.Pz());
	k2.SetXYZ(tau2.Px(), tau2.Py() , tau2.Pz());
	return this->CalculatePhiStarCPSame(k1, k2, chargPart1, chargPart2, "gen");
}


double CPQuantities::CalculatePCADifferece(SMatrixSym3D cov_PV, TVector3 IP)
{
	TVector3 n = IP.Unit();
	const int dim=3;
	ROOT::Math::SVector<double, dim> Sn(n.x(),n.y(),n.z());
	double alpha = TMath::Sqrt((ROOT::Math::Dot(Sn,cov_PV*Sn)));
	return alpha;
}

double B_SI = 0.0;
TVector3 Ref(0.,0.,0.);
TVector3 PV_v(0.,0.,0.);
const double c = 2.99792458*1e8; //speed of light in m/s
double v_z_SI = 0.0;

short sign(double x)
{
	return (x > 0) ? 1 : ((x < 0) ? -1 : 0);
}

double get_phi1(double phi, short charge) //returns phi1
{
	return -1*TMath::ACos(-1*charge*TMath::Sin(phi))*sign(TMath::Cos(phi)*charge);
}

double f_x1(double x, double qOp, double l, double p)
{
	double t = TMath::Pi()/2-l;
	double pars[4];
	pars[1] = TMath::Sin(t)/(B_SI*qOp); //Radius
	pars[3] = get_phi1(p,sign(qOp)); //phi1
	pars[0] = Ref.x()-pars[1]*TMath::Cos(pars[3]); //Ox
	pars[2] = std::abs(qOp)*B_SI*c; //Omega
	return pars[0]+pars[1]*TMath::Cos(pars[2]*x+pars[3]);
}

double f_x2(double x, double qOp, double l, double p)
{
	double t = TMath::Pi()/2-l;
	double pars[4];
	pars[1] = TMath::Sin(t)/(B_SI*qOp); //Radius
	pars[3] = get_phi1(p,sign(qOp)); //phi1
	pars[0] = Ref.y()+pars[1]*TMath::Sin(pars[3]); //Oy
	pars[2] = std::abs(qOp)*B_SI*c; //Omega
	return pars[0]-pars[1]*TMath::Sin(pars[2]*x+pars[3]);
}

double f_x3(double x, double l)
{
	// double t = TMath::Pi()/2-l;
	double pars[] = {Ref.z(),v_z_SI};//c*TMath::Sin(l)};//c*TMath::Cos(t)};
	return pars[0]+pars[1]*x;
}

double tot(double x, double qOp, double l, double p) {
	return pow(pow(f_x1(x,qOp,l,p)-PV_v[0],2)+pow(f_x2(x,qOp,l,p)-PV_v[1],2)+pow(f_x3(x,l)-PV_v[2],2),0.5);
}

void minuitFunction(int& nDim, double* gout, double& result, double par[], int flg) {
	double x = par[0];
	double qOp = par[1];
	double l = par[2];
	double p = par[3];
	result = tot(x,qOp,l,p);
}

double qOp_Brent;
double l_Brent;
double p_Brent;

double BrentFunc(double x)
{
	return tot(x,qOp_Brent,l_Brent,p_Brent);
}

double minuit2fcn(const double *xx )
{
	long double x = xx[0];
	return tot(x,qOp_Brent,l_Brent,p_Brent);
}

TVector3 tangent_at_x(double x, double qOp, double l, double p)
{
	double t = TMath::Pi()/2-l;
	double pars[4];
	pars[1] = TMath::Sin(t)/(B_SI*qOp); //Radius
	pars[3] = get_phi1(p,sign(qOp)); //phi1
	pars[0] = Ref.x()-pars[1]*TMath::Cos(pars[3]); //Ox
	pars[2] = std::abs(qOp)*B_SI*c; //Omega
	double X = -pars[1]*pars[2]*TMath::Sin(pars[2]*x+pars[3]);

	double pars2[4];
	pars2[1] = TMath::Sin(t)/(B_SI*qOp); //Radius
	pars2[3] = get_phi1(p,sign(qOp));//phi1
	pars2[0] = Ref.y()+pars2[1]*TMath::Sin(pars2[3]);
	pars2[2] = std::abs(qOp)*B_SI*c; //Omega
	double Y = -pars2[1]*pars2[2]*TMath::Cos(pars2[2]*x+pars2[3]);

	double pars3[] = {Ref.z(),v_z_SI};//c*TMath::Sin(l)};
	double Z = pars3[1];
	TVector3 sol(X,Y,Z);
	return sol;
}

TVector3 CPQuantities::CalculatePCA(double B, short charge, std::vector<float> h_param,	ROOT::Math::SMatrix<float,5,5, ROOT::Math::MatRepSym<float,5>> cov, RMPoint ref, RMPoint PrV, bool write, double* return_scalar_product, KLepton* recoParticle, double* xBest)
{
	//everything in SI
	const double eQ = 1.60217662*1e-19; //elementary charge in C
	B_SI = B*1e3/(c*1e-8); //in Tesla
	double q_SI = charge * eQ; //in Coulomb
	double p_SI = std::abs(1/h_param[0]); //in GeV
	p_SI *= 1e9*eQ/(c); //conversion from GeV to kg*m/s
	double qOverP = q_SI/p_SI;
	v_z_SI = ((recoParticle->p4.Pz())/(recoParticle->p4.E()))*c;
	//std::cout << v_z_SI << std::endl;
	double lambda = h_param[1]; //lambda in rad
	double phi = h_param[2]; //phi in rad
	// double dxy = (h_param[3]);
	// double dsz = (h_param[4]);
	double theta = TMath::Pi()/2-lambda;
	Ref.SetXYZ(ref.x(),ref.y(),ref.z());
	Ref*=0.01; //conversion from cm to m

	PV_v.SetXYZ(PrV.x(),PrV.y(),PrV.z());
	PV_v*=0.01; //conversion from cm to m

	double Radius = TMath::Sin(theta)/(B_SI*qOverP);
	double Omega = qOverP*B_SI*c;
	Omega = (Omega<0 ? -Omega : Omega); //std::abs
	//double T = 2*TMath::Pi()/Omega;
	double Phi_1 = get_phi1(phi,charge);

	Double_t Ox = Ref.x()-Radius*TMath::Cos(Phi_1);
	Double_t Oy = Ref.y()+Radius*TMath::Sin(Phi_1);
	Double_t Oz = Ref.z();
	TVector3 Oprime(Ox,Oy,Oz);

	qOp_Brent = qOverP;
	l_Brent = lambda;
	p_Brent = phi;

	// Double_t v_z = c*TMath::Cos(theta);

	//for (int i=0;i<3;i++) PV_comp[i] = PV_v[i];//.x(),PV_v.y(),PV_v.z()};
	//double xmin = -T/2;
	//double xmax = -xmin;
	/*
	double sigma_qOverP = pow(cov(0,0),0.5)*eQ/(1e9*eQ/(c));
	double sigma_lambda = pow(cov(1,1),0.5); //=sigma_theta, since they're linear
	double sigma_Phi = pow(cov(2,2),0.5); //=sigma_phi_1, for the same reason
	*/


	// Save all calculated variables used in the fit:
	this->SetHelixRadius(Radius);
	this->SetRecoMagneticField(B_SI);
	this->SetRecoP_SI(p_SI);
	this->SetRecoV_z_SI(v_z_SI);
	this->SetRecoOmega(Omega);
	this->SetRecoPhi1(Phi_1);
	this->SetRecoOprime(RMPoint(Ox, Oy, Oz));

	double x_best = 0.0;
	//minimizing the distance between the helix and the primary vertex PV


	//1. Minimizer: Minuit
	ROOT::Math::Minimizer* min = ROOT::Math::Factory::CreateMinimizer("Minuit2", "Combined");
	ROOT::Math::Functor f(&minuit2fcn,1);
	min->SetFunction(f);
	min->SetVariable(0,"x",1e-14, 1e-16);
	min->SetTolerance(1e-15);
	min->Minimize();

	const double *xs = min->X();
	x_best=xs[0];
	/*
	std::ofstream sc2("x_bests.res",std::fstream::app);
	sc2 << x_best*Omega << std::endl;
	sc2.close();
	*/
	//2. Minimizer: Brent
	/*
	ROOT::Math::Functor1D func(&BrentFunc);
	ROOT::Math::BrentMinimizer1D bm;
	bm.SetFunction(func,xmin,xmax);
	bm.Minimize(20,1.E-18,1.E-18);
	double x_best_Brent = bm.XMinimum();
	x_best = x_best_Brent;
	*/

	//3. Minimizer: Taylor expand delta^2 in small Omega*t
	/*
	std::cout << "x_bests:" << std::endl;
	std::cout <<"Brent:" << x_best << std::endl;
	TVector3 Delta = PV_v - Ref;
	double v_3 = c*TMath::Sin(lambda)/Omega;
	double A_q = -2*(-Delta(0)*0.5*Radius*TMath::Sin(Phi_1)+Delta(1)*Radius*0.5*TMath::Cos(Phi_1));
	double B_q = -2*(-Delta(0)*Radius*TMath::Cos(Phi_1)+Delta(1)*Radius*TMath::Sin(Phi_1))+2*(Radius*Radius+v_3*v_3);
	double C_q = -2*(-Delta(0)*Radius*TMath::Sin(Phi_1)-Delta(1)*Radius*TMath::Cos(Phi_1)+Delta(2)*v_3);
	double Disk = B_q*B_q-4*A_q*C_q;
	if (Disk<0) std::cout << "Disk. Error!" << std::endl;
	else
	{
		double t1 = (-B_q+pow(Disk,0.5))/(2*A_q*Omega);
		double t2 = (-B_q-pow(Disk,0.5))/(2*A_q*Omega);
		double delta1 = pow(tot(t1,qOverP,lambda,phi),0.5);
		double delta2 = pow(tot(t2,qOverP,lambda,phi),0.5);
		x_best = (delta1>delta2 ? t2 : t1);
		std::cout <<"Anal:" << x_best << std::endl;
	}
	*/

	*xBest = x_best;
	TVector3 res(f_x1(x_best,qOverP,lambda,phi)-PV_v.x(),f_x2(x_best,qOverP,lambda,phi)-PV_v.y(),f_x3(x_best,lambda)-PV_v.z());
	TVector3 tangent_at_x_best = tangent_at_x(x_best,qOverP,lambda,phi);
	*return_scalar_product = tangent_at_x_best.DeltaPhi(tangent_at_x(0,qOverP,lambda,phi));//tangent_at_x_best.Angle(tangent_at_x(0,qOverP,lambda,phi));//Omega*x_best_Brent;
	/*
	std::ifstream is("pca1_hel.res");
	if (!is.good() && write)
	{
		std::cout << "phi: " << phi << std::endl;
		std::cout << "Ref: ";
		for (int i=0;i<3;i++) std::cout << Ref(i) << " ";
		std::cout << "charge: " << charge << std::endl;
		std::cout << "phi_1: " << get_phi1(phi,charge) << std::endl;
		std::cout << "x_best" << x_best << std::endl;

		//std::cout << "delta = " << pow(tot(x_best_Brent,qOverP,lambda,phi),0.5) << std::endl;
		std::cout << "x = [" << f_x1(x_best,qOverP,lambda,phi)<<" , "<< f_x2(x_best,qOverP,lambda,phi) << " , " << f_x3(x_best,lambda) <<" ]" <<std::endl;

		std::ofstream f0("helix.res");
		int N = 100;
		double delta=(xmax-xmin)/(1*N); //1->30000
		for (double y=xmin/1; y<=xmax/1;y+=delta)
		{
			f0 << f_x1(y,qOverP,lambda,phi) <<" "<< f_x2(y,qOverP,lambda,phi) << " " << f_x3(y,lambda) << std::endl;
		}
		f0.close();
		N=1000;
		delta = 1./N;
		std::ofstream f1("pv.res");
		for (double x=0; x<=1;x+=delta) f1 << PV_v(0)*x <<" "<< PV_v(1)*x << " " << PV_v(2)*x << std::endl;
		f1.close();
		std::ofstream f2("r.res");
		for (double x=0; x<=1;x+=delta) f2 << Ref.x()*x <<" "<< Ref.y()*x << " " << Ref.z()*x << std::endl;
		f2.close();

		std::ofstream f5("p_b.res");
		f5 << f_x1(x_best,qOverP,lambda,phi) <<" "<< f_x2(x_best,qOverP,lambda,phi) << " " << f_x3(x_best,lambda) << std::endl;
		f5.close();

		std::ofstream f3("pca1_hel.res");
		for (double x=0; x<=1;x+=delta) f3 << (-f_x1(x_best,qOverP,lambda,phi)+PV_v(0))*x+f_x1(x_best,qOverP,lambda,phi) <<" "<< (-f_x2(x_best,qOverP,lambda,phi)+PV_v(1))*x+f_x2(x_best,qOverP,lambda,phi) << " " << (-f_x3(x_best,lambda)+PV_v(2))*x+f_x3(x_best,lambda) << std::endl;
		f3.close();

		std::ofstream f6("pca1_hel_tan.res");
		for (double x=0; x<=1;x+=delta) f6 << tangent_at_x_best.x()*x+f_x1(x_best,qOverP,lambda,phi) <<" "<< tangent_at_x_best.y()*x+f_x2(x_best,qOverP,lambda,phi) << " " << tangent_at_x_best.z()*x+f_x3(x_best,lambda) << std::endl;
		f6.close();
	}
	*/
	return res*100.; //conversion back to cm
}

ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> CPQuantities::CalculatePCACovariance(double B, short charge, std::vector<float> h_param,	ROOT::Math::SMatrix<float,5,5, ROOT::Math::MatRepSym<float,5>> cov, RMPoint ref, RMPoint PrV, SMatrixSym3D SigmaPrV, double xBest, KLepton* recoParticle)
{
	//everything in SI
	const double eQ = 1.60217662*1e-19; //elementary charge in C
	B_SI = B*1e3/(c*1e-8); //in Tesla
	double q_SI = charge * eQ; //in Coulomb
	double p_SI = std::abs(1/h_param[0]); //in GeV
	p_SI *= 1e9*eQ/(c); //conversion from GeV to kg*m/s
	double qOverP = q_SI/p_SI;
	double lambda = h_param[1]; //lambda in rad
	double phi = h_param[2]; //phi in rad
	double Phi_1 = TMath::Pi()/2+phi;
	double theta = TMath::Pi()/2-lambda;
	Ref.SetXYZ(ref.x(),ref.y(),ref.z());
	Ref*=0.01; //conversion from cm to m

	PV_v.SetXYZ(PrV.x(),PrV.y(),PrV.z());
	PV_v*=0.01; //conversion from cm to m

	double Radius = TMath::Sin(theta)/(B_SI*qOverP);
	double Omega = qOverP*B_SI*c;
	Omega = (Omega<0 ? -Omega : Omega);

	// Construct the Covariance Matrices relevant for the Impact parameter
	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepSym<float, 3>> Sigma_O; //TODO Put in actual covariance matrix
	Sigma_O(0, 0) = 0; Sigma_O(0, 1) = 0;  Sigma_O(0, 2) = 0;
	Sigma_O(1, 0) = 0; Sigma_O(1, 1) = 0; Sigma_O(1, 2) = 0;
	Sigma_O(2, 0) = 0; Sigma_O(2, 1) = 0; Sigma_O(2, 2) = 0;

	for(int i=0; i<5; i++){
		cov(0, i) *= c * 1e-9;
		cov(i, 0) *= c * 1e-9;
	} //convert to SI units, ignore the dxy and dsz components
	ROOT::Math::SMatrix<float,4,5, ROOT::Math::MatRepStd< float, 4, 5 >> JacobiHelixpar;
	/* dRadius/dqOverP */
	JacobiHelixpar(0, 0) =   TMath::Sin(TMath::Pi()/2 - lambda) / B_SI / pow(qOverP/eQ, 2);
	/* dRadius/dlambda */
	JacobiHelixpar(0, 1) = - TMath::Cos(TMath::Pi()/2 - lambda) / B_SI / qOverP*eQ;
	/* dRadius/dphi = dr/ddxy = dr/dsz = 0 */
	/* domega/dqOverP */
	JacobiHelixpar(1, 0) = 1 / B_SI;
	/* domega/dlamba = domega/dphi = domega/dxy = domega/dsz = 0 */
	/* uncertainty on phi1 does not change the uncertainty on x, there it does not need to be considered */
	/* dvz/dlambda */
	JacobiHelixpar(3, 1) = TMath::Sin(TMath::Pi() - lambda);
	/* dvz/dqOverP = dvz/dphi = dvz/dxy = dvz/dsz = 0 */

	ROOT::Math::SMatrix<float,4,4, ROOT::Math::MatRepStd< float, 4, 4 >> Sigma_par_ = JacobiHelixpar * cov * ROOT::Math::Transpose(JacobiHelixpar);

	ROOT::Math::SMatrix<float,7,7, ROOT::Math::MatRepSym< float, 7 >> Sigma_par;
	Sigma_par(0, 0) = Sigma_O(0, 0);
	Sigma_par(1, 0) = Sigma_O(1, 0); Sigma_par(1, 1) = Sigma_O(1, 1);
	Sigma_par(2, 0) = Sigma_O(2, 0); Sigma_par(2, 1) = Sigma_O(1, 2); Sigma_par(2, 2) = Sigma_O(2, 2);
	for(int i = 3; i < 7; i++)
		for(int j = 3; j <= i; j++)
			Sigma_par(i, j) = Sigma_par_(i-3, j-3);

	ROOT::Math::SMatrix<float,3,7, ROOT::Math::MatRepStd< float, 3, 7 >> Jacobifx;
	//       dO'_1              dO'_1              dO'_1
	/* df1 */ Jacobifx(0, 0) = 1; Jacobifx(0, 1) = 0; Jacobifx(0, 2) = 0;
	/* df2 */ Jacobifx(1, 0) = 0; Jacobifx(1, 1) = 1; Jacobifx(1, 2) = 0;
	/* df3 */ Jacobifx(2, 0) = 0; Jacobifx(2, 1) = 0; Jacobifx(2, 2) = 1;
	//       dr                                                   dOmega
	/* df1 */ Jacobifx(0, 3) =  TMath::Cos(Omega * xBest + Phi_1); Jacobifx(0, 4) = -Radius * TMath::Sin(Omega * xBest + Phi_1) * xBest;
	/* df2 */ Jacobifx(1, 3) = -TMath::Sin(Omega * xBest + Phi_1); Jacobifx(1, 4) = -Radius * TMath::Cos(Omega * xBest + Phi_1) * xBest;
	/* df3 */ Jacobifx(2, 3) =  0;                                 Jacobifx(2, 4) = 0;
	//       dphi1                                                         dvz
	/* df1 */ Jacobifx(0, 5) = 0/*-Radius * TMath::Sin(Omega * xBest + Phi_1)*/; Jacobifx(0, 6) = 0;
	/* df2 */ Jacobifx(1, 5) = 0/*-Radius * TMath::Cos(Omega * xBest + Phi_1)*/; Jacobifx(1, 6) = 0;
	/* df3 */ Jacobifx(2, 5) = 0;                                           Jacobifx(2, 6) = xBest;

	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> Sigma_fx = Jacobifx * Sigma_par * ROOT::Math::Transpose(Jacobifx);
	ROOT::Math::SMatrix<float,6,6, ROOT::Math::MatRepStd< float, 6, 6 >> Cov_fxPV;
	for(int i = 0; i < 6; i++){
		for(int j = 0; j < 6; j++){
			switch( ((i < 3) && (j < 3))? 1: ((i >= 3) && (j>=3))? 2:0 ){
				case 0: break;
				case 1: Cov_fxPV(i,j) = Sigma_fx(i, j); break;
				case 2: Cov_fxPV(i,j) = SigmaPrV(i-3, j-3)*1e-4; break; // conversion from cm^2 to m^2
			}
		}
	}

	ROOT::Math::SMatrix<float,3,6, ROOT::Math::MatRepStd< float, 3, 6 >> JacobiIP;
	JacobiIP(0, 0) = 1;
	JacobiIP(1, 1) = 1;
	JacobiIP(2, 2) = 1;
	JacobiIP(0, 3) = -1;
	JacobiIP(1, 4) = -1;
	JacobiIP(2, 5) = -1;

	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> CovIP = JacobiIP * Cov_fxPV * Transpose(JacobiIP);
	return CovIP * 1e4; //conversion to cm^2
}

// this version uses track and vertex information to calculate the decay planes (useful for RecoTauCPProducer)
double CPQuantities::CalculatePhiStarCP(KVertex* pv, KTrack track1, KTrack track2,  RMFLV chargPart1, RMFLV chargPart2)
{
	//Primary vertex
	RMFLV::BetaVector pvpos;
	pvpos.SetXYZ((pv->position).X(), (pv->position).Y(), (pv->position).Z());

	//Points on tau tracks
	RMFLV::BetaVector track1pos, track2pos;
	track1pos.SetXYZ((track1.ref).X(), (track1.ref).Y(), (track1.ref).Z());
	track2pos.SetXYZ((track2.ref).X(), (track2.ref).Y(), (track2.ref).Z());

	//Flight direction of taus determined from pv and trackpos
	RMFLV::BetaVector k1, k2;
	k1 = track1pos - pvpos;
	k2 = track2pos - pvpos;
	return this->CalculatePhiStarCPSame(k1, k2, chargPart1, chargPart2, "reco");

}

//this function calculates Phi* and Phi*CP using the rho decay planes
double CPQuantities::CalculatePhiStarCPRho(RMFLV chargedPiP, RMFLV chargedPiM, RMFLV piZeroP, RMFLV piZeroM, bool merge)
{
    return this->CalculatePhiStarCPCommon(chargedPiP, chargedPiM,
					  piZeroP, piZeroM,
					  false, merge, merge, "");
}

// calculation of variables Phi* and Phi*CP
// IP vectors calculated within the function
double CPQuantities::CalculatePhiStarCPSame(RMFLV::BetaVector k1, RMFLV::BetaVector k2, RMFLV chargPart1, RMFLV chargPart2, std::string level)
{
	//Step 1: Creating a Boost M into the ZMF of the (chargPart1(+), chargedPart2(-)) decay
	RMFLV ProngImp = chargPart1 + chargPart2;
	RMFLV::BetaVector boostvec = ProngImp.BoostToCM();
	ROOT::Math::Boost M(boostvec);

	//Step 2: Calculating impact parameter vectors n1 n2

	//Momentum vectors of the charged particles
	RMFLV::BetaVector p1, p2;
	p1.SetXYZ(chargPart1.Px(), chargPart1.Py() , chargPart1.Pz());
	p2.SetXYZ(chargPart2.Px(), chargPart2.Py() , chargPart2.Pz());

	//Not normalized n1, n2
	RMFLV::BetaVector n1 = k1 - ((k1.Dot(p1)) / (p1.Dot(p1))) * p1;
	RMFLV::BetaVector n2 = k2 - ((k2.Dot(p2)) / (p2.Dot(p2))) * p2;

	//Normalized n1, n2
	n1 = n1.Unit();
	n2 = n2.Unit();
	// save azimuthal angles of the decay planes in the lab frame
	if(level=="reco"){
		this->SetRecoPhiPlusIPMeth(n1.Phi());
		this->SetRecoPhiMinusIPMeth(n2.Phi());
	}

	//Step 3: Boosting 4-vectors (n1,0), (n2,0), p1, p2 with M
	RMFLV n1_mu, n2_mu;
	n1_mu.SetXYZT(n1.X(), n1.Y(), n1.Z(), 0);
	n2_mu.SetXYZT(n2.X(), n2.Y(), n2.Z(), 0);

	n1_mu = M * n1_mu;
	n2_mu = M * n2_mu;
	chargPart1 = M * chargPart1;
	chargPart2 = M * chargPart2;

	//Step 4: Calculation of the transverse component of n1, n2 to p1, p2 (after Boosting)
	n1.SetXYZ(n1_mu.Px(), n1_mu.Py(), n1_mu.Pz());
	n2.SetXYZ(n2_mu.Px(), n2_mu.Py(), n2_mu.Pz());
	p1.SetXYZ(chargPart1.Px(), chargPart1.Py(), chargPart1.Pz());
	p2.SetXYZ(chargPart2.Px(), chargPart2.Py(), chargPart2.Pz());

	RMFLV::BetaVector n1t = n1 - ((n1.Dot(p1)) / (p1.Dot(p1))) * p1;
	n1t = n1t.Unit();
	RMFLV::BetaVector n2t = n2 - ((n2.Dot(p2)) / (p2.Dot(p2))) * p2;
	n2t = n2t.Unit();
	RMFLV::BetaVector p1n = p1.Unit();
	// save azimuthal angles of the decay planes in the ZMF
	if(level=="reco"){
		this->SetRecoPhiStarPlusIPMeth(n1t.Phi());
		this->SetRecoPhiStarMinusIPMeth(n2t.Phi());
	}

	if(level=="reco")
	{
		this->SetRecoPhiStar(acos(n2t.Dot(n1t)));
		this->SetRecoOStarCP(p1n.Dot(n2t.Cross(n1t)));
	}
	else if (level=="gen")
	{
		this->SetGenPhiStar(acos(n2t.Dot(n1t)));
		this->SetGenOStarCP(p1n.Dot(n2t.Cross(n1t)));
	}

	//Step 5: Calculating Phi*CP
	double phiStarCP = 0;
	if(p1n.Dot(n2t.Cross(n1t))>=0)
	{
		phiStarCP = acos(n2t.Dot(n1t));
	}
	else
	{
		phiStarCP = 2*ROOT::Math::Pi()-acos(n2t.Dot(n1t));
	}
	return phiStarCP;
}


// calculation of Phi*CP
// passing the IP vectors as arguments
// assummed that chargedPart1 is positive
double CPQuantities::CalculatePhiStarCP(RMFLV chargPart1, RMFLV chargPart2, TVector3 ipvec1, TVector3 ipvec2, std::string level){

  RMFLV ipLV1;
  ipLV1.SetXYZT(ipvec1.X(), ipvec1.Y(), ipvec1.Z(), 0);
  RMFLV ipLV2;
  ipLV2.SetXYZT(ipvec2.X(), ipvec2.Y(), ipvec2.Z(), 0);

  return this->CalculatePhiStarCPCommon(chargPart1, chargPart2,
					ipLV1, ipLV2,
					false, false, false,
					level);
}


// calculation of phiStarCP using the IP+rho combined method using the arho-channel
// (i.e. one tau decays to charged particle a, and the other tau to rho, which decays to pi pi0)
// The function takes the charge of the particle a as argument,
// since the calculation of OStarCP depends on which particle is positively charged
// (which is taken as reference)
double CPQuantities::CalculatePhiStarCPComb(TVector3 ipvec, RMFLV chargPart, RMFLV pion, RMFLV pizero, int charge, bool merge){

	// save azimuthal angles of the decay planes in the lab frame
	if (charge>0){
		this->SetRecoPhiPlusCombMeth(ipvec.Phi());
		this->SetRecoPhiMinusCombMeth(pizero.Phi());
	} else {
		this->SetRecoPhiPlusCombMeth(pizero.Phi());
		this->SetRecoPhiMinusCombMeth(ipvec.Phi());
	}

	// create LV for the IP vector
	RMFLV ipLV;
	ipLV.SetXYZT(ipvec.X(), ipvec.Y(), ipvec.Z(), 0);

	return this->CalculatePhiStarCPCommon(chargPart, pion,
					      ipLV, pizero,
					      (charge<0),
					      false, merge, "");
}

// Two functions to merge the combined Phi*CP variable for the channels in which
// the dacayChannel is tautau -> a rho
// It also stores the values for the phi angles of the decayplanes since this saves checking the decayMode twice

// if et or mt ch.
double CPQuantities::MergePhiStarCPCombSemiLeptonic(double phiStarCP, KTau* recoTau2, double reco_posyTauL, double reco_negyTauL){
	double phiStarCPMerged = -999;
	// merged variable
	if (recoTau2->charge() > 0) {
		if (reco_posyTauL > 0) phiStarCPMerged = phiStarCP;
		else {
			if (phiStarCP > ROOT::Math::Pi())
				phiStarCPMerged = phiStarCP - ROOT::Math::Pi();
			else phiStarCPMerged = phiStarCP + ROOT::Math::Pi();
		}
	} else {
		if (reco_negyTauL > 0)
			phiStarCPMerged = phiStarCP;
		else {
			if (phiStarCP > ROOT::Math::Pi())
				phiStarCPMerged = phiStarCP - ROOT::Math::Pi();
			else phiStarCPMerged = phiStarCP + ROOT::Math::Pi();
		}
	}

	return phiStarCPMerged;
}



double CPQuantities::MergePhiStarCPCombFullyHadronic(double phiStarCP, KTau* recoTau1, KTau* recoTau2, double reco_posyTauL, double reco_negyTauL){
	double phiStarCPMerged = -999;
	// tau1->rho, tau2->a
	if (recoTau1->decayMode == 1 && recoTau2->decayMode != 1) {

		// FIXME:	Currently not saved because they are not used
		//		Should they be deleted?
		// azimuthal angles of the tau decay planes
		// *recoPhiPlusCombMeth = CPQuantities::GetRecoPhiPlusCombMeth();
		// *recoPhiMinusCombMeth = CPQuantities::GetRecoPhiMinusCombMeth();
		// *recoPhiStarPlusCombMeth = CPQuantities::GetRecoPhiStarPlusCombMeth();
		// *recoPhiStarMinusCombMeth = CPQuantities::GetRecoPhiStarMinusCombMeth();

		// merged variable
		if (recoTau1->charge() > 0) {
			if (reco_posyTauL > 0) phiStarCPMerged = phiStarCP;
			else {
				if (phiStarCP > ROOT::Math::Pi())
					phiStarCPMerged = phiStarCP - ROOT::Math::Pi();
				else phiStarCPMerged = phiStarCP + ROOT::Math::Pi();
			}
		} // recoTau1->charge > 0
		else {
			if (reco_negyTauL > 0)
				phiStarCPMerged = phiStarCP;
			else {
				if (phiStarCP > ROOT::Math::Pi())
					phiStarCPMerged = phiStarCP - ROOT::Math::Pi();
				else phiStarCPMerged = phiStarCP + ROOT::Math::Pi();
			} // recoTau1->charge() < 0
		}
	} // tau1->rho, tau2->a

	// tau1->a, tau2->rho
	if (recoTau1->decayMode != 1 && recoTau2->decayMode ==1){
		// merged variable
		if (recoTau2->charge() > 0) {
			if (reco_posyTauL > 0)
				phiStarCPMerged = phiStarCP;
			else {
				if (phiStarCP > ROOT::Math::Pi())
					phiStarCPMerged = phiStarCP - ROOT::Math::Pi();
				else phiStarCPMerged = phiStarCP + ROOT::Math::Pi();
			}
		} // recoTau2->charge > 0
		else {
			if (reco_negyTauL > 0)
				phiStarCPMerged = phiStarCP;
			else {
				if (phiStarCP > ROOT::Math::Pi())
					phiStarCPMerged = phiStarCP - ROOT::Math::Pi();
				else phiStarCPMerged = phiStarCP + ROOT::Math::Pi();
			} // recoTau2->charge() < 0
		}
	} // tau1->a, tau2->rho

	return phiStarCPMerged;
}

// calculation of the hadron Energies in the approximate diTau restframe
double CPQuantities::CalculateChargedHadronEnergy(RMFLV diTauMomentum, RMFLV chargHad)
{
	// Step 1: Creating Boost into diTau rest frame
	RMFLV::BetaVector boostditau = diTauMomentum.BoostToCM();
	ROOT::Math::Boost Mditau(boostditau);
	// Step 2: Boosting hadron and extracting energy
	chargHad = Mditau * chargHad;
	return chargHad.E();
}


// estimation of the impact parameter error (used on recostruction level)
double CPQuantities::CalculateTrackReferenceError(KTrack track)
{
	return sqrt(track.errDz()*track.errDz()+track.errDxy()*track.errDxy());
}


// calculation of the angle Phi between the tau decay planes
// - using tau- direction in the tautau RF as reference
// - calculating the normal vectors to the planes
// - everything is defined in the Higgs boson rest frame
double CPQuantities::CalculatePhiCP(RMFLV boson, RMFLV tau1, RMFLV tau2, RMFLV chargPart1, RMFLV chargPart2)
{
	// Step 1: Boosts into the boson rest frames to boost charged particles 4-momentums
	RMFLV::BetaVector boostvech = boson.BoostToCM();
	ROOT::Math::Boost Mh(boostvech);

	// Step 2: Boosting the 4-momentum vectors to boson rest frame
	tau1 = Mh * tau1;
	tau2 = Mh * tau2;

	chargPart1 = Mh * chargPart1;
	chargPart2 = Mh * chargPart2;

	// Step 3: Creating 3-momentum normal vectors on decay planes
	RMFLV::BetaVector km, pm, pp, nm, np, ez;
	km.SetXYZ(tau1.Px(),tau1.Py(),tau1.Pz());
	pm.SetXYZ(chargPart1.Px(),chargPart1.Py(),chargPart1.Pz());
	pp.SetXYZ(chargPart2.Px(),chargPart2.Py(),chargPart2.Pz());

	nm = (km.Cross(pm)).Unit(); np = (km.Cross(pp)).Unit(); ez = km.Unit();

	// Step 4: Calculating PhiCP
	this->SetGenPhi(acos(np.Dot(nm)));
	this->SetGenOCP(ez.Dot(np.Cross(nm)));
	double phiCP = 0;
	if(ez.Dot(np.Cross(nm))>=0)
	{
		phiCP = acos(np.Dot(nm));
	}
	else
	{
		phiCP = 2*ROOT::Math::Pi()-acos(np.Dot(nm));
	}
	return phiCP;
}


// calculate phicp in the lab frame
// this function is useable both at gen and reco level
double CPQuantities::CalculatePhiCPLab(RMFLV chargPart1, TVector3 ipvec1, TVector3 ipvec2)
{
	// creating 3-momentum normal vectors on decay planes
	TVector3 p1, n1, n2;
	p1.SetXYZ(chargPart1.Px(),chargPart1.Py(),chargPart1.Pz());
	n1 = ipvec1;
	n2 = ipvec2;

	p1 = p1.Unit();
	n1 = n1.Unit();
	n2 = n2.Unit();

	// calculating PhiCP in the lab frame
	double phiCP = 0;
	if(p1.Dot(n1.Cross(n2))>=0)
	{
		phiCP = acos(n1.Dot(n2));
	}
	else
	{
		phiCP = 2*ROOT::Math::Pi()-acos(n1.Dot(n2));
	}
	return phiCP;
}


// calculation of the charged prong energy in tau restframe
double CPQuantities::CalculateChargedProngEnergy(RMFLV tau, RMFLV chargedProng)
{
	// Step 1: Creating boost to Tau restframe
	RMFLV::BetaVector boosttauvect = tau.BoostToCM();
	ROOT::Math::Boost TauRestFrame(boosttauvect);

	// Step 2: Boosting charged Prong 4-momentum vector and extracting energy
	chargedProng = TauRestFrame * chargedProng;
	return chargedProng.E();
}

// calculation of the spin analysing discriminant (y^{tau}) using the rest frame of the taus (only gen level)
// FIXME it is not called in RecoTauCPProducer. Could it be removed?
double CPQuantities::CalculateSpinAnalysingDiscriminantRho(RMFLV tau1, RMFLV tau2, RMFLV pionP, RMFLV pionM, RMFLV pi0P, RMFLV pi0M)
{
	// Step 1: Extract all pion energies in the tau restframe
	double pionP_energy = CalculateChargedProngEnergy(tau1, pionP);
	double pionM_energy = CalculateChargedProngEnergy(tau2, pionM);
	double pi0P_energy = CalculateChargedProngEnergy(tau1, pi0P);
	double pi0M_energy = CalculateChargedProngEnergy(tau2, pi0M);

	// Step 2: Calculate the y for each pair of pions respectively
	double ytauP = (pionP_energy - pi0P_energy) / (pionP_energy + pi0P_energy);
	double ytauM = (pionM_energy - pi0M_energy) / (pionM_energy + pi0M_energy);

	return ytauM * ytauP;
}

// calculation of the spin analysing discriminant (y^{tau}_L) using the laboratory system of the rhos
double CPQuantities::CalculateSpinAnalysingDiscriminantRho(RMFLV chargedPion, RMFLV pi0)
{
	return (chargedPion.E() - pi0.E()) / (chargedPion.E() + pi0.E());
}


// Calculate longitudinal polarization variables (z+, z-, zs)
double CPQuantities::CalculateZPlusMinus(RMFLV higgs, RMFLV chargedPart)
{
	//calculating boost into higgs restframe
	RMFLV::BetaVector boostHiggs = higgs.BoostToCM();
	ROOT::Math::Boost higgsRestFrame(boostHiggs);

	//boost particles into rest frame
	higgs = higgsRestFrame * higgs;
	chargedPart = higgsRestFrame * chargedPart;

	// calculate Z+-
	double zPlusMinus = 2 * chargedPart.E() / higgs.E();
	return zPlusMinus;
}


double CPQuantities::CalculateZs(double zPlus, double zMinus)
{
	//calculate the surface between z+ = z- and z+ = z- + a for each event
	//z+ and z- are in range [0,1]. So maximum surface is 0.5
	//negative a defines the surface below the diagonal line
	double a = zPlus - zMinus;
	double zs = 0;
	if (a >= 0)
	{
		zs = 0.5 * (1 - ((1 - a) * (1 - a)));
	}
	else
	{
		a = -a;
		zs = 0.5 * (1 - ((1 - a) * (1 - a)));
		zs = -zs;
	}
	return zs;
}


double CPQuantities::CalculateD0sArea(double d0_1, double d0_2)
{
	//calculate the surface between d0_1 = d0_2 and d0_1 = d0_2 + a for each event
	//d0_1 and d0_2 are constricted between 0 and 0.05. So maximum surface is 1.25x10^-3
	//negative a defines the surface below the diagonal line
	double a = std::abs(d0_1) - std::abs(d0_2);
	double ds = 0.0;
	if (d0_1 < -900 || d0_2 < -900 )
	{
		ds = -1000;
	}
	else
	{
		if (a >= 0)
		{
			ds = 0.5 * ((1.0/400.0) - (((1.0/20.0) - a) * (1.0/20.0 - a)));
		}
		else
		{
			a = -a;
			ds = 0.5 * ((1.0/400.0) - (((1.0/20.0) - a) * (1.0/20.0 - a)));
			ds = -ds;
		}
	}
	return ds;
}

double CPQuantities::CalculateD0sDist(double d0_1, double d0_2)
{
	//calculate the distance of a point from the d0_1 = d0_2 diagonal line for each event
	//d0_1 and d0_2 are constricted between 0 and 0.05. So maximum length is 0.03
	//negative a defines the surface below the diagonal line
	double a = std::abs(d0_1) - std::abs(d0_2);
	double ds = 0.0;

	if (d0_1 < -900 || d0_2 < -900 )
	{
		ds = -1000;
	}
	else
	{
		if (a >= 0)
		{
			ds = a/(std::sqrt(2.0));
		}
		else
		{
			a = -a;
			ds = a/(std::sqrt(2.0));
			ds = -ds;
		}
	}
	return ds;
}

double CPQuantities::PhiTransform(double phi)
{
	phi = 	fmod((phi + ROOT::Math::Pi()),(2 * ROOT::Math::Pi()));
	return phi;
}


// Calculate shortest distance between the track and a point - gen level.
// When distance between track and PV -> shortest distance is the IP vector.
TVector3 CPQuantities::CalculateShortestDistance(KGenParticle* genParticle, RMPoint* pv){

	TVector3 k, p, IP;

	if(genParticle->vertex.x() != 0 && genParticle->vertex.y() != 0 && genParticle->vertex.z() != 0) {
		k.SetXYZ(genParticle->vertex.x() - pv->x(), genParticle->vertex.y() - pv->y(), genParticle->vertex.z() - pv->z());
	}
	else k.SetXYZ(-999, -999, -999);

	p.SetXYZ(genParticle->p4.Px(), genParticle->p4.Py(), genParticle->p4.Pz());

	if ( p.Mag() != 0 && k.x() != -999 && (k.x()!=0 && k.y()!=0 && k.z()!=0) ) {
		IP = k - (p.Dot(k) / p.Mag2()) * p;
	}
	else IP.SetXYZ(-999, -999, -999);

	return IP;

}


// Calculate the shortest distance between a track and a point - reco level.
// When distance between track and PV => shortest distance is the IP vector.
// In case recoParticle is a tau, the track of the leading PF candidate is considered (see KLepton struct).
TVector3 CPQuantities::CalculateShortestDistance(KLepton* recoParticle, RMPoint pv){

	TVector3 k, p, IP;
	k.SetXYZ(recoParticle->track.ref.x() - pv.x(), recoParticle->track.ref.y() - pv.y(), recoParticle->track.ref.z() - pv.z());

	p.SetXYZ(recoParticle->p4.Px(), recoParticle->p4.Py(), recoParticle->p4.Pz());

	if (p.Mag() != 0) IP = k - (p.Dot(k) / p.Mag2()) * p;
	else IP.SetXYZ(-999, -999, -999);

	return IP;

}



// calculate the cosine of the angle psi (alpha in the Berges paper 1408.0798)
// needed to observe the DY distribution modulation
// this function is useable for both gen and reco level
double CPQuantities::CalculateCosPsi(RMFLV momentum, TVector3 ipvec){

	TVector3 ez, p, n;
	ez.SetXYZ(0,0,1);
	p.SetXYZ(momentum.Px(), momentum.Py(), momentum.Pz());
	n = ipvec;

	ez = ez.Unit();
	p = p.Unit();
	n = n.Unit();

	double cospsi = TMath::Abs( (ez.Cross(p)).Dot(n.Cross(p)) / (ez.Cross(p).Mag() * n.Cross(p).Mag()) );

	return cospsi;

}


// calculate the uncertainty on dxy, dz, and the magnitude of the IP vector
// calculated wrt the PV or the refitted PV, and saved in this order in the vector.
// The errors on refP of the tracks and on the momenta
// were estimated by Gaussian fit, and therefore they are hardcoded in here
// FIXME: Need to find a better solution!
std::vector<double> CPQuantities::CalculateIPErrors(KLepton* lepton, KVertex* pv, TVector3* ipvec){

	std::vector<double> IPerrors {-999,-999,-999};
	double sdxy=0;
	double sdz=0;
	double sip=0;
	// coordinates and error of the reference point of the track
	double rx = lepton->track.ref.x(); double srx=0;
	double ry = lepton->track.ref.y(); double sry=0;
	double rz = lepton->track.ref.z(); double srz=0;

	// coordinates and error of the momentum
	double px = lepton->p4.Px(); double spx=0;
	double py = lepton->p4.Py(); double spy=0;
	double pz = lepton->p4.Pz(); double spz=0;
	double p = sqrt(px*px + py*py + pz*pz);
	double pt = sqrt(px*px + py*py);

	// coordinates and error of the refitted primary vertex
	double pvx = pv->position.x();
	double pvy = pv->position.y();
	double pvz = pv->position.z();

	double Vxx = pv->covariance.At(0,0);
	double Vyy = pv->covariance.At(1,1);
	double Vzz = pv->covariance.At(2,2);
	double Vxy = pv->covariance.At(0,1);
	double Vxz = pv->covariance.At(0,2);
	double Vyz = pv->covariance.At(1,2);

	// distance between refPoint and PV
	double kx = rx - pvx;
	double ky = ry - pvy;
	double kz = rz - pvz;

	// coordinates of the IP vector
	double ipx = ipvec->X();
	double ipy = ipvec->Y();
	double ipz = ipvec->Z();
	double ip = sqrt(ipx*ipx + ipy*ipy + ipz*ipz);
	double a = (kx*px + ky*py + kz*pz)/pow(p,2);

	// partial derivatives for IPerror calculation
	// partial derivatives of IP wrt IPx, IPy, IPx
	double s = ipx/ip;   double t = ipy/ip;   double u = ipz/ip;
	// partial derivatives of IPx/y/z wrt rx/y/z
	double FxRx = -pow(px,2)/pow(p,2)+1;   double FxRy = -px*py/pow(p,2);         double FxRz = -px*pz/pow(p,2);
	double FyRx = -px*py/pow(p,2);         double FyRy = -pow(py,2)/pow(p,2)+1;   double FyRz = -py*pz/pow(p,2);
	double FzRx = -px*pz/pow(p,2);         double FzRy = -py*pz/pow(p,2);         double FzRz = -pow(pz,2)/pow(p,2)+1;
	// partial derivatives of IPx/y/z wrt pvx/y/z
	double FxPVx = pow(px,2)/pow(p,2)-1;   double FxPVy = px*py/pow(p,2);         double FxPVz = px*pz/pow(p,2);
	double FyPVx = px*py/pow(p,2);         double FyPVy = pow(py,2)/pow(p,2)-1;   double FyPVz = py*pz/pow(p,2);
	double FzPVx = px*pz/pow(p,2);         double FzPVy = py*pz/pow(p,2);         double FzPVz = pow(pz,2)/pow(p,2)-1;
	// partial derivatives of IPx/y/z wrt px/y/z
	double FxPx = -kx*px/pow(p,2)+2*a*pow(px,2)/pow(p,2)-a;
	double FxPy = -ky*px/pow(p,2)+2*a*px*py/pow(p,2);
	double FxPz = -kz*px/pow(p,2)+2*a*px*pz/pow(p,2);
	double FyPx = -kx*py/pow(p,2)+2*a*px*py/pow(p,2);
	double FyPy = -ky*py/pow(p,2)+2*a*pow(py,2)/pow(p,2)-a;
	double FyPz = -kz*py/pow(p,2)+2*a*py*pz/pow(p,2);
	double FzPx = -kx*pz/pow(p,2)+2*a*px*pz/pow(p,2);
	double FzPy = -ky*pz/pow(p,2)+2*a*py*pz/pow(p,2);
	double FzPz = -kz*pz/pow(p,2)+2*a*pow(pz,2)/pow(p,2)-a;

	// error on dxy
	sdxy = sqrt(
		(1/pow(pt,2)) *
		(
			pow(kx*px+ky*py, 2)
			* ( pow(py*spx, 2) + pow(px*spy, 2) )
			+ pow(py,2) * ( pow(srx,2) + Vxx )
			+ pow(px,2) * ( pow(sry,2) + Vyy )
			- 2*px*py*Vxy
		)
	);


	// error on dz
	sdz = sqrt(
		(1/pow(pt,4))
		* (
			pow(px,2) * pow(pz,2) * ( pow(srx,2) + Vxx )
			+
			pow(py,2) * pow(pz,2) * ( pow(sry,2) + Vyy )
		)
		+ ( pow(srz,2) + Vzz )
		+ (1/pow(pt,8))
		* (
			pow(2*px*pz * (kx*px+ky*py) - kx*pz*pow(pt,2), 2) * pow(spx,2)
			+
			pow(2*py*pz * (kx*px+ky*py) - ky*pz*pow(pt,2), 2) * pow(spy,2)
		)
		+ (1/pow(pt,2)) * pow(kx*px+ky*py, 2) * pow(spz,2)
		+ (2/pow(pt,4)) * ( px*py*pow(pz,2)*Vxy - px*pz*pow(pt,2)*Vxz - py*pz*pow(pt,2)*Vyz )
	);


	// error on IPvec mag
	sip = sqrt(
			pow(s,2)
			* (
				pow(FxRx*srx,2) + pow(FxRy*sry,2) + pow(FxRz*srz,2)
				+ pow(FxPx*spx,2) + pow(FxPy*spy,2) + pow(FxPz*spz,2)
				+ pow(FxPVx,2)*Vxx + pow(FxPVy,2)*Vyy + pow(FxPVz,2)*Vzz
				+ 2*FxPVx*FxPVy*Vxy + 2*FxPVx*FxPVz*Vxz + 2*FxPVy*FxPVz*Vyz
			)
			+
			pow(t,2)
			* (
				pow(FyRx*srx,2) + pow(FyRy*sry,2) + pow(FyRz*srz,2)
				+ pow(FyPx*spx,2) + pow(FyPy*spy,2) + pow(FyPz*spz,2)
				+ pow(FyPVx,2)*Vxx + pow(FyPVy,2)*Vyy + pow(FyPVz,2)*Vzz
				+ 2*FyPVx*FyPVy*Vxy + 2*FyPVx*FyPVz*Vxz + 2*FyPVy*FyPVz*Vyz
			)
			+
			pow(u,2)
			* (
				pow(FzRx*srx,2) + pow(FzRy*sry,2) + pow(FzRz*srz,2)
				+ pow(FzPx*spx,2) + pow(FzPy*spy,2) + pow(FzPz*spz,2)
				+ pow(FzPVx,2)*Vxx + pow(FzPVy,2)*Vyy + pow(FzPVz,2)*Vzz
				+ 2*FzPVx*FzPVy*Vxy + 2*FzPVx*FzPVz*Vxz + 2*FzPVy*FzPVz*Vyz
			)
			+
			2*s*t
			* (
				FxRx*FyRx*pow(srx,2) + FxRy*FyRy*pow(sry,2) + FxRz*FyRz*pow(srz,2)
				+ FxPx*FyPx*pow(spx,2) + FxPy*FyPy*pow(spy,2) + FxPz*FyPz*pow(spz,2)
				+ FxPVx*FyPVx*Vxx + FxPVy*FyPVy*Vyy + FxPVz*FyPVz*Vzz
				+ ( FxPVx*FyPVy + FxPVy*FyPVx ) * Vxy
				+ ( FxPVx*FyPVz + FxPVz*FyPVx ) * Vxz
				+ ( FxPVy*FyPVz + FxPVz*FyPVy ) * Vyz
			)
			+
			2*s*u
			* (
				FxRx*FzRx*pow(srx,2) + FxRy*FzRy*pow(sry,2) + FxRz*FzRz*pow(srz,2)
				+ FxPx*FzPx*pow(spx,2) + FxPy*FzPy*pow(spy,2) + FxPz*FzPz*pow(spz,2)
				+ FxPVx*FzPVx*Vxx + FxPVy*FzPVy*Vyy + FxPVz*FzPVz*Vzz
				+ ( FxPVx*FzPVy + FxPVy*FzPVx ) * Vxy
				+ ( FxPVx*FzPVz + FxPVz*FzPVx ) * Vxz
				+ ( FxPVy*FzPVz + FxPVz*FzPVy ) * Vyz
			)
			+
			2*t*u
			* (
				FyRx*FzRx*pow(srx,2) + FyRy*FzRy*pow(sry,2) + FyRz*FzRz*pow(srz,2)
				+ FyPx*FzPx*pow(spx,2) + FyPy*FzPy*pow(spy,2) + FyPz*FzPz*pow(spz,2)
				+ FyPVx*FzPVx*Vxx + FyPVy*FzPVy*Vyy + FyPVz*FzPVz*Vzz
				+ ( FyPVx*FzPVy + FyPVy*FzPVx ) * Vxy
				+ ( FyPVx*FzPVz + FyPVz*FzPVx ) * Vxz
				+ ( FyPVy*FzPVz + FyPVz*FzPVy ) * Vyz
			)
	);

	IPerrors.at(0) = sdxy;
	IPerrors.at(1) = sdz;
	IPerrors.at(2) = sip;

	return IPerrors;

}
//method which can be used to calculate PhiCP for different cases
//inputs:
//charged1,2: LV of patricles definig ZMF, e.g. charged prongs or true (gen) taus
//ref1,2: LV definig other direction, e.g. (IP,0), pi0 or true (gen) charged prongs
//firstNegative: true if first particle has negative charge, default false
//dp1,2: true is ref1,2 is used to define decay plane and non trivial y1,2 should be computed, default false
double CPQuantities::CalculatePhiStarCPCommon(RMFLV charged1, RMFLV charged2,
					      RMFLV ref1, RMFLV ref2,
					      bool firstNegative,
					      bool dp1, bool dp2,
					      std::string level) {

  //Compute spin analysing disscrimiant y in the LAB frame.
  //It is trivial, i.e. equal to 1, for non-decay-plane method.
  double yL1 = dp1 ? this->CalculateSpinAnalysingDiscriminantRho(charged1, ref1) : 1.;
  double yL2 = dp2 ? this->CalculateSpinAnalysingDiscriminantRho(charged2, ref2) : 1.;
  double yL = yL1 * yL2;

  //Creating a boost M into the ZMF of the (charged1, charged2) decay...
  RMFLV ProngImp = charged1 + charged2;
  RMFLV::BetaVector boostvec = ProngImp.BoostToCM();
  ROOT::Math::Boost M(boostvec);

  //DPDP method (rho-method)
  //Save azimuthal angles of the decay planes in the lab frame
  if (dp1 && dp2) {
    if (firstNegative) {
      this->SetRecoPhiPlusRhoMeth(ref2.Phi());
      this->SetRecoPhiMinusRhoMeth(ref1.Phi());
    }
    else {
      this->SetRecoPhiPlusRhoMeth(ref1.Phi());
      this->SetRecoPhiMinusRhoMeth(ref2.Phi());
    }
  }

  //and boosting 4-vectors to the ZMF
  charged1 = M * charged1;
  charged2 = M * charged2;
  ref1 = M * ref1;
  ref2 = M * ref2;

  //Get normalised 3-vectors ("momenta directions") in the ZMF
  RMFLV::BetaVector p1 = charged1.Vect().Unit();
  RMFLV::BetaVector p2 = charged2.Vect().Unit();
  RMFLV::BetaVector k1 = ref1.Vect().Unit();
  RMFLV::BetaVector k2 = ref2.Vect().Unit();

  //and then normalised transverse components to the planes spanned by them
  RMFLV::BetaVector n1t = (k1 - p1*(p1.Dot(k1))).Unit();
  RMFLV::BetaVector n2t = (k2 - p2*(p2.Dot(k2))).Unit();

  double phiStarCP = acos(n1t.Dot(n2t));
  double oStarCP = p2.Dot(n1t.Cross(n2t));
  //double phiStarCPOriginal = phiStarCP;
  //double oStarCPOriginal = oStarCP;

  if (firstNegative) {
    oStarCP = p1.Dot(n2t.Cross(n1t));
  }
  if (oStarCP<0) {
    phiStarCP = 2*ROOT::Math::Pi() - phiStarCP;
  }
  if (yL<0) {
    if (phiStarCP > ROOT::Math::Pi())
      phiStarCP = phiStarCP - ROOT::Math::Pi();
    else
      phiStarCP = phiStarCP + ROOT::Math::Pi();
  }
  // save phi* and O*CP
  //IPIP
  if (!dp1 && !dp2) {
    if (level == "reco") {
      this->SetRecoPhiStar(phiStarCP);
      this->SetRecoOStarCP(oStarCP);
    }
    else if (level == "gen") {
      this->SetGenPhiStar(phiStarCP);
      this->SetGenOStarCP(oStarCP);
    }
  }
  else if ((dp1 && !dp2) || (!dp1 && dp2)) {
    if (firstNegative) {
      this->SetRecoPhiStarPlusCombMeth(n2t.Phi());
      this->SetRecoPhiStarMinusCombMeth(n1t.Phi());
    }
    else {
      this->SetRecoPhiStarPlusCombMeth(n1t.Phi());
      this->SetRecoPhiStarMinusCombMeth(n2t.Phi());
    }
  }
  else if (dp1 && dp2) {
    // save azimuthal angles of the decay planes in the ZMF
    if (firstNegative) {
      this->SetRecoPhiStarPlusRhoMeth(n2t.Phi());
      this->SetRecoPhiStarMinusRhoMeth(n1t.Phi());
    }
    else {
      this->SetRecoPhiStarPlusRhoMeth(n1t.Phi());
      this->SetRecoPhiStarMinusRhoMeth(n2t.Phi());
    }
  }

  return phiStarCP;
}
