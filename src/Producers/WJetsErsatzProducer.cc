#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/WJetsErsatzProducer.h"


std::string WJetsErsatzProducer::GetProducerId() const
{
    return "WJetsErsatzProducer";
}

void WJetsErsatzProducer::Init(setting_type const& settings)
{
    ProducerBase<HttTypes>::Init(settings);
    ////std::cout << "WJetsErsatzProducer is initialized" << std::endl;
}

void WJetsErsatzProducer::Produce(event_type const& event, product_type & product, 
                                   setting_type const& settings) const
{
    //std::cout << std::endl;
    //std::cout << "--------  WJetsErsatzProducer running  --------" << std::endl;
    //std::cout << "number of valid muons: " << product.m_validMuons.size() << std::endl; 
    //std::cout << "number of invalid muons: " << product.m_invalidMuons.size() << std::endl; 
    //std::cout << "number of valid loose muons: " << product.m_validLooseMuons.size() << std::endl; 
    //std::cout << "number of invalid loose muons: " << product.m_invalidLooseMuons.size() << std::endl; 
    //std::cout << "number of valid veto muons: " << product.m_validVetoMuons.size() << std::endl; 
    //std::cout << "number of invalid veto muons: " << product.m_invalidVetoMuons.size() << std::endl; 
    //std::cout << "number of valid taus: " << product.m_validTaus.size() << std::endl; 
    //std::cout << "number of valid jets: " << product.m_validJets.size() << std::endl; 
    //std::cout << "number of valid btagged jets: " << product.m_bTaggedJets.size() << std::endl; 
    //std::cout << "valid Z boson found? " << product.m_zValid << std::endl;
    //std::cout << std::setprecision(9);

    // Deciding, which of the Muons for the Z Boson should be cleaned
    product.m_cleanedMuonForWJetsErsatz = bool(event.m_eventInfo->nEvent % 2) ?  product.m_zLeptons.first : product.m_zLeptons.second;
    product.m_leftMuonForWJetsErsatz = bool(event.m_eventInfo->nEvent % 2) ?  product.m_zLeptons.second: product.m_zLeptons.first;
    double muon_mass = product.m_leftMuonForWJetsErsatz->p4.M();
    //std::cout << "mu1 in lab Pt, Eta, Phi, M, E " << product.m_cleanedMuonForWJetsErsatz->p4.Pt() << " " << product.m_cleanedMuonForWJetsErsatz->p4.Eta() << " " << product.m_cleanedMuonForWJetsErsatz->p4.Phi() << " " << product.m_cleanedMuonForWJetsErsatz->p4.M() << " " << product.m_cleanedMuonForWJetsErsatz->p4.E() << std::endl;
    //std::cout << "mu2 in lab Pt, Eta, Phi, M, E " <<  product.m_leftMuonForWJetsErsatz->p4.Pt() << " " << product.m_leftMuonForWJetsErsatz->p4.Eta() << " " << product.m_leftMuonForWJetsErsatz->p4.Phi() << " " << product.m_leftMuonForWJetsErsatz->p4.M() << " " <<  product.m_leftMuonForWJetsErsatz->p4.E() << std::endl;

    // Correcting the 4-vector such, that there is a W instead of the Z with the same 3-vector
    RMFLV zBosonP4 = product.m_cleanedMuonForWJetsErsatz->p4 + product.m_leftMuonForWJetsErsatz->p4;
    ROOT::Math::Boost zRestFrameBoost(zBosonP4.BoostToCM());
    float massRatio = 803850.0/911876.0;
    RMFLV neutrinoInZFrame = zRestFrameBoost * product.m_cleanedMuonForWJetsErsatz->p4;
    RMFLV muonInZFrame = zRestFrameBoost * product.m_leftMuonForWJetsErsatz->p4;
    //std::cout << "mu1 neutrino in Z rest frame Pt, Eta, Phi, M, E " <<  neutrinoInZFrame.Pt() << " " << neutrinoInZFrame.Eta() << " " << neutrinoInZFrame.Phi() << " " << neutrinoInZFrame.M() << " " << neutrinoInZFrame.E() << std::endl;
    //std::cout << "mu2 muon in Z rest frame Pt, Eta, Phi, M, E " <<  muonInZFrame.Pt() << " " << muonInZFrame.Eta() << " " << muonInZFrame.Phi() << " " << muonInZFrame.M() << " " << muonInZFrame.E() << std::endl;
    neutrinoInZFrame = massRatio*(zRestFrameBoost * product.m_cleanedMuonForWJetsErsatz->p4);
    muonInZFrame = massRatio*(zRestFrameBoost * product.m_leftMuonForWJetsErsatz->p4);
    //std::cout << "mu1 neutrino in W rest frame Pt, Eta, Phi, M, E, P " <<  neutrinoInZFrame.Pt() << " " << neutrinoInZFrame.Eta() << " " << neutrinoInZFrame.Phi() << " " << neutrinoInZFrame.M() << " " << neutrinoInZFrame.E() << " " << neutrinoInZFrame.P() << std::endl;
    //std::cout << "mu2 muon in W rest frame Pt, Eta, Phi, M, E, P " <<  muonInZFrame.Pt() << " " << muonInZFrame.Eta() << " " << muonInZFrame.Phi() << " " << muonInZFrame.M() << " " << muonInZFrame.E() << " " << muonInZFrame.P() << std::endl;


    RMFLV wBosonInRF = neutrinoInZFrame + muonInZFrame;
    // muon mass correction
    double muon_energy = wBosonInRF.M()/2;
    //std::cout << "W-Boson mass: " << wBosonInRF.M() <<  " muon energy: " << muon_energy << " muon mass: " << muon_mass << std::endl;
    //std::cout << "Magnitude self computed " << std::sqrt(muonInZFrame.Px()*muonInZFrame.Px() + muonInZFrame.Py()*muonInZFrame.Py() + muonInZFrame.Pz()*muonInZFrame.Pz()) << std::endl;
    //std::cout << "Magnitude ROOT " << muonInZFrame.P() << std::endl;
    double abs_desired_3p = std::sqrt(muon_energy*muon_energy - muon_mass*muon_mass);
    double sf = abs_desired_3p/muonInZFrame.P();
    //std::cout << "scale factor muon mass: " << sf << std::endl;
    RMFLV new_neutrino2(std::sqrt(sf*neutrinoInZFrame.Px()*sf*neutrinoInZFrame.Px() + sf*neutrinoInZFrame.Py()*sf*neutrinoInZFrame.Py()),neutrinoInZFrame.Eta(), neutrinoInZFrame.Phi(), muon_mass);
    neutrinoInZFrame = new_neutrino2;
    RMFLV new_muon2(std::sqrt(sf*muonInZFrame.Px()*sf*muonInZFrame.Px() + sf*muonInZFrame.Py()*sf*muonInZFrame.Py()), muonInZFrame.Eta(), muonInZFrame.Phi(), muon_mass);
    muonInZFrame = new_muon2;
    //std::cout << "mu1 neutrino in W rest frame after muon mass correction Pt, Eta, Phi, M, E, P " <<  neutrinoInZFrame.Pt() << " " << neutrinoInZFrame.Eta() << " " << neutrinoInZFrame.Phi() << " " << neutrinoInZFrame.M() << " " << neutrinoInZFrame.E() << " " << neutrinoInZFrame.P() << std::endl;
    //std::cout << "mu2 muon in W rest frame after muon mass correction Pt, Eta, Phi, M, E, P " <<  muonInZFrame.Pt() << " " << muonInZFrame.Eta() << " " << muonInZFrame.Phi() << " " << muonInZFrame.M() << " " << muonInZFrame.E() << " " << muonInZFrame.P() << std::endl;

    // neutrino mass correction
    double sf2 = (3*muon_energy*muon_energy + muonInZFrame.P()*muonInZFrame.P())/(4*muon_energy*muonInZFrame.P());
    //std::cout << "scale factor neutrino mass: " << sf2 << std::endl;
    //double new_muon_energy = std::sqrt(muon_energy*muon_energy + (sf2*sf2 -1)*muonInZFrame.P()*muonInZFrame.P());
    //std::cout << "muon energy after neutrino correction computed: " << new_muon_energy << std::endl;
    RMFLV new_neutrino(std::sqrt(sf2*neutrinoInZFrame.Px()*sf2*neutrinoInZFrame.Px() + sf2*neutrinoInZFrame.Py()*sf2*neutrinoInZFrame.Py()),neutrinoInZFrame.Eta(), neutrinoInZFrame.Phi(), 0.0);
    neutrinoInZFrame = new_neutrino;
    RMFLV new_muon(std::sqrt(sf2*muonInZFrame.Px()*sf2*muonInZFrame.Px() + sf2*muonInZFrame.Py()*sf2*muonInZFrame.Py()), muonInZFrame.Eta(), muonInZFrame.Phi(), muon_mass);
    muonInZFrame = new_muon;
    //std::cout << "mu1 neutrino in W rest frame after neutrino mass correction Pt, Eta, Phi, M, E " <<  neutrinoInZFrame.Pt() << " " << neutrinoInZFrame.Eta() << " " << neutrinoInZFrame.Phi() << " " << neutrinoInZFrame.M() << " " << neutrinoInZFrame.E() << std::endl;
    //std::cout << "mu2 muon in W rest frame after neutrino mass correction Pt, Eta, Phi, M, E " <<  muonInZFrame.Pt() << " " << muonInZFrame.Eta() << " " << muonInZFrame.Phi() << " " << muonInZFrame.M() << " " << muonInZFrame.E() << std::endl;

    ////std::cout << "W: " << wBosonInRF.Px() << " " << wBosonInRF.Py() << " " << wBosonInRF.Pz() << " " << wBosonInRF.E() << std::endl;
    ////std::cout << "Z: " << zBosonP4.Px() << " " << zBosonP4.Py() << " " << zBosonP4.Pz() << " " << zBosonP4.E() << std::endl;
    //std::cout << "P Magnitude squared " << zBosonP4.P()*zBosonP4.P() << " P Magnitude squared self computed " << zBosonP4.Px()*zBosonP4.Px() + zBosonP4.Py()*zBosonP4.Py() + zBosonP4.Pz()*zBosonP4.Pz() << std::endl;

    float wBosonEnergy = std::sqrt(zBosonP4.Px()*zBosonP4.Px() + zBosonP4.Py()*zBosonP4.Py() + zBosonP4.Pz()*zBosonP4.Pz() + wBosonInRF.M2());
    ////std::cout << "W Boson energy: " << wBosonEnergy << std::endl;
    RMFLV::BetaVector wBosonBackToLab = zBosonP4.Vect()/wBosonEnergy;
    ROOT::Math::Boost wToLabFrameBoost(wBosonBackToLab);
    RMFLV neutrino = wToLabFrameBoost * neutrinoInZFrame;
    RMFLV muon = wToLabFrameBoost * muonInZFrame;

    // Smearing muon and neutrino 4-vectors by one percent to simulate worse reconstruction.
    //TRandom *r3 = new TRandom3();
    //r3->SetSeed(event.m_eventInfo->nEvent);
    //float r_muon = (1.0+r3->Gaus(0.0,0.1));
    //float r_neutrino = (1.0+r3->Gaus(0.0,0.1));
    ////std::cout << "smearing factor for the muon: " << r_muon << std::endl;
    ////std::cout << "smearing factor for the neutrino: " << r_neutrino << std::endl;
    //muon *= r_muon; neutrino *= r_neutrino;

    product.m_cleanedMuonForWJetsErsatz->p4.SetPxPyPzE(neutrino.Px(),neutrino.Py(),neutrino.Pz(),neutrino.E());
    product.m_leftMuonForWJetsErsatz->p4.SetPxPyPzE(muon.Px(), muon.Py(), muon.Pz(), muon.E());
    //RMFLV wBosonP4 = muon + neutrino;
    //std::cout << "Z pt: " << zBosonP4.Pt() << " Z pz: " << zBosonP4.Pz() << " Z energy: " << zBosonP4.E() << std::endl;
    //std::cout << "W pt: " << wBosonP4.Pt() << " W pz: " << wBosonP4.Pz() << " W energy: " << wBosonP4.E() << std::endl;
    //std::cout << "muon pt: " << muon.Pt() << " muon pz: " << muon.Pz() << " muon energy: " << muon.E() << " muon eta " << muon.Eta() << " muon phi " << muon.Phi() << "muon mass " << muon.M() << " muon magnitude of 3-momentum " << muon.P() << std::endl;
    //std::cout << "neutrino pt: " << neutrino.Pt() << " neutrino pz: " << neutrino.Pz() << " neutrino energy: " << neutrino.E() << " neutrino eta " << neutrino.Eta() << " neutrino phi " << neutrino.Phi() << " neutrino mass " << neutrino.M() << " neutrino magnitude of 3-momentum " << neutrino.P() << std::endl;

    //Update of all relevant collections, which are affected by the manipulation of the muons from the Z Boson.

    //Determining Pt Cuts used on different valid muons
    float signalMuonsPtCut = 0.0;
    float looseMuonsPtCut = 0.0;
    float vetoMuonsPtCut = 0.0;
    for(unsigned int i = 0; i < settings.GetMuonLowerPtCuts().size(); i++)
    {
        ////std::cout << "Cut:" << std::stof(settings.GetMuonLowerPtCuts().at(i)) << std::endl; 
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

    ////std::cout << "Pt cut thresholds:" << std::endl;
    ////std::cout << "Signal" << signalMuonsPtCut << std::endl;
    ////std::cout << "Loose" << looseMuonsPtCut << std::endl;
    ////std::cout << "Veto" << vetoMuonsPtCut << std::endl;

    // Signal Muons

    ////std::cout << "Muon to clean pointer: " << product.m_cleanedMuonForWJetsErsatz << std::endl;
    for(unsigned int i=0; i< product.m_validMuons.size(); i++)
    {
        ////std::cout << "Valid muon pointer: " << product.m_validMuons.at(i) << std::endl;
        if(product.m_cleanedMuonForWJetsErsatz == product.m_validMuons.at(i))
        {
            ////std::cout << "Cleaning in valid muons: " << product.m_cleanedMuonForWJetsErsatz << std::endl;
            product.m_invalidMuons.push_back(product.m_validMuons.at(i));
            product.m_validMuons.erase(product.m_validMuons.begin()+i);
            i--;
        }
        else if(product.m_leftMuonForWJetsErsatz == product.m_validMuons.at(i) && product.m_leftMuonForWJetsErsatz->p4.Pt() < signalMuonsPtCut)
        {
            ////std::cout << "Cleaning in valid muons: " << product.m_leftMuonForWJetsErsatz << std::endl;
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
        ////std::cout << "Valid loose muon pointer: " << product.m_validLooseMuons.at(i) << std::endl;
        if(product.m_cleanedMuonForWJetsErsatz == product.m_validLooseMuons.at(i))
        {
            ////std::cout << "Cleaning in valid loose muons: " << product.m_cleanedMuonForWJetsErsatz << std::endl;
            product.m_invalidLooseMuons.push_back(product.m_validLooseMuons.at(i));
            product.m_validLooseMuons.erase(product.m_validLooseMuons.begin()+i);
            i--;
        }
        else if(product.m_leftMuonForWJetsErsatz == product.m_validLooseMuons.at(i) && product.m_leftMuonForWJetsErsatz->p4.Pt() < looseMuonsPtCut)
        {
            ////std::cout << "Cleaning in valid muons: " << product.m_leftMuonForWJetsErsatz << std::endl;
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
        ////std::cout << "Valid veto muon pointer: " << product.m_validVetoMuons.at(i) << std::endl;
        if(product.m_cleanedMuonForWJetsErsatz == product.m_validVetoMuons.at(i))
        {
            ////std::cout << "Cleaning in valid veto muons: " << product.m_cleanedMuonForWJetsErsatz << std::endl;
            product.m_invalidVetoMuons.push_back(product.m_validVetoMuons.at(i));
            product.m_validVetoMuons.erase(product.m_validVetoMuons.begin()+i);
            i--;
        }
        else if(product.m_leftMuonForWJetsErsatz == product.m_validVetoMuons.at(i)  && product.m_leftMuonForWJetsErsatz->p4.Pt() < vetoMuonsPtCut)
        {
            ////std::cout << "Cleaning in valid muons: " << product.m_leftMuonForWJetsErsatz << std::endl;
            product.m_invalidVetoMuons.push_back(product.m_validVetoMuons.at(i));
            product.m_validVetoMuons.erase(product.m_validVetoMuons.begin()+i);
            i--;
        }
    }
    std::sort(product.m_invalidVetoMuons.begin(), product.m_invalidVetoMuons.end(),
                      [](KMuon* muon1, KMuon* muon2) -> bool
                      { return muon1->p4.Pt() > muon2->p4.Pt(); });
    ////std::cout << "Event: " << event.m_eventInfo->nEvent << std::endl;
    // Removing taus within Delta R = 0.3
    for(unsigned int i=0; i< product.m_validTaus.size(); i++)
    {
        ////std::cout << "Valid Tau pointer: " << product.m_validTaus.at(i) << std::endl;
        //std::cout << "Current tau. Pt " << product.m_validTaus.at(i)->p4.Pt() << " Eta " << product.m_validTaus.at(i)->p4.Eta() << " Phi " << product.m_validTaus.at(i)->p4.Phi() << std::endl;
        if(ROOT::Math::VectorUtil::DeltaR(product.m_cleanedMuonForWJetsErsatz->p4,product.m_validTaus.at(i)->p4) < 0.3)
        {
            ////std::cout << "Cleaning Tau: " << product.m_validTaus.at(i) << std::endl;
            product.m_invalidTaus.push_back(product.m_validTaus.at(i));
            //std::cout << "Erasing tau. Pt " << (*(product.m_validTaus.begin()+i))->p4.Pt() << " Eta " << (*(product.m_validTaus.begin()+i))->p4.Eta() << " Phi " << (*(product.m_validTaus.begin()+i))->p4.Phi() << std::endl;
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
        ////std::cout << "Valid Jets pointer: " << product.m_validJets.at(i) << std::endl;
        if(ROOT::Math::VectorUtil::DeltaR(product.m_cleanedMuonForWJetsErsatz->p4,product.m_validJets.at(i)->p4) < 0.3)
        {
            ////std::cout << "Cleaning valid jet: " << product.m_validJets.at(i) << std::endl;
            product.m_invalidJets.push_back(product.m_validJets.at(i));
            product.m_validJets.erase(product.m_validJets.begin()+i);
            i--;
        }
    }
    std::sort(product.m_invalidJets.begin(), product.m_invalidJets.end(),
                      [](KBasicJet* jet1, KBasicJet* jet2) -> bool
                      { return jet1->p4.Pt() > jet2->p4.Pt(); });
    // Removing btagged jets within Delta R = 0.3
    for(unsigned int i=0; i< product.m_bTaggedJets.size(); i++)
    {
        ////std::cout << "Valid btagged Jets pointer: " << product.m_bTaggedJets.at(i) << std::endl;
        if(ROOT::Math::VectorUtil::DeltaR(product.m_cleanedMuonForWJetsErsatz->p4,product.m_bTaggedJets.at(i)->p4) < 0.3)
        {
            ////std::cout << "Cleaning btagged Jet: " << product.m_bTaggedJets.at(i) << std::endl;
            product.m_nonBTaggedJets.push_back(product.m_bTaggedJets.at(i));
            product.m_bTaggedJets.erase(product.m_bTaggedJets.begin()+i);
            i--;
        }
    }
    std::sort(product.m_bTaggedJets.begin(), product.m_bTaggedJets.end(),
                      [](KBasicJet* jet1, KBasicJet* jet2) -> bool
                      { return jet1->p4.Pt() > jet2->p4.Pt(); });
    
    //std::cout << "--------  WJetsErsatzProducer finishing --------" << std::endl;
    //std::cout << "number of valid muons: " << product.m_validMuons.size() << std::endl; 
    //std::cout << "number of invalid muons: " << product.m_invalidMuons.size() << std::endl; 
    //std::cout << "number of valid loose muons: " << product.m_validLooseMuons.size() << std::endl; 
    //std::cout << "number of invalid loose muons: " << product.m_invalidLooseMuons.size() << std::endl; 
    //std::cout << "number of valid veto muons: " << product.m_validVetoMuons.size() << std::endl; 
    //std::cout << "number of invalid veto muons: " << product.m_invalidVetoMuons.size() << std::endl; 
    //std::cout << "number of valid taus: " << product.m_validTaus.size() << std::endl; 
    for(unsigned int i=0; i< product.m_validTaus.size(); i++)
    {
        //std::cout << "Current tau. Pt " << product.m_validTaus.at(i)->p4.Pt() << " Eta " << product.m_validTaus.at(i)->p4.Eta() << " Phi " << product.m_validTaus.at(i)->p4.Phi() << std::endl;
    }
    //std::cout << "number of valid jets: " << product.m_validJets.size() << std::endl; 
    //std::cout << "number of valid btagged jets: " << product.m_bTaggedJets.size() << std::endl; 
}
