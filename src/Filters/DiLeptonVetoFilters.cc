
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/DiLeptonVetoFilters.h"


DiVetoElectronVetoFilter::DiVetoElectronVetoFilter() :
	DiLeptonVetoFilterBase(&product_type::m_validVetoElectrons,
	                       &setting_type::GetDiVetoElectronVetoMode)
{
}

DiVetoMuonVetoFilter::DiVetoMuonVetoFilter() :
	DiLeptonVetoFilterBase(&product_type::m_validVetoMuons,
	                       &setting_type::GetDiVetoMuonVetoMode)
{
}

