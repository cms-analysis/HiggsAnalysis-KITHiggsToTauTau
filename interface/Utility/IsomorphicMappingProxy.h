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
	IsomorphicMappingProxy(std::string decaychannel, std::string ipVersion, std::string year, bool onlyPrompt=false)
	{
		m_ipVersion = ipVersion;
		m_year = year;
		m_onlyPrompt = onlyPrompt;

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

		ip_r_prompt_str     = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/prompt/calib_zmm" + m_year + "/ip" + m_bs + "_mag.root");
		ip_phi_prompt_str   = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/prompt/calib_zmm" + m_year + "/ip" + m_bs + "_phi.root");
		ip_theta_prompt_str = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/prompt/calib_zmm" + m_year + "/ip" + m_bs + "_theta.root");
		ip_r_nonprompt_str     = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/" + m_decayChannel + "/calib" + m_year + "_emb/ip" + m_bs + "_mag.root");
		ip_phi_nonprompt_str   = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/" + m_decayChannel + "/calib" + m_year + "_emb/ip" + m_bs + "_phi.root");
		ip_theta_nonprompt_str = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/" + m_decayChannel + "/calib" + m_year + "_emb/ip" + m_bs + "_theta.root");

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

	}

	~IsomorphicMappingProxy()
	{
		// delete m_workspace;
	};

	double GetR(RMPoint IP, int gen_match){
		if(gen_match == 2 || gen_match == 1){
			m_calibIP.SetMagThetaPhi(m_ip_r_prompt_isomap->Eval(IP.R()),
						m_ip_theta_prompt_isomap->Eval(IP.Theta()),
						m_ip_phi_prompt_isomap->Eval(IP.Phi())
			);
		} else if ( (gen_match != 6) && (gen_match > 2) && (!m_onlyPrompt) ) {
			m_calibIP.SetMagThetaPhi(m_ip_r_nonprompt_isomap->Eval(IP.R()),
						m_ip_theta_nonprompt_isomap->Eval(IP.Theta()),
						m_ip_phi_nonprompt_isomap->Eval(IP.Phi())
			);
		} else {
			m_calibIP.SetMagThetaPhi(IP.R(),
						IP.Theta(),
						IP.Phi()
			);
		}
		return m_calibIP.Mag();
	}
	double GetPhi(RMPoint IP, int gen_match){
		if(gen_match == 2 || gen_match == 1){
			m_calibIP.SetMagThetaPhi(m_ip_r_prompt_isomap->Eval(IP.R()),
						m_ip_theta_prompt_isomap->Eval(IP.Theta()),
						m_ip_phi_prompt_isomap->Eval(IP.Phi())
			);
		} else if ( (gen_match != 6) && (gen_match > 2) && (!m_onlyPrompt) ) {
			m_calibIP.SetMagThetaPhi(m_ip_r_nonprompt_isomap->Eval(IP.R()),
						m_ip_theta_nonprompt_isomap->Eval(IP.Theta()),
						m_ip_phi_nonprompt_isomap->Eval(IP.Phi())
			);
		} else {
			m_calibIP.SetMagThetaPhi(IP.R(),
						IP.Theta(),
						IP.Phi()
			);
		}

		return m_calibIP.Phi();
	}
	double GetTheta(RMPoint IP, int gen_match){
		if(gen_match == 2 || gen_match == 1){
			m_calibIP.SetMagThetaPhi(m_ip_r_prompt_isomap->Eval(IP.R()),
						m_ip_theta_prompt_isomap->Eval(IP.Theta()),
						m_ip_phi_prompt_isomap->Eval(IP.Phi())
			);
		} else if ( (gen_match != 6) && (gen_match > 2) && (!m_onlyPrompt) ) {
			m_calibIP.SetMagThetaPhi(m_ip_r_nonprompt_isomap->Eval(IP.R()),
						m_ip_theta_nonprompt_isomap->Eval(IP.Theta()),
						m_ip_phi_nonprompt_isomap->Eval(IP.Phi())
			);
		} else {
			m_calibIP.SetMagThetaPhi(IP.R(),
						IP.Theta(),
						IP.Phi()
			);
		}

		return m_calibIP.Theta();
	}
	double GetX(RMPoint IP, int gen_match){
		if(gen_match == 2 || gen_match == 1){
			m_calibIP.SetMagThetaPhi(m_ip_r_prompt_isomap->Eval(IP.R()),
						m_ip_theta_prompt_isomap->Eval(IP.Theta()),
						m_ip_phi_prompt_isomap->Eval(IP.Phi())
			);
		} else if ( (gen_match != 6) && (gen_match > 2) && (!m_onlyPrompt) ) {
			m_calibIP.SetMagThetaPhi(m_ip_r_nonprompt_isomap->Eval(IP.R()),
						m_ip_theta_nonprompt_isomap->Eval(IP.Theta()),
						m_ip_phi_nonprompt_isomap->Eval(IP.Phi())
			);
		} else {
			m_calibIP.SetMagThetaPhi(IP.R(),
						IP.Theta(),
						IP.Phi()
			);
		}

		return m_calibIP.X();
	}
	double GetY(RMPoint IP, int gen_match){
		if(gen_match == 2 || gen_match == 1){
			m_calibIP.SetMagThetaPhi(m_ip_r_prompt_isomap->Eval(IP.R()),
						m_ip_theta_prompt_isomap->Eval(IP.Theta()),
						m_ip_phi_prompt_isomap->Eval(IP.Phi())
			);
		} else if ( (gen_match != 6) && (gen_match > 2) && (!m_onlyPrompt) ) {
			m_calibIP.SetMagThetaPhi(m_ip_r_nonprompt_isomap->Eval(IP.R()),
						m_ip_theta_nonprompt_isomap->Eval(IP.Theta()),
						m_ip_phi_nonprompt_isomap->Eval(IP.Phi())
			);
		} else {
			m_calibIP.SetMagThetaPhi(IP.R(),
						IP.Theta(),
						IP.Phi()
			);
		}

		return m_calibIP.Y();
	}
	double GetZ(RMPoint IP, int gen_match){
		if(gen_match == 2 || gen_match == 1){
			m_calibIP.SetMagThetaPhi(m_ip_r_prompt_isomap->Eval(IP.R()),
						m_ip_theta_prompt_isomap->Eval(IP.Theta()),
						m_ip_phi_prompt_isomap->Eval(IP.Phi())
			);
		} else if ( (gen_match != 6) && (gen_match > 2) && (!m_onlyPrompt) ) {
			m_calibIP.SetMagThetaPhi(m_ip_r_nonprompt_isomap->Eval(IP.R()),
						m_ip_theta_nonprompt_isomap->Eval(IP.Theta()),
						m_ip_phi_nonprompt_isomap->Eval(IP.Phi())
			);
		} else {
			m_calibIP.SetMagThetaPhi(IP.R(),
						IP.Theta(),
						IP.Phi()
			);
		}

		return m_calibIP.Z();
	}

private:
	std::string m_decayChannel;
	std::string m_ipVersion;
	std::string m_year = "";
	std::string m_bs = "";
	bool m_onlyPrompt = false;
	TVector3 m_IP;
	TVector3 m_calibIP;

	TGraph* m_ip_r_prompt_isomap = nullptr;
	TGraph* m_ip_theta_prompt_isomap = nullptr;
	TGraph* m_ip_phi_prompt_isomap = nullptr;

	TGraph* m_ip_r_nonprompt_isomap = nullptr;
	TGraph* m_ip_theta_nonprompt_isomap = nullptr;
	TGraph* m_ip_phi_nonprompt_isomap = nullptr;
};
