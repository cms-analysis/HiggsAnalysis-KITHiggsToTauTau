#include "Artus/Utility/interface/SafeMap.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/PrefiringWeightProducer.h"



PrefiringWeightProducer::~PrefiringWeightProducer()
{
}

std::string PrefiringWeightProducer::GetProducerId() const
{
	return "PrefiringWeightProducer";
}

void PrefiringWeightProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);

	JetPrefireProbabilityFile = settings.GetJetPrefireProbabilityFile();

	TFile* jetPrefireProbabilityTFile = TFile::Open(JetPrefireProbabilityFile.c_str(), "READ");
	jetPrefireProbabilityHist = (TH2F*)jetPrefireProbabilityTFile->Get("L1prefiring_jetpt_2017BtoF");
	jetPrefireProbabilityHist->SetDirectory(nullptr);
	jetPrefireProbabilityTFile->Close();
	delete jetPrefireProbabilityTFile;
}

void PrefiringWeightProducer::Produce(event_type const& event, product_type& product,
                                    setting_type const& settings, metadata_type const& metadata) const
{
	float prefiringWeight = 1.0;
	LOG(DEBUG) << "!!!!!!!!!!!!!!!!!!!!!STARTEVENT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << std::endl;
	for (std::vector<KJet>::const_iterator jet = (event.m_tjets)->begin();
		 jet != (event.m_tjets)->end(); ++jet)
	{
		LOG(DEBUG) << "jet eta: \t \t" << jet->p4.Eta() << std::endl;
		LOG(DEBUG) << "jet pt: \t \t" << jet->p4.Pt() << std::endl;
		float jetPrefireProbability = 0.;
		int Bin;
		if(std::abs(jet->p4.Eta())>=2.0)
		{
			Bin = jetPrefireProbabilityHist->FindBin(jet->p4.Eta(),jet->p4.Pt());
			//std::cout << "found Bin" << std::endl;
			jetPrefireProbability = jetPrefireProbabilityHist->GetBinContent(Bin);
		}
		LOG(DEBUG) << "jetPrefireProbability \t" << jetPrefireProbability << std::endl;
		prefiringWeight = prefiringWeight * (1.-jetPrefireProbability);
		LOG(DEBUG) << "prefiringWeight \t " << prefiringWeight << std::endl;
	}
	LOG(DEBUG) << "----------------------------------------------------------" << std::endl;
	product.m_optionalWeights["prefiringWeight"] = prefiringWeight; 
}

