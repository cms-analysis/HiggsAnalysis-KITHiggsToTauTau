
#pragma once

#include "Artus/KappaAnalysis/interface/Producers/TmvaClassificationMultiReaderBase.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/**
   \brief Producer for discriminator agains TTbar (as used in the EM channel)

   Required config tags with an short example:
{
     "MVATestMethodsInputQuantities": [
        "0;pVecSum,lep1Pt:=pt_1,lep1MetMt:=mt_1,lep2Pt:=pt_2,lep2MetMt:=mt_2,pfMetPt:=met,mvaMetPt:=mvamet,pZetaMissVis,pZetaMiss,pZetaVis,nJets30:=njets,nBJets20:=nbtag,min_ll_jet_eta,lep1_centrality,lep2_centrality,delta_lep_centrality,lep1IsoOverPt:=iso_1",
        "1;pVecSum,lep1Pt:=pt_1,lep1MetMt:=mt_1,lep2Pt:=pt_2,lep2MetMt:=mt_2,pfMetPt:=met,mvaMetPt:=mvamet,pZetaMissVis,pZetaMiss,pZetaVis,nJets30:=njets,nBJets20:=nbtag,min_ll_jet_eta,lep1_centrality,lep2_centrality,delta_lep_centrality,lep1IsoOverPt:=iso_1"
    ],
    "MVATestMethodsMethods": [
        "0;BDT",
        "0;BDT",
        "0;BDT",
        "1;BDT",
		"1;BDT"
    ],
    "MVATestMethodsNFolds": [
        3,
        1,
		1
    ],
    "MVATestMethodsNames": [
        "ggh_150_zXX",
        "ggh_250_zXX"
    ],
    "MVATestMethodsWeights": [
        "/nfs/dust/cms/user/mschmitt/analysis/CMSSW_7_1_5/src/test_nfold/weights/T1_BDT_ggh_150_zXX.weights.xml",
        "/nfs/dust/cms/user/mschmitt/analysis/CMSSW_7_1_5/src/test_nfold/weights/T2_BDT_ggh_150_zXX.weights.xml",
        "/nfs/dust/cms/user/mschmitt/analysis/CMSSW_7_1_5/src/test_nfold/weights/T3_BDT_ggh_150_zXX.weights.xml",
        "/nfs/dust/cms/user/mschmitt/analysis/CMSSW_7_1_5/src/test_nfold/weights/T1_BDT_ggh_250_zXX.weights.xml",
		"/nfs/dust/cms/user/mschmitt/analysis/CMSSW_7_1_5/src/test_nfold/weights/T1_BDT_ggh_250_zXX.weights.xml"
    ]
}

   Detailed description:
   "MVATestMethodsInputQuantities": This is a string list containing training variables for different TMVA Factory instances. The number followed by ; defines the number of factory those variables belong to.
   "MVATestMethodsMethods": Number followed by ; defines the number ob factory those method belongs to
   "MVATestMethodsNFolds": This number indicates how much of the methods belong to one N-Fold Training:
   as in the example the 0;BDT methods belong to one single 3-Fold training and are treated accordingly
   "MVATestMethodsNames": This is a name base for n-fold and regular training.
   There will be exactly this name as variable and in case of N-Fold training several names derived from that one. For the 3-Fod training in the example:
   ggh_150_zXX -> {ggh_150_zXX, T1ggh_150_zXX, T2ggh_150_zXX, T3ggh_150_zXX}
   for a regular training there will not be a T1base_name present
	"MVATestMethodsWeights": Stringlist of weightfiles in the same order as the methods were specified
*/
class MVATestMethodsProducer: public TmvaClassificationMultiReaderBase<HttTypes>
{
public:

	virtual std::string GetProducerId() const override
	{
		return "MVATestMethodsProducer";
	}
	MVATestMethodsProducer();

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type& product,
						 setting_type const& settings, metadata_type const& metadata) const override;
};

