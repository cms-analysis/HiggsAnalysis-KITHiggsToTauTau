
#pragma once

#include "Artus/KappaAnalysis/interface/Producers/TmvaClassificationReaderBase.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/**
   \brief Producer for discriminator agains TTbar (as used in the EM channel)
   
   Required config tags:
   - AntiTtbarTmvaInputQuantities
   - AntiTtbarTmvaMethods
   - AntiTtbarTmvaWeights (same length as for AntiTtbarTmvaMethods required)
*/
class AntiTtbarDiscriminatorTmvaReader: public TmvaClassificationReaderBase<HttTypes>
{
public:

	virtual std::string GetProducerId() const override
	{
		return "AntiTtbarDiscriminatorTmvaReader";
	}
	
	AntiTtbarDiscriminatorTmvaReader();
	
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
	
	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;

};

class TauPolarisationTmvaReader: public TmvaClassificationReaderBase<HttTypes>
{
public:

	virtual std::string GetProducerId() const override
	{
		return "TauPolarisationTmvaReader";
	}
	
	TauPolarisationTmvaReader();
	
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
	
	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;

};

class HttEventClassifierTmvaReader: public TmvaClassificationReaderBase<HttTypes>
{
public:

	virtual std::string GetProducerId() const override
	{
		return "HttEventClassifierTmvaReader";
	}

	HttEventClassifierTmvaReader();

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;

	// static std::vector<float> read_mva_scores(unsigned isEven, std::vector<float> vars);
	// virtual std::pair<float,int> getMaxScoreWithIndex(std::vector<float> vec);


	std::vector<float*> m_vars;
	// float var0_, var1_, var2_, var3_, var4_, var5_, var6_, var7_, var8_, var9_;

private:

	TMVA::Reader *reader_even_;
	TMVA::Reader *reader_odd_;

};

