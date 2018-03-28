
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
			std::map<KLepton*, float> product_type::*polarisationOmegasMember,
			std::map<KLepton*, float> product_type::*polarisationOmegaBarsMember,
			std::map<KLepton*, float> product_type::*polarisationOmegaVisiblesMember,
			float product_type::*polarisationCombinedOmegaMember,
			float product_type::*polarisationCombinedOmegaBarMember,
			float product_type::*polarisationCombinedOmegaVisibleMember,
			bool genMatched = false
	);
	
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;

private:
	std::string m_name;
	std::map<KLepton*, RMFLV> product_type::*m_fittedTausMember;
	std::map<KLepton*, float> product_type::*m_polarisationOmegasMember;
	std::map<KLepton*, float> product_type::*m_polarisationOmegaBarsMember;
	std::map<KLepton*, float> product_type::*m_polarisationOmegaVisiblesMember;
	float product_type::*m_polarisationCombinedOmegaMember;
	float product_type::*m_polarisationCombinedOmegaBarMember;
	float product_type::*m_polarisationCombinedOmegaVisibleMember;
	bool m_genMatched = false;
	
	std::vector<TLorentzVector> GetInputLepton(product_type& product, KLepton* lepton, bool genMatched=false) const;
	std::vector<TLorentzVector> GetInputPion(product_type& product, KLepton* lepton, bool genMatched=false) const;
	std::vector<TLorentzVector> GetInputRho(product_type& product, KLepton* lepton, bool genMatched=false) const;
	std::vector<TLorentzVector> GetInputA1(product_type& product, KLepton* lepton, bool genMatched=false) const;

};


class GenMatchedPolarisationQuantitiesProducer: public PolarisationQuantitiesProducerBase {
public:

	GenMatchedPolarisationQuantitiesProducer();
	virtual std::string GetProducerId() const override;
};


class PolarisationQuantitiesSvfitProducer: public PolarisationQuantitiesProducerBase {
public:

	PolarisationQuantitiesSvfitProducer();
	virtual std::string GetProducerId() const override;
};

class PolarisationQuantitiesSvfitM91Producer: public PolarisationQuantitiesProducerBase {
public:

	PolarisationQuantitiesSvfitM91Producer();
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
