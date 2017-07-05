#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/WJetsErsatzProducer.h"


std::string WJetsErsatzProducer::GetProducerId() const
{
    return "WJetsErsatzProducer";
}

void WJetsErsatzProducer::Init(setting_type const& settings)
{
    ProducerBase<HttTypes>::Init(settings);
    //std::cout << "WJetsErsatzProducer is initialized" << std::endl;
}

void WJetsErsatzProducer::Produce(event_type const& event, product_type & product, 
                                   setting_type const& settings) const
{
    //std::cout << std::endl;
    //std::cout << "number of valid muons: " << product.m_validMuons.size() << std::endl; 
    //std::cout << "number of invalid muons: " << product.m_invalidMuons.size() << std::endl; 
    //std::cout << "number of valid loose muons: " << product.m_validLooseMuons.size() << std::endl; 
    //std::cout << "number of invalid loose muons: " << product.m_invalidLooseMuons.size() << std::endl; 
    //std::cout << "number of valid veto muons: " << product.m_validVetoMuons.size() << std::endl; 
    //std::cout << "number of invalid veto muons: " << product.m_invalidVetoMuons.size() << std::endl; 
    //std::cout << "number of valid taus: " << product.m_validTaus.size() << std::endl; 
    //std::cout << "number of valid jets: " << product.m_validJets.size() << std::endl; 
    //std::cout << "valid Z boson found? " << product.m_zValid << std::endl;

    // Deciding, which of the Muons for the Z Boson should be cleaned
    product.m_cleanedMuonForWJetsErsatz = bool(event.m_eventInfo->nEvent % 2) ?  product.m_zLeptons.first : product.m_zLeptons.second;
    product.m_leftMuonForWJetsErsatz = bool(event.m_eventInfo->nEvent % 2) ?  product.m_zLeptons.second: product.m_zLeptons.first;

    // Correcting the 4-vector such, that there is a W instead of the Z with the same 3-vector
    RMFLV zBosonP4 = product.m_cleanedMuonForWJetsErsatz->p4 + product.m_leftMuonForWJetsErsatz->p4;
    ROOT::Math::Boost zRestFrameBoost(zBosonP4.BoostToCM());
    float massRatio = 803850.0/911876.0;
    RMFLV neutrinoInZFrame = massRatio*(zRestFrameBoost * product.m_cleanedMuonForWJetsErsatz->p4);
    RMFLV muonInZFrame =massRatio* (zRestFrameBoost * product.m_leftMuonForWJetsErsatz->p4);
    //std::cout << "neutrino in Z frame: " << neutrinoInZFrame.Px() << " " << neutrinoInZFrame.Py() << " " << neutrinoInZFrame.Pz() << " " << neutrinoInZFrame.E() << std::endl;
    //std::cout << "muon in Z frame: " << muonInZFrame.Px() << " " << muonInZFrame.Py() << " " << muonInZFrame.Pz() << " " << muonInZFrame.E() << std::endl;
    

    RMFLV wBosonInRF = neutrinoInZFrame + muonInZFrame;
    //std::cout << "W: " << wBosonInRF.Px() << " " << wBosonInRF.Py() << " " << wBosonInRF.Pz() << " " << wBosonInRF.E() << std::endl;
    //std::cout << "Z: " << zBosonP4.Px() << " " << zBosonP4.Py() << " " << zBosonP4.Pz() << " " << zBosonP4.E() << std::endl;
    //std::cout << "P Magnitude squared " << zBosonP4.P() << " P Magnitude squared self computed " << zBosonP4.Px()*zBosonP4.Px() + zBosonP4.Py()*zBosonP4.Py() + zBosonP4.Pz()*zBosonP4.Pz() << std::endl;

    float wBosonEnergy = std::sqrt(zBosonP4.Px()*zBosonP4.Px() + zBosonP4.Py()*zBosonP4.Py() + zBosonP4.Pz()*zBosonP4.Pz() + wBosonInRF.M2());
    //std::cout << "W Boson energy: " << wBosonEnergy << std::endl;
    RMFLV::BetaVector wBosonBackToLab = zBosonP4.Vect()/wBosonEnergy;
    ROOT::Math::Boost wToLabFrameBoost(wBosonBackToLab);
    RMFLV neutrino = wToLabFrameBoost * neutrinoInZFrame;
    RMFLV muon = wToLabFrameBoost * muonInZFrame;
    product.m_cleanedMuonForWJetsErsatz->p4.SetPxPyPzE(neutrino.Px(),neutrino.Py(),neutrino.Pz(),neutrino.E());
    product.m_leftMuonForWJetsErsatz->p4.SetPxPyPzE(muon.Px(), muon.Py(), muon.Pz(), muon.E());
    //RMFLV wBosonP4 = muon + neutrino;
    //std::cout << "Z pt: " << zBosonP4.Pt() << " Z pz: " << zBosonP4.Pz() << " Z energy: " << zBosonP4.E() << std::endl;
    //std::cout << "W pt: " << wBosonP4.Pt() << " W pz: " << wBosonP4.Pz() << " W energy: " << wBosonP4.E() << std::endl;

    //Update of all relevant collections, which are affected by the manipulation of the muons from the Z Boson.

    //Determining Pt Cuts used on different valid muons
    float signalMuonsPtCut = 0.0;
    float looseMuonsPtCut = 0.0;
    float vetoMuonsPtCut = 0.0;
    for(unsigned int i = 0; i < settings.GetMuonLowerPtCuts().size(); i++)
    {
        //std::cout << "Cut:" << std::stof(settings.GetMuonLowerPtCuts().at(i)) << std::endl; 
        if(std::stof(settings.GetMuonLowerPtCuts().at(i)) > signalMuonsPtCut)
        {
            signalMuonsPtCut = std::stof(settings.GetMuonLowerPtCuts().at(i));
        }
    }
    for(unsigned int i = 0; i < settings.GetLooseMuonLowerPtCuts().size(); i++)
    {
        if(std::stof(settings.GetLooseMuonLowerPtCuts().at(i)) > looseMuonsPtCut)
        {
            looseMuonsPtCut = std::stof(settings.GetLooseMuonLowerPtCuts().at(i));
        }
    }
    for(unsigned int i = 0; i < settings.GetVetoMuonLowerPtCuts().size(); i++)
    {
        if(std::stof(settings.GetVetoMuonLowerPtCuts().at(i)) > vetoMuonsPtCut)
        {
            vetoMuonsPtCut = std::stof(settings.GetVetoMuonLowerPtCuts().at(i));
        }
    }

    //std::cout << "Pt cut thresholds:" << std::endl;
    //std::cout << "Signal" << signalMuonsPtCut << std::endl;
    //std::cout << "Loose" << looseMuonsPtCut << std::endl;
    //std::cout << "Veto" << vetoMuonsPtCut << std::endl;

    // Signal Muons

    //std::cout << "Muon to clean pointer: " << product.m_cleanedMuonForWJetsErsatz << std::endl;
    for(unsigned int i=0; i< product.m_validMuons.size(); i++)
    {
        //std::cout << "Valid muon pointer: " << product.m_validMuons.at(i) << std::endl;
        if(product.m_cleanedMuonForWJetsErsatz == product.m_validMuons.at(i))
        {
            //std::cout << "Cleaning in valid muons: " << product.m_cleanedMuonForWJetsErsatz << std::endl;
            product.m_invalidMuons.push_back(product.m_validMuons.at(i));
            product.m_validMuons.erase(product.m_validMuons.begin()+i);
            i--;
        }
        else if(product.m_leftMuonForWJetsErsatz == product.m_validMuons.at(i) && product.m_leftMuonForWJetsErsatz->p4.Pt() < signalMuonsPtCut)
        {
            //std::cout << "Cleaning in valid muons: " << product.m_leftMuonForWJetsErsatz << std::endl;
            product.m_invalidMuons.push_back(product.m_validMuons.at(i));
            product.m_validMuons.erase(product.m_validMuons.begin()+i);
            i--;
        }
    }
    std::sort(product.m_invalidMuons.begin(), product.m_invalidMuons.end(),
                      [](KMuon* muon1, KMuon* muon2) -> bool
                      { return muon1->p4.Pt() > muon2->p4.Pt(); });

    // Loose Muons

    for(unsigned int i=0; i< product.m_validLooseMuons.size(); i++)
    {
        //std::cout << "Valid loose muon pointer: " << product.m_validLooseMuons.at(i) << std::endl;
        if(product.m_cleanedMuonForWJetsErsatz == product.m_validLooseMuons.at(i))
        {
            //std::cout << "Cleaning in valid loose muons: " << product.m_cleanedMuonForWJetsErsatz << std::endl;
            product.m_invalidLooseMuons.push_back(product.m_validLooseMuons.at(i));
            product.m_validLooseMuons.erase(product.m_validLooseMuons.begin()+i);
            i--;
        }
        else if(product.m_leftMuonForWJetsErsatz == product.m_validLooseMuons.at(i) && product.m_leftMuonForWJetsErsatz->p4.Pt() < looseMuonsPtCut)
        {
            //std::cout << "Cleaning in valid muons: " << product.m_leftMuonForWJetsErsatz << std::endl;
            product.m_invalidLooseMuons.push_back(product.m_validLooseMuons.at(i));
            product.m_validLooseMuons.erase(product.m_validLooseMuons.begin()+i);
            i--;
        }
    }
    std::sort(product.m_invalidLooseMuons.begin(), product.m_invalidLooseMuons.end(),
                      [](KMuon* muon1, KMuon* muon2) -> bool
                      { return muon1->p4.Pt() > muon2->p4.Pt(); });

    // Veto Muons

    for(unsigned int i=0; i< product.m_validVetoMuons.size(); i++)
    {
        //std::cout << "Valid veto muon pointer: " << product.m_validVetoMuons.at(i) << std::endl;
        if(product.m_cleanedMuonForWJetsErsatz == product.m_validVetoMuons.at(i))
        {
            //std::cout << "Cleaning in valid veto muons: " << product.m_cleanedMuonForWJetsErsatz << std::endl;
            product.m_invalidVetoMuons.push_back(product.m_validVetoMuons.at(i));
            product.m_validVetoMuons.erase(product.m_validVetoMuons.begin()+i);
            i--;
        }
        else if(product.m_leftMuonForWJetsErsatz == product.m_validVetoMuons.at(i)  && product.m_leftMuonForWJetsErsatz->p4.Pt() < vetoMuonsPtCut)
        {
            //std::cout << "Cleaning in valid muons: " << product.m_leftMuonForWJetsErsatz << std::endl;
            product.m_invalidVetoMuons.push_back(product.m_validVetoMuons.at(i));
            product.m_validVetoMuons.erase(product.m_validVetoMuons.begin()+i);
            i--;
        }
    }
    std::sort(product.m_invalidVetoMuons.begin(), product.m_invalidVetoMuons.end(),
                      [](KMuon* muon1, KMuon* muon2) -> bool
                      { return muon1->p4.Pt() > muon2->p4.Pt(); });
    //std::cout << "Event: " << event.m_eventInfo->nEvent << std::endl;
    // Removing taus within Delta R = 0.3
    for(unsigned int i=0; i< product.m_validTaus.size(); i++)
    {
        //std::cout << "Valid Tau pointer: " << product.m_validTaus.at(i) << std::endl;
        if(ROOT::Math::VectorUtil::DeltaR(product.m_cleanedMuonForWJetsErsatz->p4,product.m_validTaus.at(i)->p4) < 0.3)
        {
            //std::cout << "Cleaning Tau: " << product.m_validTaus.at(i) << std::endl;
            product.m_invalidTaus.push_back(product.m_validTaus.at(i));
            product.m_validTaus.erase(product.m_validTaus.begin()+i);
            i--;
        }
    }
    std::sort(product.m_invalidTaus.begin(), product.m_invalidTaus.end(),
                      [](KTau* tau1, KTau* tau2) -> bool
                      { return tau1->p4.Pt() > tau2->p4.Pt(); });
    // Removing jets within Delta R = 0.3
    for(unsigned int i=0; i< product.m_validJets.size(); i++)
    {
        //std::cout << "Valid Jets pointer: " << product.m_validJets.at(i) << std::endl;
        if(ROOT::Math::VectorUtil::DeltaR(product.m_cleanedMuonForWJetsErsatz->p4,product.m_validJets.at(i)->p4) < 0.3)
        {
            //std::cout << "Cleaning Tau: " << product.m_validJets.at(i) << std::endl;
            product.m_invalidJets.push_back(product.m_validJets.at(i));
            product.m_validJets.erase(product.m_validJets.begin()+i);
            i--;
        }
    }
    std::sort(product.m_invalidJets.begin(), product.m_invalidJets.end(),
                      [](KBasicJet* jet1, KBasicJet* jet2) -> bool
                      { return jet1->p4.Pt() > jet2->p4.Pt(); });
    
}
