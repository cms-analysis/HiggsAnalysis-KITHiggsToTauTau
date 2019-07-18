
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"
#include "Artus/Utility/interface/UnitConverter.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/CPQuantities.h"
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

	// thePV coordinates and parameters
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "thePVx", [](event_type const& event, product_type const& product)
	{
		return event.m_vertexSummary->pv.position.x();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "thePVy", [](event_type const& event, product_type const& product)
	{
		return event.m_vertexSummary->pv.position.y();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "thePVz", [](event_type const& event, product_type const& product)
	{
		return event.m_vertexSummary->pv.position.z();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "thePVchi2", [](event_type const& event, product_type const& product)
	{
		return event.m_vertexSummary->pv.chi2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "thePVnDOF", [](event_type const& event, product_type const& product)
	{
		return event.m_vertexSummary->pv.nDOF;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "thePVnTracks", [](event_type const& event, product_type const& product)
	{
		return event.m_vertexSummary->pv.nTracks;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "thePVsigmaxx", [](event_type const& event, product_type const& product)
	{
		return event.m_vertexSummary->pv.covariance.At(0,0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "thePVsigmayy", [](event_type const& event, product_type const& product)
	{
		return event.m_vertexSummary->pv.covariance.At(1,1);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "thePVsigmazz", [](event_type const& event, product_type const& product)
	{
		return event.m_vertexSummary->pv.covariance.At(2,2);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "thePVsigmaxy", [](event_type const& event, product_type const& product)
	{
		return event.m_vertexSummary->pv.covariance.At(0,1);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "thePVsigmaxz", [](event_type const& event, product_type const& product)
	{
		return event.m_vertexSummary->pv.covariance.At(0,2);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "thePVsigmayz", [](event_type const& event, product_type const& product)
	{
		return event.m_vertexSummary->pv.covariance.At(1,2);
	});

	// BS coordinates and parameters
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "theBSx", [](event_type const& event, product_type const& product)
	{
		return event.m_beamSpot->position.x();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "theBSy", [](event_type const& event, product_type const& product)
	{
		return event.m_beamSpot->position.y();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "theBSz", [](event_type const& event, product_type const& product)
	{
		return event.m_beamSpot->position.z();
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

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCP_rho", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCP_rho;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCP_rho_merged", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCP_rho_merged;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "reco_posyTauL", [](event_type const& event, product_type const& product)
	{
		return product.m_reco_posyTauL;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "reco_negyTauL", [](event_type const& event, product_type const& product)
	{
		return product.m_reco_negyTauL;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPrPV", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPrPV;
	});
	//LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPrPV2", [](event_type const& event, product_type const& product)
	//{
	//	return product.m_recoPhiStarCPrPV2;
	//});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPComb", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPComb;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombMerged", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPCombMerged;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombMergedBS", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPCombMergedBS;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPComb_norefit", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPComb_norefit;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombMerged_norefit", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPCombMerged_norefit;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPComb_norefit_helical", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPComb_norefit_helical;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombMerged_norefit_helical", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPCombMerged_norefit_helical;
	});


	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCP_helical", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCP_helical;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPrPV_helical", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPrPV_helical;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPComb_helical", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPComb_helical;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPCombMerged_helical", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPCombMerged_helical;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarCPrPVBS", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPrPVBS;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStar", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStar;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStar_rho", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStar_rho;
	});

	// azimuthal angles of the tau decay planes
	// ip method
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiPlus_ipmeth", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiPlus_ipmeth;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiMinus_ipmeth", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiMinus_ipmeth;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarPlus_ipmeth", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarPlus_ipmeth;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarMinus_ipmeth", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarMinus_ipmeth;
	});
	// comb method
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiPlus_combmeth", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiPlus_combmeth;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiMinus_combmeth", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiMinus_combmeth;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarPlus_combmeth", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarPlus_combmeth;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarMinus_combmeth", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarMinus_combmeth;
	});
	// rho method
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiPlus_rhometh", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiPlus_rhometh;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiMinus_rhometh", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiMinus_rhometh;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarPlus_rhometh", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarPlus_rhometh;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoPhiStarMinus_rhometh", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarMinus_rhometh;
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
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixQOverP_1", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0) ? (product.m_flavourOrderedLeptons.at(0)->track.helixParameters())[0] : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixLambda_1", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0) ? (product.m_flavourOrderedLeptons.at(0)->track.helixParameters())[1] : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixPhi_1", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0) ? (product.m_flavourOrderedLeptons.at(0)->track.helixParameters())[2] : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixDxy_1", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0) ? (product.m_flavourOrderedLeptons.at(0)->track.helixParameters())[3] : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixDsz_1", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(0) ? (product.m_flavourOrderedLeptons.at(0)->track.helixParameters())[4] : DefaultValues::UndefinedDouble;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixQOverP_2", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1) ? (product.m_flavourOrderedLeptons.at(1)->track.helixParameters())[0] : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixLambda_2", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1) ? (product.m_flavourOrderedLeptons.at(1)->track.helixParameters())[1] : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixPhi_2", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1) ? (product.m_flavourOrderedLeptons.at(1)->track.helixParameters())[2] : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixDxy_2", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1) ? (product.m_flavourOrderedLeptons.at(1)->track.helixParameters())[3] : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "helixDsz_2", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons.at(1) ? (product.m_flavourOrderedLeptons.at(1)->track.helixParameters())[4] : DefaultValues::UndefinedDouble;
	});


	// impact parameters d0=dxy and dz
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "d0_refitPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_refitPV ? product.m_flavourOrderedLeptons.at(0)->track.getDxy(product.m_refitPV) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "d0_refitPVBS_1", [](event_type const& event, product_type const& product)
	{
		return product.m_refitPVBS ? product.m_flavourOrderedLeptons.at(0)->track.getDxy(product.m_refitPVBS) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "dZ_refitPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_refitPV ? product.m_flavourOrderedLeptons.at(0)->track.getDz(product.m_refitPV) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "dZ_refitPVBS_1", [](event_type const& event, product_type const& product)
	{
		return product.m_refitPVBS ? product.m_flavourOrderedLeptons.at(0)->track.getDz(product.m_refitPVBS) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "d0_refitPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_refitPV ? product.m_flavourOrderedLeptons.at(1)->track.getDxy(product.m_refitPV) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "d0_refitPVBS_2", [](event_type const& event, product_type const& product)
	{
		return product.m_refitPVBS ? product.m_flavourOrderedLeptons.at(1)->track.getDxy(product.m_refitPVBS) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "dZ_refitPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_refitPV ? product.m_flavourOrderedLeptons.at(1)->track.getDz(product.m_refitPV) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "dZ_refitPVBS_2", [](event_type const& event, product_type const& product)
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

	// IP vectors wrt thePV
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_1mag", [](event_type const& event, product_type const& product)
	{
		return (((product.m_recoIP1).x() != -999) ? ( sqrt( (product.m_recoIP1).x()*(product.m_recoIP1).x() + (product.m_recoIP1).y()*(product.m_recoIP1).y() + (product.m_recoIP1).z()*(product.m_recoIP1).z() ) ) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_1x", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1 != nullptr) ? (product.m_recoIP1).x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_1y", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1 != nullptr) ? (product.m_recoIP1).y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_1z", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1 != nullptr) ? (product.m_recoIP1).z() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_2mag", [](event_type const& event, product_type const& product)
	{
		return (((product.m_recoIP2).x() != -999) ? ( sqrt( (product.m_recoIP2).x()*(product.m_recoIP2).x() + (product.m_recoIP2).y()*(product.m_recoIP2).y() + (product.m_recoIP2).z()*(product.m_recoIP2).z() ) ) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_2x", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2 != nullptr) ? (product.m_recoIP2).x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_2y", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2 != nullptr) ? (product.m_recoIP2).y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_2z", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2 != nullptr) ? (product.m_recoIP2).z() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "thePVdistanceToPCA1", [](event_type const& event, product_type const& product)
	{
		return product.m_pca1DiffInSigma;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "thePVdistanceToPCA2", [](event_type const& event, product_type const& product)
	{
		return product.m_pca2DiffInSigma;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "thePCA1projToPVellipsoid", [](event_type const& event, product_type const& product)
	{
		return product.m_pca1proj;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "thePCA2projToPVellipsoid", [](event_type const& event, product_type const& product)
	{
		return product.m_pca2proj;
	});

	// IP vectors wrt refitted PV
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_refitPV_1mag", [](event_type const& event, product_type const& product)
	{
		return (((product.m_recoIP1_refitPV).x() != -999) ? ( sqrt( (product.m_recoIP1_refitPV).x()*(product.m_recoIP1_refitPV).x() + (product.m_recoIP1_refitPV).y()*(product.m_recoIP1_refitPV).y() + (product.m_recoIP1_refitPV).z()*(product.m_recoIP1_refitPV).z() ) ) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_refitPV_1x", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_refitPV != nullptr) ? (product.m_recoIP1_refitPV).x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_refitPV_1y", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_refitPV != nullptr) ? (product.m_recoIP1_refitPV).y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_refitPV_1z", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_refitPV != nullptr) ? (product.m_recoIP1_refitPV).z() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_refitPV_2mag", [](event_type const& event, product_type const& product)
	{
		return (((product.m_recoIP2_refitPV).x() != -999) ? ( sqrt( (product.m_recoIP2_refitPV).x()*(product.m_recoIP2_refitPV).x() + (product.m_recoIP2_refitPV).y()*(product.m_recoIP2_refitPV).y() + (product.m_recoIP2_refitPV).z()*(product.m_recoIP2_refitPV).z() ) ) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_refitPV_2x", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_refitPV != nullptr) ? (product.m_recoIP2_refitPV).x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_refitPV_2y", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_refitPV != nullptr) ? (product.m_recoIP2_refitPV).y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_refitPV_2z", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_refitPV != nullptr) ? (product.m_recoIP2_refitPV).z() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "thePVdistanceToPCA1_refitPV", [](event_type const& event, product_type const& product)
	{
		return product.m_pca1DiffInSigma_refitPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "thePVdistanceToPCA2_refitPV", [](event_type const& event, product_type const& product)
	{
		return product.m_pca2DiffInSigma_refitPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "thePCA1projToPVellipsoid_refitPV", [](event_type const& event, product_type const& product)
	{
		return product.m_pca1proj_refitPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "thePCA2projToPVellipsoid_refitPV", [](event_type const& event, product_type const& product)
	{
		return product.m_pca2proj_refitPV;
	});

	// IP vectors wrt refitted PV with BS constraint
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_refitPVBS_1mag", [](event_type const& event, product_type const& product)
	{
		return (((product.m_recoIP1_refitPVBS).x() != -999) ? ( sqrt( (product.m_recoIP1_refitPVBS).x()*(product.m_recoIP1_refitPVBS).x() + (product.m_recoIP1_refitPVBS).y()*(product.m_recoIP1_refitPVBS).y() + (product.m_recoIP1_refitPVBS).z()*(product.m_recoIP1_refitPVBS).z() ) ) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_refitPVBS_1x", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_refitPVBS != nullptr) ? (product.m_recoIP1_refitPVBS).x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_refitPVBS_1y", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_refitPVBS != nullptr) ? (product.m_recoIP1_refitPVBS).y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_refitPVBS_1z", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_refitPVBS != nullptr) ? (product.m_recoIP1_refitPVBS).z() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_refitPVBS_2mag", [](event_type const& event, product_type const& product)
	{
		return (((product.m_recoIP2_refitPVBS).x() != -999) ? ( sqrt( (product.m_recoIP2_refitPVBS).x()*(product.m_recoIP2_refitPVBS).x() + (product.m_recoIP2_refitPVBS).y()*(product.m_recoIP2_refitPVBS).y() + (product.m_recoIP2_refitPVBS).z()*(product.m_recoIP2_refitPVBS).z() ) ) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_refitPVBS_2x", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_refitPVBS != nullptr) ? (product.m_recoIP2_refitPVBS).x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_refitPVBS_2y", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_refitPVBS != nullptr) ? (product.m_recoIP2_refitPVBS).y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_refitPVBS_2z", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_refitPVBS != nullptr) ? (product.m_recoIP2_refitPVBS).z() : DefaultValues::UndefinedFloat);
	});

	// IP vectors wrt thePV with helical approach
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_helical_1mag", [](event_type const& event, product_type const& product)
	{
		return (((product.m_recoIP1_helical).x() != -999) ? ( sqrt( (product.m_recoIP1_helical).x()*(product.m_recoIP1_helical).x() + (product.m_recoIP1_helical).y()*(product.m_recoIP1_helical).y() + (product.m_recoIP1_helical).z()*(product.m_recoIP1_helical).z() ) ) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_helical_1x", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_helical != nullptr) ? (product.m_recoIP1_helical).x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_helical_1y", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_helical != nullptr) ? (product.m_recoIP1_helical).y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_helical_1z", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_helical != nullptr) ? (product.m_recoIP1_helical).z() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_helical_2mag", [](event_type const& event, product_type const& product)
	{
		return (((product.m_recoIP2_helical).x() != -999) ? ( sqrt( (product.m_recoIP2_helical).x()*(product.m_recoIP2_helical).x() + (product.m_recoIP2_helical).y()*(product.m_recoIP2_helical).y() + (product.m_recoIP2_helical).z()*(product.m_recoIP2_helical).z() ) ) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_helical_2x", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_helical != nullptr) ? (product.m_recoIP2_helical).x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_helical_2y", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_helical != nullptr) ? (product.m_recoIP2_helical).y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_helical_2z", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_helical != nullptr) ? (product.m_recoIP2_helical).z() : DefaultValues::UndefinedFloat);
	});

	//The elements of the covariance matrix from the IP with helical approach
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP1MagPerSig", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_IP1MagPerSig!= nullptr) ? product.m_IP1MagPerSig : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP2MagPerSig", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_IP2MagPerSig!= nullptr) ? product.m_IP2MagPerSig : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIP1_helicalCovxx", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_helicalCovxx != nullptr) ? (product.m_recoIP1_helicalCovxx) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIP1_helicalCovxy", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_helicalCovxy != nullptr) ? (product.m_recoIP1_helicalCovxy) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIP1_helicalCovxz", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_helicalCovxz != nullptr) ? (product.m_recoIP1_helicalCovxz) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIP1_helicalCovyy", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_helicalCovyy != nullptr) ? (product.m_recoIP1_helicalCovyy) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIP1_helicalCovyz", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_helicalCovyz != nullptr) ? (product.m_recoIP1_helicalCovyz) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIP1_helicalCovzz", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_helicalCovzz != nullptr) ? (product.m_recoIP1_helicalCovzz) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIP2_helicalCovxx", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_helicalCovxx != nullptr) ? (product.m_recoIP2_helicalCovxx) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIP2_helicalCovxy", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_helicalCovxy != nullptr) ? (product.m_recoIP2_helicalCovxy) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIP2_helicalCovxz", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_helicalCovxz != nullptr) ? (product.m_recoIP2_helicalCovxz) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIP2_helicalCovyy", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_helicalCovyy != nullptr) ? (product.m_recoIP2_helicalCovyy) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIP2_helicalCovyz", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_helicalCovyz != nullptr) ? (product.m_recoIP2_helicalCovyz) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIP2_helicalCovzz", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_helicalCovzz != nullptr) ? (product.m_recoIP2_helicalCovzz) : DefaultValues::UndefinedFloat);
	});

	// IP vectors wrt the refitted PV with helical approach
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_helical_refitPV_1mag", [](event_type const& event, product_type const& product)
	{
		return (((product.m_recoIP1_helical_refitPV).x() != -999) ? ( sqrt( (product.m_recoIP1_helical_refitPV).x()*(product.m_recoIP1_helical_refitPV).x() + (product.m_recoIP1_helical_refitPV).y()*(product.m_recoIP1_helical_refitPV).y() + (product.m_recoIP1_helical_refitPV).z()*(product.m_recoIP1_helical_refitPV).z() ) ) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_helical_refitPV_1x", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_helical_refitPV != nullptr) ? (product.m_recoIP1_helical_refitPV).x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_helical_refitPV_1y", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_helical_refitPV != nullptr) ? (product.m_recoIP1_helical_refitPV).y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_helical_refitPV_1z", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_helical_refitPV != nullptr) ? (product.m_recoIP1_helical_refitPV).z() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_helical_refitPV_2mag", [](event_type const& event, product_type const& product)
	{
		return (((product.m_recoIP2_helical_refitPV).x() != -999) ? ( sqrt( (product.m_recoIP2_helical_refitPV).x()*(product.m_recoIP2_helical_refitPV).x() + (product.m_recoIP2_helical_refitPV).y()*(product.m_recoIP2_helical_refitPV).y() + (product.m_recoIP2_helical_refitPV).z()*(product.m_recoIP2_helical_refitPV).z() ) ) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_helical_refitPV_2x", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_helical_refitPV != nullptr) ? (product.m_recoIP2_helical_refitPV).x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_helical_refitPV_2y", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_helical_refitPV != nullptr) ? (product.m_recoIP2_helical_refitPV).y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP_helical_refitPV_2z", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_helical_refitPV != nullptr) ? (product.m_recoIP2_helical_refitPV).z() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP1MagPerSigrPV", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_IP1MagPerSigrPV!= nullptr) ? product.m_IP1MagPerSigrPV : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "IP2MagPerSigrPV", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_IP2MagPerSigrPV!= nullptr) ? product.m_IP2MagPerSigrPV : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIP1_helical_refitPVCovxx", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_helical_refitPVCovxx != nullptr) ? (product.m_recoIP1_helical_refitPVCovxx) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIP1_helical_refitPVCovxy", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_helical_refitPVCovxy != nullptr) ? (product.m_recoIP1_helical_refitPVCovxy) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIP1_helical_refitPVCovxz", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_helical_refitPVCovxz != nullptr) ? (product.m_recoIP1_helical_refitPVCovxz) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIP1_helical_refitPVCovyy", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_helical_refitPVCovyy != nullptr) ? (product.m_recoIP1_helical_refitPVCovyy) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIP1_helical_refitPVCovyz", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_helical_refitPVCovyz != nullptr) ? (product.m_recoIP1_helical_refitPVCovyz) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIP1_helical_refitPVCovzz", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_helical_refitPVCovzz != nullptr) ? (product.m_recoIP1_helical_refitPVCovzz) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIP2_helical_refitPVCovxx", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_helical_refitPVCovxx != nullptr) ? (product.m_recoIP2_helical_refitPVCovxx) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIP2_helical_refitPVCovxy", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_helical_refitPVCovxy != nullptr) ? (product.m_recoIP2_helical_refitPVCovxy) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIP2_helical_refitPVCovxz", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_helical_refitPVCovxz != nullptr) ? (product.m_recoIP2_helical_refitPVCovxz) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIP2_helical_refitPVCovyy", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_helical_refitPVCovyy != nullptr) ? (product.m_recoIP2_helical_refitPVCovyy) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIP2_helical_refitPVCovyz", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_helical_refitPVCovyz != nullptr) ? (product.m_recoIP2_helical_refitPVCovyz) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "recoIP2_helical_refitPVCovzz", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_helical_refitPVCovzz != nullptr) ? (product.m_recoIP2_helical_refitPVCovzz) : DefaultValues::UndefinedFloat);
	});

	// distance between track and theBS
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "trackFromBS_1mag", [](event_type const& event, product_type const& product)
	{
		return (((product.m_track1FromBS).x() != -999) ? ( sqrt( (product.m_track1FromBS).x()*(product.m_track1FromBS).x() + (product.m_track1FromBS).y()*(product.m_track1FromBS).y() + (product.m_track1FromBS).z()*(product.m_track1FromBS).z() ) ) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "trackFromBS_1x", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_track1FromBS != nullptr) ? (product.m_track1FromBS).x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "trackFromBS_1y", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_track1FromBS != nullptr) ? (product.m_track1FromBS).y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "trackFromBS_1z", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_track1FromBS != nullptr) ? (product.m_track1FromBS).z() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "trackFromBS_2mag", [](event_type const& event, product_type const& product)
	{
		return (((product.m_track2FromBS).x() != -999) ? ( sqrt( (product.m_track2FromBS).x()*(product.m_track2FromBS).x() + (product.m_track2FromBS).y()*(product.m_track2FromBS).y() + (product.m_track2FromBS).z()*(product.m_track2FromBS).z() ) ) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "trackFromBS_2x", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_track2FromBS != nullptr) ? (product.m_track2FromBS).x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "trackFromBS_2y", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_track2FromBS != nullptr) ? (product.m_track2FromBS).y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "trackFromBS_2z", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_track2FromBS != nullptr) ? (product.m_track2FromBS).z() : DefaultValues::UndefinedFloat);
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
		return product.m_cosPsiPlus_norefit;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "cosPsiMinus", [](event_type const& event, product_type const& product)
	{
		return product.m_cosPsiMinus_norefit;
	});

	// errors on dxy, dz and IP wrt thePV
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
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errD0_refitPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP1vec_refitPV.at(0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errDZ_refitPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP1vec_refitPV.at(1);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errIP_refitPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP1vec_refitPV.at(2);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errD0_refitPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP2vec_refitPV.at(0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errDZ_refitPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP2vec_refitPV.at(1);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errIP_refitPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP2vec_refitPV.at(2);
	});


	// deltaEta, deltaPhi, deltaR and angle delta between genIP and recoIP(thePV)
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIP1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaEtaGenRecoIP1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIP2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaEtaGenRecoIP2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIP1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaPhiGenRecoIP1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIP2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaPhiGenRecoIP2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIP1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaRGenRecoIP1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIP2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaRGenRecoIP2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIP1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaGenRecoIP1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIP2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaGenRecoIP2;
	});

	// deltaEta, deltaPhi, deltaR and angle delta between genIP and recoIP_helical(thePV)
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIP1_helical", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaEtaGenRecoIP1_helical;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIP2_helical", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaEtaGenRecoIP2_helical;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIP1_helical", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaPhiGenRecoIP1_helical;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIP2_helical", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaPhiGenRecoIP2_helical;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIP1_helical", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaRGenRecoIP1_helical;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIP2_helical", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaRGenRecoIP2_helical;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIP1_helical", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaGenRecoIP1_helical;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIP2_helical", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaGenRecoIP2_helical;
	});

	// deltaEta, deltaPhi, deltaR and angle delta between genIP and recoIP_helical(refitPV)
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIP1_helical_refitPV", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaEtaGenRecoIP1_helical_refitPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIP2_helical_refitPV", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaEtaGenRecoIP2_helical_refitPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIP1_helical_refitPV", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaPhiGenRecoIP1_helical_refitPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIP2_helical_refitPV", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaPhiGenRecoIP2_helical_refitPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIP1_helical_refitPV", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaRGenRecoIP1_helical_refitPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIP2_helical_refitPV", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaRGenRecoIP2_helical_refitPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIP1_helical_refitPV", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaGenRecoIP1_helical_refitPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIP2_helical_refitPV", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaGenRecoIP2_helical_refitPV;
	});

	// deltaEta, deltaPhi, deltaR and angle delta between genIP and recoIP(refitPV)
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIP1_refitPV", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaEtaGenRecoIP1_refitPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaEtaGenRecoIP2_refitPV", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaEtaGenRecoIP2_refitPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIP1_refitPV", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaPhiGenRecoIP1_refitPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaPhiGenRecoIP2_refitPV", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaPhiGenRecoIP2_refitPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIP1_refitPV", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaRGenRecoIP1_refitPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaRGenRecoIP2_refitPV", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaRGenRecoIP2_refitPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIP1_refitPV", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaGenRecoIP1_refitPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "deltaGenRecoIP2_refitPV", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaGenRecoIP2_refitPV;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "d0s_area", [](event_type const& event, product_type const& product)
	{
		return product.m_d0s_area;
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
	product.m_recoIP1_refitPV.SetXYZ(-999,-999,-999);
	product.m_recoIP2_refitPV.SetXYZ(-999,-999,-999);
	TVector3 IPPlus;
	TVector3 IPMinus;
	TVector3 IPPlus_helical;
	TVector3 IPMinus_helical;
	IPPlus.SetXYZ(-999,-999,-999);
	IPMinus.SetXYZ(-999,-999,-999);

	// reconstructed leptons
	KLepton* recoParticle1 = product.m_flavourOrderedLeptons.at(0);
	KLepton* recoParticle2 = product.m_flavourOrderedLeptons.at(1);
	KLepton* chargedPart1  = product.m_chargeOrderedLeptons.at(0);
	KLepton* chargedPart2  = product.m_chargeOrderedLeptons.at(1);

	// Defining CPQuantities object to use variables and functions of this class
	CPQuantities cpq;

	// quantitites needed for calculation of recoPhiStarCP
	KTrack trackP = chargedPart1->track; // in case of tau_h, the track of the lead. prong is saved in the KTau track member
	KTrack trackM = chargedPart2->track;
	RMFLV momentumP = ((chargedPart1->flavour() == KLeptonFlavour::TAU) ? static_cast<KTau*>(chargedPart1)->chargedHadronCandidates.at(0).p4 : chargedPart1->p4);
	RMFLV momentumM = ((chargedPart2->flavour() == KLeptonFlavour::TAU) ? static_cast<KTau*>(chargedPart2)->chargedHadronCandidates.at(0).p4 : chargedPart2->p4);

	// ----------
	// rho-method
	// ----------
	RMFLV piZeroP = ((chargedPart1->flavour() == KLeptonFlavour::TAU) ? static_cast<KTau*>(chargedPart1)->piZeroMomentum() : DefaultValues::UndefinedRMFLV);
	RMFLV piZeroM = ((chargedPart2->flavour() == KLeptonFlavour::TAU) ? static_cast<KTau*>(chargedPart2)->piZeroMomentum() : DefaultValues::UndefinedRMFLV);


	double phiStarCP_rho = cpq.CalculatePhiStarCP_rho(momentumP, momentumM, piZeroP, piZeroM);
	double posyL_rho = cpq.CalculateSpinAnalysingDiscriminant_rho(momentumP, piZeroP);
	double negyL_rho = cpq.CalculateSpinAnalysingDiscriminant_rho(momentumM, piZeroM);
	// azimuthal angles of the tau decay planes
	product.m_recoPhiPlus_rhometh = cpq.GetRecoPhiPlus_rhometh();
	product.m_recoPhiMinus_rhometh = cpq.GetRecoPhiMinus_rhometh();
	product.m_recoPhiStarPlus_rhometh = cpq.GetRecoPhiStarPlus_rhometh();
	product.m_recoPhiStarMinus_rhometh = cpq.GetRecoPhiStarMinus_rhometh();

	product.m_recoPhiStarCP_rho = phiStarCP_rho;
	product.m_reco_posyTauL = posyL_rho;
	product.m_reco_negyTauL = negyL_rho;

	//fill additional variable to produce a merged phiStarCP plot with increased statistics
	if (posyL_rho*negyL_rho > 0) {
		product.m_recoPhiStarCP_rho_merged = phiStarCP_rho;
	}
	else {
		if (phiStarCP_rho > ROOT::Math::Pi()) {
		 product.m_recoPhiStarCP_rho_merged = phiStarCP_rho - ROOT::Math::Pi();
		}
		else product.m_recoPhiStarCP_rho_merged = phiStarCP_rho + ROOT::Math::Pi();
	}


	product.m_d0s_area = cpq.CalculateD0sArea((product.m_refitPV ? product.m_flavourOrderedLeptons.at(0)->track.getDxy(product.m_refitPV) : DefaultValues::UndefinedDouble), (product.m_refitPV ? product.m_flavourOrderedLeptons.at(1)->track.getDxy(product.m_refitPV) : DefaultValues::UndefinedDouble));

	product.m_d0s_dist = cpq.CalculateD0sDist((product.m_refitPV ? product.m_flavourOrderedLeptons.at(0)->track.getDxy(product.m_refitPV) : DefaultValues::UndefinedDouble), (product.m_refitPV ? product.m_flavourOrderedLeptons.at(1)->track.getDxy(product.m_refitPV) : DefaultValues::UndefinedDouble));

	// ---------
	// ip-method
	// ---------
	// phi*CP wrt thePV
	// FIXME is it still needed?
	product.m_recoPhiStarCP = cpq.CalculatePhiStarCP(&(event.m_vertexSummary->pv), trackP, trackM, momentumP, momentumM);

	// calculation of the IP vectors and relative errors
	// IP wrt thePV
	product.m_recoIP1 = cpq.CalculateShortestDistance(recoParticle1, event.m_vertexSummary->pv.position);
	product.m_recoIP2 = cpq.CalculateShortestDistance(recoParticle2, event.m_vertexSummary->pv.position);
	product.m_errorIP1vec = cpq.CalculateIPErrors(recoParticle1, &(event.m_vertexSummary->pv), &product.m_recoIP1);
	product.m_errorIP2vec = cpq.CalculateIPErrors(recoParticle2, &(event.m_vertexSummary->pv), &product.m_recoIP2);

	//Projection of Point of closest approach (PCA) to the primary vertex (PV) uncertainty ellipsoid
	product.m_pca1proj = cpq.CalculatePCADifferece(event.m_vertexSummary->pv.covariance,product.m_recoIP1);
	product.m_pca2proj = cpq.CalculatePCADifferece(event.m_vertexSummary->pv.covariance,product.m_recoIP2);
	//Distance of Point of closest approach (PCA) from the primary vertex (PV) in units of sigma_PV
	product.m_pca1DiffInSigma = product.m_recoIP1.Mag()/product.m_pca1proj;
	product.m_pca2DiffInSigma = product.m_recoIP2.Mag()/product.m_pca2proj;

	double scalar_product = 0.0; //to study whether the tangent and the radial part are orthogonal
	double xBest1 = 0.0;
	double xBest2 = 0.0;
	//Impact parameters via helical approach in cm:
	product.m_recoIP1_helical = cpq.CalculatePCA(product.m_flavourOrderedLeptons.at(0)->track.magneticField,product.m_flavourOrderedLeptons.at(0)->track.charge,product.m_flavourOrderedLeptons.at(0)->track.helixParameters(),product.m_flavourOrderedLeptons.at(0)->track.helixCovariance, product.m_RefHelix_1,event.m_vertexSummary->pv.position, false, &scalar_product,recoParticle1 , &xBest1);
	product.m_recoIP2_helical = cpq.CalculatePCA(product.m_flavourOrderedLeptons.at(1)->track.magneticField,product.m_flavourOrderedLeptons.at(1)->track.charge,product.m_flavourOrderedLeptons.at(1)->track.helixParameters(),product.m_flavourOrderedLeptons.at(1)->track.helixCovariance, product.m_RefHelix_2,event.m_vertexSummary->pv.position, false, &scalar_product,recoParticle2, &xBest2);

	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IP1HelixCov = cpq.CalculatePCACovariance(product.m_flavourOrderedLeptons.at(0)->track.magneticField,product.m_flavourOrderedLeptons.at(0)->track.charge,product.m_flavourOrderedLeptons.at(0)->track.helixParameters(),product.m_flavourOrderedLeptons.at(0)->track.helixCovariance, product.m_RefHelix_1,event.m_vertexSummary->pv.position, event.m_vertexSummary->pv.covariance, xBest1);
	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IP2HelixCov = cpq.CalculatePCACovariance(product.m_flavourOrderedLeptons.at(1)->track.magneticField,product.m_flavourOrderedLeptons.at(1)->track.charge,product.m_flavourOrderedLeptons.at(1)->track.helixParameters(),product.m_flavourOrderedLeptons.at(1)->track.helixCovariance, product.m_RefHelix_2,event.m_vertexSummary->pv.position, event.m_vertexSummary->pv.covariance, xBest2);

	product.m_recoIP1_helicalCovxx = IP1HelixCov(0,0);
	product.m_recoIP1_helicalCovxy = IP1HelixCov(0,1);
	product.m_recoIP1_helicalCovxz = IP1HelixCov(0,2);
	product.m_recoIP1_helicalCovyy = IP1HelixCov(1,1);
	product.m_recoIP1_helicalCovyz = IP1HelixCov(1,2);
	product.m_recoIP1_helicalCovzz = IP1HelixCov(2,2);

	product.m_recoIP2_helicalCovxx = IP2HelixCov(0,0);
	product.m_recoIP2_helicalCovxy = IP2HelixCov(0,1);
	product.m_recoIP2_helicalCovxz = IP2HelixCov(0,2);
	product.m_recoIP2_helicalCovyy = IP2HelixCov(1,1);
	product.m_recoIP2_helicalCovyz = IP2HelixCov(1,2);
	product.m_recoIP2_helicalCovzz = IP2HelixCov(2,2);


	ROOT::Math::SVector<float, 3> IP1_(product.m_recoIP1_helical(0), product.m_recoIP1_helical(1), product.m_recoIP1_helical(2)); // Conversion from TVector3 to SVector
	IP1_ /= sqrt((ROOT::Math::Dot(IP1_, IP1_))); // Normalize
	ROOT::Math::SVector<float, 3> IP2_(product.m_recoIP2_helical(0), product.m_recoIP2_helical(1), product.m_recoIP2_helical(2));
	IP2_ /= sqrt((ROOT::Math::Dot(IP2_, IP2_)));

	product.m_IP1MagPerSig = sqrt( (product.m_recoIP1_helical).x()*(product.m_recoIP1_helical).x() + (product.m_recoIP1_helical).y()*(product.m_recoIP1_helical).y() + (product.m_recoIP1_helical).z()*(product.m_recoIP1_helical).z() ) / sqrt( ROOT::Math::Dot(IP1_, IP1HelixCov * IP1_ ) );
	product.m_IP2MagPerSig = sqrt( (product.m_recoIP2_helical).x()*(product.m_recoIP2_helical).x() + (product.m_recoIP2_helical).y()*(product.m_recoIP2_helical).y() + (product.m_recoIP2_helical).z()*(product.m_recoIP2_helical).z() ) / sqrt( ROOT::Math::Dot(IP2_, IP2HelixCov * IP2_ ) );

	// Testing: Calculate some interesting values
	double qOverP_1     = (product.m_flavourOrderedLeptons.at(0)->track.helixParameters())[0];
	double lambda_1     = (product.m_flavourOrderedLeptons.at(0)->track.helixParameters())[1];
	double phi_1        = (product.m_flavourOrderedLeptons.at(0)->track.helixParameters())[2];
	double dxy_1        = (product.m_flavourOrderedLeptons.at(0)->track.helixParameters())[3];
	double dsz_1        = (product.m_flavourOrderedLeptons.at(0)->track.helixParameters())[4];
	double mass_1       = recoParticle1->p4.mass();
	double B_1          = product.m_flavourOrderedLeptons.at(0)->track.magneticField;
	int    sgnQ_1       = qOverP_1/TMath::Abs(qOverP_1);
	double omegaHelix_1 = B_1 * UnitConverter::eQ * sqrt( pow(UnitConverter::c, 2) * pow(mass_1, 2) / ( pow(UnitConverter::c, 2) * pow(mass_1, 2) + pow(sgnQ_1/qOverP_1,2) ) ) / mass_1;
	double Omega_1      = qOverP_1*B_1*UnitConverter::c;

	double qOverP_2     = (product.m_flavourOrderedLeptons.at(1)->track.helixParameters())[0];
	double lambda_2     = (product.m_flavourOrderedLeptons.at(1)->track.helixParameters())[1];
	double phi_2        = (product.m_flavourOrderedLeptons.at(1)->track.helixParameters())[2];
	double dxy_2        = (product.m_flavourOrderedLeptons.at(1)->track.helixParameters())[3];
	double dsz_2        = (product.m_flavourOrderedLeptons.at(1)->track.helixParameters())[4];
	double mass_2       = recoParticle2->p4.mass();
	double B_2          = product.m_flavourOrderedLeptons.at(1)->track.magneticField;
	int    sgnQ_2       = qOverP_2/TMath::Abs(qOverP_2);
	double omegaHelix_2 = B_2 * UnitConverter::eQ * sqrt( pow(UnitConverter::c, 2) * pow(mass_2, 2) / ( pow(UnitConverter::c, 2) * pow(mass_2, 2) + pow(sgnQ_2/qOverP_2,2) ) ) / mass_2;
	double Omega_2      = qOverP_2*B_2*UnitConverter::c;

	//TVector3 PHelix_1;
	product.m_PHelix_1.SetXYZ(TMath::Cos(lambda_1) * TMath::Cos(phi_1) * sgnQ_1 / qOverP_1,
			TMath::Cos(lambda_1) * TMath::Sin(phi_1) * sgnQ_1 / qOverP_1,
			TMath::Sin(lambda_1) * sgnQ_1 / qOverP_1);

	//TVector3 PHelix_2;
	product.m_PHelix_2.SetXYZ(TMath::Cos(lambda_2) * TMath::Cos(phi_2) * sgnQ_2 / qOverP_2,
			TMath::Cos(lambda_2) * TMath::Sin(phi_2) * sgnQ_2 / qOverP_2,
			TMath::Sin(lambda_2) * sgnQ_2 / qOverP_2);

	//TVector3 RefHelix_1;
	product.m_RefHelix_1.SetXYZ(-dsz_1 * TMath::Cos(phi_1) * TMath::Sin(lambda_1) - dxy_1 * TMath::Sin(phi_1),
			 dxy_1 * TMath::Cos(phi_1) - dsz_1 * TMath::Sin(lambda_1) * TMath::Sin(phi_1),
			 dsz_1 * TMath::Cos(lambda_1) );

	//TVector3 RefHelix_2;
	product.m_RefHelix_2.SetXYZ(-dsz_2 * TMath::Cos(phi_2) * TMath::Sin(lambda_2) - dxy_2 * TMath::Sin(phi_2),
			 dxy_2 * TMath::Cos(phi_2) - dsz_2 * TMath::Sin(lambda_2) * TMath::Sin(phi_2),
			 dsz_2 * TMath::Cos(lambda_2) );

	// distance between track and BS center
	product.m_track1FromBS = cpq.CalculateShortestDistance(recoParticle1, event.m_beamSpot->position);
	product.m_track2FromBS = cpq.CalculateShortestDistance(recoParticle2, event.m_beamSpot->position);


	// ---------
	// comb-method
	// ---------
	// The combined method is possible if one tau_h->rho is present in the channel (i.e. et, mt, tt).
	// In the tt ch., we want to use the combined method when only one of the two taus decays to rho.
	// If both taus decay to rho, then the rho method is preferred.
	if ( product.m_decayChannel == HttEnumTypes::DecayChannel::MT || product.m_decayChannel == HttEnumTypes::DecayChannel::ET ){

		KTau* recoTau2 = static_cast<KTau*>(recoParticle2);
		product.m_recoPhiStarCPComb_norefit       = cpq.CalculatePhiStarCPComb(product.m_recoIP1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
		product.m_recoPhiStarCPCombMerged_norefit = cpq.MergePhiStarCPCombSemiLeptonic(product.m_recoPhiStarCPComb_norefit, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);

		product.m_recoPhiStarCPComb_norefit_helical       = cpq.CalculatePhiStarCPComb(product.m_recoIP1_helical, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
		product.m_recoPhiStarCPCombMerged_norefit_helical = cpq.MergePhiStarCPCombSemiLeptonic(product.m_recoPhiStarCPComb_norefit_helical, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);

	}  // if et or mt ch.

	if ( product.m_decayChannel == HttEnumTypes::DecayChannel::TT ){
		KTau* recoTau1 = static_cast<KTau*>(recoParticle1);
		KTau* recoTau2 = static_cast<KTau*>(recoParticle2);

		// tau1->rho, tau2->a
		if (recoTau1->decayMode == 1 && recoTau2->decayMode != 1) {
			product.m_recoPhiStarCPComb_norefit       = cpq.CalculatePhiStarCPComb(product.m_recoIP2, recoParticle2->p4, recoTau1->chargedHadronCandidates.at(0).p4, recoTau1->piZeroMomentum(), recoParticle2->charge());
			product.m_recoPhiStarCPCombMerged_norefit = cpq.MergePhiStarCPCombFullyHadronic(product.m_recoPhiStarCPComb_norefit, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);

			product.m_recoPhiStarCPComb_norefit_helical       = cpq.CalculatePhiStarCPComb(product.m_recoIP2_helical, recoParticle2->p4, recoTau1->chargedHadronCandidates.at(0).p4, recoTau1->piZeroMomentum(), recoParticle2->charge());
			product.m_recoPhiStarCPCombMerged_norefit_helical = cpq.MergePhiStarCPCombFullyHadronic(product.m_recoPhiStarCPComb_norefit_helical, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
		} // tau1->rho, tau2->a

		// tau1->a, tau2->rho
		if (recoTau1->decayMode != 1 && recoTau2->decayMode ==1){
			product.m_recoPhiStarCPComb_norefit       = cpq.CalculatePhiStarCPComb(product.m_recoIP1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
			product.m_recoPhiStarCPCombMerged_norefit = cpq.MergePhiStarCPCombFullyHadronic(product.m_recoPhiStarCPComb_norefit, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);

			product.m_recoPhiStarCPComb_norefit_helical       = cpq.CalculatePhiStarCPComb(product.m_recoIP1_helical, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
			product.m_recoPhiStarCPCombMerged_norefit_helical = cpq.MergePhiStarCPCombFullyHadronic(product.m_recoPhiStarCPComb_norefit_helical, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
		} // tau1->a, tau2->rho

	}  // if tt ch.

	// Calculate the psi+- without a refitted vertex
	product.m_cosPsiPlus_norefit  = cpq.CalculateCosPsi(recoParticle1->p4, product.m_recoIP1);
	product.m_cosPsiMinus_norefit = cpq.CalculateCosPsi(recoParticle2->p4, product.m_recoIP2);

	// Calculate the phi*cp by taking the ipvectors from the helical approach as arguments
	if (recoParticle1->getHash() == chargedPart1->getHash()){
		IPPlus_helical  = product.m_recoIP1_helical;
		IPMinus_helical = product.m_recoIP2_helical;
	} else {
		IPPlus_helical  = product.m_recoIP2_helical;
		IPMinus_helical = product.m_recoIP1_helical;
	}
	product.m_recoPhiStarCP_helical = cpq.CalculatePhiStarCP(momentumP, momentumM, IPPlus_helical, IPMinus_helical, "reco");

	if(&product.m_genIP1 != nullptr && product.m_genIP1.x() != -999){
		//with the tangential approach
		product.m_deltaEtaGenRecoIP1 = product.m_recoIP1.Eta() - product.m_genIP1.Eta();
		product.m_deltaPhiGenRecoIP1 = product.m_recoIP1.DeltaPhi(product.m_genIP1);
		product.m_deltaRGenRecoIP1   = product.m_recoIP1.DeltaR(product.m_genIP1);
		product.m_deltaGenRecoIP1    = product.m_recoIP1.Angle(product.m_genIP1);

		//with the helical approach
		product.m_deltaEtaGenRecoIP1_helical = product.m_recoIP1_helical.Eta() - product.m_genIP1.Eta();
		product.m_deltaPhiGenRecoIP1_helical = product.m_recoIP1_helical.DeltaPhi(product.m_genIP1);//product.m_recoIP1);//
		product.m_deltaRGenRecoIP1_helical   = product.m_recoIP1_helical.DeltaR(product.m_genIP1);
		product.m_deltaGenRecoIP1_helical    = product.m_recoIP1_helical.Angle(product.m_genIP1);//product.m_recoIP1);//
	} // if genIP1 exists
	if(&product.m_genIP2 != nullptr && product.m_genIP2.x() != -999){
		product.m_deltaEtaGenRecoIP2 = product.m_recoIP2.Eta() - product.m_genIP2.Eta();
		product.m_deltaPhiGenRecoIP2 = product.m_recoIP2.DeltaPhi(product.m_genIP2);
		product.m_deltaRGenRecoIP2   = product.m_recoIP2.DeltaR(product.m_genIP2);
		product.m_deltaGenRecoIP2    = product.m_recoIP2.Angle(product.m_genIP2);

		product.m_deltaEtaGenRecoIP2_helical = product.m_recoIP2_helical.Eta() - product.m_genIP2.Eta();
		product.m_deltaPhiGenRecoIP2_helical = product.m_recoIP2_helical.DeltaPhi(product.m_genIP2);
		product.m_deltaRGenRecoIP2_helical   = product.m_recoIP2_helical.DeltaR(product.m_genIP2);
		product.m_deltaGenRecoIP2_helical    = product.m_recoIP2_helical.Angle(product.m_genIP2);
	} // if genIP2 exists

	if (product.m_refitPV != nullptr){

		// IP wrt refitPV
		product.m_recoIP1_refitPV = cpq.CalculateShortestDistance(recoParticle1, product.m_refitPV->position);
		product.m_recoIP2_refitPV = cpq.CalculateShortestDistance(recoParticle2, product.m_refitPV->position);
		product.m_errorIP1vec_refitPV = cpq.CalculateIPErrors(recoParticle1, product.m_refitPV, &product.m_recoIP1_refitPV);
		product.m_errorIP2vec_refitPV = cpq.CalculateIPErrors(recoParticle2, product.m_refitPV, &product.m_recoIP2_refitPV);

		product.m_recoIP1_refitPVBS = cpq.CalculateShortestDistance(recoParticle1, product.m_refitPVBS->position);
		product.m_recoIP2_refitPVBS = cpq.CalculateShortestDistance(recoParticle2, product.m_refitPVBS->position);
		product.m_errorIP1vec_refitPVBS = cpq.CalculateIPErrors(recoParticle1, product.m_refitPVBS, &product.m_recoIP1_refitPV);
		product.m_errorIP2vec_refitPVBS = cpq.CalculateIPErrors(recoParticle2, product.m_refitPVBS, &product.m_recoIP2_refitPV);

		//Projection of Point of closest approach (PCA) to the primary vertex (PV) uncertainty ellipsoid
		product.m_pca1proj_refitPV = cpq.CalculatePCADifferece(product.m_refitPV->covariance,product.m_recoIP1_refitPV);
		product.m_pca2proj_refitPV = cpq.CalculatePCADifferece(product.m_refitPV->covariance,product.m_recoIP2_refitPV);
		//Distance of Point of closest approach (PCA) from the primary vertex (PV) in units of sigma_PV
		product.m_pca1DiffInSigma_refitPV = product.m_recoIP1_refitPV.Mag()/product.m_pca1proj_refitPV;
		product.m_pca2DiffInSigma_refitPV = product.m_recoIP2_refitPV.Mag()/product.m_pca2proj_refitPV;

		//Impact parameters via helical approach in cm:
		xBest1 = -999;
		xBest2 = -999;
		// product.m_recoIP1_helical_refitPV = cpq.CalculatePCA(product.m_flavourOrderedLeptons.at(0)->track.magneticField,product.m_flavourOrderedLeptons.at(0)->track.charge,product.m_flavourOrderedLeptons.at(0)->track.helixParameters(),product.m_flavourOrderedLeptons.at(0)->track.helixCovariance, product.m_flavourOrderedLeptons.at(0)->track.ref,product.m_refitPV->position, false, &scalar_product,recoParticle1, &xBest1);
		// product.m_recoIP2_helical_refitPV = cpq.CalculatePCA(product.m_flavourOrderedLeptons.at(1)->track.magneticField,product.m_flavourOrderedLeptons.at(1)->track.charge,product.m_flavourOrderedLeptons.at(1)->track.helixParameters(),product.m_flavourOrderedLeptons.at(1)->track.helixCovariance, product.m_flavourOrderedLeptons.at(1)->track.ref,product.m_refitPV->position, false, &scalar_product,recoParticle2, &xBest2);
		 product.m_recoIP1_helical_refitPV = cpq.CalculatePCA(product.m_flavourOrderedLeptons.at(0)->track.magneticField,product.m_flavourOrderedLeptons.at(0)->track.charge,product.m_flavourOrderedLeptons.at(0)->track.helixParameters(),product.m_flavourOrderedLeptons.at(0)->track.helixCovariance, product.m_RefHelix_1,product.m_refitPV->position, false, &scalar_product,recoParticle1, &xBest1);
		product.m_recoIP2_helical_refitPV = cpq.CalculatePCA(product.m_flavourOrderedLeptons.at(1)->track.magneticField,product.m_flavourOrderedLeptons.at(1)->track.charge,product.m_flavourOrderedLeptons.at(1)->track.helixParameters(),product.m_flavourOrderedLeptons.at(1)->track.helixCovariance, product.m_RefHelix_2,product.m_refitPV->position, false, &scalar_product,recoParticle2, &xBest2);

		ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IP1HelixRefitPVCov = cpq.CalculatePCACovariance(product.m_flavourOrderedLeptons.at(0)->track.magneticField,product.m_flavourOrderedLeptons.at(0)->track.charge,product.m_flavourOrderedLeptons.at(0)->track.helixParameters(),product.m_flavourOrderedLeptons.at(0)->track.helixCovariance, product.m_RefHelix_1,product.m_refitPV->position, product.m_refitPV->covariance, xBest1);
		ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> IP2HelixRefitPVCov = cpq.CalculatePCACovariance(product.m_flavourOrderedLeptons.at(1)->track.magneticField,product.m_flavourOrderedLeptons.at(1)->track.charge,product.m_flavourOrderedLeptons.at(1)->track.helixParameters(),product.m_flavourOrderedLeptons.at(1)->track.helixCovariance, product.m_RefHelix_2,product.m_refitPV->position, product.m_refitPV->covariance, xBest2);

		product.m_recoIP1_helical_refitPVCovxx = IP1HelixRefitPVCov(0,0);
		product.m_recoIP1_helical_refitPVCovxy = IP1HelixRefitPVCov(0,1);
		product.m_recoIP1_helical_refitPVCovxz = IP1HelixRefitPVCov(0,2);
		product.m_recoIP1_helical_refitPVCovyy = IP1HelixRefitPVCov(1,1);
		product.m_recoIP1_helical_refitPVCovyz = IP1HelixRefitPVCov(1,2);
		product.m_recoIP1_helical_refitPVCovzz = IP1HelixRefitPVCov(2,2);

		product.m_recoIP2_helical_refitPVCovxx = IP2HelixRefitPVCov(0,0);
		product.m_recoIP2_helical_refitPVCovxy = IP2HelixRefitPVCov(0,1);
		product.m_recoIP2_helical_refitPVCovxz = IP2HelixRefitPVCov(0,2);
		product.m_recoIP2_helical_refitPVCovyy = IP2HelixRefitPVCov(1,1);
		product.m_recoIP2_helical_refitPVCovyz = IP2HelixRefitPVCov(1,2);
		product.m_recoIP2_helical_refitPVCovzz = IP2HelixRefitPVCov(2,2);

		ROOT::Math::SVector<float, 3> IP1rPV_(product.m_recoIP1_helical_refitPV(0), product.m_recoIP2_helical_refitPV(1), product.m_recoIP1_helical_refitPV(2));// Conversion from TVector3 to SVector
		IP1rPV_ /= sqrt(ROOT::Math::Dot(IP1rPV_, IP1rPV_));// Normalize
		ROOT::Math::SVector<float, 3> IP2rPV_(product.m_recoIP2_helical_refitPV(0), product.m_recoIP2_helical_refitPV(1), product.m_recoIP2_helical_refitPV(2));
		IP2rPV_ /= sqrt(ROOT::Math::Dot(IP2rPV_, IP2rPV_));
		product.m_IP1MagPerSigrPV = sqrt( (product.m_recoIP1_helical_refitPV).x()*(product.m_recoIP1_helical_refitPV).x() + (product.m_recoIP1_helical_refitPV).y()*(product.m_recoIP1_helical_refitPV).y() + (product.m_recoIP1_helical_refitPV).z()*(product.m_recoIP1_helical_refitPV).z() ) / sqrt( ROOT::Math::Dot(IP1rPV_, IP1HelixRefitPVCov * IP1rPV_) );
		product.m_IP2MagPerSigrPV = sqrt( (product.m_recoIP1_helical_refitPV).x()*(product.m_recoIP1_helical_refitPV).x() + (product.m_recoIP1_helical_refitPV).y()*(product.m_recoIP1_helical_refitPV).y() + (product.m_recoIP1_helical_refitPV).z()*(product.m_recoIP1_helical_refitPV).z() ) / sqrt( ROOT::Math::Dot(IP2rPV_, IP2HelixRefitPVCov * IP2rPV_) );

		// calculate cosPsi
		if (recoParticle1->charge() == +1){
			product.m_cosPsiPlus  = cpq.CalculateCosPsi(recoParticle1->p4, product.m_recoIP1_refitPV);
			product.m_cosPsiMinus = cpq.CalculateCosPsi(recoParticle2->p4, product.m_recoIP2_refitPV);
		} else {
			product.m_cosPsiPlus  = cpq.CalculateCosPsi(recoParticle2->p4, product.m_recoIP2_refitPV);
			product.m_cosPsiMinus = cpq.CalculateCosPsi(recoParticle1->p4, product.m_recoIP1_refitPV);
		}

		// calculate phi*cp using the refitted PV
		// FIXME two functions are called, need to remove one of the two
		// in this case, the ipvectors are calculated within the CalculatePhiStarCP functions
		product.m_recoPhiStarCPrPV = cpq.CalculatePhiStarCP(product.m_refitPV, trackP, trackM, momentumP, momentumM);
		product.m_recoPhiStarCPrPVBS = cpq.CalculatePhiStarCP(product.m_refitPVBS, trackP, trackM, momentumP, momentumM);

		// azimuthal angles of the tau decay planes
		product.m_recoPhiPlus_ipmeth = cpq.GetRecoPhiPlus_ipmeth();
		product.m_recoPhiMinus_ipmeth = cpq.GetRecoPhiMinus_ipmeth();
		product.m_recoPhiStarPlus_ipmeth = cpq.GetRecoPhiStarPlus_ipmeth();
		product.m_recoPhiStarMinus_ipmeth = cpq.GetRecoPhiStarMinus_ipmeth();

		// calcalute phi*cp by passing ipvectors as arguments
		// get the IP vectors corresponding to charge+ and charge- particles
		if (recoParticle1->getHash() == chargedPart1->getHash()){
			IPPlus  = product.m_recoIP1_refitPV;
			IPMinus = product.m_recoIP2_refitPV;
			IPPlus_helical  = product.m_recoIP1_helical_refitPV;
			IPMinus_helical = product.m_recoIP2_helical_refitPV;
		} else {
			IPPlus  = product.m_recoIP2_refitPV;
			IPMinus = product.m_recoIP1_refitPV;
			IPPlus_helical  =  product.m_recoIP2_helical_refitPV;
			IPMinus_helical =  product.m_recoIP1_helical_refitPV;
		}

		// calculate phi*cp, by taking the IP vectors as an argument
		// FIXME keep it and remove the previous call, or the other way around
		// product.m_recoPhiStarCPrPV2 = cpq.CalculatePhiStarCP(momentumP, momentumM, IPPlus, IPMinus, "reco");
		product.m_recoPhiStarCPrPV_helical = cpq.CalculatePhiStarCP(momentumP, momentumM, IPPlus_helical, IPMinus_helical, "reco");


		// ---------
		// comb-method - with refitted PV
		// ---------
		if ( product.m_decayChannel == HttEnumTypes::DecayChannel::MT || product.m_decayChannel == HttEnumTypes::DecayChannel::ET ){
			KTau* recoTau2 = static_cast<KTau*>(recoParticle2);

			product.m_recoPhiStarCPComb       = cpq.CalculatePhiStarCPComb(product.m_recoIP1_refitPV, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
			product.m_recoPhiStarCPCombMerged = cpq.MergePhiStarCPCombSemiLeptonic(product.m_recoPhiStarCPComb, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);

			product.m_recoPhiStarCPCombBS       = cpq.CalculatePhiStarCPComb(product.m_recoIP1_refitPVBS, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
			product.m_recoPhiStarCPCombMergedBS = cpq.MergePhiStarCPCombSemiLeptonic(product.m_recoPhiStarCPCombBS, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);

			product.m_recoPhiStarCPComb_helical       = cpq.CalculatePhiStarCPComb(product.m_recoIP1_refitPVBS, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
			product.m_recoPhiStarCPCombMerged_helical = cpq.MergePhiStarCPCombSemiLeptonic(product.m_recoPhiStarCPComb_helical, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
		}
		if ( product.m_decayChannel == HttEnumTypes::DecayChannel::TT ){
			KTau* recoTau1 = static_cast<KTau*>(recoParticle1);
			KTau* recoTau2 = static_cast<KTau*>(recoParticle2);
			// tau1->rho, tau2->a
			if (recoTau1->decayMode == 1 && recoTau2->decayMode != 1) {
				product.m_recoPhiStarCPComb       = cpq.CalculatePhiStarCPComb(product.m_recoIP2_refitPV, recoParticle2->p4, recoTau1->chargedHadronCandidates.at(0).p4, recoTau1->piZeroMomentum(), recoParticle2->charge());
				product.m_recoPhiStarCPCombMerged = cpq.MergePhiStarCPCombFullyHadronic(product.m_recoPhiStarCPComb, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);

				product.m_recoPhiStarCPCombBS       = cpq.CalculatePhiStarCPComb(product.m_recoIP2_refitPVBS, recoParticle2->p4, recoTau1->chargedHadronCandidates.at(0).p4, recoTau1->piZeroMomentum(), recoParticle2->charge());
				product.m_recoPhiStarCPCombMergedBS = cpq.MergePhiStarCPCombFullyHadronic(product.m_recoPhiStarCPCombBS, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);

				product.m_recoPhiStarCPComb_helical       = cpq.CalculatePhiStarCPComb(product.m_recoIP2_refitPV, recoParticle2->p4, recoTau1->chargedHadronCandidates.at(0).p4, recoTau1->piZeroMomentum(), recoParticle2->charge());
				product.m_recoPhiStarCPCombMerged_helical = cpq.MergePhiStarCPCombFullyHadronic(product.m_recoPhiStarCPComb_helical, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
			}
			// tau1->a, tau2->rho
			if (recoTau1->decayMode != 1 && recoTau2->decayMode ==1){
				product.m_recoPhiStarCPComb       = cpq.CalculatePhiStarCPComb(product.m_recoIP1_refitPV, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
				product.m_recoPhiStarCPCombMerged = cpq.MergePhiStarCPCombFullyHadronic(product.m_recoPhiStarCPComb, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);

				product.m_recoPhiStarCPCombBS       = cpq.CalculatePhiStarCPComb(product.m_recoIP1_refitPVBS, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
				product.m_recoPhiStarCPCombMergedBS = cpq.MergePhiStarCPCombFullyHadronic(product.m_recoPhiStarCPCombBS, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);

				product.m_recoPhiStarCPComb_helical       = cpq.CalculatePhiStarCPComb(product.m_recoIP1_helical_refitPV, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
				product.m_recoPhiStarCPCombMerged_helical = cpq.MergePhiStarCPCombFullyHadronic(product.m_recoPhiStarCPComb_helical, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
			}

		}  // if tt ch.

		if (!m_isData){
			// calculate deltaR, deltaEta, deltaPhi and delta between recoIPvec and genIPvec
			if(&product.m_genIP1 != nullptr && product.m_genIP1.x() != -999){
				// wrt thePV
				product.m_deltaEtaGenRecoIP1 = product.m_recoIP1.Eta() - product.m_genIP1.Eta();
				product.m_deltaPhiGenRecoIP1 = product.m_recoIP1.DeltaPhi(product.m_genIP1);
				product.m_deltaRGenRecoIP1   = product.m_recoIP1.DeltaR(product.m_genIP1);
				product.m_deltaGenRecoIP1    = product.m_recoIP1.Angle(product.m_genIP1);

				//with the helical approach
				product.m_deltaEtaGenRecoIP1_helical = product.m_recoIP1_helical.Eta() - product.m_genIP1.Eta();
				product.m_deltaPhiGenRecoIP1_helical = product.m_recoIP1_helical.DeltaPhi(product.m_genIP1);//product.m_recoIP1);//
				product.m_deltaRGenRecoIP1_helical   = product.m_recoIP1_helical.DeltaR(product.m_genIP1);
				product.m_deltaGenRecoIP1_helical    = product.m_recoIP1_helical.Angle(product.m_genIP1);//product.m_recoIP1);//

				// wrt refitted PV
				product.m_deltaEtaGenRecoIP1_refitPV = product.m_recoIP1_refitPV.Eta() - product.m_genIP1.Eta();
				product.m_deltaPhiGenRecoIP1_refitPV = product.m_recoIP1_refitPV.DeltaPhi(product.m_genIP1);//product.m_recoIP1_refitPV);//
				product.m_deltaRGenRecoIP1_refitPV   = product.m_recoIP1_refitPV.DeltaR(product.m_genIP1);
				product.m_deltaGenRecoIP1_refitPV    = product.m_recoIP1_refitPV.Angle(product.m_genIP1);//product.m_recoIP1_refitPV);//

				product.m_deltaEtaGenRecoIP1_helical_refitPV = product.m_recoIP1_helical_refitPV.Eta() - product.m_genIP1.Eta();
				product.m_deltaPhiGenRecoIP1_helical_refitPV = product.m_recoIP1_helical_refitPV.DeltaPhi(product.m_genIP1);
				product.m_deltaRGenRecoIP1_helical_refitPV   = product.m_recoIP1_helical_refitPV.DeltaR(product.m_genIP1);
				product.m_deltaGenRecoIP1_helical_refitPV    = product.m_recoIP1_helical_refitPV.Angle(product.m_genIP1);
			} // if genIP1 exists

			if(&product.m_genIP2 != nullptr && product.m_genIP2.x() != -999){
				// wrt refitted PV
				product.m_deltaEtaGenRecoIP2_refitPV = product.m_recoIP2_refitPV.Eta() - product.m_genIP2.Eta();
				product.m_deltaPhiGenRecoIP2_refitPV = product.m_recoIP2_refitPV.DeltaPhi(product.m_genIP2);
				product.m_deltaRGenRecoIP2_refitPV   = product.m_recoIP2_refitPV.DeltaR(product.m_genIP2);
				product.m_deltaGenRecoIP2_refitPV    = product.m_recoIP2_refitPV.Angle(product.m_genIP2);

				product.m_deltaEtaGenRecoIP2_helical_refitPV = product.m_recoIP2_helical_refitPV.Eta() - product.m_genIP2.Eta();
				product.m_deltaPhiGenRecoIP2_helical_refitPV = product.m_recoIP2_helical_refitPV.DeltaPhi(product.m_genIP2);
				product.m_deltaRGenRecoIP2_helical_refitPV   = product.m_recoIP2_helical_refitPV.DeltaR(product.m_genIP2);
				product.m_deltaGenRecoIP2_helical_refitPV    = product.m_recoIP2_helical_refitPV.Angle(product.m_genIP2);
			} // if genIP2 exists

		} // if MC sample
	} // if the refitPV exists
}
