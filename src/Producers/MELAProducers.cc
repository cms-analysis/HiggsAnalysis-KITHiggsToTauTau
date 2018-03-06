
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MELAProducers.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/Utility.h"


MELAProducer::MELAProducer(
		std::string name,
		SvfitResults product_type::*svfitResultsMember,
		
		float product_type::*melaProbCPEvenGGHMember,
		float product_type::*melaProbCPOddGGHMember,
		float product_type::*melaProbCPMixGGHMember,
		float product_type::*melaDiscriminatorD0MinusGGHMember,
		float product_type::*melaDiscriminatorDCPGGHMember,

		float product_type::*melaProbCPEvenVBFMember,
		float product_type::*melaProbCPOddVBFMember,
		float product_type::*melaProbCPMixVBFMember,
		float product_type::*melaDiscriminatorD0MinusVBFMember,
		float product_type::*melaDiscriminatorDCPVBFMember

		/*
		float product_type::*melaProbCPEvenWlepHMember,
		float product_type::*melaProbCPOddWlepHMember,
		float product_type::*melaProbCPMixWlepHMember,
		float product_type::*melaDiscriminatorD0MinusWlepHMember,
		float product_type::*melaDiscriminatorDCPWlepHMember,

		float product_type::*melaProbCPEvenWhadHMember,
		float product_type::*melaProbCPOddWhadHMember,
		float product_type::*melaProbCPMixWhadHMember,
		float product_type::*melaDiscriminatorD0MinusWhadHMember,
		float product_type::*melaDiscriminatorDCPWhadHMember,

		float product_type::*melaProbCPEvenZlepHMember,
		float product_type::*melaProbCPOddZlepHMember,
		float product_type::*melaProbCPMixZlepHMember,
		float product_type::*melaDiscriminatorD0MinusZlepHMember,
		float product_type::*melaDiscriminatorDCPZlepHMember,

		float product_type::*melaProbCPEvenZhadHMember,
		float product_type::*melaProbCPOddZhadHMember,
		float product_type::*melaProbCPMixZhadHMember,
		float product_type::*melaDiscriminatorD0MinusZhadHMember,
		float product_type::*melaDiscriminatorDCPZhadHMember
		*/
) :
	ProducerBase<HttTypes>(),
	m_name(name),
	m_svfitResultsMember(svfitResultsMember),
	
	m_melaProbCPEvenGGHMember(melaProbCPEvenGGHMember),
	m_melaProbCPOddGGHMember(melaProbCPOddGGHMember),
	m_melaProbCPMixGGHMember(melaProbCPMixGGHMember),
	m_melaDiscriminatorD0MinusGGHMember(melaDiscriminatorD0MinusGGHMember),
	m_melaDiscriminatorDCPGGHMember(melaDiscriminatorDCPGGHMember),

	m_melaProbCPEvenVBFMember(melaProbCPEvenVBFMember),
	m_melaProbCPOddVBFMember(melaProbCPOddVBFMember),
	m_melaProbCPMixVBFMember(melaProbCPMixVBFMember),
	m_melaDiscriminatorD0MinusVBFMember(melaDiscriminatorD0MinusVBFMember),
	m_melaDiscriminatorDCPVBFMember(melaDiscriminatorDCPVBFMember)

	/*
	m_melaProbCPEvenWlepHMember(melaProbCPEvenWlepHMember),
	m_melaProbCPOddWlepHMember(melaProbCPOddWlepHMember),
	m_melaProbCPMixWlepHMember(melaProbCPMixWlepHMember),
	m_melaDiscriminatorD0MinusWlepHMember(melaDiscriminatorD0MinusWlepHMember),
	m_melaDiscriminatorDCPWlepHMember(melaDiscriminatorDCPWlepHMember),

	m_melaProbCPEvenWhadHMember(melaProbCPEvenWhadHMember),
	m_melaProbCPOddWhadHMember(melaProbCPOddWhadHMember),
	m_melaProbCPMixWhadHMember(melaProbCPMixWhadHMember),
	m_melaDiscriminatorD0MinusWhadHMember(melaDiscriminatorD0MinusWhadHMember),
	m_melaDiscriminatorDCPWhadHMember(melaDiscriminatorDCPWhadHMember),

	m_melaProbCPEvenZlepHMember(melaProbCPEvenZlepHMember),
	m_melaProbCPOddZlepHMember(melaProbCPOddZlepHMember),
	m_melaProbCPMixZlepHMember(melaProbCPMixZlepHMember),
	m_melaDiscriminatorD0MinusZlepHMember(melaDiscriminatorD0MinusZlepHMember),
	m_melaDiscriminatorDCPZlepHMember(melaDiscriminatorDCPZlepHMember),

	m_melaProbCPEvenZhadHMember(melaProbCPEvenZhadHMember),
	m_melaProbCPOddZhadHMember(melaProbCPOddZhadHMember),
	m_melaProbCPMixZhadHMember(melaProbCPMixZhadHMember),
	m_melaDiscriminatorD0MinusZhadHMember(melaDiscriminatorD0MinusZhadHMember),
	m_melaDiscriminatorDCPZhadHMember(melaDiscriminatorDCPZhadHMember)
	*/
{
}

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
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"ProbCPEvenGGH", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaProbCPEvenGGHMember);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"ProbCPOddGGH", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaProbCPOddGGHMember);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"ProbCPMixGGH", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaProbCPMixGGHMember);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"DiscriminatorD0MinusGGH", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaDiscriminatorD0MinusGGHMember);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"DiscriminatorDCPGGH", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaDiscriminatorDCPGGHMember);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"ProbCPEvenVBF", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaProbCPEvenVBFMember);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"ProbCPOddVBF", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaProbCPOddVBFMember);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"ProbCPMixVBF", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaProbCPMixVBFMember);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"DiscriminatorD0MinusVBF", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaDiscriminatorD0MinusVBFMember);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"DiscriminatorDCPVBF", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaDiscriminatorDCPVBFMember);
	});
	
	/*
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"ProbCPEvenWlepH", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaProbCPEvenWlepHMember);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"ProbCPOddWlepH", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaProbCPOddWlepHMember);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"ProbCPMixWlepH", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaProbCPMixWlepHMember);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"DiscriminatorD0MinusWlepH", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaDiscriminatorD0MinusWlepHMember);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"DiscriminatorDCPWlepH", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaDiscriminatorDCPWlepHMember);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"ProbCPEvenWhadH", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaProbCPEvenWhadHMember);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"ProbCPOddWhadH", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaProbCPOddWhadHMember);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"ProbCPMixWhadH", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaProbCPMixWhadHMember);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"DiscriminatorD0MinusWhadH", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaDiscriminatorD0MinusWhadHMember);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"DiscriminatorDCPWhadH", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaDiscriminatorDCPWhadHMember);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"ProbCPEvenZlepH", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaProbCPEvenZlepHMember);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"ProbCPOddZlepH", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaProbCPOddZlepHMember);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"ProbCPMixZlepH", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaProbCPMixZlepHMember);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"DiscriminatorD0MinusZlepH", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaDiscriminatorD0MinusZlepHMember);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"DiscriminatorDCPZlepH", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaDiscriminatorDCPZlepHMember);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"ProbCPEvenZhadH", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaProbCPEvenZhadHMember);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"ProbCPOddZhadH", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaProbCPOddZhadHMember);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"ProbCPMixZhadH", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaProbCPMixZhadHMember);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"DiscriminatorD0MinusZhadH", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaDiscriminatorD0MinusZhadHMember);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mela"+m_name+"DiscriminatorDCPZhadH", [this](event_type const& event, product_type const& product)
	{
		return (product.*m_melaDiscriminatorDCPZhadHMember);
	});
	*/
}


void MELAProducer::Produce(event_type const& event, product_type& product,
                           setting_type const& settings, metadata_type const& metadata) const
{
	if ((product.*m_svfitResultsMember).fittedHiggsLV != nullptr)
	{
		SimpleParticleCollection_t daughters; // Higgs boson or two tau leptons
		SimpleParticleCollection_t associated; // additional reconstructed jets
		//SimpleParticleCollection_t mothers; // incoming partons in case of gen level mode
		
		TLorentzVector higgsLV = Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*((product.*m_svfitResultsMember).fittedHiggsLV));
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
		CalculateProbabilitiesGGH((product.*m_melaProbCPEvenGGHMember), (product.*m_melaProbCPOddGGHMember), (product.*m_melaProbCPMixGGHMember));
		CalculateProbabilitiesVBF((product.*m_melaProbCPEvenVBFMember), (product.*m_melaProbCPOddVBFMember), (product.*m_melaProbCPMixVBFMember));
		/*
		CalculateProbabilitiesWlepH((product.*m_melaProbCPEvenWlepHMember), (product.*m_melaProbCPOddWlepHMember), (product.*m_melaProbCPMixWlepHMember));
		CalculateProbabilitiesWhadH((product.*m_melaProbCPEvenWhadHMember), (product.*m_melaProbCPOddWhadHMember), (product.*m_melaProbCPMixWhadHMember));
		CalculateProbabilitiesZlepH((product.*m_melaProbCPEvenZlepHMember), (product.*m_melaProbCPOddZlepHMember), (product.*m_melaProbCPMixZlepHMember));
		CalculateProbabilitiesZhadH((product.*m_melaProbCPEvenZhadHMember), (product.*m_melaProbCPOddZhadHMember), (product.*m_melaProbCPMixZhadHMember));
		*/
		
		// calculate discriminators
		CalculateDiscriminators((product.*m_melaProbCPEvenGGHMember), (product.*m_melaProbCPOddGGHMember), (product.*m_melaProbCPMixGGHMember),
		                        (product.*m_melaDiscriminatorD0MinusGGHMember), (product.*m_melaDiscriminatorDCPGGHMember));
		CalculateDiscriminators((product.*m_melaProbCPEvenVBFMember), (product.*m_melaProbCPOddVBFMember), (product.*m_melaProbCPMixVBFMember),
		                        (product.*m_melaDiscriminatorD0MinusVBFMember), (product.*m_melaDiscriminatorDCPVBFMember));
		/*
		CalculateDiscriminators((product.*m_melaProbCPEvenWlepHMember), (product.*m_melaProbCPOddWlepHMember), (product.*m_melaProbCPMixWlepHMember),
		                        (product.*m_melaDiscriminatorD0MinusWlepHMember), (product.*m_melaDiscriminatorDCPWlepHMember));
		CalculateDiscriminators((product.*m_melaProbCPEvenWhadHMember), (product.*m_melaProbCPOddWhadHMember), (product.*m_melaProbCPMixWhadHMember),
		                        (product.*m_melaDiscriminatorD0MinusWhadHMember), (product.*m_melaDiscriminatorDCPWhadHMember));
		CalculateDiscriminators((product.*m_melaProbCPEvenZlepHMember), (product.*m_melaProbCPOddZlepHMember), (product.*m_melaProbCPMixZlepHMember),
		                        (product.*m_melaDiscriminatorD0MinusZlepHMember), (product.*m_melaDiscriminatorDCPZlepHMember));
		CalculateDiscriminators((product.*m_melaProbCPEvenZhadHMember), (product.*m_melaProbCPOddZhadHMember), (product.*m_melaProbCPMixZhadHMember),
		                        (product.*m_melaDiscriminatorD0MinusZhadHMember), (product.*m_melaDiscriminatorDCPZhadHMember));
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
	m_mela->setProcess(TVar::H0minus, TVar::JHUGen, TVar::JJVBF);
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
	m_mela->setProcess(TVar::H0minus, TVar::JHUGen, TVar::Lep_WH);
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
	m_mela->setProcess(TVar::H0minus, TVar::JHUGen, TVar::Had_WH);
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
	m_mela->setProcess(TVar::H0minus, TVar::JHUGen, TVar::Lep_ZH);
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
	m_mela->setProcess(TVar::H0minus, TVar::JHUGen, TVar::Had_ZH);
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


MELAM125Producer::MELAM125Producer(
) :
	MELAProducer(
			"M125",
			&product_type::m_svfitM125Results,
			
			&product_type::m_melaM125ProbCPEvenGGH,
			&product_type::m_melaM125ProbCPOddGGH,
			&product_type::m_melaM125ProbCPMixGGH,
			&product_type::m_melaM125DiscriminatorD0MinusGGH,
			&product_type::m_melaM125DiscriminatorDCPGGH,
	
			&product_type::m_melaM125ProbCPEvenVBF,
			&product_type::m_melaM125ProbCPOddVBF,
			&product_type::m_melaM125ProbCPMixVBF,
			&product_type::m_melaM125DiscriminatorD0MinusVBF,
			&product_type::m_melaM125DiscriminatorDCPVBF
	
			/*
			&product_type::m_melaM125ProbCPEvenWlepH,
			&product_type::m_melaM125ProbCPOddWlepH,
			&product_type::m_melaM125ProbCPMixWlepH,
			&product_type::m_melaM125DiscriminatorD0MinusWlepH,
			&product_type::m_melaM125DiscriminatorDCPWlepH,
	
			&product_type::m_melaM125ProbCPEvenWhadH,
			&product_type::m_melaM125ProbCPOddWhadH,
			&product_type::m_melaM125ProbCPMixWhadH,
			&product_type::m_melaM125DiscriminatorD0MinusWhadH,
			&product_type::m_melaM125DiscriminatorDCPWhadH,
	
			&product_type::m_melaM125ProbCPEvenZlepH,
			&product_type::m_melaM125ProbCPOddZlepH,
			&product_type::m_melaM125ProbCPMixZlepH,
			&product_type::m_melaM125DiscriminatorD0MinusZlepH,
			&product_type::m_melaM125DiscriminatorDCPZlepH,
	
			&product_type::m_melaM125ProbCPEvenZhadH,
			&product_type::m_melaM125ProbCPOddZhadH,
			&product_type::m_melaM125ProbCPMixZhadH,
			&product_type::m_melaM125DiscriminatorD0MinusZhadH,
			&product_type::m_melaM125DiscriminatorDCPZhadH
			*/
	)
{
}

std::string MELAM125Producer::GetProducerId() const
{
	return "MELAM125Producer";
}

