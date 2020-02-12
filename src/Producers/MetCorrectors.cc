
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MetCorrectors.h"
#include <boost/algorithm/string/split.hpp>
#include <boost/algorithm/string.hpp>

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

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "uncorrmet", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_pfmetUncorr->p4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genpX", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_pfmetCorrections[0];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genpY", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_pfmetCorrections[1];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "vispX", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_pfmetCorrections[2];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "vispY", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_pfmetCorrections[3];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pfMetCorr", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_pfmet.p4.Pt();
	});

	// m_correctGlobalMet = !settings.GetChooseMvaMet();
	m_correctGlobalMet = (HttEnumTypes::ToMetType(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy((settings.GetChooseMet)()))) == HttEnumTypes::MetType::PFMET);
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

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mvaMetUncorr", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_mvametUncorr->p4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mvaMetCorrectionGenPx", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_mvametCorrections[0];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mvaMetCorrectionGenPy", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_mvametCorrections[1];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mvaMetCorrectionVisPx", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_mvametCorrections[2];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mvaMetCorrectionVisPy", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_mvametCorrections[3];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mvaMetCorr", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_mvamet.p4.Pt();
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genpX", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_mvametCorrections.size() > 0 ? SafeMap::Get(metadata.m_commonFloatQuantities, std::string("mvaMetCorrectionGenPx"))(event, product, settings, metadata) : DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genpY", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_mvametCorrections.size() > 0 ? SafeMap::Get(metadata.m_commonFloatQuantities, std::string("mvaMetCorrectionGenPy"))(event, product, settings, metadata) : DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "vispX", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_mvametCorrections.size() > 0 ? SafeMap::Get(metadata.m_commonFloatQuantities, std::string("mvaMetCorrectionVisPx"))(event, product, settings, metadata) : DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "vispY", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_mvametCorrections.size() > 0 ? SafeMap::Get(metadata.m_commonFloatQuantities, std::string("mvaMetCorrectionVisPy"))(event, product, settings, metadata) : DefaultValues::UndefinedFloat;
	});

	// m_correctGlobalMet = settings.GetChooseMvaMet();
	m_correctGlobalMet = (HttEnumTypes::ToMetType(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy((settings.GetChooseMet)()))) == HttEnumTypes::MetType::MVAMET);
}

std::string MvaMetCorrector::GetProducerId() const
{
	return "MvaMetCorrector";
}


PuppiMetCorrector::PuppiMetCorrector() :
	MetCorrectorBase(&HttTypes::product_type::m_puppiMetUncorr,
			 &HttTypes::product_type::m_puppimet,
			 &HttTypes::product_type::m_puppimetCorrections,
			 &HttTypes::setting_type::GetPuppiMetRecoilCorrectorFile,
			 &HttTypes::setting_type::GetPuppiMetShiftCorrectorFile,
			 &HttTypes::setting_type::GetUpdateMetWithCorrectedLeptons
	)
{
}

void PuppiMetCorrector::Init(setting_type const& settings, metadata_type& metadata)
{
	MetCorrectorBase<KMET>::Init(settings, metadata);

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "puppiMetuncorr", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_puppiMetUncorr->p4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genpX", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_puppimetCorrections[0];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genpY", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_puppimetCorrections[1];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "vispX", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_puppimetCorrections[2];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "vispY", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_puppimetCorrections[3];
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "puppiMetCorr", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		return product.m_puppimet.p4.Pt();
	});

	m_correctGlobalMet = (HttEnumTypes::ToMetType(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy((settings.GetChooseMet)()))) == HttEnumTypes::MetType::PUPPIMET);
}

std::string PuppiMetCorrector::GetProducerId() const
{
	return "PuppiMetCorrector";
}
