
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
   - ElectronIsoPtSumOverPtLowerThresholdEB
   - ElectronIsoPtSumOverPtLowerThresholdEE
   - ElectronIsoPtSumOverPtUpperThresholdEB
   - ElectronIsoPtSumOverPtUpperThresholdEE
*/

class HttValidElectronsProducer: public ValidElectronsProducer<HttTypes>
{

public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	enum class ElectronIDType : int
	{
		INVALID = -2,
		NONE  = -1,
		SUMMER2013LOOSE = 0,
		SUMMER2013TIGHT = 1,
		SUMMER2013TTHTIGHT = 2,
		SUMMER2013TTHLOOSE = 3,
		PHYS14CUTBASEDLOOSE = 4,
		PHYS14CUTBASEDMEDIUM = 5,
		PHYS14CUTBASEDTIGHT = 6,
		PHYS14CUTBASEDVETO = 7,
		MVANONTRIGPHYS14LOOSE = 8,
		MVANONTRIGPHYS14TIGHT = 9,
		SPRING15CUTBASEDLOOSE = 10,
		SPRING15CUTBASEDMEDIUM = 11,
		SPRING15CUTBASEDTIGHT = 12,
		SPRING15CUTBASEDVETO = 13,
		MVANONTRIGSPRING15LOOSE = 14,
		MVANONTRIGSPRING15TIGHT = 15,
		SUMMER16CUTBASEDLOOSE = 16,
		SUMMER16CUTBASEDMEDIUM = 17,
		SUMMER16CUTBASEDTIGHT = 18,
		SUMMER16CUTBASEDVETO = 19,
	};
	enum class WorkingPoint : int
	{
		LOOSE = 0,
		MEDIUM = 1,
		TIGHT = 2,
		VETO = 3,
	};
	static ElectronIDType ToElectronIDType(std::string const& electronIDType)
	{
		if (electronIDType == "summer2013loose") return ElectronIDType::SUMMER2013LOOSE;
		else if (electronIDType == "summer2013tight") return ElectronIDType::SUMMER2013TIGHT;
		else if (electronIDType == "summer2013tthloose") return ElectronIDType::SUMMER2013TTHLOOSE;
		else if (electronIDType == "summer2013tthtight") return ElectronIDType::SUMMER2013TTHTIGHT;
		else if (electronIDType == "phys14cutbasedloose") return ElectronIDType::PHYS14CUTBASEDLOOSE;
		else if (electronIDType == "phys14cutbasedmedium") return ElectronIDType::PHYS14CUTBASEDMEDIUM;
		else if (electronIDType == "phys14cutbasedtight") return ElectronIDType::PHYS14CUTBASEDTIGHT;
		else if (electronIDType == "phys14cutbasedveto") return ElectronIDType::PHYS14CUTBASEDVETO;
		else if (electronIDType == "mvanontrigphys14loose") return ElectronIDType::MVANONTRIGPHYS14LOOSE;
		else if (electronIDType == "mvanontrigphys14tight") return ElectronIDType::MVANONTRIGPHYS14TIGHT;
		else if (electronIDType == "spring15cutbasedloose") return ElectronIDType::SPRING15CUTBASEDLOOSE;
		else if (electronIDType == "spring15cutbasedmedium") return ElectronIDType::SPRING15CUTBASEDMEDIUM;
		else if (electronIDType == "spring15cutbasedtight") return ElectronIDType::SPRING15CUTBASEDTIGHT;
		else if (electronIDType == "spring15cutbasedveto") return ElectronIDType::SPRING15CUTBASEDVETO;
		else if (electronIDType == "mvanontrigspring15loose") return ElectronIDType::MVANONTRIGSPRING15LOOSE;
		else if (electronIDType == "mvanontrigspring15tight") return ElectronIDType::MVANONTRIGSPRING15TIGHT;
		else if (electronIDType == "summer16cutbasedloose") return ElectronIDType::SUMMER16CUTBASEDLOOSE;
		else if (electronIDType == "summer16cutbasedmedium") return ElectronIDType::SUMMER16CUTBASEDMEDIUM;
		else if (electronIDType == "summer16cutbasedtight") return ElectronIDType::SUMMER16CUTBASEDTIGHT;
		else if (electronIDType == "summer16cutbasedveto") return ElectronIDType::SUMMER16CUTBASEDVETO;
		else if (electronIDType == "none") return ElectronIDType::NONE;
		else
			LOG(FATAL) << "Could not find ElectronID " << electronIDType << "! If you want the HttValidElectronsProducer to use no special ID, use \"none\" as argument."<< std::endl;
		return ElectronIDType::INVALID;
	}
	
	HttValidElectronsProducer(
			std::vector<KElectron*> product_type::*validElectrons=&product_type::m_validElectrons,
			std::vector<KElectron*> product_type::*invalidElectrons=&product_type::m_invalidElectrons,
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
			float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEB)(void) const=&setting_type::GetElectronIsoPtSumOverPtLowerThresholdEB,
			float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEE)(void) const=&setting_type::GetElectronIsoPtSumOverPtLowerThresholdEE,
			float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEB)(void) const=&setting_type::GetElectronIsoPtSumOverPtUpperThresholdEB,
			float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEE)(void) const=&setting_type::GetElectronIsoPtSumOverPtUpperThresholdEE,
			float (setting_type::*GetElectronTrackDxyCut)(void) const=&setting_type::GetElectronTrackDxyCut,
			float (setting_type::*GetElectronTrackDzCut)(void) const=&setting_type::GetElectronTrackDzCut
	);

	virtual void Init(setting_type const& settings) override;


protected:

	// Htautau specific additional definitions
	virtual bool AdditionalCriteria(KElectron* electron, event_type const& event,
	                                product_type& product, setting_type const& settings) const  override;


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
	float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEB)(void) const;
	float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEE)(void) const;
	float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEB)(void) const;
	float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEE)(void) const;
	float (setting_type::*GetElectronTrackDxyCut)(void) const;
	float (setting_type::*GetElectronTrackDzCut)(void) const;

	ElectronIDType electronIDType;
	
	bool IsMVATrigElectronTTHSummer2013(KElectron* electron, event_type const& event, bool tightID) const;
	bool IsMVANonTrigElectronHttSummer2013(KElectron* electron, event_type const& event, bool tightID) const;
	bool IsCutBasedPhys14(KElectron* electron, event_type const& event, WorkingPoint wp) const;
	bool IsCutBasedSpring15(KElectron* electron, event_type const& event, WorkingPoint wp) const;
	bool IsCutBasedSummer16(KElectron* electron, event_type const& event, WorkingPoint wp) const;
	bool IsMVANonTrigPhys14(KElectron* electron, event_type const& event, bool tightID) const;
	bool IsMVANonTrigSpring15(KElectron* electron, event_type const& event, bool tightID) const;
	std::string ChooseCutBasedId(const KElectronMetadata *meta, WorkingPoint wp) const;
	std::string ChooseMvaNonTrigId(const KElectronMetadata *meta) const;
};


/**
 */
class HttValidLooseElectronsProducer: public HttValidElectronsProducer
{

public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetProducerId() const override {
		return "HttValidLooseElectronsProducer";
	}
	
	virtual void Init(setting_type const& settings) override {
	
		HttValidElectronsProducer::Init(settings);
	
		// add possible quantities for the lambda ntuples consumers
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity("nLooseElectrons", [this](event_type const& event, product_type const& product) {
			return product.m_validLooseElectrons.size();
		});
	}
	
	HttValidLooseElectronsProducer(
			std::vector<KElectron*> product_type::*validElectrons=&product_type::m_validLooseElectrons,
			std::vector<KElectron*> product_type::*invalidElectrons=&product_type::m_invalidLooseElectrons,
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
			float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEB)(void) const=&setting_type::GetLooseElectronIsoPtSumOverPtLowerThresholdEB,
			float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEE)(void) const=&setting_type::GetLooseElectronIsoPtSumOverPtLowerThresholdEE,
			float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEB)(void) const=&setting_type::GetLooseElectronIsoPtSumOverPtUpperThresholdEB,
			float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEE)(void) const=&setting_type::GetLooseElectronIsoPtSumOverPtUpperThresholdEE,
			float (setting_type::*GetElectronTrackDxyCut)(void) const=&setting_type::GetLooseElectronTrackDxyCut,
			float (setting_type::*GetElectronTrackDzCut)(void) const=&setting_type::GetLooseElectronTrackDzCut
	);

};


/**
 */
class HttValidVetoElectronsProducer: public HttValidElectronsProducer
{

public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetProducerId() const override {
		return "HttValidVetoElectronsProducer";
	}

	virtual void Init(setting_type const& settings) override {
	
		HttValidElectronsProducer::Init(settings);
	
		// add possible quantities for the lambda ntuples consumers
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity("nVetoElectrons", [this](event_type const& event, product_type const& product) {
			return product.m_validVetoElectrons.size();
		});
	}
	
	HttValidVetoElectronsProducer(
			std::vector<KElectron*> product_type::*validElectrons=&product_type::m_validVetoElectrons,
			std::vector<KElectron*> product_type::*invalidElectrons=&product_type::m_invalidVetoElectrons,
			std::string (setting_type::*GetElectronID)(void) const=&setting_type::GetVetoElectronID,
			std::string (setting_type::*GetElectronIDType)(void) const=&setting_type::GetVetoElectronIDType,
			std::string (setting_type::*GetElectronIsoType)(void) const=&setting_type::GetVetoElectronIsoType,
			std::string (setting_type::*GetElectronIso)(void) const=&setting_type::GetVetoElectronIso,
			std::string (setting_type::*GetElectronReco)(void) const=&setting_type::GetVetoElectronReco,
			std::vector<std::string>& (setting_type::*GetLowerPtCuts)(void) const=&setting_type::GetVetoElectronLowerPtCuts,
			std::vector<std::string>& (setting_type::*GetUpperAbsEtaCuts)(void) const=&setting_type::GetVetoElectronUpperAbsEtaCuts,
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
			float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEB)(void) const=&setting_type::GetVetoElectronIsoPtSumOverPtLowerThresholdEB,
			float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEE)(void) const=&setting_type::GetVetoElectronIsoPtSumOverPtLowerThresholdEE,
			float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEB)(void) const=&setting_type::GetVetoElectronIsoPtSumOverPtUpperThresholdEB,
			float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEE)(void) const=&setting_type::GetVetoElectronIsoPtSumOverPtUpperThresholdEE,
			float (setting_type::*GetElectronTrackDxyCut)(void) const=&setting_type::GetElectronTrackDxyCut,
			float (setting_type::*GetElectronTrackDzCut)(void) const=&setting_type::GetElectronTrackDzCut
	);

};

