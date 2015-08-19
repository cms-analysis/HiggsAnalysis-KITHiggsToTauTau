
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
		this->m_event.m_mvaMetTT = this->SecureFileInterfaceGet<KMET>(settings.GetMvaMetTT(), false);
	if(! settings.GetMvaMetMT().empty())
		this->m_event.m_mvaMetMT = this->SecureFileInterfaceGet<KMET>(settings.GetMvaMetMT(), false);
	if(! settings.GetMvaMetET().empty())
		this->m_event.m_mvaMetET = this->SecureFileInterfaceGet<KMET>(settings.GetMvaMetET(), false);
	if(! settings.GetMvaMetEM().empty())
		this->m_event.m_mvaMetEM = this->SecureFileInterfaceGet<KMET>(settings.GetMvaMetEM(), false);
	
	// (New) MVA MET collections
	if(! settings.GetMvaMetsTT().empty())
		this->m_event.m_mvaMetsTT = this->SecureFileInterfaceGet<KMETs>(settings.GetMvaMetsTT());
	if(! settings.GetMvaMetsMT().empty())
		this->m_event.m_mvaMetsMT = this->SecureFileInterfaceGet<KMETs>(settings.GetMvaMetsMT());
	if(! settings.GetMvaMetsET().empty())
		this->m_event.m_mvaMetsET = this->SecureFileInterfaceGet<KMETs>(settings.GetMvaMetsET());
	if(! settings.GetMvaMetsEM().empty())
		this->m_event.m_mvaMetsEM = this->SecureFileInterfaceGet<KMETs>(settings.GetMvaMetsEM());
	
}

