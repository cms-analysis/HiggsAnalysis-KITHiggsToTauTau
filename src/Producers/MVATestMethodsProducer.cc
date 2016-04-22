#include <Math/VectorUtil.h>
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MVATestMethodsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/Quantities.h"
#include "Artus/Utility/interface/DefaultValues.h"

MVATestMethodsProducer::MVATestMethodsProducer() :
	TmvaClassificationMultiReaderBase<HttTypes>(&spec_setting_type::GetMVATestMethodsInputQuantities,
											&spec_setting_type::GetMVATestMethodsMethods,
											&spec_setting_type::GetMVATestMethodsWeights,
											&spec_product_type::m_MVATestMethodsDiscriminators)
{
}

void MVATestMethodsProducer::Init(spec_setting_type const& settings)
{
	uint output_index = 0;
	for (uint NFoldIndex = 0; NFoldIndex < settings.GetMVATestMethodsNFolds().size(); ++NFoldIndex)
	{
		if (settings.GetMVATestMethodsNFolds()[NFoldIndex] <= 1)
		{
			std::string bdt_out_name = settings.GetMVATestMethodsNames()[NFoldIndex];
			LOG(DEBUG) << "fill singlefold training " << bdt_out_name << std::endl;
			LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(bdt_out_name, [bdt_out_name, output_index](spec_event_type const& event, spec_product_type const& product)
			{
				return ((product.m_MVATestMethodsDiscriminators.size() > 0 ) ? product.m_MVATestMethodsDiscriminators[output_index] : DefaultValues::UndefinedFloat);
			});
			output_index += 1;
		}
		else
		{
			for (int TrainingIndex = 1; TrainingIndex <= settings.GetMVATestMethodsNFolds()[NFoldIndex]; ++TrainingIndex)
			{
				std::string bdt_out_name = "T" + boost::lexical_cast<std::string>(TrainingIndex) + settings.GetMVATestMethodsNames()[NFoldIndex];
				LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(bdt_out_name, [bdt_out_name, output_index](spec_event_type const& event, spec_product_type const& product)
				{
					LOG(DEBUG) << "fill NFold training " << bdt_out_name << " with training index " << output_index << std::endl;
					return ((product.m_MVATestMethodsDiscriminators.size() > 0 ) ? product.m_MVATestMethodsDiscriminators[output_index] : DefaultValues::UndefinedFloat);
				});
				output_index += 1;
			}
			output_index -= 1;
			std::string bdt_out_name = settings.GetMVATestMethodsNames()[NFoldIndex];
			LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(bdt_out_name, [bdt_out_name, output_index, settings, NFoldIndex](spec_event_type const& event, spec_product_type const& product)
			{
				int ts_value = (event.m_eventInfo->nEvent)%100, width = 100/settings.GetMVATestMethodsNFolds()[NFoldIndex];
				for (int finalIndex = 1; finalIndex <= settings.GetMVATestMethodsNFolds()[NFoldIndex]; ++finalIndex)
				{
					if( ((finalIndex-1)*width <= ts_value) and (ts_value < finalIndex*width))
					{
						LOG(DEBUG) << "fill combined NFold training " << bdt_out_name << " with TSV " << ts_value << " with index " << output_index-settings.GetMVATestMethodsNFolds()[NFoldIndex]+finalIndex << std::endl;
						return ((product.m_MVATestMethodsDiscriminators.size() > 0 ) ? product.m_MVATestMethodsDiscriminators[output_index-settings.GetMVATestMethodsNFolds()[NFoldIndex]+finalIndex] : DefaultValues::UndefinedFloat);
					}
					else if (((settings.GetMVATestMethodsNFolds()[NFoldIndex]-1)*width <= ts_value) and (ts_value < 100) and (finalIndex == settings.GetMVATestMethodsNFolds()[NFoldIndex])){
						LOG(DEBUG) << "fill combined NFold training " << bdt_out_name << " with TSV " << ts_value << " with index " << output_index-settings.GetMVATestMethodsNFolds()[NFoldIndex]+finalIndex << " in else part" << std::endl;
						return ((product.m_MVATestMethodsDiscriminators.size() > 0 ) ? product.m_MVATestMethodsDiscriminators[output_index-settings.GetMVATestMethodsNFolds()[NFoldIndex]+finalIndex] : DefaultValues::UndefinedFloat);
					}
				}
				return -2.0;
			});
			output_index += 1;
		}
	}
	// has to be called at the end of the subclass function
	TmvaClassificationMultiReaderBase<HttTypes>::Init(settings);
}

void  MVATestMethodsProducer::Produce(spec_event_type const& event,
										spec_product_type& product,
										spec_setting_type const& settings) const
{
	assert(product.m_flavourOrderedLeptons.size() >= 2);
	assert(event.m_tjets);
	assert(event.m_jetMetadata);
	assert(product.m_metUncorr);
	// has to be called at the end of the subclass function
	TmvaClassificationMultiReaderBase<HttTypes>::Produce(event, product, settings);
}

