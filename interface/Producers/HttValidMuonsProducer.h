
#pragma once

#include "Artus/KappaAnalysis/interface/Producers/ValidMuonsProducer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/**
   \brief GlobalProducer, for valid muons.
   
   Required config tags in addtion to the ones of the base class:
   - MuonChargedIsoVetoConeSize (default given)
   - MuonNeutralIsoVetoConeSize (default given)
   - MuonPhotonIsoVetoConeSize (default given)
   - MuonDeltaBetaIsoVetoConeSize (default given)
   - MuonChargedIsoPtThreshold (default given)
   - MuonNeutralIsoPtThreshold (default given)
   - MuonPhotonIsoPtThreshold (default given)
   - MuonDeltaBetaIsoPtThreshold (default given)
   - MuonIsoTypeUserMode (default: "fromcmssw")
   - MuonIsoSignalConeSize
   - MuonDeltaBetaCorrectionFactor
   - MuonIsoPtSumOverPtLowerThresholdEB
   - MuonIsoPtSumOverPtLowerThresholdEE
   - MuonIsoPtSumOverPtUpperThresholdEB
   - MuonIsoPtSumOverPtUpperThresholdEE
*/

class HttValidMuonsProducer: public ValidMuonsProducer<HttTypes>
{

public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	enum class MuonIsoTypeUserMode : int
	{
		NONE  = -1,
		FROMCMSSW = 0, // isolation cone 0.3
		CALCULATED = 1,
		FROMCMSSWR04 = 2 // isolation cone 0.4
	};

	static MuonIsoTypeUserMode ToMuonIsoTypeUserMode(std::string const& muonIsoTypeUserMode)
	{
		if (muonIsoTypeUserMode == "fromcmssw") return MuonIsoTypeUserMode::FROMCMSSW;
		else if (muonIsoTypeUserMode == "fromcmsswr04") return MuonIsoTypeUserMode::FROMCMSSWR04;
		else if (muonIsoTypeUserMode == "calculated") return MuonIsoTypeUserMode::CALCULATED;
		else return MuonIsoTypeUserMode::NONE;
	}
	
	HttValidMuonsProducer(
			std::vector<KMuon*> product_type::*validMuons=&product_type::m_validMuons,
			std::vector<KMuon*> product_type::*invalidMuons=&product_type::m_invalidMuons,
			std::string (setting_type::*GetMuonID)(void) const=&setting_type::GetMuonID,
			std::string (setting_type::*GetMuonIsoType)(void) const=&setting_type::GetMuonIsoType,
			std::string (setting_type::*GetMuonIsoTypeUserMode)(void) const=&setting_type::GetMuonIsoTypeUserMode,
			std::string (setting_type::*GetMuonIso)(void) const=&setting_type::GetMuonIso,
			std::vector<std::string>& (setting_type::*GetLowerPtCuts)(void) const=&setting_type::GetMuonLowerPtCuts,
			std::vector<std::string>& (setting_type::*GetUpperAbsEtaCuts)(void) const=&setting_type::GetMuonUpperAbsEtaCuts,
			float (setting_type::*GetMuonChargedIsoVetoConeSize)(void) const=&setting_type::GetMuonChargedIsoVetoConeSize,
			float (setting_type::*GetMuonNeutralIsoVetoConeSize)(void) const=&setting_type::GetMuonNeutralIsoVetoConeSize,
			float (setting_type::*GetMuonPhotonIsoVetoConeSize)(void) const=&setting_type::GetMuonPhotonIsoVetoConeSize,
			float (setting_type::*GetMuonDeltaBetaIsoVetoConeSize)(void) const=&setting_type::GetMuonDeltaBetaIsoVetoConeSize,
			float (setting_type::*GetMuonChargedIsoPtThreshold)(void) const=&setting_type::GetMuonChargedIsoPtThreshold,
			float (setting_type::*GetMuonNeutralIsoPtThreshold)(void) const=&setting_type::GetMuonNeutralIsoPtThreshold,
			float (setting_type::*GetMuonPhotonIsoPtThreshold)(void) const=&setting_type::GetMuonPhotonIsoPtThreshold,
			float (setting_type::*GetMuonDeltaBetaIsoPtThreshold)(void) const=&setting_type::GetMuonDeltaBetaIsoPtThreshold,
			float (setting_type::*GetMuonIsoSignalConeSize)(void) const=&setting_type::GetMuonIsoSignalConeSize,
			float (setting_type::*GetMuonDeltaBetaCorrectionFactor)(void) const=&setting_type::GetMuonDeltaBetaCorrectionFactor,
			float (setting_type::*GetMuonIsoPtSumOverPtLowerThresholdEB)(void) const=&setting_type::GetMuonIsoPtSumOverPtLowerThresholdEB,
			float (setting_type::*GetMuonIsoPtSumOverPtLowerThresholdEE)(void) const=&setting_type::GetMuonIsoPtSumOverPtLowerThresholdEE,
			float (setting_type::*GetMuonIsoPtSumOverPtUpperThresholdEB)(void) const=&setting_type::GetMuonIsoPtSumOverPtUpperThresholdEB,
			float (setting_type::*GetMuonIsoPtSumOverPtUpperThresholdEE)(void) const=&setting_type::GetMuonIsoPtSumOverPtUpperThresholdEE,
			float (setting_type::*GetMuonTrackDxyCut)(void) const=&setting_type::GetMuonTrackDxyCut,
			float (setting_type::*GetMuonTrackDzCut)(void) const=&setting_type::GetMuonTrackDzCut
	);
	
	virtual void Init(setting_type const& settings) {

		ValidMuonsProducer<HttTypes>::Init(settings);
		
		muonIsoTypeUserMode = ToMuonIsoTypeUserMode(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy((settings.*GetMuonIsoTypeUserMode)())));

		// add possible quantities for the lambda ntuples consumers
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("leadingMuonIso", [this](event_type const& event, product_type const& product) {
			return product.m_validMuons.size() >= 1 ? SafeMap::GetWithDefault(product.m_muonIsolation, product.m_validMuons[0], DefaultValues::UndefinedDouble) : DefaultValues::UndefinedDouble;
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("leadingMuonIsoOverPt", [this](event_type const& event, product_type const& product) {
			return product.m_validMuons.size() >= 1 ? SafeMap::GetWithDefault(product.m_muonIsolationOverPt, product.m_validMuons[0], DefaultValues::UndefinedDouble) : DefaultValues::UndefinedDouble;
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("id_m_loose_1", [this](event_type const& event, product_type const& product)
		{
			return product.m_validMuons.size() >= 1 ? product.m_validMuons[0]->idLoose() : DefaultValues::UndefinedFloat;
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("id_m_medium_1", [this](event_type const& event, product_type const& product)
		{
			return product.m_validMuons.size() >= 1 ? product.m_validMuons[0]->idMedium() : DefaultValues::UndefinedFloat;
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("id_m_tight_1", [this](event_type const& event, product_type const& product)
		{
			return product.m_validMuons.size() >= 1 ? product.m_validMuons[0]->idTight() : DefaultValues::UndefinedFloat;
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("id_m_highpt_1", [this](event_type const& event, product_type const& product)
		{
			return product.m_validMuons.size() >= 1 ? product.m_validMuons[0]->idHighPt() : DefaultValues::UndefinedFloat;
		});
	}


protected:

	// Htautau specific additional definitions
	MuonIsoTypeUserMode muonIsoTypeUserMode;

	virtual bool AdditionalCriteria(KMuon* muon, event_type const& event,
	                                product_type& product, setting_type const& settings) const  override;


private:
	std::string (setting_type::*GetMuonIsoTypeUserMode)(void) const=&setting_type::GetMuonIsoTypeUserMode;
	float (setting_type::*GetMuonChargedIsoVetoConeSize)(void) const;
	float (setting_type::*GetMuonNeutralIsoVetoConeSize)(void) const;
	float (setting_type::*GetMuonPhotonIsoVetoConeSize)(void) const;
	float (setting_type::*GetMuonDeltaBetaIsoVetoConeSize)(void) const;
	float (setting_type::*GetMuonChargedIsoPtThreshold)(void) const;
	float (setting_type::*GetMuonNeutralIsoPtThreshold)(void) const;
	float (setting_type::*GetMuonPhotonIsoPtThreshold)(void) const;
	float (setting_type::*GetMuonDeltaBetaIsoPtThreshold)(void) const;
	float (setting_type::*GetMuonIsoSignalConeSize)(void) const;
	float (setting_type::*GetMuonDeltaBetaCorrectionFactor)(void) const;
	float (setting_type::*GetMuonIsoPtSumOverPtLowerThresholdEB)(void) const;
	float (setting_type::*GetMuonIsoPtSumOverPtLowerThresholdEE)(void) const;
	float (setting_type::*GetMuonIsoPtSumOverPtUpperThresholdEB)(void) const;
	float (setting_type::*GetMuonIsoPtSumOverPtUpperThresholdEE)(void) const;
	float (setting_type::*GetMuonTrackDxyCut)(void) const;
	float (setting_type::*GetMuonTrackDzCut)(void) const;	
};


/**
   \brief 
*/

class HttValidLooseMuonsProducer: public HttValidMuonsProducer
{

public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetProducerId() const override {
		return "HttValidLooseMuonsProducer";
	}
	
	virtual void Init(setting_type const& settings) override {
	
		HttValidMuonsProducer::Init(settings);
	
		// add possible quantities for the lambda ntuples consumers
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity("nLooseMuons", [this](event_type const& event, product_type const& product) {
			return product.m_validLooseMuons.size();
		});
	}
	
	HttValidLooseMuonsProducer(
			std::vector<KMuon*> product_type::*validMuons=&product_type::m_validLooseMuons,
			std::vector<KMuon*> product_type::*invalidMuons=&product_type::m_invalidLooseMuons,
			std::string (setting_type::*GetMuonID)(void) const=&setting_type::GetLooseMuonID,
			std::string (setting_type::*GetMuonIsoType)(void) const=&setting_type::GetLooseMuonIsoType,
			std::string (setting_type::*GetMuonIsoTypeUserMode)(void) const=&setting_type::GetMuonIsoTypeUserMode,
			std::string (setting_type::*GetMuonIso)(void) const=&setting_type::GetLooseMuonIso,
			std::vector<std::string>& (setting_type::*GetLowerPtCuts)(void) const=&setting_type::GetLooseMuonLowerPtCuts,
			std::vector<std::string>& (setting_type::*GetUpperAbsEtaCuts)(void) const=&setting_type::GetLooseMuonUpperAbsEtaCuts,
			float (setting_type::*GetMuonChargedIsoVetoConeSize)(void) const=&setting_type::GetMuonChargedIsoVetoConeSize,
			float (setting_type::*GetMuonNeutralIsoVetoConeSize)(void) const=&setting_type::GetMuonNeutralIsoVetoConeSize,
			float (setting_type::*GetMuonPhotonIsoVetoConeSize)(void) const=&setting_type::GetMuonPhotonIsoVetoConeSize,
			float (setting_type::*GetMuonDeltaBetaIsoVetoConeSize)(void) const=&setting_type::GetMuonDeltaBetaIsoVetoConeSize,
			float (setting_type::*GetMuonChargedIsoPtThreshold)(void) const=&setting_type::GetMuonChargedIsoPtThreshold,
			float (setting_type::*GetMuonNeutralIsoPtThreshold)(void) const=&setting_type::GetMuonNeutralIsoPtThreshold,
			float (setting_type::*GetMuonPhotonIsoPtThreshold)(void) const=&setting_type::GetMuonPhotonIsoPtThreshold,
			float (setting_type::*GetMuonDeltaBetaIsoPtThreshold)(void) const=&setting_type::GetMuonDeltaBetaIsoPtThreshold,
			float (setting_type::*GetMuonIsoSignalConeSize)(void) const=&setting_type::GetMuonIsoSignalConeSize,
			float (setting_type::*GetMuonDeltaBetaCorrectionFactor)(void) const=&setting_type::GetMuonDeltaBetaCorrectionFactor,
			float (setting_type::*GetMuonIsoPtSumOverPtLowerThresholdEB)(void) const=&setting_type::GetLooseMuonIsoPtSumOverPtLowerThresholdEB,
			float (setting_type::*GetMuonIsoPtSumOverPtLowerThresholdEE)(void) const=&setting_type::GetLooseMuonIsoPtSumOverPtLowerThresholdEE,
			float (setting_type::*GetMuonIsoPtSumOverPtUpperThresholdEB)(void) const=&setting_type::GetLooseMuonIsoPtSumOverPtUpperThresholdEB,
			float (setting_type::*GetMuonIsoPtSumOverPtUpperThresholdEE)(void) const=&setting_type::GetLooseMuonIsoPtSumOverPtUpperThresholdEE,
			float (setting_type::*GetMuonTrackDxyCut)(void) const=&setting_type::GetLooseMuonTrackDxyCut,
			float (setting_type::*GetMuonTrackDzCut)(void) const=&setting_type::GetLooseMuonTrackDzCut
	);

};


/**
   \brief 
*/

class HttValidVetoMuonsProducer: public HttValidMuonsProducer
{

public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetProducerId() const override {
		return "HttValidVetoMuonsProducer";
	}

	virtual void Init(setting_type const& settings) override {
	
		HttValidMuonsProducer::Init(settings);
		// add possible quantities for the lambda ntuples consumers
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity("nVetoMuons", [this](event_type const& event, product_type const& product) {
			return product.m_validVetoMuons.size();
		});
	}
	
	HttValidVetoMuonsProducer(
			std::vector<KMuon*> product_type::*validMuons=&product_type::m_validVetoMuons,
			std::vector<KMuon*> product_type::*invalidMuons=&product_type::m_invalidVetoMuons,
			std::string (setting_type::*GetMuonID)(void) const=&setting_type::GetVetoMuonID,
			std::string (setting_type::*GetMuonIsoType)(void) const=&setting_type::GetVetoMuonIsoType,
			std::string (setting_type::*GetMuonIsoTypeUserMode)(void) const=&setting_type::GetMuonIsoTypeUserMode,
			std::string (setting_type::*GetMuonIso)(void) const=&setting_type::GetVetoMuonIso,
			std::vector<std::string>& (setting_type::*GetLowerPtCuts)(void) const=&setting_type::GetVetoMuonLowerPtCuts,
			std::vector<std::string>& (setting_type::*GetUpperAbsEtaCuts)(void) const=&setting_type::GetVetoMuonUpperAbsEtaCuts,
			float (setting_type::*GetMuonChargedIsoVetoConeSize)(void) const=&setting_type::GetMuonChargedIsoVetoConeSize,
			float (setting_type::*GetMuonNeutralIsoVetoConeSize)(void) const=&setting_type::GetMuonNeutralIsoVetoConeSize,
			float (setting_type::*GetMuonPhotonIsoVetoConeSize)(void) const=&setting_type::GetMuonPhotonIsoVetoConeSize,
			float (setting_type::*GetMuonDeltaBetaIsoVetoConeSize)(void) const=&setting_type::GetMuonDeltaBetaIsoVetoConeSize,
			float (setting_type::*GetMuonChargedIsoPtThreshold)(void) const=&setting_type::GetMuonChargedIsoPtThreshold,
			float (setting_type::*GetMuonNeutralIsoPtThreshold)(void) const=&setting_type::GetMuonNeutralIsoPtThreshold,
			float (setting_type::*GetMuonPhotonIsoPtThreshold)(void) const=&setting_type::GetMuonPhotonIsoPtThreshold,
			float (setting_type::*GetMuonDeltaBetaIsoPtThreshold)(void) const=&setting_type::GetMuonDeltaBetaIsoPtThreshold,
			float (setting_type::*GetMuonIsoSignalConeSize)(void) const=&setting_type::GetMuonIsoSignalConeSize,
			float (setting_type::*GetMuonDeltaBetaCorrectionFactor)(void) const=&setting_type::GetMuonDeltaBetaCorrectionFactor,
			float (setting_type::*GetMuonIsoPtSumOverPtLowerThresholdEB)(void) const=&setting_type::GetVetoMuonIsoPtSumOverPtLowerThresholdEB,
			float (setting_type::*GetMuonIsoPtSumOverPtLowerThresholdEE)(void) const=&setting_type::GetVetoMuonIsoPtSumOverPtLowerThresholdEE,
			float (setting_type::*GetMuonIsoPtSumOverPtUpperThresholdEB)(void) const=&setting_type::GetVetoMuonIsoPtSumOverPtUpperThresholdEB,
			float (setting_type::*GetMuonIsoPtSumOverPtUpperThresholdEE)(void) const=&setting_type::GetVetoMuonIsoPtSumOverPtUpperThresholdEE,
			float (setting_type::*GetMuonTrackDxyCut)(void) const=&setting_type::GetMuonTrackDxyCut,
			float (setting_type::*GetMuonTrackDzCut)(void) const=&setting_type::GetMuonTrackDzCut
	);

};

