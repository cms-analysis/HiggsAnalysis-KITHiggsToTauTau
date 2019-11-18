#pragma once

#include <string>

#include <TFile.h>
#include <TH2.h>


class SinTwoThetaWReweighting
{
public:
	SinTwoThetaWReweighting(
			std::string weightsFilename,
			std::string weightsPositivePolarisationUpQuarks,
			std::string weightsNegativePolarisationUpQuarks,
			std::string weightsPositivePolarisationDownQuarks,
			std::string weightsNegativePolarisationDownQuarks
	)
	{
		TFile* rootFile = TFile::Open(weightsFilename.c_str());
		
		m_weightsPositivePolarisationUpQuarks = static_cast<TH2*>(rootFile->Get(weightsPositivePolarisationUpQuarks.c_str()));
		m_weightsNegativePolarisationUpQuarks = static_cast<TH2*>(rootFile->Get(weightsNegativePolarisationUpQuarks.c_str()));
		m_weightsPositivePolarisationDownQuarks = static_cast<TH2*>(rootFile->Get(weightsPositivePolarisationDownQuarks.c_str()));
		m_weightsNegativePolarisationDownQuarks = static_cast<TH2*>(rootFile->Get(weightsNegativePolarisationDownQuarks.c_str()));
		
		m_weightsPositivePolarisationUpQuarks->SetDirectory(nullptr);
		m_weightsNegativePolarisationUpQuarks->SetDirectory(nullptr);
		m_weightsPositivePolarisationDownQuarks->SetDirectory(nullptr);
		m_weightsNegativePolarisationDownQuarks->SetDirectory(nullptr);
		
		rootFile->Close();
		delete rootFile;
	}
	
	~SinTwoThetaWReweighting()
	{
		if (m_weightsPositivePolarisationUpQuarks) delete m_weightsPositivePolarisationUpQuarks;
		if (m_weightsNegativePolarisationUpQuarks) delete m_weightsNegativePolarisationUpQuarks;
		if (m_weightsPositivePolarisationDownQuarks) delete m_weightsPositivePolarisationDownQuarks;
		if (m_weightsNegativePolarisationDownQuarks) delete m_weightsNegativePolarisationDownQuarks;
	}
	
	double ScaleFactor(double energy, double sin2theta, bool positivePolarisation, bool upQuarks)
	{
		TH2* weights = nullptr;
		if (positivePolarisation)
		{
			if (upQuarks)
			{
				weights = m_weightsPositivePolarisationUpQuarks;
			}
			else
			{
				weights = m_weightsPositivePolarisationDownQuarks;
			}
		}
		else
		{
			if (upQuarks)
			{
				weights = m_weightsNegativePolarisationUpQuarks;
			}
			else
			{
				weights = m_weightsNegativePolarisationDownQuarks;
			}
		}
		
		int xBin = std::max(1, std::min(weights->GetNbinsX(), weights->GetXaxis()->FindBin(energy)));
		int yBin = std::max(1, std::min(weights->GetNbinsY(), weights->GetYaxis()->FindBin(sin2theta)));
		return weights->GetBinContent(xBin, yBin);
	}

private:
	TH2* m_weightsPositivePolarisationUpQuarks = nullptr;
	TH2* m_weightsNegativePolarisationUpQuarks = nullptr;
	TH2* m_weightsPositivePolarisationDownQuarks = nullptr;
	TH2* m_weightsNegativePolarisationDownQuarks = nullptr;
};

