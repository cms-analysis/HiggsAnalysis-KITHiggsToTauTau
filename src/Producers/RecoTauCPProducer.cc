
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"
#include "Artus/Utility/interface/UnitConverter.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/CPQuantities.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/ImpactParameter.h"
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

	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "nominalPV", [](event_type const& event, product_type const& product)
	{
		return event.m_vertexSummary->pv.position;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "nominalPVchi2", [](event_type const& event, product_type const& product)
	{
		return event.m_vertexSummary->pv.chi2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "nominalPVnDOF", [](event_type const& event, product_type const& product)
	{
		return event.m_vertexSummary->pv.nDOF;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "nominalPVnTracks", [](event_type const& event, product_type const& product)
	{
		return event.m_vertexSummary->pv.nTracks;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "nominalPVsigmaxx", [](event_type const& event, product_type const& product)
	{
		return event.m_vertexSummary->pv.covariance.At(0,0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "nominalPVsigmayy", [](event_type const& event, product_type const& product)
	{
		return event.m_vertexSummary->pv.covariance.At(1,1);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "nominalPVsigmazz", [](event_type const& event, product_type const& product)
	{
		return event.m_vertexSummary->pv.covariance.At(2,2);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "nominalPVsigmaxy", [](event_type const& event, product_type const& product)
	{
		return event.m_vertexSummary->pv.covariance.At(0,1);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "nominalPVsigmaxz", [](event_type const& event, product_type const& product)
	{
		return event.m_vertexSummary->pv.covariance.At(0,2);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "nominalPVsigmayz", [](event_type const& event, product_type const& product)
	{
		return event.m_vertexSummary->pv.covariance.At(1,2);
	});

	// BS coordinates and parameters
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "theBS", [](event_type const& event, product_type const& product)
	{
		return event.m_beamSpot->position;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "theBSsigmax", [](event_type const& event, product_type const& product)
	{
		return event.m_beamSpot->beamWidthX;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "theBSsigmay", [](event_type const& event, product_type const& product)
	{
		return event.m_beamSpot->beamWidthY;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "theBSsigmaz", [](event_type const& event, product_type const& product)
	{
		return event.m_beamSpot->sigmaZ;
	});

	// CP-related quantities
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCP", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCP;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPHel", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPHel;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPrPV", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPHelrPV", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPHelrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPrPVBS", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPHelrPVBS", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPHelrPVBS;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPRho", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPRho;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPRhoMerged", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPRhoMerged;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "reco_posyTauL", [](event_type const& event, product_type const& product)
	{
		return product.m_reco_posyTauL;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "reco_negyTauL", [](event_type const& event, product_type const& product)
	{
		return product.m_reco_negyTauL;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPComb", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPComb;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombMerged", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPCombMerged;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombHel", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPCombHel;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombMergedHel", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPCombMergedHel;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombrPV", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPCombrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombMergedrPV", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPCombMergedrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombHelrPV", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPCombHelrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombMergedHelrPV", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPCombMergedHelrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombrPVBS", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPCombrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombMergedrPVBS", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPCombMergedrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombHelrPVBS", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPCombHelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombMergedHelrPVBS", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPCombMergedHelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStar", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStar;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarRho", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarRho;
	});

	// azimuthal angles of the tau decay planes
	// ip method
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiPlusIPMeth", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiPlusIPMeth;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiMinusIPMeth", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiMinusIPMeth;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarPlusIPMeth", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarPlusIPMeth;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarMinusIPMeth", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarMinusIPMeth;
	});
	// comb method
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiPlusCombMeth", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiPlusCombMeth;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiMinusCombMeth", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiMinusCombMeth;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarPlusCombMeth", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarPlusCombMeth;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarMinusCombMeth", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarMinusCombMeth;
	});
	// rho method
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiPlusRhoMeth", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiPlusRhoMeth;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiMinusRhoMeth", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiMinusRhoMeth;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarPlusRhoMeth", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarPlusRhoMeth;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarMinusRhoMeth", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarMinusRhoMeth;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoChargedHadron1HiggsFrameEnergy", [](event_type const& event, product_type const& product)
	{
		return product.m_recoChargedHadronEnergies.first;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoChargedHadron2HiggsFrameEnergy", [](event_type const& event, product_type const& product)
	{
		return product.m_recoChargedHadronEnergies.second;
	});

	// Helix Paramters
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixRadius_1", [](event_type const& event, product_type const& product)
	{
		return product.m_Radius_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixRadius_2", [](event_type const& event, product_type const& product)
	{
		return product.m_Radius_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixQOverP_1", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0) ? (product.m_flavourOrderedLeptons.at(0)->track.helixParameters(event.m_beamSpot, 0)) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixLambda_1", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0) ? (product.m_flavourOrderedLeptons.at(0)->track.helixParameters(event.m_beamSpot, 1)) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixPhi_1", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0) ? (product.m_flavourOrderedLeptons.at(0)->track.helixParameters(event.m_beamSpot, 2)) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixDxy_1", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0) ? (product.m_flavourOrderedLeptons.at(0)->track.helixParameters(event.m_beamSpot, 3)) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixDsz_1", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0) ? (product.m_flavourOrderedLeptons.at(0)->track.helixParameters(event.m_beamSpot, 4)) : DefaultValues::UndefinedDouble;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixQOverP_2", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1) ? (product.m_flavourOrderedLeptons.at(1)->track.helixParameters(event.m_beamSpot, 0)) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixLambda_2", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1) ? (product.m_flavourOrderedLeptons.at(1)->track.helixParameters(event.m_beamSpot, 1)) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixPhi_2", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1) ? (product.m_flavourOrderedLeptons.at(1)->track.helixParameters(event.m_beamSpot, 2)) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixDxy_2", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1) ? (product.m_flavourOrderedLeptons.at(1)->track.helixParameters(event.m_beamSpot, 3)) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixDsz_2", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1) ? (product.m_flavourOrderedLeptons.at(1)->track.helixParameters(event.m_beamSpot, 4)) : DefaultValues::UndefinedDouble;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixRadius", [](event_type const& event, product_type const& product)
	{
		return product.m_HelixRadius;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoMagneticField", [](event_type const& event, product_type const& product)
	{
		return product.m_recoMagneticField;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoP_SI", [](event_type const& event, product_type const& product)
	{
		return product.m_recoP_SI;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoV_z_SI", [](event_type const& event, product_type const& product)
	{
		return product.m_recoV_z_SI;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoOmega", [](event_type const& event, product_type const& product)
	{
		return product.m_recoOmega;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhi1", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhi1;
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "recoOprime", [](event_type const& event, product_type const& product)
	{
		return product.m_recoOprime;
	});

	// impact parameters d0=dxy and dz
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "d0rPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_refitPV ? product.m_flavourOrderedLeptons.at(0)->track.getDxy(product.m_refitPV) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "d0rPVBS_1", [](event_type const& event, product_type const& product)
	{
		return product.m_refitPVBS ? product.m_flavourOrderedLeptons.at(0)->track.getDxy(product.m_refitPVBS) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "dZrPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_refitPV ? product.m_flavourOrderedLeptons.at(0)->track.getDz(product.m_refitPV) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "dZrPVBS_1", [](event_type const& event, product_type const& product)
	{
		return product.m_refitPVBS ? product.m_flavourOrderedLeptons.at(0)->track.getDz(product.m_refitPVBS) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "d0rPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_refitPV ? product.m_flavourOrderedLeptons.at(1)->track.getDxy(product.m_refitPV) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "d0rPVBS_2", [](event_type const& event, product_type const& product)
	{
		return product.m_refitPVBS ? product.m_flavourOrderedLeptons.at(1)->track.getDxy(product.m_refitPVBS) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "dZrPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_refitPV ? product.m_flavourOrderedLeptons.at(1)->track.getDz(product.m_refitPV) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "dZrPVBS_2", [](event_type const& event, product_type const& product)
	{
		return product.m_refitPVBS ? product.m_flavourOrderedLeptons.at(1)->track.getDz(product.m_refitPVBS) : DefaultValues::UndefinedDouble;
	});
//	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoImpactParameter1", [](event_type const& event, product_type const& product)
//	{
//		return product.m_recoIP1;
//	});
//	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoImpactParameter2", [](event_type const& event, product_type const& product)
//	{
//		return product.m_recoIP2;
//	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoTrackRefError1", [](event_type const& event, product_type const& product)
	{
		return product.m_recoTrackRefError1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoTrackRefError2", [](event_type const& event, product_type const& product)
	{
		return product.m_recoTrackRefError2;
	});

	// IP vectors wrt nominalPV
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "IP_1", [](event_type const& event, product_type const& product)
	{
		return (((product.m_recoIP1).x() != -999) ? RMPoint( (product.m_recoIP1).x(), (product.m_recoIP1).y(), (product.m_recoIP1).z() ) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "IP_2", [](event_type const& event, product_type const& product)
	{
		return (((product.m_recoIP2).x() != -999) ? RMPoint( (product.m_recoIP2).x(), (product.m_recoIP2).y(), (product.m_recoIP2).z() ) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificance_1", [](event_type const& event, product_type const& product)
	{
		return product.m_pca1DiffInSigma;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificance_2", [](event_type const& event, product_type const& product)
	{
		return product.m_pca2DiffInSigma;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIP_1", [](event_type const& event, product_type const& product)
	{
		return product.m_pca1proj;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIP_2", [](event_type const& event, product_type const& product)
	{
		return product.m_pca2proj;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPHel_1", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIPHel_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPHel_2", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIPHel_2;
	});

	// IP vectors wrt refitted PV
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "IPrPV_1", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPrPV_1) != nullptr) ? RMPoint( (product.m_recoIPrPV_1).x(), (product.m_recoIPrPV_1).y(), (product.m_recoIPrPV_1).z() ) : DefaultValues::UndefinedRMPoint;
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "IPrPV_2", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPrPV_2) != nullptr) ? RMPoint( (product.m_recoIPrPV_2).x(), (product.m_recoIPrPV_2).y(), (product.m_recoIPrPV_2).z() ) : DefaultValues::UndefinedRMPoint;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificancerPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_pca1DiffInSigmarPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificancerPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_pca2DiffInSigmarPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPHelrPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIPHelrPV_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPHelrPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIPHelrPV_2;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificancerPVBS_1", [](event_type const& event, product_type const& product)
	{
		return product.m_pca1DiffInSigmarPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificancerPVBS_2", [](event_type const& event, product_type const& product)
	{
		return product.m_pca2DiffInSigmarPVBS;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPrPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_pca1projrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPrPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_pca2projrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPrPVBS_1", [](event_type const& event, product_type const& product)
	{
		return product.m_pca1projrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPrPVBS_2", [](event_type const& event, product_type const& product)
	{
		return product.m_pca2projrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPHelrPVBS_1", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIPHelrPVBS_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "sigmaIPHelrPVBS_2", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIPHelrPVBS_2;
	});




	// IP vectors wrt refitted PV with BS constraint
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "IPrPVBS_1", [](event_type const& event, product_type const& product)
	{
		return (((product.m_recoIPrPVBS_1).x() != -999) ? RMPoint( (product.m_recoIPrPVBS_1).x(), (product.m_recoIPrPVBS_1).y(), (product.m_recoIPrPVBS_1).z() ) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "IPrPVBS_2", [](event_type const& event, product_type const& product)
	{
		return (((product.m_recoIPrPVBS_2).x() != -999) ? RMPoint( (product.m_recoIPrPVBS_2).x(), (product.m_recoIPrPVBS_2).y(), (product.m_recoIPrPVBS_2).z() ) : DefaultValues::UndefinedRMPoint);
	});
	// IP vectors wrt nominalPV with helical approach
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "IPHel_1", [](event_type const& event, product_type const& product)
	{
		return (((product.m_recoIPHel_1).x() != -999) ? RMPoint( (product.m_recoIPHel_1).x(), (product.m_recoIPHel_1).y(), (product.m_recoIPHel_1).z() ) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "IPHel_2", [](event_type const& event, product_type const& product)
	{
		return (((product.m_recoIPHel_2).x() != -999) ? RMPoint( (product.m_recoIPHel_2).x(), (product.m_recoIPHel_2).y(), (product.m_recoIPHel_2).z() ) : DefaultValues::UndefinedRMPoint);
	});

	//The elements of the covariance matrix from the IP with helical approach
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificanceHel_1", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_IPSignificanceHel_1!= nullptr) ? product.m_IPSignificanceHel_1 : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificanceHel_2", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_IPSignificanceHel_2!= nullptr) ? product.m_IPSignificanceHel_2 : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelCovxx_1", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPHelCovxx_1 != nullptr) ? (product.m_recoIPHelCovxx_1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelCovxy_1", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPHelCovxy_1 != nullptr) ? (product.m_recoIPHelCovxy_1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelCovxz_1", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPHelCovxz_1 != nullptr) ? (product.m_recoIPHelCovxz_1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelCovyy_1", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPHelCovyy_1 != nullptr) ? (product.m_recoIPHelCovyy_1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelCovyz_1", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPHelCovyz_1 != nullptr) ? (product.m_recoIPHelCovyz_1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelCovzz_1", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPHelCovzz_1 != nullptr) ? (product.m_recoIPHelCovzz_1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelCovxx_2", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPHelCovxx_2 != nullptr) ? (product.m_recoIPHelCovxx_2) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelCovxy_2", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPHelCovxy_2 != nullptr) ? (product.m_recoIPHelCovxy_2) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelCovxz_2", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPHelCovxz_2 != nullptr) ? (product.m_recoIPHelCovxz_2) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelCovyy_2", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPHelCovyy_2 != nullptr) ? (product.m_recoIPHelCovyy_2) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelCovyz_2", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPHelCovyz_2 != nullptr) ? (product.m_recoIPHelCovyz_2) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelCovzz_2", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPHelCovzz_2 != nullptr) ? (product.m_recoIPHelCovzz_2) : DefaultValues::UndefinedFloat);
	});

	// IP vectors wrt the refitted PV with helical approach
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "IPHelrPV_1", [](event_type const& event, product_type const& product)
	{
		return (((product.m_recoIPHelrPV_1).x() != -999) ? RMPoint( (product.m_recoIPHelrPV_1).x(), (product.m_recoIPHelrPV_1).y(), (product.m_recoIPHelrPV_1).z() ) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "IPHelrPV_2", [](event_type const& event, product_type const& product)
	{
		return (((product.m_recoIPHelrPV_2).x() != -999) ? RMPoint( (product.m_recoIPHelrPV_2).x(), (product.m_recoIPHelrPV_2).y(), (product.m_recoIPHelrPV_2).z() ) : DefaultValues::UndefinedRMPoint);
	});

	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "IPHelrPVBS_1", [](event_type const& event, product_type const& product)
	{
		return (((product.m_recoIPHelrPVBS_1).x() != -999) ? RMPoint( (product.m_recoIPHelrPVBS_1).x(), (product.m_recoIPHelrPVBS_1).y(), (product.m_recoIPHelrPVBS_1).z() ) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "IPHelrPVBS_2", [](event_type const& event, product_type const& product)
	{
		return (((product.m_recoIPHelrPVBS_2).x() != -999) ? RMPoint( (product.m_recoIPHelrPVBS_2).x(), (product.m_recoIPHelrPVBS_2).y(), (product.m_recoIPHelrPVBS_2).z() ) : DefaultValues::UndefinedRMPoint);
	});
	// Components
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificanceHelrPV_1", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_IPSignificanceHelrPV_1!= nullptr) ? product.m_IPSignificanceHelrPV_1 : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificanceHelrPV_2", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_IPSignificanceHelrPV_2!= nullptr) ? product.m_IPSignificanceHelrPV_2 : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelrPVCovxx_1", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPHelrPVCovxx_1 != nullptr) ? (product.m_recoIPHelrPVCovxx_1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelrPVCovxy_1", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPHelrPVCovxy_1 != nullptr) ? (product.m_recoIPHelrPVCovxy_1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelrPVCovxz_1", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPHelrPVCovxz_1 != nullptr) ? (product.m_recoIPHelrPVCovxz_1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelrPVCovyy_1", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPHelrPVCovyy_1 != nullptr) ? (product.m_recoIPHelrPVCovyy_1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelrPVCovyz_1", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPHelrPVCovyz_1 != nullptr) ? (product.m_recoIPHelrPVCovyz_1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelrPVCovzz_1", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPHelrPVCovzz_1 != nullptr) ? (product.m_recoIPHelrPVCovzz_1) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelrPVCovxx_2", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPHelrPVCovxx_2 != nullptr) ? (product.m_recoIPHelrPVCovxx_2) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelrPVCovxy_2", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPHelrPVCovxy_2 != nullptr) ? (product.m_recoIPHelrPVCovxy_2) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelrPVCovxz_2", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPHelrPVCovxz_2 != nullptr) ? (product.m_recoIPHelrPVCovxz_2) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelrPVCovyy_2", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPHelrPVCovyy_2 != nullptr) ? (product.m_recoIPHelrPVCovyy_2) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelrPVCovyz_2", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPHelrPVCovyz_2 != nullptr) ? (product.m_recoIPHelrPVCovyz_2) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIPHelrPVCovzz_2", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIPHelrPVCovzz_2 != nullptr) ? (product.m_recoIPHelrPVCovzz_2) : DefaultValues::UndefinedFloat);
	});


	// IP with helical approach, refitPV and BS
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificanceHelrPVBS_1", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_IPSignificanceHelrPVBS_1!= nullptr) ? product.m_IPSignificanceHelrPVBS_1 : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IPSignificanceHelrPVBS_2", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_IPSignificanceHelrPVBS_2!= nullptr) ? product.m_IPSignificanceHelrPVBS_2 : DefaultValues::UndefinedFloat);
	});

	// distance between track and theBS
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "trackFromBS_1", [](event_type const& event, product_type const& product)
	{
		return (((product.m_track1FromBS).x() != -999) ? RMPoint(product.m_track1FromBS.x(), product.m_track1FromBS.y(), product.m_track1FromBS.z()) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "trackFromBS_2", [](event_type const& event, product_type const& product)
	{
		return (((product.m_track2FromBS).x() != -999) ? RMPoint(product.m_track2FromBS.x(), product.m_track2FromBS.y(), product.m_track2FromBS.z()) : DefaultValues::UndefinedRMPoint);
	});

	// cosPsi
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "cosPsiPlus", [](event_type const& event, product_type const& product)
	{
		return product.m_cosPsiPlus;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "cosPsiMinus", [](event_type const& event, product_type const& product)
	{
		return product.m_cosPsiMinus;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "cosPsiPlus", [](event_type const& event, product_type const& product)
	{
		return product.m_cosPsiPlus;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "cosPsiMinus", [](event_type const& event, product_type const& product)
	{
		return product.m_cosPsiMinus;
	});

	// errors on dxy, dz and IP wrt nominalPV
	// using propagation of errors
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errD0_1_newErr", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP1vec.at(0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errDZ_1_newErr", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP1vec.at(1);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errIP_1", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP1vec.at(2);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errD0_2_newErr", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP2vec.at(0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errDZ_2_newErr", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP2vec.at(1);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errIP_2", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP2vec.at(2);
	});


	// errors on dxy, dz and IP wrt refitted PV
	// using propagation of errors
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errD0rPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP1vecrPV.at(0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errDZrPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP1vecrPV.at(1);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errIPrPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP1vecrPV.at(2);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errD0rPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP2vecrPV.at(0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errDZrPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP2vecrPV.at(1);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errIPrPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP2vecrPV.at(2);
	});


	// deltaEta, deltaPhi, deltaR and angle delta between genIP and recoIP(nominalPV)
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIP_1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaEtaGenRecoIP_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIP_2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaEtaGenRecoIP_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIP_1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaPhiGenRecoIP_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIP_2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaPhiGenRecoIP_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIP_1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaRGenRecoIP_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIP_2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaRGenRecoIP_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIP_1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaGenRecoIP_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIP_2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaGenRecoIP_2;
	});

	// deltaEta, deltaPhi, deltaR and angle delta between genIP and recoIPHel(nominalPV)
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIPHel_1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaEtaGenRecoIPHel_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIPHel_2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaEtaGenRecoIPHel_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIPHel_1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaPhiGenRecoIPHel_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIPHel_2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaPhiGenRecoIPHel_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIPHel_1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaRGenRecoIPHel_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIPHel_2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaRGenRecoIPHel_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIPHel_1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaGenRecoIPHel_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIPHel_2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaGenRecoIPHel_2;
	});

	// deltaEta, deltaPhi, deltaR and angle delta between genIP and recoIPHel(refitPV)
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIPHelrPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaEtaGenRecoIPHelrPV_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIPHelrPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaEtaGenRecoIPHelrPV_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIPHelrPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaPhiGenRecoIPHelrPV_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIPHelrPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaPhiGenRecoIPHelrPV_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIPHelrPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaRGenRecoIPHelrPV_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIPHelrPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaRGenRecoIPHelrPV_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIPHelrPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaGenRecoIPHelrPV_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIPHelrPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaGenRecoIPHelrPV_2;
	});

	// deltaEta, deltaPhi, deltaR and angle delta between genIP and recoIPHel(refitPVBS)
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIPHelrPVBS_1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaEtaGenRecoIPHelrPVBS_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIPHelrPVBS_2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaEtaGenRecoIPHelrPVBS_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIPHelrPVBS_1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaPhiGenRecoIPHelrPVBS_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIPHelrPVBS_2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaPhiGenRecoIPHelrPVBS_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIPHelrPVBS_1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaRGenRecoIPHelrPVBS_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIPHelrPVBS_2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaRGenRecoIPHelrPVBS_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIPHelrPVBS_1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaGenRecoIPHelrPVBS_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIPHelrPVBS_2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaGenRecoIPHelrPVBS_2;
	});


	// deltaEta, deltaPhi, deltaR and angle delta between genIP and recoIP(refitPV)
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIPrPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaEtaGenRecoIPrPV_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIPrPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaEtaGenRecoIPrPV_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIPrPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaPhiGenRecoIPrPV_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIPrPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaPhiGenRecoIPrPV_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIPrPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaRGenRecoIPrPV_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIPrPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaRGenRecoIPrPV_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIPrPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaGenRecoIPrPV_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIPrPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaGenRecoIPrPV_2;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "d0s_area", [](event_type const& event, product_type const& product)
	{
		return product.m_d0s_area;
	});

	// deltaEta, deltaPhi, deltaR and angle delta between genIP and recoIP(refitPVBS)
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIPrPVBS_1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaEtaGenRecoIPrPVBS_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIPrPVBS_2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaEtaGenRecoIPrPVBS_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIPrPVBS_1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaPhiGenRecoIPrPVBS_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIPrPVBS_2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaPhiGenRecoIPrPVBS_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIPrPVBS_1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaRGenRecoIPrPVBS_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIPrPVBS_2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaRGenRecoIPrPVBS_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIPrPVBS_1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaGenRecoIPrPVBS_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIPrPVBS_2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaGenRecoIPrPVBS_2;
	});


	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "d0s_dist", [](event_type const& event, product_type const& product)
	{
		return product.m_d0s_dist;
	});

	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "RefHelix_1", [](event_type const& event, product_type const& product)
	{
		return product.m_RefHelix_1;
	});

	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "RefHelix_2", [](event_type const& event, product_type const& product)
	{
		return product.m_RefHelix_2;
	});

	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "PHelix_1", [](event_type const& event, product_type const& product)
	{
		return product.m_PHelix_1;
	});

	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "PHelix_2", [](event_type const& event, product_type const& product)
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
	// rho-method
	// ----------
	RMFLV piZeroP = ((chargedPart1->flavour() == KLeptonFlavour::TAU) ? static_cast<KTau*>(chargedPart1)->piZeroMomentum() : DefaultValues::UndefinedRMFLV);
	RMFLV piZeroM = ((chargedPart2->flavour() == KLeptonFlavour::TAU) ? static_cast<KTau*>(chargedPart2)->piZeroMomentum() : DefaultValues::UndefinedRMFLV);


	double phiStarCPRho = cpq.CalculatePhiStarCPRho(momentumP, momentumM, piZeroP, piZeroM);
	double posyLRho = cpq.CalculateSpinAnalysingDiscriminantRho(momentumP, piZeroP);
	double negyLRho = cpq.CalculateSpinAnalysingDiscriminantRho(momentumM, piZeroM);
	// azimuthal angles of the tau decay planes
	product.m_recoPhiPlusRhoMeth = cpq.GetRecoPhiPlusRhoMeth();
	product.m_recoPhiMinusRhoMeth = cpq.GetRecoPhiMinusRhoMeth();
	product.m_recoPhiStarPlusRhoMeth = cpq.GetRecoPhiStarPlusRhoMeth();
	product.m_recoPhiStarMinusRhoMeth = cpq.GetRecoPhiStarMinusRhoMeth();

	product.m_recoPhiStarCPRho = phiStarCPRho;
	product.m_reco_posyTauL = posyLRho;
	product.m_reco_negyTauL = negyLRho;

	//fill additional variable to produce a merged phiStarCP plot with increased statistics
	if (posyLRho*negyLRho > 0) {
		product.m_recoPhiStarCPRhoMerged = phiStarCPRho;
	}
	else {
		if (phiStarCPRho > ROOT::Math::Pi()) {
		 product.m_recoPhiStarCPRhoMerged = phiStarCPRho - ROOT::Math::Pi();
		}
		else product.m_recoPhiStarCPRhoMerged = phiStarCPRho + ROOT::Math::Pi();
	}


	product.m_d0s_area = cpq.CalculateD0sArea((product.m_refitPV ? product.m_flavourOrderedLeptons.at(0)->track.getDxy(product.m_refitPV) : DefaultValues::UndefinedDouble), (product.m_refitPV ? product.m_flavourOrderedLeptons.at(1)->track.getDxy(product.m_refitPV) : DefaultValues::UndefinedDouble));

	product.m_d0s_dist = cpq.CalculateD0sDist((product.m_refitPV ? product.m_flavourOrderedLeptons.at(0)->track.getDxy(product.m_refitPV) : DefaultValues::UndefinedDouble), (product.m_refitPV ? product.m_flavourOrderedLeptons.at(1)->track.getDxy(product.m_refitPV) : DefaultValues::UndefinedDouble));

	// ---------
	// ip-method
	// ---------
	// phi*CP wrt nominalPV
	product.m_recoPhiStarCP = cpq.CalculatePhiStarCP(&(event.m_vertexSummary->pv), trackP, trackM, momentumP, momentumM);

	// calculation of the IP vectors and relative errors
	// IP wrt nominalPV
	product.m_recoIP1 = ip.CalculateShortestDistance(recoParticle1->p4, recoParticle1->track.ref, event.m_vertexSummary->pv.position);
	product.m_recoIP2 = ip.CalculateShortestDistance(recoParticle2->p4, recoParticle2->track.ref, event.m_vertexSummary->pv.position);
	// FIXME This is not needed anymore
	product.m_errorIP1vec = cpq.CalculateIPErrors(recoParticle1, &(event.m_vertexSummary->pv), &product.m_recoIP1);
	product.m_errorIP2vec = cpq.CalculateIPErrors(recoParticle2, &(event.m_vertexSummary->pv), &product.m_recoIP2);

	//Projection of Point of closest approach (PCA) to the primary vertex (PV) uncertainty ellipsoid
	product.m_pca1proj = ip.CalculatePCADifferece(event.m_vertexSummary->pv.covariance,product.m_recoIP1);
	product.m_pca2proj = ip.CalculatePCADifferece(event.m_vertexSummary->pv.covariance,product.m_recoIP2);
	//Distance of Point of closest approach (PCA) from the primary vertex (PV) in units of sigma_PV
	product.m_pca1DiffInSigma = product.m_recoIP1.Mag()/product.m_pca1proj;
	product.m_pca2DiffInSigma = product.m_recoIP2.Mag()/product.m_pca2proj;

	//Impact parameters via helical approach in cm:

	product.m_recoIPHel_1 = ip.CalculatePCA(product.m_flavourOrderedLeptons.at(0)->track.magneticField, product.m_flavourOrderedLeptons.at(0)->track.helixParameters(), product.m_flavourOrderedLeptons.at(0)->track.ref, event.m_vertexSummary->pv.position, recoParticle1->p4);
	product.m_recoIPHel_2 = ip.CalculatePCA(product.m_flavourOrderedLeptons.at(1)->track.magneticField, product.m_flavourOrderedLeptons.at(1)->track.helixParameters(), product.m_flavourOrderedLeptons.at(1)->track.ref, event.m_vertexSummary->pv.position, recoParticle2->p4);

	// IP Significance for the helical approach
	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IPHelCov_1 = ip.CalculatePCACovariance(product.m_flavourOrderedLeptons.at(0)->track.helixCovariance, event.m_vertexSummary->pv.covariance);
	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IPHelCov_2 = ip.CalculatePCACovariance(product.m_flavourOrderedLeptons.at(1)->track.helixCovariance, event.m_vertexSummary->pv.covariance);

	product.m_HelixRadius = ip.GetHelixRadius();
	product.m_recoMagneticField = ip.GetRecoMagneticField();
	product.m_recoV_z_SI = ip.GetRecoV_z_SI();
	product.m_recoOmega = ip.GetRecoOmega();
	product.m_recoPhi1 = ip.GetRecoPhi1();
	product.m_recoOprime = ip.GetRecoOprime();

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
	ROOT::Math::SVector<float, 3> IP1_(product.m_recoIPHel_1(0), product.m_recoIPHel_1(1), product.m_recoIPHel_1(2));
	ROOT::Math::SVector<float, 3> IP2_(product.m_recoIPHel_2(0), product.m_recoIPHel_2(1), product.m_recoIPHel_2(2));

	IP1_ = IP1_.Unit();
	IP2_ = IP2_.Unit();

	product.m_errorIPHel_1 = sqrt( ROOT::Math::Dot(IP1_, IPHelCov_1 * IP1_ ) );
	product.m_errorIPHel_2 = sqrt( ROOT::Math::Dot(IP2_, IPHelCov_2 * IP1_ ) );

	product.m_IPSignificanceHel_1 = product.m_recoIPHel_1.Mag() / product.m_errorIPHel_1;
	product.m_IPSignificanceHel_2 = product.m_recoIPHel_2.Mag() / product.m_errorIPHel_2;

	//product.m_IPSignificanceHel_1 = sqrt( (product.m_recoIPHel_1).x()*(product.m_recoIPHel_1).x() + (product.m_recoIPHel_1).y()*(product.m_recoIPHel_1).y() + (product.m_recoIPHel_1).z()*(product.m_recoIPHel_1).z() ) / sqrt( ROOT::Math::Dot(IP1_, IPHelCov_1 * IP1_ ) );
	//product.m_IPSignificanceHel_2 = sqrt( (product.m_recoIPHel_2).x()*(product.m_recoIPHel_2).x() + (product.m_recoIPHel_2).y()*(product.m_recoIPHel_2).y() + (product.m_recoIPHel_2).z()*(product.m_recoIPHel_2).z() ) / sqrt( ROOT::Math::Dot(IP2_, IPHelCov_2 * IP2_ ) );

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
	// comb-method
	// ---------
	// The combined method is possible if one tau_h->rho is present in the channel (i.e. et, mt, tt).
	// In the tt ch., we want to use the combined method when only one of the two taus decays to rho.
	// If both taus decay to rho, then the rho method is preferred.
	if ( product.m_decayChannel == HttEnumTypes::DecayChannel::MT || product.m_decayChannel == HttEnumTypes::DecayChannel::ET ){

		KTau* recoTau2 = static_cast<KTau*>(recoParticle2);
		product.m_recoPhiStarCPComb    = cpq.CalculatePhiStarCPComb(product.m_recoIP1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
		product.m_recoPhiStarCPCombHel = cpq.CalculatePhiStarCPComb(product.m_recoIPHel_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());

		product.m_recoPhiStarCPCombMerged    = cpq.MergePhiStarCPCombSemiLeptonic(product.m_recoPhiStarCPComb, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
		product.m_recoPhiStarCPCombMergedHel = cpq.MergePhiStarCPCombSemiLeptonic(product.m_recoPhiStarCPCombHel, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);

	}  // if et or mt ch.

	if ( product.m_decayChannel == HttEnumTypes::DecayChannel::TT ){
		KTau* recoTau1 = static_cast<KTau*>(recoParticle1);
		KTau* recoTau2 = static_cast<KTau*>(recoParticle2);

		// tau1->rho, tau2->a
		if (recoTau1->decayMode == 1 && recoTau2->decayMode != 1) {
			product.m_recoPhiStarCPComb    = cpq.CalculatePhiStarCPComb(product.m_recoIP2, recoParticle2->p4, recoTau1->chargedHadronCandidates.at(0).p4, recoTau1->piZeroMomentum(), recoParticle2->charge());
			product.m_recoPhiStarCPCombHel = cpq.CalculatePhiStarCPComb(product.m_recoIPHel_2, recoParticle2->p4, recoTau1->chargedHadronCandidates.at(0).p4, recoTau1->piZeroMomentum(), recoParticle2->charge());

			product.m_recoPhiStarCPCombMerged    = cpq.MergePhiStarCPCombFullyHadronic(product.m_recoPhiStarCPComb, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
			product.m_recoPhiStarCPCombMergedHel = cpq.MergePhiStarCPCombFullyHadronic(product.m_recoPhiStarCPCombHel, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
		} // tau1->rho, tau2->a

		// tau1->a, tau2->rho
		if (recoTau1->decayMode != 1 && recoTau2->decayMode ==1){
			product.m_recoPhiStarCPComb    = cpq.CalculatePhiStarCPComb(product.m_recoIP1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
			product.m_recoPhiStarCPCombHel = cpq.CalculatePhiStarCPComb(product.m_recoIPHel_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());

			product.m_recoPhiStarCPCombMerged = cpq.MergePhiStarCPCombFullyHadronic(product.m_recoPhiStarCPComb, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
			product.m_recoPhiStarCPCombMergedHel = cpq.MergePhiStarCPCombFullyHadronic(product.m_recoPhiStarCPCombHel, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
		} // tau1->a, tau2->rho

	}  // if tt ch.

	// Calculate the psi+- without a refitted vertex
	product.m_cosPsiPlus  = cpq.CalculateCosPsi(recoParticle1->p4, product.m_recoIP1);
	product.m_cosPsiMinus = cpq.CalculateCosPsi(recoParticle2->p4, product.m_recoIP2);

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

	if (product.m_refitPV != nullptr){

		// IP wrt refitPV
		// FIXME the errorIP1vecrPV is not used anymore
		product.m_recoIPrPV_1 = ip.CalculateShortestDistance(recoParticle1->p4, recoParticle1->track.ref, product.m_refitPV->position);
		product.m_recoIPrPV_2 = ip.CalculateShortestDistance(recoParticle2->p4, recoParticle2->track.ref, product.m_refitPV->position);
		product.m_errorIP1vecrPV = cpq.CalculateIPErrors(recoParticle1, product.m_refitPV, &product.m_recoIPrPV_1);
		product.m_errorIP2vecrPV = cpq.CalculateIPErrors(recoParticle2, product.m_refitPV, &product.m_recoIPrPV_2);

		product.m_recoIPrPVBS_1 = ip.CalculateShortestDistance(recoParticle1->p4, recoParticle1->track.ref, product.m_refitPVBS->position);
		product.m_recoIPrPVBS_2 = ip.CalculateShortestDistance(recoParticle2->p4, recoParticle2->track.ref, product.m_refitPVBS->position);
		product.m_errorIP1vecrPVBS = cpq.CalculateIPErrors(recoParticle1, product.m_refitPVBS, &product.m_recoIPrPV_1);
		product.m_errorIP2vecrPVBS = cpq.CalculateIPErrors(recoParticle2, product.m_refitPVBS, &product.m_recoIPrPV_2);

		//Projection of Point of closest approach (PCA) to the primary vertex (PV) uncertainty ellipsoid
		product.m_pca1projrPV = ip.CalculatePCADifferece(product.m_refitPV->covariance,product.m_recoIPrPV_1);
		product.m_pca2projrPV = ip.CalculatePCADifferece(product.m_refitPV->covariance,product.m_recoIPrPV_2);
		//Distance of Point of closest approach (PCA) from the primary vertex (PV) in units of sigma_PV
		product.m_pca1DiffInSigmarPV = sqrt( product.m_recoIPrPV_1 * product.m_recoIPrPV_1 )/product.m_pca1projrPV;
		product.m_pca2DiffInSigmarPV = sqrt( product.m_recoIPrPV_2 * product.m_recoIPrPV_2 )/product.m_pca2projrPV;
		//Projection of Point of closest approach (PCA) to the primary vertex (PV) uncertainty ellipsoid
		product.m_pca1projrPVBS = ip.CalculatePCADifferece(product.m_refitPVBS->covariance,product.m_recoIPrPVBS_1);
		product.m_pca2projrPVBS = ip.CalculatePCADifferece(product.m_refitPVBS->covariance,product.m_recoIPrPVBS_2);
		//Distance of Point of closest approach (PCA) from the primary vertex (PV) with BS constraint in units of sigma_PV
		product.m_pca1DiffInSigmarPVBS = sqrt( product.m_recoIPrPVBS_1 * product.m_recoIPrPVBS_1 )/product.m_pca1projrPVBS;
		product.m_pca2DiffInSigmarPVBS = sqrt( product.m_recoIPrPVBS_2 * product.m_recoIPrPVBS_2 )/product.m_pca2projrPVBS;
		//Impact parameters via helical approach in cm:

		product.m_recoIPHelrPV_1 = ip.CalculatePCA(product.m_flavourOrderedLeptons.at(0)->track.magneticField, product.m_flavourOrderedLeptons.at(0)->track.helixParameters(), product.m_flavourOrderedLeptons.at(0)->track.ref, product.m_refitPV->position, recoParticle1->p4);
		product.m_recoIPHelrPV_2 = ip.CalculatePCA(product.m_flavourOrderedLeptons.at(1)->track.magneticField, product.m_flavourOrderedLeptons.at(1)->track.helixParameters(), product.m_flavourOrderedLeptons.at(1)->track.ref, product.m_refitPV->position, recoParticle2->p4);

		ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IPHelrPVCov_1 = ip.CalculatePCACovariance(product.m_flavourOrderedLeptons.at(0)->track.helixCovariance, product.m_refitPV->covariance);
		ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IPHelrPVCov_2 = ip.CalculatePCACovariance(product.m_flavourOrderedLeptons.at(1)->track.helixCovariance, product.m_refitPV->covariance);

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

		product.m_recoIPHelrPVBS_1 = ip.CalculatePCA(product.m_flavourOrderedLeptons.at(0)->track.magneticField, product.m_flavourOrderedLeptons.at(0)->track.helixParameters(), product.m_flavourOrderedLeptons.at(0)->track.ref, product.m_refitPVBS->position, recoParticle1->p4);
		product.m_recoIPHelrPVBS_2 = ip.CalculatePCA(product.m_flavourOrderedLeptons.at(1)->track.magneticField, product.m_flavourOrderedLeptons.at(1)->track.helixParameters(), product.m_flavourOrderedLeptons.at(1)->track.ref, product.m_refitPVBS->position, recoParticle2->p4);

		ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IPHelrPVBSCov_1 = ip.CalculatePCACovariance(product.m_flavourOrderedLeptons.at(0)->track.helixCovariance, product.m_refitPVBS->covariance);
		ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IPHelrPVBSCov_2 = ip.CalculatePCACovariance(product.m_flavourOrderedLeptons.at(1)->track.helixCovariance, product.m_refitPVBS->covariance);
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

		product.m_errorIPHelrPVBS_1 = sqrt( ROOT::Math::Dot(IPrPVBS_1_, IPHelrPVBSCov_1 * IP1_ ) );
		product.m_errorIPHelrPVBS_2 = sqrt( ROOT::Math::Dot(IPrPVBS_2_, IPHelrPVBSCov_2 * IP2_ ) );

		product.m_IPSignificanceHelrPVBS_1 = product.m_recoIPHelrPVBS_1.Mag() / product.m_errorIPHelrPVBS_1;
		product.m_IPSignificanceHelrPVBS_2 = product.m_recoIPHelrPVBS_2.Mag() / product.m_errorIPHelrPVBS_2;

		// calculate cosPsi
		if (recoParticle1->charge() == +1){
			product.m_cosPsiPlus  = cpq.CalculateCosPsi(recoParticle1->p4, product.m_recoIPrPV_1);
			product.m_cosPsiMinus = cpq.CalculateCosPsi(recoParticle2->p4, product.m_recoIPrPV_2);
		} else {
			product.m_cosPsiPlus  = cpq.CalculateCosPsi(recoParticle2->p4, product.m_recoIPrPV_2);
			product.m_cosPsiMinus = cpq.CalculateCosPsi(recoParticle1->p4, product.m_recoIPrPV_1);
		}

		// calculate phi*cp using the refitted PV
		// FIXME two functions are called, need to remove one of the two
		// in this case, the ipvectors are calculated within the CalculatePhiStarCP functions
		product.m_recoPhiStarCPrPV = cpq.CalculatePhiStarCP(product.m_refitPV, trackP, trackM, momentumP, momentumM);
		product.m_recoPhiStarCPrPVBS = cpq.CalculatePhiStarCP(product.m_refitPVBS, trackP, trackM, momentumP, momentumM);

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
		product.m_recoPhiStarCPrPV   = cpq.CalculatePhiStarCP(product.m_refitPV, trackP, trackM, momentumP, momentumM);
		product.m_recoPhiStarCPrPVBS = cpq.CalculatePhiStarCP(product.m_refitPVBS, trackP, trackM, momentumP, momentumM);

		// ---------
		// comb-method - with refitted PV
		// ---------
		if ( product.m_decayChannel == HttEnumTypes::DecayChannel::MT || product.m_decayChannel == HttEnumTypes::DecayChannel::ET ){
			KTau* recoTau2 = static_cast<KTau*>(recoParticle2);

			product.m_recoPhiStarCPCombrPV      = cpq.CalculatePhiStarCPComb(product.m_recoIPrPV_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
			product.m_recoPhiStarCPCombrPVBS    = cpq.CalculatePhiStarCPComb(product.m_recoIPrPVBS_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
			product.m_recoPhiStarCPCombHelrPV   = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPV_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
			product.m_recoPhiStarCPCombHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPVBS_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());

			product.m_recoPhiStarCPCombMergedrPV      = cpq.MergePhiStarCPCombSemiLeptonic(product.m_recoPhiStarCPCombrPV, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
			product.m_recoPhiStarCPCombMergedrPVBS    = cpq.MergePhiStarCPCombSemiLeptonic(product.m_recoPhiStarCPCombrPVBS, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
			product.m_recoPhiStarCPCombMergedHelrPV   = cpq.MergePhiStarCPCombSemiLeptonic(product.m_recoPhiStarCPCombHelrPV, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
			product.m_recoPhiStarCPCombMergedHelrPVBS = cpq.MergePhiStarCPCombSemiLeptonic(product.m_recoPhiStarCPCombHelrPVBS, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
		}
		if ( product.m_decayChannel == HttEnumTypes::DecayChannel::TT ){
			KTau* recoTau1 = static_cast<KTau*>(recoParticle1);
			KTau* recoTau2 = static_cast<KTau*>(recoParticle2);
			// tau1->rho, tau2->a
			if (recoTau1->decayMode == 1 && recoTau2->decayMode != 1) {
				product.m_recoPhiStarCPCombrPV    = cpq.CalculatePhiStarCPComb(product.m_recoIPrPV_2, recoParticle2->p4, recoTau1->chargedHadronCandidates.at(0).p4, recoTau1->piZeroMomentum(), recoParticle2->charge());
				product.m_recoPhiStarCPCombrPVBS  = cpq.CalculatePhiStarCPComb(product.m_recoIPrPVBS_2, recoParticle2->p4, recoTau1->chargedHadronCandidates.at(0).p4, recoTau1->piZeroMomentum(), recoParticle2->charge());
				product.m_recoPhiStarCPCombHelrPV = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPV_2, recoParticle2->p4, recoTau1->chargedHadronCandidates.at(0).p4, recoTau1->piZeroMomentum(), recoParticle2->charge());
				product.m_recoPhiStarCPCombHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPVBS_2, recoParticle2->p4, recoTau1->chargedHadronCandidates.at(0).p4, recoTau1->piZeroMomentum(), recoParticle2->charge());

				product.m_recoPhiStarCPCombMergedrPV      = cpq.MergePhiStarCPCombFullyHadronic(product.m_recoPhiStarCPCombrPV, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
				product.m_recoPhiStarCPCombMergedrPVBS    = cpq.MergePhiStarCPCombFullyHadronic(product.m_recoPhiStarCPCombrPVBS, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
				product.m_recoPhiStarCPCombMergedHelrPV   = cpq.MergePhiStarCPCombFullyHadronic(product.m_recoPhiStarCPCombHelrPV, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
				product.m_recoPhiStarCPCombMergedHelrPVBS = cpq.MergePhiStarCPCombFullyHadronic(product.m_recoPhiStarCPCombHelrPVBS, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
			}
			// tau1->a, tau2->rho
			if (recoTau1->decayMode != 1 && recoTau2->decayMode ==1){
				product.m_recoPhiStarCPCombrPV      = cpq.CalculatePhiStarCPComb(product.m_recoIPrPV_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
				product.m_recoPhiStarCPCombrPVBS    = cpq.CalculatePhiStarCPComb(product.m_recoIPrPVBS_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
				product.m_recoPhiStarCPCombHelrPV   = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPV_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
				product.m_recoPhiStarCPCombHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPVBS_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());

				product.m_recoPhiStarCPCombMergedrPV      = cpq.MergePhiStarCPCombFullyHadronic(product.m_recoPhiStarCPCombrPV, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
				product.m_recoPhiStarCPCombMergedrPVBS    = cpq.MergePhiStarCPCombFullyHadronic(product.m_recoPhiStarCPCombrPVBS, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
				product.m_recoPhiStarCPCombMergedHelrPV   = cpq.MergePhiStarCPCombFullyHadronic(product.m_recoPhiStarCPCombHelrPV, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
				product.m_recoPhiStarCPCombMergedHelrPVBS = cpq.MergePhiStarCPCombFullyHadronic(product.m_recoPhiStarCPCombHelrPVBS, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
			}

		}  // if tt ch.

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
	} // if the refitPV exists
}
