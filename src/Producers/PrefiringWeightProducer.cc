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
	float prefiringWeight = 1.0, prefiringWeightUp =1.0, prefiringWeightDown = 1.0;
	LOG(DEBUG) << "!!!!!!!!!!!!!!!!!!!!!STARTEVENT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << std::endl;
	
	for (std::vector<KJet>::const_iterator jet = (event.m_tjets)->begin();
		 jet != (event.m_tjets)->end(); ++jet)
	{
		LOG(DEBUG) << "jet eta: \t \t" << jet->p4.Eta() << std::endl;
		LOG(DEBUG) << "jet pt: \t \t" << jet->p4.Pt() << std::endl;
		float jetPrefireProbability =0., jetPrefireProbabilityUp=0., jetPrefireProbabilityDown = 0.;
		float jetPrefireStatError=0., jetPrefire20Error=0., jetPrefireProbabilityShift = 0.;

		if( jet->p4.Pt() < 20.) continue;
		if( std::abs(jet->p4.Eta() <2.)) continue;
		if( std::abs(jet->p4.Eta() >3.)) continue;

		int Bin;
		
		Bin = jetPrefireProbabilityHist->FindBin(jet->p4.Eta(),jet->p4.Pt());
		//std::cout << "found Bin" << std::endl;
		jetPrefireProbability = jetPrefireProbabilityHist->GetBinContent(Bin);
		jetPrefireStatError = jetPrefireProbabilityHist->GetBinError(Bin);
		jetPrefire20Error = 0.2 * jetPrefireProbability;
		//std::cout << "STATISTICAL ERROR \t :" << jetPrefireStatError << std::endl;
		//std::cout << "20 percent ERROR  \t :" << jetPrefire20Error << std::endl;
		jetPrefireProbabilityShift= std::max(jetPrefireStatError, jetPrefire20Error);

		jetPrefireProbabilityUp=std::min(1.f,jetPrefireProbability+jetPrefireProbabilityShift); //make sure its smaller<1
		jetPrefireProbabilityDown=std::max(0.f,jetPrefireProbability-jetPrefireProbabilityShift);//make sure its smaller>0

		//std::cout << "jetPrefireProbability \t" << jetPrefireProbability << std::endl;

		prefiringWeight = prefiringWeight * std::min(1.f,1.f-jetPrefireProbability); //make sure its smaller<1
		//smaller chance for prefireprobability is a shift up in the prefiringweight, (fewer prefiring)
		prefiringWeightUp = prefiringWeight * std::min(1.f,1.f-jetPrefireProbabilityDown); //make sure its smaller<1
		//higher chance for prefireprobability is a shift down in the prefiringweight, (larger prefiring)
		prefiringWeightDown = prefiringWeight * std::min(1.f,1.f-jetPrefireProbabilityUp); //make sure its smaller<1
		
		LOG(DEBUG) << "prefiringWeight \t " << prefiringWeight << std::endl;
		
	}

	LOG(DEBUG) << "----------------------------------------------------------" << std::endl;
	product.m_optionalWeights["prefiringWeight"] = prefiringWeight;
	product.m_optionalWeights["prefiringWeightUp"] = prefiringWeightUp;
	product.m_optionalWeights["prefiringWeightDown"] = prefiringWeightDown;
}

