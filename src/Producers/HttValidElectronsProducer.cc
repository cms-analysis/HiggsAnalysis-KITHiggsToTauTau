
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidElectronsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/ParticleIsolation.h"


HttValidElectronsProducer::HttValidElectronsProducer(std::vector<KElectron*> product_type::*validElectrons,
                                                     std::vector<KElectron*> product_type::*invalidElectrons,
                                                     std::string (setting_type::*GetElectronID)(void) const,
                                                     std::string (setting_type::*GetElectronIDType)(void) const,
                                                     std::string (setting_type::*GetElectronIsoType)(void) const,
                                                     std::string (setting_type::*GetElectronIso)(void) const,
                                                     std::string (setting_type::*GetElectronReco)(void) const,
                                                     std::vector<std::string>& (setting_type::*GetLowerPtCuts)(void) const,
                                                     std::vector<std::string>& (setting_type::*GetUpperAbsEtaCuts)(void) const,
                                                     float (setting_type::*GetElectronChargedIsoVetoConeSizeEB)(void) const,
                                                     float (setting_type::*GetElectronChargedIsoVetoConeSizeEE)(void) const,
                                                     float (setting_type::*GetElectronNeutralIsoVetoConeSize)(void) const,
                                                     float (setting_type::*GetElectronPhotonIsoVetoConeSizeEB)(void) const,
                                                     float (setting_type::*GetElectronPhotonIsoVetoConeSizeEE)(void) const,
                                                     float (setting_type::*GetElectronDeltaBetaIsoVetoConeSize)(void) const,
                                                     float (setting_type::*GetElectronChargedIsoPtThreshold)(void) const,
                                                     float (setting_type::*GetElectronNeutralIsoPtThreshold)(void) const,
                                                     float (setting_type::*GetElectronPhotonIsoPtThreshold)(void) const,
                                                     float (setting_type::*GetElectronDeltaBetaIsoPtThreshold)(void) const,
                                                     float (setting_type::*GetElectronIsoSignalConeSize)(void) const,
                                                     float (setting_type::*GetElectronDeltaBetaCorrectionFactor)(void) const,
                                                     float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEB)(void) const,
                                                     float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEE)(void) const,
                                                     float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEB)(void) const,
                                                     float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEE)(void) const,
                                                     float (setting_type::*GetElectronTrackDxyCut)(void) const,
                                                     float (setting_type::*GetElectronTrackDzCut)(void) const) :
	ValidElectronsProducer(validElectrons, invalidElectrons,
	                       GetElectronID, GetElectronIsoType, GetElectronIso, GetElectronReco,
	                       GetLowerPtCuts, GetUpperAbsEtaCuts),
	GetElectronIDType(GetElectronIDType),
	GetElectronChargedIsoVetoConeSizeEB(GetElectronChargedIsoVetoConeSizeEB),
	GetElectronChargedIsoVetoConeSizeEE(GetElectronChargedIsoVetoConeSizeEE),
	GetElectronNeutralIsoVetoConeSize(GetElectronNeutralIsoVetoConeSize),
	GetElectronPhotonIsoVetoConeSizeEB(GetElectronPhotonIsoVetoConeSizeEB),
	GetElectronPhotonIsoVetoConeSizeEE(GetElectronPhotonIsoVetoConeSizeEE),
	GetElectronDeltaBetaIsoVetoConeSize(GetElectronDeltaBetaIsoVetoConeSize),
	GetElectronChargedIsoPtThreshold(GetElectronChargedIsoPtThreshold),
	GetElectronNeutralIsoPtThreshold(GetElectronNeutralIsoPtThreshold),
	GetElectronPhotonIsoPtThreshold(GetElectronPhotonIsoPtThreshold),
	GetElectronDeltaBetaIsoPtThreshold(GetElectronDeltaBetaIsoPtThreshold),
	GetElectronIsoSignalConeSize(GetElectronIsoSignalConeSize),
	GetElectronDeltaBetaCorrectionFactor(GetElectronDeltaBetaCorrectionFactor),
	GetElectronIsoPtSumOverPtLowerThresholdEB(GetElectronIsoPtSumOverPtLowerThresholdEB),
	GetElectronIsoPtSumOverPtLowerThresholdEE(GetElectronIsoPtSumOverPtLowerThresholdEE),
	GetElectronIsoPtSumOverPtUpperThresholdEB(GetElectronIsoPtSumOverPtUpperThresholdEB),
	GetElectronIsoPtSumOverPtUpperThresholdEE(GetElectronIsoPtSumOverPtUpperThresholdEE),
	GetElectronTrackDxyCut(GetElectronTrackDxyCut),
	GetElectronTrackDzCut(GetElectronTrackDzCut)
{
}

void HttValidElectronsProducer::Init(setting_type const& settings)
{
	ValidElectronsProducer<HttTypes>::Init(settings);
	
	electronIDType = ToElectronIDType(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy((settings.*GetElectronIDType)())));

	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("leadingEleIso", [this](event_type const& event, product_type const& product) {
		return product.m_validElectrons.size() >=1 ? SafeMap::GetWithDefault(product.m_electronIsolation, product.m_validElectrons[0], DefaultValues::UndefinedDouble) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("leadingEleIsoOverPt", [this](event_type const& event, product_type const& product) {
		return product.m_validElectrons.size() >=1 ? SafeMap::GetWithDefault(product.m_electronIsolationOverPt, product.m_validElectrons[0], DefaultValues::UndefinedDouble) : DefaultValues::UndefinedDouble;
	});
}

bool HttValidElectronsProducer::AdditionalCriteria(KElectron* electron,
                                                   event_type const& event, product_type& product,
                                                   setting_type const& settings) const
{
	assert(event.m_vertexSummary);
	
	bool validElectron = ValidElectronsProducer<HttTypes>::AdditionalCriteria(electron, event, product, settings);
	
	double isolationPtSum = DefaultValues::UndefinedDouble;
	
	// require no missing inner hits
	if (validElectron && electronReco == ElectronReco::USER) {
		validElectron = validElectron && (electron->track.nInnerHits == 0);
	}

	// custom WPs for electron ID
	// https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingSummer2013#Electron_ID
	if (validElectron && electronID == ElectronID::USER) {
		if (electronIDType == ElectronIDType::SUMMER2013LOOSE)
		{
			validElectron = validElectron && IsMVANonTrigElectronHttSummer2013(&(*electron), event, false);
		}
		else if (electronIDType == ElectronIDType::SUMMER2013TIGHT)
		{
			validElectron = validElectron && IsMVANonTrigElectronHttSummer2013(&(*electron), event, true);
		}
		else if (electronIDType == ElectronIDType::SUMMER2013TTHLOOSE)
		{
			validElectron = validElectron && IsMVATrigElectronTTHSummer2013(&(*electron), event, false);
		}
		else if (electronIDType == ElectronIDType::SUMMER2013TTHTIGHT)
		{
			validElectron = validElectron && IsMVATrigElectronTTHSummer2013(&(*electron), event, true);
		}
		else if (electronIDType == ElectronIDType::MVATRIGV050NSCSA14)
		{
			validElectron = validElectron && IsMVATrigV050nsCsa14(&(*electron), event, true);
		}
		else if (electronIDType == ElectronIDType::MVATRIGV025NSCSA14)
		{
			validElectron = validElectron && IsMVATrigV025nsCsa14(&(*electron), event, true);
		}
		else if (electronIDType == ElectronIDType::MVANONTRIGV050NSCSA14)
		{
			validElectron = validElectron && IsMVANonTrigV050nsCsa14(&(*electron), event, true);
		}
		else if (electronIDType == ElectronIDType::MVANONTRIGV025NSCSA14)
		{
			validElectron = validElectron && IsMVANonTrigV025nsCsa14(&(*electron), event, true);
		}
		else if (electronIDType == ElectronIDType::PHYS14CUTBASEDLOOSE)
		{
			validElectron = validElectron && IsCutBasedPhys14(&(*electron), event, WorkingPoint::LOOSE);
		}
		else if (electronIDType == ElectronIDType::PHYS14CUTBASEDMEDIUM)
		{
			validElectron = validElectron && IsCutBasedPhys14(&(*electron), event, WorkingPoint::MEDIUM);
		}
		else if (electronIDType == ElectronIDType::PHYS14CUTBASEDTIGHT)
		{
			validElectron = validElectron && IsCutBasedPhys14(&(*electron), event, WorkingPoint::TIGHT);
		}
		else if (electronIDType == ElectronIDType::PHYS14CUTBASEDVETO)
		{
			validElectron = validElectron && IsCutBasedPhys14(&(*electron), event, WorkingPoint::VETO);
		}
		else if (electronIDType == ElectronIDType::MVANONTRIGV025NSPHYS14)
		{
			validElectron = validElectron && IsMVANonTrigV025nsPhys14(&(*electron), event, true);
		}
		else if (electronIDType != ElectronIDType::NONE)
			LOG(FATAL) << "Electron ID type of type " << Utility::ToUnderlyingValue(electronIDType) << " not yet implemented!";
	}

	// custom electron isolation with delta beta correction
	// https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingSummer2013#Electron_Muon_Isolation
	if (validElectron && electronIsoType == ElectronIsoType::USER) {
		if (event.m_pfChargedHadronsNoPileUp &&
		    event.m_pfNeutralHadronsNoPileUp &&
		    event.m_pfPhotonsNoPileUp &&
		    event.m_pfChargedHadronsPileUp)
		{
			isolationPtSum = ParticleIsolation::IsolationPtSum(
					electron->p4, event,
					(settings.*GetElectronIsoSignalConeSize)(),
					(settings.*GetElectronDeltaBetaCorrectionFactor)(),
					(settings.*GetElectronChargedIsoVetoConeSizeEB)(),
					(settings.*GetElectronChargedIsoVetoConeSizeEE)(),
					(settings.*GetElectronNeutralIsoVetoConeSize)(),
					(settings.*GetElectronPhotonIsoVetoConeSizeEB)(),
					(settings.*GetElectronPhotonIsoVetoConeSizeEE)(),
					(settings.*GetElectronDeltaBetaIsoVetoConeSize)(),
					(settings.*GetElectronChargedIsoPtThreshold)(),
					(settings.*GetElectronNeutralIsoPtThreshold)(),
					(settings.*GetElectronPhotonIsoPtThreshold)(),
					(settings.*GetElectronDeltaBetaIsoPtThreshold)()
			);
		}
		else {
			isolationPtSum = electron->pfIso((settings.*GetElectronDeltaBetaCorrectionFactor)());
		}
		
		double isolationPtSumOverPt = isolationPtSum / electron->p4.Pt();
		
		product.m_leptonIsolation[electron] = isolationPtSum;
		product.m_leptonIsolationOverPt[electron] = isolationPtSumOverPt;
		product.m_electronIsolation[electron] = isolationPtSum;
		product.m_electronIsolationOverPt[electron] = isolationPtSumOverPt;
		
		if (std::abs(electron->p4.Eta()) < DefaultValues::EtaBorderEB)
		{
			if ((isolationPtSumOverPt > (settings.*GetElectronIsoPtSumOverPtLowerThresholdEB)()) &&
			    (isolationPtSumOverPt < (settings.*GetElectronIsoPtSumOverPtUpperThresholdEB)()))
			{
				validElectron = settings.GetDirectIso();
			}
			else
			{
				validElectron = (! settings.GetDirectIso());
			}
		}
		else
		{
			if ((isolationPtSumOverPt > (settings.*GetElectronIsoPtSumOverPtLowerThresholdEE)()) &&
			    (isolationPtSumOverPt < (settings.*GetElectronIsoPtSumOverPtUpperThresholdEE)()))
			{
				validElectron = settings.GetDirectIso();
			}
			else
			{
				validElectron = (! settings.GetDirectIso());
			}
		}
	}
	
	// (tighter) cut on impact parameters of track
	validElectron = validElectron
	                && ((settings.*GetElectronTrackDxyCut)() <= 0.0 || std::abs(electron->track.getDxy(&event.m_vertexSummary->pv)) < (settings.*GetElectronTrackDxyCut)())
	                && ((settings.*GetElectronTrackDzCut)() <= 0.0 || std::abs(electron->track.getDz(&event.m_vertexSummary->pv)) < (settings.*GetElectronTrackDzCut)());

	return validElectron;
}

bool HttValidElectronsProducer::IsMVATrigElectronTTHSummer2013(KElectron* electron, event_type const& event, bool tightID) const
{
	bool validElectron = true;
	
	validElectron = validElectron && electron->getId("mvaTrigV0", event.m_electronMetadata) > (tightID ? 0.5 : 0.5);

	return validElectron;
}

bool HttValidElectronsProducer::IsMVANonTrigElectronHttSummer2013(KElectron* electron, event_type const& event, bool tightID) const
{
	bool validElectron = true;
	
	// https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingSummer2013#Electron_ID
	validElectron = validElectron &&
		(
			(
				(electron->p4.Pt() < 20.0)
				&&
				(
					(std::abs(electron->superclusterPosition.Eta()) < 0.8 && electron->getId("mvaNonTrigV0", event.m_electronMetadata) > 0.925)
					|| (std::abs(electron->superclusterPosition.Eta()) > 0.8 && std::abs(electron->superclusterPosition.Eta()) < DefaultValues::EtaBorderEB && electron->getId("mvaNonTrigV0", event.m_electronMetadata) > 0.915)
					|| (std::abs(electron->superclusterPosition.Eta()) > DefaultValues::EtaBorderEB && electron->getId("mvaNonTrigV0", event.m_electronMetadata) > 0.965)
				)
			)
			||
			(
				(electron->p4.Pt() >= 20.0) &&
				(
					(std::abs(electron->superclusterPosition.Eta()) < 0.8 && electron->getId("mvaNonTrigV0", event.m_electronMetadata) > (tightID ? 0.925 : 0.905))
					|| (std::abs(electron->superclusterPosition.Eta()) > 0.8 && std::abs(electron->superclusterPosition.Eta()) < DefaultValues::EtaBorderEB && electron->getId("mvaNonTrigV0", event.m_electronMetadata) > (tightID ? 0.975 : 0.955))
					|| (std::abs(electron->superclusterPosition.Eta()) > DefaultValues::EtaBorderEB && electron->getId("mvaNonTrigV0", event.m_electronMetadata) > (tightID ? 0.985 : 0.975))
				)
			)
		);

	return validElectron;
}

bool HttValidElectronsProducer::IsMVATrigV050nsCsa14(KElectron* electron, event_type const& event, bool tightID) const
{
	bool validElectron = true;
	
	validElectron = validElectron &&
		(
			(
				(electron->p4.Pt() < 20.0)
				&&
				(
					(electron->getId("mvaTrigV050nsCSA14", event.m_electronMetadata) > 0.9)
				)
			)
			||
			(
				(electron->p4.Pt() >= 20.0) &&
				(
					(electron->getId("mvaTrigV050nsCSA14", event.m_electronMetadata) > 0.9)
				)
			)
		);

	return validElectron;
}

bool HttValidElectronsProducer::IsMVATrigV025nsCsa14(KElectron* electron, event_type const& event, bool tightID) const
{
	bool validElectron = true;

	validElectron = validElectron &&
		(
			(
				(electron->p4.Pt() < 20.0)
				&&
				(
					(electron->getId("mvaTrigV025nsCSA14", event.m_electronMetadata) > 0.9)
				)
			)
			||
			(
				(electron->p4.Pt() >= 20.0) &&
				(
					(electron->getId("mvaTrigV025nsCSA14", event.m_electronMetadata) > 0.9)
				)
			)
		);

	return validElectron;
}

bool HttValidElectronsProducer::IsMVANonTrigV050nsCsa14(KElectron* electron, event_type const& event, bool tightID) const
{
	bool validElectron = true;

	validElectron = validElectron &&
		(
			(
				(electron->p4.Pt() < 20.0)
				&&
				(
					(electron->getId("mvaNonTrigV050nsCSA14", event.m_electronMetadata) > 0.9)
				)
			)
			||
			(
				(electron->p4.Pt() >= 20.0) &&
				(
					(electron->getId("mvaNonTrigV050nsCSA14", event.m_electronMetadata) > 0.9)
				)
			)
		);

	return validElectron;
}

bool HttValidElectronsProducer::IsMVANonTrigV025nsCsa14(KElectron* electron, event_type const& event, bool tightID) const
{
	bool validElectron = true;

	validElectron = validElectron &&
		(
			(
				(electron->p4.Pt() < 20.0)
				&&
				(
					(electron->getId("mvaNonTrigV025nsCSA14", event.m_electronMetadata) > 0.9)
				)
			)
			||
			(
				(electron->p4.Pt() >= 20.0) &&
				(
					(electron->getId("mvaNonTrigV025nsCSA14", event.m_electronMetadata) > 0.9)
				)
			)
		);

	return validElectron;
}

bool HttValidElectronsProducer::IsCutBasedPhys14(KElectron* electron, event_type const& event, WorkingPoint wp) const
{
	bool validElectron = true;

	auto choseID = [=] (const KElectronMetadata *meta, const std::string &option1, const std::string &option2 ) { return ( Utility::Contains(meta->idNames, option1) ? option1 : option2); };
	if (wp == WorkingPoint::LOOSE)
		validElectron = validElectron && electron->getId( choseID(event.m_electronMetadata, "cutBasedEleIdPHYS14Loose", "egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-loose"), event.m_electronMetadata);
	
	if (wp == WorkingPoint::MEDIUM)
		validElectron = validElectron && electron->getId( choseID(event.m_electronMetadata, "cutBasedEleIdPHYS14Medium", "egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-medium"), event.m_electronMetadata);
	
	if (wp == WorkingPoint::TIGHT)
		validElectron = validElectron && electron->getId( choseID(event.m_electronMetadata, "cutBasedEleIdPHYS14Tight", "egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-tight"), event.m_electronMetadata);

	if (wp == WorkingPoint::VETO)
		validElectron = validElectron && electron->getId( choseID(event.m_electronMetadata, "cutBasedEleIdPHYS14Veto", "egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-veto"), event.m_electronMetadata);

	return validElectron;
}

bool HttValidElectronsProducer::IsMVANonTrigV025nsPhys14(KElectron* electron, event_type const& event, bool tightID) const
{
	bool validElectron = true;

	validElectron = validElectron &&
		(
			(
				(electron->p4.Pt() < 20.0)
				&&
				(
					(electron->getId("mvaNonTrigV025nsPHYS14", event.m_electronMetadata) > 0.9)
				)
			)
			||
			(
				(electron->p4.Pt() >= 20.0) &&
				(
					(electron->getId("mvaNonTrigV025nsPHYS14", event.m_electronMetadata) > 0.9)
				)
			)
		);

	return validElectron;
}

HttValidLooseElectronsProducer::HttValidLooseElectronsProducer(
		std::vector<KElectron*> product_type::*validElectrons,
		std::vector<KElectron*> product_type::*invalidElectrons,
		std::string (setting_type::*GetElectronID)(void) const,
		std::string (setting_type::*GetElectronIDType)(void) const,
		std::string (setting_type::*GetElectronIsoType)(void) const,
		std::string (setting_type::*GetElectronIso)(void) const,
		std::string (setting_type::*GetElectronReco)(void) const,
		std::vector<std::string>& (setting_type::*GetLowerPtCuts)(void) const,
		std::vector<std::string>& (setting_type::*GetUpperAbsEtaCuts)(void) const,
		float (setting_type::*GetElectronChargedIsoVetoConeSizeEB)(void) const,
		float (setting_type::*GetElectronChargedIsoVetoConeSizeEE)(void) const,
		float (setting_type::*GetElectronNeutralIsoVetoConeSize)(void) const,
		float (setting_type::*GetElectronPhotonIsoVetoConeSizeEB)(void) const,
		float (setting_type::*GetElectronPhotonIsoVetoConeSizeEE)(void) const,
		float (setting_type::*GetElectronDeltaBetaIsoVetoConeSize)(void) const,
		float (setting_type::*GetElectronChargedIsoPtThreshold)(void) const,
		float (setting_type::*GetElectronNeutralIsoPtThreshold)(void) const,
		float (setting_type::*GetElectronPhotonIsoPtThreshold)(void) const,
		float (setting_type::*GetElectronDeltaBetaIsoPtThreshold)(void) const,
		float (setting_type::*GetElectronIsoSignalConeSize)(void) const,
		float (setting_type::*GetElectronDeltaBetaCorrectionFactor)(void) const,
		float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEB)(void) const,
		float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEE)(void) const,
		float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEB)(void) const,
		float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEE)(void) const,
		float (setting_type::*GetElectronTrackDxyCut)(void) const,
		float (setting_type::*GetElectronTrackDzCut)(void) const
) :
	HttValidElectronsProducer(validElectrons,
	                          invalidElectrons,
	                          GetElectronID,
	                          GetElectronIDType,
	                          GetElectronIsoType,
	                          GetElectronIso,
	                          GetElectronReco,
	                          GetLowerPtCuts,
	                          GetUpperAbsEtaCuts,
	                          GetElectronChargedIsoVetoConeSizeEB,
	                          GetElectronChargedIsoVetoConeSizeEE,
	                          GetElectronNeutralIsoVetoConeSize,
	                          GetElectronPhotonIsoVetoConeSizeEB,
	                          GetElectronPhotonIsoVetoConeSizeEE,
	                          GetElectronDeltaBetaIsoVetoConeSize,
	                          GetElectronChargedIsoPtThreshold,
	                          GetElectronNeutralIsoPtThreshold,
	                          GetElectronPhotonIsoPtThreshold,
	                          GetElectronDeltaBetaIsoPtThreshold,
	                          GetElectronIsoSignalConeSize,
	                          GetElectronDeltaBetaCorrectionFactor,
	                          GetElectronIsoPtSumOverPtLowerThresholdEB,
	                          GetElectronIsoPtSumOverPtLowerThresholdEE,
	                          GetElectronIsoPtSumOverPtUpperThresholdEB,
	                          GetElectronIsoPtSumOverPtUpperThresholdEE,
	                          GetElectronTrackDxyCut,
	                          GetElectronTrackDzCut)
{
}



HttValidVetoElectronsProducer::HttValidVetoElectronsProducer(
		std::vector<KElectron*> product_type::*validElectrons,
		std::vector<KElectron*> product_type::*invalidElectrons,
		std::string (setting_type::*GetElectronID)(void) const,
		std::string (setting_type::*GetElectronIDType)(void) const,
		std::string (setting_type::*GetElectronIsoType)(void) const,
		std::string (setting_type::*GetElectronIso)(void) const,
		std::string (setting_type::*GetElectronReco)(void) const,
		std::vector<std::string>& (setting_type::*GetLowerPtCuts)(void) const,
		std::vector<std::string>& (setting_type::*GetUpperAbsEtaCuts)(void) const,
		float (setting_type::*GetElectronChargedIsoVetoConeSizeEB)(void) const,
		float (setting_type::*GetElectronChargedIsoVetoConeSizeEE)(void) const,
		float (setting_type::*GetElectronNeutralIsoVetoConeSize)(void) const,
		float (setting_type::*GetElectronPhotonIsoVetoConeSizeEB)(void) const,
		float (setting_type::*GetElectronPhotonIsoVetoConeSizeEE)(void) const,
		float (setting_type::*GetElectronDeltaBetaIsoVetoConeSize)(void) const,
		float (setting_type::*GetElectronChargedIsoPtThreshold)(void) const,
		float (setting_type::*GetElectronNeutralIsoPtThreshold)(void) const,
		float (setting_type::*GetElectronPhotonIsoPtThreshold)(void) const,
		float (setting_type::*GetElectronDeltaBetaIsoPtThreshold)(void) const,
		float (setting_type::*GetElectronIsoSignalConeSize)(void) const,
		float (setting_type::*GetElectronDeltaBetaCorrectionFactor)(void) const,
		float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEB)(void) const,
		float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEE)(void) const,
		float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEB)(void) const,
		float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEE)(void) const,
		float (setting_type::*GetElectronTrackDxyCut)(void) const,
		float (setting_type::*GetElectronTrackDzCut)(void) const
) :
	HttValidElectronsProducer(validElectrons,
	                          invalidElectrons,
	                          GetElectronID,
	                          GetElectronIDType,
	                          GetElectronIsoType,
	                          GetElectronIso,
	                          GetElectronReco,
	                          GetLowerPtCuts,
	                          GetUpperAbsEtaCuts,
	                          GetElectronChargedIsoVetoConeSizeEB,
	                          GetElectronChargedIsoVetoConeSizeEE,
	                          GetElectronNeutralIsoVetoConeSize,
	                          GetElectronPhotonIsoVetoConeSizeEB,
	                          GetElectronPhotonIsoVetoConeSizeEE,
	                          GetElectronDeltaBetaIsoVetoConeSize,
	                          GetElectronChargedIsoPtThreshold,
	                          GetElectronNeutralIsoPtThreshold,
	                          GetElectronPhotonIsoPtThreshold,
	                          GetElectronDeltaBetaIsoPtThreshold,
	                          GetElectronIsoSignalConeSize,
	                          GetElectronDeltaBetaCorrectionFactor,
	                          GetElectronIsoPtSumOverPtLowerThresholdEB,
	                          GetElectronIsoPtSumOverPtLowerThresholdEE,
	                          GetElectronIsoPtSumOverPtUpperThresholdEB,
	                          GetElectronIsoPtSumOverPtUpperThresholdEE,
	                          GetElectronTrackDxyCut,
	                          GetElectronTrackDzCut)
{
}

