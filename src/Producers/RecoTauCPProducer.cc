
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/CPQuantities.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/RecoTauCPProducer.h"


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
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("thePVx", [](event_type const& event, product_type const& product)
	{
		return (product.m_thePV)->position.x();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("thePVy", [](event_type const& event, product_type const& product)
	{
		return (product.m_thePV)->position.y();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("thePVz", [](event_type const& event, product_type const& product)
	{
		return (product.m_thePV)->position.z();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("thePVchi2", [](event_type const& event, product_type const& product)
	{
		return (product.m_thePV)->chi2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("thePVnDOF", [](event_type const& event, product_type const& product)
	{
		return (product.m_thePV)->nDOF;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("thePVnTracks", [](event_type const& event, product_type const& product)
	{
		return (product.m_thePV)->nTracks;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("thePVsigmaxx", [](event_type const& event, product_type const& product)
	{
		return (product.m_thePV)->covariance.At(0,0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("thePVsigmayy", [](event_type const& event, product_type const& product)
	{
		return (product.m_thePV)->covariance.At(1,1);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("thePVsigmazz", [](event_type const& event, product_type const& product)
	{
		return (product.m_thePV)->covariance.At(2,2);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("thePVsigmaxy", [](event_type const& event, product_type const& product)
	{
		return (product.m_thePV)->covariance.At(0,1);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("thePVsigmaxz", [](event_type const& event, product_type const& product)
	{
		return (product.m_thePV)->covariance.At(0,2);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("thePVsigmayz", [](event_type const& event, product_type const& product)
	{
		return (product.m_thePV)->covariance.At(1,2);
	});

	// BS coordinates and parameters
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("theBSx", [](event_type const& event, product_type const& product)
	{
		return (product.m_theBS)->position.x();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("theBSy", [](event_type const& event, product_type const& product)
	{
		return (product.m_theBS)->position.y();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("theBSz", [](event_type const& event, product_type const& product)
	{
		return (product.m_theBS)->position.z();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("theBSsigmax", [](event_type const& event, product_type const& product)
	{
		return (product.m_theBS)->beamWidthX;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("theBSsigmay", [](event_type const& event, product_type const& product)
	{
		return (product.m_theBS)->beamWidthY;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("theBSsigmaz", [](event_type const& event, product_type const& product)
	{
		return (product.m_theBS)->sigmaZ;
	});

	// CP-related quantities
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoPhiStarCP", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCP;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoPhiStarCP_rho", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCP_rho;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoPhiStarCP_rho_merged", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCP_rho_merged;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("reco_posyTauL", [](event_type const& event, product_type const& product)
	{
		return product.m_reco_posyTauL;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("reco_negyTauL", [](event_type const& event, product_type const& product)
	{
		return product.m_reco_negyTauL;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoPhiStarCPrPV", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoPhiStarCPrPV2", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPrPV2;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoPhiStarCPrPVbs", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCPrPVbs;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoPhiStar", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStar;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoPhiStar_rho", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStar_rho;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoChargedHadron1HiggsFrameEnergy", [](event_type const& event, product_type const& product)
	{
		return product.m_recoChargedHadronEnergies.first;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoChargedHadron2HiggsFrameEnergy", [](event_type const& event, product_type const& product)
	{
		return product.m_recoChargedHadronEnergies.second;
	});

	// impact parameters d0=dxy and dz
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("d0_refitPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_refitPV ? product.m_flavourOrderedLeptons.at(0)->track.getDxy(product.m_refitPV) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("d0_refitPVBS_1", [](event_type const& event, product_type const& product)
	{
		return product.m_refitPVBS ? product.m_flavourOrderedLeptons.at(0)->track.getDxy(product.m_refitPVBS) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("dZ_refitPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_refitPV ? product.m_flavourOrderedLeptons.at(0)->track.getDz(product.m_refitPV) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("dZ_refitPVBS_1", [](event_type const& event, product_type const& product)
	{
		return product.m_refitPVBS ? product.m_flavourOrderedLeptons.at(0)->track.getDz(product.m_refitPVBS) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("d0_refitPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_refitPV ? product.m_flavourOrderedLeptons.at(1)->track.getDxy(product.m_refitPV) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("d0_refitPVBS_2", [](event_type const& event, product_type const& product)
	{
		return product.m_refitPVBS ? product.m_flavourOrderedLeptons.at(1)->track.getDxy(product.m_refitPVBS) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("dZ_refitPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_refitPV ? product.m_flavourOrderedLeptons.at(1)->track.getDz(product.m_refitPV) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("dZ_refitPVBS_2", [](event_type const& event, product_type const& product)
	{
		return product.m_refitPVBS ? product.m_flavourOrderedLeptons.at(1)->track.getDz(product.m_refitPVBS) : DefaultValues::UndefinedDouble;
	});
//	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoImpactParameter1", [](event_type const& event, product_type const& product)
//	{
//		return product.m_recoIP1;
//	});
//	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoImpactParameter2", [](event_type const& event, product_type const& product)
//	{
//		return product.m_recoIP2;
//	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoTrackRefError1", [](event_type const& event, product_type const& product)
	{
		return product.m_recoTrackRefError1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoTrackRefError2", [](event_type const& event, product_type const& product)
	{
		return product.m_recoTrackRefError2;
	});

	// IP vectors wrt thePV
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("IP_1x", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1 != nullptr) ? (product.m_recoIP1).x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("IP_1y", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1 != nullptr) ? (product.m_recoIP1).y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("IP_1z", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1 != nullptr) ? (product.m_recoIP1).z() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("IP_2x", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2 != nullptr) ? (product.m_recoIP2).x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("IP_2y", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2 != nullptr) ? (product.m_recoIP2).y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("IP_2z", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2 != nullptr) ? (product.m_recoIP2).z() : DefaultValues::UndefinedFloat);
	});

	// IP vectors wrt refitted PV
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("IP_refitPV_1x", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_refitPV != nullptr) ? (product.m_recoIP1_refitPV).x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("IP_refitPV_1y", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_refitPV != nullptr) ? (product.m_recoIP1_refitPV).y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("IP_refitPV_1z", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP1_refitPV != nullptr) ? (product.m_recoIP1_refitPV).z() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("IP_refitPV_2x", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_refitPV != nullptr) ? (product.m_recoIP2_refitPV).x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("IP_refitPV_2y", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_refitPV != nullptr) ? (product.m_recoIP2_refitPV).y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("IP_refitPV_2z", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_recoIP2_refitPV != nullptr) ? (product.m_recoIP2_refitPV).z() : DefaultValues::UndefinedFloat);
	});

	// cosPsi
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("cosPsiPlus", [](event_type const& event, product_type const& product)
	{
		return product.m_cosPsiPlus;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("cosPsiMinus", [](event_type const& event, product_type const& product)
	{
		return product.m_cosPsiMinus;
	});

	// errors on dxy, dz and IP wrt thePV
	// using propagation of errors
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("errD0_1_newErr", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP1vec.at(0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("errDZ_1_newErr", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP1vec.at(1);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("errIP_1", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP1vec.at(2);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("errD0_2_newErr", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP2vec.at(0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("errDZ_2_newErr", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP2vec.at(1);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("errIP_2", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP2vec.at(2);
	});


	// errors on dxy, dz and IP wrt refitted PV
	// using propagation of errors
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("errD0_refitPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP1vec_refitPV.at(0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("errDZ_refitPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP1vec_refitPV.at(1);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("errIP_refitPV_1", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP1vec_refitPV.at(2);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("errD0_refitPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP2vec_refitPV.at(0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("errDZ_refitPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP2vec_refitPV.at(1);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("errIP_refitPV_2", [](event_type const& event, product_type const& product)
	{
		return product.m_errorIP2vec_refitPV.at(2);
	});


	// deltaEta, deltaPhi, deltaR and angle delta between IP vectors
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("deltaEtaGenRecoIP1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaEtaGenRecoIP1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("deltaEtaGenRecoIP2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaEtaGenRecoIP2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("deltaPhiGenRecoIP1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaPhiGenRecoIP1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("deltaPhiGenRecoIP2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaPhiGenRecoIP2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("deltaRGenRecoIP1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaRGenRecoIP1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("deltaRGenRecoIP2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaRGenRecoIP2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("deltaGenRecoIP1", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaGenRecoIP1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("deltaGenRecoIP2", [](event_type const& event, product_type const& product)
	{
		return product.m_deltaGenRecoIP2;
	});

}

void RecoTauCPProducer::Produce(event_type const& event, product_type& product, setting_type const& settings, metadata_type const& metadata) const
{
	assert(event.m_vertexSummary);
	assert(product.m_flavourOrderedLeptons.size() >= 2);

	// save the PV and the BS
	product.m_thePV = &event.m_vertexSummary->pv;
	product.m_theBS = event.m_beamSpot;

	// initialization of TVector3 objects
	product.m_recoIP1.SetXYZ(-999,-999,-999);
	product.m_recoIP2.SetXYZ(-999,-999,-999);
	product.m_recoIP1_refitPV.SetXYZ(-999,-999,-999);
	product.m_recoIP2_refitPV.SetXYZ(-999,-999,-999);
	TVector3 IPPlus;
	TVector3 IPMinus;
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




	// ---------
	// ip-method
	// ---------
	// phi*CP wrt thePV
	product.m_recoPhiStarCP = cpq.CalculatePhiStarCP(product.m_thePV, trackP, trackM, momentumP, momentumM);

	if (product.m_refitPV != nullptr){
		// calculation of the IP vectors and relative errors
		product.m_recoIP1 = cpq.CalculateIPVector(recoParticle1, product.m_thePV);
		product.m_recoIP2 = cpq.CalculateIPVector(recoParticle2, product.m_thePV);
		product.m_errorIP1vec = cpq.CalculateIPErrors(recoParticle1, product.m_thePV, &product.m_recoIP1);
		product.m_errorIP2vec = cpq.CalculateIPErrors(recoParticle2, product.m_thePV, &product.m_recoIP2);

		product.m_recoIP1_refitPV = cpq.CalculateIPVector(recoParticle1, product.m_refitPV);
		product.m_recoIP2_refitPV = cpq.CalculateIPVector(recoParticle2, product.m_refitPV);
		product.m_errorIP1vec_refitPV = cpq.CalculateIPErrors(recoParticle1, product.m_refitPV, &product.m_recoIP1_refitPV);
		product.m_errorIP2vec_refitPV = cpq.CalculateIPErrors(recoParticle2, product.m_refitPV, &product.m_recoIP2_refitPV);

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

		// calcalute phi*cp by passing ipvectors as arguments
		// get the IP vectors corresponding to charge+ and charge- particles
		if (recoParticle1->getHash() == chargedPart1->getHash()){
			IPPlus  = product.m_recoIP1_refitPV;
			IPMinus = product.m_recoIP2_refitPV;
		} else {
			IPPlus  = product.m_recoIP2_refitPV;
			IPMinus = product.m_recoIP1_refitPV;
		}
		
		// calculate phi*cp
		product.m_recoPhiStarCPrPV2 = cpq.CalculatePhiStarCP(momentumP, momentumM, IPPlus, IPMinus);
			


		if (!m_isData){
			// calculate deltaR, deltaEta, deltaPhi and delta between recoIPvec and genIPvec
			// only for recoIPvec wrt refitted PV
			if(&product.m_genIP1 != nullptr && product.m_genIP1.x() != -999){
				product.m_deltaEtaGenRecoIP1 = product.m_recoIP1_refitPV.Eta() - product.m_genIP1.Eta();
				product.m_deltaPhiGenRecoIP1 = product.m_recoIP1_refitPV.DeltaPhi(product.m_genIP1);
				product.m_deltaRGenRecoIP1   = product.m_recoIP1_refitPV.DeltaR(product.m_genIP1);
				product.m_deltaGenRecoIP1    = product.m_recoIP1_refitPV.Angle(product.m_genIP1);
			} // if genIP1 exists

			if(&product.m_genIP2 != nullptr && product.m_genIP2.x() != -999){
				product.m_deltaEtaGenRecoIP2 = product.m_recoIP2_refitPV.Eta() - product.m_genIP2.Eta();
				product.m_deltaPhiGenRecoIP2 = product.m_recoIP2_refitPV.DeltaPhi(product.m_genIP2);
				product.m_deltaRGenRecoIP2   = product.m_recoIP2_refitPV.DeltaR(product.m_genIP2);
				product.m_deltaGenRecoIP2    = product.m_recoIP2_refitPV.Angle(product.m_genIP2);
			} // if genIP2 exists

		} // if MC sample


	} // if the refitPV exists


}
