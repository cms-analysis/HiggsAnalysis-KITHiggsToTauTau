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

		TGraph* m_ipHelrPV_x_prompt_isomap = nullptr;
		TGraph* m_ipHelrPV_y_prompt_isomap = nullptr;
		TGraph* m_ipHelrPV_z_prompt_isomap = nullptr;

		TGraph* m_ipHelrPV_x_muon_isomap = nullptr;
		TGraph* m_ipHelrPV_y_muon_isomap = nullptr;
		TGraph* m_ipHelrPV_z_muon_isomap = nullptr;

		TGraph* m_ipHelrPV_x_pion_isomap = nullptr;
		TGraph* m_ipHelrPV_y_pion_isomap = nullptr;
		TGraph* m_ipHelrPV_z_pion_isomap = nullptr;

		TGraph* m_ipHelrPVBS_x_prompt_isomap = nullptr;
		TGraph* m_ipHelrPVBS_y_prompt_isomap = nullptr;
		TGraph* m_ipHelrPVBS_z_prompt_isomap = nullptr;

		TGraph* m_ipHelrPVBS_x_muon_isomap = nullptr;
		TGraph* m_ipHelrPVBS_y_muon_isomap = nullptr;
		TGraph* m_ipHelrPVBS_z_muon_isomap = nullptr;

		TGraph* m_ipHelrPVBS_x_pion_isomap = nullptr;
		TGraph* m_ipHelrPVBS_y_pion_isomap = nullptr;
		TGraph* m_ipHelrPVBS_z_pion_isomap = nullptr;

	public:
		TVector3 CalibrateIPHelrPVBS(TVector3 IP, int gen_match, bool isMuon) const {
			TVector3 calibIP;
			if(gen_match == 2 || gen_match == 1){
				calibIP.SetXYZ(m_ipHelrPVBS_x_prompt_isomap->Eval(IP.X()),
							m_ipHelrPVBS_y_prompt_isomap->Eval(IP.Y()),
							m_ipHelrPVBS_z_prompt_isomap->Eval(IP.Z())
				);
			} else if ( (gen_match != 6) && (gen_match > 2) && isMuon ) {
				calibIP.SetXYZ(m_ipHelrPVBS_x_muon_isomap->Eval(IP.X()),
							m_ipHelrPVBS_y_muon_isomap->Eval(IP.Y()),
							m_ipHelrPVBS_z_muon_isomap->Eval(IP.Z())
				);
			} else if ( (gen_match != 6) && (gen_match > 2) && !isMuon ) {
				calibIP.SetXYZ(m_ipHelrPVBS_x_pion_isomap->Eval(IP.X()),
							m_ipHelrPVBS_y_pion_isomap->Eval(IP.Y()),
							m_ipHelrPVBS_z_pion_isomap->Eval(IP.Z())
				);
			} else {

				calibIP.SetXYZ(IP.X(),
							IP.Y(),
							IP.Z()
				);
			}
			return calibIP;
		}

		const TVector3 CalibrateIPHelrPV(TVector3 IP, int gen_match, bool isMuon) const {
			TVector3 calibIP;
			if(gen_match == 2 || gen_match == 1){
				calibIP.SetXYZ(m_ipHelrPV_x_prompt_isomap->Eval(IP.X()),
							m_ipHelrPV_y_prompt_isomap->Eval(IP.Y()),
							m_ipHelrPV_z_prompt_isomap->Eval(IP.Z())
				);
			} else if ( (gen_match != 6) && (gen_match > 2) && isMuon ) {
				calibIP.SetXYZ(m_ipHelrPV_x_muon_isomap->Eval(IP.X()),
							m_ipHelrPV_y_muon_isomap->Eval(IP.Y()),
							m_ipHelrPV_z_muon_isomap->Eval(IP.Z())
				);
			} else if ( (gen_match != 6) && (gen_match > 2) && !isMuon ) {
				calibIP.SetXYZ(m_ipHelrPV_x_pion_isomap->Eval(IP.X()),
							m_ipHelrPV_y_pion_isomap->Eval(IP.Y()),
							m_ipHelrPV_z_pion_isomap->Eval(IP.Z())
				);
			} else {

				calibIP.SetXYZ(IP.X(),
							IP.Y(),
							IP.Z()
				);
			}
			return calibIP;
		}

		virtual std::string GetProducerId() const override;

		virtual void Init(setting_type const& settings, metadata_type& metadata)  override;

		virtual void Produce(event_type const& event, product_type& product, setting_type const& settings, metadata_type const& metadata) const override;
};
