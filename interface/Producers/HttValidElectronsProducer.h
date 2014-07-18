
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
	
	HttValidElectronsProducer(
			std::vector<KDataElectron*> product_type::*validElectrons=&product_type::m_validElectrons,
			std::vector<KDataElectron*> product_type::*invalidElectrons=&product_type::m_invalidElectrons,
			std::string (setting_type::*GetElectronID)(void) const=&setting_type::GetElectronID,
			std::string (setting_type::*GetElectronIDType)(void) const=&setting_type::GetElectronIDType,
			std::string (setting_type::*GetElectronIsoType)(void) const=&setting_type::GetElectronIsoType,
			std::string (setting_type::*GetElectronIso)(void) const=&setting_type::GetElectronIso,
			std::string (setting_type::*GetElectronReco)(void) const=&setting_type::GetElectronReco,
			std::vector<std::string>& (setting_type::*GetLowerPtCuts)(void) const=&setting_type::GetElectronLowerPtCuts,
			std::vector<std::string>& (setting_type::*GetUpperAbsEtaCuts)(void) const=&setting_type::GetElectronUpperAbsEtaCuts,
			float (setting_type::*GetElectronChargedIsoVetoConeSizeEB)(void) const=&setting_type::GetElectronChargedIsoVetoConeSizeEB,
			float (setting_type::*GetElectronChargedIsoVetoConeSizeEE)(void) const=&setting_type::GetElectronChargedIsoVetoConeSizeEE,
			float (setting_type::*GetElectronNeutralIsoVetoConeSize)(void) const=&setting_type::GetElectronNeutralIsoVetoConeSize,
			float (setting_type::*GetElectronPhotonIsoVetoConeSizeEB)(void) const=&setting_type::GetElectronPhotonIsoVetoConeSizeEB,
			float (setting_type::*GetElectronPhotonIsoVetoConeSizeEE)(void) const=&setting_type::GetElectronPhotonIsoVetoConeSizeEE,
			float (setting_type::*GetElectronDeltaBetaIsoVetoConeSize)(void) const=&setting_type::GetElectronDeltaBetaIsoVetoConeSize,
			float (setting_type::*GetElectronChargedIsoPtThreshold)(void) const=&setting_type::GetElectronChargedIsoPtThreshold,
			float (setting_type::*GetElectronNeutralIsoPtThreshold)(void) const=&setting_type::GetElectronNeutralIsoPtThreshold,
			float (setting_type::*GetElectronPhotonIsoPtThreshold)(void) const=&setting_type::GetElectronPhotonIsoPtThreshold,
			float (setting_type::*GetElectronDeltaBetaIsoPtThreshold)(void) const=&setting_type::GetElectronDeltaBetaIsoPtThreshold,
			float (setting_type::*GetElectronIsoSignalConeSize)(void) const=&setting_type::GetElectronIsoSignalConeSize,
			float (setting_type::*GetElectronDeltaBetaCorrectionFactor)(void) const=&setting_type::GetElectronDeltaBetaCorrectionFactor,
			float (setting_type::*GetElectronIsoPtSumOverPtThresholdEB)(void) const=&setting_type::GetElectronIsoPtSumOverPtThresholdEB,
			float (setting_type::*GetElectronIsoPtSumOverPtThresholdEE)(void) const=&setting_type::GetElectronIsoPtSumOverPtThresholdEE,
			float (setting_type::*GetElectronTrackDxyCut)(void) const=&setting_type::GetElectronTrackDxyCut,
			float (setting_type::*GetElectronTrackDzCut)(void) const=&setting_type::GetElectronTrackDzCut
	);

	virtual void Init(setting_type const& settings) ARTUS_CPP11_OVERRIDE;


protected:

	// Htautau specific additional definitions
	virtual bool AdditionalCriteria(KDataElectron* electron, event_type const& event,
	                                product_type& product, setting_type const& settings) const  ARTUS_CPP11_OVERRIDE;


private:
	std::string (setting_type::*GetElectronIDType)(void) const;
	float (setting_type::*GetElectronChargedIsoVetoConeSizeEB)(void) const;
	float (setting_type::*GetElectronChargedIsoVetoConeSizeEE)(void) const;
	float (setting_type::*GetElectronNeutralIsoVetoConeSize)(void) const;
	float (setting_type::*GetElectronPhotonIsoVetoConeSizeEB)(void) const;
	float (setting_type::*GetElectronPhotonIsoVetoConeSizeEE)(void) const;
	float (setting_type::*GetElectronDeltaBetaIsoVetoConeSize)(void) const;
	float (setting_type::*GetElectronChargedIsoPtThreshold)(void) const;
	float (setting_type::*GetElectronNeutralIsoPtThreshold)(void) const;
	float (setting_type::*GetElectronPhotonIsoPtThreshold)(void) const;
	float (setting_type::*GetElectronDeltaBetaIsoPtThreshold)(void) const;
	float (setting_type::*GetElectronIsoSignalConeSize)(void) const;
	float (setting_type::*GetElectronDeltaBetaCorrectionFactor)(void) const;
	float (setting_type::*GetElectronIsoPtSumOverPtThresholdEB)(void) const;
	float (setting_type::*GetElectronIsoPtSumOverPtThresholdEE)(void) const;
	float (setting_type::*GetElectronTrackDxyCut)(void) const;
	float (setting_type::*GetElectronTrackDzCut)(void) const;

	ElectronIDType electronIDType;
	
	bool IsMVANonTrigElectronHttSummer2013(KDataElectron* electron, bool tightID) const;
};


/**
 */
class HttValidLooseElectronsProducer: public HttValidElectronsProducer
{

public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "valid_loose_electrons";
	}
	
	HttValidLooseElectronsProducer(
			std::vector<KDataElectron*> product_type::*validElectrons=&product_type::m_validLooseElectrons,
			std::vector<KDataElectron*> product_type::*invalidElectrons=&product_type::m_invalidLooseElectrons,
			std::string (setting_type::*GetElectronID)(void) const=&setting_type::GetLooseElectronID,
			std::string (setting_type::*GetElectronIDType)(void) const=&setting_type::GetLooseElectronIDType,
			std::string (setting_type::*GetElectronIsoType)(void) const=&setting_type::GetLooseElectronIsoType,
			std::string (setting_type::*GetElectronIso)(void) const=&setting_type::GetLooseElectronIso,
			std::string (setting_type::*GetElectronReco)(void) const=&setting_type::GetLooseElectronReco,
			std::vector<std::string>& (setting_type::*GetLowerPtCuts)(void) const=&setting_type::GetLooseElectronLowerPtCuts,
			std::vector<std::string>& (setting_type::*GetUpperAbsEtaCuts)(void) const=&setting_type::GetLooseElectronUpperAbsEtaCuts,
			float (setting_type::*GetElectronChargedIsoVetoConeSizeEB)(void) const=&setting_type::GetElectronChargedIsoVetoConeSizeEB,
			float (setting_type::*GetElectronChargedIsoVetoConeSizeEE)(void) const=&setting_type::GetElectronChargedIsoVetoConeSizeEE,
			float (setting_type::*GetElectronNeutralIsoVetoConeSize)(void) const=&setting_type::GetElectronNeutralIsoVetoConeSize,
			float (setting_type::*GetElectronPhotonIsoVetoConeSizeEB)(void) const=&setting_type::GetElectronPhotonIsoVetoConeSizeEB,
			float (setting_type::*GetElectronPhotonIsoVetoConeSizeEE)(void) const=&setting_type::GetElectronPhotonIsoVetoConeSizeEE,
			float (setting_type::*GetElectronDeltaBetaIsoVetoConeSize)(void) const=&setting_type::GetElectronDeltaBetaIsoVetoConeSize,
			float (setting_type::*GetElectronChargedIsoPtThreshold)(void) const=&setting_type::GetElectronChargedIsoPtThreshold,
			float (setting_type::*GetElectronNeutralIsoPtThreshold)(void) const=&setting_type::GetElectronNeutralIsoPtThreshold,
			float (setting_type::*GetElectronPhotonIsoPtThreshold)(void) const=&setting_type::GetElectronPhotonIsoPtThreshold,
			float (setting_type::*GetElectronDeltaBetaIsoPtThreshold)(void) const=&setting_type::GetElectronDeltaBetaIsoPtThreshold,
			float (setting_type::*GetElectronIsoSignalConeSize)(void) const=&setting_type::GetElectronIsoSignalConeSize,
			float (setting_type::*GetElectronDeltaBetaCorrectionFactor)(void) const=&setting_type::GetElectronDeltaBetaCorrectionFactor,
			float (setting_type::*GetElectronIsoPtSumOverPtThresholdEB)(void) const=&setting_type::GetLooseElectronIsoPtSumOverPtThresholdEB,
			float (setting_type::*GetElectronIsoPtSumOverPtThresholdEE)(void) const=&setting_type::GetLooseElectronIsoPtSumOverPtThresholdEE,
			float (setting_type::*GetElectronTrackDxyCut)(void) const=&setting_type::GetElectronTrackDxyCut,
			float (setting_type::*GetElectronTrackDzCut)(void) const=&setting_type::GetElectronTrackDzCut
	);

};

