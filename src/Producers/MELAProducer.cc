
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MELAProducer.h"

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
		float probCPEven = 0.0;
		m_mela->computeProdP(probCPEven, false);
		
		// CP odd
		if (m_higgsProductionMode == HttEnumTypes::MELAHiggsProductionMode::GGH)
		{
			m_mela->setProcess(TVar::H0minus, TVar::JHUGen, TVar::JJQCD);
		}
		else if (m_higgsProductionMode == HttEnumTypes::MELAHiggsProductionMode::VBF)
		{
			m_mela->setProcess(TVar::H0minus, TVar::JHUGen, TVar::JJVBF);
		}
		float probCPOdd = 0.0;
		m_mela->computeProdP(probCPOdd, false);
		
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
		float probCPMix = 0.0;
		m_mela->computeProdP(probCPMix, false);
		
		LOG(WARNING) << "probabilities: " << probCPEven << ", " << probCPOdd << ", " << probCPMix;
		
		float discriminatorD0minus = DefaultValues::UndefinedFloat;
		float discriminatorDCP = DefaultValues::UndefinedFloat;
		if ((probCPEven + probCPOdd) != 0.0)
		{
			discriminatorD0minus = probCPEven / (probCPEven + probCPOdd) if ;
			discriminatorDCP = (probCPMix - probCPEven - probCPOdd) / (probCPEven + probCPOdd);
		}
		LOG(WARNING) << "discriminators: " << discriminatorD0minus << ", " << discriminatorDCP;
		
		m_mela->resetInputEvent();
	}
}

