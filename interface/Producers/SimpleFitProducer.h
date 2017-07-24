#pragma once

#include "Artus/Utility/interface/Utility.h"

#include "../HttTypes.h"
#include "TauPolSoftware/SimpleFits/interface/TrackParticle.h"
#include "TauPolSoftware/SimpleFits/interface/LorentzVectorParticle.h"
#include "TauPolSoftware/SimpleFits/interface/Particle.h"
//#include "TauPolSoftware/SimpleFits/interface/PTObject.h"

#include "TMatrixT.h"
#include "TMatrixTSym.h"
#include "TVector3.h"

//using namespace std;

class SimpleFitProducer: public ProducerBase<HttTypes>
{
 public:
    
    typedef typename HttTypes::event_type event_type;
    typedef typename HttTypes::product_type product_type;
    typedef typename HttTypes::setting_type setting_type;
    
    
    virtual std::string GetProducerId() const override
	{
            return "SimpleFitProducer";
	}
    
    
    virtual void Init(setting_type const& settings) override;
    
    virtual void Produce(event_type const& event, product_type& product,
                         setting_type const& settings) const override;      
    
};


