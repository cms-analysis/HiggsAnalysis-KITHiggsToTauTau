
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/DiLeptonVetoFilters.h"


DiVetoElectronVetoFilter::DiVetoElectronVetoFilter() :
	DiLeptonVetoFilterBase<KElectron>(&product_type::m_validVetoElectrons,
	                                  &setting_type::GetDiVetoElectronVetoMode)
{
}

DiVetoMuonVetoFilter::DiVetoMuonVetoFilter() :
	DiLeptonVetoFilterBase<KMuon>(&product_type::m_validVetoMuons,
	                              &setting_type::GetDiVetoMuonVetoMode)
{
}

