
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MetCorrectors.h"


MetCorrector::MetCorrector() :
	MetCorrectorBase(&HttTypes::product_type::m_pfmetUncorr,
			 &HttTypes::product_type::m_pfmet,
			 &HttTypes::product_type::m_pfmetCorrections,
			 &HttTypes::setting_type::GetMetRecoilCorrectorFile,
			 &HttTypes::setting_type::GetMetShiftCorrectorFile,
			 &HttTypes::setting_type::GetUpdateMetWithCorrectedLeptons
	)
{
}

void MetCorrector::Init(setting_type const& settings, metadata_type& metadata)
{
	MetCorrectorBase<KMET>::Init(settings, metadata);
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("uncorrmet", [](event_type const& event, product_type const& product) {
		return product.m_pfmetUncorr->p4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genpX", [](event_type const& event, product_type const& product) {
		return product.m_pfmetCorrections[0];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genpY", [](event_type const& event, product_type const& product) {
		return product.m_pfmetCorrections[1];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("vispX", [](event_type const& event, product_type const& product) {
		return product.m_pfmetCorrections[2];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("vispY", [](event_type const& event, product_type const& product) {
		return product.m_pfmetCorrections[3];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pfMetCorr", [](event_type const& event, product_type const& product) {
		return product.m_pfmet.p4.Pt();
	});

	m_correctGlobalMet = !settings.GetChooseMvaMet();
}

std::string MetCorrector::GetProducerId() const
{
	return "MetCorrector";
}


MvaMetCorrector::MvaMetCorrector() :
	MetCorrectorBase(&HttTypes::product_type::m_mvametUncorr,
			 &HttTypes::product_type::m_mvamet,
			 &HttTypes::product_type::m_mvametCorrections,
			 &HttTypes::setting_type::GetMvaMetRecoilCorrectorFile,
			 &HttTypes::setting_type::GetMvaMetShiftCorrectorFile,
			 &HttTypes::setting_type::GetUpdateMetWithCorrectedLeptons
	)
{
}

void MvaMetCorrector::Init(setting_type const& settings, metadata_type& metadata)
{
	MetCorrectorBase<KMET>::Init(settings, metadata);
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mvaMetUncorr", [](event_type const& event, product_type const& product) {
		return product.m_mvametUncorr->p4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mvaMetCorrectionGenPx", [](event_type const& event, product_type const& product) {
		return product.m_mvametCorrections[0];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mvaMetCorrectionGenPy", [](event_type const& event, product_type const& product) {
		return product.m_mvametCorrections[1];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mvaMetCorrectionVisPx", [](event_type const& event, product_type const& product) {
		return product.m_mvametCorrections[2];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mvaMetCorrectionVisPy", [](event_type const& event, product_type const& product) {
		return product.m_mvametCorrections[3];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mvaMetCorr", [](event_type const& event, product_type const& product) {
		return product.m_mvamet.p4.Pt();
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genpX", [](event_type const& event, product_type const& product)
	{
		return product.m_mvametCorrections.size() > 0 ? LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["mvaMetCorrectionGenPx"](event, product) : DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genpY", [](event_type const& event, product_type const& product)
	{
		return product.m_mvametCorrections.size() > 0 ? LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["mvaMetCorrectionGenPy"](event, product) : DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("vispX", [](event_type const& event, product_type const& product)
	{
		return product.m_mvametCorrections.size() > 0 ? LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["mvaMetCorrectionVisPx"](event, product) : DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("vispY", [](event_type const& event, product_type const& product)
	{
		return product.m_mvametCorrections.size() > 0 ? LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["mvaMetCorrectionVisPy"](event, product) : DefaultValues::UndefinedFloat;
	});

	m_correctGlobalMet = settings.GetChooseMvaMet();
}

std::string MvaMetCorrector::GetProducerId() const
{
	return "MvaMetCorrector";
}
