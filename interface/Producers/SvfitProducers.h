
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/SvfitTools.h"


/** Producer for SVfit
 */
class SvfitProducer: public ProducerBase<HttTypes> {
public:

	SvfitProducer(
			std::string name="",
			float diTauMassConstraint=-1.0,
			SvfitEventKey product_type::*svfitEventKeyMember=&product_type::m_svfitEventKey,
			SvfitResults product_type::*svfitResultsMember=&product_type::m_svfitResults,
			std::map<KLepton*, RMFLV> product_type::*svfitTausMember=&product_type::m_svfitTaus,
			std::string (setting_type::*GetSvfitCacheFileMember)(void) const=&setting_type::GetSvfitCacheFile,
			std::string (setting_type::*GetSvfitCacheFileFolderMember)(void) const=&setting_type::GetSvfitCacheFileFolder,
			std::string (setting_type::*GetSvfitCacheTreeMember)(void) const=&setting_type::GetSvfitCacheTree
	);

	virtual std::string GetProducerId() const override;
	
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;

private:
	std::string m_name = "";
	float m_diTauMassConstraint = -1.0;
	mutable SvfitEventKey product_type::*m_svfitEventKeyMember;
	mutable SvfitResults product_type::*m_svfitResultsMember;
	std::map<KLepton*, RMFLV> product_type::*m_svfitTausMember;
	std::string (setting_type::*GetSvfitCacheFileMember)(void) const;
	std::string (setting_type::*GetSvfitCacheFileFolderMember)(void) const;
	std::string (setting_type::*GetSvfitCacheTreeMember)(void) const;
	
	HttEnumTypes::SvfitCacheMissBehaviour m_svfitCacheMissBehaviour;
	mutable SvfitTools svfitTools;

};


class SvfitM91Producer: public SvfitProducer {
public:

	SvfitM91Producer();
	
	virtual std::string GetProducerId() const override;

};


class SvfitM125Producer: public SvfitProducer {
public:

	SvfitM125Producer();
	
	virtual std::string GetProducerId() const override;

};

