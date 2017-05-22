
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/ZPtReweightProducer.h"


std::string ZPtReweightProducer::GetProducerId() const
{
	return "ZPtReweightProducer";
}

void ZPtReweightProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
	TDirectory *savedir(gDirectory);
	TFile *savefile(gFile);
	TFile f(settings.GetZptRooWorkspace().c_str());
	gSystem->AddIncludePath("-I$ROOFITSYS/include");
	m_workspace = (RooWorkspace*)f.Get("w");
	f.Close();
	gDirectory = savedir;
	gFile = savefile;

	m_ZptWeightFunktor = m_workspace->function("zpt_weight_nom")->functor(m_workspace->argSet({"z_gen_mass,z_gen_pt"}));
	if (settings.GetDoZptUncertainties())
	{
		m_ZptWeightUncertaintiesFunktor["zPtWeightEsUp"] = m_workspace->function("zpt_weight_esup")->functor(m_workspace->argSet("z_gen_mass,z_gen_pt"));
		m_ZptWeightUncertaintiesFunktor["zPtWeightEsDown"] = m_workspace->function("zpt_weight_esdown")->functor(m_workspace->argSet("z_gen_mass,z_gen_pt"));
		m_ZptWeightUncertaintiesFunktor["zPtWeightStatPt0Up"] = m_workspace->function("zpt_weight_statpt0up")->functor(m_workspace->argSet("z_gen_mass,z_gen_pt"));
		m_ZptWeightUncertaintiesFunktor["zPtWeightStatPt0Down"] = m_workspace->function("zpt_weight_statpt0down")->functor(m_workspace->argSet("z_gen_mass,z_gen_pt"));
		m_ZptWeightUncertaintiesFunktor["zPtWeightStatPt40Up"] = m_workspace->function("zpt_weight_statpt40up")->functor(m_workspace->argSet("z_gen_mass,z_gen_pt"));
		m_ZptWeightUncertaintiesFunktor["zPtWeightStatPt40Down"] = m_workspace->function("zpt_weight_statpt40down")->functor(m_workspace->argSet("z_gen_mass,z_gen_pt"));
		m_ZptWeightUncertaintiesFunktor["zPtWeightStatPt80Up"] = m_workspace->function("zpt_weight_statpt80up")->functor(m_workspace->argSet("z_gen_mass,z_gen_pt"));
		m_ZptWeightUncertaintiesFunktor["zPtWeightStatPt80Down"] = m_workspace->function("zpt_weight_statpt80down")->functor(m_workspace->argSet("z_gen_mass,z_gen_pt"));
		m_ZptWeightUncertaintiesFunktor["zPtWeightTTbarUp"] = m_workspace->function("zpt_weight_ttup")->functor(m_workspace->argSet("z_gen_mass,z_gen_pt"));
		m_ZptWeightUncertaintiesFunktor["zPtWeightTTbarDown"] = m_workspace->function("zpt_weight_ttdown")->functor(m_workspace->argSet("z_gen_mass,z_gen_pt"));
	}
	
	m_applyReweighting = boost::regex_search(settings.GetNickname(), boost::regex("DY.?JetsToLLM(50|150)", boost::regex::icase | boost::regex::extended));
}

void ZPtReweightProducer::Produce( event_type const& event, product_type & product, 
	                     setting_type const& settings) const
{
	float genPt = 0.;  // generator Z(W) pt
	float genMass = 0.;  // generator Z(W) mass
	RMFLV genMomentum;
	if (m_applyReweighting)
	{
		for (KGenParticles::const_iterator genParticle = event.m_genParticles->begin();
		genParticle != event.m_genParticles->end(); ++genParticle)
		{
			int pdgId = std::abs(genParticle->pdgId);
			
			if ( (pdgId >= DefaultValues::pdgIdElectron && pdgId <= DefaultValues::pdgIdNuTau && genParticle->fromHardProcessFinalState()) || (genParticle->isDirectHardProcessTauDecayProduct()) )
			{
				genMomentum += genParticle->p4;
			}
		}
		genPt = genMomentum.Pt();
		genMass = genMomentum.M();
		auto args = std::vector<double>{genMass,genPt};
		product.m_optionalWeights["zPtReweightWeight"] = m_ZptWeightFunktor->eval(args.data());
		if (settings.GetDoZptUncertainties())
		{
			for(auto uncertainty: m_ZptWeightUncertaintiesFunktor)
			{
				product.m_optionalWeights[uncertainty.first] = uncertainty.second->eval(args.data());
			}
		}
	}
}
