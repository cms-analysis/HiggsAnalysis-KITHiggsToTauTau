
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "Artus/Utility/interface/Utility.h"
#include <Math/VectorUtil.h>

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
		return "HttValidGenTausProducer";
	}

	virtual void Init(setting_type const& settings)  ARTUS_CPP11_OVERRIDE;
	virtual void Produce(event_type const& event, product_type& product,
						 setting_type const& settings) const ARTUS_CPP11_OVERRIDE;

	template <typename T>
	bool DoesGenRecoMatch(std::vector<T> const recoTaus, std::vector<KDataGenTau*> const genTaus) const
	{
		if (recoTaus.size() != genTaus.size())
			return false;

		for (unsigned int i = 0; i < recoTaus.size(); i++)
		{
			float deltaR = ROOT::Math::VectorUtil::DeltaR(recoTaus.at(i)->p4, genTaus.at(i)->p4_vis);
			if (deltaR > m_deltaR)
				return false;
		}
		return true;
	}

private:
	double m_deltaR;
	bool m_validateMatching;
	bool m_swapIfNecessary;
	void ValidateMatching(event_type const& event, product_type& product,
						  setting_type const& settings) const;
	void SortVectors(event_type const& event, product_type& product,
					 setting_type const& settings) const;
	void CopyVectors(event_type const& event, product_type& product,
					 setting_type const& settings) const;

};

