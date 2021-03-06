
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"
#include "Artus/Utility/interface/UnitConverter.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/CPQuantities.h"
#include "HiggsCPinTauDecays/ImpactParameter/interface/ImpactParameter.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/RecoTauCPProducer.h"

#include <fstream>

std::string RecoTauCPProducer::GetProducerId() const
{
	return "RecoTauCPProducer";
}

void RecoTauCPProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	m_isData = settings.GetInputIsData();
	m_useAltPiZero = true;//FIXME: add a new setting?

	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "nominalPV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return event.m_vertexSummary->pv.position;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "nominalPVchi2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return event.m_vertexSummary->pv.chi2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "nominalPVnDOF", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return event.m_vertexSummary->pv.nDOF;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "nominalPVnTracks", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return event.m_vertexSummary->pv.nTracks;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "nominalPVsigmaxx", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return event.m_vertexSummary->pv.covariance.At(0,0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "nominalPVsigmayy", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return event.m_vertexSummary->pv.covariance.At(1,1);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "nominalPVsigmazz", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return event.m_vertexSummary->pv.covariance.At(2,2);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "nominalPVsigmaxy", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return event.m_vertexSummary->pv.covariance.At(0,1);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "nominalPVsigmaxz", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return event.m_vertexSummary->pv.covariance.At(0,2);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "nominalPVsigmayz", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return event.m_vertexSummary->pv.covariance.At(1,2);
	});

	// BS coordinates and parameters
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "theBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return event.m_beamSpot->position;
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "theBSatRef1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return event.m_beamSpot->Position(product.m_RefHelix_1.Z());
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "theBSatRef2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return event.m_beamSpot->Position(product.m_RefHelix_2.Z());
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "theBSatnominalPV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return event.m_beamSpot->Position(event.m_vertexSummary->pv.position.Z());
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "theBSsigmax", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return event.m_beamSpot->beamWidthX;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "theBSsigmay", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return event.m_beamSpot->beamWidthY;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "theBSsigmaz", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return event.m_beamSpot->sigmaZ;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "theBSdxdz", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return event.m_beamSpot->dxdz;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "theBSdydz", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return event.m_beamSpot->dydz;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "dxy_BSatRef1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_flavourOrderedLeptons.at(0)->track.helixParameters(event.m_beamSpot->Position(product.m_RefHelix_1.Z()), 3);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "dxy_BSatRef2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_flavourOrderedLeptons.at(1)->track.helixParameters(event.m_beamSpot->Position(product.m_RefHelix_2.Z()), 3);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "dxy_BSatnominalPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_flavourOrderedLeptons.at(0)->track.helixParameters(event.m_beamSpot->Position(event.m_vertexSummary->pv.position.Z()), 3);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "dxy_BSatnominalPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_flavourOrderedLeptons.at(1)->track.helixParameters(event.m_beamSpot->Position(event.m_vertexSummary->pv.position.Z()), 3);
	});

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

	// Helix Paramters
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixRadius_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_Radius_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixRadius_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_Radius_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixQOverP_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_flavourOrderedLeptons.at(0) ? (product.m_flavourOrderedLeptons.at(0)->track.helixParameters(event.m_beamSpot, 0)) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixLambda_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_flavourOrderedLeptons.at(0) ? (product.m_flavourOrderedLeptons.at(0)->track.helixParameters(event.m_beamSpot, 1)) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixPhi_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_flavourOrderedLeptons.at(0) ? (product.m_flavourOrderedLeptons.at(0)->track.helixParameters(event.m_beamSpot, 2)) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixDxy_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_flavourOrderedLeptons.at(0) ? (product.m_flavourOrderedLeptons.at(0)->track.helixParameters(event.m_beamSpot, 3)) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixDsz_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_flavourOrderedLeptons.at(0) ? (product.m_flavourOrderedLeptons.at(0)->track.helixParameters(event.m_beamSpot, 4)) : DefaultValues::UndefinedDouble;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixQOverP_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_flavourOrderedLeptons.at(1) ? (product.m_flavourOrderedLeptons.at(1)->track.helixParameters(event.m_beamSpot, 0)) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixLambda_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_flavourOrderedLeptons.at(1) ? (product.m_flavourOrderedLeptons.at(1)->track.helixParameters(event.m_beamSpot, 1)) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixPhi_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_flavourOrderedLeptons.at(1) ? (product.m_flavourOrderedLeptons.at(1)->track.helixParameters(event.m_beamSpot, 2)) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixDxy_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_flavourOrderedLeptons.at(1) ? (product.m_flavourOrderedLeptons.at(1)->track.helixParameters(event.m_beamSpot, 3)) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixDsz_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_flavourOrderedLeptons.at(1) ? (product.m_flavourOrderedLeptons.at(1)->track.helixParameters(event.m_beamSpot, 4)) : DefaultValues::UndefinedDouble;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixRadius", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_HelixRadius;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoMagneticField", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoMagneticField;
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

	// impact parameters d0=dxy and dz
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "d0rPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_refitPV ? product.m_flavourOrderedLeptons.at(0)->track.getDxy(product.m_refitPV) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "d0rPVBS_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_refitPVBS ? product.m_flavourOrderedLeptons.at(0)->track.getDxy(product.m_refitPVBS) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "dZrPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_refitPV ? product.m_flavourOrderedLeptons.at(0)->track.getDz(product.m_refitPV) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "dZrPVBS_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_refitPVBS ? product.m_flavourOrderedLeptons.at(0)->track.getDz(product.m_refitPVBS) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "d0rPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_refitPV ? product.m_flavourOrderedLeptons.at(1)->track.getDxy(product.m_refitPV) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "d0rPVBS_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_refitPVBS ? product.m_flavourOrderedLeptons.at(1)->track.getDxy(product.m_refitPVBS) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "dZrPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_refitPV ? product.m_flavourOrderedLeptons.at(1)->track.getDz(product.m_refitPV) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "dZrPVBS_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_refitPVBS ? product.m_flavourOrderedLeptons.at(1)->track.getDz(product.m_refitPVBS) : DefaultValues::UndefinedDouble;
	});
//	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoImpactParameter1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
//	{
//		return product.m_recoIP1;
//	});
//	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoImpactParameter2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
//	{
//		return product.m_recoIP2;
//	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoTrackRefError1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoTrackRefError1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoTrackRefError2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_recoTrackRefError2;
	});

	// IP vectors wrt nominalPV
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "IP_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_recoIP1).x() != -999) ? RMPoint( (product.m_recoIP1).x(), (product.m_recoIP1).y(), (product.m_recoIP1).z() ) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "IP_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_recoIP2).x() != -999) ? RMPoint( (product.m_recoIP2).x(), (product.m_recoIP2).y(), (product.m_recoIP2).z() ) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificance_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_pca1DiffInSigma;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificance_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_pca2DiffInSigma;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIP_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_pca1proj;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIP_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_pca2proj;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPHel_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_errorIPHel_1;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPHel_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_errorIPHel_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPHel_Track_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_errorIPHel_Track_1;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPHel_Track_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_errorIPHel_Track_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPHel_PV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_errorIPHel_PV_1;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPHel_PV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_errorIPHel_PV_2;
	});

	// IP vectors wrt refitted PV
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "IPrPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPrPV_1) != nullptr) ? RMPoint( (product.m_recoIPrPV_1).x(), (product.m_recoIPrPV_1).y(), (product.m_recoIPrPV_1).z() ) : DefaultValues::UndefinedRMPoint;
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "IPrPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPrPV_2) != nullptr) ? RMPoint( (product.m_recoIPrPV_2).x(), (product.m_recoIPrPV_2).y(), (product.m_recoIPrPV_2).z() ) : DefaultValues::UndefinedRMPoint;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificancerPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_pca1DiffInSigmarPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificancerPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_pca2DiffInSigmarPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPHelrPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_errorIPHelrPV_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPHelrPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_errorIPHelrPV_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPHelrPV_Track_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_refitPV ? product.m_errorIPHelrPV_Track_1 : DefaultValues::UndefinedDouble;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPHelrPV_Track_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_refitPV ? product.m_errorIPHelrPV_Track_2 : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPHelrPV_PV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_refitPV ? product.m_errorIPHelrPV_PV_1 : DefaultValues::UndefinedDouble;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPHelrPV_PV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_refitPV ? product.m_errorIPHelrPV_PV_2 : DefaultValues::UndefinedDouble;
	});



	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificancerPVBS_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_pca1DiffInSigmarPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificancerPVBS_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_pca2DiffInSigmarPVBS;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPrPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_pca1projrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPrPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_pca2projrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPrPVBS_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_pca1projrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPrPVBS_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_pca2projrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPHelrPVBS_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_errorIPHelrPVBS_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPHelrPVBS_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_errorIPHelrPVBS_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPHelrPVBS_Track_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_refitPV ? product.m_errorIPHelrPVBS_Track_1 : DefaultValues::UndefinedDouble;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPHelrPVBS_Track_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_refitPV ? product.m_errorIPHelrPVBS_Track_2 : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPHelrPVBS_PV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_refitPV ? product.m_errorIPHelrPVBS_PV_1 : DefaultValues::UndefinedDouble;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPHelrPVBS_PV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_refitPV ? product.m_errorIPHelrPVBS_PV_2 : DefaultValues::UndefinedDouble;
	});

	// IP vectors wrt refitted PV with BS constraint
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "IPrPVBS_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_recoIPrPVBS_1).x() != -999) ? RMPoint( (product.m_recoIPrPVBS_1).x(), (product.m_recoIPrPVBS_1).y(), (product.m_recoIPrPVBS_1).z() ) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "IPrPVBS_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_recoIPrPVBS_2).x() != -999) ? RMPoint( (product.m_recoIPrPVBS_2).x(), (product.m_recoIPrPVBS_2).y(), (product.m_recoIPrPVBS_2).z() ) : DefaultValues::UndefinedRMPoint);
	});
	// IP vectors wrt nominalPV with helical approach
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "IPHel_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_recoIPHel_1).x() != -999) ? RMPoint( (product.m_recoIPHel_1).x(), (product.m_recoIPHel_1).y(), (product.m_recoIPHel_1).z() ) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "IPHel_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_recoIPHel_2).x() != -999) ? RMPoint( (product.m_recoIPHel_2).x(), (product.m_recoIPHel_2).y(), (product.m_recoIPHel_2).z() ) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificanceHel_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_IPSignificanceHel_1!= nullptr) ? product.m_IPSignificanceHel_1 : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificanceHel_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_IPSignificanceHel_2!= nullptr) ? product.m_IPSignificanceHel_2 : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificanceHel_Track_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_IPSignificanceHel_Track_1!= nullptr) ? product.m_IPSignificanceHel_Track_1 : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificanceHel_Track_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_IPSignificanceHel_Track_2!= nullptr) ? product.m_IPSignificanceHel_Track_2 : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificanceHel_PV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_IPSignificanceHel_PV_1!= nullptr) ? product.m_IPSignificanceHel_PV_1 : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificanceHel_PV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_IPSignificanceHel_PV_2!= nullptr) ? product.m_IPSignificanceHel_PV_2 : DefaultValues::UndefinedFloat);
	});
	//The elements of the covariance matrix from the IP with helical approach
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelCovxx_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPHelCovxx_1 != nullptr) ? (product.m_recoIPHelCovxx_1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelCovxy_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPHelCovxy_1 != nullptr) ? (product.m_recoIPHelCovxy_1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelCovxz_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPHelCovxz_1 != nullptr) ? (product.m_recoIPHelCovxz_1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelCovyy_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPHelCovyy_1 != nullptr) ? (product.m_recoIPHelCovyy_1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelCovyz_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPHelCovyz_1 != nullptr) ? (product.m_recoIPHelCovyz_1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelCovzz_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPHelCovzz_1 != nullptr) ? (product.m_recoIPHelCovzz_1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelCovxx_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPHelCovxx_2 != nullptr) ? (product.m_recoIPHelCovxx_2) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelCovxy_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPHelCovxy_2 != nullptr) ? (product.m_recoIPHelCovxy_2) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelCovxz_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPHelCovxz_2 != nullptr) ? (product.m_recoIPHelCovxz_2) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelCovyy_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPHelCovyy_2 != nullptr) ? (product.m_recoIPHelCovyy_2) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelCovyz_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPHelCovyz_2 != nullptr) ? (product.m_recoIPHelCovyz_2) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelCovzz_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPHelCovzz_2 != nullptr) ? (product.m_recoIPHelCovzz_2) : DefaultValues::UndefinedFloat);
	});

	// IP vectors wrt the refitted PV with helical approach
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "IPHelrPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_recoIPHelrPV_1).x() != -999) ? RMPoint( (product.m_recoIPHelrPV_1).x(), (product.m_recoIPHelrPV_1).y(), (product.m_recoIPHelrPV_1).z() ) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "IPHelrPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_recoIPHelrPV_2).x() != -999) ? RMPoint( (product.m_recoIPHelrPV_2).x(), (product.m_recoIPHelrPV_2).y(), (product.m_recoIPHelrPV_2).z() ) : DefaultValues::UndefinedRMPoint);
	});

	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "IPHelrPVBS_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_recoIPHelrPVBS_1).x() != -999) ? RMPoint( (product.m_recoIPHelrPVBS_1).x(), (product.m_recoIPHelrPVBS_1).y(), (product.m_recoIPHelrPVBS_1).z() ) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "IPHelrPVBS_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_recoIPHelrPVBS_2).x() != -999) ? RMPoint( (product.m_recoIPHelrPVBS_2).x(), (product.m_recoIPHelrPVBS_2).y(), (product.m_recoIPHelrPVBS_2).z() ) : DefaultValues::UndefinedRMPoint);
	});
	// Components
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificanceHelrPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_IPSignificanceHelrPV_1!= nullptr) ? product.m_IPSignificanceHelrPV_1 : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificanceHelrPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_IPSignificanceHelrPV_2!= nullptr) ? product.m_IPSignificanceHelrPV_2 : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificanceHelrPV_Track_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_IPSignificanceHelrPV_Track_1!= nullptr) ? product.m_IPSignificanceHelrPV_Track_1 : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificanceHelrPV_Track_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_IPSignificanceHelrPV_Track_2!= nullptr) ? product.m_IPSignificanceHelrPV_Track_2 : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificanceHelrPV_PV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_IPSignificanceHelrPV_PV_1!= nullptr) ? product.m_IPSignificanceHelrPV_PV_1 : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificanceHelrPV_PV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_IPSignificanceHelrPV_PV_2!= nullptr) ? product.m_IPSignificanceHelrPV_PV_2 : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelrPVCovxx_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPHelrPVCovxx_1 != nullptr) ? (product.m_recoIPHelrPVCovxx_1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelrPVCovxy_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPHelrPVCovxy_1 != nullptr) ? (product.m_recoIPHelrPVCovxy_1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelrPVCovxz_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPHelrPVCovxz_1 != nullptr) ? (product.m_recoIPHelrPVCovxz_1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelrPVCovyy_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPHelrPVCovyy_1 != nullptr) ? (product.m_recoIPHelrPVCovyy_1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelrPVCovyz_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPHelrPVCovyz_1 != nullptr) ? (product.m_recoIPHelrPVCovyz_1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelrPVCovzz_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPHelrPVCovzz_1 != nullptr) ? (product.m_recoIPHelrPVCovzz_1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelrPVCovxx_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPHelrPVCovxx_2 != nullptr) ? (product.m_recoIPHelrPVCovxx_2) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelrPVCovxy_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPHelrPVCovxy_2 != nullptr) ? (product.m_recoIPHelrPVCovxy_2) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelrPVCovxz_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPHelrPVCovxz_2 != nullptr) ? (product.m_recoIPHelrPVCovxz_2) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelrPVCovyy_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPHelrPVCovyy_2 != nullptr) ? (product.m_recoIPHelrPVCovyy_2) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelrPVCovyz_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPHelrPVCovyz_2 != nullptr) ? (product.m_recoIPHelrPVCovyz_2) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelrPVCovzz_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_recoIPHelrPVCovzz_2 != nullptr) ? (product.m_recoIPHelrPVCovzz_2) : DefaultValues::UndefinedFloat);
	});


	// IP with helical approach, refitPV and BS
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificanceHelrPVBS_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_IPSignificanceHelrPVBS_1!= nullptr) ? product.m_IPSignificanceHelrPVBS_1 : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificanceHelrPVBS_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_IPSignificanceHelrPVBS_2!= nullptr) ? product.m_IPSignificanceHelrPVBS_2 : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificanceHelrPVBS_Track_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_IPSignificanceHelrPVBS_Track_1!= nullptr) ? product.m_IPSignificanceHelrPVBS_Track_1 : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificanceHelrPVBS_Track_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_IPSignificanceHelrPVBS_Track_2!= nullptr) ? product.m_IPSignificanceHelrPVBS_Track_2 : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificanceHelrPVBS_PV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_IPSignificanceHelrPVBS_PV_1!= nullptr) ? product.m_IPSignificanceHelrPVBS_PV_1 : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificanceHelrPVBS_PV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_IPSignificanceHelrPVBS_PV_2!= nullptr) ? product.m_IPSignificanceHelrPVBS_PV_2 : DefaultValues::UndefinedFloat);
	});

	// distance between track and theBS
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "trackFromBS_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_track1FromBS).x() != -999) ? RMPoint(product.m_track1FromBS.x(), product.m_track1FromBS.y(), product.m_track1FromBS.z()) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "trackFromBS_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_track2FromBS).x() != -999) ? RMPoint(product.m_track2FromBS.x(), product.m_track2FromBS.y(), product.m_track2FromBS.z()) : DefaultValues::UndefinedRMPoint);
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

	// errors on dxy, dz and IP wrt nominalPV
	// using propagation of errors
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errD0_1_newErr", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_errorIP1vec.at(0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errDZ_1_newErr", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_errorIP1vec.at(1);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errIP_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_errorIP1vec.at(2);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errD0_2_newErr", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_errorIP2vec.at(0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errDZ_2_newErr", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_errorIP2vec.at(1);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errIP_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_errorIP2vec.at(2);
	});


	// errors on dxy, dz and IP wrt refitted PV
	// using propagation of errors
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errD0rPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_errorIP1vecrPV.at(0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errDZrPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_errorIP1vecrPV.at(1);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errIPrPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_errorIP1vecrPV.at(2);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errD0rPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_errorIP2vecrPV.at(0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errDZrPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_errorIP2vecrPV.at(1);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errIPrPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_errorIP2vecrPV.at(2);
	});


	// deltaEta, deltaPhi, deltaR and angle delta between genIP and recoIP(nominalPV)
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIP_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaEtaGenRecoIP_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIP_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaEtaGenRecoIP_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIP_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaPhiGenRecoIP_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIP_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaPhiGenRecoIP_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIP_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaRGenRecoIP_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIP_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaRGenRecoIP_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIP_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaGenRecoIP_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIP_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaGenRecoIP_2;
	});

	// deltaEta, deltaPhi, deltaR and angle delta between genIP and recoIPHel(nominalPV)
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIPHel_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaEtaGenRecoIPHel_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIPHel_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaEtaGenRecoIPHel_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIPHel_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaPhiGenRecoIPHel_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIPHel_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaPhiGenRecoIPHel_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIPHel_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaRGenRecoIPHel_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIPHel_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaRGenRecoIPHel_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIPHel_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaGenRecoIPHel_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIPHel_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaGenRecoIPHel_2;
	});

	// deltaEta, deltaPhi, deltaR and angle delta between genIP and recoIPHel(refitPV)
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIPHelrPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaEtaGenRecoIPHelrPV_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIPHelrPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaEtaGenRecoIPHelrPV_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIPHelrPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaPhiGenRecoIPHelrPV_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIPHelrPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaPhiGenRecoIPHelrPV_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIPHelrPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaRGenRecoIPHelrPV_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIPHelrPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaRGenRecoIPHelrPV_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIPHelrPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaGenRecoIPHelrPV_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIPHelrPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaGenRecoIPHelrPV_2;
	});

	// deltaEta, deltaPhi, deltaR and angle delta between genIP and recoIPHel(refitPVBS)
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIPHelrPVBS_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaEtaGenRecoIPHelrPVBS_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIPHelrPVBS_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaEtaGenRecoIPHelrPVBS_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIPHelrPVBS_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaPhiGenRecoIPHelrPVBS_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIPHelrPVBS_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaPhiGenRecoIPHelrPVBS_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIPHelrPVBS_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaRGenRecoIPHelrPVBS_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIPHelrPVBS_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaRGenRecoIPHelrPVBS_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIPHelrPVBS_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaGenRecoIPHelrPVBS_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIPHelrPVBS_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaGenRecoIPHelrPVBS_2;
	});


	// deltaEta, deltaPhi, deltaR and angle delta between genIP and recoIP(refitPV)
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIPrPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaEtaGenRecoIPrPV_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIPrPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaEtaGenRecoIPrPV_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIPrPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaPhiGenRecoIPrPV_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIPrPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaPhiGenRecoIPrPV_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIPrPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaRGenRecoIPrPV_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIPrPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaRGenRecoIPrPV_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIPrPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaGenRecoIPrPV_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIPrPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaGenRecoIPrPV_2;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "d0s_area", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_d0s_area;
	});

	// deltaEta, deltaPhi, deltaR and angle delta between genIP and recoIP(refitPVBS)
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIPrPVBS_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaEtaGenRecoIPrPVBS_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIPrPVBS_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaEtaGenRecoIPrPVBS_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIPrPVBS_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaPhiGenRecoIPrPVBS_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIPrPVBS_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaPhiGenRecoIPrPVBS_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIPrPVBS_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaRGenRecoIPrPVBS_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIPrPVBS_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaRGenRecoIPrPVBS_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIPrPVBS_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaGenRecoIPrPVBS_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIPrPVBS_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaGenRecoIPrPVBS_2;
	});
	// deltaEta, deltaPhi, deltaR and angle delta between the IP from Tangential and Helical Approach
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaTanHelIP_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaEtaTanHelIP_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaTanHelIP_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaEtaTanHelIP_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiTanHelIP_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaPhiTanHelIP_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiTanHelIP_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaPhiTanHelIP_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRTanHelIP_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaRTanHelIP_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRTanHelIP_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaRTanHelIP_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaTanHelIP_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaTanHelIP_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaTanHelIP_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaTanHelIP_2;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaTanHelIPrPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaEtaTanHelIPrPV_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaTanHelIPrPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaEtaTanHelIPrPV_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiTanHelIPrPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaPhiTanHelIPrPV_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiTanHelIPrPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaPhiTanHelIPrPV_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRTanHelIPrPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaRTanHelIPrPV_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRTanHelIPrPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaRTanHelIPrPV_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaTanHelIPrPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaTanHelIPrPV_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaTanHelIPrPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaTanHelIPrPV_2;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaTanHelIPrPVBS_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaEtaTanHelIPrPVBS_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaTanHelIPrPVBS_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaEtaTanHelIPrPVBS_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiTanHelIPrPVBS_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaPhiTanHelIPrPVBS_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiTanHelIPrPVBS_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaPhiTanHelIPrPVBS_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRTanHelIPrPVBS_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaRTanHelIPrPVBS_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRTanHelIPrPVBS_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaRTanHelIPrPVBS_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaTanHelIPrPVBS_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaTanHelIPrPVBS_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaTanHelIPrPVBS_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_deltaTanHelIPrPVBS_2;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "d0s_dist", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_d0s_dist;
	});

	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "RefHelix_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_RefHelix_1;
	});

	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "RefHelix_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_RefHelix_2;
	});

	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "PHelix_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_PHelix_1;
	});

	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "PHelix_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_PHelix_2;
	});
}

void RecoTauCPProducer::Produce(event_type const& event, product_type& product, setting_type const& settings, metadata_type const& metadata) const
{
	assert(event.m_vertexSummary);
	assert(product.m_flavourOrderedLeptons.size() >= 2);

	// initialization of TVector3 objects
	product.m_recoIP1.SetXYZ(-999,-999,-999);
	product.m_recoIP2.SetXYZ(-999,-999,-999);
	product.m_recoIPrPV_1.SetXYZ(-999,-999,-999);
	product.m_recoIPrPV_2.SetXYZ(-999,-999,-999);
	product.m_recoIPrPVBS_1.SetXYZ(-999,-999,-999);
	product.m_recoIPrPVBS_2.SetXYZ(-999,-999,-999);
	product.m_recoIPHel_1.SetXYZ(-999,-999,-999);
	product.m_recoIPHel_2.SetXYZ(-999,-999,-999);
	product.m_recoIPHelrPV_1.SetXYZ(-999,-999,-999);
	product.m_recoIPHelrPV_2.SetXYZ(-999,-999,-999);
	product.m_recoIPHelrPVBS_1.SetXYZ(-999,-999,-999);
	product.m_recoIPHelrPVBS_2.SetXYZ(-999,-999,-999);
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

	// Calculate the PCA relative to the center of the detector
	double qOverP_1     = (product.m_flavourOrderedLeptons.at(0)->track.helixParameters())[0];
	double lambda_1     = (product.m_flavourOrderedLeptons.at(0)->track.helixParameters())[1];
	double phi_1        = (product.m_flavourOrderedLeptons.at(0)->track.helixParameters())[2];
	double dxy_1        = (product.m_flavourOrderedLeptons.at(0)->track.helixParameters())[3];
	double dsz_1        = (product.m_flavourOrderedLeptons.at(0)->track.helixParameters())[4];
	int    sgnQ_1       = qOverP_1/TMath::Abs(qOverP_1);

	double qOverP_2     = (product.m_flavourOrderedLeptons.at(1)->track.helixParameters())[0];
	double lambda_2     = (product.m_flavourOrderedLeptons.at(1)->track.helixParameters())[1];
	double phi_2        = (product.m_flavourOrderedLeptons.at(1)->track.helixParameters())[2];
	double dxy_2        = (product.m_flavourOrderedLeptons.at(1)->track.helixParameters())[3];
	double dsz_2        = (product.m_flavourOrderedLeptons.at(1)->track.helixParameters())[4];
	int    sgnQ_2       = qOverP_2/TMath::Abs(qOverP_2);

	//TVector3 PHelix_1;
	product.m_PHelix_1.SetXYZ(TMath::Cos(lambda_1) * TMath::Cos(phi_1) * sgnQ_1 / qOverP_1,
			TMath::Cos(lambda_1) * TMath::Sin(phi_1) * sgnQ_1 / qOverP_1,
			TMath::Sin(lambda_1) * sgnQ_1 / qOverP_1);

	//TVector3 PHelix_2;
	product.m_PHelix_2.SetXYZ(TMath::Cos(lambda_2) * TMath::Cos(phi_2) * sgnQ_2 / qOverP_2,
			TMath::Cos(lambda_2) * TMath::Sin(phi_2) * sgnQ_2 / qOverP_2,
			TMath::Sin(lambda_2) * sgnQ_2 / qOverP_2);

	//TVector3 RefHelix_1;
	// product.m_RefHelix_1.SetXYZ(-dsz_1 * TMath::Cos(phi_1) * TMath::Sin(lambda_1) - dxy_1 * TMath::Sin(phi_1),
	//		 dxy_1 * TMath::Cos(phi_1) - dsz_1 * TMath::Sin(lambda_1) * TMath::Sin(phi_1),
	//		 dsz_1 * TMath::Cos(lambda_1) );

	product.m_RefHelix_1.SetXYZ(- dxy_1 * TMath::Sin(phi_1),
					dxy_1 * TMath::Cos(phi_1),
					dsz_1 / TMath::Cos(lambda_1));

	//TVector3 RefHelix_2;
	// product.m_RefHelix_2.SetXYZ(-dsz_2 * TMath::Cos(phi_2) * TMath::Sin(lambda_2) - dxy_2 * TMath::Sin(phi_2),
	//		 dxy_2 * TMath::Cos(phi_2) - dsz_2 * TMath::Sin(lambda_2) * TMath::Sin(phi_2),
	//		 dsz_2 * TMath::Cos(lambda_2) );

	product.m_RefHelix_2.SetXYZ(- dxy_2 * TMath::Sin(phi_2),
					dxy_2 * TMath::Cos(phi_2),
					dsz_2 / TMath::Cos(lambda_2));

	// distance between track and BS center
	product.m_track1FromBS = cpq.CalculateShortestDistance(recoParticle1, event.m_beamSpot->position);
	product.m_track2FromBS = cpq.CalculateShortestDistance(recoParticle2, event.m_beamSpot->position);

	// ----------
	// rho-method (DP+DP)
	// ----------
	double posyLRho = 1;
	double negyLRho = 1;
	RMFLV piZeroP(0,0,0,0);
	RMFLV piZeroM(0,0,0,0);
	RMFLV piSSFromRhoP(0,0,0,0);
	RMFLV piOSP(0,0,0,0);
	RMFLV piSSFromRhoM(0,0,0,0);
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
				piSSFromRhoP, piOSP);
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
				piSSFromRhoM, piOSM);
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

	product.m_d0s_area = cpq.CalculateD0sArea((product.m_refitPV ? product.m_flavourOrderedLeptons.at(0)->track.getDxy(product.m_refitPV) : DefaultValues::UndefinedDouble), (product.m_refitPV ? product.m_flavourOrderedLeptons.at(1)->track.getDxy(product.m_refitPV) : DefaultValues::UndefinedDouble));

	product.m_d0s_dist = cpq.CalculateD0sDist((product.m_refitPV ? product.m_flavourOrderedLeptons.at(0)->track.getDxy(product.m_refitPV) : DefaultValues::UndefinedDouble), (product.m_refitPV ? product.m_flavourOrderedLeptons.at(1)->track.getDxy(product.m_refitPV) : DefaultValues::UndefinedDouble));

	// ---------
	// ip-method (IP+IP)
	// ---------
	// phi*CP wrt nominalPV
	product.m_recoPhiStarCP = cpq.CalculatePhiStarCP(&(event.m_vertexSummary->pv), trackP, trackM, momentumP, momentumM);

	// calculation of the IP vectors and relative errors
	// IP wrt nominalPV
	product.m_recoIP1 = ip.CalculateShortestDistance(recoParticle1->p4, recoParticle1->track.ref, event.m_vertexSummary->pv.position);
	product.m_recoIP2 = ip.CalculateShortestDistance(recoParticle2->p4, recoParticle2->track.ref, event.m_vertexSummary->pv.position);
	product.m_errorIP1vec = cpq.CalculateIPErrors(recoParticle1, &(event.m_vertexSummary->pv), &product.m_recoIP1);
	product.m_errorIP2vec = cpq.CalculateIPErrors(recoParticle2, &(event.m_vertexSummary->pv), &product.m_recoIP2);

	//Projection of Point of closest approach (PCA) to the primary vertex (PV) uncertainty ellipsoid
	product.m_pca1proj = ip.CalculatePCADifferece(event.m_vertexSummary->pv.covariance,product.m_recoIP1);
	product.m_pca2proj = ip.CalculatePCADifferece(event.m_vertexSummary->pv.covariance,product.m_recoIP2);
	//Distance of Point of closest approach (PCA) from the primary vertex (PV) in units of sigma_PV
	product.m_pca1DiffInSigma = ip.CalculateIPSignificanceTangential(product.m_recoIP1, event.m_vertexSummary->pv.covariance);
	product.m_pca2DiffInSigma = ip.CalculateIPSignificanceTangential(product.m_recoIP2, event.m_vertexSummary->pv.covariance);

	//Impact parameters via helical approach in cm:
	product.m_recoIPHel_1 = ip.CalculatePCA(product.m_flavourOrderedLeptons.at(0)->track.magneticField, product.m_flavourOrderedLeptons.at(0)->track.helixParameters(), product.m_flavourOrderedLeptons.at(0)->track.ref, event.m_vertexSummary->pv.position);
	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IPHelCov_1 = ip.CalculatePCACovariance(product.m_flavourOrderedLeptons.at(0)->track.helixCovariance, event.m_vertexSummary->pv.covariance);
	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IPHelCovTrack_1 = ip.CalculatePCACovarianceTrack(product.m_flavourOrderedLeptons.at(0)->track.helixCovariance);
	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IPHelCovPV_1 = ip.CalculatePCACovariancePV(event.m_vertexSummary->pv.covariance);

	product.m_recoIPHel_2 = ip.CalculatePCA(product.m_flavourOrderedLeptons.at(1)->track.magneticField, product.m_flavourOrderedLeptons.at(1)->track.helixParameters(), product.m_flavourOrderedLeptons.at(1)->track.ref, event.m_vertexSummary->pv.position);
	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IPHelCov_2 = ip.CalculatePCACovariance(product.m_flavourOrderedLeptons.at(1)->track.helixCovariance, event.m_vertexSummary->pv.covariance);
	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IPHelCovTrack_2 = ip.CalculatePCACovarianceTrack(product.m_flavourOrderedLeptons.at(1)->track.helixCovariance);
	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IPHelCovPV_2 = ip.CalculatePCACovariancePV(event.m_vertexSummary->pv.covariance);

	ROOT::Math::SVector<float, 3> IP_1_(product.m_recoIPHel_1(0), product.m_recoIPHel_1(1), product.m_recoIPHel_1(2));
	ROOT::Math::SVector<float, 3> IP_2_(product.m_recoIPHel_2(0), product.m_recoIPHel_2(1), product.m_recoIPHel_2(2));

	IP_1_ = IP_1_.Unit();
	IP_2_ = IP_2_.Unit();

	product.m_errorIPHel_Track_1 = sqrt( ROOT::Math::Dot(IP_1_, IPHelCovTrack_1 * IP_1_ ) );
	product.m_errorIPHel_Track_2 = sqrt( ROOT::Math::Dot(IP_2_, IPHelCovTrack_2 * IP_2_ ) );

	product.m_IPSignificanceHel_Track_1 = product.m_recoIPHel_1.Mag() / product.m_errorIPHel_Track_1;
	product.m_IPSignificanceHel_Track_2 = product.m_recoIPHel_2.Mag() / product.m_errorIPHel_Track_2;

	product.m_errorIPHel_PV_1 = sqrt( ROOT::Math::Dot(IP_1_, IPHelCovPV_1 * IP_1_ ) );
	product.m_errorIPHel_PV_2 = sqrt( ROOT::Math::Dot(IP_2_, IPHelCovPV_2 * IP_2_ ) );

	product.m_IPSignificanceHel_PV_1 = product.m_recoIPHel_1.Mag() / product.m_errorIPHel_PV_1;
	product.m_IPSignificanceHel_PV_2 = product.m_recoIPHel_2.Mag() / product.m_errorIPHel_PV_2;

	product.m_recoIPHelCovxx_1 = IPHelCov_1(0,0);
	product.m_recoIPHelCovxy_1 = IPHelCov_1(0,1);
	product.m_recoIPHelCovxz_1 = IPHelCov_1(0,2);
	product.m_recoIPHelCovyy_1 = IPHelCov_1(1,1);
	product.m_recoIPHelCovyz_1 = IPHelCov_1(1,2);
	product.m_recoIPHelCovzz_1 = IPHelCov_1(2,2);

	product.m_recoIPHelCovxx_2 = IPHelCov_2(0,0);
	product.m_recoIPHelCovxy_2 = IPHelCov_2(0,1);
	product.m_recoIPHelCovxz_2 = IPHelCov_2(0,2);
	product.m_recoIPHelCovyy_2 = IPHelCov_2(1,1);
	product.m_recoIPHelCovyz_2 = IPHelCov_2(1,2);
	product.m_recoIPHelCovzz_2 = IPHelCov_2(2,2);

	// Conversion from TVector3 to SVector
	product.m_IPSignificanceHel_1 = ip.CalculateIPSignificanceHelical(product.m_recoIPHel_1, IPHelCov_1);
	product.m_IPSignificanceHel_2 = ip.CalculateIPSignificanceHelical(product.m_recoIPHel_2, IPHelCov_2);
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
	RMFLV piOS1(0,0,0,0);
	unsigned int decayType1 = 0;//0: lep or pi, 1: rho or a1(1-prong), 2: 3-prongs
	if (recoTau1 != nullptr) {
	  if (recoTau1->decayMode > 0) {
	    int dmMva = (int)recoTau1->getDiscriminator("MVADM2017v1", event.m_tauMetadata);
	    if (dmMva == 1 || dmMva == 2)
	      decayType1 = 1;
	    else if(dmMva == 10 || dmMva == 11)
	      decayType1 = 2;
	  }
	}
	KTau* recoTau2 = dynamic_cast<KTau*>(recoParticle2);
	RMFLV piZero2(0,0,0,0);
	RMFLV piSSFromRho2(0,0,0,0);
	RMFLV piOS2(0,0,0,0);
	unsigned int decayType2 = 0;//0: lep or pi, 1: rho or a1(1-prong), 2: 3-prongs
	if (recoTau2 != nullptr) {
	  if (recoTau2->decayMode > 0) {
	    int dmMva = (int)recoTau2->getDiscriminator("MVADM2017v1", event.m_tauMetadata);
	    if (dmMva == 1 || dmMva == 2)
	      decayType2 = 1;
	    else if(dmMva == 10 || dmMva == 11)
	      decayType2 = 2;
	  }
	}
	if (recoParticle1->getHash() == chargedPart1->getHash()) {
	  piZero1 = piZeroP;
	  piSSFromRho1 = piSSFromRhoP;
	  piOS1 = piOSP;
	  piZero2 = piZeroM;
	  piSSFromRho2 = piSSFromRhoM;
	  piOS2 = piOSM;
	}
	else {
	  piZero1 = piZeroM;
	  piSSFromRho1 = piSSFromRhoM;
	  piOS1 = piOSM;
	  piZero2 = piZeroP;
	  piSSFromRho2 = piSSFromRhoP;
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

	product.m_deltaEtaTanHelIP_1 = product.m_recoIP1.Eta() - product.m_recoIPHel_1.Eta();
	product.m_deltaPhiTanHelIP_1 = product.m_recoIP1.DeltaPhi(product.m_recoIPHel_1);
	product.m_deltaRTanHelIP_1 = product.m_recoIP1.DeltaR(product.m_recoIPHel_1);
	product.m_deltaTanHelIP_1 = product.m_recoIP1.Angle(product.m_recoIPHel_1);

	product.m_deltaEtaTanHelIP_2 = product.m_recoIP2.Eta() - product.m_recoIPHel_2.Eta();
	product.m_deltaPhiTanHelIP_2 = product.m_recoIP2.DeltaPhi(product.m_recoIPHel_2);
	product.m_deltaRTanHelIP_2 = product.m_recoIP2.DeltaR(product.m_recoIPHel_2);
	product.m_deltaTanHelIP_2 = product.m_recoIP2.Angle(product.m_recoIPHel_2);

	if (!m_isData){
		if(&product.m_genIP1 != nullptr && product.m_genIP1.x() != -999){
			//with the tangential approach
			product.m_deltaEtaGenRecoIP_1 = product.m_recoIP1.Eta() - product.m_genIP1.Eta();
			product.m_deltaPhiGenRecoIP_1 = product.m_recoIP1.DeltaPhi(product.m_genIP1);
			product.m_deltaRGenRecoIP_1   = product.m_recoIP1.DeltaR(product.m_genIP1);
			product.m_deltaGenRecoIP_1    = product.m_recoIP1.Angle(product.m_genIP1);

			//with the helical approach
			product.m_deltaEtaGenRecoIPHel_1 = product.m_recoIPHel_1.Eta() - product.m_genIP1.Eta();
			product.m_deltaPhiGenRecoIPHel_1 = product.m_recoIPHel_1.DeltaPhi(product.m_genIP1);//product.m_recoIP1);//
			product.m_deltaRGenRecoIPHel_1   = product.m_recoIPHel_1.DeltaR(product.m_genIP1);
			product.m_deltaGenRecoIPHel_1    = product.m_recoIPHel_1.Angle(product.m_genIP1);//product.m_recoIP1);//

		} // if genIP1 exists
		if(&product.m_genIP2 != nullptr && product.m_genIP2.x() != -999){
			product.m_deltaEtaGenRecoIP_2 = product.m_recoIP2.Eta() - product.m_genIP2.Eta();
			product.m_deltaPhiGenRecoIP_2 = product.m_recoIP2.DeltaPhi(product.m_genIP2);
			product.m_deltaRGenRecoIP_2   = product.m_recoIP2.DeltaR(product.m_genIP2);
			product.m_deltaGenRecoIP_2    = product.m_recoIP2.Angle(product.m_genIP2);

			product.m_deltaEtaGenRecoIPHel_2 = product.m_recoIPHel_2.Eta() - product.m_genIP2.Eta();
			product.m_deltaPhiGenRecoIPHel_2 = product.m_recoIPHel_2.DeltaPhi(product.m_genIP2);
			product.m_deltaRGenRecoIPHel_2   = product.m_recoIPHel_2.DeltaR(product.m_genIP2);
			product.m_deltaGenRecoIPHel_2    = product.m_recoIPHel_2.Angle(product.m_genIP2);

		} // if genIP2 exists
	} // if this is not data

	//FIXME: check if refitPV exists removed =>
	// IP wrt refitPV
	// FIXME the errorIP1vecrPV is not used anymore
	product.m_recoIPrPV_1 = ip.CalculateShortestDistance(recoParticle1->p4, recoParticle1->track.ref, rPV->position);
	product.m_recoIPrPV_2 = ip.CalculateShortestDistance(recoParticle2->p4, recoParticle2->track.ref, rPV->position);
	product.m_errorIP1vecrPV = cpq.CalculateIPErrors(recoParticle1, rPV, &product.m_recoIPrPV_1);
	product.m_errorIP2vecrPV = cpq.CalculateIPErrors(recoParticle2, rPV, &product.m_recoIPrPV_2);

	product.m_recoIPrPVBS_1 = ip.CalculateShortestDistance(recoParticle1->p4, recoParticle1->track.ref, rPVBS->position);
	product.m_recoIPrPVBS_2 = ip.CalculateShortestDistance(recoParticle2->p4, recoParticle2->track.ref, rPVBS->position);
	product.m_errorIP1vecrPVBS = cpq.CalculateIPErrors(recoParticle1, rPVBS, &product.m_recoIPrPV_1);
	product.m_errorIP2vecrPVBS = cpq.CalculateIPErrors(recoParticle2, rPVBS, &product.m_recoIPrPV_2);

	//Projection of Point of closest approach (PCA) to the primary vertex (PV) uncertainty ellipsoid
	product.m_pca1projrPV = ip.CalculatePCADifferece(rPV->covariance,product.m_recoIPrPV_1);
	product.m_pca2projrPV = ip.CalculatePCADifferece(rPV->covariance,product.m_recoIPrPV_2);
	//Distance of Point of closest approach (PCA) from the primary vertex (PV) in units of sigma_PV
	product.m_pca1DiffInSigmarPV = sqrt( product.m_recoIPrPV_1 * product.m_recoIPrPV_1 )/product.m_pca1projrPV;
	product.m_pca2DiffInSigmarPV = sqrt( product.m_recoIPrPV_2 * product.m_recoIPrPV_2 )/product.m_pca2projrPV;
	//Projection of Point of closest approach (PCA) to the primary vertex (PV) uncertainty ellipsoid
	product.m_pca1projrPVBS = ip.CalculatePCADifferece(rPVBS->covariance,product.m_recoIPrPVBS_1);
	product.m_pca2projrPVBS = ip.CalculatePCADifferece(rPVBS->covariance,product.m_recoIPrPVBS_2);
	//Distance of Point of closest approach (PCA) from the primary vertex (PV) with BS constraint in units of sigma_PV
	product.m_pca1DiffInSigmarPVBS = sqrt( product.m_recoIPrPVBS_1 * product.m_recoIPrPVBS_1 )/product.m_pca1projrPVBS;
	product.m_pca2DiffInSigmarPVBS = sqrt( product.m_recoIPrPVBS_2 * product.m_recoIPrPVBS_2 )/product.m_pca2projrPVBS;
	//Impact parameters via helical approach in cm:
	product.m_recoIPHelrPV_1 = ip.CalculatePCA(product.m_flavourOrderedLeptons.at(0)->track.magneticField, product.m_flavourOrderedLeptons.at(0)->track.helixParameters(), product.m_flavourOrderedLeptons.at(0)->track.ref, rPV->position);
	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IPHelrPVCov_1 = ip.CalculatePCACovariance(product.m_flavourOrderedLeptons.at(0)->track.helixCovariance, rPV->covariance);
	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IPHelrPVCovTrack_1 = ip.CalculatePCACovarianceTrack(product.m_flavourOrderedLeptons.at(0)->track.helixCovariance);
	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IPHelrPVCovPV_1 = ip.CalculatePCACovariancePV(rPV->covariance);

	product.m_recoIPHelrPV_2 = ip.CalculatePCA(product.m_flavourOrderedLeptons.at(1)->track.magneticField, product.m_flavourOrderedLeptons.at(1)->track.helixParameters(), product.m_flavourOrderedLeptons.at(1)->track.ref, rPV->position);
	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IPHelrPVCov_2 = ip.CalculatePCACovariance(product.m_flavourOrderedLeptons.at(1)->track.helixCovariance, rPV->covariance);
	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IPHelrPVCovTrack_2 = ip.CalculatePCACovarianceTrack(product.m_flavourOrderedLeptons.at(1)->track.helixCovariance);
	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IPHelrPVCovPV_2 = ip.CalculatePCACovariancePV(rPV->covariance);

	product.m_recoIPHelrPVCovxx_1 = IPHelrPVCov_1(0,0);
	product.m_recoIPHelrPVCovxy_1 = IPHelrPVCov_1(0,1);
	product.m_recoIPHelrPVCovxz_1 = IPHelrPVCov_1(0,2);
	product.m_recoIPHelrPVCovyy_1 = IPHelrPVCov_1(1,1);
	product.m_recoIPHelrPVCovyz_1 = IPHelrPVCov_1(1,2);
	product.m_recoIPHelrPVCovzz_1 = IPHelrPVCov_1(2,2);

	product.m_recoIPHelrPVCovxx_2 = IPHelrPVCov_2(0,0);
	product.m_recoIPHelrPVCovxy_2 = IPHelrPVCov_2(0,1);
	product.m_recoIPHelrPVCovxz_2 = IPHelrPVCov_2(0,2);
	product.m_recoIPHelrPVCovyy_2 = IPHelrPVCov_2(1,1);
	product.m_recoIPHelrPVCovyz_2 = IPHelrPVCov_2(1,2);
	product.m_recoIPHelrPVCovzz_2 = IPHelrPVCov_2(2,2);
	// Conversion from TVector3 to SVector
	ROOT::Math::SVector<float, 3> IPrPV_1_(product.m_recoIPHelrPV_1(0), product.m_recoIPHelrPV_1(1), product.m_recoIPHelrPV_1(2));
	ROOT::Math::SVector<float, 3> IPrPV_2_(product.m_recoIPHelrPV_2(0), product.m_recoIPHelrPV_2(1), product.m_recoIPHelrPV_2(2));
	
	IPrPV_1_ = IPrPV_1_.Unit();
	IPrPV_2_ = IPrPV_2_.Unit();

	product.m_errorIPHelrPV_1 = sqrt( ROOT::Math::Dot(IPrPV_1_, IPHelrPVCov_1 * IPrPV_1_ ) );
	product.m_errorIPHelrPV_2 = sqrt( ROOT::Math::Dot(IPrPV_2_, IPHelrPVCov_2 * IPrPV_2_ ) );

	product.m_IPSignificanceHelrPV_1 = product.m_recoIPHelrPV_1.Mag() / product.m_errorIPHelrPV_1;
	product.m_IPSignificanceHelrPV_2 = product.m_recoIPHelrPV_2.Mag() / product.m_errorIPHelrPV_2;

	product.m_errorIPHelrPV_Track_1 = sqrt( ROOT::Math::Dot(IPrPV_1_, IPHelrPVCovTrack_1 * IPrPV_1_ ) );
	product.m_errorIPHelrPV_Track_2 = sqrt( ROOT::Math::Dot(IPrPV_2_, IPHelrPVCovTrack_2 * IPrPV_2_ ) );

	product.m_IPSignificanceHelrPV_Track_1 = product.m_recoIPHelrPV_1.Mag() / product.m_errorIPHelrPV_Track_1;
	product.m_IPSignificanceHelrPV_Track_2 = product.m_recoIPHelrPV_2.Mag() / product.m_errorIPHelrPV_Track_2;

	product.m_errorIPHelrPV_PV_1 = sqrt( ROOT::Math::Dot(IPrPV_1_, IPHelrPVCovPV_1 * IPrPV_1_ ) );
	product.m_errorIPHelrPV_PV_2 = sqrt( ROOT::Math::Dot(IPrPV_2_, IPHelrPVCovPV_2 * IPrPV_2_ ) );

	product.m_IPSignificanceHelrPV_PV_1 = product.m_recoIPHelrPV_1.Mag() / product.m_errorIPHelrPV_PV_1;
	product.m_IPSignificanceHelrPV_PV_2 = product.m_recoIPHelrPV_2.Mag() / product.m_errorIPHelrPV_PV_2;

	product.m_recoIPHelrPVBS_1 = ip.CalculatePCA(product.m_flavourOrderedLeptons.at(0)->track.magneticField, product.m_flavourOrderedLeptons.at(0)->track.helixParameters(), product.m_flavourOrderedLeptons.at(0)->track.ref, rPVBS->position);
	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IPHelrPVBSCov_1 = ip.CalculatePCACovariance(product.m_flavourOrderedLeptons.at(0)->track.helixCovariance, rPVBS->covariance);
	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IPHelrPVBSCovTrack_1 = ip.CalculatePCACovarianceTrack(product.m_flavourOrderedLeptons.at(0)->track.helixCovariance);
	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IPHelrPVBSCovPV_1 = ip.CalculatePCACovariancePV(rPVBS->covariance);

	product.m_recoIPHelrPVBS_2 = ip.CalculatePCA(product.m_flavourOrderedLeptons.at(1)->track.magneticField, product.m_flavourOrderedLeptons.at(1)->track.helixParameters(), product.m_flavourOrderedLeptons.at(1)->track.ref, rPVBS->position);
	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IPHelrPVBSCov_2 = ip.CalculatePCACovariance(product.m_flavourOrderedLeptons.at(1)->track.helixCovariance, rPVBS->covariance);
	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IPHelrPVBSCovTrack_2 = ip.CalculatePCACovarianceTrack(product.m_flavourOrderedLeptons.at(1)->track.helixCovariance);
	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IPHelrPVBSCovPV_2 = ip.CalculatePCACovariancePV(rPVBS->covariance);

	product.m_recoIPHelrPVBSCovxx_1 = IPHelrPVBSCov_1(0,0);
	product.m_recoIPHelrPVBSCovxy_1 = IPHelrPVBSCov_1(0,1);
	product.m_recoIPHelrPVBSCovxz_1 = IPHelrPVBSCov_1(0,2);
	product.m_recoIPHelrPVBSCovyy_1 = IPHelrPVBSCov_1(1,1);
	product.m_recoIPHelrPVBSCovyz_1 = IPHelrPVBSCov_1(1,2);
	product.m_recoIPHelrPVBSCovzz_1 = IPHelrPVBSCov_1(2,2);

	product.m_recoIPHelrPVBSCovxx_2 = IPHelrPVBSCov_2(0,0);
	product.m_recoIPHelrPVBSCovxy_2 = IPHelrPVBSCov_2(0,1);
	product.m_recoIPHelrPVBSCovxz_2 = IPHelrPVBSCov_2(0,2);
	product.m_recoIPHelrPVBSCovyy_2 = IPHelrPVBSCov_2(1,1);
	product.m_recoIPHelrPVBSCovyz_2 = IPHelrPVBSCov_2(1,2);
	product.m_recoIPHelrPVBSCovzz_2 = IPHelrPVBSCov_2(2,2);
	// Conversion from TVector3 to SVector
	ROOT::Math::SVector<float, 3> IPrPVBS_1_(product.m_recoIPHelrPVBS_1(0), product.m_recoIPHelrPVBS_1(1), product.m_recoIPHelrPVBS_1(2));
	ROOT::Math::SVector<float, 3> IPrPVBS_2_(product.m_recoIPHelrPVBS_2(0), product.m_recoIPHelrPVBS_2(1), product.m_recoIPHelrPVBS_2(2));

	IPrPVBS_1_ = IPrPVBS_1_.Unit();
	IPrPVBS_2_ = IPrPVBS_2_.Unit();

	product.m_errorIPHelrPVBS_1 = sqrt( ROOT::Math::Dot(IPrPVBS_1_, IPHelrPVBSCov_1 * IPrPVBS_1_ ) );
	product.m_errorIPHelrPVBS_2 = sqrt( ROOT::Math::Dot(IPrPVBS_2_, IPHelrPVBSCov_2 * IPrPVBS_2_ ) );

	product.m_IPSignificanceHelrPVBS_1 = product.m_recoIPHelrPVBS_1.Mag() / product.m_errorIPHelrPVBS_1;
	product.m_IPSignificanceHelrPVBS_2 = product.m_recoIPHelrPVBS_2.Mag() / product.m_errorIPHelrPVBS_2;

	product.m_errorIPHelrPVBS_Track_1 = sqrt( ROOT::Math::Dot(IPrPVBS_1_, IPHelrPVBSCovTrack_1 * IPrPVBS_1_ ) );
	product.m_errorIPHelrPVBS_Track_2 = sqrt( ROOT::Math::Dot(IPrPVBS_2_, IPHelrPVBSCovTrack_2 * IPrPVBS_2_ ) );

	product.m_IPSignificanceHelrPVBS_Track_1 = product.m_recoIPHelrPVBS_1.Mag() / product.m_errorIPHelrPVBS_Track_1;
	product.m_IPSignificanceHelrPVBS_Track_2 = product.m_recoIPHelrPVBS_2.Mag() / product.m_errorIPHelrPVBS_Track_2;

	product.m_errorIPHelrPVBS_PV_1 = sqrt( ROOT::Math::Dot(IPrPVBS_1_, IPHelrPVBSCovPV_1 * IPrPVBS_1_ ) );
	product.m_errorIPHelrPVBS_PV_2 = sqrt( ROOT::Math::Dot(IPrPVBS_2_, IPHelrPVBSCovPV_2 * IPrPVBS_2_ ) );

	product.m_IPSignificanceHelrPVBS_PV_1 = product.m_recoIPHelrPVBS_1.Mag() / product.m_errorIPHelrPVBS_PV_1;
	product.m_IPSignificanceHelrPVBS_PV_2 = product.m_recoIPHelrPVBS_2.Mag() / product.m_errorIPHelrPVBS_PV_2;

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
	  else if (decayType2 == 1 && decayType2 == 0) {
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
	}  // if tt ch.

	product.m_deltaEtaTanHelIPrPV_1 = product.m_recoIPrPV_1.Eta() - product.m_recoIPHelrPV_1.Eta();
	product.m_deltaPhiTanHelIPrPV_1 = product.m_recoIPrPV_1.DeltaPhi(product.m_recoIPHelrPV_1);
	product.m_deltaRTanHelIPrPV_1 = product.m_recoIPrPV_1.DeltaR(product.m_recoIPHelrPV_1);
	product.m_deltaTanHelIPrPV_1 = product.m_recoIPrPV_1.Angle(product.m_recoIPHelrPV_1);

	product.m_deltaEtaTanHelIPrPV_2 = product.m_recoIPrPV_2.Eta() - product.m_recoIPHelrPV_2.Eta();
	product.m_deltaPhiTanHelIPrPV_2 = product.m_recoIPrPV_2.DeltaPhi(product.m_recoIPHelrPV_2);
	product.m_deltaRTanHelIPrPV_2 = product.m_recoIPrPV_2.DeltaR(product.m_recoIPHelrPV_2);
	product.m_deltaTanHelIPrPV_2 = product.m_recoIPrPV_2.Angle(product.m_recoIPHelrPV_2);

	product.m_deltaEtaTanHelIPrPVBS_1 = product.m_recoIPrPVBS_1.Eta() - product.m_recoIPHelrPVBS_1.Eta();
	product.m_deltaPhiTanHelIPrPVBS_1 = product.m_recoIPrPVBS_1.DeltaPhi(product.m_recoIPHelrPVBS_1);
	product.m_deltaRTanHelIPrPVBS_1 = product.m_recoIPrPVBS_1.DeltaR(product.m_recoIPHelrPVBS_1);
	product.m_deltaTanHelIPrPVBS_1 = product.m_recoIPrPVBS_1.Angle(product.m_recoIPHelrPVBS_1);

	product.m_deltaEtaTanHelIPrPVBS_2 = product.m_recoIPrPVBS_2.Eta() - product.m_recoIPHelrPVBS_2.Eta();
	product.m_deltaPhiTanHelIPrPVBS_2 = product.m_recoIPrPVBS_2.DeltaPhi(product.m_recoIPHelrPVBS_2);
	product.m_deltaRTanHelIPrPVBS_2 = product.m_recoIPrPVBS_2.DeltaR(product.m_recoIPHelrPVBS_2);
	product.m_deltaTanHelIPrPVBS_2 = product.m_recoIPrPVBS_2.Angle(product.m_recoIPHelrPVBS_2);

	if (!m_isData){
	  // calculate deltaR, deltaEta, deltaPhi and delta between recoIPvec and genIPvec
	  if(&product.m_genIP1 != nullptr && product.m_genIP1.x() != -999){
	    // wrt refitted PV
	    product.m_deltaEtaGenRecoIPrPV_1 = product.m_recoIPrPV_1.Eta() - product.m_genIP1.Eta();
	    product.m_deltaPhiGenRecoIPrPV_1 = product.m_recoIPrPV_1.DeltaPhi(product.m_genIP1);//product.m_recoIPrPV_1);//
	    product.m_deltaRGenRecoIPrPV_1   = product.m_recoIPrPV_1.DeltaR(product.m_genIP1);
	    product.m_deltaGenRecoIPrPV_1    = product.m_recoIPrPV_1.Angle(product.m_genIP1);//product.m_recoIPrPV_1);//

	    product.m_deltaEtaGenRecoIPHelrPV_1 = product.m_recoIPHelrPV_1.Eta() - product.m_genIP1.Eta();
	    product.m_deltaPhiGenRecoIPHelrPV_1 = product.m_recoIPHelrPV_1.DeltaPhi(product.m_genIP1);
	    product.m_deltaRGenRecoIPHelrPV_1   = product.m_recoIPHelrPV_1.DeltaR(product.m_genIP1);
	    product.m_deltaGenRecoIPHelrPV_1    = product.m_recoIPHelrPV_1.Angle(product.m_genIP1);

	    product.m_deltaEtaGenRecoIPrPVBS_1 = product.m_recoIPrPVBS_1.Eta() - product.m_genIP1.Eta();
	    product.m_deltaPhiGenRecoIPrPVBS_1 = product.m_recoIPrPVBS_1.DeltaPhi(product.m_genIP1);//product.m_recoIPrPV_1);//
	    product.m_deltaRGenRecoIPrPVBS_1   = product.m_recoIPrPVBS_1.DeltaR(product.m_genIP1);
	    product.m_deltaGenRecoIPrPVBS_1    = product.m_recoIPrPVBS_1.Angle(product.m_genIP1);//product.m_recoIPrPV_1);//

	    product.m_deltaEtaGenRecoIPHelrPVBS_1 = product.m_recoIPHelrPVBS_1.Eta() - product.m_genIP1.Eta();
	    product.m_deltaPhiGenRecoIPHelrPVBS_1 = product.m_recoIPHelrPVBS_1.DeltaPhi(product.m_genIP1);
	    product.m_deltaRGenRecoIPHelrPVBS_1   = product.m_recoIPHelrPVBS_1.DeltaR(product.m_genIP1);
	    product.m_deltaGenRecoIPHelrPVBS_1    = product.m_recoIPHelrPVBS_1.Angle(product.m_genIP1);
  
	  } // if genIP1 exists

	  if(&product.m_genIP2 != nullptr && product.m_genIP2.x() != -999){
	    // wrt refitted PV
	    product.m_deltaEtaGenRecoIPrPV_2 = product.m_recoIPrPV_2.Eta() - product.m_genIP2.Eta();
	    product.m_deltaPhiGenRecoIPrPV_2 = product.m_recoIPrPV_2.DeltaPhi(product.m_genIP2);
	    product.m_deltaRGenRecoIPrPV_2   = product.m_recoIPrPV_2.DeltaR(product.m_genIP2);
	    product.m_deltaGenRecoIPrPV_2    = product.m_recoIPrPV_2.Angle(product.m_genIP2);

	    product.m_deltaEtaGenRecoIPHelrPV_2 = product.m_recoIPHelrPV_2.Eta() - product.m_genIP2.Eta();
	    product.m_deltaPhiGenRecoIPHelrPV_2 = product.m_recoIPHelrPV_2.DeltaPhi(product.m_genIP2);
	    product.m_deltaRGenRecoIPHelrPV_2   = product.m_recoIPHelrPV_2.DeltaR(product.m_genIP2);
	    product.m_deltaGenRecoIPHelrPV_2    = product.m_recoIPHelrPV_2.Angle(product.m_genIP2);

	    product.m_deltaEtaGenRecoIPrPVBS_2 = product.m_recoIPrPVBS_2.Eta() - product.m_genIP2.Eta();
	    product.m_deltaPhiGenRecoIPrPVBS_2 = product.m_recoIPrPVBS_2.DeltaPhi(product.m_genIP2);//product.m_recoIPrPV_2);//
	    product.m_deltaRGenRecoIPrPVBS_2   = product.m_recoIPrPVBS_2.DeltaR(product.m_genIP2);
	    product.m_deltaGenRecoIPrPVBS_2    = product.m_recoIPrPVBS_2.Angle(product.m_genIP2);//product.m_recoIPrPV_2);//

	    product.m_deltaEtaGenRecoIPHelrPVBS_2 = product.m_recoIPHelrPVBS_2.Eta() - product.m_genIP2.Eta();
	    product.m_deltaPhiGenRecoIPHelrPVBS_2 = product.m_recoIPHelrPVBS_2.DeltaPhi(product.m_genIP2);
	    product.m_deltaRGenRecoIPHelrPVBS_2   = product.m_recoIPHelrPVBS_2.DeltaR(product.m_genIP2);
	    product.m_deltaGenRecoIPHelrPVBS_2    = product.m_recoIPHelrPVBS_2.Angle(product.m_genIP2);
	  } // if genIP2 exists
	} // if MC sample
	//<= FIXME: check if refitPV exists removed =>
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
					    RMFLV& piOSMomentum) const {

  //Reset 4-momenta
  piSSFromRhoMomentum.SetCoordinates(0,0,0,0);
  piOSMomentum.SetCoordinates(0,0,0,0);

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
  for (std::vector<KPFCandidate>::const_iterator candidate = tau->chargedHadronCandidates.begin();
       candidate != tau->chargedHadronCandidates.end(); ++candidate) {
    if (candidate->charge()*tau->charge()>0) {
      float deltaM = std::abs((candidate->p4+piOSMomentum).M()-DefaultValues::RhoMass);
      if (deltaM < minDeltaM) {
	piSSFromRhoMomentum = candidate->p4;
	minDeltaM = deltaM;
      }
    }
  }

  return (piOSMomentum.pt()> 0 && piSSFromRhoMomentum.pt()>0); //Sanity check
}
