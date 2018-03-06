#!/bin/sh
# call with Artus project directory containing GluGluToHToTauTauM125_RunIIFall15MiniAODv2_PU25nsData2015v1_13TeV_MINIAOD_amcatnlo-pythia8 outputs

for x in 10 20 30 40 50 60 70 80 90; do
	higgsplot.py -j HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/control_plots/13TeV/default/jdphi.json \
	-d $1 \
	-i "merged/GluGluToHToTauTauM125_RunIIFall15MiniAODv2_PU25nsData2015v1_13TeV_MINIAOD_amcatnlo-pythia8/*.root" \
	-f "mt_nominal/ntuple et_nominal/ntuple tt_nominal/ntuple em_nominal/ntuple" \
	--www cp \
	-w \
	"(jeta_1*jeta_2<0) * (mjj>500) * (abs(jdeta)>2.0) * (njets>1)" \
	"(jeta_1*jeta_2<0) * (mjj>500) * (abs(jdeta)>2.0) * (njets>1) * madGraphWeight100/madGraphWeightSample" \
	"(jeta_1*jeta_2<0) * (mjj>500) * (abs(jdeta)>2.0) * (njets>1) * madGraphWeight050/madGraphWeightSample" \
	"(jeta_1*jeta_2<0) * (mjj>500) * (abs(jdeta)>2.0) * (njets>1) * madGraphWeight0${x}/madGraphWeightSample" \
	--nicks 000 100 wi050 xwi0${x} \
	--analysis-modules AddHistograms \
	--add-scale-factors \
	"0.5 0.5" \
	"1 -1" \
	"0`echo "c(${x}*2*a(1)/100)^2" | bc -l` 0`echo "s(${x}*2*a(1)/100)^2" | bc -l`" \
	"1 -1" \
	"`echo "c(${x}*2*a(1)/100)^2-c(${x}*2*a(1)/100)*s(${x}*2*a(1)/100)" | bc -l` `echo "s(${x}*2*a(1)/100)^2-c(${x}*2*a(1)/100)*s(${x}*2*a(1)/100)" | bc -l` `echo "2*c(${x}*2*a(1)/100)*s(${x}*2*a(1)/100)" | bc -l`" \
	--add-nicks "000 100" "wi050 woi050" "000 100" "xwi0${x} xwoi0${x}" "000 100 wi050" \
	--add-result-nicks woi050 i050 xwoi0${x} xi0${x} xp0${x} \
	--filename jdphi_0${x} \
	--nicks-whitelist ^000\$ ^100\$ ^wi050\$ ^woi050\$ ^i050\$ ^xwi0${x}\$ ^xwoi0${x}\$ ^xi0${x}\$ ^xp0${x}\$ \
	--subplot-nicks ^i050\$ ^xi0${x}\$ \
	--labels \
	"#alpha=0 (CP even)" \
	"#alpha=#pi/2 (CP odd)" \
	"#alpha=0.5#times#pi/2 (w interference)" \
	"#alpha=0.5#times#pi/2 (w/o interference)" \
	"#alpha=0.5#times#pi/2 (interference)" \
	"#alpha=0`echo "scale=1; ${x}/100" | bc`#times#pi/2 (w interference)" \
	"#alpha=0`echo "scale=1; ${x}/100" | bc`#times#pi/2 (w/o interference)" \
	"#alpha=0`echo "scale=1; ${x}/100" | bc`#times#pi/2 (interference)" \
	"#alpha=0`echo "scale=1; ${x}/100" | bc`#times#pi/2 (parametrisation)" \
	--legend-markers L L L L L L L L ELP --legend 0.2 0.5 0.9 0.85 --legend-cols 2 \
	--y-rel-lims 0 1.6 --y-label "arb. units" --y-subplot-label Interference \
	-m LINE LINE LINE LINE LINE LINE LINE E E --line-widths 2 2 2 2 3 3 3 1 1 --line-styles 1 2 1 2 1 1 2 1 1 -C kBlack kBlack kRed kRed kRed kGreen kGreen kGreen kViolet \
	--formats pdf png \
	-x "(leadingJetLV.Phi()-trailingJetLV.Phi()) * (-1 * (leadingJetLV.Eta() > 0) + (leadingJetLV.Eta() < 0))" &
done

