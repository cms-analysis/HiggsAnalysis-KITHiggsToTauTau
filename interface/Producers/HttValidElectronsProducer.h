
#pragma once

#include "Artus/KappaAnalysis/interface/Producers/ValidElectronsProducer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/**
   \brief GlobalProducer, for valid electrons.
   
   Required config tags in addtion to the ones of the base class:
   - ElectronIDType
   - ElectronChargedIsoVetoConeSizeEB (default given)
   - ElectronChargedIsoVetoConeSizeEE (default given)
   - ElectronNeutralIsoVetoConeSize (default given)
   - ElectronPhotonIsoVetoConeSizeEB (default given)
   - ElectronPhotonIsoVetoConeSizeEE (default given)
   - ElectronDeltaBetaIsoVetoConeSize (default given)
   - ElectronChargedIsoPtThreshold (default given)
   - ElectronNeutralIsoPtThreshold (default given)
   - ElectronPhotonIsoPtThreshold (default given)
   - ElectronDeltaBetaIsoPtThreshold (default given)
   - ElectronIsoSignalConeSize
   - ElectronDeltaBetaCorrectionFactor
   - ElectronIsoPtSumOverPtThresholdEB
   - ElectronIsoPtSumOverPtThresholdEE
*/

class HttValidElectronsProducer: public ValidElectronsProducer<HttTypes>
{

public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	enum class ElectronIDType : int
	{
		NONE  = -1,
		SUMMER2013LOOSE = 0,
		SUMMER2013TIGHT = 1,
	};
	static ElectronIDType ToElectronIDType(std::string const& electronIDType)
	{
		if (electronIDType == "summer2013loose") return ElectronIDType::SUMMER2013LOOSE;
		else if (electronIDType == "summer2013tight") return ElectronIDType::SUMMER2013TIGHT;
		else return ElectronIDType::NONE;
	}
	
	HttValidElectronsProducer(std::vector<KDataElectron*> product_type::*validElectrons=&product_type::m_validElectrons,
	                      std::vector<KDataElectron*> product_type::*invalidElectrons=&product_type::m_invalidElectrons,
	                      std::string (setting_type::*GetElectronID)(void) const=&setting_type::GetElectronID,
	                      std::string (setting_type::*GetElectronIsoType)(void) const=&setting_type::GetElectronIsoType,
	                      std::string (setting_type::*GetElectronIso)(void) const=&setting_type::GetElectronIso,
	                      std::string (setting_type::*GetElectronReco)(void) const=&setting_type::GetElectronReco,
	                      std::vector<std::string>& (setting_type::*GetLowerPtCuts)(void) const=&setting_type::GetElectronLowerPtCuts,
	                      std::vector<std::string>& (setting_type::*GetUpperAbsEtaCuts)(void) const=&setting_type::GetElectronUpperAbsEtaCuts);

	virtual void Init(setting_type const& settings) ARTUS_CPP11_OVERRIDE;


protected:

	// Htautau specific additional definitions
	virtual bool AdditionalCriteria(KDataElectron* electron, event_type const& event,
	                                product_type& product, setting_type const& settings) const  ARTUS_CPP11_OVERRIDE;


private:
	ElectronIDType electronIDType;
	
	bool IsMVANonTrigElectronHttSummer2013(KDataElectron* electron, bool tightID) const;
};

