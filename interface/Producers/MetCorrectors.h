
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/ProducerBase.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/RecoilCorrector.h"

#include <boost/regex.hpp>


/**
   \brief Corrects the MET created by the MET producer
   
   Run this producer after the Valid(Tagged)JetsProducer, since it relies on the number of
   jets in the event.
*/


template<class TMet>
class MetCorrectorBase: public ProducerBase<HttTypes>
{
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	MetCorrectorBase(TMet* product_type::*metMemberUncorrected,
			 TMet product_type::*metMemberCorrected,
			 std::vector<float> product_type::*metCorrections,
			 std::string (setting_type::*GetRecoilCorrectorFile)(void) const
	) :
		ProducerBase<HttTypes>(),
		m_metMemberUncorrected(metMemberUncorrected),
		m_metMemberCorrected(metMemberCorrected),
		m_metCorrections(metCorrections),
		GetRecoilCorrectorFile(GetRecoilCorrectorFile)
	{
	}

	virtual void Init(setting_type const& settings) override
	{
		ProducerBase<HttTypes>::Init(settings);
		
		m_recoilCorrector = new RecoilCorrector((settings.*GetRecoilCorrectorFile)());
	}

	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings) const override
	{
		assert(m_metMemberUncorrected != nullptr);
		
		// Retrieve the needed informations from the event content
		float metX = (product.*m_metMemberUncorrected)->p4.Px();
		float metY = (product.*m_metMemberUncorrected)->p4.Py();
		float metEnergy = (product.*m_metMemberUncorrected)->p4.energy();
		float metResolution = std::sqrt(metEnergy * metEnergy - metX * metX - metY * metY);
		int nJets30 = product_type::GetNJetsAbovePtThreshold(product.m_validJets, 30.0);
		
		// In selected W+Jets events one of the leptons is faked by hadronic jet and this 
		// jet should be counted as a part of hadronic recoil to the W boson
		if (boost::regex_search(product.m_nickname, boost::regex("W.?JetsToLNu", boost::regex::icase | boost::regex::extended)))
		{
			nJets30 += 1;
		}
		
		float genPx = 0.;  // generator Z(W) px
		float genPy = 0.;  // generator Z(W) py
		float visPx = 0.;  // visible (generator) Z(W) px
		float visPy = 0.;  // visible (generator) Z(W) py
		
		for (KGenParticles::const_iterator genParticle = event.m_genParticles->begin();
		 genParticle != event.m_genParticles->end(); ++genParticle)
		{
			int pdgId = std::abs(genParticle->pdgId);     
			
			if ( (pdgId >= DefaultValues::pdgIdElectron && pdgId <= DefaultValues::pdgIdNuTau && genParticle->fromHardProcessFinalState()) ||
			     (genParticle->isDirectHardProcessTauDecayProduct()) )
			{
				genPx += genParticle->p4.Px();
				genPy += genParticle->p4.Py();
				
				if ( !(pdgId == DefaultValues::pdgIdNuE || pdgId == DefaultValues::pdgIdNuMu || pdgId == DefaultValues::pdgIdNuTau) )
				{
					visPx += genParticle->p4.Px();
					visPy += genParticle->p4.Py();
				}
			}
		}
		
		// Save the ingredients for the correction
		(product.*m_metCorrections).push_back(genPx);
		(product.*m_metCorrections).push_back(genPy);
		(product.*m_metCorrections).push_back(visPx);
		(product.*m_metCorrections).push_back(visPy);
		
		float correctedMetX, correctedMetY;
		
		m_recoilCorrector->CorrectByMeanResolution(
			metX,
			metY,
			genPx,
			genPy,
			visPx,
			visPy,
			nJets30,
			correctedMetX,
			correctedMetY);
		
		// Apply the correction to the MET object
		(product.*m_metMemberCorrected) = *(product.*m_metMemberUncorrected);
		(product.*m_metMemberCorrected).p4.SetPxPyPzE(
			correctedMetX,
			correctedMetY,
			0.,
			std::sqrt(metResolution * metResolution + correctedMetX * correctedMetX + correctedMetY * correctedMetY));
	}

protected:
	TMet* product_type::*m_metMemberUncorrected;
	TMet product_type::*m_metMemberCorrected;
	std::vector<float> product_type::*m_metCorrections;
	std::string (setting_type::*GetRecoilCorrectorFile)(void) const;
	RecoilCorrector* m_recoilCorrector;
};



/**
   \brief Corrector for (PF) MET
*/
class MetCorrector: public MetCorrectorBase<KMET>
{
public:
	MetCorrector();
	virtual void Init(setting_type const& settings) override;
	virtual std::string GetProducerId() const override;
};

/**
   \brief Corrector for MVAMET
*/
class MvaMetCorrector: public MetCorrectorBase<KMET>
{
public:
	MvaMetCorrector();
	virtual void Init(setting_type const& settings) override;
	virtual std::string GetProducerId() const override;
};
