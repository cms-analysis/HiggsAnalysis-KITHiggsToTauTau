
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/ZBosonVetoFilter.h"


void ZBosonVetoFilter::Init(setting_type const& settings, metadata_type& metadata)
{
	FilterBase<HttTypes>::Init(settings, metadata);
	
	vetoType = ToZBosonVetoType(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetZBosonVetoType())));
}

bool ZBosonVetoFilter::DoesEventPass(event_type const& event,
                                     product_type const& product,
                                     setting_type const& settings, metadata_type const& metadata) const
{
	bool validEvent = true;
	
	// Z boson veto optimized for ttH search in the dilepton channel
	// if different definitions are needed, simply add another ZBosonVetoType
	if (vetoType == ZBosonVetoType::HF) {
		
		validEvent = validEvent && (
		    product.m_diLeptonSystem.mass() < (65.5 + 3. * product.m_met.p4.Pt()/8) ||
		    product.m_diLeptonSystem.mass() > (108.0 - 1. * product.m_met.p4.Pt()/4) ||
		    product.m_diLeptonSystem.mass() < (79.0 - 3. * product.m_met.p4.Pt()/4) ||
		    product.m_diLeptonSystem.mass() > (99.0 + 1. * product.m_met.p4.Pt()/2)); 
	}
	
	else if (vetoType == ZBosonVetoType::LF) {
		
		validEvent = validEvent && !(
		    product.m_diLeptonSystem.mass() < (65.5 + 3. * product.m_met.p4.Pt()/8) ||
		    product.m_diLeptonSystem.mass() > (108.0 - 1. * product.m_met.p4.Pt()/4) ||
		    product.m_diLeptonSystem.mass() < (79.0 - 3. * product.m_met.p4.Pt()/4) ||
		    product.m_diLeptonSystem.mass() > (99.0 + 1. * product.m_met.p4.Pt()/2));
		    
		validEvent = validEvent && (std::abs(product.m_diLeptonSystem.mass() - 91.) < 10);
	}
	
	return validEvent;
}
