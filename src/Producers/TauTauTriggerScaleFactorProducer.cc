
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauTauTriggerScaleFactorProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
 #include "Artus/KappaAnalysis/interface/Utility/GeneratorInfo.h"

std::string TauTauTriggerScaleFactorProducer::GetProducerId() const
{
	return "TauTauTriggerScaleFactorProducer";
}

void TauTauTriggerScaleFactorProducer::Produce( event_type const& event, product_type & product, 
	                     setting_type const& settings) const
{
	for(int index = 0; index < 2; index++)
    {
        double WeightTau = 1.0;
        auto args = std::vector<double>{product.m_flavourOrderedLeptons[index]->p4.Pt()};
        KGenParticle* genParticle = product.m_flavourOrderedGenLeptons.at(index);
        if (genParticle && (GeneratorInfo::GetGenMatchingCode(genParticle) == KappaEnumTypes::GenMatchingCode::IS_TAU_HAD_DECAY))
        {  
            WeightTau = m_functorTau1->eval(args.data());
        }
        else
        {
            WeightTau = m_functorTau1ss->eval(args.data());
        }
        product.m_weights["triggerWeight_"+std::to_string(index+1)] = WeightTau;
    }

}
