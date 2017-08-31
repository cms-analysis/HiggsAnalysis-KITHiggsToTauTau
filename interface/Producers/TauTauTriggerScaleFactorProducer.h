
#pragma once

#include "Artus/Core/interface/ProducerBase.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "RooWorkspace.h"
#include "RooFunctor.h"
#include "TSystem.h"

/**
   \brief TauTauTriggerScaleFactorProducer
   Config tags:
   - Fill me with something meaningful

*/

class TauTauTriggerScaleFactorProducer: public ProducerBase<HttTypes> {
public:

	std::string GetProducerId() const;

	virtual void Init(setting_type const& settings, metadata_type& metadata) override
	{
		ProducerBase<HttTypes>::Init(settings, metadata);
        TDirectory *savedir(gDirectory);
        TFile *savefile(gFile);
		TFile f(settings.GetRooWorkspace().c_str());
		gSystem->AddIncludePath("-I$ROOFITSYS/include");
		m_workspace = (RooWorkspace*)f.Get("w");
		f.Close();
        gDirectory = savedir;
        gFile = savefile;
        m_functorTau1 = m_workspace->function("t_trgTightIso_data")->functor(m_workspace->argSet("t_pt"));
        m_functorTau1ss = m_workspace->function("t_trgTightIsoSS_data")->functor(m_workspace->argSet("t_pt"));
	}

	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings, metadata_type const& metadata) const override;
private:
    RooWorkspace *m_workspace;
    RooFunctor* m_functorTau1;
    RooFunctor* m_functorTau1ss;


};
