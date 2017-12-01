
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MELAProducer.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/Utility.h"

#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>


std::string MELAProducer::GetProducerId() const
{
	return "MELAProducer";
}

void MELAProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	
	m_higgsProductionMode = HttEnumTypes::ToMELAHiggsProductionMode(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetMELAHiggsProductionMode())));
	
	// https://github.com/cms-analysis/HiggsAnalysis-ZZMatrixElement/blob/v2.1.1/MELA/interface/Mela.h
	// https://github.com/cms-analysis/HiggsAnalysis-ZZMatrixElement/blob/v2.1.1/MELA/interface/TVar.hh
	m_mela = std::unique_ptr<Mela>(new Mela(13.0, 125.0, TVar::SILENT));
	
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaProbCPEven", [](event_type const& event, product_type const& product)
	{
		return product.m_melaProbCPEven;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaProbCPOdd", [](event_type const& event, product_type const& product)
	{
		return product.m_melaProbCPOdd;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaProbCPMix", [](event_type const& event, product_type const& product)
	{
		return product.m_melaProbCPMix;
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaDiscriminatorD0Minus", [](event_type const& event, product_type const& product)
	{
		return product.m_melaDiscriminatorD0Minus;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "melaDiscriminatorDCP", [](event_type const& event, product_type const& product)
	{
		return product.m_melaDiscriminatorDCP;
	});
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
		
		// CP even
		if (m_higgsProductionMode == HttEnumTypes::MELAHiggsProductionMode::GGH)
		{
			m_mela->setProcess(TVar::HSMHiggs, TVar::JHUGen, TVar::JJQCD);
		}
		else if (m_higgsProductionMode == HttEnumTypes::MELAHiggsProductionMode::VBF)
		{
			m_mela->setProcess(TVar::HSMHiggs, TVar::JHUGen, TVar::JJVBF);
		}
		m_mela->computeProdP(product.m_melaProbCPEven, false);
		
		// CP odd
		if (m_higgsProductionMode == HttEnumTypes::MELAHiggsProductionMode::GGH)
		{
			m_mela->setProcess(TVar::H0minus, TVar::JHUGen, TVar::JJQCD);
		}
		else if (m_higgsProductionMode == HttEnumTypes::MELAHiggsProductionMode::VBF)
		{
			m_mela->setProcess(TVar::H0minus, TVar::JHUGen, TVar::JJVBF);
		}
		m_mela->computeProdP(product.m_melaProbCPOdd, false);
		
		// CP mixing (maximum)
		if (m_higgsProductionMode == HttEnumTypes::MELAHiggsProductionMode::GGH)
		{
			m_mela->setProcess(TVar::SelfDefine_spin0, TVar::JHUGen, TVar::JJQCD);
			m_mela->selfDHggcoupl[0][gHIGGS_GG_2][0] = 1; // a1
			m_mela->selfDHggcoupl[0][gHIGGS_GG_4][0] = 1; // a3
		}
		else if (m_higgsProductionMode == HttEnumTypes::MELAHiggsProductionMode::VBF)
		{
			m_mela->setProcess(TVar::SelfDefine_spin0, TVar::JHUGen, TVar::JJVBF);
			m_mela->selfDHzzcoupl[0][gHIGGS_VV_1][0] = 1; // a1
			m_mela->selfDHzzcoupl[0][gHIGGS_VV_4][0] = 0.297979; // a3
		}
		m_mela->computeProdP(product.m_melaProbCPMix, false);
		
		if ((product.m_melaProbCPEven + product.m_melaProbCPOdd) != 0.0)
		{
			product.m_melaDiscriminatorD0Minus = product.m_melaProbCPEven / (product.m_melaProbCPEven + product.m_melaProbCPOdd);
			product.m_melaDiscriminatorDCP = (product.m_melaProbCPMix - product.m_melaProbCPEven - product.m_melaProbCPOdd) / (product.m_melaProbCPEven + product.m_melaProbCPOdd);
		}
		
		m_mela->resetInputEvent();
	}
}

