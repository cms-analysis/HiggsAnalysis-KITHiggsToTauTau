
#pragma once

#include <TFile.h>
#include <TH1.h>
#include <TH2.h>
#include <TF1.h>
#include <TString.h>
#include <TRandom.h>
#include <TMath.h>
#include <assert.h>

class MEtSys {
  
 public:
  MEtSys(TString fileName);
  ~MEtSys(){};

  void ApplyMEtSys(float metPx,
		   float metPy,
		   float genVPx,
		   float genVPy,
		   float visVPx,
		   float visVPy,
		   int njets,
		   int bkgdType,
		   int sysType,
		   int shiftType,
		   float & metShiftPx,
		   float & metShiftPy);

  void ShiftMEt(float metPx,
		float metPy,
		float genVPx, 
		float genVPy,
		float visVPx,
		float visVPy,
		int njets,
		int bkgdType,
		int sysType,
		float sysShift,
		float & metShiftPx,
		float & metShiftPy);

  void ShiftResponseMet(float metPx,
			float metPy,
			float genVPx, 
			float genVPy,
			float visVPx,
			float visVPy,
			int njets,
			int bkgdType,
			float sysShift,
			float & metShiftPx,
			float & metShiftPy);

  
  void ShiftResolutionMet(float metPx,
			  float metPy,
			  float genVPx, 
			  float genVPy,
			  float visVPx,
			  float visVPy,
			  int njets,
			  int bkgdType,
			  float sysShift,
			  float & metShiftPx,
			  float & metShiftPy);

  enum ProcessType{BOSON=0, EWK=1, TOP=2};
  enum SysType{NoType=-1, Response=0, Resolution=1};
  enum SysShift{NoShift=-1, Up=0, Down=1};

 private:

  void ComputeHadRecoilFromMet(float metX,
			       float metY,
			       float genVPx, 
			       float genVPy,
			       float visVPx,
			       float visVPy,
			       float & Hparal,
			       float & Hperp);


  void ComputeMetFromHadRecoil(float Hparal,
			       float Hperp,
			       float genVPx, 
			       float genVPy,
			       float visVPx,
			       float visVPy,
			       float & metX,
			       float & metY);
  
  
  int nBkgdTypes;
  int nJetBins;
  TH1D * responseHist[3][5];
  float sysUnc[3][2][3]; // first  index : bkgd type 
  // second index : type of uncertainty 0=response, 1=resolution
  // third index  : jet multiplicity bin (0,1,2);

};
