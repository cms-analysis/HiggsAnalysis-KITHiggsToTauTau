
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TTHTauPairProducer.h"


void TTHTauPairProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
}

void TTHTauPairProducer::Produce(event_type const& event, product_type& product,
	                         setting_type const& settings) const
{
	
	size_t nTaus = product.m_validTaus.size();
	
	KDataPFTau* tau1;
	KDataPFTau* tau2;
	
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
			float iso1 = tau1->getDiscriminator("hpsPFTauDiscriminationByIsolationMVA2raw", event.m_tauDiscriminatorMetadata);
			float iso2 = tau2->getDiscriminator("hpsPFTauDiscriminationByIsolationMVA2raw", event.m_tauDiscriminatorMetadata);
			
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
			product.m_validTTHTaus.push_back(product.m_validTaus[selectedTau1]);
			product.m_validTTHTaus.push_back(product.m_validTaus[selectedTau2]);
		}
}

