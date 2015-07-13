
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
		return product.m_validElectrons.size() >= 1 ? SafeMap::GetWithDefault(product.m_electronIsolation, product.m_validElectrons[0], DefaultValues::UndefinedDouble) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("leadingEleIsoOverPt", [this](event_type const& event, product_type const& product) {
		return product.m_validElectrons.size() >= 1 ? SafeMap::GetWithDefault(product.m_electronIsolationOverPt, product.m_validElectrons[0], DefaultValues::UndefinedDouble) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("id_e_mva_nt_loose_1", [this](event_type const& event, product_type const& product)
	{
		return (product.m_validElectrons.size() >= 1 && electronIDType != ElectronIDType::NONE) ? product.m_validElectrons[0]->getId(chooseMvaNonTrigId(event.m_electronMetadata), event.m_electronMetadata) : DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("id_e_cut_veto_1", [this](event_type const& event, product_type const& product)
	{
		return (product.m_validElectrons.size() >= 1 && electronIDType != ElectronIDType::NONE) ? product.m_validElectrons[0]->getId(chooseCutBasedId(event.m_electronMetadata, WorkingPoint::VETO), event.m_electronMetadata) : DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("id_e_cut_loose_1", [this](event_type const& event, product_type const& product)
	{
		return (product.m_validElectrons.size() >= 1 && electronIDType != ElectronIDType::NONE) ? product.m_validElectrons[0]->getId(chooseCutBasedId(event.m_electronMetadata, WorkingPoint::LOOSE), event.m_electronMetadata) : DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("id_e_cut_medium_1", [this](event_type const& event, product_type const& product)
	{
		return (product.m_validElectrons.size() >= 1 && electronIDType != ElectronIDType::NONE) ? product.m_validElectrons[0]->getId(chooseCutBasedId(event.m_electronMetadata, WorkingPoint::MEDIUM), event.m_electronMetadata) : DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("id_e_cut_tight_1", [this](event_type const& event, product_type const& product)
	{
		return (product.m_validElectrons.size() >= 1 && electronIDType != ElectronIDType::NONE) ? product.m_validElectrons[0]->getId(chooseCutBasedId(event.m_electronMetadata, WorkingPoint::TIGHT), event.m_electronMetadata) : DefaultValues::UndefinedFloat;
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
		else if (electronIDType == ElectronIDType::MVANONTRIGPHYS14LOOSE)
		{
			validElectron = validElectron && IsMVANonTrigPhys14(&(*electron), event, false);
		}
		else if (electronIDType == ElectronIDType::MVANONTRIGPHYS14TIGHT)
		{
			validElectron = validElectron && IsMVANonTrigPhys14(&(*electron), event, true);
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

bool HttValidElectronsProducer::IsCutBasedPhys14(KElectron* electron, event_type const& event, WorkingPoint wp) const
{
	bool validElectron = electron->getId(chooseCutBasedId(event.m_electronMetadata, wp), event.m_electronMetadata);

	return validElectron;
}

bool HttValidElectronsProducer::IsMVANonTrigPhys14(KElectron* electron, event_type const& event, bool tightID) const
{
	bool validElectron = true;

	// https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentificationRun2#Non_triggering_electron_MVA
	// pT always greater than 10 GeV
	validElectron = validElectron &&
		( 
			(std::abs(electron->p4.Eta()) < 0.8 && electron->getId(chooseMvaNonTrigId(event.m_electronMetadata), event.m_electronMetadata) > (tightID ? 0.965 : 0.933))
			||
			(std::abs(electron->p4.Eta()) > 0.8 && std::abs(electron->p4.Eta()) < DefaultValues::EtaBorderEB && electron->getId(chooseMvaNonTrigId(event.m_electronMetadata), event.m_electronMetadata) > (tightID? 0.917 : 0.825))
			||
			(std::abs(electron->p4.Eta()) > DefaultValues::EtaBorderEB && electron->getId(chooseMvaNonTrigId(event.m_electronMetadata), event.m_electronMetadata) > (tightID ? 0.683 : 0.337))
		);

	return validElectron;
}

std::string HttValidElectronsProducer::chooseCutBasedId(const KElectronMetadata *meta, WorkingPoint wp) const
{
	std::string stringID;

	if (wp == WorkingPoint::LOOSE) {
		if (Utility::Contains(meta->idNames, std::string("cutBasedEleIdPHYS14Loose")))
			stringID = "cutBasedEleIdPHYS14Loose";
		else if (Utility::Contains(meta->idNames, std::string("egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-loose")))
			stringID = "egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-loose";
		else if (Utility::Contains(meta->idNames, std::string("egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-loose")))
			stringID = "egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-loose";
		else
			LOG(FATAL) << "HttValidElectronsProducer::chooseCutBasedId: could not find any Id for the loose WP" << std::endl;
	}

	if (wp == WorkingPoint::MEDIUM) {
		if (Utility::Contains(meta->idNames, std::string("cutBasedEleIdPHYS14Medium")))
			stringID = "cutBasedEleIdPHYS14Medium";
		else if (Utility::Contains(meta->idNames, std::string("egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-medium")))
			stringID = "egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-medium";
		else if (Utility::Contains(meta->idNames, std::string("egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-medium")))
			stringID = "egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-medium";
		else
			LOG(FATAL) << "HttValidElectronsProducer::chooseCutBasedId: could not find any Id for the medium WP" << std::endl;
	}

	if (wp == WorkingPoint::TIGHT) {
		if (Utility::Contains(meta->idNames, std::string("cutBasedEleIdPHYS14Tight")))
			stringID = "cutBasedEleIdPHYS14Tight";
		else if (Utility::Contains(meta->idNames, std::string("egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-tight")))
			stringID = "egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-tight";
		else if (Utility::Contains(meta->idNames, std::string("egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-tight")))
			stringID = "egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-tight";
		else
			LOG(FATAL) << "HttValidElectronsProducer::chooseCutBasedId: could not find any Id for the tight WP" << std::endl;
	}

	if (wp == WorkingPoint::VETO) {
		if (Utility::Contains(meta->idNames, std::string("cutBasedEleIdPHYS14Veto")))
			stringID = "cutBasedEleIdPHYS14Veto";
		else if (Utility::Contains(meta->idNames, std::string("egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-veto")))
			stringID = "egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-veto";
		else if (Utility::Contains(meta->idNames, std::string("egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-veto")))
			stringID = "egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-veto";
		else
			LOG(FATAL) << "HttValidElectronsProducer::chooseCutBasedId: could not find any Id for the veto WP" << std::endl;
	}

	return stringID;
}

std::string HttValidElectronsProducer::chooseMvaNonTrigId(const KElectronMetadata *meta) const
{
	std::string stringID;

	if (Utility::Contains(meta->idNames, std::string("mvaNonTrigV025nsPHYS14")))
		stringID = "mvaNonTrigV025nsPHYS14";
	else if (Utility::Contains(meta->idNames, std::string("mvaNonTrig25nsPHYS14")))
		stringID = "mvaNonTrig25nsPHYS14";
	else if (Utility::Contains(meta->idNames, std::string("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Phys14NonTrigValues")))
		stringID = "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Phys14NonTrigValues";
	else
		LOG(FATAL) << "HttValidElectronsProducer::chooseMvaNotTrigId: could not find any Id" << std::endl;

	return stringID;
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

