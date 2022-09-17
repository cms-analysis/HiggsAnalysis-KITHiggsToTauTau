#pragma once

#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


class SimpleFitProducer: public ProducerBase<HttTypes>
{
public:

	virtual std::string GetProducerId() const override;

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;

	static TMatrixT<double> ComputeLorentzVectorPar(TMatrixT<double> &inpar);
	static TVectorD EigenValues(TMatrixTSym<double> M);
	static TMatrixTSym<double> RegulariseCovariance(TMatrixTSym<double>  M, double coef);

protected:

	float m_massConstraint;
	bool m_useCollinearityTauMu;
	bool m_useMVADecayModes;
	std::string m_minimizer;
};

class SimpleFitThreeProngThreeProngProducer: public SimpleFitProducer
{
public:

	virtual std::string GetProducerId() const override{
		return "SimpleFitThreeProngThreeProngProducer";
	};

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;

};