#include "Kappa/DataFormats/interface/Kappa.h"

void EmbeddingVertexCorrection()
{
	TFile* file = new TFile("vertex_check.root", "READ");
	
	TTree* selected = (TTree*) file->Get("common1");
	TTree* embedded = (TTree*) file->Get("common2");
	TTree* mirrored = (TTree*) file->Get("common3");


	TFile* output = new TFile("EmbeddingVertexCorrection.root", "RECREATE");
	TDirectory* histograms = output->mkdir("histograms");
		
	TH1D* vtx_dx = new TH1D("vtx_dx","vtx_dx",42,-0.0105,0.0105);
	TH1D* vtx_dy = new TH1D("vtx_dy","vtx_dy",42,-0.0105,0.0105);
	TH1D* vtx_dz = new TH1D("vtx_dz","vtx_dz",42,-0.0105,0.0105);
	
	Float_t selected_x,selected_y,selected_z;
	Float_t mirrored_x,mirrored_y,mirrored_z;
	
	Double_t dx,dy,dz;
	
	selected->SetBranchAddress("firstPV_X", &selected_x);
	selected->SetBranchAddress("firstPV_Y", &selected_y);
	selected->SetBranchAddress("firstPV_Z", &selected_z);

	mirrored->SetBranchAddress("firstPV_X", &mirrored_x);
	mirrored->SetBranchAddress("firstPV_Y", &mirrored_y);
	mirrored->SetBranchAddress("firstPV_Z", &mirrored_z);
	
	unsigned int overflow = 0;
	for(unsigned int i=0;i<selected->GetEntries();i++)
	{
		mirrored->GetEntry(i);
		selected->GetEntry(i);
		
		dx = selected_x - mirrored_x;
		dy = selected_y - mirrored_y;
		dz = selected_z - mirrored_z;
		
		if(i % 10000 == 0){
			std::cout << i+1 << " events processed." << std::endl;
		}
		if(dx < 0.01 && dx >= -0.01) vtx_dx->Fill(dx);
		else if(dx >= 0.01) vtx_dx->Fill(0.01);
		else vtx_dx->Fill(-0.0105);
		
		if(dy < 0.01 && dx >= -0.01) vtx_dy->Fill(dy);
		else if(dy >= 0.01) vtx_dy->Fill(0.01);
		else vtx_dy->Fill(-0.0105);

		if(dz < 0.01 && dz >= -0.01) vtx_dz->Fill(dz);
		else if(dz >= 0.01) vtx_dz->Fill(0.01);
		else vtx_dz->Fill(-0.0105);

		if(!(std::abs(dx) < 0.01 && std::abs(dy) < 0.01 && std::abs(dz) < 0.01)) overflow++;
	}

	std::cout << "Entries Selected: " << selected->GetEntries() << std::endl;
	std::cout << "Entries Mirrored: " << mirrored->GetEntries() << std::endl;
    std::cout << "Entries Embedded: " << mirrored->GetEntries() << std::endl;
	std::cout << "Percentage of overflow events: " << overflow*100.0/selected->GetEntries() << std::endl;
	
	histograms->cd();
	vtx_dx->Write();
	vtx_dy->Write();
	vtx_dz->Write();
}
