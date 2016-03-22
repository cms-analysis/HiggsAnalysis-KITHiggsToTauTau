
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MetCorrectors.h"


MetCorrector::MetCorrector() :
	MetCorrectorBase(&HttTypes::product_type::m_pfmet,
			 &HttTypes::setting_type::GetMetRecoilCorrectorFile
	)
{
}

std::string MetCorrector::GetProducerId() const
{
	return "MetCorrector";
}


MvaMetCorrector::MvaMetCorrector() :
	MetCorrectorBase(&HttTypes::product_type::m_met,
			 &HttTypes::setting_type::GetMvaMetRecoilCorrectorFile
	)
{
}

std::string MvaMetCorrector::GetProducerId() const
{
	return "MvaMetCorrector";
}
