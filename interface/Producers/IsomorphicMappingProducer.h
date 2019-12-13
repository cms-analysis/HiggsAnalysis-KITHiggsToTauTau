#pragma once

#include "Artus/Utility/interface/Utility.h"


#include "Kappa/DataFormats/interface/Kappa.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "Artus/Utility/interface/DefaultValues.h"

/**
   \brief
*/

class IsomorphicMappingProducer : public ProducerBase<HttTypes> {
	private:
		bool m_isData;
		bool m_isEmbedding;
		std::string m_year;
		std::string m_decayChannel;
		std::string m_emb;

		TGraph* m_ipHelrPV_r_prompt_isomap = nullptr;
		TGraph* m_ipHelrPV_theta_prompt_isomap = nullptr;
		TGraph* m_ipHelrPV_phi_prompt_isomap = nullptr;
		TGraph* m_ipHelrPV_x_prompt_isomap = nullptr;
		TGraph* m_ipHelrPV_y_prompt_isomap = nullptr;
		TGraph* m_ipHelrPV_z_prompt_isomap = nullptr;

		TGraph* m_ipHelrPV_r_muon_isomap = nullptr;
		TGraph* m_ipHelrPV_theta_muon_isomap = nullptr;
		TGraph* m_ipHelrPV_phi_muon_isomap = nullptr;
		TGraph* m_ipHelrPV_x_muon_isomap = nullptr;
		TGraph* m_ipHelrPV_y_muon_isomap = nullptr;
		TGraph* m_ipHelrPV_z_muon_isomap = nullptr;

		TGraph* m_ipHelrPV_r_pion_isomap = nullptr;
		TGraph* m_ipHelrPV_theta_pion_isomap = nullptr;
		TGraph* m_ipHelrPV_phi_pion_isomap = nullptr;
		TGraph* m_ipHelrPV_x_pion_isomap = nullptr;
		TGraph* m_ipHelrPV_y_pion_isomap = nullptr;
		TGraph* m_ipHelrPV_z_pion_isomap = nullptr;

		TGraph* m_ipHelrPVBS_r_prompt_isomap = nullptr;
		TGraph* m_ipHelrPVBS_theta_prompt_isomap = nullptr;
		TGraph* m_ipHelrPVBS_phi_prompt_isomap = nullptr;
		TGraph* m_ipHelrPVBS_x_prompt_isomap = nullptr;
		TGraph* m_ipHelrPVBS_y_prompt_isomap = nullptr;
		TGraph* m_ipHelrPVBS_z_prompt_isomap = nullptr;

		TGraph* m_ipHelrPVBS_r_muon_isomap = nullptr;
		TGraph* m_ipHelrPVBS_theta_muon_isomap = nullptr;
		TGraph* m_ipHelrPVBS_phi_muon_isomap = nullptr;
		TGraph* m_ipHelrPVBS_x_muon_isomap = nullptr;
		TGraph* m_ipHelrPVBS_y_muon_isomap = nullptr;
		TGraph* m_ipHelrPVBS_z_muon_isomap = nullptr;

		TGraph* m_ipHelrPVBS_r_pion_isomap = nullptr;
		TGraph* m_ipHelrPVBS_theta_pion_isomap = nullptr;
		TGraph* m_ipHelrPVBS_phi_pion_isomap = nullptr;
		TGraph* m_ipHelrPVBS_x_pion_isomap = nullptr;
		TGraph* m_ipHelrPVBS_y_pion_isomap = nullptr;
		TGraph* m_ipHelrPVBS_z_pion_isomap = nullptr;

	public:
		TVector3 CalibrateIPHelrPVBS(TVector3 IP, int gen_match, bool isMuon) const {
			TVector3 calibIP;
			if(gen_match == 2 || gen_match == 1){
				calibIP.SetMagThetaPhi(m_ipHelrPVBS_r_prompt_isomap->Eval(IP.Mag()),
							m_ipHelrPVBS_theta_prompt_isomap->Eval(IP.Theta()),
							m_ipHelrPVBS_phi_prompt_isomap->Eval(IP.Phi())
				);
			} else if ( (gen_match != 6) && (gen_match > 2) && isMuon ) {
				calibIP.SetMagThetaPhi(m_ipHelrPVBS_r_muon_isomap->Eval(IP.Mag()),
							m_ipHelrPVBS_theta_muon_isomap->Eval(IP.Theta()),
							m_ipHelrPVBS_phi_muon_isomap->Eval(IP.Phi())
				);
			} else if ( (gen_match != 6) && (gen_match > 2) && !isMuon ) {
				calibIP.SetMagThetaPhi(m_ipHelrPVBS_r_pion_isomap->Eval(IP.Mag()),
							m_ipHelrPVBS_theta_pion_isomap->Eval(IP.Theta()),
							m_ipHelrPVBS_phi_pion_isomap->Eval(IP.Phi())
				);
			} else {

				calibIP.SetMagThetaPhi(IP.Mag(),
							IP.Theta(),
							IP.Phi()
				);
			}
			return calibIP;
		}

		const TVector3 CalibrateIPHelrPV(TVector3 IP, int gen_match, bool isMuon) const {
			TVector3 calibIP;
			if(gen_match == 2 || gen_match == 1){
				calibIP.SetMagThetaPhi(m_ipHelrPV_r_prompt_isomap->Eval(IP.Mag()),
							m_ipHelrPV_theta_prompt_isomap->Eval(IP.Theta()),
							m_ipHelrPV_phi_prompt_isomap->Eval(IP.Phi())
				);
			} else if ( (gen_match != 6) && (gen_match > 2) && isMuon ) {
				calibIP.SetMagThetaPhi(m_ipHelrPV_r_muon_isomap->Eval(IP.Mag()),
							m_ipHelrPV_theta_muon_isomap->Eval(IP.Theta()),
							m_ipHelrPV_phi_muon_isomap->Eval(IP.Phi())
				);
			} else if ( (gen_match != 6) && (gen_match > 2) && !isMuon ) {
				calibIP.SetMagThetaPhi(m_ipHelrPV_r_pion_isomap->Eval(IP.Mag()),
							m_ipHelrPV_theta_pion_isomap->Eval(IP.Theta()),
							m_ipHelrPV_phi_pion_isomap->Eval(IP.Phi())
				);
			} else {

				calibIP.SetMagThetaPhi(IP.Mag(),
							IP.Theta(),
							IP.Phi()
				);
			}
			return calibIP;
		}
		/*
		TVector3 CalibrateIP(TVector3 IP, int gen_match, TGraph* ip_r_prompt_isomap, TGraph* ip_theta_prompt_isomap, TGraph* ip_phi_prompt_isomap, TGraph* ip_r_nonprompt_isomap, TGraph* ip_theta_nonprompt_isomap, TGraph* ip_phi_nonprompt_isomap){
			TVector3 calibIP;
			if(gen_match == 2 || gen_match == 1){
				calibIP.SetMagThetaPhi(ip_r_prompt_isomap->Eval(IP.Mag()),
							ip_theta_prompt_isomap->Eval(IP.Theta()),
							ip_phi_prompt_isomap->Eval(IP.Phi())
				);
			} else if ( (gen_match != 6) && (gen_match > 2) ) {
				calibIP.SetMagThetaPhi(ip_r_nonprompt_isomap->Eval(IP.Mag()),
							ip_theta_nonprompt_isomap->Eval(IP.Theta()),
							ip_phi_nonprompt_isomap->Eval(IP.Phi())
				);
			} else {
				calibIP.SetMagThetaPhi(IP.Mag(),
							IP.Theta(),
							IP.Phi()
				);
			}
			return calibIP;
		}
		*/

		virtual std::string GetProducerId() const override;

		virtual void Init(setting_type const& settings, metadata_type& metadata)  override;

		virtual void Produce(event_type const& event, product_type& product, setting_type const& settings, metadata_type const& metadata) const override;
};
