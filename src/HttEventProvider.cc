
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEventProvider.h"

/**
   \brief class to connect the analysis specific event content to the pipelines.
*/


HttEventProvider::HttEventProvider(FileInterface2 & fileInterface, InputTypeEnum inpType) :
		KappaEventProvider<HttTypes>(fileInterface, inpType)
{

}

void HttEventProvider::WireEvent(global_setting_type const& globalSettings)
{
	KappaEventProvider::WireEvent(globalSettings);
	
	// MET infos
	if(! globalSettings.GetMvaMetTT().empty())
		this->m_event.m_mvaMetTT = this->SecureFileInterfaceGet<KDataPFMET>(globalSettings.GetMvaMetTT());
	if(! globalSettings.GetMvaMetMT().empty())
		this->m_event.m_mvaMetMT = this->SecureFileInterfaceGet<KDataPFMET>(globalSettings.GetMvaMetMT());
	if(! globalSettings.GetMvaMetET().empty())
		this->m_event.m_mvaMetET = this->SecureFileInterfaceGet<KDataPFMET>(globalSettings.GetMvaMetET());
	if(! globalSettings.GetMvaMetEM().empty())
		this->m_event.m_mvaMetEM = this->SecureFileInterfaceGet<KDataPFMET>(globalSettings.GetMvaMetEM());
	
}

