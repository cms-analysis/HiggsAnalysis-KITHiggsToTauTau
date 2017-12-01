
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"

// https://github.com/cms-analysis/HiggsAnalysis-ZZMatrixElement/tree/v2.1.1/MELA
// https://twiki.cern.ch/twiki/bin/viewauth/CMS/MELAProject
// http://hroskes.web.cern.ch/hroskes/JHUGen/manJHUGenerator.pdf
#include "ZZMatrixElement/MELA/interface/Mela.h"


class MELAProducer: public ProducerBase<HttTypes>
{
public:

	virtual std::string GetProducerId() const override;

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type& product,
						 setting_type const& settings, metadata_type const& metadata) const override;

private:
	void CalculateProbabilitiesGGH(float& probCPEven, float& probCPOdd, float& probCPMix) const;
	void CalculateProbabilitiesVBF(float& probCPEven, float& probCPOdd, float& probCPMix) const;
	void CalculateProbabilitiesWlepH(float& probCPEven, float& probCPOdd, float& probCPMix) const;
	void CalculateProbabilitiesWhadH(float& probCPEven, float& probCPOdd, float& probCPMix) const;
	void CalculateProbabilitiesZlepH(float& probCPEven, float& probCPOdd, float& probCPMix) const;
	void CalculateProbabilitiesZhadH(float& probCPEven, float& probCPOdd, float& probCPMix) const;
	
	void CalculateDiscriminators(float probCPEven, float probCPOdd, float probCPMix,
	                             float& discriminatorD0Minus, float& discriminatorDCP) const;

	std::unique_ptr<Mela> m_mela;

};

