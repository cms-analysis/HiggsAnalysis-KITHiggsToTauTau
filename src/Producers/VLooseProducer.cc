#include "Artus/Utility/interface/SafeMap.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/VLooseProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/Quantities.h"

std::string VLooseProducer::GetProducerId() const
{
	return "VLooseProducer";
}


void VLooseProducer::Produce(event_type const& event, product_type& product,
                                    setting_type const& settings) const
{
    if(m_isSample)
    {


	int hadTau_idMVA_vLoose = -1;
	int hadTau_idMVA_Loose = -1;
	double tau_pt = product.m_flavourOrderedLeptons[1]->p4.Pt();
	double raw_mva = static_cast<KTau*>(product.m_flavourOrderedLeptons[1])->getDiscriminator("byIsolationMVArun2v1DBoldDMwLTraw", event.m_tauMetadata);

	 if ( mvaOutput_normalization_DBoldDMwLT->Eval(raw_mva) > DBoldDMwLTvLoose->Eval(tau_pt) )
	 {
                 hadTau_idMVA_vLoose = 1;
         }
	 else 
	 {
                 hadTau_idMVA_vLoose = 0;
         }
	 if ( mvaOutput_normalization_DBoldDMwLT->Eval(raw_mva) > DBoldDMwLTLoose->Eval(tau_pt) ) 
	 {
                 hadTau_idMVA_Loose = 1;
         }
	 else 
	 {
                 hadTau_idMVA_Loose = 0;
         }

	product.m_optionalWeights["byVLooseIsolationMVAWeight_2"] = hadTau_idMVA_vLoose;
	product.m_optionalWeights["byLooseIsolationMVAWeight_2"] = hadTau_idMVA_Loose;
    
    }
}
