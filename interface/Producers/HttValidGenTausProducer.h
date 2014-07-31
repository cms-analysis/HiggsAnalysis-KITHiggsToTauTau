
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "Artus/Utility/interface/Utility.h"

/**
   \brief Fill lists of generator taus in compareable to the Lists of reconstructed particles
   This producer needs the m_genTaus vector from Artus filled.
*/

class HttValidGenTausProducer: public ProducerBase<HttTypes>
{

public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE
	{
		std::cout << "getproducerid" << std::endl;
		return "valid_gen_taus";
	}

	virtual void Init(setting_type const& settings)  ARTUS_CPP11_OVERRIDE;
	virtual void Produce(event_type const& event, product_type& product,
						 setting_type const& settings) const ARTUS_CPP11_OVERRIDE;

	template <typename T>
	bool doesGenRecoMatch(std::vector<T> const recoTaus, std::vector<KDataGenTau*> const genTaus) const;

private:
	double m_deltaR;
	bool m_validateMatching;
	bool m_swapIfNecessary;
	void validateMatching(event_type const& event, product_type& product,
						  setting_type const& settings) const;
	void sortVectors(event_type const& event, product_type& product,
					 setting_type const& settings) const;
	void copyVectors(event_type const& event, product_type& product,
					 setting_type const& settings) const;

};

