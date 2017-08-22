
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEventProvider.h"

/**
   \brief class to connect the analysis specific event content to the pipelines.
*/


HttEventProvider::HttEventProvider(FileInterface2 & fileInterface, InputTypeEnum inpType, bool batchMode) :
		KappaEventProvider<HttTypes>(fileInterface, inpType, batchMode)
{

}

void HttEventProvider::WireEvent(setting_type const& settings)
{
	KappaEventProvider::WireEvent(settings);
	
	// (Old) MVA MET collections
	if(! settings.GetMvaMetTT().empty())
		this->m_event.m_mvaMetTT = this->SecureFileInterfaceGetEvent<KMET>(settings.GetMvaMetTT(), false);
	if(! settings.GetMvaMetMT().empty())
		this->m_event.m_mvaMetMT = this->SecureFileInterfaceGetEvent<KMET>(settings.GetMvaMetMT(), false);
	if(! settings.GetMvaMetET().empty())
		this->m_event.m_mvaMetET = this->SecureFileInterfaceGetEvent<KMET>(settings.GetMvaMetET(), false);
	if(! settings.GetMvaMetEM().empty())
		this->m_event.m_mvaMetEM = this->SecureFileInterfaceGetEvent<KMET>(settings.GetMvaMetEM(), false);
	
	// (New) MVA MET collections
	if(! settings.GetMvaMetsTT().empty())
		this->m_event.m_mvaMetsTT = this->SecureFileInterfaceGetEvent<KMETs>(settings.GetMvaMetsTT());
	if(! settings.GetMvaMetsMT().empty())
		this->m_event.m_mvaMetsMT = this->SecureFileInterfaceGetEvent<KMETs>(settings.GetMvaMetsMT());
	if(! settings.GetMvaMetsET().empty())
		this->m_event.m_mvaMetsET = this->SecureFileInterfaceGetEvent<KMETs>(settings.GetMvaMetsET());
	if(! settings.GetMvaMetsEM().empty())
		this->m_event.m_mvaMetsEM = this->SecureFileInterfaceGetEvent<KMETs>(settings.GetMvaMetsEM());
	if(! settings.GetMvaMets().empty())
		this->m_event.m_mvaMets = this->SecureFileInterfaceGetEvent<KMETs>(settings.GetMvaMets());
	
}

