
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/SvfitTools.h"

// https://github.com/cms-analysis/HiggsAnalysis-ZZMatrixElement/tree/v2.1.1/MELA
// https://github.com/JHUGen/JHUGenMELA
// https://twiki.cern.ch/twiki/bin/viewauth/CMS/MELAProject
// http://hroskes.web.cern.ch/hroskes/JHUGen/manJHUGenerator.pdf
#include "JHUGenMELA/MELA/interface/Mela.h"


class MELAProducer: public ProducerBase<HttTypes>
{
public:
	
	MELAProducer(
			std::string name="",
			SvfitResults product_type::*m_svfitResultsMember=&product_type::m_svfitResults,
			
			float product_type::*m_melaProbCPEvenGGHMember = &product_type::m_melaProbCPEvenGGH,
			float product_type::*m_melaProbCPOddGGHMember = &product_type::m_melaProbCPOddGGH,
			float product_type::*m_melaProbCPMixGGHMember = &product_type::m_melaProbCPMixGGH,
			float product_type::*m_melaDiscriminatorD0MinusGGHMember = &product_type::m_melaDiscriminatorD0MinusGGH,
			float product_type::*m_melaDiscriminatorDCPGGHMember = &product_type::m_melaDiscriminatorDCPGGH,
	
			float product_type::*m_melaProbCPEvenVBFMember = &product_type::m_melaProbCPEvenVBF,
			float product_type::*m_melaProbCPOddVBFMember = &product_type::m_melaProbCPOddVBF,
			float product_type::*m_melaProbCPMixVBFMember = &product_type::m_melaProbCPMixVBF,
			float product_type::*m_melaDiscriminatorD0MinusVBFMember = &product_type::m_melaDiscriminatorD0MinusVBF,
			float product_type::*m_melaDiscriminatorDCPVBFMember = &product_type::m_melaDiscriminatorDCPVBF
	
			/*
			float product_type::*m_melaProbCPEvenWlepHMember = &product_type::m_melaProbCPEvenWlepH,
			float product_type::*m_melaProbCPOddWlepHMember = &product_type::m_melaProbCPOddWlepH,
			float product_type::*m_melaProbCPMixWlepHMember = &product_type::m_melaProbCPMixWlepH,
			float product_type::*m_melaDiscriminatorD0MinusWlepHMember = &product_type::m_melaDiscriminatorD0MinusWlepH,
			float product_type::*m_melaDiscriminatorDCPWlepHMember = &product_type::m_melaDiscriminatorDCPWlepH,
	
			float product_type::*m_melaProbCPEvenWhadHMember = &product_type::m_melaProbCPEvenWhadH,
			float product_type::*m_melaProbCPOddWhadHMember = &product_type::m_melaProbCPOddWhadH,
			float product_type::*m_melaProbCPMixWhadHMember = &product_type::m_melaProbCPMixWhadH,
			float product_type::*m_melaDiscriminatorD0MinusWhadHMember = &product_type::m_melaDiscriminatorD0MinusWhadH,
			float product_type::*m_melaDiscriminatorDCPWhadHMember = &product_type::m_melaDiscriminatorDCPWhadH,
	
			float product_type::*m_melaProbCPEvenZlepHMember = &product_type::m_melaProbCPEvenZlepH,
			float product_type::*m_melaProbCPOddZlepHMember = &product_type::m_melaProbCPOddZlepH,
			float product_type::*m_melaProbCPMixZlepHMember = &product_type::m_melaProbCPMixZlepH,
			float product_type::*m_melaDiscriminatorD0MinusZlepHMember = &product_type::m_melaDiscriminatorD0MinusZlepH,
			float product_type::*m_melaDiscriminatorDCPZlepHMember = &product_type::m_melaDiscriminatorDCPZlepH,
	
			float product_type::*m_melaProbCPEvenZhadHMember = &product_type::m_melaProbCPEvenZhadH,
			float product_type::*m_melaProbCPOddZhadHMember = &product_type::m_melaProbCPOddZhadH,
			float product_type::*m_melaProbCPMixZhadHMember = &product_type::m_melaProbCPMixZhadH,
			float product_type::*m_melaDiscriminatorD0MinusZhadHMember = &product_type::m_melaDiscriminatorD0MinusZhadH,
			float product_type::*m_melaDiscriminatorDCPZhadHMember = &product_type::m_melaDiscriminatorDCPZhadH
			*/
	);

	virtual std::string GetProducerId() const override;

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type& product,
						 setting_type const& settings, metadata_type const& metadata) const override;

private:

	std::string m_name = "";
	SvfitResults product_type::*m_svfitResultsMember;
	
	float product_type::*m_melaProbCPEvenGGHMember;
	float product_type::*m_melaProbCPOddGGHMember;
	float product_type::*m_melaProbCPMixGGHMember;
	float product_type::*m_melaDiscriminatorD0MinusGGHMember;
	float product_type::*m_melaDiscriminatorDCPGGHMember;
	
	float product_type::*m_melaProbCPEvenVBFMember;
	float product_type::*m_melaProbCPOddVBFMember;
	float product_type::*m_melaProbCPMixVBFMember;
	float product_type::*m_melaDiscriminatorD0MinusVBFMember;
	float product_type::*m_melaDiscriminatorDCPVBFMember;
	
	/*
	float product_type::*m_melaProbCPEvenWlepHMember;
	float product_type::*m_melaProbCPOddWlepHMember;
	float product_type::*m_melaProbCPMixWlepHMember;
	float product_type::*m_melaDiscriminatorD0MinusWlepHMember;
	float product_type::*m_melaDiscriminatorDCPWlepHMember;
	
	float product_type::*m_melaProbCPEvenWhadHMember;
	float product_type::*m_melaProbCPOddWhadHMember;
	float product_type::*m_melaProbCPMixWhadHMember;
	float product_type::*m_melaDiscriminatorD0MinusWhadHMember;
	float product_type::*m_melaDiscriminatorDCPWhadHMember;
	
	float product_type::*m_melaProbCPEvenZlepHMember;
	float product_type::*m_melaProbCPOddZlepHMember;
	float product_type::*m_melaProbCPMixZlepHMember;
	float product_type::*m_melaDiscriminatorD0MinusZlepHMember;
	float product_type::*m_melaDiscriminatorDCPZlepHMember;
	
	float product_type::*m_melaProbCPEvenZhadHMember;
	float product_type::*m_melaProbCPOddZhadHMember;
	float product_type::*m_melaProbCPMixZhadHMember;
	float product_type::*m_melaDiscriminatorD0MinusZhadHMember;
	float product_type::*m_melaDiscriminatorDCPZhadHMember;
	*/

	std::unique_ptr<Mela> m_mela;
	
	void CalculateProbabilitiesGGH(float& probCPEven, float& probCPOdd, float& probCPMix) const;
	void CalculateProbabilitiesVBF(float& probCPEven, float& probCPOdd, float& probCPMix) const;
	void CalculateProbabilitiesWlepH(float& probCPEven, float& probCPOdd, float& probCPMix) const;
	void CalculateProbabilitiesWhadH(float& probCPEven, float& probCPOdd, float& probCPMix) const;
	void CalculateProbabilitiesZlepH(float& probCPEven, float& probCPOdd, float& probCPMix) const;
	void CalculateProbabilitiesZhadH(float& probCPEven, float& probCPOdd, float& probCPMix) const;
	
	void CalculateDiscriminators(float probCPEven, float probCPOdd, float probCPMix,
	                             float& discriminatorD0Minus, float& discriminatorDCP) const;

};


class MELAM125Producer: public MELAProducer
{
public:
	
	MELAM125Producer();
	
	virtual std::string GetProducerId() const override;

};

