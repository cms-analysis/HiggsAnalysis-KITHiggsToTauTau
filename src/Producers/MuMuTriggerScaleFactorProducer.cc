
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MuMuTriggerScaleFactorProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
 #include "Artus/KappaAnalysis/interface/Utility/GeneratorInfo.h"

std::string MuMuTriggerScaleFactorProducer::GetProducerId() const
{
	return "MuMuTriggerScaleFactorProducer";
}

void MuMuTriggerScaleFactorProducer::Produce( event_type const& event, product_type & product, 
	                     setting_type const& settings, metadata_type const& metadata) const
{
    double WeightMu = 1.0;
	for(int index = 0; index < 2; index++)
    {
        auto args = std::vector<double>{product.m_flavourOrderedLeptons[index]->p4.Pt(),product.m_flavourOrderedLeptons[index]->p4.Eta(),SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_flavourOrderedLeptons[index], std::numeric_limits<double>::max())};
        WeightMu *= (1.0-m_functorMu->eval(args.data()));
    }
    product.m_weights["triggerWeight"] = 1-WeightMu;

}
