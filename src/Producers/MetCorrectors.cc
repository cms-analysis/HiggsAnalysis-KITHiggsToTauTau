
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MetCorrectors.h"


MetCorrector::MetCorrector() :
	MetCorrectorBase(&HttTypes::product_type::m_pfmet,
			 &HttTypes::product_type::m_pfmetCorrections,
			 &HttTypes::setting_type::GetMetRecoilCorrectorFile
	)
{
}

void MetCorrector::Init(setting_type const& settings)
{
	MetCorrectorBase<KMET>::Init(settings);
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pfMetUncorr", [](event_type const& event, product_type const& product) {
		return product.m_pfmetCorrections[0];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pfMetCorrectionGenPx", [](event_type const& event, product_type const& product) {
		return product.m_pfmetCorrections[1];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pfMetCorrectionGenPy", [](event_type const& event, product_type const& product) {
		return product.m_pfmetCorrections[2];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pfMetCorrectionVisPx", [](event_type const& event, product_type const& product) {
		return product.m_pfmetCorrections[3];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pfMetCorrectionVisPy", [](event_type const& event, product_type const& product) {
		return product.m_pfmetCorrections[4];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pfMetCorr", [](event_type const& event, product_type const& product) {
		return product.m_pfmetCorrections[5];
	});
}

std::string MetCorrector::GetProducerId() const
{
	return "MetCorrector";
}


MvaMetCorrector::MvaMetCorrector() :
	MetCorrectorBase(&HttTypes::product_type::m_met,
			 &HttTypes::product_type::m_metCorrections,
			 &HttTypes::setting_type::GetMvaMetRecoilCorrectorFile
	)
{
}

void MvaMetCorrector::Init(setting_type const& settings)
{
	MetCorrectorBase<KMET>::Init(settings);
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mvaMetUncorr", [](event_type const& event, product_type const& product) {
		return product.m_metCorrections[0];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mvaMetCorrectionGenPx", [](event_type const& event, product_type const& product) {
		return product.m_metCorrections[1];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mvaMetCorrectionGenPy", [](event_type const& event, product_type const& product) {
		return product.m_metCorrections[2];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mvaMetCorrectionVisPx", [](event_type const& event, product_type const& product) {
		return product.m_metCorrections[3];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mvaMetCorrectionVisPy", [](event_type const& event, product_type const& product) {
		return product.m_metCorrections[4];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mvaMetCorr", [](event_type const& event, product_type const& product) {
		return product.m_metCorrections[5];
	});
}

std::string MvaMetCorrector::GetProducerId() const
{
	return "MvaMetCorrector";
}
