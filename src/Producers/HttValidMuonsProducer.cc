
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidMuonsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/ParticleIsolation.h"


HttValidMuonsProducer::HttValidMuonsProducer(std::vector<KMuon*> product_type::*validMuons,
                                             std::vector<KMuon*> product_type::*invalidMuons,
                                             std::string (setting_type::*GetMuonID)(void) const,
                                             std::string (setting_type::*GetMuonIsoType)(void) const,
                                             std::string (setting_type::*GetMuonIsoTypeUserMode)(void) const,
                                             std::string (setting_type::*GetMuonIso)(void) const,
                                             std::vector<std::string>& (setting_type::*GetLowerPtCuts)(void) const,
                                             std::vector<std::string>& (setting_type::*GetUpperAbsEtaCuts)(void) const,
                                             float (setting_type::*GetMuonChargedIsoVetoConeSize)(void) const,
                                             float (setting_type::*GetMuonNeutralIsoVetoConeSize)(void) const,
                                             float (setting_type::*GetMuonPhotonIsoVetoConeSize)(void) const,
                                             float (setting_type::*GetMuonDeltaBetaIsoVetoConeSize)(void) const,
                                             float (setting_type::*GetMuonChargedIsoPtThreshold)(void) const,
                                             float (setting_type::*GetMuonNeutralIsoPtThreshold)(void) const,
                                             float (setting_type::*GetMuonPhotonIsoPtThreshold)(void) const,
                                             float (setting_type::*GetMuonDeltaBetaIsoPtThreshold)(void) const,
                                             float (setting_type::*GetMuonIsoSignalConeSize)(void) const,
                                             float (setting_type::*GetMuonDeltaBetaCorrectionFactor)(void) const,
                                             float (setting_type::*GetMuonIsoPtSumOverPtLowerThresholdEB)(void) const,
                                             float (setting_type::*GetMuonIsoPtSumOverPtLowerThresholdEE)(void) const,
                                             float (setting_type::*GetMuonIsoPtSumOverPtUpperThresholdEB)(void) const,
                                             float (setting_type::*GetMuonIsoPtSumOverPtUpperThresholdEE)(void) const,
                                             float (setting_type::*GetMuonTrackDxyCut)(void) const,
                                             float (setting_type::*GetMuonTrackDzCut)(void) const)
                                              :
	ValidMuonsProducer(validMuons, invalidMuons,
	                   GetMuonID, GetMuonIsoType, GetMuonIso,
	                   GetLowerPtCuts, GetUpperAbsEtaCuts),
    GetMuonIsoTypeUserMode(GetMuonIsoTypeUserMode),
	GetMuonChargedIsoVetoConeSize(GetMuonChargedIsoVetoConeSize),
	GetMuonNeutralIsoVetoConeSize(GetMuonNeutralIsoVetoConeSize),
	GetMuonPhotonIsoVetoConeSize(GetMuonPhotonIsoVetoConeSize),
	GetMuonDeltaBetaIsoVetoConeSize(GetMuonDeltaBetaIsoVetoConeSize),
	GetMuonChargedIsoPtThreshold(GetMuonChargedIsoPtThreshold),
	GetMuonNeutralIsoPtThreshold(GetMuonNeutralIsoPtThreshold),
	GetMuonPhotonIsoPtThreshold(GetMuonPhotonIsoPtThreshold),
	GetMuonDeltaBetaIsoPtThreshold(GetMuonDeltaBetaIsoPtThreshold),
	GetMuonIsoSignalConeSize(GetMuonIsoSignalConeSize),
	GetMuonDeltaBetaCorrectionFactor(GetMuonDeltaBetaCorrectionFactor),
	GetMuonIsoPtSumOverPtLowerThresholdEB(GetMuonIsoPtSumOverPtLowerThresholdEB),
	GetMuonIsoPtSumOverPtLowerThresholdEE(GetMuonIsoPtSumOverPtLowerThresholdEE),
	GetMuonIsoPtSumOverPtUpperThresholdEB(GetMuonIsoPtSumOverPtUpperThresholdEB),
	GetMuonIsoPtSumOverPtUpperThresholdEE(GetMuonIsoPtSumOverPtUpperThresholdEE),
	GetMuonTrackDxyCut(GetMuonTrackDxyCut),
	GetMuonTrackDzCut(GetMuonTrackDzCut)
{
}


bool HttValidMuonsProducer::AdditionalCriteria(KMuon* muon,
                                               event_type const& event, product_type& product,
                                               setting_type const& settings) const
{
	bool validMuon = ValidMuonsProducer<HttTypes>::AdditionalCriteria(muon, event, product, settings);
	double isolationPtSum = DefaultValues::UndefinedDouble;

	if (validMuon && muonIsoType == MuonIsoType::USER) {
		if (1==0)
			event.m_pfChargedHadronsNoPileUp &&
		    event.m_pfNeutralHadronsNoPileUp &&
		    event.m_pfPhotonsNoPileUp &&
		    event.m_pfChargedHadronsPileUp)
		{
			isolationPtSum = ParticleIsolation::IsolationPtSum(
					muon->p4, event,
					(settings.*GetMuonIsoSignalConeSize)(),
					(settings.*GetMuonDeltaBetaCorrectionFactor)(),
					(settings.*GetMuonChargedIsoVetoConeSize)(),
					(settings.*GetMuonChargedIsoVetoConeSize)(),
					(settings.*GetMuonNeutralIsoVetoConeSize)(),
					(settings.*GetMuonPhotonIsoVetoConeSize)(),
					(settings.*GetMuonPhotonIsoVetoConeSize)(),
					(settings.*GetMuonDeltaBetaIsoVetoConeSize)(),
					(settings.*GetMuonChargedIsoPtThreshold)(),
					(settings.*GetMuonNeutralIsoPtThreshold)(),
					(settings.*GetMuonPhotonIsoPtThreshold)(),
					(settings.*GetMuonDeltaBetaIsoPtThreshold)()
			);
		}
		else {
			//Apply different Iso modes
			if ((settings.*GetMuonIsoTypeUserMode)() == "ONLYALL")
			{
				isolationPtSum = muon->pfIsoOnlyAll();
				//std::cout << "0 " << (settings.*GetMuonIsoTypeUserMode)() << std::endl;
				//std::cout << "OnlyAllIso: " << isolationPtSum << std::endl;
			}
			else if ((settings.*GetMuonIsoTypeUserMode)() == "ONLYHADRON")
			{
				isolationPtSum = muon->pfIsoOnlyHadron();
				//std::cout << "1 " << (settings.*GetMuonIsoTypeUserMode)() << std::endl;
				//std::cout << "OnlyHadronIso: " << isolationPtSum << std::endl;
			}
			else if ((settings.*GetMuonIsoTypeUserMode)() == "ONLYNEUTRAL")
			{
				isolationPtSum = muon->pfIsoOnlyNeutral();
				//std::cout << "2 " << (settings.*GetMuonIsoTypeUserMode)() << std::endl;
				//std::cout << "OnlyNeutralIso: " << isolationPtSum << std::endl;
			}
			else if ((settings.*GetMuonIsoTypeUserMode)() == "ONLYPHOTONS")
			{
				isolationPtSum = muon->pfIsoOnlyPhoton();
				//std::cout << "3 " << (settings.*GetMuonIsoTypeUserMode)() << std::endl;
				//std::cout << "OnlyPhotonIso: " << isolationPtSum << std::endl;
			}
			else if ((settings.*GetMuonIsoTypeUserMode)() == "ONLYPU")
			{
				isolationPtSum = muon->pfIsoOnlyPu();
				//std::cout << "0 " << (settings.*GetMuonIsoTypeUserMode)() << std::endl;
				//std::cout << "OnlyAllIso: " << isolationPtSum << std::endl;
			}
			else if ((settings.*GetMuonIsoTypeUserMode)() == "NONEUTRAL")
			{
				isolationPtSum = muon->pfIsoNoNeutral((settings.*GetMuonDeltaBetaCorrectionFactor)());
				//std::cout << "4 " << (settings.*GetMuonIsoTypeUserMode)() << std::endl;
				//std::cout << "NoNeutralIso: " << isolationPtSum << std::endl;
			}
			else if ((settings.*GetMuonIsoTypeUserMode)() == "NOPHOTONS")
			{
				isolationPtSum = muon->pfIsoNoPhoton((settings.*GetMuonDeltaBetaCorrectionFactor)());
				//std::cout << "5 " << (settings.*GetMuonIsoTypeUserMode)() << std::endl;
				//std::cout << "NoPhotonIso: " << isolationPtSum << std::endl;
			}
			else if ((settings.*GetMuonIsoTypeUserMode)() == "NOPU")
			{
				isolationPtSum = muon->pfIsoNoPU();
				//std::cout << "6 " << (settings.*GetMuonIsoTypeUserMode)() << std::endl;
				//std::cout << "NoPUIso: " << isolationPtSum << std::endl;
			}
			else
			{
				isolationPtSum = muon->pfIso((settings.*GetMuonDeltaBetaCorrectionFactor)());
				//std::cout << "-1 " << (settings.*GetMuonIsoTypeUserMode)() << std::endl;
				//std::cout << "NormalIso: " << isolationPtSum << std::endl;
			}
			
		}
		
		double isolationPtSumOverPt = isolationPtSum / muon->p4.Pt();
		
		product.m_leptonIsolation[muon] = isolationPtSum;
		product.m_leptonIsolationOverPt[muon] = isolationPtSumOverPt;
		product.m_muonIsolation[muon] = isolationPtSum;
		product.m_muonIsolationOverPt[muon] = isolationPtSumOverPt;
		
		if (std::abs(muon->p4.Eta()) < DefaultValues::EtaBorderEB)
		{
			if ((isolationPtSumOverPt > (settings.*GetMuonIsoPtSumOverPtLowerThresholdEB)()) &&
			    (isolationPtSumOverPt < (settings.*GetMuonIsoPtSumOverPtUpperThresholdEB)()))
			{
				validMuon = settings.GetDirectIso();
			}
			else
			{
				validMuon = (! settings.GetDirectIso());
			}
		}
		else
		{
			if ((isolationPtSumOverPt > (settings.*GetMuonIsoPtSumOverPtLowerThresholdEE)()) &&
			    (isolationPtSumOverPt < (settings.*GetMuonIsoPtSumOverPtUpperThresholdEE)()))
			{
				validMuon = settings.GetDirectIso();
			}
			else
			{
				validMuon = (! settings.GetDirectIso());
			}
		}
	}
	
	// (tighter) cut on impact parameters of track
	validMuon = validMuon
	            && ((settings.*GetMuonTrackDxyCut)() <= 0.0 || std::abs(muon->dxy) < (settings.*GetMuonTrackDxyCut)())
	            && ((settings.*GetMuonTrackDzCut)() <= 0.0 || std::abs(muon->dz) < (settings.*GetMuonTrackDzCut)());

	return validMuon;
}


HttValidLooseMuonsProducer::HttValidLooseMuonsProducer(
		std::vector<KMuon*> product_type::*validMuons,
		std::vector<KMuon*> product_type::*invalidMuons,
		std::string (setting_type::*GetMuonID)(void) const,
		std::string (setting_type::*GetMuonIsoType)(void) const,
		std::string (setting_type::*GetMuonIsoTypeUserMode)(void) const,
		std::string (setting_type::*GetMuonIso)(void) const,
		std::vector<std::string>& (setting_type::*GetLowerPtCuts)(void) const,
		std::vector<std::string>& (setting_type::*GetUpperAbsEtaCuts)(void) const,
		float (setting_type::*GetMuonChargedIsoVetoConeSize)(void) const,
		float (setting_type::*GetMuonNeutralIsoVetoConeSize)(void) const,
		float (setting_type::*GetMuonPhotonIsoVetoConeSize)(void) const,
		float (setting_type::*GetMuonDeltaBetaIsoVetoConeSize)(void) const,
		float (setting_type::*GetMuonChargedIsoPtThreshold)(void) const,
		float (setting_type::*GetMuonNeutralIsoPtThreshold)(void) const,
		float (setting_type::*GetMuonPhotonIsoPtThreshold)(void) const,
		float (setting_type::*GetMuonDeltaBetaIsoPtThreshold)(void) const,
		float (setting_type::*GetMuonIsoSignalConeSize)(void) const,
		float (setting_type::*GetMuonDeltaBetaCorrectionFactor)(void) const,
		float (setting_type::*GetMuonIsoPtSumOverPtLowerThresholdEB)(void) const,
		float (setting_type::*GetMuonIsoPtSumOverPtLowerThresholdEE)(void) const,
		float (setting_type::*GetMuonIsoPtSumOverPtUpperThresholdEB)(void) const,
		float (setting_type::*GetMuonIsoPtSumOverPtUpperThresholdEE)(void) const,
		float (setting_type::*GetMuonTrackDxyCut)(void) const,
		float (setting_type::*GetMuonTrackDzCut)(void) const
) :
	HttValidMuonsProducer(validMuons,
	                      invalidMuons,
	                      GetMuonID,
	                      GetMuonIsoType,
	                      GetMuonIsoTypeUserMode,
	                      GetMuonIso,
	                      GetLowerPtCuts,
	                      GetUpperAbsEtaCuts,
	                      GetMuonChargedIsoVetoConeSize,
	                      GetMuonNeutralIsoVetoConeSize,
	                      GetMuonPhotonIsoVetoConeSize,
	                      GetMuonDeltaBetaIsoVetoConeSize,
	                      GetMuonChargedIsoPtThreshold,
	                      GetMuonNeutralIsoPtThreshold,
	                      GetMuonPhotonIsoPtThreshold,
	                      GetMuonDeltaBetaIsoPtThreshold,
	                      GetMuonIsoSignalConeSize,
	                      GetMuonDeltaBetaCorrectionFactor,
	                      GetMuonIsoPtSumOverPtLowerThresholdEB,
	                      GetMuonIsoPtSumOverPtLowerThresholdEE,
	                      GetMuonIsoPtSumOverPtUpperThresholdEB,
	                      GetMuonIsoPtSumOverPtUpperThresholdEE,
	                      GetMuonTrackDxyCut,
	                      GetMuonTrackDzCut)
{
}


HttValidVetoMuonsProducer::HttValidVetoMuonsProducer(
		std::vector<KMuon*> product_type::*validMuons,
		std::vector<KMuon*> product_type::*invalidMuons,
		std::string (setting_type::*GetMuonID)(void) const,
		std::string (setting_type::*GetMuonIsoType)(void) const,
		std::string (setting_type::*GetMuonIsoTypeUserMode)(void) const,
		std::string (setting_type::*GetMuonIso)(void) const,
		std::vector<std::string>& (setting_type::*GetLowerPtCuts)(void) const,
		std::vector<std::string>& (setting_type::*GetUpperAbsEtaCuts)(void) const,
		float (setting_type::*GetMuonChargedIsoVetoConeSize)(void) const,
		float (setting_type::*GetMuonNeutralIsoVetoConeSize)(void) const,
		float (setting_type::*GetMuonPhotonIsoVetoConeSize)(void) const,
		float (setting_type::*GetMuonDeltaBetaIsoVetoConeSize)(void) const,
		float (setting_type::*GetMuonChargedIsoPtThreshold)(void) const,
		float (setting_type::*GetMuonNeutralIsoPtThreshold)(void) const,
		float (setting_type::*GetMuonPhotonIsoPtThreshold)(void) const,
		float (setting_type::*GetMuonDeltaBetaIsoPtThreshold)(void) const,
		float (setting_type::*GetMuonIsoSignalConeSize)(void) const,
		float (setting_type::*GetMuonDeltaBetaCorrectionFactor)(void) const,
		float (setting_type::*GetMuonIsoPtSumOverPtLowerThresholdEB)(void) const,
		float (setting_type::*GetMuonIsoPtSumOverPtLowerThresholdEE)(void) const,
		float (setting_type::*GetMuonIsoPtSumOverPtUpperThresholdEB)(void) const,
		float (setting_type::*GetMuonIsoPtSumOverPtUpperThresholdEE)(void) const,
		float (setting_type::*GetMuonTrackDxyCut)(void) const,
		float (setting_type::*GetMuonTrackDzCut)(void) const
) :
	HttValidMuonsProducer(validMuons,
	                      invalidMuons,
	                      GetMuonID,
	                      GetMuonIsoType,
	                      GetMuonIsoTypeUserMode,
	                      GetMuonIso,
	                      GetLowerPtCuts,
	                      GetUpperAbsEtaCuts,
	                      GetMuonChargedIsoVetoConeSize,
	                      GetMuonNeutralIsoVetoConeSize,
	                      GetMuonPhotonIsoVetoConeSize,
	                      GetMuonDeltaBetaIsoVetoConeSize,
	                      GetMuonChargedIsoPtThreshold,
	                      GetMuonNeutralIsoPtThreshold,
	                      GetMuonPhotonIsoPtThreshold,
	                      GetMuonDeltaBetaIsoPtThreshold,
	                      GetMuonIsoSignalConeSize,
	                      GetMuonDeltaBetaCorrectionFactor,
	                      GetMuonIsoPtSumOverPtLowerThresholdEB,
	                      GetMuonIsoPtSumOverPtLowerThresholdEE,
	                      GetMuonIsoPtSumOverPtUpperThresholdEB,
	                      GetMuonIsoPtSumOverPtUpperThresholdEE,
	                      GetMuonTrackDxyCut,
	                      GetMuonTrackDzCut)
{
}

