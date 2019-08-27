
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/ImpactParameter.h"

#include "TMatrix.h"
#include "Math/Functor.h"
#include "Math/BrentMinimizer1D.h"
#include "Math/Minimizer.h"
#include "Math/Factory.h"

//typedef ROOT::Math::PositionVector3D<ROOT::Math::Cartesian3D<float> > RMPoint;

// Variables used during the fit
// The minimizer doesn't like it if these are members of the class and thus
// they are declared here as global
// Possible Fix: Give them as arguments to the functions instead of using
// global variables start with a capital letter
double MagneticField = -999;
TVector3 ReferencePoint(-999,-999,-999);
TVector3 PrimaryVertex(-999,-999,-999);
double QOverP = -999;
double Lambda = -999;
double Phi = -999;
double V_z = -999;

const double eQ = 1.60217662e-19; // elementary charge
const double c = 2.99792458*1e8; // speed of light in m/s

short Sign(double x){
	return (x > 0) ? 1 : ((x < 0) ? -1 : 0);
}

double getPhi_1(double phi, short charge){
	return -1*TMath::ACos(-1*charge*TMath::Sin(phi))*Sign(TMath::Cos(phi)*charge);
}

double getRadius(double qOverP, double lambda, double B){
	return TMath::Sin( TMath::PiOver2() - lambda ) / (B * qOverP); //Radius;
}

double PointOnHelix_x(double x, double qOp, double l, double p){
	double pars[4];
	pars[1] = getRadius(qOp, l, MagneticField); //Radius
	pars[3] = getPhi_1(p,Sign(qOp)); //phi1
	pars[0] = ReferencePoint.x()-pars[1]*TMath::Cos(pars[3]); //Ox
	//pars[0] = ReferencePoint.x()-Radius*TMath::Cos(Phi_1); //Ox
	pars[2] = std::abs(qOp)*MagneticField*c; //Omega
	return pars[0]+pars[1]*TMath::Cos(pars[2]*x+pars[3]);
}

double PointOnHelix_y(double x, double qOp, double l, double p){
	double pars[4];
	pars[1] = getRadius(qOp, l, MagneticField); //TMath::Sin(t)/(MagneticField*qOp); //Radius
	pars[3] = getPhi_1(p,Sign(qOp)); //phi1
	pars[0] = ReferencePoint.y()+pars[1]*TMath::Sin(pars[3]); //Oy
	pars[2] = std::abs(qOp)*MagneticField*c; //Omega
	return pars[0]-pars[1]*TMath::Sin(pars[2]*x+pars[3]);
}

double PointOnHelix_z(double x, double l){
	double pars[] = {ReferencePoint.z(),V_z};//c*TMath::Sin(l)};//c*TMath::Cos(t)};
	return pars[0]+pars[1]*x;
}

double DistancePVToHelix(double x, double qOp, double l, double p){
	return pow(PointOnHelix_x(x,qOp,l,p)-PrimaryVertex[0],2)+pow(PointOnHelix_y(x,qOp,l,p)-PrimaryVertex[1],2)+pow(PointOnHelix_z(x,l)-PrimaryVertex[2],2);
}

double minuitFunction(const double *xx ){
	long double x = xx[0];
	return DistancePVToHelix(x,QOverP,Lambda,Phi);
}

/*
TVector3 TangentAtX(double x, double qOp, double l, double p){
	double pars[4];
	pars[1] = getRadius(qOp, l, MagneticField); // Radius
	pars[3] = getPhi_1(p,Sign(qOp)); //phi1
	pars[0] = ReferencePoint.x()-pars[1]*TMath::Cos(pars[3]); //Ox
	pars[2] = std::abs(qOp)*MagneticField*c; //Omega
	double X = -pars[1]*pars[2]*TMath::Sin(pars[2]*x+pars[3]);

	double pars2[4];
	pars2[1] = getRadius(qOp, l, MagneticField); // Radius
	pars2[3] = getPhi_1(p,Sign(qOp));//phi1
	pars2[0] = ReferencePoint.y()+pars2[1]*TMath::Sin(pars2[3]);
	pars2[2] = std::abs(qOp)*MagneticField*c; //Omega
	double Y = -pars2[1]*pars2[2]*TMath::Cos(pars2[2]*x+pars2[3]);

	double pars3[] = {ReferencePoint.z(),V_z};//c*TMath::Sin(l)};
	double Z = pars3[1];
	TVector3 sol(X,Y,Z);
	return sol;
}
*/

TVector3 ImpactParameter::CalculatePCA(double B, std::vector<float> h_param, RMPoint ref, RMPoint PrV, RMFLV p4){
	//everything in SI
	short charge = Sign(h_param[0]);
	double qOverP = h_param[0] * c * 1e-9;
	double lambda = h_param[1]; //lambda in rad
	double phi = h_param[2]; //phi in rad
	MagneticField = B * 1e3 / c*1e8; //in Tesla
	V_z = p4.Pz()/p4.E() * c;
	ReferencePoint.SetXYZ(ref.x(),ref.y(),ref.z());
	ReferencePoint*=0.01; //conversion from cm to m

	PrimaryVertex.SetXYZ(PrV.x(),PrV.y(),PrV.z());
	PrimaryVertex*=0.01; //conversion from cm to m

	// The helix is scanned from -T/2 to T/2, thus the sign of Omega is irrelevant
	double Omega = std::abs(qOverP*MagneticField*c);
	double Phi_1 = getPhi_1(phi,charge);
	double Radius = getRadius(qOverP, lambda, MagneticField);

	Double_t Ox = ReferencePoint.x()-Radius*TMath::Cos(Phi_1);
	Double_t Oy = ReferencePoint.y()+Radius*TMath::Sin(Phi_1);
	Double_t Oz = ReferencePoint.z();
	TVector3 Oprime(Ox,Oy,Oz);

	QOverP = qOverP;
	Lambda = lambda;
	Phi = phi;
	// Save all calculated variables used in the fit:
	this->SetHelixRadius(getRadius(qOverP, lambda, MagneticField));
	this->SetRecoMagneticField( B * 1e3 / (c*1e-8) );
	this->SetRecoV_z_SI(V_z);
	this->SetRecoOmega(Omega);
	this->SetRecoPhi1(Phi_1);
	this->SetRecoQOverP(qOverP);
	this->SetRecoDxy(h_param[3]);
	this->SetRecoDsz(h_param[4]);
	this->SetRecoOprime(RMPoint(Ox, Oy, Oz));

	//minimizing the distance between the helix and the primary vertex PV
	double x_best = 0.0;
	ROOT::Math::Minimizer* min = ROOT::Math::Factory::CreateMinimizer("Minuit2", "Combined");
	ROOT::Math::Functor f(&minuitFunction,1);
	min->SetFunction(f);
	min->SetVariable(0,"x",1e-14, 1e-16);
	min->SetTolerance(1e-15);
	min->Minimize();

	const double *xs = min->X();
	x_best=xs[0];
	this->SetXBest(x_best);
	TVector3 res(PointOnHelix_x(x_best,qOverP,lambda,phi)-PrimaryVertex.x(),PointOnHelix_y(x_best,qOverP,lambda,phi)-PrimaryVertex.y(),PointOnHelix_z(x_best,lambda)-PrimaryVertex.z());

	return res*100.; //conversion back to cm
}

double ImpactParameter::CalculatePCADifferece(SMatrixSym3D cov_PV, TVector3 IP)
{
	TVector3 n = IP.Unit();
	const int dim=3;
	ROOT::Math::SVector<double, dim> Sn(n.x(),n.y(),n.z());
	double alpha = TMath::Sqrt((ROOT::Math::Dot(Sn,cov_PV*Sn)));
	return alpha;
}

ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> ImpactParameter::CalculatePCACovariance(ROOT::Math::SMatrix<float,5,5, ROOT::Math::MatRepSym<float,5>> helixCovariance, SMatrixSym3D primaryVertexCovariance)
{
	double Radius = GetHelixRadius();
	double Omega = GetRecoOmega();
	double Phi_1 = GetRecoPhi1();
	double Dxy = GetRecoDxy() * 0.01;
	double Dsz = GetRecoDsz() * 0.01;
	double xBest = GetXBest();

	for(int i=0; i<5; i++){
		//qoverP
		helixCovariance(0, i) *= c * 1e-9;
		helixCovariance(i, 0) *= c * 1e-9;
		// dxy
		helixCovariance(3, i) *= 0.01;
		helixCovariance(i, 3) *= 0.01;
		// dsz
		helixCovariance(4, i) *= 0.01;
		helixCovariance(i, 4) *= 0.01;
	} //convert to SI units

	/*
	// Construct the Covariance Matrices relevant for the Impact parameter
	ROOT::Math::SMatrix<float,8,8, ROOT::Math::MatRepSym<float, 8>> BSHelixCov;
	BSHelixCov(0, 0) = 0; //BSSigma.X() * 0.01;
	BSHelixCov(1, 1) = 0; //BSSigma.Y() * 0.01;
	BSHelixCov(2, 2) = 0; //BSSigma.Z() * 0.01;
	for(int i=3; i<8; i++){
		for(int j=3; j<i; j++){
			BSHelixCov(i, j) = helixCovariance(i-3, j-3);
		}
	}
	*/

	ROOT::Math::SMatrix<float,3,5, ROOT::Math::MatRepStd< float, 3, 5 >> jacobiOprime;
	/*
	   All unitialized elemnts are set to default
	   thus only the non-zero elements appear in the following
	*/
	//derivatives wrt helix parameters
	// dOprime / dqOverP = 0 for all components of Oprime
	// dOprime / dlambda
	jacobiOprime(2, 1) = - Dsz * TMath::Sin(Lambda) / TMath::Cos(Lambda) / TMath::Cos(Lambda);
	// dOprime / dphi
	jacobiOprime(0, 2) = - Dxy * TMath::Cos(Phi);
	jacobiOprime(1, 2) = - Dxy * TMath::Sin(Phi);
	// dOprime / ddxy
	jacobiOprime(0, 3) = - TMath::Sin(Lambda);
	jacobiOprime(1, 3) =   TMath::Cos(Lambda);
	// dOprime / ddsz
	jacobiOprime(2, 4) = 1 / TMath::Cos(Lambda);

	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> OprimeCovariance = jacobiOprime * helixCovariance * ROOT::Math::Transpose(jacobiOprime);

	///
	ROOT::Math::SMatrix<float,4,5, ROOT::Math::MatRepStd< float, 4, 5 >> jacobiHelixpar;
	/* dRadius/dqOverP */
	jacobiHelixpar(0, 0) =   TMath::Sin(TMath::PiOver2() - Lambda) / MagneticField / pow(QOverP/eQ, 2);
	/* dRadius/dlambda */
	jacobiHelixpar(0, 1) = - TMath::Cos(TMath::PiOver2() - Lambda) / MagneticField / QOverP*eQ;
	/* dRadius/dphi = dr/ddxy = dr/dsz = 0 */
	/* domega/dqOverP */
	jacobiHelixpar(1, 0) = 1 / MagneticField;
	/* domega/dlamba = domega/dphi = domega/dxy = domega/dsz = 0 */
	/* uncertainty on phi1 does not change the uncertainty on x, there it does not need to be considered */
	/* dvz/dlambda */
	jacobiHelixpar(3, 1) = TMath::Sin(TMath::Pi() - Lambda);
	/* dvz/dqOverP = dvz/dphi = dvz/dxy = dvz/dsz = 0 */

	// Covariance for the parameterization using r, omega, phi_1, Oprime, and the time x
	ROOT::Math::SMatrix<float,4,4, ROOT::Math::MatRepStd< float, 4, 4 >> parameterCovariance_ = jacobiHelixpar * helixCovariance * ROOT::Math::Transpose(jacobiHelixpar);

	ROOT::Math::SMatrix<float,7,7, ROOT::Math::MatRepSym< float, 7 >> parameterCovariance;
	parameterCovariance(0, 0) = OprimeCovariance(0, 0);
	parameterCovariance(1, 0) = OprimeCovariance(1, 0); parameterCovariance(1, 1) = OprimeCovariance(1, 1);
	parameterCovariance(2, 0) = OprimeCovariance(2, 0); parameterCovariance(2, 1) = OprimeCovariance(1, 2); parameterCovariance(2, 2) = OprimeCovariance(2, 2);
	for(int i = 3; i < 7; i++)
		for(int j = 3; j <= i; j++)
			parameterCovariance(i, j) = parameterCovariance_(i-3, j-3);

	ROOT::Math::SMatrix<float,3,7, ROOT::Math::MatRepStd< float, 3, 7 >> jacobiPointOnHelix;
	// dPointOnHelix / dOprime
	jacobiPointOnHelix(0, 0) = 1;
	jacobiPointOnHelix(1, 1) = 1;
	jacobiPointOnHelix(2, 2) = 1;
	// dPointOnHelix / dRadius
	jacobiPointOnHelix(0, 3) =  TMath::Cos(Omega * xBest + Phi_1);
	jacobiPointOnHelix(1, 3) = -TMath::Sin(Omega * xBest + Phi_1);
	// dPointOnHelix / dOmega
	jacobiPointOnHelix(0, 4) = -Radius * TMath::Sin(Omega * xBest + Phi_1) * xBest;
	jacobiPointOnHelix(1, 4) = -Radius * TMath::Cos(Omega * xBest + Phi_1) * xBest;
	// The Phi_1 does not change how precisely you can find the PCA
	// thus it is not considered in error propagation
	// dHelixOnPoint / dv_z
	jacobiPointOnHelix(2, 6) = xBest;

	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> pointOnHelixCovariance = jacobiPointOnHelix * parameterCovariance * ROOT::Math::Transpose(jacobiPointOnHelix);
	ROOT::Math::SMatrix<float,6,6, ROOT::Math::MatRepStd< float, 6, 6 >> pointOnHelixPVCovariance;
	for(int i = 0; i < 6; i++){
		for(int j = 0; j < 6; j++){
			switch( ((i < 3) * (j < 3))? 1:0 | ((i >= 3) * (j>=3))? 2:0 ){
				case 0: break;
				case 1: pointOnHelixPVCovariance(i,j) = pointOnHelixCovariance(i, j); break;
				case 2: pointOnHelixPVCovariance(i,j) = primaryVertexCovariance(i-3, j-3)*1e-4; break; // conversion from cm^2 to m^2
			}
		}
	}

	ROOT::Math::SMatrix<float,3,6, ROOT::Math::MatRepStd< float, 3, 6 >> jacobiIP;
	jacobiIP(0, 0) = 1;
	jacobiIP(1, 1) = 1;
	jacobiIP(2, 2) = 1;
	jacobiIP(0, 3) = -1;
	jacobiIP(1, 4) = -1;
	jacobiIP(2, 5) = -1;

	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> CovIP = jacobiIP * pointOnHelixPVCovariance * Transpose(jacobiIP);
	return CovIP * 1e4; //conversion to cm^2
}

// Calculate shortest distance between the track and a point - gen level.
// When distance between track and PV -> shortest distance is the IP vector.
TVector3 ImpactParameter::CalculateShortestDistance(RMFLV p4, RMPoint vertex, RMPoint* pv){

	TVector3 k, p, IP;

	if(vertex.x() != 0 && vertex.y() != 0 && vertex.z() != 0) {
		k.SetXYZ(vertex.x() - pv->x(), vertex.y() - pv->y(), vertex.z() - pv->z());
	}
	else k.SetXYZ(-999, -999, -999);

	p.SetXYZ(p4.Px(), p4.Py(), p4.Pz());

	if ( p.Mag() != 0 && k.x() != -999 && (k.x()!=0 && k.y()!=0 && k.z()!=0) ) {
		IP = k - (p.Dot(k) / p.Mag2()) * p;
	}
	else IP.SetXYZ(-999, -999, -999);

	return IP;

}

// Calculate the shortest distance between a track and a point - reco level.
// When distance between track and PV => shortest distance is the IP vector.
TVector3 ImpactParameter::CalculateShortestDistance(RMFLV p4, RMPoint ref, RMPoint pv){

	TVector3 k, p, IP;
	k.SetXYZ(ref.x() - pv.x(), ref.y() - pv.y(), ref.z() - pv.z());

	p.SetXYZ(p4.Px(), p4.Py(), p4.Pz());

	if (p.Mag() != 0) IP = k - (p.Dot(k) / p.Mag2()) * p;
	else IP.SetXYZ(-999, -999, -999);

	return IP;

}
