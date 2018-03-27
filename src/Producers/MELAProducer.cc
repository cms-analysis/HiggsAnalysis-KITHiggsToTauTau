
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MELAProducer.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/Utility.h"


std::string MELAProducer::GetProducerId() const
{
	return "MELAProducer";
}

void MELAProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	
	// https://github.com/cms-analysis/HiggsAnalysis-ZZMatrixElement/blob/v2.1.1/MELA/interface/Mela.h
	// https://github.com/cms-analysis/HiggsAnalysis-ZZMatrixElement/blob/v2.1.1/MELA/interface/TVar.hh
	m_mela = std::unique_ptr<Mela>(new Mela(13.0, 125.0, TVar::SILENT));
	
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaProbCPEvenGGH", [](event_type const& event, product_type const& product)
	{
		return product.m_melaProbCPEvenGGH;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaProbCPOddGGH", [](event_type const& event, product_type const& product)
	{
		return product.m_melaProbCPOddGGH;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaProbCPMixGGH", [](event_type const& event, product_type const& product)
	{
		return product.m_melaProbCPMixGGH;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaDiscriminatorD0MinusGGH", [](event_type const& event, product_type const& product)
	{
		return product.m_melaDiscriminatorD0MinusGGH;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaDiscriminatorDCPGGH", [](event_type const& event, product_type const& product)
	{
		return product.m_melaDiscriminatorDCPGGH;
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaProbCPEvenVBF", [](event_type const& event, product_type const& product)
	{
		return product.m_melaProbCPEvenVBF;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaProbCPOddVBF", [](event_type const& event, product_type const& product)
	{
		return product.m_melaProbCPOddVBF;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaProbCPMixVBF", [](event_type const& event, product_type const& product)
	{
		return product.m_melaProbCPMixVBF;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaDiscriminatorD0MinusVBF", [](event_type const& event, product_type const& product)
	{
		return product.m_melaDiscriminatorD0MinusVBF;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaDiscriminatorDCPVBF", [](event_type const& event, product_type const& product)
	{
		return product.m_melaDiscriminatorDCPVBF;
	});
	
	/*
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaProbCPEvenWlepH", [](event_type const& event, product_type const& product)
	{
		return product.m_melaProbCPEvenWlepH;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaProbCPOddWlepH", [](event_type const& event, product_type const& product)
	{
		return product.m_melaProbCPOddWlepH;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaProbCPMixWlepH", [](event_type const& event, product_type const& product)
	{
		return product.m_melaProbCPMixWlepH;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaDiscriminatorD0MinusWlepH", [](event_type const& event, product_type const& product)
	{
		return product.m_melaDiscriminatorD0MinusWlepH;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaDiscriminatorDCPWlepH", [](event_type const& event, product_type const& product)
	{
		return product.m_melaDiscriminatorDCPWlepH;
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaProbCPEvenWhadH", [](event_type const& event, product_type const& product)
	{
		return product.m_melaProbCPEvenWhadH;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaProbCPOddWhadH", [](event_type const& event, product_type const& product)
	{
		return product.m_melaProbCPOddWhadH;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaProbCPMixWhadH", [](event_type const& event, product_type const& product)
	{
		return product.m_melaProbCPMixWhadH;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaDiscriminatorD0MinusWhadH", [](event_type const& event, product_type const& product)
	{
		return product.m_melaDiscriminatorD0MinusWhadH;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaDiscriminatorDCPWhadH", [](event_type const& event, product_type const& product)
	{
		return product.m_melaDiscriminatorDCPWhadH;
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaProbCPEvenZlepH", [](event_type const& event, product_type const& product)
	{
		return product.m_melaProbCPEvenZlepH;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaProbCPOddZlepH", [](event_type const& event, product_type const& product)
	{
		return product.m_melaProbCPOddZlepH;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaProbCPMixZlepH", [](event_type const& event, product_type const& product)
	{
		return product.m_melaProbCPMixZlepH;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaDiscriminatorD0MinusZlepH", [](event_type const& event, product_type const& product)
	{
		return product.m_melaDiscriminatorD0MinusZlepH;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaDiscriminatorDCPZlepH", [](event_type const& event, product_type const& product)
	{
		return product.m_melaDiscriminatorDCPZlepH;
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaProbCPEvenZhadH", [](event_type const& event, product_type const& product)
	{
		return product.m_melaProbCPEvenZhadH;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaProbCPOddZhadH", [](event_type const& event, product_type const& product)
	{
		return product.m_melaProbCPOddZhadH;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaProbCPMixZhadH", [](event_type const& event, product_type const& product)
	{
		return product.m_melaProbCPMixZhadH;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaDiscriminatorD0MinusZhadH", [](event_type const& event, product_type const& product)
	{
		return product.m_melaDiscriminatorD0MinusZhadH;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaDiscriminatorDCPZhadH", [](event_type const& event, product_type const& product)
	{
		return product.m_melaDiscriminatorDCPZhadH;
	});
	*/
}


void MELAProducer::Produce(event_type const& event, product_type& product,
                           setting_type const& settings, metadata_type const& metadata) const
{
	if (product.m_svfitResults.fittedHiggsLV != nullptr)
	{
		SimpleParticleCollection_t daughters; // Higgs boson or two tau leptons
		SimpleParticleCollection_t associated; // additional reconstructed jets
		//SimpleParticleCollection_t mothers; // incoming partons in case of gen level mode
		
		TLorentzVector higgsLV = Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*product.m_svfitResults.fittedHiggsLV);
		daughters.emplace_back(DefaultValues::pdgIdH, higgsLV);
		
		for (std::vector<KBasicJet*>::iterator jet = product.m_validJets.begin(); jet != product.m_validJets.end(); ++jet)
		{
			if ((*jet)->p4.Pt() > 30.0)
			{
				TLorentzVector jetLV = Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>((*jet)->p4);
				associated.emplace_back(0, jetLV); // PDG ID = 0 -> unknown (quark or gluon) // TODO: find correct PDG ID from gen matching or from reco jet in Kappa dataformat?
			}
		}
		
		m_mela->setInputEvent(&daughters, &associated, nullptr /*&mothers*/, false);
		
		// caluculate matrix elements for various hypotheses
		CalculateProbabilitiesGGH(product.m_melaProbCPEvenGGH, product.m_melaProbCPOddGGH, product.m_melaProbCPMixGGH);
		CalculateProbabilitiesVBF(product.m_melaProbCPEvenVBF, product.m_melaProbCPOddVBF, product.m_melaProbCPMixVBF);
		/*
		CalculateProbabilitiesWlepH(product.m_melaProbCPEvenWlepH, product.m_melaProbCPOddWlepH, product.m_melaProbCPMixWlepH);
		CalculateProbabilitiesWhadH(product.m_melaProbCPEvenWhadH, product.m_melaProbCPOddWhadH, product.m_melaProbCPMixWhadH);
		CalculateProbabilitiesZlepH(product.m_melaProbCPEvenZlepH, product.m_melaProbCPOddZlepH, product.m_melaProbCPMixZlepH);
		CalculateProbabilitiesZhadH(product.m_melaProbCPEvenZhadH, product.m_melaProbCPOddZhadH, product.m_melaProbCPMixZhadH);
		*/
		
		// calculate discriminators
		CalculateDiscriminators(product.m_melaProbCPEvenGGH, product.m_melaProbCPOddGGH, product.m_melaProbCPMixGGH,
		                        product.m_melaDiscriminatorD0MinusGGH, product.m_melaDiscriminatorDCPGGH);
		CalculateDiscriminators(product.m_melaProbCPEvenVBF, product.m_melaProbCPOddVBF, product.m_melaProbCPMixVBF,
		                        product.m_melaDiscriminatorD0MinusVBF, product.m_melaDiscriminatorDCPVBF);
		/*
		CalculateDiscriminators(product.m_melaProbCPEvenWlepH, product.m_melaProbCPOddWlepH, product.m_melaProbCPMixWlepH,
		                        product.m_melaDiscriminatorD0MinusWlepH, product.m_melaDiscriminatorDCPWlepH);
		CalculateDiscriminators(product.m_melaProbCPEvenWhadH, product.m_melaProbCPOddWhadH, product.m_melaProbCPMixWhadH,
		                        product.m_melaDiscriminatorD0MinusWhadH, product.m_melaDiscriminatorDCPWhadH);
		CalculateDiscriminators(product.m_melaProbCPEvenZlepH, product.m_melaProbCPOddZlepH, product.m_melaProbCPMixZlepH,
		                        product.m_melaDiscriminatorD0MinusZlepH, product.m_melaDiscriminatorDCPZlepH);
		CalculateDiscriminators(product.m_melaProbCPEvenZhadH, product.m_melaProbCPOddZhadH, product.m_melaProbCPMixZhadH,
		                        product.m_melaDiscriminatorD0MinusZhadH, product.m_melaDiscriminatorDCPZhadH);
		*/
		
		m_mela->resetInputEvent();
	}
}

// configurations below from Skype chat with Heshy Roskes from 30.11./01.12.2017
void MELAProducer::CalculateProbabilitiesGGH(float& probCPEven, float& probCPOdd, float& probCPMix) const
{
	// CP even
	m_mela->setProcess(TVar::HSMHiggs, TVar::JHUGen, TVar::JJQCD);
	m_mela->computeProdP(probCPEven, false);
	
	// CP odd
	m_mela->setProcess(TVar::H0minus, TVar::JHUGen, TVar::JJQCD);
	m_mela->computeProdP(probCPOdd, false);
	
	// CP mixing (maximum)
	m_mela->setProcess(TVar::SelfDefine_spin0, TVar::JHUGen, TVar::JJQCD);
	m_mela->selfDHggcoupl[0][gHIGGS_GG_2][0] = 1; // a1
	m_mela->selfDHggcoupl[0][gHIGGS_GG_4][0] = 1; // a3
	m_mela->computeProdP(probCPMix, false);
}

void MELAProducer::CalculateProbabilitiesVBF(float& probCPEven, float& probCPOdd, float& probCPMix) const
{
	// CP even
	m_mela->setProcess(TVar::HSMHiggs, TVar::JHUGen, TVar::JJVBF);
	m_mela->computeProdP(probCPEven, false);
	
	// CP odd
	m_mela->setProcess(TVar::SelfDefine_spin0, TVar::JHUGen, TVar::JJVBF);
	m_mela->selfDHzzcoupl[0][gHIGGS_VV_4][0] = 0.297979; // a3
	m_mela->computeProdP(probCPOdd, false);
	
	// CP mixing (maximum)
	m_mela->setProcess(TVar::SelfDefine_spin0, TVar::JHUGen, TVar::JJVBF);
	m_mela->selfDHzzcoupl[0][gHIGGS_VV_1][0] = 1; // a1
	m_mela->selfDHzzcoupl[0][gHIGGS_VV_4][0] = 0.297979; // a3
	m_mela->computeProdP(probCPMix, false);
}

void MELAProducer::CalculateProbabilitiesWlepH(float& probCPEven, float& probCPOdd, float& probCPMix) const
{
	// CP even
	m_mela->setProcess(TVar::HSMHiggs, TVar::JHUGen, TVar::Lep_WH);
	m_mela->computeProdP(probCPEven, false);
	
	// CP odd
	m_mela->setProcess(TVar::SelfDefine_spin0, TVar::JHUGen, TVar::Lep_WH);
	m_mela->selfDHzzcoupl[0][gHIGGS_VV_4][0] = 0.1236136; // a3
	m_mela->computeProdP(probCPOdd, false);
	
	// CP mixing (maximum)
	m_mela->setProcess(TVar::SelfDefine_spin0, TVar::JHUGen, TVar::Lep_WH);
	m_mela->selfDHzzcoupl[0][gHIGGS_VV_1][0] = 1; // a1
	m_mela->selfDHzzcoupl[0][gHIGGS_VV_4][0] = 0.1236136; // a3
	m_mela->computeProdP(probCPMix, false);
}

void MELAProducer::CalculateProbabilitiesWhadH(float& probCPEven, float& probCPOdd, float& probCPMix) const
{
	// CP even
	m_mela->setProcess(TVar::HSMHiggs, TVar::JHUGen, TVar::Had_WH);
	m_mela->computeProdP(probCPEven, false);
	
	// CP odd
	m_mela->setProcess(TVar::SelfDefine_spin0, TVar::JHUGen, TVar::Had_WH);
	m_mela->selfDHzzcoupl[0][gHIGGS_VV_4][0] = 0.1236136; // a3
	m_mela->computeProdP(probCPOdd, false);
	
	// CP mixing (maximum)
	m_mela->setProcess(TVar::SelfDefine_spin0, TVar::JHUGen, TVar::Had_WH);
	m_mela->selfDHzzcoupl[0][gHIGGS_VV_1][0] = 1; // a1
	m_mela->selfDHzzcoupl[0][gHIGGS_VV_4][0] = 0.1236136; // a3
	m_mela->computeProdP(probCPMix, false);
}

void MELAProducer::CalculateProbabilitiesZlepH(float& probCPEven, float& probCPOdd, float& probCPMix) const
{
	// CP even
	m_mela->setProcess(TVar::HSMHiggs, TVar::JHUGen, TVar::Lep_ZH);
	m_mela->computeProdP(probCPEven, false);
	
	// CP odd
	m_mela->setProcess(TVar::SelfDefine_spin0, TVar::JHUGen, TVar::Lep_ZH);
	m_mela->selfDHzzcoupl[0][gHIGGS_VV_4][0] = 0.144057; // a3
	m_mela->computeProdP(probCPOdd, false);
	
	// CP mixing (maximum)
	m_mela->setProcess(TVar::SelfDefine_spin0, TVar::JHUGen, TVar::Lep_ZH);
	m_mela->selfDHzzcoupl[0][gHIGGS_VV_1][0] = 1; // a1
	m_mela->selfDHzzcoupl[0][gHIGGS_VV_4][0] = 0.144057; // a3
	m_mela->computeProdP(probCPMix, false);
}

void MELAProducer::CalculateProbabilitiesZhadH(float& probCPEven, float& probCPOdd, float& probCPMix) const
{
	// CP even
	m_mela->setProcess(TVar::HSMHiggs, TVar::JHUGen, TVar::Had_ZH);
	m_mela->computeProdP(probCPEven, false);
	
	// CP odd
	m_mela->setProcess(TVar::SelfDefine_spin0, TVar::JHUGen, TVar::Had_ZH);
	m_mela->selfDHzzcoupl[0][gHIGGS_VV_4][0] = 0.144057; // a3
	m_mela->computeProdP(probCPOdd, false);
	
	// CP mixing (maximum)
	m_mela->setProcess(TVar::SelfDefine_spin0, TVar::JHUGen, TVar::Had_ZH);
	m_mela->selfDHzzcoupl[0][gHIGGS_VV_1][0] = 1; // a1
	m_mela->selfDHzzcoupl[0][gHIGGS_VV_4][0] = 0.144057; // a3
	m_mela->computeProdP(probCPMix, false);
}

void MELAProducer::CalculateDiscriminators(float probCPEven, float probCPOdd, float probCPMix,
                                           float& discriminatorD0Minus, float& discriminatorDCP) const
{
	if ((probCPEven + probCPOdd) != 0.0)
	{
		discriminatorD0Minus = probCPEven / (probCPEven + probCPOdd);
		discriminatorDCP = (probCPMix - probCPEven - probCPOdd) / (probCPEven + probCPOdd);
	}
	else
	{
		discriminatorD0Minus = DefaultValues::UndefinedFloat;
		discriminatorDCP = DefaultValues::UndefinedFloat;
	}
}

