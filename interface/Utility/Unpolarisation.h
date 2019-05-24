#pragma once

#include <string>

#include <TFile.h>
#include <TH1.h>


class Unpolarisation
{
public:
	Unpolarisation(
			std::string scaleFactorsFilenameUpQuarks,
			std::string scaleFactorsPositivePolarisationUpQuarks,
			std::string scaleFactorsNegativePolarisationUpQuarks,
			std::string scaleFactorsFilenameDownQuarks,
			std::string scaleFactorsPositivePolarisationDownQuarks,
			std::string scaleFactorsNegativePolarisationDownQuarks
	)
	{
		TFile* rootFile = nullptr;
		
		rootFile = TFile::Open(scaleFactorsFilenameUpQuarks.c_str());
		m_scaleFactorsPositivePolarisationUpQuarks = static_cast<TH1*>(rootFile->Get(scaleFactorsPositivePolarisationUpQuarks.c_str()));
		m_scaleFactorsNegativePolarisationUpQuarks = static_cast<TH1*>(rootFile->Get(scaleFactorsNegativePolarisationUpQuarks.c_str()));
		m_scaleFactorsPositivePolarisationUpQuarks->SetDirectory(nullptr);
		m_scaleFactorsNegativePolarisationUpQuarks->SetDirectory(nullptr);
		rootFile->Close();
		
		rootFile = TFile::Open(scaleFactorsFilenameDownQuarks.c_str());
		m_scaleFactorsPositivePolarisationDownQuarks = static_cast<TH1*>(rootFile->Get(scaleFactorsPositivePolarisationDownQuarks.c_str()));
		m_scaleFactorsNegativePolarisationDownQuarks = static_cast<TH1*>(rootFile->Get(scaleFactorsNegativePolarisationDownQuarks.c_str()));
		m_scaleFactorsPositivePolarisationDownQuarks->SetDirectory(nullptr);
		m_scaleFactorsNegativePolarisationDownQuarks->SetDirectory(nullptr);
		rootFile->Close();
		
		delete rootFile;
	}
	
	~Unpolarisation()
	{
		if (m_scaleFactorsPositivePolarisationUpQuarks) delete m_scaleFactorsPositivePolarisationUpQuarks;
		if (m_scaleFactorsNegativePolarisationUpQuarks) delete m_scaleFactorsNegativePolarisationUpQuarks;
		if (m_scaleFactorsPositivePolarisationDownQuarks) delete m_scaleFactorsPositivePolarisationDownQuarks;
		if (m_scaleFactorsNegativePolarisationDownQuarks) delete m_scaleFactorsNegativePolarisationDownQuarks;
	}
	
	double ScaleFactor(double energy, bool positivePolarisation, bool upQuarks)
	{
		TH1* histogram = nullptr;
		if (positivePolarisation)
		{
			if (upQuarks)
			{
				histogram = m_scaleFactorsPositivePolarisationUpQuarks;
			}
			else
			{
				histogram = m_scaleFactorsPositivePolarisationDownQuarks;
			}
		}
		else
		{
			if (upQuarks)
			{
				histogram = m_scaleFactorsNegativePolarisationUpQuarks;
			}
			else
			{
				histogram = m_scaleFactorsNegativePolarisationDownQuarks;
			}
		}
		return histogram->GetBinContent(histogram->FindBin(energy));
	}

private:
	TH1* m_scaleFactorsPositivePolarisationUpQuarks = nullptr;
	TH1* m_scaleFactorsNegativePolarisationUpQuarks = nullptr;
	TH1* m_scaleFactorsPositivePolarisationDownQuarks = nullptr;
	TH1* m_scaleFactorsNegativePolarisationDownQuarks = nullptr;
};

