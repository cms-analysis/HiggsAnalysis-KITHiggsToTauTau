#pragma once

#include <string>
#include <TFile.h>
#include <TH1.h>
#include <TMath.h>
#include "TVector3.h"
#include <Math/Point3D.h>
#include <TGraph.h>

typedef ROOT::Math::PositionVector3D<ROOT::Math::Cartesian3D<float> > RMPoint;

class IsomorphicMappingProxy
{
public:
	IsomorphicMappingProxy(std::string decaychannel, std::string ipVersion, std::string year, bool onlyPrompt=false, bool isEmbedding=false)
	{
		m_ipVersion = ipVersion;
		m_year = year;
		m_onlyPrompt = onlyPrompt;

		if (isEmbedding){
			m_emb = "_emb";
		}
		if (decaychannel == "mt") {
			if (m_ipVersion.find("_1") != std::string::npos) {
				m_decayChannel = "muon";
			} else {
				m_decayChannel = "pion";
			}
		} else if (decaychannel == "tt") {
			m_decayChannel = "pion";
		}

		if (m_ipVersion.find("BS") != std::string::npos) {
			m_bs = "_bs";
		}

		std::string ip_r_prompt_str;
		std::string ip_phi_prompt_str;
		std::string ip_theta_prompt_str;
		std::string ip_r_nonprompt_str;
		std::string ip_phi_nonprompt_str;
		std::string ip_theta_nonprompt_str;

		std::string ip_x_prompt_str;
		std::string ip_y_prompt_str;
		std::string ip_z_prompt_str;
		std::string ip_x_nonprompt_str;
		std::string ip_y_nonprompt_str;
		std::string ip_z_nonprompt_str;

		ip_r_prompt_str     = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/prompt/calib_zmm" + m_year + "/ip" + m_bs + "_mag.root");
		ip_phi_prompt_str   = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/prompt/calib_zmm" + m_year + "/ip" + m_bs + "_phi.root");
		ip_theta_prompt_str = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/prompt/calib_zmm" + m_year + "/ip" + m_bs + "_theta.root");
		ip_r_nonprompt_str     = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/" + m_decayChannel + "/calib" + m_year + m_emb + "/ip" + m_bs + "_mag.root");
		ip_phi_nonprompt_str   = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/" + m_decayChannel + "/calib" + m_year + m_emb + "/ip" + m_bs + "_phi.root");
		ip_theta_nonprompt_str = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/" + m_decayChannel + "/calib" + m_year + m_emb + "/ip" + m_bs + "_theta.root");

		ip_x_prompt_str = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/prompt/calib_zmm" + m_year + "/ip" + m_bs + "_nx.root");
		ip_y_prompt_str = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/prompt/calib_zmm" + m_year + "/ip" + m_bs + "_ny.root");
		ip_z_prompt_str = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/prompt/calib_zmm" + m_year + "/ip" + m_bs + "_nz.root");
		ip_x_nonprompt_str = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/" + m_decayChannel + "/calib" + m_year + m_emb + "/ip" + m_bs + "_nx.root");
		ip_y_nonprompt_str = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/" + m_decayChannel + "/calib" + m_year + m_emb + "/ip" + m_bs + "_ny.root");
		ip_z_nonprompt_str = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/" + m_decayChannel + "/calib" + m_year + m_emb + "/ip" + m_bs + "_nz.root");

		TFile inputFilePrompt_ip_r(ip_r_prompt_str.c_str(), "READ");
		m_ip_r_prompt_isomap = static_cast<TGraph*>(inputFilePrompt_ip_r.Get("isomap"));
		inputFilePrompt_ip_r.Close();

		TFile inputFilePrompt_ip_theta(ip_theta_prompt_str.c_str(), "READ");
		m_ip_theta_prompt_isomap = static_cast<TGraph*>(inputFilePrompt_ip_theta.Get("isomap"));
		inputFilePrompt_ip_theta.Close();

		TFile inputFilePrompt_ip_phi(ip_phi_prompt_str.c_str(), "READ");
		m_ip_phi_prompt_isomap = static_cast<TGraph*>(inputFilePrompt_ip_phi.Get("isomap"));
		inputFilePrompt_ip_phi.Close();

		TFile inputFileNonPrompt_ip_r(ip_r_nonprompt_str.c_str(), "READ");
		m_ip_r_nonprompt_isomap = static_cast<TGraph*>(inputFileNonPrompt_ip_r.Get("isomap"));
		inputFileNonPrompt_ip_r.Close();

		TFile inputFileNonPrompt_ip_theta(ip_theta_nonprompt_str.c_str(), "READ");
		m_ip_theta_nonprompt_isomap = static_cast<TGraph*>(inputFileNonPrompt_ip_theta.Get("isomap"));
		inputFileNonPrompt_ip_theta.Close();

		TFile inputFileNonPrompt_ip_phi(ip_phi_nonprompt_str.c_str(), "READ");
		m_ip_phi_nonprompt_isomap = static_cast<TGraph*>(inputFileNonPrompt_ip_phi.Get("isomap"));
		inputFileNonPrompt_ip_phi.Close();

		TFile inputFilePrompt_ip_x(ip_x_prompt_str.c_str(), "READ");
		m_ip_x_prompt_isomap = static_cast<TGraph*>(inputFilePrompt_ip_x.Get("isomap"));
		inputFilePrompt_ip_x.Close();

		TFile inputFilePrompt_ip_y(ip_y_prompt_str.c_str(), "READ");
		m_ip_y_prompt_isomap = static_cast<TGraph*>(inputFilePrompt_ip_y.Get("isomap"));
		inputFilePrompt_ip_y.Close();

		TFile inputFilePrompt_ip_z(ip_z_prompt_str.c_str(), "READ");
		m_ip_z_prompt_isomap = static_cast<TGraph*>(inputFilePrompt_ip_z.Get("isomap"));
		inputFilePrompt_ip_z.Close();

		TFile inputFileNonPrompt_ip_x(ip_x_nonprompt_str.c_str(), "READ");
		m_ip_x_nonprompt_isomap = static_cast<TGraph*>(inputFileNonPrompt_ip_x.Get("isomap"));
		inputFileNonPrompt_ip_x.Close();

		TFile inputFileNonPrompt_ip_y(ip_y_nonprompt_str.c_str(), "READ");
		m_ip_y_nonprompt_isomap = static_cast<TGraph*>(inputFileNonPrompt_ip_y.Get("isomap"));
		inputFileNonPrompt_ip_y.Close();

		TFile inputFileNonPrompt_ip_z(ip_z_nonprompt_str.c_str(), "READ");
		m_ip_z_nonprompt_isomap = static_cast<TGraph*>(inputFileNonPrompt_ip_z.Get("isomap"));
		inputFileNonPrompt_ip_z.Close();

	}

	~IsomorphicMappingProxy()
	{
		// delete m_workspace;
	};

	double GetR(RMPoint IP, int gen_match, bool useCartesian){
		TVector3 calibIP;
		if(useCartesian){
			if(gen_match == 2 || gen_match == 1){
				calibIP.SetXYZ(m_ip_x_prompt_isomap->Eval(IP.X()),
							m_ip_y_prompt_isomap->Eval(IP.Y()),
							m_ip_z_prompt_isomap->Eval(IP.Z())
				);
			} else if ( (gen_match != 6) && (gen_match > 2) && (!m_onlyPrompt) ) {
				calibIP.SetXYZ(m_ip_x_nonprompt_isomap->Eval(IP.X()),
							m_ip_y_nonprompt_isomap->Eval(IP.Y()),
							m_ip_z_nonprompt_isomap->Eval(IP.Z())
				);
			} else {
				calibIP.SetXYZ(IP.X(), IP.Y(), IP.Z());
			}
		} else {
			if(gen_match == 2 || gen_match == 1){
				calibIP.SetMagThetaPhi(m_ip_r_prompt_isomap->Eval(IP.R()),
							m_ip_theta_prompt_isomap->Eval(IP.Theta()),
							m_ip_phi_prompt_isomap->Eval(IP.Phi())
				);
			} else if ( (gen_match != 6) && (gen_match > 2) && (!m_onlyPrompt) ) {
				calibIP.SetMagThetaPhi(m_ip_r_nonprompt_isomap->Eval(IP.R()),
							m_ip_theta_nonprompt_isomap->Eval(IP.Theta()),
							m_ip_phi_nonprompt_isomap->Eval(IP.Phi())
				);
			} else {
				calibIP.SetMagThetaPhi(IP.R(), IP.Theta(), IP.Phi());
			}
		}
		return calibIP.Mag();
	}
	double GetPhi(RMPoint IP, int gen_match, bool useCartesian){
		TVector3 calibIP;
		if(useCartesian){
			if(gen_match == 2 || gen_match == 1){
				calibIP.SetXYZ(m_ip_x_prompt_isomap->Eval(IP.X()),
							m_ip_y_prompt_isomap->Eval(IP.Y()),
							m_ip_z_prompt_isomap->Eval(IP.Z())
				);
			} else if ( (gen_match != 6) && (gen_match > 2) && (!m_onlyPrompt) ) {
				calibIP.SetXYZ(m_ip_x_nonprompt_isomap->Eval(IP.X()),
							m_ip_y_nonprompt_isomap->Eval(IP.Y()),
							m_ip_z_nonprompt_isomap->Eval(IP.Z())
				);
			} else {
				calibIP.SetXYZ(IP.X(), IP.Y(), IP.Z());
			}
		} else {
			if(gen_match == 2 || gen_match == 1){
				calibIP.SetMagThetaPhi(m_ip_r_prompt_isomap->Eval(IP.R()),
							m_ip_theta_prompt_isomap->Eval(IP.Theta()),
							m_ip_phi_prompt_isomap->Eval(IP.Phi())
				);
			} else if ( (gen_match != 6) && (gen_match > 2) && (!m_onlyPrompt) ) {
				calibIP.SetMagThetaPhi(m_ip_r_nonprompt_isomap->Eval(IP.R()),
							m_ip_theta_nonprompt_isomap->Eval(IP.Theta()),
							m_ip_phi_nonprompt_isomap->Eval(IP.Phi())
				);
			} else {
				calibIP.SetMagThetaPhi(IP.R(), IP.Theta(), IP.Phi());
			}
		}
		return calibIP.Phi();
	}
	double GetTheta(RMPoint IP, int gen_match, bool useCartesian){
		TVector3 calibIP;
		if(useCartesian){
			if(gen_match == 2 || gen_match == 1){
				calibIP.SetXYZ(m_ip_x_prompt_isomap->Eval(IP.X()),
							m_ip_y_prompt_isomap->Eval(IP.Y()),
							m_ip_z_prompt_isomap->Eval(IP.Z())
				);
			} else if ( (gen_match != 6) && (gen_match > 2) && (!m_onlyPrompt) ) {
				calibIP.SetXYZ(m_ip_x_nonprompt_isomap->Eval(IP.X()),
							m_ip_y_nonprompt_isomap->Eval(IP.Y()),
							m_ip_z_nonprompt_isomap->Eval(IP.Z())
				);
			} else {
				calibIP.SetXYZ(IP.X(), IP.Y(), IP.Z());
			}
		} else {
			if(gen_match == 2 || gen_match == 1){
				calibIP.SetMagThetaPhi(m_ip_r_prompt_isomap->Eval(IP.R()),
							m_ip_theta_prompt_isomap->Eval(IP.Theta()),
							m_ip_phi_prompt_isomap->Eval(IP.Phi())
				);
			} else if ( (gen_match != 6) && (gen_match > 2) && (!m_onlyPrompt) ) {
				calibIP.SetMagThetaPhi(m_ip_r_nonprompt_isomap->Eval(IP.R()),
							m_ip_theta_nonprompt_isomap->Eval(IP.Theta()),
							m_ip_phi_nonprompt_isomap->Eval(IP.Phi())
				);
			} else {
				calibIP.SetMagThetaPhi(IP.R(), IP.Theta(), IP.Phi());
			}
		}
		return calibIP.Theta();
	}
	double GetX(RMPoint IP, int gen_match, bool useCartesian){
		TVector3 calibIP;
		if(useCartesian){
			if(gen_match == 2 || gen_match == 1){
				calibIP.SetXYZ(m_ip_x_prompt_isomap->Eval(IP.X()),
							m_ip_y_prompt_isomap->Eval(IP.Y()),
							m_ip_z_prompt_isomap->Eval(IP.Z())
				);
			} else if ( (gen_match != 6) && (gen_match > 2) && (!m_onlyPrompt) ) {
				calibIP.SetXYZ(m_ip_x_nonprompt_isomap->Eval(IP.X()),
							m_ip_y_nonprompt_isomap->Eval(IP.Y()),
							m_ip_z_nonprompt_isomap->Eval(IP.Z())
				);
			} else {
				calibIP.SetXYZ(IP.X(), IP.Y(), IP.Z());
			}
		} else {
			if(gen_match == 2 || gen_match == 1){
				calibIP.SetMagThetaPhi(m_ip_r_prompt_isomap->Eval(IP.R()),
							m_ip_theta_prompt_isomap->Eval(IP.Theta()),
							m_ip_phi_prompt_isomap->Eval(IP.Phi())
				);
			} else if ( (gen_match != 6) && (gen_match > 2) && (!m_onlyPrompt) ) {
				calibIP.SetMagThetaPhi(m_ip_r_nonprompt_isomap->Eval(IP.R()),
							m_ip_theta_nonprompt_isomap->Eval(IP.Theta()),
							m_ip_phi_nonprompt_isomap->Eval(IP.Phi())
				);
			} else {
				calibIP.SetMagThetaPhi(IP.R(), IP.Theta(), IP.Phi());
			}
		}
		return calibIP.X();
	}
	double GetY(RMPoint IP, int gen_match, bool useCartesian){
		TVector3 calibIP;
		if(useCartesian){
			if(gen_match == 2 || gen_match == 1){
				calibIP.SetXYZ(m_ip_x_prompt_isomap->Eval(IP.X()),
							m_ip_y_prompt_isomap->Eval(IP.Y()),
							m_ip_z_prompt_isomap->Eval(IP.Z())
				);
			} else if ( (gen_match != 6) && (gen_match > 2) && (!m_onlyPrompt) ) {
				calibIP.SetXYZ(m_ip_x_nonprompt_isomap->Eval(IP.X()),
							m_ip_y_nonprompt_isomap->Eval(IP.Y()),
							m_ip_z_nonprompt_isomap->Eval(IP.Z())
				);
			} else {
				calibIP.SetXYZ(IP.X(), IP.Y(), IP.Z());
			}
		} else {
			if(gen_match == 2 || gen_match == 1){
				calibIP.SetMagThetaPhi(m_ip_r_prompt_isomap->Eval(IP.R()),
							m_ip_theta_prompt_isomap->Eval(IP.Theta()),
							m_ip_phi_prompt_isomap->Eval(IP.Phi())
				);
			} else if ( (gen_match != 6) && (gen_match > 2) && (!m_onlyPrompt) ) {
				calibIP.SetMagThetaPhi(m_ip_r_nonprompt_isomap->Eval(IP.R()),
							m_ip_theta_nonprompt_isomap->Eval(IP.Theta()),
							m_ip_phi_nonprompt_isomap->Eval(IP.Phi())
				);
			} else {
				calibIP.SetMagThetaPhi(IP.R(), IP.Theta(), IP.Phi());
			}
		}
		return calibIP.Y();
	}
	double GetZ(RMPoint IP, int gen_match, bool useCartesian){
		TVector3 calibIP;
		if(useCartesian){
			if(gen_match == 2 || gen_match == 1){
				calibIP.SetXYZ(m_ip_x_prompt_isomap->Eval(IP.X()),
							m_ip_y_prompt_isomap->Eval(IP.Y()),
							m_ip_z_prompt_isomap->Eval(IP.Z())
				);
			} else if ( (gen_match != 6) && (gen_match > 2) && (!m_onlyPrompt) ) {
				calibIP.SetXYZ(m_ip_x_nonprompt_isomap->Eval(IP.X()),
							m_ip_y_nonprompt_isomap->Eval(IP.Y()),
							m_ip_z_nonprompt_isomap->Eval(IP.Z())
				);
			} else {
				calibIP.SetXYZ(IP.X(), IP.Y(), IP.Z());
			}
		} else {
			if(gen_match == 2 || gen_match == 1){
				calibIP.SetMagThetaPhi(m_ip_r_prompt_isomap->Eval(IP.R()),
							m_ip_theta_prompt_isomap->Eval(IP.Theta()),
							m_ip_phi_prompt_isomap->Eval(IP.Phi())
				);
			} else if ( (gen_match != 6) && (gen_match > 2) && (!m_onlyPrompt) ) {
				calibIP.SetMagThetaPhi(m_ip_r_nonprompt_isomap->Eval(IP.R()),
							m_ip_theta_nonprompt_isomap->Eval(IP.Theta()),
							m_ip_phi_nonprompt_isomap->Eval(IP.Phi())
				);
			} else {
				calibIP.SetMagThetaPhi(IP.R(), IP.Theta(), IP.Phi());
			}
		}
		return calibIP.Z();
	}

private:
	std::string m_decayChannel;
	std::string m_ipVersion;
	std::string m_year = "";
	std::string m_bs = "";
	std::string m_emb = "";
	bool m_onlyPrompt = false;

	TGraph* m_ip_r_prompt_isomap = nullptr;
	TGraph* m_ip_theta_prompt_isomap = nullptr;
	TGraph* m_ip_phi_prompt_isomap = nullptr;

	TGraph* m_ip_r_nonprompt_isomap = nullptr;
	TGraph* m_ip_theta_nonprompt_isomap = nullptr;
	TGraph* m_ip_phi_nonprompt_isomap = nullptr;

	TGraph* m_ip_x_prompt_isomap = nullptr;
	TGraph* m_ip_y_prompt_isomap = nullptr;
	TGraph* m_ip_z_prompt_isomap = nullptr;

	TGraph* m_ip_x_nonprompt_isomap = nullptr;
	TGraph* m_ip_y_nonprompt_isomap = nullptr;
	TGraph* m_ip_z_nonprompt_isomap = nullptr;
};
