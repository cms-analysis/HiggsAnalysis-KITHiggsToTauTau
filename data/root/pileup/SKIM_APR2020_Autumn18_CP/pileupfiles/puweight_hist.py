import sys
import numpy as np

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from optparse import OptionParser

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

#Autumn18 from SimGeneral.MixingModule.mix_2018_25ns_JuneProjectionFull18_PoissonOOTPU_cfi 
probFunctionVariable = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
    20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
    40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
    60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
    80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99
    ]
npu = np.array([i for i in probFunctionVariable], dtype=np.double)

print "No. of PU bins:", len(probFunctionVariable)

probValue = [
    4.695341e-10, 1.206213e-06, 1.162593e-06, 6.118058e-06, 1.626767e-05,
    3.508135e-05, 7.12608e-05, 0.0001400641, 0.0002663403, 0.0004867473,
    0.0008469, 0.001394142, 0.002169081, 0.003198514, 0.004491138,
    0.006036423, 0.007806509, 0.00976048, 0.0118498, 0.01402411,
    0.01623639, 0.01844593, 0.02061956, 0.02273221, 0.02476554,
    0.02670494, 0.02853662, 0.03024538, 0.03181323, 0.03321895,
    0.03443884, 0.035448, 0.03622242, 0.03674106, 0.0369877,
    0.03695224, 0.03663157, 0.03602986, 0.03515857, 0.03403612,
    0.0326868, 0.03113936, 0.02942582, 0.02757999, 0.02563551,
    0.02362497, 0.02158003, 0.01953143, 0.01750863, 0.01553934,
    0.01364905, 0.01186035, 0.01019246, 0.008660705, 0.007275915,
    0.006043917, 0.004965276, 0.004035611, 0.003246373, 0.002585932,
    0.002040746, 0.001596402, 0.001238498, 0.0009533139, 0.0007282885,
    0.000552306, 0.0004158005, 0.0003107302, 0.0002304612, 0.0001696012,
    0.0001238161, 8.96531e-05, 6.438087e-05, 4.585302e-05, 3.23949e-05,
    2.271048e-05, 1.580622e-05, 1.09286e-05, 7.512748e-06, 5.140304e-06,
    3.505254e-06, 2.386437e-06, 1.625859e-06, 1.111865e-06, 7.663272e-07,
    5.350694e-07, 3.808318e-07, 2.781785e-07, 2.098661e-07, 1.642811e-07,
    1.312835e-07, 1.081326e-07, 9.141993e-08, 7.890983e-08, 6.91468e-08,
    6.119019e-08, 5.443693e-08, 4.85036e-08, 4.31486e-08, 3.822112e-08
]

print "No. of PU probability values:",len(probValue)
probpu = np.array([i for i in probValue], dtype=np.double)

sumP = 0
for prob in probValue:
    sumP += prob
print "Sum of the probability values (should be 1):",sumP

fmc = ROOT.TFile("pileupAutumn18MC.root","RECREATE")
grmc = ROOT.TGraph(len(probFunctionVariable),npu,probpu)
grmc.SetName("gr_pileupMC")
hmc = ROOT.TH1D("h_pileupMC","pileup MC;n^{truth}_{PU};probability",len(probFunctionVariable),0,len(probFunctionVariable))
i=1
for prob in probValue:
    hmc.SetBinContent(i,prob)
    i += 1
hmc.SetBinContent(0,0)#underflow
hmc.SetBinContent(i+1,0)#overflow

grmc.Write()
hmc.Write()

#2018 data from /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PileUp
fdata = ROOT.TFile("PileupHistogram-goldenJSON-13tev-2018-69200ub-100bins.root")
hdata = fdata.Get("pileup")
#hdata.Print()

fweight = ROOT.TFile("Pileup_weight_goldenJSON-13TeV-2018_Autumn18MC_69200ub_100bins.root","RECREATE")

hweight = hdata.Clone("pileup")
hweight.Reset()
hweight.SetTitle("pileup weights;n_{PU}^{truth};weight")

norm = 0
for n in probFunctionVariable:
    bin = hdata.GetXaxis().FindBin(n)
    n_data = hdata.GetBinContent(bin)
    n_mc = hmc.GetBinContent(bin)
    #print n,bin,n_data,n_mc,n_data/n_mc
    if n_mc>0:
        hweight.SetBinContent(bin,n_data/n_mc)
    else:
        hweight.SetBinContent(bin,0)
    norm += n_data
#print norm
for bin in xrange(1,hweight.GetNbinsX()+1):
    w = hweight.GetBinContent(bin)
    hweight.SetBinContent(bin,w/norm)
cutoff=1000 #arbitrary cut off
if hweight.GetBinContent(1)>cutoff:
    print "WARNING: weight for npu=0 is very high (>",cutoff,"):",hweight.GetBinContent(1)
    print "\t=> Setting it to 0 to avid artificial enhancement those rare events:"
    hweight.SetBinContent(1,0)

hweight.Write()

fweight.Close()
fdata.Close()
fmc.Close()
