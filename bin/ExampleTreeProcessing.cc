
#include <iostream>

#include <TChain.h>
#include <TInterpreter.h>
#include <Math/Vector4D.h>
#include <Math/Vector4Dfwd.h>


int main(int argc, char** argv)
{
	gInterpreter->GenerateDictionary("ROOT::Math::PtEtaPhiM4D<float>", "Math/LorentzVector.h");
	gInterpreter->GenerateDictionary("ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> >", "Math/LorentzVector.h");

	TChain lvTree("lv/ntuple");
	int nFiles = lvTree.Add("/net/scratch_cms/institut_3b/tmuller/artus/2016-08-18_22-10_Run2InitialStateCPStudies/output/GluGluH2JetsToTauTauM125CPmixingsmJHU_RunIISpring16MiniAODv2_PUSpring16RAWAODSIM_13TeV_MINIAOD_unspecified/*.root");
	//int nFiles = lvTree.Add("output.root");
	std::cout << "Tree \"lv/ntuple\" initialised with " << nFiles << " file(s)." << std::endl;
	
	//ROOT::Math::PtEtaPhiMVector* jet1 = new ROOT::Math::PtEtaPhiMVector();
	//lvTree.SetBranchAddress("jlv_1", jet1);
	//lvTree.SetBranchAddress("jlv_1", &jet1);
	
	ROOT::Math::PtEtaPhiMVector jet1;
	lvTree.SetBranchAddress("jlv_1", &jet1);
	
	for (Long64_t entry = 0; entry < 10/*lvTree.GetEntries()*/; ++entry)
	{
		lvTree.GetEntry(entry);
		std::cout << "Processing entry " << entry << "..." << std::endl;
		
		//std::cout << "\tJet 1: (Pt, Eta, Phi, M) = (" << jet1->Pt() << ", " << jet1->Eta() << ", " << jet1->Phi() << ", " << jet1->M() << ")" << std::endl;
		std::cout << "\tJet 1: (Pt, Eta, Phi, M) = (" << jet1.Pt() << ", " << jet1.Eta() << ", " << jet1.Phi() << ", " << jet1.M() << ")" << std::endl;
	}
	
	return 0;
}
