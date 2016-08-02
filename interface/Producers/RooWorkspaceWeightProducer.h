
#pragma once

//#include "Artus/KappaAnalysis/interface/KappaProducerBase.h"
#include "Artus/Core/interface/ProducerBase.h"
#include "RooWorkspace.h"
#include "RooFunctor.h"
#include <boost/algorithm/string/split.hpp>
#include <boost/algorithm/string.hpp>
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

/**
   \brief EmuQcdWeightProducer
   Config tags:
   - Fill me with something meaningful

*/

//class EmuQcdWeightProducer : public KappaProducerBase {
class RooWorkspaceWeightProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	std::string GetProducerId() const;

	virtual void Init(setting_type const& settings) override
	{
		ProducerBase<HttTypes>::Init(settings);
		TDirectory *savedir(gDirectory);
		TFile *savefile(gFile);
		TFile f(settings.GetRooWorkspace().c_str());
		m_workspace = (RooWorkspace*)f.Get("w");
		f.Close();
		gDirectory = savedir;
		gFile = savefile;
		m_weightNames = Utility::ParseMapTypes<int,std::string>(Utility::ParseVectorToMap(settings.GetRooWorkspaceWeightNames()));

        std::map<int,std::vector<std::string>> m_objectNames = Utility::ParseMapTypes<int,std::string>(Utility::ParseVectorToMap(settings.GetRooWorkspaceObjectNames()));
        m_functorArgs = Utility::ParseMapTypes<int,std::string>(Utility::ParseVectorToMap(settings.GetRooWorkspaceObjectArguments()));
        for(auto objectName:m_objectNames)
        {
            for(size_t index = 0; index < objectName.second.size(); index++)
            {
                m_functors[objectName.first].push_back(m_workspace->function(objectName.second[index].c_str())->functor(m_workspace->argSet(m_functorArgs[objectName.first][index].c_str())));
            }
        }

	}

	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings) const override;
private:
    std::map<int,std::vector<std::string>> m_weightNames;
    std::map<int,std::vector<std::string>> m_functorArgs;
    std::map<int,std::vector<RooFunctor*>> m_functors;
    RooWorkspace *m_workspace;

};
