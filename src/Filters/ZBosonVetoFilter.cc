
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/ZBosonVetoFilter.h"


bool ZBosonVetoFilter::DoesEventPass(event_type const& event,
                                     product_type const& product,
                                     setting_type const& settings) const
{
	return (product.m_diLeptonSystem.mass() < (65.5 + 3. * product.m_met->p4.Pt()/8) ||
	        product.m_diLeptonSystem.mass() > (108.0 - 1. * product.m_met->p4.Pt()/4) ||
	        product.m_diLeptonSystem.mass() < (79.0 - 3. * product.m_met->p4.Pt()/4) ||
	        product.m_diLeptonSystem.mass() > (99.0 + 1. * product.m_met->p4.Pt()/2)
	        );
}
