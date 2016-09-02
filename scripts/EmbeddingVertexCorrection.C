#include "Kappa/DataFormats/interface/Kappa.h"

void EmbeddingVertexCorrection(TString vertex_check_file = "vertex_check.root")
{
	TFile* file = new TFile(vertex_check_file);
	
	TTree* selected = (TTree*) file->Get("common1");
	TTree* embedded = (TTree*) file->Get("common2");


	TFile* output = new TFile("EmbeddingVertexCorrection.root", "RECREATE");
	TDirectory* histograms = output->mkdir("histograms");
	TTree* vertex_quantities = new TTree("vertex_quantities","vertex_quantities");
	
	Double_t *dxy_bins = new Double_t[22];
	Double_t *dz_bins = new Double_t[22];
	for(UInt_t i = 0;i<=21;i++)
	{
		dxy_bins[i] = i*(0.01/20);
		dz_bins[i] = i*(0.01/20.);
	}
	
	TH1D* vtx_dxy = new TH1D("vtx_dxy","vtx_dxy",21,dxy_bins);
	TH1D* vtx_dz = new TH1D("vtx_dz","vtx_dz",21,dz_bins);
	
	Float_t selected_x,selected_y,selected_z;
	Float_t embedded_x,embedded_y,embedded_z;
	
	Double_t dxy,dz;
	
	selected->SetBranchAddress("firstPV_X", &selected_x);
	selected->SetBranchAddress("firstPV_Y", &selected_y);
	selected->SetBranchAddress("firstPV_Z", &selected_z);

	embedded->SetBranchAddress("firstPV_X", &embedded_x);
	embedded->SetBranchAddress("firstPV_Y", &embedded_y);
	embedded->SetBranchAddress("firstPV_Z", &embedded_z);
	
	vertex_quantities->Branch("dxy",&dxy,"dxy/D");
	vertex_quantities->Branch("dz",&dz,"dz/D");
	
	int counter_dxy_too_big = 0;
	int counter_dz_too_big = 0;
	for(unsigned int i=0;i<selected->GetEntries();i++)
	{
		embedded->GetEntry(i);
		selected->GetEntry(i);
		
		dxy = TMath::Sqrt((selected_x-embedded_x)*(selected_x-embedded_x) + (selected_y-embedded_y)*(selected_y-embedded_y));
		dz = std::abs(selected_z - embedded_z);
		vertex_quantities->Fill();
		
		if(i % 10000 == 0){
			std::cout << i+1 << " events processed." << std::endl;
		}
		if(dxy < 0.01) vtx_dxy->Fill(dxy);
		else vtx_dxy->Fill(0.01);
		
		if(dz < 0.01) vtx_dz->Fill(dz);
		else vtx_dz->Fill(0.01);

		if(dxy > 0.0015) counter_dxy_too_big++;
		if(dz > 0.002) counter_dz_too_big++;
	}

	std::cout << "Entries Selected: " << selected->GetEntries() << std::endl;
	std::cout << "Entries Embedded: " << embedded->GetEntries() << std::endl;

	std::cout << "Too big dxy for " << counter_dxy_too_big << " events. Percentage: " << counter_dxy_too_big*100.0/selected->GetEntries() << "%" << std::endl;
	std::cout << "Too big dz for " << counter_dz_too_big << " events. Percentage: " << counter_dz_too_big*100.0/selected->GetEntries() << "%" << std::endl;
	output->cd();
	vertex_quantities->Write();
	
	histograms->cd();
	vtx_dxy->Write();
	vtx_dz->Write();
}
