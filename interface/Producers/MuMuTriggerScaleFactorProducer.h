
#pragma once

#include "Artus/Core/interface/ProducerBase.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "RooWorkspace.h"
#include "RooFunctor.h"
#include "TSystem.h"

/**
   \brief MuMuTriggerScaleFactorProducer
   Config tags:
   - Fill me with something meaningful

*/

class MuMuTriggerScaleFactorProducer: public ProducerBase<HttTypes> {
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
        m_functorMu = m_workspace->function("m_trgIsoMu22orTkIsoMu22_desy_data")->functor(m_workspace->argSet("m_pt,m_eta"));
	}

	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings, metadata_type const& metadata) const override;
private:
    RooWorkspace *m_workspace;
    RooFunctor* m_functorMu;


};
