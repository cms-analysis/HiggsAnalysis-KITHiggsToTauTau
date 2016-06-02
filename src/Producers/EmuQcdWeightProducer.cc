
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/EmuQcdWeightProducer.h"
#include <Math/VectorUtil.h>

std::string EmuQcdWeightProducer::GetProducerId() const
{
	return "EmuQcdWeightProducer";
}

void EmuQcdWeightProducer::Produce( event_type const& event, product_type & product, 
	                     setting_type const& settings) const
{

    float qcdWeightUp = 1.;
    float qcdWeightNom = 1.;
    float qcdWeightDown = 1.;
    
    float electronPt = product.m_flavourOrderedLeptons[0]->p4.Pt();
    float muonPt = product.m_flavourOrderedLeptons[1]->p4.Pt();
    float deltaR = ROOT::Math::VectorUtil::DeltaR(product.m_flavourOrderedLeptons[0]->p4, product.m_flavourOrderedLeptons[1]->p4);
    qcdWeightNom = m_qcdWeights->getWeight(electronPt, muonPt, deltaR);
    qcdWeightUp = m_qcdWeights->getWeightUp(electronPt, muonPt, deltaR);
    qcdWeightDown = qcdWeightNom*qcdWeightNom/qcdWeightUp;

    product.m_optionalWeights["emuQcdWeightUp"] = qcdWeightUp;
    product.m_optionalWeights["emuQcdWeightNom"] = qcdWeightNom;
    product.m_optionalWeights["emuQcdWeightDown"] = qcdWeightDown;
}
