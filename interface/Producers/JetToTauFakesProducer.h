
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "Artus/KappaAnalysis/interface/KappaProducerBase.h"
#include "HTTutilities/Jet2TauFakes/interface/FakeFactor.h"

#if ROOT_VERSION_CODE < ROOT_VERSION(6,0,0)
#include <TROOT.h>
#endif

/**
   \brief JetToTauFakesProducer
   Config tags:
   
    Run this producer after the Run2DecayModeProducer

*/

class JetToTauFakesProducer : public ProducerBase<HttTypes> {
public:

    typedef typename HttTypes::event_type event_type;
    typedef typename HttTypes::product_type product_type;
    typedef typename HttTypes::setting_type setting_type;
    
    std::string GetProducerId() const override;

    virtual void Init(setting_type const& settings) override
 	{
         #if ROOT_VERSION_CODE < ROOT_VERSION(6,0,0)
         gROOT->ProcessLine("#include <map>");
         #endif

         ProducerBase<HttTypes>::Init(settings);
         TDirectory *savedir(gDirectory);
         TFile *savefile(gFile);
         TString cmsswBase = TString( getenv ("CMSSW_BASE") );
         ff_file = new TFile(cmsswBase+"/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/fakeFactors_20160425.root");
         gDirectory = savedir;
         gFile = savefile;
 	}

    void Produce(event_type const& event, product_type& product,
                 setting_type const& settings) const override;
private:

    TFile* ff_file;
};
