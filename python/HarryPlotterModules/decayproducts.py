#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import HarryPlotter.Plotting.harrycore as harrycore
import HarryPlotter.Plotting.plot1d as plot1d
import HarryPlotter.Plotting.tools.utils as utils
import HarryPlotter.Plotting.tools.labels as labels
import HarryPlotter.Plotting.tools.mplconvert as mplconvert
import copy

# particle dictionary with name, masslims, ...
particledict = {
	  25: [r'Higgs', [123, 126]],
	  22: [r'$\gamma$', [-0.1, 0.1]],
      -20213: [r'$a_1(1260)^-$', [0, 400]],
       20213: [r'$a_1(1260)^+$', [0, 400]],
	-323: [r'$K^*(892)^-$', [0, 400]],
	 323: [r'$K^*(892)^+$', [0, 400]],
	-321: [r'$K^-$', [0.48, 0.51]],
	 321: [r'$K^+$', [0.48, 0.51]],
	-213: [r'$\rho (770)^-$', [0, 400]],
	 213: [r'$\rho (770)^+$', [0, 400]],
	-211: [r'$\pi ^-$', [0.12, 0.16]],
	 211: [r'$\pi ^+$', [0.12, 0.16]],
	 -24: [r'$W^-$', [0, 400]],
	  24: [r'$W^+$', [0, 400]],
	  15: [r'$\tau ^-$', [1.75, 1.8]],
	 -15: [r'$\tau ^+$', [1.75, 1.8]],
          13: [r'$\mu ^-$', [0, 0.2]],
         -13: [r'$\mu ^+$', [0, 0.2]],
	  11: [r'$e^-$', [-0.1, 0.1]],
	 -11: [r'$e^+$', [-0.1, 0.1]],
	  12: [r'$\nu_e$', [-0.1, 0.1]],
	 -12: [r'$\bar{\nu_e}$', [-0.1, 0.1]],
	  14: [r'$\nu_{\mu}$', [-0.1, 0.1]],
	 -14: [r'$\bar{\nu_{\mu}}$', [-0.1, 0.1]],
	  16: [r'$\nu_{\tau}$', [-0.1, 0.1]],
	 -16: [r'$\bar{\nu_{\tau}}$', [-0.1, 0.1]]

	}

xlimsdict = {

	"tauSpinnerWeight": [0, 2],
	"Pt": [0, 400],
	"Eta": [-6.5, 6.5],
	"Phi": [-3.15, 3.15],
	"Mass": ["mass"]
	}


def ratioplot(plotdict):
	""" This function sorts particles depending on the pdgids-list"""

	plotdict['xlims'] = [-20300.5, 20299.5]
	plotdict['nbins'] = 40600

	plot1d.get_root_histos(plotdict)
	plot1d.get_mpl_histos(plotdict)
	# remove empty bins
	# map  plotdict["mplhistos"]  x entries (=pdgIDs) to particle names
	# regroup

	pdgids = [-20213, 20213, -323, 323, -321, 321, -213, 213, -211, 211, -24, 24, 11, -11, 13, -13]
	for i in range(len(plotdict["mplhistos"])):
		for xc, y in zip(plotdict["mplhistos"][i].xc, plotdict["mplhistos"][i].y):
			if (y != 0) and not (xc in pdgids) and (xc != 0):
				print "PdgId %5.0f is not contained in the list 'pdgids'" % xc
				sys.exit(1)

	binlabelslist = [particledict.get(p) for p in pdgids]

	for i in range(len(plotdict["mplhistos"])):
		new_y = [0] * len(pdgids)
		new_yerr = [0] * len(pdgids)
		for j in range(len(pdgids)):
			for xc, y, yerr in zip(plotdict["mplhistos"][i].xc, plotdict["mplhistos"][i].y, plotdict["mplhistos"][i].yerr):
				if pdgids[j] == xc:
					new_y[j] = y
					new_yerr[j] = yerr
		numblist = range(len(pdgids))
		for k in numblist:
			numblist[k] -= 0.5
		plotdict["mplhistos"][i].x = numblist
		plotdict["mplhistos"][i].xc = range(len(pdgids))
		plotdict["mplhistos"][i].y = new_y
		plotdict["mplhistos"][i].yerr = new_yerr

	plot1d.plot1d_mpl(plotdict)  # plottet mplhistos

	# set x axis xticks, xticklabels
	plotdict['axes'].set_ylim(top=1.2 * max(d.ymax() for d in plotdict['mplhistos']), bottom=0)
	labels.add_labels(plotdict)
	plotdict["axes"].set_xticks(range(len(pdgids)))
	plotdict["axes"].set_xticklabels(binlabelslist, rotation=90)
	utils.save(plotdict)


def multiplot(plotdict):
	"""This function makes similar plots with the same quantities and different cuts and selections"""
	pdgids = [211, 321, 11, 13]
	quantities = ["tauSpinnerWeight", "1genBoson1Daughter2GranddaughterPt", "1genBoson1Daughter2GranddaughterEta", "1genBoson1Daughter2GranddaughterPhi", "1genBoson1Daughter2GranddaughterMass"]
	for i in pdgids:
		for quantity in quantities:
			local_plotdict = utils.copyplotdict(plotdict)
			for key in xlimsdict.keys():
				if key in quantity:
					local_plotdict['xlims'] = xlimsdict[key]
					if local_plotdict['xlims'] == ["mass"]:
						local_plotdict['xlims'] = particledict.get(i)[1]

			local_plotdict["x"] = [quantity]
			if quantity == "tauSpinnerWeight":
				local_plotdict["log"] = True
			local_plotdict["weights"][0] = 'abs(1genBoson1Daughter2GranddaughterPdgId) == %0.0f && tauSpinnerWeight != -999 && tauSpinnerWeight != -777' % i
			#print local_plotdict["weights"][0]
			local_plotdict["filename"] = local_plotdict["x"][0] + 'ForPdgId%s' % i
			local_plotdict["title"] = local_plotdict["x"][0] + ' for ' + particledict.get(i)[0] + ' and ' + particledict.get(-i)[0]
			#local_local_plotdict["labels"] = local_plotdict["x"][0] + ' for ' + particledict.get(i) + ' and ' + particledict.get(-i)
			plot1d.get_root_histos(local_plotdict)

			plot1d.get_mpl_histos(local_plotdict)
			plot1d.plot1d_mpl(local_plotdict)

			labels.add_labels(local_plotdict)
			utils.setaxislimits(local_plotdict)
			utils.save(local_plotdict)

