
#pragma once

#include "../HttTypes.h"

/** Producer for simple di-lepton/di-tau quantities.
 */

// pdg mass constants
namespace 
{
	const double piMass = 0.13957018;
	const double piMassSquared = piMass*piMass;
	const double protonMass = 0.938272046;
	const double protonMassSquared = protonMass*protonMass;
	const double kShortMass = 0.497614;
	const double lambdaMass = 1.115683;
}

typedef ROOT::Math::SMatrix<double, 3, 3, ROOT::Math::MatRepSym<double, 3> > SMatrixSym3D;
typedef ROOT::Math::SVector<double, 3> SVector3;

class KaonsProducer: public ProducerBase<HttTypes> 
{
	public:

		typedef typename HttTypes::event_type event_type;
		typedef typename HttTypes::product_type product_type;
		typedef typename HttTypes::setting_type setting_type;

		virtual std::string GetProducerId() const override;
		
		virtual void Init(setting_type const& settings) override;

		virtual void Produce(event_type const& event, product_type& product,
							 setting_type const& settings) const override;

		bool TrackIsGood(KTrack tmpTrack, KBeamSpot theBeamSpot, RMPoint referencePos, KVertex referenceVtx, bool verbose = false) const ;
	private:
		bool UseVertex;
		bool VertexFitter;
		bool UseRefTracks;
		bool DoKShorts;
		bool DoLambdas;	
		float  TkChi2Cut;
		int  kNHitsCut;
		float TkPtCut;
		float TkIPSigXYCut;
		float TkIPSigZCut;
		float VtxChi2Cut;
		float VtxDecaySigXYZCut;
		float VtxDecaySigXYCut;
		float TkDCACut;
		int TkNHitsCut;
		float MPiPiCut;
		float InnerHitPosCut;
		float CosThetaXYCut;
		float CosThetaXYZCut;
		float KShortMassCut;
		float LambdaMassCut;
		bool KaonDebugOutput;

	void dout() const
	{

		if (KaonDebugOutput) std::cout << std::endl;
	}
	template <typename Head, typename... Tail>
	void dout(Head H, Tail... T) const
	{
		if (KaonDebugOutput)
		{
			std::cout << H << ' ';
			dout(T...);
		}
	}

};

