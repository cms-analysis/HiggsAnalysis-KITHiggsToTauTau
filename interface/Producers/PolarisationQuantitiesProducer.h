
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

#include <TLorentzVector.h>


/** Producer for tau polarisation quantities.
 */
class PolarisationQuantitiesProducerBase: public ProducerBase<HttTypes> {
public:

	PolarisationQuantitiesProducerBase(
			std::string name,
			std::map<KLepton*, RMFLV> product_type::*fittedTausMember,
			std::map<KLepton*, double> product_type::*polarisationOmegasMember,
			std::map<KLepton*, double> product_type::*polarisationOmegaBarsMember,
			std::map<KLepton*, double> product_type::*polarisationOmegaVisiblesMember,
			double product_type::*polarisationCombinedOmegaMember,
			double product_type::*polarisationCombinedOmegaBarMember,
			double product_type::*polarisationCombinedOmegaVisibleMember
	);
	
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;

protected:
	std::string m_name;
	std::map<KLepton*, RMFLV> product_type::*m_fittedTausMember;
	std::map<KLepton*, double> product_type::*m_polarisationOmegasMember;
	std::map<KLepton*, double> product_type::*m_polarisationOmegaBarsMember;
	std::map<KLepton*, double> product_type::*m_polarisationOmegaVisiblesMember;
	double product_type::*m_polarisationCombinedOmegaMember;
	double product_type::*m_polarisationCombinedOmegaBarMember;
	double product_type::*m_polarisationCombinedOmegaVisibleMember;

private:
	std::vector<TLorentzVector> GetInputLepton(product_type& product, KLepton* lepton) const;
	std::vector<TLorentzVector> GetInputPion(product_type& product, KLepton* lepton) const;
	std::vector<TLorentzVector> GetInputRho(product_type& product, KLepton* lepton) const;
	std::vector<TLorentzVector> GetInputA1(product_type& product, KLepton* lepton) const;

};


class PolarisationQuantitiesSvfitProducer: public PolarisationQuantitiesProducerBase {
public:

	PolarisationQuantitiesSvfitProducer();
	virtual std::string GetProducerId() const override;
};

class PolarisationQuantitiesSimpleFitProducer: public PolarisationQuantitiesProducerBase {
public:

	PolarisationQuantitiesSimpleFitProducer();
	virtual std::string GetProducerId() const override;
};

/*
class PolarisationQuantitiesHHKinFitProducer: public PolarisationQuantitiesProducerBase {
public:

	PolarisationQuantitiesHHKinFitProducer();
	virtual std::string GetProducerId() const override;
};
*/
