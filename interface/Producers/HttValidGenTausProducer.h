
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

	virtual std::string GetProducerId() const override
	{
		return "HttValidGenTausProducer";
	}

	virtual void Init(setting_type const& settings, metadata_type& metadata)  override;
	virtual void Produce(event_type const& event, product_type& product,
						 setting_type const& settings, metadata_type const& metadata) const override;

	template <typename T>
	bool DoesGenRecoMatch(std::vector<T> const recoTaus, std::vector<KGenTau*> const genTaus) const
	{
		if (recoTaus.size() != genTaus.size())
			return false;

		for (unsigned int i = 0; i < recoTaus.size(); i++)
		{
			float deltaR = ROOT::Math::VectorUtil::DeltaR(recoTaus.at(i)->p4, genTaus.at(i)->visible.p4);
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
						  setting_type const& settings, metadata_type const& metadata) const;
	void SortVectors(event_type const& event, product_type& product,
					 setting_type const& settings, metadata_type const& metadata) const;
	void CopyVectors(event_type const& event, product_type& product,
					 setting_type const& settings, metadata_type const& metadata) const;

};

