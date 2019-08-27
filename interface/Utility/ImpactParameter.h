
#pragma once

#include <TMath.h>
#include "TVector3.h"
#include "TMatrix.h"

#include <Math/PtEtaPhiM4D.h>
#include <Math/LorentzVector.h>
#include <Math/Point3D.h>
#include <Math/MatrixRepresentationsStatic.h>
#include <Math/SMatrix.h>

typedef ROOT::Math::PtEtaPhiM4D<float> RMFLV_Store;
typedef ROOT::Math::SMatrix<double, 3, 3, ROOT::Math::MatRepSym<double, 3> > SMatrixSym3D;

typedef ROOT::Math::LorentzVector<RMFLV_Store> RMFLV;
typedef ROOT::Math::PositionVector3D<ROOT::Math::Cartesian3D<float> > RMPoint;

/*
	A class to collect all approaches for calculating the Impact Parameter
	The tangential approach is far simpler to calculate but the uncertainty
	propagation is incomplete (cmssw does not give errors on the track or momentum)
	The helical appraoch is more complicated but allows for full error propagation,
	since all used variables depend on either the helix parameters or the
 	primary Vertex and the given covariance matrices allow for error propagation
*/

class ImpactParameter
{
public:
	double CalculatePCADifferece(SMatrixSym3D cov, TVector3 DeltaPCA);
	TVector3 CalculatePCA(double B, std::vector<float> h_param, RMPoint ref, RMPoint PrV, RMFLV p4);
	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> CalculatePCACovariance(ROOT::Math::SMatrix<float,5,5, ROOT::Math::MatRepSym<float,5>> helixCov, SMatrixSym3D SigmaPrV);
	//TVector3 CalculateShortestDistance(KGenParticle* genParticle, RMPoint* pv);
	TVector3 CalculateShortestDistance(RMFLV p4, RMPoint vertex, RMPoint* pv);
	TVector3 CalculateShortestDistance(RMFLV p4, RMPoint ref, RMPoint pv);
	//std::vector<double> CalculateIPErrors(RMFLV p4, RMPoint ref, KVertex* pv, TVector3* ipvec);

	// set functions for variables used in the helical approach
	inline double GetHelixRadius(){ return helixRadius; }
	inline double GetRecoMagneticField(){ return recoMagneticField;}
	inline double GetRecoV_z_SI(){ return recoV_z_SI; }
	inline double GetRecoQOverP(){ return recoQOverP; }
	inline double GetRecoDxy(){ return recoDxy; }
	inline double GetRecoDsz(){ return recoDsz; }
	inline double GetRecoOmega(){ return recoOmega; }
	inline double GetRecoPhi1(){ return recoPhi1; }
	inline double GetXBest(){ return xBest; }
	inline RMPoint GetRecoOprime(){ return recoOprime; }
private:
	double helixRadius;
	double recoMagneticField;
	double recoV_z_SI;
	double recoOmega;
	double recoPhi1;
	double xBest;
	double recoQOverP;
	double recoDxy;
	double recoDsz;
	RMPoint recoOprime;

	// set functions for variables used in the helical approach
	inline void SetHelixRadius(double radius){ helixRadius = radius; }
	inline void SetRecoMagneticField(double magneticField){ recoMagneticField = magneticField;}
	inline void SetRecoV_z_SI(double v_z_SI){ recoV_z_SI = v_z_SI; }
	inline void SetRecoOmega(double Omega){ recoOmega = recoOmega; }
	inline void SetRecoPhi1(double Phi_1){ recoPhi1 = Phi_1; }
	inline void SetXBest(double XBest){ xBest = XBest; }
	inline void SetRecoDxy(double Dxy){ recoDxy = Dxy; }
	inline void SetRecoDsz(double Dsz){ recoDsz = Dsz; }
	inline void SetRecoQOverP(double qoverp){ recoQOverP = qoverp; }
	inline void SetRecoOprime(RMPoint Oprime){ recoOprime = Oprime; }
};

