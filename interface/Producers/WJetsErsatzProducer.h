#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/ProducerBase.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"

#include <TMath.h>

/**
    \brief Producer to estimate WJets events from Z->mumu events
    inputs needed:
        - muons from ZmumuProducer as reference for a Z->mumu
        - valid muons collection produced by ValidMuonsProducer, which will be modified to modife Z->mumu to W->munu
        - [ tau and jets candidates (ValidTausProducer, ValidTaggedJetsProducer), to be cleaned if found near muon ]
*/


class WJetsErsatzProducer: public ProducerBase<HttTypes>
{
public:
    typedef typename HttTypes::event_type event_type;
    typedef typename HttTypes::product_type product_type;
    typedef typename HttTypes::setting_type setting_type;

    virtual void Init(setting_type const& settings) override;


    virtual void Produce(event_type const& event, product_type & product, 
                         setting_type const& settings) const override;

    std::string GetProducerId() const override;
//private:
};
