
// #include "Artus/Utility/interface/UnitConverter.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/ImpactParameter.h"

#include "TMatrix.h"
#include "Math/SVector.h"
//#include "TFitter.h"
#include "Math/Functor.h"
#include "Math/BrentMinimizer1D.h"
#include "Math/Minimizer.h"
#include "Math/Factory.h"

typedef ROOT::Math::PositionVector3D<ROOT::Math::Cartesian3D<float> > RMPoint;

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

// calculate the uncertainty on dxy, dz, and the magnitude of the IP vector
// calculated wrt the PV or the refitted PV, and saved in this order in the vector.
// The errors on refP of the tracks and on the momenta
// were estimated by Gaussian fit, and therefore they are hardcoded in here
// FIXME: Need to find a better solution!
std::vector<double> ImpactParameter::CalculateIPErrors(RMFLV p4, RMPoint ref, KVertex* pv, TVector3* ipvec){

	std::vector<double> IPerrors {-999,-999,-999};
	double sdxy=0;
	double sdz=0;
	double sip=0;
	// coordinates and error of the reference point of the track
	double rx = ref.x(); double srx=0;
	double ry = ref.y(); double sry=0;
	double rz = ref.z(); double srz=0;

	// coordinates and error of the momentum
	double px = p4.Px(); double spx=0;
	double py = p4.Py(); double spy=0;
	double pz = p4.Pz(); double spz=0;
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
