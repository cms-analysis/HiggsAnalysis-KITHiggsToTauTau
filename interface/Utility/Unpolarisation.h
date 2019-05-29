#pragma once

#include <string>

#include <TFile.h>
#include <TH1.h>
#include <TSpline.h>


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
		m_scaleFactorsPositivePolarisationUpQuarks = new TSpline3(static_cast<TH1*>(rootFile->Get(scaleFactorsPositivePolarisationUpQuarks.c_str())));
		m_scaleFactorsNegativePolarisationUpQuarks = new TSpline3(static_cast<TH1*>(rootFile->Get(scaleFactorsNegativePolarisationUpQuarks.c_str())));
		rootFile->Close();
		
		rootFile = TFile::Open(scaleFactorsFilenameDownQuarks.c_str());
		m_scaleFactorsPositivePolarisationDownQuarks = new TSpline3(static_cast<TH1*>(rootFile->Get(scaleFactorsPositivePolarisationDownQuarks.c_str())));
		m_scaleFactorsNegativePolarisationDownQuarks = new TSpline3(static_cast<TH1*>(rootFile->Get(scaleFactorsNegativePolarisationDownQuarks.c_str())));
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
		TSpline3* scaleFactors = nullptr;
		if (positivePolarisation)
		{
			if (upQuarks)
			{
				scaleFactors = m_scaleFactorsPositivePolarisationUpQuarks;
			}
			else
			{
				scaleFactors = m_scaleFactorsPositivePolarisationDownQuarks;
			}
		}
		else
		{
			if (upQuarks)
			{
				scaleFactors = m_scaleFactorsNegativePolarisationUpQuarks;
			}
			else
			{
				scaleFactors = m_scaleFactorsNegativePolarisationDownQuarks;
			}
		}
		return scaleFactors->Eval(energy);
	}

private:
	TSpline3* m_scaleFactorsPositivePolarisationUpQuarks = nullptr;
	TSpline3* m_scaleFactorsNegativePolarisationUpQuarks = nullptr;
	TSpline3* m_scaleFactorsPositivePolarisationDownQuarks = nullptr;
	TSpline3* m_scaleFactorsNegativePolarisationDownQuarks = nullptr;
};

