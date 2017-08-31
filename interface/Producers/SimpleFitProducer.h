#pragma once

#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

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

	virtual std::string GetProducerId() const override;
	
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
	
	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;
	
};


