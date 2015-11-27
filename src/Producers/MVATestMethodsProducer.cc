
#include <Math/VectorUtil.h>

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MVATestMethodsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/Quantities.h"
#include "Artus/Utility/interface/DefaultValues.h"

    
MVATestMethodsProducer::MVATestMethodsProducer() :
    TmvaClassificationReaderBase<HttTypes>(&spec_setting_type::GetMVATestMethodsInputQuantities,
                                           &spec_setting_type::GetMVATestMethodsMethods,
                                           &spec_setting_type::GetMVATestMethodsWeights,
                                           &spec_product_type::m_MVATestMethodsDiscriminators)
{
}

void MVATestMethodsProducer::Init(spec_setting_type const& settings)
{
    
    for (size_t mvaMethodIndex = 0; mvaMethodIndex < (settings.GetMVATestMethodsMethods)().size(); ++mvaMethodIndex)
        {
            std::string bdt_out_name = "MVATestMethod_" + boost::lexical_cast<std::string>(mvaMethodIndex);
            LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(bdt_out_name, [bdt_out_name, mvaMethodIndex](spec_event_type const& event, spec_product_type const& product)
            {    
                return ((product.m_MVATestMethodsDiscriminators.size() > 0 ) ? product.m_MVATestMethodsDiscriminators[mvaMethodIndex] : DefaultValues::UndefinedFloat);
            });
        }
    
    // has to be called at the end of the subclass function
    TmvaClassificationReaderBase<HttTypes>::Init(settings);
}

void  MVATestMethodsProducer::Produce(spec_event_type const& event,
                                               spec_product_type& product,
                                               spec_setting_type const& settings) const
{
    assert(product.m_flavourOrderedLeptons.size() >= 2);
    assert(event.m_tjets);
    assert(event.m_jetMetadata);
    assert(product.m_met);
    
    // has to be called at the end of the subclass function
    TmvaClassificationReaderBase<HttTypes>::Produce(event, product, settings);
}

