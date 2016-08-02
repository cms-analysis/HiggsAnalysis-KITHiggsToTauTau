
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/RooWorkspaceWeightProducer.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/SafeMap.h"

std::string RooWorkspaceWeightProducer::GetProducerId() const
{
	return "RooWorkspaceWeightProducer";
}

void RooWorkspaceWeightProducer::Produce( event_type const& event, product_type & product, 
	                     setting_type const& settings) const
{

    for(auto weightNames:m_weightNames)
    {
        KLepton* lepton = product.m_flavourOrderedLeptons[weightNames.first];
        for(size_t index = 0; index < weightNames.second.size(); index++)
        {
            auto args = std::vector<double>{};
            std::vector<std::string> arguments;
            boost::split(arguments,  m_functorArgs.at(weightNames.first).at(index) , boost::is_any_of(","));
            for(auto arg:arguments)
            {
                if(arg=="m_pt")
                {
                    args.push_back(lepton->p4.Pt());
                }
                if(arg=="m_eta")
                {
                    args.push_back(lepton->p4.Eta());
                }
                if(arg=="m_iso")
                {
                    args.push_back(SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, lepton, std::numeric_limits<double>::max()));
                }
            }
            //std::cout << weightNames.second.at(index) << std::endl;
            //for(auto arg:arguments) std::cout << arg << " ";
            //for(auto arg:args) std::cout << arg << " ";
            //std::cout << std::endl << m_functors.at(weightNames.first).at(index)->eval(args.data()) << std::endl;
            product.m_weights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = m_functors.at(weightNames.first).at(index)->eval(args.data());
        }
    }
    if((product.m_weights.find("idweight_1") != product.m_weights.end()) && (product.m_weights.find("idweight_1") != product.m_weights.end()))
    {
        product.m_weights["identificationWeight_1"] = product.m_weights["idweight_1"]*product.m_weights["isoweight_1"];
        product.m_weights["idweight_1"] = 1.0;
        product.m_weights["isoweight_1"] = 1.0;
    }
}
