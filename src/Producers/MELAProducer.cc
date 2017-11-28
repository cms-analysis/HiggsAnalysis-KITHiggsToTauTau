
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MELAProducer.h"

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
	if (metadata.m_mela == nullptr)
	{
		metadata.m_mela = new Mela(13.0, 125.0, TVar::SILENT);
	}
}


void MELAProducer::Produce(event_type const& event, product_type& product,
                           setting_type const& settings, metadata_type const& metadata) const
{
	if (product.m_svfitResults.fittedHiggsLV != nullptr)
	{
		SimpleParticleCollection_t daughters; // Higgs boson or two tau leptons
		SimpleParticleCollection_t associated; // additional reconstructed jets
		SimpleParticleCollection_t mothers; // incoming partons in case of gen level mode
		
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
		
		metadata.m_mela->setInputEvent(&daughters, &associated, &mothers, false);
		
		metadata.m_mela->setProcess(TVar::HSMHiggs, TVar::JHUGen, TVar::ZZGG); // TODO
		float result = 0.0;
		metadata.m_mela->computeProdP(result, true);
		LOG(INFO) << "production matrix element: " << result;
		
		metadata.m_mela->resetInputEvent();
	}
}

