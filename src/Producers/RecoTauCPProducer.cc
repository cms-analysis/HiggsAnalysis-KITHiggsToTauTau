
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"
#include "Artus/Utility/interface/UnitConverter.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/CPQuantities.h"
#include "HiggsCPinTauDecays/ImpactParameter/interface/ImpactParameter.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/RecoTauCPProducer.h"

#include "TauPolSoftware/TauDecaysInterface/interface/SCalculator.h"

#include <fstream>

std::string RecoTauCPProducer::GetProducerId() const
{
	return "RecoTauCPProducer";
}

void RecoTauCPProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	m_useAltPiZero = true;//FIXME: add a new setting?
	m_useMVADecayModes = settings.GetGEFUseMVADecayModes();

	// CP-related quantities
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCP", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCP;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPHel", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPHel;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPrPV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPHelrPV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPHelrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPHelrPVBS;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPRho", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPRho;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPRhoMerged", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPRhoMerged;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "reco_posyTauL", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_reco_posyTauL;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "reco_negyTauL", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_reco_negyTauL;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPComb", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPComb;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombMerged", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPCombMerged;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombHel", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPCombHel;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombMergedHel", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPCombMergedHel;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombrPV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPCombrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombMergedrPV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPCombMergedrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombHelrPV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPCombHelrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombMergedHelrPV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPCombMergedHelrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPCombrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombMergedrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPCombMergedrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPCombHelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombMergedHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPCombMergedHelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStar", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStar;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarRho", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarRho;
	});

	// azimuthal angles of the tau decay planes
	// IP+IP method
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiPlusIPMeth", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiPlusIPMeth;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiMinusIPMeth", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiMinusIPMeth;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarPlusIPMeth", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarPlusIPMeth;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarMinusIPMeth", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarMinusIPMeth;
	});
	// comb (IP+DP) method
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiPlusCombMeth", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiPlusCombMeth;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiMinusCombMeth", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiMinusCombMeth;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarPlusCombMeth", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarPlusCombMeth;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarMinusCombMeth", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarMinusCombMeth;
	});
	// rho (DP+DP) method
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiPlusRhoMeth", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiPlusRhoMeth;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiMinusRhoMeth", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiMinusRhoMeth;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarPlusRhoMeth", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarPlusRhoMeth;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarMinusRhoMeth", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarMinusRhoMeth;
	});

	// Polarimetric Vector method
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecTau1Tau2HelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecTau1Tau2HelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecTau1VisTau2HelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecTau1VisTau2HelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecTau1Tau2VisHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecTau1Tau2VisHelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecTau1Tau2PiSSFromRhoHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecTau1Tau2PiSSFromRhoHelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecTau1Tau2PiHighPtHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecTau1Tau2PiHighPtHelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecTau1VisTau2VisHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecTau1VisTau2VisHelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecTau1VisTau2PiSSFromRhoHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecTau1VisTau2PiSSFromRhoHelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecTau1VisTau2PiHighPtHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecTau1VisTau2PiHighPtHelrPVBS;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecCombTau1Tau2HelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecCombTau1Tau2HelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecCombTau1VisTau2HelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecCombTau1VisTau2HelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecCombTau1Tau2VisHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecCombTau1Tau2VisHelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecCombTau1Tau2PiSSFromRhoHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecCombTau1Tau2PiSSFromRhoHelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecCombTau1Tau2PiHighPtHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecCombTau1Tau2PiHighPtHelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecCombTau1VisTau2VisHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecCombTau1VisTau2VisHelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecCombTau1VisTau2PiSSFromRhoHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecCombTau1VisTau2PiSSFromRhoHelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecCombTau1VisTau2PiHighPtHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecCombTau1VisTau2PiHighPtHelrPVBS;
	});


	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecTauOneProngTauA1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecTauOneProngTauA1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecOneProngTauA1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecOneProngTauA1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecTauOneProngA1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecTauOneProngA1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecOneProngA1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecOneProngA1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecTauOneProngA1PiSSFromRho", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecTauOneProngA1PiSSFromRho;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecTauOneProngA1PiHighPt", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecTauOneProngA1PiHighPt;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecOneProngA1PiSSFromRho", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecOneProngA1PiSSFromRho;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecOneProngA1PiHighPt", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecOneProngA1PiHighPt;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecCombTauOneProngTauA1HelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecCombTauOneProngTauA1HelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecCombOneProngTauA1HelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecCombOneProngTauA1HelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecCombTauOneProngA1HelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecCombTauOneProngA1HelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecCombOneProngA1HelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecCombOneProngA1HelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecCombTauOneProngA1PiSSFromRhoHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecCombTauOneProngA1PiSSFromRhoHelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecCombTauOneProngA1PiHighPtHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecCombTauOneProngA1PiHighPtHelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecCombOneProngA1PiSSFromRhoHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecCombOneProngA1PiSSFromRhoHelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPPolVecCombOneProngA1PiHighPtHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPPolVecCombOneProngA1PiHighPtHelrPVBS;
	});

	//aliases for CP angles used in the analysis
	// IP+IP method
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "acotautau_00", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPHelrPVBS;
	});
	// IP+DP (combined) method
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "acotautau_01", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPCombMergedHelrPVBS;
	});
	// DP+DP method
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "acotautau_11", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhiStarCPRhoMerged;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoChargedHadron1HiggsFrameEnergy", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoChargedHadronEnergies.first;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoChargedHadron2HiggsFrameEnergy", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoChargedHadronEnergies.second;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoP_SI", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoP_SI;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoV_z_SI", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoV_z_SI;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoOmega", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoOmega;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhi1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoPhi1;
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "recoOprime", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoOprime;
	});

	// cosPsi
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "cosPsiPlus", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_cosPsiPlus;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "cosPsiMinus", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_cosPsiMinus;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "cosPsiPlusrPV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_cosPsiPlusrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "cosPsiMinusrPV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_cosPsiMinusrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "cosPsiPlusrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_cosPsiPlusrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "cosPsiMinusrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_cosPsiMinusrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "cosPsiPlusHel", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_cosPsiPlusHel;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "cosPsiMinusHel", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_cosPsiMinusHel;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "cosPsiPlusHelrPV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_cosPsiPlusHelrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "cosPsiMinusHelrPV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_cosPsiMinusHelrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "cosPsiPlusHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_cosPsiPlusHelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "cosPsiMinusHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_cosPsiMinusHelrPVBS;
	});

	for (size_t leptonIndex = 0; leptonIndex < 2; ++leptonIndex)
	{
		LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "polarimetricVectorsTauOneProngTauA1SimpleFit_" + std::to_string(leptonIndex+1), [leptonIndex](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			return static_cast<RMPoint>(SafeMap::GetWithDefault(product.m_polarimetricVectorsTauOneProngTauA1SimpleFit, product.m_flavourOrderedLeptons.at(leptonIndex), static_cast<RMFLV::BetaVector>(DefaultValues::UndefinedRMPoint)));
		});
		LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "polarimetricVectorsOneProngTauA1SimpleFit_" + std::to_string(leptonIndex+1), [leptonIndex](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			return static_cast<RMPoint>(SafeMap::GetWithDefault(product.m_polarimetricVectorsOneProngTauA1SimpleFit, product.m_flavourOrderedLeptons.at(leptonIndex), static_cast<RMFLV::BetaVector>(DefaultValues::UndefinedRMPoint)));
		});
		LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "polarimetricVectorsTauOneProngA1SimpleFit_" + std::to_string(leptonIndex+1), [leptonIndex](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			return static_cast<RMPoint>(SafeMap::GetWithDefault(product.m_polarimetricVectorsTauOneProngA1SimpleFit, product.m_flavourOrderedLeptons.at(leptonIndex), static_cast<RMFLV::BetaVector>(DefaultValues::UndefinedRMPoint)));
		});
		LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "polarimetricVectorsOneProngA1SimpleFit_" + std::to_string(leptonIndex+1), [leptonIndex](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			return static_cast<RMPoint>(SafeMap::GetWithDefault(product.m_polarimetricVectorsOneProngA1SimpleFit, product.m_flavourOrderedLeptons.at(leptonIndex), static_cast<RMFLV::BetaVector>(DefaultValues::UndefinedRMPoint)));
		});
		LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "polarimetricVectorsTauOneProngA1PiSSFromRhoSimpleFit_" + std::to_string(leptonIndex+1), [leptonIndex](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			return static_cast<RMPoint>(SafeMap::GetWithDefault(product.m_polarimetricVectorsTauOneProngA1PiSSFromRhoSimpleFit, product.m_flavourOrderedLeptons.at(leptonIndex), static_cast<RMFLV::BetaVector>(DefaultValues::UndefinedRMPoint)));
		});
		LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "polarimetricVectorsTauOneProngA1PiHighPtSimpleFit_" + std::to_string(leptonIndex+1), [leptonIndex](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			return static_cast<RMPoint>(SafeMap::GetWithDefault(product.m_polarimetricVectorsTauOneProngA1PiHighPtSimpleFit, product.m_flavourOrderedLeptons.at(leptonIndex), static_cast<RMFLV::BetaVector>(DefaultValues::UndefinedRMPoint)));
		});
		LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "polarimetricVectorsOneProngA1PiSSFromRhoSimpleFit_" + std::to_string(leptonIndex+1), [leptonIndex](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			return static_cast<RMPoint>(SafeMap::GetWithDefault(product.m_polarimetricVectorsOneProngA1PiSSFromRhoSimpleFit, product.m_flavourOrderedLeptons.at(leptonIndex), static_cast<RMFLV::BetaVector>(DefaultValues::UndefinedRMPoint)));
		});
		LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "polarimetricVectorsOneProngA1PiHighPtSimpleFit_" + std::to_string(leptonIndex+1), [leptonIndex](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			return static_cast<RMPoint>(SafeMap::GetWithDefault(product.m_polarimetricVectorsOneProngA1PiHighPtSimpleFit, product.m_flavourOrderedLeptons.at(leptonIndex), static_cast<RMFLV::BetaVector>(DefaultValues::UndefinedRMPoint)));
		});
	}
}

void RecoTauCPProducer::Produce(event_type const& event, product_type& product, setting_type const& settings, metadata_type const& metadata) const
{
	assert(event.m_vertexSummary);
	assert(product.m_flavourOrderedLeptons.size() >= 2);

	//FIXME These Vectors are only needed for the helical approach
	TVector3 IPPlus;
	TVector3 IPMinus;
	TVector3 IPPlusHel;
	TVector3 IPMinusHel;
	TVector3 IPPlusrPV;
	TVector3 IPMinusrPV;
	TVector3 IPPlusHelrPV;
	TVector3 IPMinusHelrPV;
	TVector3 IPPlusrPVBS;
	TVector3 IPMinusrPVBS;
	TVector3 IPPlusHelrPVBS;
	TVector3 IPMinusHelrPVBS;

	IPPlus.SetXYZ(-999,-999,-999);
	IPMinus.SetXYZ(-999,-999,-999);
	IPPlusHel.SetXYZ(-999,-999,-999);
	IPMinusHel.SetXYZ(-999,-999,-999);
	IPPlusrPV.SetXYZ(-999,-999,-999);
	IPMinusrPV.SetXYZ(-999,-999,-999);
	IPPlusHelrPV.SetXYZ(-999,-999,-999);
	IPMinusHelrPV.SetXYZ(-999,-999,-999);
	IPPlusrPVBS.SetXYZ(-999,-999,-999);
	IPMinusrPVBS.SetXYZ(-999,-999,-999);
	IPPlusHelrPVBS.SetXYZ(-999,-999,-999);
	IPMinusHelrPVBS.SetXYZ(-999,-999,-999);

	// reconstructed leptons
	KLepton* recoParticle1 = product.m_flavourOrderedLeptons.at(0);
	KLepton* recoParticle2 = product.m_flavourOrderedLeptons.at(1);
	KLepton* chargedPart1  = product.m_chargeOrderedLeptons.at(0);
	KLepton* chargedPart2  = product.m_chargeOrderedLeptons.at(1);

	// PV: in case of missing refitted PV use non-refitted one (default)
	// FIXME: propagate also to lambda?
	KVertex *rPV = product.m_refitPV != nullptr ? product.m_refitPV : &event.m_vertexSummary->pv;
	KVertex *rPVBS = product.m_refitPVBS != nullptr ? product.m_refitPVBS : &event.m_vertexSummary->pv;

	// Defining CPQuantities object to use variables and functions of this class
	CPQuantities cpq;
	ImpactParameter ip;

	// quantitites needed for calculation of recoPhiStarCP
	KTrack trackP = chargedPart1->track; // in case of tau_h, the track of the lead. prong is saved in the KTau track member
	KTrack trackM = chargedPart2->track;
	RMFLV momentumP = ((chargedPart1->flavour() == KLeptonFlavour::TAU) ? static_cast<KTau*>(chargedPart1)->chargedHadronCandidates.at(0).p4 : chargedPart1->p4);
	RMFLV momentumM = ((chargedPart2->flavour() == KLeptonFlavour::TAU) ? static_cast<KTau*>(chargedPart2)->chargedHadronCandidates.at(0).p4 : chargedPart2->p4);

	// ----------
	// rho-method (DP+DP)
	// ----------
	double posyLRho = 1;
	double negyLRho = 1;
	RMFLV piZeroP(0,0,0,0);
	RMFLV piZeroM(0,0,0,0);
	RMFLV piSSFromRhoP(0,0,0,0);
	RMFLV piSSHighPtP(0,0,0,0);
	RMFLV piOSP(0,0,0,0);
	RMFLV piSSFromRhoM(0,0,0,0);
	RMFLV piSSHighPtM(0,0,0,0);
	RMFLV piOSM(0,0,0,0);
	int decayModeP = -1, decayModeMvaP = -1;
	int decayModeM = -1, decayModeMvaM = -1;
	if (chargedPart1->flavour() == KLeptonFlavour::TAU) {
	  decayModeP = static_cast<KTau*>(chargedPart1)->decayMode;
	  decayModeMvaP = (int)static_cast<KTau*>(chargedPart1)->getDiscriminator("MVADM2017v1", event.m_tauMetadata);
	  piZeroP = m_useAltPiZero ? alternativePiZeroMomentum(static_cast<KTau*>(chargedPart1)) :
	    static_cast<KTau*>(chargedPart1)->piZeroMomentum();
	  if (decayModeP > 0 && (decayModeMvaP == 1 || decayModeMvaP == 2)) {
	    posyLRho = cpq.CalculateSpinAnalysingDiscriminantRho(momentumP, piZeroP);
	  }
	  else if (decayModeMvaP == 10 || decayModeMvaP == 11) {
	    pionsFromRho3Prongs(static_cast<KTau*>(chargedPart1),
				piSSFromRhoP, piOSP, piSSHighPtP);
	    posyLRho = cpq.CalculateSpinAnalysingDiscriminantRho(piSSFromRhoP, piOSP);
	  }
	}
	if (chargedPart2->flavour() == KLeptonFlavour::TAU) {
	  decayModeM = static_cast<KTau*>(chargedPart2)->decayMode;
	  decayModeMvaM = (int)static_cast<KTau*>(chargedPart2)->getDiscriminator("MVADM2017v1", event.m_tauMetadata);
	  piZeroM = m_useAltPiZero ? alternativePiZeroMomentum(static_cast<KTau*>(chargedPart2)) :
	    static_cast<KTau*>(chargedPart2)->piZeroMomentum();
	  if (decayModeM > 0 && (decayModeMvaM == 1 || decayModeMvaM == 2)) {
	    negyLRho = cpq.CalculateSpinAnalysingDiscriminantRho(momentumM, piZeroM);
	  }
	  else if (decayModeMvaM == 10 || decayModeMvaM == 11) {
	    pionsFromRho3Prongs(static_cast<KTau*>(chargedPart2),
				piSSFromRhoM, piOSM, piSSHighPtM);
	    negyLRho = cpq.CalculateSpinAnalysingDiscriminantRho(piSSFromRhoM, piOSM);
	  }
	}
	product.m_reco_posyTauL = posyLRho;
	product.m_reco_negyTauL = negyLRho;

	if ( product.m_decayChannel == HttEnumTypes::DecayChannel::TT ) {

	  if ( decayModeP > 0 && decayModeMvaP > 0 &&
	       decayModeM > 0 && decayModeMvaM > 0 ) {

	    // rho/a1(1-prong)+rho/a1(1-prong)
	    if ((decayModeMvaP == 1 || decayModeMvaP == 2) &&
		(decayModeMvaM == 1 || decayModeMvaM == 2) ){
	      product.m_recoPhiStarCPRho = cpq.CalculatePhiStarCPRho(momentumP, momentumM, piZeroP, piZeroM);

	      // azimuthal angles of the tau decay planes
	      product.m_recoPhiPlusRhoMeth = cpq.GetRecoPhiPlusRhoMeth();
	      product.m_recoPhiMinusRhoMeth = cpq.GetRecoPhiMinusRhoMeth();
	      product.m_recoPhiStarPlusRhoMeth = cpq.GetRecoPhiStarPlusRhoMeth();
	      product.m_recoPhiStarMinusRhoMeth = cpq.GetRecoPhiStarMinusRhoMeth();

	      //fill additional variable to produce a merged phiStarCP plot with increased statistics
	      product.m_recoPhiStarCPRhoMerged = cpq.CalculatePhiStarCPRho(momentumP, momentumM, piZeroP, piZeroM, true);
	    }
	    // rho/a1(1-prong)+3-prongs
	    else if ((decayModeMvaP == 1  || decayModeMvaP == 2) &&
		     (decayModeMvaM == 10 || decayModeMvaM == 11) ) {
	      product.m_recoPhiStarCPRho = cpq.CalculatePhiStarCPRho(momentumP, piSSFromRhoM, piZeroP, piOSM);

	      // azimuthal angles of the tau decay planes
	      product.m_recoPhiPlusRhoMeth = cpq.GetRecoPhiPlusRhoMeth();
	      product.m_recoPhiMinusRhoMeth = cpq.GetRecoPhiMinusRhoMeth();
	      product.m_recoPhiStarPlusRhoMeth = cpq.GetRecoPhiStarPlusRhoMeth();
	      product.m_recoPhiStarMinusRhoMeth = cpq.GetRecoPhiStarMinusRhoMeth();

	      //fill additional variable to produce a merged phiStarCP plot with increased statistics
	      product.m_recoPhiStarCPRhoMerged = cpq.CalculatePhiStarCPRho(momentumP, piSSFromRhoM, piZeroP, piOSM, true);
	    }
	    // 3-prongs+rho/a1(1-prong)
	    else if ((decayModeMvaP==10 || decayModeMvaP == 11) &&
		     (decayModeMvaM==1  || decayModeMvaM == 2) ) {
	      product.m_recoPhiStarCPRho = cpq.CalculatePhiStarCPRho(piSSFromRhoP, momentumM, piOSP, piZeroM);

	      // azimuthal angles of the tau decay planes
	      product.m_recoPhiPlusRhoMeth = cpq.GetRecoPhiPlusRhoMeth();
	      product.m_recoPhiMinusRhoMeth = cpq.GetRecoPhiMinusRhoMeth();
	      product.m_recoPhiStarPlusRhoMeth = cpq.GetRecoPhiStarPlusRhoMeth();
	      product.m_recoPhiStarMinusRhoMeth = cpq.GetRecoPhiStarMinusRhoMeth();

	      //fill additional variable to produce a merged phiStarCP plot with increased statistics
	      product.m_recoPhiStarCPRhoMerged = cpq.CalculatePhiStarCPRho(piSSFromRhoP, momentumM, piOSP, piZeroM, true);
	    }
	    // 3-prongs+3-prongs
	    else if ((decayModeMvaP == 10 || decayModeMvaP == 11) &&
		     (decayModeMvaM == 10 || decayModeMvaM == 11) ) {
	      product.m_recoPhiStarCPRho = cpq.CalculatePhiStarCPRho(piSSFromRhoP, piSSFromRhoM, piOSP, piOSM);

	      // azimuthal angles of the tau decay planes
	      product.m_recoPhiPlusRhoMeth = cpq.GetRecoPhiPlusRhoMeth();
	      product.m_recoPhiMinusRhoMeth = cpq.GetRecoPhiMinusRhoMeth();
	      product.m_recoPhiStarPlusRhoMeth = cpq.GetRecoPhiStarPlusRhoMeth();
	      product.m_recoPhiStarMinusRhoMeth = cpq.GetRecoPhiStarMinusRhoMeth();

	      //fill additional variable to produce a merged phiStarCP plot with increased statistics
	      product.m_recoPhiStarCPRhoMerged = cpq.CalculatePhiStarCPRho(piSSFromRhoP, piSSFromRhoM, piOSP, piOSM, true);
	    }
	  }
	}

	// ---------
	// ip-method (IP+IP)
	// ---------
	// phi*CP wrt nominalPV
	product.m_recoPhiStarCP = cpq.CalculatePhiStarCP(&(event.m_vertexSummary->pv), trackP, trackM, momentumP, momentumM);

	// Calculate the phi*cp by taking the ipvectors from the helical approach as arguments
	if (recoParticle1->getHash() == chargedPart1->getHash()){
		IPPlusHel  = product.m_recoIPHel_1;
		IPMinusHel = product.m_recoIPHel_2;
	} else {
		IPPlusHel  = product.m_recoIPHel_2;
		IPMinusHel = product.m_recoIPHel_1;
	}
	product.m_recoPhiStarCPHel = cpq.CalculatePhiStarCP(momentumP, momentumM, IPPlusHel, IPMinusHel, "reco");

	// ---------
	// comb-method (IP+DP)
	// ---------
	// The combined method is possible if one tau_h->rho is present in the channel (i.e. et, mt, tt).
	// In the tt ch., we want to use the combined method when only one of the two taus decays to rho.
	// If both taus decay to rho, then the rho method is preferred.
	KTau* recoTau1 = dynamic_cast<KTau*>(recoParticle1);
	RMFLV piZero1(0,0,0,0);
	RMFLV piSSFromRho1(0,0,0,0);
	RMFLV piSSHighPt1(0,0,0,0);
	RMFLV piOS1(0,0,0,0);
	int dmMva_1(-999);
	unsigned int decayType1 = 0;//0: lep or pi, 1: rho or a1(1-prong), 2: 3-prongs
	if (recoTau1 != nullptr) {
	  if (recoTau1->decayMode >= 0) {
	    dmMva_1 = (int)recoTau1->getDiscriminator("MVADM2017v1", event.m_tauMetadata);
	    if (dmMva_1 == 1 || dmMva_1 == 2)
	      decayType1 = 1;
	    else if(dmMva_1 == 10 || dmMva_1 == 11)
	      decayType1 = 2;
	  }
	}
	KTau* recoTau2 = dynamic_cast<KTau*>(recoParticle2);
	RMFLV piZero2(0,0,0,0);
	RMFLV piSSFromRho2(0,0,0,0);
	RMFLV piSSHighPt2(0,0,0,0);
	RMFLV piOS2(0,0,0,0);
	int dmMva_2(-999);
	unsigned int decayType2 = 0;//0: lep or pi, 1: rho or a1(1-prong), 2: 3-prongs
	if (recoTau2 != nullptr) {
	  if (recoTau2->decayMode >= 0) {
	    dmMva_2 = (int)recoTau2->getDiscriminator("MVADM2017v1", event.m_tauMetadata);
	    if (dmMva_2 == 1 || dmMva_2 == 2)
	      decayType2 = 1;
	    else if(dmMva_2 == 10 || dmMva_2 == 11)
	      decayType2 = 2;
	  }
	}
	if (recoParticle1->getHash() == chargedPart1->getHash()) {
	  piZero1 = piZeroP;
	  piSSFromRho1 = piSSFromRhoP;
	  piSSHighPt1 = piSSHighPtP;
	  piOS1 = piOSP;
	  piZero2 = piZeroM;
	  piSSFromRho2 = piSSFromRhoM;
	  piSSHighPt2 = piSSHighPtM;
	  piOS2 = piOSM;
	}
	else {
	  piZero1 = piZeroM;
	  piSSFromRho1 = piSSFromRhoM;
	  piSSHighPt1 = piSSHighPtM;
	  piOS1 = piOSM;
	  piZero2 = piZeroP;
	  piSSFromRho2 = piSSFromRhoP;
	  piSSHighPt2 = piSSHighPtP;
	  piOS2 = piOSP;
	}

	if ( (product.m_decayChannel == HttEnumTypes::DecayChannel::MT || product.m_decayChannel == HttEnumTypes::DecayChannel::ET) ){

		// l+rho/a1(1-prong)
		if (decayType2 == 1) {
			product.m_recoPhiStarCPComb          = cpq.CalculatePhiStarCPComb(product.m_recoIP1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, piZero2, recoParticle1->charge());
			product.m_recoPhiStarCPCombHel       = cpq.CalculatePhiStarCPComb(product.m_recoIPHel_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, piZero2, recoParticle1->charge());

			product.m_recoPhiStarCPCombMerged    = cpq.CalculatePhiStarCPComb(product.m_recoIP1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, piZero2, recoParticle1->charge(), true);
			product.m_recoPhiStarCPCombMergedHel = cpq.CalculatePhiStarCPComb(product.m_recoIPHel_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, piZero2, recoParticle1->charge(), true);
		}
		// l+3-prongs
		else if (decayType2 == 2) {
			product.m_recoPhiStarCPComb          = cpq.CalculatePhiStarCPComb(product.m_recoIP1, recoParticle1->p4, piSSFromRho2, piOS2, recoParticle1->charge());
			product.m_recoPhiStarCPCombHel       = cpq.CalculatePhiStarCPComb(product.m_recoIPHel_1, recoParticle1->p4, piSSFromRho2, piOS2, recoParticle1->charge());

			product.m_recoPhiStarCPCombMerged    = cpq.CalculatePhiStarCPComb(product.m_recoIP1, recoParticle1->p4, piSSFromRho2, piOS2, recoParticle1->charge(), true);
			product.m_recoPhiStarCPCombMergedHel = cpq.CalculatePhiStarCPComb(product.m_recoIPHel_1, recoParticle1->p4, piSSFromRho2, piOS2, recoParticle1->charge(), true);
		}
	}  // if et or mt ch.
	if ( product.m_decayChannel == HttEnumTypes::DecayChannel::TT ) {
		// rho/a1(1-prong)+pi
		if (decayType1 == 1 && decayType2 == 0) {
			product.m_recoPhiStarCPComb          = cpq.CalculatePhiStarCPComb(product.m_recoIP2, recoTau2->chargedHadronCandidates.at(0).p4, recoTau1->chargedHadronCandidates.at(0).p4, piZero1, recoTau2->charge());
			product.m_recoPhiStarCPCombHel       = cpq.CalculatePhiStarCPComb(product.m_recoIPHel_2, recoTau2->chargedHadronCandidates.at(0).p4, recoTau1->chargedHadronCandidates.at(0).p4, piZero1, recoTau2->charge());

			product.m_recoPhiStarCPCombMerged    = cpq.CalculatePhiStarCPComb(product.m_recoIP2, recoTau2->chargedHadronCandidates.at(0).p4, recoTau1->chargedHadronCandidates.at(0).p4, piZero1, recoTau2->charge(), true);
			product.m_recoPhiStarCPCombMergedHel = cpq.CalculatePhiStarCPComb(product.m_recoIPHel_2, recoTau2->chargedHadronCandidates.at(0).p4, recoTau1->chargedHadronCandidates.at(0).p4, piZero1, recoTau2->charge(), true);
		}
		// 3-prongs+pi
		else if (decayType1 == 2 && decayType2 == 0) {
			product.m_recoPhiStarCPComb          = cpq.CalculatePhiStarCPComb(product.m_recoIP2, recoTau2->chargedHadronCandidates.at(0).p4, piSSFromRho1, piOS1, recoTau2->charge());
			product.m_recoPhiStarCPCombHel       = cpq.CalculatePhiStarCPComb(product.m_recoIPHel_2, recoTau2->chargedHadronCandidates.at(0).p4, piSSFromRho1, piZero1, recoTau2->charge());

			product.m_recoPhiStarCPCombMerged    = cpq.CalculatePhiStarCPComb(product.m_recoIP2, recoTau2->chargedHadronCandidates.at(0).p4, piSSFromRho1, piOS1, recoTau2->charge(), true);
			product.m_recoPhiStarCPCombMergedHel = cpq.CalculatePhiStarCPComb(product.m_recoIPHel_2, recoTau2->chargedHadronCandidates.at(0).p4, piSSFromRho1, piOS1, recoTau2->charge(), true);
		}
		// pi+rho/a1(1-prong)
		else if (decayType1 == 0 && decayType2 == 1) {
			product.m_recoPhiStarCPComb          = cpq.CalculatePhiStarCPComb(product.m_recoIP1, recoTau1->chargedHadronCandidates.at(0).p4, recoTau2->chargedHadronCandidates.at(0).p4, piZero2, recoTau1->charge());
			product.m_recoPhiStarCPCombHel       = cpq.CalculatePhiStarCPComb(product.m_recoIPHel_1, recoTau1->chargedHadronCandidates.at(0).p4, recoTau2->chargedHadronCandidates.at(0).p4, piZero2, recoTau1->charge());

			product.m_recoPhiStarCPCombMerged    = cpq.CalculatePhiStarCPComb(product.m_recoIP1, recoTau1->chargedHadronCandidates.at(0).p4, recoTau2->chargedHadronCandidates.at(0).p4, piZero2, recoTau1->charge(), true);
			product.m_recoPhiStarCPCombMergedHel = cpq.CalculatePhiStarCPComb(product.m_recoIPHel_1, recoTau1->chargedHadronCandidates.at(0).p4, recoTau2->chargedHadronCandidates.at(0).p4, piZero2, recoTau1->charge(), true);
		}
		// pi+3-prongs
		else if (decayType1 == 0 && decayType2 == 2) {
			product.m_recoPhiStarCPComb          = cpq.CalculatePhiStarCPComb(product.m_recoIP1, recoTau1->chargedHadronCandidates.at(0).p4, piSSFromRho2, piOS2, recoTau1->charge());
			product.m_recoPhiStarCPCombHel       = cpq.CalculatePhiStarCPComb(product.m_recoIPHel_1, recoTau1->chargedHadronCandidates.at(0).p4, piSSFromRho2, piOS2, recoTau1->charge());

			product.m_recoPhiStarCPCombMerged    = cpq.CalculatePhiStarCPComb(product.m_recoIP1, recoTau1->chargedHadronCandidates.at(0).p4, piSSFromRho2, piOS2, recoTau1->charge(), true);
			product.m_recoPhiStarCPCombMergedHel = cpq.CalculatePhiStarCPComb(product.m_recoIPHel_1, recoTau1->chargedHadronCandidates.at(0).p4, piSSFromRho2, piOS2, recoTau1->charge(), true);
		}
	}  // if tt ch.

	// Calculate the psi+- without a refitted vertex
	if (recoParticle1->charge() == +1){
		product.m_cosPsiPlus  = cpq.CalculateCosPsi(recoParticle2->p4, product.m_recoIP1);
		product.m_cosPsiMinus = cpq.CalculateCosPsi(recoParticle2->p4, product.m_recoIP2);
		product.m_cosPsiPlusHel  = cpq.CalculateCosPsi(recoParticle2->p4, product.m_recoIPHel_1);
		product.m_cosPsiMinusHel = cpq.CalculateCosPsi(recoParticle2->p4, product.m_recoIPHel_2);
	} else {
		product.m_cosPsiPlus  = cpq.CalculateCosPsi(recoParticle2->p4, product.m_recoIP2);
		product.m_cosPsiMinus = cpq.CalculateCosPsi(recoParticle1->p4, product.m_recoIP1);
		product.m_cosPsiPlusHel  = cpq.CalculateCosPsi(recoParticle2->p4, product.m_recoIPHel_2);
		product.m_cosPsiMinusHel = cpq.CalculateCosPsi(recoParticle1->p4, product.m_recoIPHel_1);
	}

	// calculate cosPsi
	if (recoParticle1->charge() == +1){
		product.m_cosPsiPlusrPV  = cpq.CalculateCosPsi(recoParticle1->p4, product.m_recoIPrPV_1);
		product.m_cosPsiMinusrPV = cpq.CalculateCosPsi(recoParticle2->p4, product.m_recoIPrPV_2);
		product.m_cosPsiPlusHelrPV  = cpq.CalculateCosPsi(recoParticle1->p4, product.m_recoIPHelrPV_1);
		product.m_cosPsiMinusHelrPV = cpq.CalculateCosPsi(recoParticle2->p4, product.m_recoIPHelrPV_2);

		product.m_cosPsiPlusrPVBS  = cpq.CalculateCosPsi(recoParticle1->p4, product.m_recoIPrPVBS_1);
		product.m_cosPsiMinusrPVBS = cpq.CalculateCosPsi(recoParticle2->p4, product.m_recoIPrPVBS_2);
		product.m_cosPsiPlusHelrPVBS  = cpq.CalculateCosPsi(recoParticle1->p4, product.m_recoIPHelrPVBS_1);
		product.m_cosPsiMinusHelrPVBS = cpq.CalculateCosPsi(recoParticle2->p4, product.m_recoIPHelrPVBS_2);
	} else {
		product.m_cosPsiPlusrPV  = cpq.CalculateCosPsi(recoParticle2->p4, product.m_recoIPrPV_2);
		product.m_cosPsiMinusrPV = cpq.CalculateCosPsi(recoParticle1->p4, product.m_recoIPrPV_1);
		product.m_cosPsiPlusHelrPV  = cpq.CalculateCosPsi(recoParticle2->p4, product.m_recoIPrPV_2);
		product.m_cosPsiMinusHelrPV = cpq.CalculateCosPsi(recoParticle1->p4, product.m_recoIPrPV_1);

		product.m_cosPsiPlusrPVBS  = cpq.CalculateCosPsi(recoParticle2->p4, product.m_recoIPrPVBS_2);
		product.m_cosPsiMinusrPVBS = cpq.CalculateCosPsi(recoParticle1->p4, product.m_recoIPrPVBS_1);
		product.m_cosPsiPlusHelrPVBS  = cpq.CalculateCosPsi(recoParticle2->p4, product.m_recoIPHelrPVBS_2);
		product.m_cosPsiMinusHelrPVBS = cpq.CalculateCosPsi(recoParticle1->p4, product.m_recoIPHelrPVBS_1);
	}

	// calculate phi*cp using the refitted PV
	// FIXME two functions are called, need to remove one of the two
	// in this case, the ipvectors are calculated within the CalculatePhiStarCP functions
	product.m_recoPhiStarCPrPV = cpq.CalculatePhiStarCP(rPV, trackP, trackM, momentumP, momentumM);
	product.m_recoPhiStarCPrPVBS = cpq.CalculatePhiStarCP(rPVBS, trackP, trackM, momentumP, momentumM);

	// azimuthal angles of the tau decay planes
	product.m_recoPhiPlusIPMeth = cpq.GetRecoPhiPlusIPMeth();
	product.m_recoPhiMinusIPMeth = cpq.GetRecoPhiMinusIPMeth();
	product.m_recoPhiStarPlusIPMeth = cpq.GetRecoPhiStarPlusIPMeth();
	product.m_recoPhiStarMinusIPMeth = cpq.GetRecoPhiStarMinusIPMeth();

	// get the IP vectors corresponding to charge+ and charge- particles
	if (recoParticle1->getHash() == chargedPart1->getHash()){
	  IPPlusHelrPV  = product.m_recoIPHelrPV_1;
	  IPMinusHelrPV = product.m_recoIPHelrPV_2;
	  IPPlusHelrPVBS  = product.m_recoIPHelrPVBS_1;
	  IPMinusHelrPVBS = product.m_recoIPHelrPVBS_2;
	} else {
	  IPPlusHelrPV  =  product.m_recoIPHelrPV_2;
	  IPMinusHelrPV =  product.m_recoIPHelrPV_1;
	  IPPlusHelrPVBS  =  product.m_recoIPHelrPVBS_2;
	  IPMinusHelrPVBS =  product.m_recoIPHelrPVBS_1;
	}
	// The Helical Approach
	product.m_recoPhiStarCPHelrPV   = cpq.CalculatePhiStarCP(momentumP, momentumM, IPPlusHelrPV, IPMinusHelrPV, "reco");
	product.m_recoPhiStarCPHelrPVBS = cpq.CalculatePhiStarCP(momentumP, momentumM, IPPlusHelrPVBS, IPMinusHelrPVBS, "reco");
	// The Tangential Approach
	product.m_recoPhiStarCPrPV   = cpq.CalculatePhiStarCP(rPV, trackP, trackM, momentumP, momentumM);
	product.m_recoPhiStarCPrPVBS = cpq.CalculatePhiStarCP(rPVBS, trackP, trackM, momentumP, momentumM);

	// ---------
	// comb-method (IP+DP) with refitted PV
	// ---------
	if ( (product.m_decayChannel == HttEnumTypes::DecayChannel::MT || product.m_decayChannel == HttEnumTypes::DecayChannel::ET) ) {

	  // l+rho/a1(1-prong)
	  if (decayType2 == 1) {
	    product.m_recoPhiStarCPCombrPV            = cpq.CalculatePhiStarCPComb(product.m_recoIPrPV_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, piZero2, recoParticle1->charge());
	    product.m_recoPhiStarCPCombrPVBS          = cpq.CalculatePhiStarCPComb(product.m_recoIPrPVBS_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, piZero2, recoParticle1->charge());
	    product.m_recoPhiStarCPCombHelrPV         = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPV_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, piZero2, recoParticle1->charge());
	    product.m_recoPhiStarCPCombHelrPVBS       = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPVBS_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, piZero2, recoParticle1->charge());

	    product.m_recoPhiStarCPCombMergedrPV      = cpq.CalculatePhiStarCPComb(product.m_recoIPrPV_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, piZero2, recoParticle1->charge(), true);
	    product.m_recoPhiStarCPCombMergedrPVBS    = cpq.CalculatePhiStarCPComb(product.m_recoIPrPVBS_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, piZero2, recoParticle1->charge(), true);
	    product.m_recoPhiStarCPCombMergedHelrPV   = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPV_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, piZero2, recoParticle1->charge(), true);
	    product.m_recoPhiStarCPCombMergedHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPVBS_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, piZero2, recoParticle1->charge(), true);
	  }
	  // l+3-prongs
	  else if (decayType2 == 2) {
	    product.m_recoPhiStarCPCombrPV            = cpq.CalculatePhiStarCPComb(product.m_recoIPrPV_1, recoParticle1->p4, piSSFromRho2, piOS2, recoParticle1->charge());
	    product.m_recoPhiStarCPCombrPVBS          = cpq.CalculatePhiStarCPComb(product.m_recoIPrPVBS_1, recoParticle1->p4, piSSFromRho2, piOS2, recoParticle1->charge());
	    product.m_recoPhiStarCPCombHelrPV         = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPV_1, recoParticle1->p4, piSSFromRho2, piOS2, recoParticle1->charge());
	    product.m_recoPhiStarCPCombHelrPVBS       = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPVBS_1, recoParticle1->p4, piSSFromRho2, piOS2, recoParticle1->charge());

	    product.m_recoPhiStarCPCombMergedrPV      = cpq.CalculatePhiStarCPComb(product.m_recoIPrPV_1, recoParticle1->p4, piSSFromRho2, piOS2, recoParticle1->charge(), true);
	    product.m_recoPhiStarCPCombMergedrPVBS    = cpq.CalculatePhiStarCPComb(product.m_recoIPrPVBS_1, recoParticle1->p4, piSSFromRho2, piOS2, recoParticle1->charge(), true);
	    product.m_recoPhiStarCPCombMergedHelrPV   = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPV_1, recoParticle1->p4, piSSFromRho2, piOS2, recoParticle1->charge(), true);
	    product.m_recoPhiStarCPCombMergedHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPVBS_1, recoParticle1->p4, piSSFromRho2, piOS2, recoParticle1->charge(), true);
	  }
	}  // if et or mt ch.
	if ( product.m_decayChannel == HttEnumTypes::DecayChannel::TT ) {
		// pi + pi: check m_recoPhiStarCPrPVBS
		// rho/a1(1-prong) + rho/a1(1-prong): check m_recoPhiStarCPRhoMerged
	  // rho/a1(1-prong)+pi
	  if (decayType1 == 1 && decayType2 == 0) {
	    product.m_recoPhiStarCPCombrPV      = cpq.CalculatePhiStarCPComb(product.m_recoIPrPV_2, recoTau2->chargedHadronCandidates.at(0).p4, recoTau1->chargedHadronCandidates.at(0).p4, piZero1, recoTau2->charge());
	    product.m_recoPhiStarCPCombrPVBS    = cpq.CalculatePhiStarCPComb(product.m_recoIPrPVBS_2, recoTau2->chargedHadronCandidates.at(0).p4, recoTau1->chargedHadronCandidates.at(0).p4, piZero1, recoTau2->charge());
	    product.m_recoPhiStarCPCombHelrPV   = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPV_2, recoTau2->chargedHadronCandidates.at(0).p4, recoTau1->chargedHadronCandidates.at(0).p4, piZero1, recoTau2->charge());
	    product.m_recoPhiStarCPCombHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPVBS_2, recoTau2->chargedHadronCandidates.at(0).p4, recoTau1->chargedHadronCandidates.at(0).p4, piZero1, recoTau2->charge());

	    product.m_recoPhiStarCPCombMergedrPV      = cpq.CalculatePhiStarCPComb(product.m_recoIPrPV_2, recoTau2->chargedHadronCandidates.at(0).p4, recoTau1->chargedHadronCandidates.at(0).p4, piZero1, recoTau2->charge(), true);
	    product.m_recoPhiStarCPCombMergedrPVBS    = cpq.CalculatePhiStarCPComb(product.m_recoIPrPVBS_2, recoTau2->chargedHadronCandidates.at(0).p4, recoTau1->chargedHadronCandidates.at(0).p4, piZero1, recoTau2->charge(), true);
	    product.m_recoPhiStarCPCombMergedHelrPV   = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPV_2, recoTau2->chargedHadronCandidates.at(0).p4, recoTau1->chargedHadronCandidates.at(0).p4, piZero1, recoTau2->charge(), true);
	    product.m_recoPhiStarCPCombMergedHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPVBS_2, recoTau2->chargedHadronCandidates.at(0).p4, recoTau1->chargedHadronCandidates.at(0).p4, piZero1, recoTau2->charge(), true);
	  }
	  // 3-prongs+pi
	  else if (decayType1 == 2 && decayType2 == 0) {
	    product.m_recoPhiStarCPCombrPV      = cpq.CalculatePhiStarCPComb(product.m_recoIPrPV_2, recoTau2->chargedHadronCandidates.at(0).p4, piSSFromRho1, piOS1, recoTau2->charge());
	    product.m_recoPhiStarCPCombrPVBS    = cpq.CalculatePhiStarCPComb(product.m_recoIPrPVBS_2, recoTau2->chargedHadronCandidates.at(0).p4, piSSFromRho1, piOS1, recoTau2->charge());
	    product.m_recoPhiStarCPCombHelrPV   = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPV_2, recoTau2->chargedHadronCandidates.at(0).p4, piSSFromRho1, piOS1, recoTau2->charge());
	    product.m_recoPhiStarCPCombHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPVBS_2, recoTau2->chargedHadronCandidates.at(0).p4, piSSFromRho1, piOS1, recoTau2->charge());

	    product.m_recoPhiStarCPCombMergedrPV      = cpq.CalculatePhiStarCPComb(product.m_recoIPrPV_2, recoTau2->chargedHadronCandidates.at(0).p4, piSSFromRho1, piOS1, recoTau2->charge(), true);
	    product.m_recoPhiStarCPCombMergedrPVBS    = cpq.CalculatePhiStarCPComb(product.m_recoIPrPVBS_2, recoTau2->chargedHadronCandidates.at(0).p4, piSSFromRho1, piOS1, recoTau2->charge(), true);
	    product.m_recoPhiStarCPCombMergedHelrPV   = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPV_2, recoTau2->chargedHadronCandidates.at(0).p4, piSSFromRho1, piOS1, recoTau2->charge(), true);
	    product.m_recoPhiStarCPCombMergedHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPVBS_2, recoTau2->chargedHadronCandidates.at(0).p4, piSSFromRho1, piOS1, recoTau2->charge(), true);
	  }
	  // pi+rho/a1(1-prong)
	  else if (decayType1 == 0 && decayType2 == 1) {
	    product.m_recoPhiStarCPCombrPV      = cpq.CalculatePhiStarCPComb(product.m_recoIPrPV_1, recoTau1->chargedHadronCandidates.at(0).p4, recoTau2->chargedHadronCandidates.at(0).p4, piZero2, recoTau1->charge());
	    product.m_recoPhiStarCPCombrPVBS    = cpq.CalculatePhiStarCPComb(product.m_recoIPrPVBS_1, recoTau1->chargedHadronCandidates.at(0).p4, recoTau2->chargedHadronCandidates.at(0).p4, piZero2, recoTau1->charge());
	    product.m_recoPhiStarCPCombHelrPV   = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPV_1, recoTau1->chargedHadronCandidates.at(0).p4, recoTau2->chargedHadronCandidates.at(0).p4, piZero2, recoTau1->charge());
	    product.m_recoPhiStarCPCombHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPVBS_1, recoTau1->chargedHadronCandidates.at(0).p4, recoTau2->chargedHadronCandidates.at(0).p4, piZero2, recoTau1->charge());

	    product.m_recoPhiStarCPCombMergedrPV      = cpq.CalculatePhiStarCPComb(product.m_recoIPrPV_1, recoTau1->chargedHadronCandidates.at(0).p4, recoTau2->chargedHadronCandidates.at(0).p4, piZero2, recoTau1->charge(), true);
	    product.m_recoPhiStarCPCombMergedrPVBS    = cpq.CalculatePhiStarCPComb(product.m_recoIPrPVBS_1, recoTau1->chargedHadronCandidates.at(0).p4, recoTau2->chargedHadronCandidates.at(0).p4, piZero2, recoTau1->charge(), true);
	    product.m_recoPhiStarCPCombMergedHelrPV   = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPV_1, recoTau1->chargedHadronCandidates.at(0).p4, recoTau2->chargedHadronCandidates.at(0).p4, piZero2, recoTau1->charge(), true);
	    product.m_recoPhiStarCPCombMergedHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPVBS_1, recoTau1->chargedHadronCandidates.at(0).p4, recoTau2->chargedHadronCandidates.at(0).p4, piZero2, recoTau1->charge(), true);
	  }
	  // pi+3-prongs
	  else if (decayType1 == 0 && decayType2 == 2) {
	    product.m_recoPhiStarCPCombrPV      = cpq.CalculatePhiStarCPComb(product.m_recoIPrPV_1, recoTau1->chargedHadronCandidates.at(0).p4, piSSFromRho2, piOS2, recoTau1->charge());
	    product.m_recoPhiStarCPCombrPVBS    = cpq.CalculatePhiStarCPComb(product.m_recoIPrPVBS_1, recoTau1->chargedHadronCandidates.at(0).p4, piSSFromRho2, piOS2, recoTau1->charge());
	    product.m_recoPhiStarCPCombHelrPV   = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPV_1, recoTau1->chargedHadronCandidates.at(0).p4, piSSFromRho2, piOS2, recoTau1->charge());
	    product.m_recoPhiStarCPCombHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPVBS_1, recoTau1->chargedHadronCandidates.at(0).p4, piSSFromRho2, piOS2, recoTau1->charge());

	    product.m_recoPhiStarCPCombMergedrPV      = cpq.CalculatePhiStarCPComb(product.m_recoIPrPV_1, recoTau1->chargedHadronCandidates.at(0).p4, piSSFromRho2, piOS2, recoTau1->charge(), true);
	    product.m_recoPhiStarCPCombMergedrPVBS    = cpq.CalculatePhiStarCPComb(product.m_recoIPrPVBS_1, recoTau1->chargedHadronCandidates.at(0).p4, piSSFromRho2, piOS2, recoTau1->charge(), true);
	    product.m_recoPhiStarCPCombMergedHelrPV   = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPV_1, recoTau1->chargedHadronCandidates.at(0).p4, piSSFromRho2, piOS2, recoTau1->charge(), true);
	    product.m_recoPhiStarCPCombMergedHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPVBS_1, recoTau1->chargedHadronCandidates.at(0).p4, piSSFromRho2, piOS2, recoTau1->charge(), true);
	  }
	  // rho/a1(1-prong)+3-prongs
	  if (decayType1 == 1 && decayType2 == 2) {
	    product.m_recoPhiStarCPCombrPV      = cpq.CalculatePhiStarCPCommon(recoTau1->chargedHadronCandidates.at(0).p4, piSSFromRho2, piZero1, piOS2, recoTau1->charge(), false, false, "");
	    product.m_recoPhiStarCPCombrPVBS    = cpq.CalculatePhiStarCPCommon(recoTau1->chargedHadronCandidates.at(0).p4, piSSFromRho2, piZero1, piOS2, recoTau1->charge(), false, false, "");
	    product.m_recoPhiStarCPCombHelrPV   = cpq.CalculatePhiStarCPCommon(recoTau1->chargedHadronCandidates.at(0).p4, piSSFromRho2, piZero1, piOS2, recoTau1->charge(), false, false, "");
	    product.m_recoPhiStarCPCombHelrPVBS = cpq.CalculatePhiStarCPCommon(recoTau1->chargedHadronCandidates.at(0).p4, piSSFromRho2, piZero1, piOS2, recoTau1->charge(), false, false, "");

	    product.m_recoPhiStarCPCombMergedrPV      = cpq.CalculatePhiStarCPCommon(recoTau1->chargedHadronCandidates.at(0).p4, piSSFromRho2, piZero1, piOS2, recoTau1->charge(), true, true, "");
	    product.m_recoPhiStarCPCombMergedrPVBS    = cpq.CalculatePhiStarCPCommon(recoTau1->chargedHadronCandidates.at(0).p4, piSSFromRho2, piZero1, piOS2, recoTau1->charge(), true, true, "");
	    product.m_recoPhiStarCPCombMergedHelrPV   = cpq.CalculatePhiStarCPCommon(recoTau1->chargedHadronCandidates.at(0).p4, piSSFromRho2, piZero1, piOS2, recoTau1->charge(), true, true, "");
	    product.m_recoPhiStarCPCombMergedHelrPVBS = cpq.CalculatePhiStarCPCommon(recoTau1->chargedHadronCandidates.at(0).p4, piSSFromRho2, piZero1, piOS2, recoTau1->charge(), true, true, "");
	  }
	  // 3-prongs+rho/a1(1-prong)
	  if (decayType1 == 2 && decayType2 == 1) {
	    product.m_recoPhiStarCPCombrPV      = cpq.CalculatePhiStarCPCommon(recoTau2->chargedHadronCandidates.at(0).p4, piSSFromRho1, piZero2, piOS1, recoTau2->charge(), false, false, "");
	    product.m_recoPhiStarCPCombrPVBS    = cpq.CalculatePhiStarCPCommon(recoTau2->chargedHadronCandidates.at(0).p4, piSSFromRho1, piZero2, piOS1, recoTau2->charge(), false, false, "");
	    product.m_recoPhiStarCPCombHelrPV   = cpq.CalculatePhiStarCPCommon(recoTau2->chargedHadronCandidates.at(0).p4, piSSFromRho1, piZero2, piOS1, recoTau2->charge(), false, false, "");
	    product.m_recoPhiStarCPCombHelrPVBS = cpq.CalculatePhiStarCPCommon(recoTau2->chargedHadronCandidates.at(0).p4, piSSFromRho1, piZero2, piOS1, recoTau2->charge(), false, false, "");

	    product.m_recoPhiStarCPCombMergedrPV      = cpq.CalculatePhiStarCPCommon(recoTau2->chargedHadronCandidates.at(0).p4, piSSFromRho1, piZero2, piOS1, recoTau2->charge(), true, true, "");
	    product.m_recoPhiStarCPCombMergedrPVBS    = cpq.CalculatePhiStarCPCommon(recoTau2->chargedHadronCandidates.at(0).p4, piSSFromRho1, piZero2, piOS1, recoTau2->charge(), true, true, "");
	    product.m_recoPhiStarCPCombMergedHelrPV   = cpq.CalculatePhiStarCPCommon(recoTau2->chargedHadronCandidates.at(0).p4, piSSFromRho1, piZero2, piOS1, recoTau2->charge(), true, true, "");
	    product.m_recoPhiStarCPCombMergedHelrPVBS = cpq.CalculatePhiStarCPCommon(recoTau2->chargedHadronCandidates.at(0).p4, piSSFromRho1, piZero2, piOS1, recoTau2->charge(), true, true, "");
	  }
	  // 3-prongs+3-prongs
	  else if (decayType1 == 2 && decayType2 == 2) {
	    product.m_recoPhiStarCPCombrPV      = cpq.CalculatePhiStarCPCommon(piSSFromRho1, piSSFromRho2, piOS1,piOS2, recoTau1->charge(), false, false, "");
	    product.m_recoPhiStarCPCombrPVBS    = cpq.CalculatePhiStarCPCommon(piSSFromRho1, piSSFromRho2, piOS1,piOS2, recoTau1->charge(), false, false, "");
	    product.m_recoPhiStarCPCombHelrPV   = cpq.CalculatePhiStarCPCommon(piSSFromRho1, piSSFromRho2, piOS1,piOS2, recoTau1->charge(), false, false, "");
	    product.m_recoPhiStarCPCombHelrPVBS = cpq.CalculatePhiStarCPCommon(piSSFromRho1, piSSFromRho2, piOS1,piOS2, recoTau1->charge(), false, false, "");

	    product.m_recoPhiStarCPCombMergedrPV      = cpq.CalculatePhiStarCPCommon(piSSFromRho1, piSSFromRho2, piOS1, piOS2, recoTau1->charge(), true, true, "");
	    product.m_recoPhiStarCPCombMergedrPVBS    = cpq.CalculatePhiStarCPCommon(piSSFromRho1, piSSFromRho2, piOS1, piOS2, recoTau1->charge(), true, true, "");
	    product.m_recoPhiStarCPCombMergedHelrPV   = cpq.CalculatePhiStarCPCommon(piSSFromRho1, piSSFromRho2, piOS1, piOS2, recoTau1->charge(), true, true, "");
	    product.m_recoPhiStarCPCombMergedHelrPVBS = cpq.CalculatePhiStarCPCommon(piSSFromRho1, piSSFromRho2, piOS1, piOS2, recoTau1->charge(), true, true, "");
	  }
	}  // if tt ch.

	// ---------
	// polarimetric vector method using GEF (polvec + polvec)
	// ---------
	// The polarimetric vector method is possible, when the tau rest frame is known
	// The GEF is able to reconstruct both taus enabling the polarimetric vector method for
	// all final states with a1+X (X=a1,rho,pi,mu,e)

	if ((product.m_simpleFitTaus.size() > 1)) // && product.m_simpleFitConverged)
	{
		KLepton* oneProng = nullptr;
		KTau* a1 = nullptr;
		RMFLV IPLVHelrPVBSOneProng;

		for (std::vector<KLepton*>::iterator leptonIt = product.m_flavourOrderedLeptons.begin();
		     leptonIt != product.m_flavourOrderedLeptons.end(); ++leptonIt)
		{
			if ((*leptonIt)->flavour() == KLeptonFlavour::TAU)
			{
				KTau* tau = static_cast<KTau*>(*leptonIt);
				int decaymode = m_useMVADecayModes ? (int)tau->getDiscriminator("MVADM2017v1", event.m_tauMetadata) : tau->decayMode;
				if ((! a1) &&
				    (decaymode == reco::PFTau::hadronicDecayMode::kThreeProng0PiZero) &&
				    (tau->chargedHadronCandidates.size() > 2) &&
				    tau->sv.valid)
				{
					a1 = tau;
				}
				else if ((! oneProng) &&
				         ((decaymode == reco::PFTau::hadronicDecayMode::kOneProng0PiZero)
				         ||(decaymode == reco::PFTau::hadronicDecayMode::kOneProng1PiZero)))
				{
					oneProng = *leptonIt;
					TVector3 IPOneProng = product.m_recoIPsHelrPVBS[*leptonIt];
					IPLVHelrPVBSOneProng.SetXYZT(IPOneProng.X(), IPOneProng.Y(), IPOneProng.Z(), 0);
				}
			}
			else if (! oneProng)
			{
				oneProng = *leptonIt;
				TVector3 IPOneProng = product.m_recoIPsHelrPVBS[*leptonIt];
				IPLVHelrPVBSOneProng.SetXYZT(IPOneProng.X(), IPOneProng.Y(), IPOneProng.Z(), 0);
			}
		}
		if (oneProng != nullptr && a1 != nullptr)
		{
			RMFLV simpleFitTau1 = product.m_simpleFitTaus[product.m_flavourOrderedLeptons.at(0)];
			RMFLV simpleFitTau2 = product.m_simpleFitTaus[product.m_flavourOrderedLeptons.at(1)];

			RMFLV Tau1Tau2ZMF = simpleFitTau1 + simpleFitTau2;
			RMFLV Tau1VisTau2ZMF = product.m_flavourOrderedLeptons.at(0)->p4 + simpleFitTau2;
			RMFLV Tau1Tau2VisZMF = simpleFitTau1 + product.m_flavourOrderedLeptons.at(1)->p4;
			RMFLV Tau1VisTau2VisZMF = product.m_flavourOrderedLeptons.at(0)->p4 + product.m_flavourOrderedLeptons.at(1)->p4;

			RMFLV Tau1Tau2PiSSFromRhoZMF, Tau1Tau2PiHighPtZMF, Tau1VisTau2PiSSFromRhoZMF, Tau1VisTau2PiHighPtZMF;

			RMFLV simpleFitTauA1 = product.m_simpleFitTaus[a1];
			RMFLV simpleFitTauOneProng = product.m_simpleFitTaus[oneProng];

			RMFLV TauOneProngTauA1ZMF = simpleFitTauA1 + simpleFitTauOneProng;
			RMFLV OneProngTauA1ZMF = oneProng->p4 + simpleFitTauA1;
			RMFLV TauOneProngA1ZMF = simpleFitTauOneProng + a1->p4;
			RMFLV OneProngA1ZMF = oneProng->p4 + a1->p4;

			RMFLV TauOneProngA1PiSSFromRhoZMF, TauOneProngA1PiHighPtZMF, OneProngA1PiSSFromRhoZMF, OneProngA1PiHighPtZMF, A1PiSSHighPt, A1PiSSFromRho;

			if (dmMva_2 == 10)
			{
				Tau1Tau2PiSSFromRhoZMF = simpleFitTau1 + piSSFromRho2;
				Tau1Tau2PiHighPtZMF = simpleFitTau1 + piSSHighPt2;
				Tau1VisTau2PiSSFromRhoZMF = product.m_flavourOrderedLeptons.at(0)->p4 + piSSFromRho2;
				Tau1VisTau2PiHighPtZMF = product.m_flavourOrderedLeptons.at(0)->p4 + piSSHighPt2;

				A1PiSSHighPt = piSSHighPt2;
				A1PiSSFromRho = piSSFromRho2;
			}
			else if (dmMva_1 == 10)
			{
				Tau1Tau2PiSSFromRhoZMF = simpleFitTau2 + piSSFromRho1;
				Tau1Tau2PiHighPtZMF = simpleFitTau2 + piSSHighPt1;
				Tau1VisTau2PiSSFromRhoZMF = product.m_flavourOrderedLeptons.at(1)->p4 + piSSFromRho1;
				Tau1VisTau2PiHighPtZMF = product.m_flavourOrderedLeptons.at(1)->p4 + piSSHighPt1;

				A1PiSSHighPt = piSSHighPt1;
				A1PiSSFromRho = piSSFromRho1;
			}
			TauOneProngA1PiSSFromRhoZMF = simpleFitTauOneProng + A1PiSSFromRho;
			TauOneProngA1PiHighPtZMF = simpleFitTauOneProng + A1PiSSHighPt;
			OneProngA1PiSSFromRhoZMF = oneProng->p4 + A1PiSSFromRho;
			OneProngA1PiHighPtZMF = oneProng->p4 + A1PiSSHighPt;

			// LOG(INFO) << "Tau1Tau2ZMF: " << Tau1Tau2ZMF;
			// LOG(INFO) << "TauOneProngTauA1ZMF: " << TauOneProngTauA1ZMF;
			//
			// LOG(INFO) << "Tau1VisTau2ZMF: " << Tau1VisTau2ZMF;
			// LOG(INFO) << "OneProngTauA1ZMF: " << OneProngTauA1ZMF;
			//
			// LOG(INFO) << "Tau1Tau2VisZMF: " << Tau1Tau2VisZMF;
			// LOG(INFO) << "TauOneProngA1ZMF: " << TauOneProngA1ZMF;
			//
			// LOG(INFO) << "Tau1VisTau2VisZMF: " << Tau1VisTau2VisZMF;
			// LOG(INFO) << "OneProngA1ZMF: " << OneProngA1ZMF;
			//
			// LOG(INFO) << "Tau1Tau2PiSSFromRhoZMF: " << Tau1Tau2PiSSFromRhoZMF;
			// LOG(INFO) << "TauOneProngA1PiSSFromRhoZMF: " << TauOneProngA1PiSSFromRhoZMF;
			//
			// LOG(INFO) << "Tau1Tau2PiHighPtZMF: " << Tau1Tau2PiHighPtZMF;
			// LOG(INFO) << "TauOneProngA1PiHighPtZMF: " << TauOneProngA1PiHighPtZMF;
			//
			// LOG(INFO) << "Tau1VisTau2PiSSFromRhoZMF: " << Tau1VisTau2PiSSFromRhoZMF;
			// LOG(INFO) << "OneProngA1PiSSFromRhoZMF: " << OneProngA1PiSSFromRhoZMF;
			//
			// LOG(INFO) << "Tau1VisTau2PiHighPtZMF: " << Tau1VisTau2PiHighPtZMF;
			// LOG(INFO) << "OneProngA1PiHighPtZMF: " << OneProngA1PiHighPtZMF;

			for (std::vector<KLepton*>::iterator lepton = product.m_flavourOrderedLeptons.begin();
				 lepton != product.m_flavourOrderedLeptons.end(); ++lepton)
			{
				std::vector<TLorentzVector> inputs;
				std::string type = "";
				int charge(-999);
				if (((*lepton)->flavour() == KLeptonFlavour::ELECTRON) || ((*lepton)->flavour() == KLeptonFlavour::MUON))
				{
					// inputs.push_back(GetInputLepton(product, *lepton));
					type = "lepton";
					// charges.push_back((*lepton)->charge());
					// DO NOTHING; Polarimetric Vector is not reconstructable on reco level for leptonic decays
				}
				else if ((*lepton)->flavour() == KLeptonFlavour::TAU)
				{
					KTau* tau = static_cast<KTau*>(*lepton);
					int dm_tau = (int)tau->getDiscriminator("MVADM2017v1", event.m_tauMetadata);
					// int dmMva = tau->decayMode;
					if ((dm_tau == 10) && (tau->chargedHadronCandidates.size() > 2))
					{
						inputs = GetInputA1(product, *lepton);
						type = "a1";
						charge = (*lepton)->charge();
					}
					else if ((dm_tau == 1) &&
					         (tau->chargedHadronCandidates.size() > 0) &&
					         ((tau->piZeroCandidates.size() > 0) || (tau->gammaCandidates.size() > 0)))
					{
						inputs = GetInputRho(product, *lepton);
						type = "rho";
						charge = (*lepton)->charge();
					}
					else if (dm_tau == 0)
					{
						inputs = GetInputPion(product, *lepton);
						type = "pion";
						charge = (*lepton)->charge();
					}
				}
				if (inputs.size() > 0 && type != "lepton")
				{
					SCalculator SpinCalculatorInterfaceTau1Tau2(type);
					SpinCalculatorInterfaceTau1Tau2.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(Tau1Tau2ZMF), charge);
					product.m_polarimetricVectorsTau1Tau2SimpleFit[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(SpinCalculatorInterfaceTau1Tau2.pv());

					SCalculator SpinCalculatorInterfaceTau1VisTau2(type);
					SpinCalculatorInterfaceTau1VisTau2.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(Tau1VisTau2ZMF), charge);
					product.m_polarimetricVectorsTau1VisTau2SimpleFit[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(SpinCalculatorInterfaceTau1VisTau2.pv());

					SCalculator SpinCalculatorInterfaceTau1Tau2Vis(type);
					SpinCalculatorInterfaceTau1Tau2Vis.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(Tau1Tau2VisZMF), charge);
					product.m_polarimetricVectorsTau1Tau2VisSimpleFit[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(SpinCalculatorInterfaceTau1Tau2Vis.pv());

					SCalculator SpinCalculatorInterfaceTau1VisTau2Vis(type);
					SpinCalculatorInterfaceTau1VisTau2Vis.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(Tau1VisTau2VisZMF), charge);
					product.m_polarimetricVectorsTau1VisTau2VisSimpleFit[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(SpinCalculatorInterfaceTau1VisTau2Vis.pv());


					SCalculator SpinCalculatorInterfaceTauOneProngTauA1(type);
					SpinCalculatorInterfaceTauOneProngTauA1.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(TauOneProngTauA1ZMF), charge);
					product.m_polarimetricVectorsTauOneProngTauA1SimpleFit[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(SpinCalculatorInterfaceTauOneProngTauA1.pv());

					SCalculator SpinCalculatorInterfaceOneProngTauA1(type);
					SpinCalculatorInterfaceOneProngTauA1.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(OneProngTauA1ZMF), charge);
					product.m_polarimetricVectorsOneProngTauA1SimpleFit[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(SpinCalculatorInterfaceOneProngTauA1.pv());

					SCalculator SpinCalculatorInterfaceTauOneProngA1(type);
					SpinCalculatorInterfaceTauOneProngA1.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(TauOneProngA1ZMF), charge);
					product.m_polarimetricVectorsTauOneProngA1SimpleFit[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(SpinCalculatorInterfaceTauOneProngA1.pv());

					SCalculator SpinCalculatorInterfaceOneProngA1(type);
					SpinCalculatorInterfaceOneProngA1.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(OneProngA1ZMF), charge);
					product.m_polarimetricVectorsOneProngA1SimpleFit[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(SpinCalculatorInterfaceOneProngA1.pv());

					if (dmMva_1 == 10 || dmMva_2 == 10)
					{
						SCalculator SpinCalculatorInterfaceTau1Tau2PiSSFromRho(type);
						SpinCalculatorInterfaceTau1Tau2PiSSFromRho.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(Tau1Tau2PiSSFromRhoZMF), charge);
						product.m_polarimetricVectorsTau1Tau2PiSSFromRhoSimpleFit[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(SpinCalculatorInterfaceTau1Tau2PiSSFromRho.pv());

						SCalculator SpinCalculatorInterfaceTau1Tau2PiHighPt(type);
						SpinCalculatorInterfaceTau1Tau2PiHighPt.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(Tau1Tau2PiHighPtZMF), charge);
						product.m_polarimetricVectorsTau1Tau2PiHighPtSimpleFit[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(SpinCalculatorInterfaceTau1Tau2PiHighPt.pv());

						SCalculator SpinCalculatorInterfaceTau1VisTau2PiSSFromRho(type);
						SpinCalculatorInterfaceTau1VisTau2PiSSFromRho.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(Tau1VisTau2PiSSFromRhoZMF), charge);
						product.m_polarimetricVectorsTau1VisTau2PiSSFromRhoSimpleFit[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(SpinCalculatorInterfaceTau1VisTau2PiSSFromRho.pv());

						SCalculator SpinCalculatorInterfaceTau1VisTau2PiHighPt(type);
						SpinCalculatorInterfaceTau1VisTau2PiHighPt.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(Tau1VisTau2PiHighPtZMF), charge);
						product.m_polarimetricVectorsTau1VisTau2PiHighPtSimpleFit[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(SpinCalculatorInterfaceTau1VisTau2PiHighPt.pv());


						SCalculator SpinCalculatorInterfaceTauOneProngA1PiSSFromRho(type);
						SpinCalculatorInterfaceTauOneProngA1PiSSFromRho.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(TauOneProngA1PiSSFromRhoZMF), charge);
						product.m_polarimetricVectorsTauOneProngA1PiSSFromRhoSimpleFit[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(SpinCalculatorInterfaceTauOneProngA1PiSSFromRho.pv());

						SCalculator SpinCalculatorInterfaceTauOneProngA1PiHighPt(type);
						SpinCalculatorInterfaceTauOneProngA1PiHighPt.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(TauOneProngA1PiHighPtZMF), charge);
						product.m_polarimetricVectorsTauOneProngA1PiHighPtSimpleFit[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(SpinCalculatorInterfaceTauOneProngA1PiHighPt.pv());

						SCalculator SpinCalculatorInterfaceOneProngA1PiSSFromRho(type);
						SpinCalculatorInterfaceOneProngA1PiSSFromRho.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(OneProngA1PiSSFromRhoZMF), charge);
						product.m_polarimetricVectorsOneProngA1PiSSFromRhoSimpleFit[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(SpinCalculatorInterfaceOneProngA1PiSSFromRho.pv());

						SCalculator SpinCalculatorInterfaceOneProngA1PiHighPt(type);
						SpinCalculatorInterfaceOneProngA1PiHighPt.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(OneProngA1PiHighPtZMF), charge);
						product.m_polarimetricVectorsOneProngA1PiHighPtSimpleFit[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(SpinCalculatorInterfaceOneProngA1PiHighPt.pv());
					}
				}
			}

			// LOG(WARNING) << "RecoTauCPProducer::Produce: Polarimetric Vectors not yet supported for leptonic decays. Polarimetric Vector defaulted to (0,0,0) for muon/electron.";
			if ( product.m_decayChannel == HttEnumTypes::DecayChannel::MT || product.m_decayChannel == HttEnumTypes::DecayChannel::ET)
			{
				bool firstNegative = product.m_flavourOrderedLeptons.at(1)->charge() < 0;
				RMFLV IPLVHelrPVBS_1;
				IPLVHelrPVBS_1.SetXYZT(product.m_recoIPHelrPVBS_1.X(), product.m_recoIPHelrPVBS_1.Y(), product.m_recoIPHelrPVBS_1.Z(), 0);
				if (dmMva_2 == 10)
				{
					if(product.m_polarimetricVectorsTau1Tau2SimpleFit.size() > 0)
					{
						RMFLV::BetaVector polVecTau1Tau2_2 = product.m_polarimetricVectorsTau1Tau2SimpleFit[product.m_flavourOrderedLeptons.at(1)];
						product.m_recoPhiStarCPPolVecCombTau1Tau2HelrPVBS = cpq.CalculatePhiStarCPPolVecComb(simpleFitTau2, simpleFitTau1, polVecTau1Tau2_2, IPLVHelrPVBS_1, firstNegative);
					}
					if(product.m_polarimetricVectorsTau1VisTau2SimpleFit.size() > 0)
					{
						RMFLV::BetaVector polVecTau1VisTau2_2 = product.m_polarimetricVectorsTau1VisTau2SimpleFit[product.m_flavourOrderedLeptons.at(1)];
						product.m_recoPhiStarCPPolVecCombTau1VisTau2HelrPVBS = cpq.CalculatePhiStarCPPolVecComb(simpleFitTau2, product.m_flavourOrderedLeptons.at(0)->p4, polVecTau1VisTau2_2, IPLVHelrPVBS_1, firstNegative);
					}
					if(product.m_polarimetricVectorsTau1Tau2VisSimpleFit.size() > 0)
					{
						RMFLV::BetaVector polVecTau1Tau2Vis_2 = product.m_polarimetricVectorsTau1Tau2VisSimpleFit[product.m_flavourOrderedLeptons.at(1)];
						product.m_recoPhiStarCPPolVecCombTau1Tau2VisHelrPVBS = cpq.CalculatePhiStarCPPolVecComb(product.m_flavourOrderedLeptons.at(1)->p4, simpleFitTau1, polVecTau1Tau2Vis_2, IPLVHelrPVBS_1, firstNegative);
					}
					if(product.m_polarimetricVectorsTau1VisTau2VisSimpleFit.size() > 0)
					{
						RMFLV::BetaVector polVecTau1VisTau2Vis_2 = product.m_polarimetricVectorsTau1VisTau2VisSimpleFit[product.m_flavourOrderedLeptons.at(1)];
						product.m_recoPhiStarCPPolVecCombTau1VisTau2VisHelrPVBS = cpq.CalculatePhiStarCPPolVecComb(product.m_flavourOrderedLeptons.at(1)->p4, product.m_flavourOrderedLeptons.at(0)->p4, polVecTau1VisTau2Vis_2, IPLVHelrPVBS_1, firstNegative);
					}
					if(product.m_polarimetricVectorsTau1Tau2PiSSFromRhoSimpleFit.size() > 0)
					{
						RMFLV::BetaVector polVecTau1Tau2PiSSFromRho_2 = product.m_polarimetricVectorsTau1Tau2PiSSFromRhoSimpleFit[product.m_flavourOrderedLeptons.at(1)];
						product.m_recoPhiStarCPPolVecCombTau1Tau2PiSSFromRhoHelrPVBS = cpq.CalculatePhiStarCPPolVecComb(piSSFromRho2, simpleFitTau1, polVecTau1Tau2PiSSFromRho_2, IPLVHelrPVBS_1, firstNegative);
					}
					if(product.m_polarimetricVectorsTau1Tau2PiHighPtSimpleFit.size() > 0)
					{
						RMFLV::BetaVector polVecTau1Tau2PiHighPt_2 = product.m_polarimetricVectorsTau1Tau2PiHighPtSimpleFit[product.m_flavourOrderedLeptons.at(1)];
						product.m_recoPhiStarCPPolVecCombTau1Tau2PiHighPtHelrPVBS = cpq.CalculatePhiStarCPPolVecComb(piSSHighPt2, simpleFitTau1, polVecTau1Tau2PiHighPt_2, IPLVHelrPVBS_1, firstNegative);
					}
					if(product.m_polarimetricVectorsTau1VisTau2PiSSFromRhoSimpleFit.size() > 0)
					{
						RMFLV::BetaVector polVecTau1VisTau2PiSSFromRho_2 = product.m_polarimetricVectorsTau1VisTau2PiSSFromRhoSimpleFit[product.m_flavourOrderedLeptons.at(1)];
						product.m_recoPhiStarCPPolVecCombTau1VisTau2PiSSFromRhoHelrPVBS = cpq.CalculatePhiStarCPPolVecComb(piSSFromRho2, product.m_flavourOrderedLeptons.at(0)->p4, polVecTau1VisTau2PiSSFromRho_2, IPLVHelrPVBS_1, firstNegative);
					}
					if(product.m_polarimetricVectorsTau1VisTau2PiHighPtSimpleFit.size() > 0)
					{
						RMFLV::BetaVector polVecTau1VisTau2PiHighPt_2 = product.m_polarimetricVectorsTau1VisTau2PiHighPtSimpleFit[product.m_flavourOrderedLeptons.at(1)];
						product.m_recoPhiStarCPPolVecCombTau1VisTau2PiHighPtHelrPVBS = cpq.CalculatePhiStarCPPolVecComb(piSSHighPt2, product.m_flavourOrderedLeptons.at(0)->p4, polVecTau1VisTau2PiHighPt_2, IPLVHelrPVBS_1, firstNegative);
					}

					// LOG(INFO) << "RecoTauCPProducer simpleFitTau1: " << simpleFitTau1;
					// LOG(INFO) << "RecoTauCPProducer simpleFitTau2: " << simpleFitTau2;
					// // LOG(INFO) << "RecoTauCPProducer polVec: " << polVec;
					// LOG(INFO) << "RecoTauCPProducer IPLVHelrPVBS_1: " << IPLVHelrPVBS_1;
					// LOG(INFO) << "RecoTauCPProducer piSSFromRho2: " << piSSFromRho2;
					// LOG(INFO) << "RecoTauCPProducer recoParticle1->p4: " << recoParticle1->p4;
					//
					// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTau1Tau2HelrPVBS: " << product.m_recoPhiStarCPPolVecCombTau1Tau2HelrPVBS;
					// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTau1VisTau2HelrPVBS: " << product.m_recoPhiStarCPPolVecCombTau1VisTau2HelrPVBS;
					// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTau1Tau2VisHelrPVBS: " << product.m_recoPhiStarCPPolVecCombTau1Tau2VisHelrPVBS;
					// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTau1VisTau2VisHelrPVBS: " << product.m_recoPhiStarCPPolVecCombTau1VisTau2VisHelrPVBS;
					// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTau1Tau2PiSSFromRhoHelrPVBS: " << product.m_recoPhiStarCPPolVecCombTau1Tau2PiSSFromRhoHelrPVBS;
					// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTau1Tau2PiHighPtHelrPVBS: " << product.m_recoPhiStarCPPolVecCombTau1Tau2PiHighPtHelrPVBS;
					// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTau1VisTau2PiSSFromRhoHelrPVBS: " << product.m_recoPhiStarCPPolVecCombTau1VisTau2PiSSFromRhoHelrPVBS;
					// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTau1VisTau2PiHighPtHelrPVBS: " << product.m_recoPhiStarCPPolVecCombTau1VisTau2PiHighPtHelrPVBS;
				}
			}
			else if (product.m_decayChannel == HttEnumTypes::DecayChannel::TT)
			{
				// RMFLV::BetaVector polVec1 = product.m_polarimetricVectorsSimpleFit[product.m_flavourOrderedLeptons.at(0)];
				// RMFLV::BetaVector polVec2 = product.m_polarimetricVectorsSimpleFit[product.m_flavourOrderedLeptons.at(1)];

				RMFLV IPLVHelrPVBS_1;
				IPLVHelrPVBS_1.SetXYZT(product.m_recoIPHelrPVBS_1.X(), product.m_recoIPHelrPVBS_1.Y(), product.m_recoIPHelrPVBS_1.Z(), 0);
				RMFLV IPLVHelrPVBS_2;
				IPLVHelrPVBS_2.SetXYZT(product.m_recoIPHelrPVBS_2.X(), product.m_recoIPHelrPVBS_2.Y(), product.m_recoIPHelrPVBS_2.Z(), 0);

				if (dmMva_1 == 10 && dmMva_2 == 0)
				{
					// TODO Fix ordering. It's mixed up for these cases. Also check other decaymode variant
					bool firstNegative = product.m_flavourOrderedLeptons.at(0)->charge() < 0;
					if(product.m_polarimetricVectorsTau1Tau2SimpleFit.size() > 0)
					{
						RMFLV::BetaVector polVecTau1Tau2_1 = product.m_polarimetricVectorsTau1Tau2SimpleFit[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1Tau2_2 = product.m_polarimetricVectorsTau1Tau2SimpleFit[product.m_flavourOrderedLeptons.at(1)];
						product.m_recoPhiStarCPPolVecTau1Tau2HelrPVBS = cpq.CalculatePhiStarCPPolVec(simpleFitTau1, simpleFitTau2, polVecTau1Tau2_1, polVecTau1Tau2_2, firstNegative);
						product.m_recoPhiStarCPPolVecCombTau1Tau2HelrPVBS = cpq.CalculatePhiStarCPPolVecComb(simpleFitTau1, simpleFitTau2, polVecTau1Tau2_1, IPLVHelrPVBS_2, firstNegative);
					}
					if(product.m_polarimetricVectorsTau1VisTau2SimpleFit.size() > 0)
					{
						RMFLV::BetaVector polVecTau1VisTau2_1 = product.m_polarimetricVectorsTau1VisTau2SimpleFit[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1VisTau2_2 = product.m_polarimetricVectorsTau1VisTau2SimpleFit[product.m_flavourOrderedLeptons.at(1)];
						product.m_recoPhiStarCPPolVecTau1VisTau2HelrPVBS = cpq.CalculatePhiStarCPPolVec(simpleFitTau1, product.m_flavourOrderedLeptons.at(1)->p4, polVecTau1VisTau2_1, polVecTau1VisTau2_2, firstNegative);
						product.m_recoPhiStarCPPolVecCombTau1VisTau2HelrPVBS = cpq.CalculatePhiStarCPPolVecComb(simpleFitTau1, product.m_flavourOrderedLeptons.at(1)->p4, polVecTau1VisTau2_1, IPLVHelrPVBS_2, firstNegative);
					}
					if(product.m_polarimetricVectorsTau1Tau2VisSimpleFit.size() > 0)
					{
						RMFLV::BetaVector polVecTau1Tau2Vis_1 = product.m_polarimetricVectorsTau1Tau2VisSimpleFit[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1Tau2Vis_2 = product.m_polarimetricVectorsTau1Tau2VisSimpleFit[product.m_flavourOrderedLeptons.at(1)];
						product.m_recoPhiStarCPPolVecTau1Tau2VisHelrPVBS = cpq.CalculatePhiStarCPPolVec(product.m_flavourOrderedLeptons.at(0)->p4, simpleFitTau2, polVecTau1Tau2Vis_1, polVecTau1Tau2Vis_2, firstNegative);
						product.m_recoPhiStarCPPolVecCombTau1Tau2VisHelrPVBS = cpq.CalculatePhiStarCPPolVecComb(product.m_flavourOrderedLeptons.at(0)->p4, simpleFitTau2, polVecTau1Tau2Vis_1, IPLVHelrPVBS_2, firstNegative);
					}
					if(product.m_polarimetricVectorsTau1VisTau2VisSimpleFit.size() > 0)
					{
						RMFLV::BetaVector polVecTau1VisTau2Vis_1 = product.m_polarimetricVectorsTau1VisTau2VisSimpleFit[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1VisTau2Vis_2 = product.m_polarimetricVectorsTau1VisTau2VisSimpleFit[product.m_flavourOrderedLeptons.at(1)];
						product.m_recoPhiStarCPPolVecTau1VisTau2VisHelrPVBS = cpq.CalculatePhiStarCPPolVec(product.m_flavourOrderedLeptons.at(0)->p4, product.m_flavourOrderedLeptons.at(1)->p4, polVecTau1VisTau2Vis_1, polVecTau1VisTau2Vis_2, firstNegative);
						product.m_recoPhiStarCPPolVecCombTau1VisTau2VisHelrPVBS = cpq.CalculatePhiStarCPPolVecComb(product.m_flavourOrderedLeptons.at(0)->p4, product.m_flavourOrderedLeptons.at(1)->p4, polVecTau1VisTau2Vis_1, IPLVHelrPVBS_2, firstNegative);
					}
					if(product.m_polarimetricVectorsTau1Tau2PiSSFromRhoSimpleFit.size() > 0)
					{
						RMFLV::BetaVector polVecTau1Tau2PiSSFromRho_1 = product.m_polarimetricVectorsTau1Tau2PiSSFromRhoSimpleFit[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1Tau2PiSSFromRho_2 = product.m_polarimetricVectorsTau1Tau2PiSSFromRhoSimpleFit[product.m_flavourOrderedLeptons.at(1)];
						product.m_recoPhiStarCPPolVecTau1Tau2PiSSFromRhoHelrPVBS = cpq.CalculatePhiStarCPPolVec(piSSFromRho1, simpleFitTau2, polVecTau1Tau2PiSSFromRho_1, polVecTau1Tau2PiSSFromRho_2, firstNegative);
						product.m_recoPhiStarCPPolVecCombTau1Tau2PiSSFromRhoHelrPVBS = cpq.CalculatePhiStarCPPolVecComb(piSSFromRho1, simpleFitTau2, polVecTau1Tau2PiSSFromRho_1, IPLVHelrPVBS_2, firstNegative);
					}
					if(product.m_polarimetricVectorsTau1Tau2PiHighPtSimpleFit.size() > 0)
					{
						RMFLV::BetaVector polVecTau1Tau2PiHighPt_1 = product.m_polarimetricVectorsTau1Tau2PiHighPtSimpleFit[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1Tau2PiHighPt_2 = product.m_polarimetricVectorsTau1Tau2PiHighPtSimpleFit[product.m_flavourOrderedLeptons.at(1)];
						product.m_recoPhiStarCPPolVecTau1Tau2PiHighPtHelrPVBS = cpq.CalculatePhiStarCPPolVec(piSSHighPt1, simpleFitTau2, polVecTau1Tau2PiHighPt_1, polVecTau1Tau2PiHighPt_2, firstNegative);
						product.m_recoPhiStarCPPolVecCombTau1Tau2PiHighPtHelrPVBS = cpq.CalculatePhiStarCPPolVecComb(piSSHighPt1, simpleFitTau2, polVecTau1Tau2PiHighPt_1, IPLVHelrPVBS_2, firstNegative);
					}
					if(product.m_polarimetricVectorsTau1VisTau2PiSSFromRhoSimpleFit.size() > 0)
					{
						RMFLV::BetaVector polVecTau1VisTau2PiSSFromRho_1 = product.m_polarimetricVectorsTau1VisTau2PiSSFromRhoSimpleFit[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1VisTau2PiSSFromRho_2 = product.m_polarimetricVectorsTau1VisTau2PiSSFromRhoSimpleFit[product.m_flavourOrderedLeptons.at(1)];
						product.m_recoPhiStarCPPolVecTau1VisTau2PiSSFromRhoHelrPVBS = cpq.CalculatePhiStarCPPolVec(piSSFromRho1, product.m_flavourOrderedLeptons.at(1)->p4, polVecTau1VisTau2PiSSFromRho_1, polVecTau1VisTau2PiSSFromRho_2, firstNegative);
						product.m_recoPhiStarCPPolVecCombTau1VisTau2PiSSFromRhoHelrPVBS = cpq.CalculatePhiStarCPPolVecComb(piSSFromRho1, product.m_flavourOrderedLeptons.at(1)->p4, polVecTau1VisTau2PiSSFromRho_1, IPLVHelrPVBS_2, firstNegative);
					}
					if(product.m_polarimetricVectorsTau1VisTau2PiHighPtSimpleFit.size() > 0)
					{
						RMFLV::BetaVector polVecTau1VisTau2PiHighPt_1 = product.m_polarimetricVectorsTau1VisTau2PiHighPtSimpleFit[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1VisTau2PiHighPt_2 = product.m_polarimetricVectorsTau1VisTau2PiHighPtSimpleFit[product.m_flavourOrderedLeptons.at(1)];
						product.m_recoPhiStarCPPolVecTau1VisTau2PiHighPtHelrPVBS = cpq.CalculatePhiStarCPPolVec(piSSHighPt1, product.m_flavourOrderedLeptons.at(1)->p4, polVecTau1VisTau2PiHighPt_1, polVecTau1VisTau2PiHighPt_2, firstNegative);
						product.m_recoPhiStarCPPolVecCombTau1VisTau2PiHighPtHelrPVBS = cpq.CalculatePhiStarCPPolVecComb(piSSHighPt1, product.m_flavourOrderedLeptons.at(1)->p4, polVecTau1VisTau2PiHighPt_1, IPLVHelrPVBS_2, firstNegative);
					}
				}
				if (dmMva_1 == 0 && dmMva_2 == 10)
				{
					bool firstNegative = product.m_flavourOrderedLeptons.at(1)->charge() < 0;
					if(product.m_polarimetricVectorsTau1Tau2SimpleFit.size() > 0)
					{
						RMFLV::BetaVector polVecTau1Tau2_1 = product.m_polarimetricVectorsTau1Tau2SimpleFit[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1Tau2_2 = product.m_polarimetricVectorsTau1Tau2SimpleFit[product.m_flavourOrderedLeptons.at(1)];
						product.m_recoPhiStarCPPolVecTau1Tau2HelrPVBS = cpq.CalculatePhiStarCPPolVec(simpleFitTau2, simpleFitTau1, polVecTau1Tau2_2, polVecTau1Tau2_1, firstNegative);
						product.m_recoPhiStarCPPolVecCombTau1Tau2HelrPVBS = cpq.CalculatePhiStarCPPolVecComb(simpleFitTau2, simpleFitTau1, polVecTau1Tau2_2, IPLVHelrPVBS_1, firstNegative);
					}
					if(product.m_polarimetricVectorsTau1VisTau2SimpleFit.size() > 0)
					{
						RMFLV::BetaVector polVecTau1VisTau2_1 = product.m_polarimetricVectorsTau1VisTau2SimpleFit[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1VisTau2_2 = product.m_polarimetricVectorsTau1VisTau2SimpleFit[product.m_flavourOrderedLeptons.at(1)];
						product.m_recoPhiStarCPPolVecTau1VisTau2HelrPVBS = cpq.CalculatePhiStarCPPolVec(simpleFitTau2, product.m_flavourOrderedLeptons.at(0)->p4, polVecTau1VisTau2_2, polVecTau1VisTau2_1, firstNegative);
						product.m_recoPhiStarCPPolVecCombTau1VisTau2HelrPVBS = cpq.CalculatePhiStarCPPolVecComb(simpleFitTau2, product.m_flavourOrderedLeptons.at(0)->p4, polVecTau1VisTau2_2, IPLVHelrPVBS_1, firstNegative);
					}
					if(product.m_polarimetricVectorsTau1Tau2VisSimpleFit.size() > 0)
					{
						RMFLV::BetaVector polVecTau1Tau2Vis_1 = product.m_polarimetricVectorsTau1Tau2VisSimpleFit[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1Tau2Vis_2 = product.m_polarimetricVectorsTau1Tau2VisSimpleFit[product.m_flavourOrderedLeptons.at(1)];
						product.m_recoPhiStarCPPolVecTau1Tau2VisHelrPVBS = cpq.CalculatePhiStarCPPolVec(product.m_flavourOrderedLeptons.at(1)->p4, simpleFitTau1, polVecTau1Tau2Vis_2, polVecTau1Tau2Vis_1, firstNegative);
						product.m_recoPhiStarCPPolVecCombTau1Tau2VisHelrPVBS = cpq.CalculatePhiStarCPPolVecComb(product.m_flavourOrderedLeptons.at(1)->p4, simpleFitTau1, polVecTau1Tau2Vis_2, IPLVHelrPVBS_1, firstNegative);
					}
					if(product.m_polarimetricVectorsTau1VisTau2VisSimpleFit.size() > 0)
					{
						RMFLV::BetaVector polVecTau1VisTau2Vis_1 = product.m_polarimetricVectorsTau1VisTau2VisSimpleFit[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1VisTau2Vis_2 = product.m_polarimetricVectorsTau1VisTau2VisSimpleFit[product.m_flavourOrderedLeptons.at(1)];
						product.m_recoPhiStarCPPolVecTau1VisTau2VisHelrPVBS = cpq.CalculatePhiStarCPPolVec(product.m_flavourOrderedLeptons.at(1)->p4, product.m_flavourOrderedLeptons.at(0)->p4, polVecTau1VisTau2Vis_2, polVecTau1VisTau2Vis_1, firstNegative);
						product.m_recoPhiStarCPPolVecCombTau1VisTau2VisHelrPVBS = cpq.CalculatePhiStarCPPolVecComb(product.m_flavourOrderedLeptons.at(1)->p4, product.m_flavourOrderedLeptons.at(0)->p4, polVecTau1VisTau2Vis_2, IPLVHelrPVBS_1, firstNegative);
					}
					if(product.m_polarimetricVectorsTau1Tau2PiSSFromRhoSimpleFit.size() > 0)
					{
						RMFLV::BetaVector polVecTau1Tau2PiSSFromRho_1 = product.m_polarimetricVectorsTau1Tau2PiSSFromRhoSimpleFit[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1Tau2PiSSFromRho_2 = product.m_polarimetricVectorsTau1Tau2PiSSFromRhoSimpleFit[product.m_flavourOrderedLeptons.at(1)];
						product.m_recoPhiStarCPPolVecTau1Tau2PiSSFromRhoHelrPVBS = cpq.CalculatePhiStarCPPolVec(piSSFromRho2, simpleFitTau1, polVecTau1Tau2PiSSFromRho_2, polVecTau1Tau2PiSSFromRho_1, firstNegative);
						product.m_recoPhiStarCPPolVecCombTau1Tau2PiSSFromRhoHelrPVBS = cpq.CalculatePhiStarCPPolVecComb(piSSFromRho2, simpleFitTau1, polVecTau1Tau2PiSSFromRho_2, IPLVHelrPVBS_1, firstNegative);
					}
					if(product.m_polarimetricVectorsTau1Tau2PiHighPtSimpleFit.size() > 0)
					{
						RMFLV::BetaVector polVecTau1Tau2PiHighPt_1 = product.m_polarimetricVectorsTau1Tau2PiHighPtSimpleFit[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1Tau2PiHighPt_2 = product.m_polarimetricVectorsTau1Tau2PiHighPtSimpleFit[product.m_flavourOrderedLeptons.at(1)];
						product.m_recoPhiStarCPPolVecTau1Tau2PiHighPtHelrPVBS = cpq.CalculatePhiStarCPPolVec(piSSHighPt2, simpleFitTau1, polVecTau1Tau2PiHighPt_2, polVecTau1Tau2PiHighPt_1, firstNegative);
						product.m_recoPhiStarCPPolVecCombTau1Tau2PiHighPtHelrPVBS = cpq.CalculatePhiStarCPPolVecComb(piSSHighPt2, simpleFitTau1, polVecTau1Tau2PiHighPt_2, IPLVHelrPVBS_1, firstNegative);
					}
					if(product.m_polarimetricVectorsTau1VisTau2PiSSFromRhoSimpleFit.size() > 0)
					{
						RMFLV::BetaVector polVecTau1VisTau2PiSSFromRho_1 = product.m_polarimetricVectorsTau1VisTau2PiSSFromRhoSimpleFit[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1VisTau2PiSSFromRho_2 = product.m_polarimetricVectorsTau1VisTau2PiSSFromRhoSimpleFit[product.m_flavourOrderedLeptons.at(1)];
						product.m_recoPhiStarCPPolVecTau1VisTau2PiSSFromRhoHelrPVBS = cpq.CalculatePhiStarCPPolVec(piSSFromRho2, product.m_flavourOrderedLeptons.at(0)->p4, polVecTau1VisTau2PiSSFromRho_2, polVecTau1VisTau2PiSSFromRho_1, firstNegative);
						product.m_recoPhiStarCPPolVecCombTau1VisTau2PiSSFromRhoHelrPVBS = cpq.CalculatePhiStarCPPolVecComb(piSSFromRho2, product.m_flavourOrderedLeptons.at(0)->p4, polVecTau1VisTau2PiSSFromRho_2, IPLVHelrPVBS_1, firstNegative);
					}
					if(product.m_polarimetricVectorsTau1VisTau2PiHighPtSimpleFit.size() > 0)
					{
						RMFLV::BetaVector polVecTau1VisTau2PiHighPt_1 = product.m_polarimetricVectorsTau1VisTau2PiHighPtSimpleFit[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1VisTau2PiHighPt_2 = product.m_polarimetricVectorsTau1VisTau2PiHighPtSimpleFit[product.m_flavourOrderedLeptons.at(1)];
						product.m_recoPhiStarCPPolVecTau1VisTau2PiHighPtHelrPVBS = cpq.CalculatePhiStarCPPolVec(piSSHighPt2, product.m_flavourOrderedLeptons.at(0)->p4, polVecTau1VisTau2PiHighPt_2, polVecTau1VisTau2PiHighPt_1, firstNegative);
						product.m_recoPhiStarCPPolVecCombTau1VisTau2PiHighPtHelrPVBS = cpq.CalculatePhiStarCPPolVecComb(piSSHighPt2, product.m_flavourOrderedLeptons.at(0)->p4, polVecTau1VisTau2PiHighPt_2, IPLVHelrPVBS_1, firstNegative);
					}
				}
				// LOG(INFO) << "---------------RECO BLOCK START---------------";
				// LOG(INFO) << "RecoTauCPProducer simpleFitTau1: " << simpleFitTau1;
				// LOG(INFO) << "RecoTauCPProducer simpleFitTau2: " << simpleFitTau2;
				// LOG(INFO) << "RecoTauCPProducer dmMva_1: " << dmMva_1;
				// LOG(INFO) << "RecoTauCPProducer dmMva_2: " << dmMva_2;
				// // LOG(INFO) << "RecoTauCPProducer polVec1: " << polVec1;
				// // LOG(INFO) << "RecoTauCPProducer polVec2: " << polVec2;
				// LOG(INFO) << "RecoTauCPProducer IPLVHelrPVBS_1: " << IPLVHelrPVBS_1;
				// LOG(INFO) << "RecoTauCPProducer IPLVHelrPVBS_2: " << IPLVHelrPVBS_2;
				// LOG(INFO) << "RecoTauCPProducer piSSFromRho1: " << piSSFromRho1;
				// LOG(INFO) << "RecoTauCPProducer piSSFromRho2: " << piSSFromRho2;
				// LOG(INFO) << "RecoTauCPProducer recoParticle1->p4: " << recoParticle1->p4;
				// LOG(INFO) << "RecoTauCPProducer recoParticle2->p4: " << recoParticle2->p4;
				// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPCombMergedHelrPVBS: " << product.m_recoPhiStarCPCombMergedHelrPVBS;
				// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecTau1Tau2HelrPVBS: " << product.m_recoPhiStarCPPolVecTau1Tau2HelrPVBS;
				// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTau1Tau2HelrPVBS: " << product.m_recoPhiStarCPPolVecCombTau1Tau2HelrPVBS;
				// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecTau1VisTau2HelrPVBS: " << product.m_recoPhiStarCPPolVecTau1VisTau2HelrPVBS;
				// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTau1VisTau2HelrPVBS: " << product.m_recoPhiStarCPPolVecCombTau1VisTau2HelrPVBS;
				// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecTau1Tau2VisHelrPVBS: " << product.m_recoPhiStarCPPolVecTau1Tau2VisHelrPVBS;
				// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTau1Tau2VisHelrPVBS: " << product.m_recoPhiStarCPPolVecCombTau1Tau2VisHelrPVBS;
				// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecTau1VisTau2VisHelrPVBS: " << product.m_recoPhiStarCPPolVecTau1VisTau2VisHelrPVBS;
				// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTau1VisTau2VisHelrPVBS: " << product.m_recoPhiStarCPPolVecCombTau1VisTau2VisHelrPVBS;
				// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecTau1Tau2PiSSFromRhoHelrPVBS: " << product.m_recoPhiStarCPPolVecTau1Tau2PiSSFromRhoHelrPVBS;
				// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTau1Tau2PiSSFromRhoHelrPVBS: " << product.m_recoPhiStarCPPolVecCombTau1Tau2PiSSFromRhoHelrPVBS;
				// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecTau1Tau2PiHighPtHelrPVBS: " << product.m_recoPhiStarCPPolVecTau1Tau2PiHighPtHelrPVBS;
				// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTau1Tau2PiHighPtHelrPVBS: " << product.m_recoPhiStarCPPolVecCombTau1Tau2PiHighPtHelrPVBS;
				// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecTau1VisTau2PiSSFromRhoHelrPVBS: " << product.m_recoPhiStarCPPolVecTau1VisTau2PiSSFromRhoHelrPVBS;
				// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTau1VisTau2PiSSFromRhoHelrPVBS: " << product.m_recoPhiStarCPPolVecCombTau1VisTau2PiSSFromRhoHelrPVBS;
				// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecTau1VisTau2PiHighPtHelrPVBS: " << product.m_recoPhiStarCPPolVecTau1VisTau2PiHighPtHelrPVBS;
				// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTau1VisTau2PiHighPtHelrPVBS: " << product.m_recoPhiStarCPPolVecCombTau1VisTau2PiHighPtHelrPVBS;
				// LOG(INFO) << "---------------RECO BLOCK END---------------";
			}
			// first particle is always a1
			bool firstNegative = a1->charge() < 0;
			if(product.m_polarimetricVectorsTauOneProngTauA1SimpleFit.size() > 0)
			{
				RMFLV::BetaVector polVecA1 = product.m_polarimetricVectorsTauOneProngTauA1SimpleFit[a1];
				RMFLV::BetaVector polVecOneProng = product.m_polarimetricVectorsTauOneProngTauA1SimpleFit[oneProng];
				product.m_recoPhiStarCPPolVecTauOneProngTauA1 = cpq.CalculatePhiStarCPPolVec(simpleFitTauA1, simpleFitTauOneProng, polVecA1, polVecOneProng, firstNegative);
				product.m_recoPhiStarCPPolVecCombTauOneProngTauA1HelrPVBS = cpq.CalculatePhiStarCPPolVecComb(simpleFitTauA1, simpleFitTauOneProng, polVecA1, IPLVHelrPVBSOneProng, firstNegative);
			}
			if(product.m_polarimetricVectorsOneProngTauA1SimpleFit.size() > 0)
			{
				RMFLV::BetaVector polVecA1 = product.m_polarimetricVectorsOneProngTauA1SimpleFit[a1];
				RMFLV::BetaVector polVecOneProng = product.m_polarimetricVectorsOneProngTauA1SimpleFit[oneProng];
				product.m_recoPhiStarCPPolVecOneProngTauA1 = cpq.CalculatePhiStarCPPolVec(simpleFitTauA1, oneProng->p4, polVecA1, polVecOneProng, firstNegative);
				product.m_recoPhiStarCPPolVecCombOneProngTauA1HelrPVBS = cpq.CalculatePhiStarCPPolVecComb(simpleFitTauA1, oneProng->p4, polVecA1, IPLVHelrPVBSOneProng, firstNegative);
			}
			if(product.m_polarimetricVectorsTauOneProngA1SimpleFit.size() > 0)
			{
				RMFLV::BetaVector polVecA1 = product.m_polarimetricVectorsTauOneProngA1SimpleFit[a1];
				RMFLV::BetaVector polVecOneProng = product.m_polarimetricVectorsTauOneProngA1SimpleFit[oneProng];
				product.m_recoPhiStarCPPolVecTauOneProngA1 = cpq.CalculatePhiStarCPPolVec(a1->p4, simpleFitTauOneProng, polVecA1, polVecOneProng, firstNegative);
				product.m_recoPhiStarCPPolVecCombTauOneProngA1HelrPVBS = cpq.CalculatePhiStarCPPolVecComb(a1->p4, simpleFitTauOneProng, polVecA1, IPLVHelrPVBSOneProng, firstNegative);
			}
			if(product.m_polarimetricVectorsOneProngA1SimpleFit.size() > 0)
			{
				RMFLV::BetaVector polVecA1 = product.m_polarimetricVectorsOneProngA1SimpleFit[a1];
				RMFLV::BetaVector polVecOneProng = product.m_polarimetricVectorsOneProngA1SimpleFit[oneProng];
				product.m_recoPhiStarCPPolVecOneProngA1 = cpq.CalculatePhiStarCPPolVec(a1->p4, oneProng->p4, polVecA1, polVecOneProng, firstNegative);
				product.m_recoPhiStarCPPolVecCombOneProngA1HelrPVBS = cpq.CalculatePhiStarCPPolVecComb(a1->p4, oneProng->p4, polVecA1, IPLVHelrPVBSOneProng, firstNegative);
			}
			if(product.m_polarimetricVectorsTauOneProngA1PiSSFromRhoSimpleFit.size() > 0)
			{
				RMFLV::BetaVector polVecA1 = product.m_polarimetricVectorsTauOneProngA1PiSSFromRhoSimpleFit[a1];
				RMFLV::BetaVector polVecOneProng = product.m_polarimetricVectorsTauOneProngA1PiSSFromRhoSimpleFit[oneProng];
				product.m_recoPhiStarCPPolVecTauOneProngA1PiSSFromRho = cpq.CalculatePhiStarCPPolVec(A1PiSSFromRho, simpleFitTauOneProng, polVecA1, polVecOneProng, firstNegative);
				product.m_recoPhiStarCPPolVecCombTauOneProngA1PiSSFromRhoHelrPVBS = cpq.CalculatePhiStarCPPolVecComb(A1PiSSFromRho, simpleFitTauOneProng, polVecA1, IPLVHelrPVBSOneProng, firstNegative);
			}
			if(product.m_polarimetricVectorsTauOneProngA1PiHighPtSimpleFit.size() > 0)
			{
				RMFLV::BetaVector polVecA1 = product.m_polarimetricVectorsTauOneProngA1PiHighPtSimpleFit[a1];
				RMFLV::BetaVector polVecOneProng = product.m_polarimetricVectorsTauOneProngA1PiHighPtSimpleFit[oneProng];
				product.m_recoPhiStarCPPolVecTauOneProngA1PiHighPt = cpq.CalculatePhiStarCPPolVec(A1PiSSHighPt, simpleFitTauOneProng, polVecA1, polVecOneProng, firstNegative);
				product.m_recoPhiStarCPPolVecCombTauOneProngA1PiHighPtHelrPVBS = cpq.CalculatePhiStarCPPolVecComb(A1PiSSHighPt, simpleFitTauOneProng, polVecA1, IPLVHelrPVBSOneProng, firstNegative);
			}
			if(product.m_polarimetricVectorsOneProngA1PiSSFromRhoSimpleFit.size() > 0)
			{
				RMFLV::BetaVector polVecA1 = product.m_polarimetricVectorsOneProngA1PiSSFromRhoSimpleFit[a1];
				RMFLV::BetaVector polVecOneProng = product.m_polarimetricVectorsOneProngA1PiSSFromRhoSimpleFit[oneProng];
				product.m_recoPhiStarCPPolVecOneProngA1PiSSFromRho = cpq.CalculatePhiStarCPPolVec(A1PiSSFromRho, oneProng->p4, polVecA1, polVecOneProng, firstNegative);
				product.m_recoPhiStarCPPolVecCombOneProngA1PiSSFromRhoHelrPVBS = cpq.CalculatePhiStarCPPolVecComb(A1PiSSFromRho, oneProng->p4, polVecA1, IPLVHelrPVBSOneProng, firstNegative);
			}
			if(product.m_polarimetricVectorsOneProngA1PiHighPtSimpleFit.size() > 0)
			{
				RMFLV::BetaVector polVecA1 = product.m_polarimetricVectorsOneProngA1PiHighPtSimpleFit[a1];
				RMFLV::BetaVector polVecOneProng = product.m_polarimetricVectorsOneProngA1PiHighPtSimpleFit[oneProng];
				product.m_recoPhiStarCPPolVecOneProngA1PiHighPt = cpq.CalculatePhiStarCPPolVec(A1PiSSHighPt, oneProng->p4, polVecA1, polVecOneProng, firstNegative);
				product.m_recoPhiStarCPPolVecCombOneProngA1PiHighPtHelrPVBS = cpq.CalculatePhiStarCPPolVecComb(A1PiSSHighPt, oneProng->p4, polVecA1, IPLVHelrPVBSOneProng, firstNegative);
			}
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecTau1Tau2HelrPVBS: " << product.m_recoPhiStarCPPolVecTau1Tau2HelrPVBS;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecTau1VisTau2HelrPVBS: " << product.m_recoPhiStarCPPolVecTau1VisTau2HelrPVBS;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecTau1Tau2VisHelrPVBS: " << product.m_recoPhiStarCPPolVecTau1Tau2VisHelrPVBS;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecTau1VisTau2VisHelrPVBS: " << product.m_recoPhiStarCPPolVecTau1VisTau2VisHelrPVBS;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecTau1Tau2PiSSFromRhoHelrPVBS: " << product.m_recoPhiStarCPPolVecTau1Tau2PiSSFromRhoHelrPVBS;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecTau1Tau2PiHighPtHelrPVBS: " << product.m_recoPhiStarCPPolVecTau1Tau2PiHighPtHelrPVBS;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecTau1VisTau2PiSSFromRhoHelrPVBS: " << product.m_recoPhiStarCPPolVecTau1VisTau2PiSSFromRhoHelrPVBS;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecTau1VisTau2PiHighPtHelrPVBS: " << product.m_recoPhiStarCPPolVecTau1VisTau2PiHighPtHelrPVBS;
			//
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecTauOneProngTauA1: " << product.m_recoPhiStarCPPolVecTauOneProngTauA1;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecOneProngTauA1: " << product.m_recoPhiStarCPPolVecOneProngTauA1;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecTauOneProngA1: " << product.m_recoPhiStarCPPolVecTauOneProngA1;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecOneProngA1: " << product.m_recoPhiStarCPPolVecOneProngA1;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecTauOneProngA1PiSSFromRho: " << product.m_recoPhiStarCPPolVecTauOneProngA1PiSSFromRho;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecTauOneProngA1PiHighPt: " << product.m_recoPhiStarCPPolVecTauOneProngA1PiHighPt;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecOneProngA1PiSSFromRho: " << product.m_recoPhiStarCPPolVecOneProngA1PiSSFromRho;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecOneProngA1PiHighPt: " << product.m_recoPhiStarCPPolVecOneProngA1PiHighPt;
			//
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTau1Tau2HelrPVBS: " << product.m_recoPhiStarCPPolVecCombTau1Tau2HelrPVBS;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTau1VisTau2HelrPVBS: " << product.m_recoPhiStarCPPolVecCombTau1VisTau2HelrPVBS;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTau1Tau2VisHelrPVBS: " << product.m_recoPhiStarCPPolVecCombTau1Tau2VisHelrPVBS;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTau1VisTau2VisHelrPVBS: " << product.m_recoPhiStarCPPolVecCombTau1VisTau2VisHelrPVBS;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTau1Tau2PiSSFromRhoHelrPVBS: " << product.m_recoPhiStarCPPolVecCombTau1Tau2PiSSFromRhoHelrPVBS;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTau1Tau2PiHighPtHelrPVBS: " << product.m_recoPhiStarCPPolVecCombTau1Tau2PiHighPtHelrPVBS;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTau1VisTau2PiSSFromRhoHelrPVBS: " << product.m_recoPhiStarCPPolVecCombTau1VisTau2PiSSFromRhoHelrPVBS;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTau1VisTau2PiHighPtHelrPVBS: " << product.m_recoPhiStarCPPolVecCombTau1VisTau2PiHighPtHelrPVBS;
			//
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTauOneProngTauA1HelrPVBS: " << product.m_recoPhiStarCPPolVecCombTauOneProngTauA1HelrPVBS;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombOneProngTauA1HelrPVBS: " << product.m_recoPhiStarCPPolVecCombOneProngTauA1HelrPVBS;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTauOneProngA1HelrPVBS: " << product.m_recoPhiStarCPPolVecCombTauOneProngA1HelrPVBS;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombOneProngA1HelrPVBS: " << product.m_recoPhiStarCPPolVecCombOneProngA1HelrPVBS;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTauOneProngA1PiSSFromRhoHelrPVBS: " << product.m_recoPhiStarCPPolVecCombTauOneProngA1PiSSFromRhoHelrPVBS;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombTauOneProngA1PiHighPtHelrPVBS: " << product.m_recoPhiStarCPPolVecCombTauOneProngA1PiHighPtHelrPVBS;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombOneProngA1PiSSFromRhoHelrPVBS: " << product.m_recoPhiStarCPPolVecCombOneProngA1PiSSFromRhoHelrPVBS;
			// LOG(INFO) << "RecoTauCPProducer product.m_recoPhiStarCPPolVecCombOneProngA1PiHighPtHelrPVBS: " << product.m_recoPhiStarCPPolVecCombOneProngA1PiHighPtHelrPVBS;
		}
	}
}

/* piZero 4-momentum defined by direction (eta,phi) of the leading (in Pt)
   gamma, energy equal to sum of energy of all gammas and pi0 mass */
RMFLV RecoTauCPProducer::alternativePiZeroMomentum(const KTau* tau) const {

  RMFLV piZeroP4;
  float sumE = 0;
  float maxPt = 0;
  for (std::vector<KPFCandidate>::const_iterator candidate = tau->gammaCandidates.begin();
       candidate != tau->gammaCandidates.end(); ++candidate) {
    sumE += candidate->p4.energy();
    if (candidate->p4.pt()>maxPt) {
      maxPt = candidate->p4.pt();
      piZeroP4 = candidate->p4;
    }
  }
  float p2 = sumE*sumE - DefaultValues::NeutralPionMass*DefaultValues::NeutralPionMass;
  float p = p2>0 ? sqrt(p2) : sumE;
  float pt = p * sin(piZeroP4.theta());
  piZeroP4.SetPt(pt);
  piZeroP4.SetM(DefaultValues::NeutralPionMass);

  return piZeroP4;
}

/* 4-momenta of charged pions from a1 decay in 3-prongs tau decay */
bool RecoTauCPProducer::pionsFromRho3Prongs(const KTau* tau,
					    RMFLV& piSSFromRhoMomentum,
					    RMFLV& piOSMomentum,
					    RMFLV& piSSHighMomentum) const {

  //Reset 4-momenta
  piSSFromRhoMomentum.SetCoordinates(0,0,0,0);
  piOSMomentum.SetCoordinates(0,0,0,0);
  piSSHighMomentum.SetCoordinates(0,0,0,0);

  //Not 3-prongs tau
  if (tau->chargedHadronCandidates.size()!=3) return false;

  //Look for charged pion with charge opposite to tau
  for (std::vector<KPFCandidate>::const_iterator candidate = tau->chargedHadronCandidates.begin();
       candidate != tau->chargedHadronCandidates.end(); ++candidate) {
    if (candidate->charge()*tau->charge()<0) {
      piOSMomentum = candidate->p4;
      break;
    }
  }

  //Look for charged pions pair from rho decay
  float minDeltaM = 1e+10;
  float highestPt = 0;
  for (std::vector<KPFCandidate>::const_iterator candidate = tau->chargedHadronCandidates.begin();
       candidate != tau->chargedHadronCandidates.end(); ++candidate) {
    if (candidate->charge()*tau->charge()>0) {
      float deltaM = std::abs((candidate->p4+piOSMomentum).M()-DefaultValues::RhoMass);
      if (deltaM < minDeltaM) {
        piSSFromRhoMomentum = candidate->p4;
        minDeltaM = deltaM;
      }
      if (candidate->p4.pt() > highestPt)
      {
        highestPt = candidate->p4.pt();
        piSSHighMomentum = candidate->p4;
      }
    }
  }

  return (piOSMomentum.pt() > 0 && piSSFromRhoMomentum.pt() > 0 && piSSHighMomentum.pt() > 0); //Sanity check
}

std::vector<TLorentzVector> RecoTauCPProducer::GetInputLepton(product_type& product, KLepton* lepton, bool genMatched) const
{
	std::vector<TLorentzVector> input;

	if (genMatched)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, lepton, static_cast<KGenTau*>(nullptr));
		if (genTau)
		{
			RMFLV* genTauVisibleLV = &(genTau->visible.p4);

			input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genTau->p4));
			input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*genTauVisibleLV));
		}
	}
	else if (Utility::Contains(product.m_simpleFitTaus, lepton))
	{
		input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(SafeMap::Get(product.m_simpleFitTaus, lepton)));
		input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(lepton->p4));
	}

	return input;
}

std::vector<TLorentzVector> RecoTauCPProducer::GetInputPion(product_type& product, KLepton* lepton, bool genMatched) const
{
	std::vector<TLorentzVector> input;

	if (genMatched)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, lepton, static_cast<KGenTau*>(nullptr));
		if (genTau)
		{
			RMFLV* genTauVisibleLV = &(genTau->visible.p4);

			input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genTau->p4));
			input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*genTauVisibleLV));
		}
	}
	else if (Utility::Contains(product.m_simpleFitTaus, lepton))
	{
		input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(SafeMap::Get(product.m_simpleFitTaus, lepton)));
		input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(lepton->p4));
	}

	return input;
}

std::vector<TLorentzVector> RecoTauCPProducer::GetInputRho(product_type& product, KLepton* lepton, bool genMatched) const
{
	std::vector<TLorentzVector> input;

	if (genMatched)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, lepton, static_cast<KGenTau*>(nullptr));
		if (genTau)
		{
			KGenParticle* genParticle = SafeMap::GetWithDefault(product.m_validGenParticlesMap, genTau, static_cast<KGenParticle*>(nullptr));
			if (genParticle)
			{
				std::vector<KGenParticle*> genTauChargedHadrons = SafeMap::GetWithDefault(product.m_validGenTausChargedHadronsMap, genParticle, std::vector<KGenParticle*>());
				std::vector<KGenParticle*> genTauNeutralHadrons = SafeMap::GetWithDefault(product.m_validGenTausNeutralHadronsMap, genParticle, std::vector<KGenParticle*>());
				if ((genTau->nProngs == 1) && (genTau->nPi0s == 1) &&
				    (genTauChargedHadrons.size() == 1) && (genTauNeutralHadrons.size() == 1))
				{
					input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genTau->p4));

					input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genTauChargedHadrons.front()->p4));
					input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genTauNeutralHadrons.front()->p4));
					// LOG(INFO) << "\t\tRecoTauCPProducer genTauChargedHadrons.front(): " << genTauChargedHadrons.front()->pdgId << ", status = " << genTauChargedHadrons.front()->status() << ", p4 = " << genTauChargedHadrons.front()->p4;
					// LOG(INFO) << "\t\tRecoTauCPProducer genTauNeutralHadrons.front(): " << genTauNeutralHadrons.front()->pdgId << ", status = " << genTauNeutralHadrons.front()->status() << ", p4 = " << genTauNeutralHadrons.front()->p4;
				}
			}
		}
	}
	else if (Utility::Contains(product.m_simpleFitTaus, lepton))
	{
		input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(SafeMap::Get(product.m_simpleFitTaus, lepton)));

		KTau* tau = static_cast<KTau*>(lepton);
		input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(tau->sumChargedHadronCandidates()));
		input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(tau->piZeroMomentum()));
	}

	return input;
}

std::vector<TLorentzVector> RecoTauCPProducer::GetInputA1(product_type& product, KLepton* lepton, bool genMatched) const
{
	std::vector<TLorentzVector> input;

	if (genMatched)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, lepton, static_cast<KGenTau*>(nullptr));
		if (genTau)
		{
			KGenParticle* genParticle = SafeMap::GetWithDefault(product.m_validGenParticlesMap, genTau, static_cast<KGenParticle*>(nullptr));
			if (genParticle)
			{
				std::vector<KGenParticle*> genTauChargedHadrons = SafeMap::GetWithDefault(product.m_validGenTausChargedHadronsMap, genParticle, std::vector<KGenParticle*>());
				std::vector<KGenParticle*> genTauNeutralHadrons = SafeMap::GetWithDefault(product.m_validGenTausNeutralHadronsMap, genParticle, std::vector<KGenParticle*>());
				// if ((genTau->nProngs == 3) && (genTau->nPi0s == 0) &&
				    // (genTauChargedHadrons.size() == 3) && (genTauNeutralHadrons.size() == 0))
				if ((genTau->nProngs == 3) && (genTauChargedHadrons.size() == 3))
				{
					input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genTau->p4));

					// sort pions from a1 decay according to their charge
					RMFLV* piSingleChargeSign = nullptr;
					RMFLV* piDoubleChargeSign1 = nullptr;
					RMFLV* piDoubleChargeSign2 = nullptr;
					if ((genTauChargedHadrons.at(0)->charge() * genTauChargedHadrons.at(1)->charge()) > 0.0)
					{
						piSingleChargeSign = &(genTauChargedHadrons.at(2)->p4);
						piDoubleChargeSign1 = &(genTauChargedHadrons.at(0)->p4);
						piDoubleChargeSign2 = &(genTauChargedHadrons.at(1)->p4);
					}
					else if ((genTauChargedHadrons.at(0)->charge() * genTauChargedHadrons.at(2)->charge()) > 0.0)
					{
						piSingleChargeSign = &(genTauChargedHadrons.at(1)->p4);
						piDoubleChargeSign1 = &(genTauChargedHadrons.at(0)->p4);
						piDoubleChargeSign2 = &(genTauChargedHadrons.at(2)->p4);
					}
					else // if ((genTauChargedHadrons.at(1)->charge() * genTauChargedHadrons.at(2)->charge()) > 0.0)
					{
						piSingleChargeSign = &(genTauChargedHadrons.at(0)->p4);
						piDoubleChargeSign1 = &(genTauChargedHadrons.at(1)->p4);
						piDoubleChargeSign2 = &(genTauChargedHadrons.at(2)->p4);
					}
					// RMFLV rho1 = *piSingleChargeSign + *piDoubleChargeSign1;
					// RMFLV rho2 = *piSingleChargeSign + *piDoubleChargeSign2;
					// LOG(INFO) << "RecoTauCPProducer gen rhos:";
					// LOG(INFO) << "\tRecoTauCPProducer gen rho1: " << rho1.M();
					// LOG(INFO) << "\tRecoTauCPProducer gen rho2: " << rho2.M();
					// LOG(INFO) << "\t\tRecoTauCPProducer genTauChargedHadrons.at(0): " << genTauChargedHadrons.at(0)->pdgId << ", status = " << genTauChargedHadrons.at(0)->status() << ", p4 = " << genTauChargedHadrons.at(0)->p4;
					// LOG(INFO) << "\t\tRecoTauCPProducer genTauChargedHadrons.at(1): " << genTauChargedHadrons.at(1)->pdgId << ", status = " << genTauChargedHadrons.at(1)->status() << ", p4 = " << genTauChargedHadrons.at(1)->p4;
					// LOG(INFO) << "\t\tRecoTauCPProducer genTauChargedHadrons.at(2): " << genTauChargedHadrons.at(2)->pdgId << ", status = " << genTauChargedHadrons.at(2)->status() << ", p4 = " << genTauChargedHadrons.at(2)->p4;
					input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*piSingleChargeSign));
					input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*piDoubleChargeSign1));
					input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*piDoubleChargeSign2));
				}
			}
		}
	}
	else if (Utility::Contains(product.m_simpleFitTaus, lepton))
	{
		input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(SafeMap::Get(product.m_simpleFitTaus, lepton)));

		KTau* tau = static_cast<KTau*>(lepton);
		assert(tau->chargedHadronCandidates.size() > 2);

		// sort pions from a1 decay according to their charge
		RMFLV* piSingleChargeSign = nullptr;
		RMFLV* piDoubleChargeSign1 = nullptr;
		RMFLV* piDoubleChargeSign2 = nullptr;
		if ((tau->chargedHadronCandidates.at(0).charge() * tau->chargedHadronCandidates.at(1).charge()) > 0.0)
		{
			piSingleChargeSign = &(tau->chargedHadronCandidates.at(2).p4);
			piDoubleChargeSign1 = &(tau->chargedHadronCandidates.at(0).p4);
			piDoubleChargeSign2 = &(tau->chargedHadronCandidates.at(1).p4);
		}
		else if ((tau->chargedHadronCandidates.at(0).charge() * tau->chargedHadronCandidates.at(2).charge()) > 0.0)
		{
			piSingleChargeSign = &(tau->chargedHadronCandidates.at(1).p4);
			piDoubleChargeSign1 = &(tau->chargedHadronCandidates.at(0).p4);
			piDoubleChargeSign2 = &(tau->chargedHadronCandidates.at(2).p4);
		}
		else // if ((tau->chargedHadronCandidates.at(1).charge() * tau->chargedHadronCandidates.at(2).charge()) > 0.0)
		{
			piSingleChargeSign = &(tau->chargedHadronCandidates.at(0).p4);
			piDoubleChargeSign1 = &(tau->chargedHadronCandidates.at(1).p4);
			piDoubleChargeSign2 = &(tau->chargedHadronCandidates.at(2).p4);
		}

		input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*piSingleChargeSign));
		input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*piDoubleChargeSign1));
		input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*piDoubleChargeSign2));
	}

	return input;
}
