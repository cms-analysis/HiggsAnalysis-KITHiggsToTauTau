
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/FastMttTools.h"


/** Producer for FastMTT
 */
class FastMttProducer: public ProducerBase<HttTypes> {
public:

	FastMttProducer(
			std::string name="",
			FastMttResults product_type::*fastmttResultsMember=&product_type::m_fastmttResults,
			std::map<KLepton*, RMFLV> product_type::*fastmttTausMember=&product_type::m_fastmttTaus
	);

	virtual std::string GetProducerId() const override;
	
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;

private:
	std::string m_name = "";
	mutable FastMttResults product_type::*m_fastmttResultsMember;
	std::map<KLepton*, RMFLV> product_type::*m_fastmttTausMember;
	
	mutable FastMttTools fastmttTools;

};
