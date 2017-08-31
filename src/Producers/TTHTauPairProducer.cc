
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TTHTauPairProducer.h"


void TTHTauPairProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "TTHTau1Pt", [this](HttTypes::event_type const& event, HttTypes::product_type const& product) {
		return product.m_validTTHTaus[0]->p4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "TTHTau2Pt", [this](HttTypes::event_type const& event, HttTypes::product_type const& product) {
		return product.m_validTTHTaus[1]->p4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "TTHTau1Eta", [this](HttTypes::event_type const& event, HttTypes::product_type const& product) {
		return product.m_validTTHTaus[0]->p4.Eta();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "TTHTau2Eta", [this](HttTypes::event_type const& event, HttTypes::product_type const& product) {
		return product.m_validTTHTaus[1]->p4.Eta();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "TTHTau1Iso", [this](HttTypes::event_type const& event, HttTypes::product_type const& product) {
		return product.m_validTTHTaus[0]->getDiscriminator("hpsPFTauDiscriminationByIsolationMVA2raw", event.m_tauMetadata);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "TTHTau2Iso", [this](HttTypes::event_type const& event, HttTypes::product_type const& product) {
		return product.m_validTTHTaus[1]->getDiscriminator("hpsPFTauDiscriminationByIsolationMVA2raw", event.m_tauMetadata);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "TTHTau1DecayMode", [this](HttTypes::event_type const& event, HttTypes::product_type const& product) {
		return product.m_validTTHTaus[0]->decayMode;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "TTHTau2DecayMode", [this](HttTypes::event_type const& event, HttTypes::product_type const& product) {
		return product.m_validTTHTaus[1]->decayMode;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "TTHTau1EleDeltaR", [this](HttTypes::event_type const& event, HttTypes::product_type const& product) {
		return product.m_validElectrons.size() >=1 ?  ROOT::Math::VectorUtil::DeltaR(product.m_validElectrons[0]->p4, product.m_validTTHTaus[0]->p4) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "TTHTau1MuonDeltaR", [this](HttTypes::event_type const& event, HttTypes::product_type const& product) {
		return product.m_validMuons.size() >=1 ?  ROOT::Math::VectorUtil::DeltaR(product.m_validMuons[0]->p4, product.m_validTTHTaus[0]->p4) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "TTHTau2EleDeltaR", [this](HttTypes::event_type const& event, HttTypes::product_type const& product) {
		return product.m_validElectrons.size() >=1 ?  ROOT::Math::VectorUtil::DeltaR(product.m_validElectrons[0]->p4, product.m_validTTHTaus[1]->p4) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "TTHTau2MuonDeltaR", [this](HttTypes::event_type const& event, HttTypes::product_type const& product) {
		return product.m_validMuons.size() >=1 ?  ROOT::Math::VectorUtil::DeltaR(product.m_validMuons[0]->p4, product.m_validTTHTaus[1]->p4) : DefaultValues::UndefinedDouble;
	});
}

void TTHTauPairProducer::Produce(event_type const& event, product_type& product,
	                         setting_type const& settings, metadata_type const& metadata) const
{
	
	size_t nTaus = product.m_validTaus.size();
	
	KTau* tau1;
	KTau* tau2;
	
	int nPossiblePairs = 0;
	unsigned int selectedTau1 = 0;
	unsigned int selectedTau2 = 0;
	
	float combinedIso = std::numeric_limits<float>::min();
	
	for (unsigned int iTau = 0; iTau < nTaus; iTau++) {
		for (unsigned int jTau = iTau+1; jTau < nTaus; jTau++) {
			
			tau1 = product.m_validTaus[iTau];
			tau2 = product.m_validTaus[jTau];
			
			//require a separation in DeltaR among the tau candidates
			if (ROOT::Math::VectorUtil::DeltaR(tau1->p4, tau2->p4) <= settings.GetTauTauLowerDeltaRCut())
				continue;
		
			//check the combined isolation of the tau pair
			float iso1 = tau1->getDiscriminator("hpsPFTauDiscriminationByIsolationMVA2raw", event.m_tauMetadata);
			float iso2 = tau2->getDiscriminator("hpsPFTauDiscriminationByIsolationMVA2raw", event.m_tauMetadata);
			
			float tempCombinedIso = (iso1 + 1.0)*(iso1 + 1.0) + (iso2 + 1.0)*(iso2 + 1.0);
			
			if (tempCombinedIso > combinedIso)
				{
					combinedIso = tempCombinedIso;
					
					nPossiblePairs++;
					selectedTau1 = iTau;
					selectedTau2 = jTau;
				}
		}
	}
	
	//require at least one tau pair
	if (nPossiblePairs != 0)
		{
			//choose the pair with the highest value of the combined isolation
			//the pair is already pT-ordered
			product.m_validTTHTaus.push_back(product.m_validTaus[selectedTau1]);
			product.m_validTTHTaus.push_back(product.m_validTaus[selectedTau2]);
		}
}

