#pragma once

#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/**
	\brief GlobalProducer, for CP studies of tau decays. Following quantities are calculated from the input of GenTauDecayProducer :

	-Phi* : this is a variable, with which one can say, whether the considered Higgs-Boson is a scalar (CP even) or a pseudoscalar (CP odd)
	-Psi*CP : this is a variable, with which one can figure out, whether the have a CP-mixture or not
*/

class GenTauCPProducerBase : public ProducerBase<HttTypes> {
public:

	GenTauCPProducerBase(std::string name);

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;

protected:
	std::vector<TLorentzVector> SetupInputsPion(product_type& product, KGenTau* genTau) const;
	std::vector<TLorentzVector> SetupInputsRho(product_type& product, KGenTau* genTau) const;
	std::vector<TLorentzVector> SetupInputsA1(product_type& product, KGenTau* genTau) const;

private:
	std::string m_name;
	std::vector<TLorentzVector> GetInputPion(product_type& product, KGenTau* genTau) const;
	std::vector<TLorentzVector> GetInputRho(product_type& product, KGenTau* genTau) const;
	std::vector<TLorentzVector> GetInputA1(product_type& product, KGenTau* genTau) const;
};

class GenTauCPProducer : public GenTauCPProducerBase {
public:

	GenTauCPProducer();

	virtual std::string GetProducerId() const override;

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;
};

class GenMatchedTauCPProducer : public GenTauCPProducerBase {
public:

	GenMatchedTauCPProducer();

	virtual std::string GetProducerId() const override;

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;

private:
	void FindGenTau(product_type& product) const;

	std::vector<TLorentzVector> GetInputPion(product_type& product, KLepton* lepton) const;
	std::vector<TLorentzVector> GetInputRho(product_type& product, KLepton* lepton) const;
	std::vector<TLorentzVector> GetInputA1(product_type& product, KLepton* lepton) const;
};
