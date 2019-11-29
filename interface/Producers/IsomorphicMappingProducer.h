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

		TGraph* ip_1_x_isomap = nullptr;
		TGraph* ip_1_y_isomap = nullptr;
		TGraph* ip_1_z_isomap = nullptr;
		// Do this better
		TGraph* ip_1_r_isomap = nullptr;
		TGraph* ip_1_theta_isomap = nullptr;
		TGraph* ip_1_phi_isomap = nullptr;
		TGraph* ip_2_r_isomap = nullptr;
		TGraph* ip_2_theta_isomap = nullptr;
		TGraph* ip_2_phi_isomap = nullptr;
		TGraph* iprPV_1_r_isomap = nullptr;
		TGraph* iprPV_1_theta_isomap = nullptr;
		TGraph* iprPV_1_phi_isomap = nullptr;
		TGraph* iprPV_2_r_isomap = nullptr;
		TGraph* iprPV_2_theta_isomap = nullptr;
		TGraph* iprPV_2_phi_isomap = nullptr;
		TGraph* iprPVBS_1_r_isomap = nullptr;
		TGraph* iprPVBS_1_theta_isomap = nullptr;
		TGraph* iprPVBS_1_phi_isomap = nullptr;
		TGraph* iprPVBS_2_r_isomap = nullptr;
		TGraph* iprPVBS_2_theta_isomap = nullptr;
		TGraph* iprPVBS_2_phi_isomap = nullptr;

		TGraph* ipHel_1_r_isomap = nullptr;
		TGraph* ipHel_1_theta_isomap = nullptr;
		TGraph* ipHel_1_phi_isomap = nullptr;
		TGraph* ipHel_2_r_isomap = nullptr;
		TGraph* ipHel_2_theta_isomap = nullptr;
		TGraph* ipHel_2_phi_isomap = nullptr;
		TGraph* ipHelrPV_1_r_isomap = nullptr;
		TGraph* ipHelrPV_1_theta_isomap = nullptr;
		TGraph* ipHelrPV_1_phi_isomap = nullptr;
		TGraph* ipHelrPV_2_r_isomap = nullptr;
		TGraph* ipHelrPV_2_theta_isomap = nullptr;
		TGraph* ipHelrPV_2_phi_isomap = nullptr;
		TGraph* ipHelrPVBS_1_r_isomap = nullptr;
		TGraph* ipHelrPVBS_1_theta_isomap = nullptr;
		TGraph* ipHelrPVBS_1_phi_isomap = nullptr;
		TGraph* ipHelrPVBS_2_r_isomap = nullptr;
		TGraph* ipHelrPVBS_2_theta_isomap = nullptr;
		TGraph* ipHelrPVBS_2_phi_isomap = nullptr;


	public:

		virtual std::string GetProducerId() const override;

		virtual void Init(setting_type const& settings, metadata_type& metadata)  override;

		virtual void Produce(event_type const& event, product_type& product, setting_type const& settings, metadata_type const& metadata) const override;
};
