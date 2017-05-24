# Script to make latex tables out of .json files created by script zmm_vs_ztt_yields.py
# Adapt it for your purposes, since a lot of things are hardcoded.


import json
from decimal import Decimal
weight_keys = {
	"em_inclusive_inclusive" : r'$e\mu$',
	"em_btag_inclusive" : r'$e\mu$ b-tag',
	"em_btag_highPzeta" : r'$e\mu$ b-tag high $P_{\zeta}$',
	"em_btag_mediumPzeta" : r'$e\mu$ b-tag medium $P_{\zeta}$',
	"em_btag_lowPzeta" : r'$e\mu$ b-tag low $P_{\zeta}$',
	"em_nobtag_inclusive" : r'$e\mu$ no b-tag',
	"em_nobtag_highPzeta" : r'$e\mu$ no b-tag high $P_{\zeta}$',
	"em_nobtag_mediumPzeta" : r'$e\mu$ no b-tag medium $P_{\zeta}$',
	"em_nobtag_lowPzeta" : r'$e\mu$ no b-tag low $P_{\zeta}$',
	"et_inclusive_inclusive" : r'$e\tau_{h}$',
	"et_btag_inclusive" : r'$e\tau_{h}$ b-tag',
	"et_btag_loosemt" : r'$e\tau_{h}$ b-tag loose $m_T$',
	"et_btag_tight" : r'$e\tau_{h}$ b-tag tight',
	"et_nobtag_inclusive" : r'$e\tau_{h}$ no b-tag',
	"et_nobtag_loosemt" : r'$e\tau_{h}$ no b-tag loose $m_T$',
	"et_nobtag_tight" : r'$e\tau_{h}$ no b-tag tight',
	"mt_inclusive_inclusive" : r'$\mu\tau_{h}$',
	"mt_btag_inclusive" : r'$\mu\tau_{h}$ b-tag',
	"mt_btag_loosemt" : r'$\mu\tau_{h}$ b-tag loose $m_T$',
	"mt_btag_tight" : r'$\mu\tau_{h}$ b-tag tight',
	"mt_nobtag_inclusive" : r'$\mu\tau_{h}$ no b-tag',
	"mt_nobtag_loosemt" : r'$\mu\tau_{h}$ no b-tag loose $m_T$',
	"mt_nobtag_tight" : r'$\mu\tau_{h}$ no b-tag tight',
	"tt_btag_inclusive" : r'$\tau_{h}\tau_{h}$ b-tag',
	"tt_nobtag_inclusive" : r'$\tau_{h}\tau_{h}$ no b-tag',
	"tt_inclusive_inclusive" : r'$\tau_{h}\tau_{h}$'
}

ztt_weight_keys = {
	"et_btag_looseiso" : r'$e\tau_{h}$ b-tag loose iso',
	"et_btag_loosemt" : r'$e\tau_{h}$ b-tag loose $m_T$',
	"et_btag_tight" : r'$e\tau_{h}$ b-tag tight',
	"et_btag_inclusive" : r'$e\tau_{h}$ b-tag',
	"et_nobtag_looseiso" : r'$e\tau_{h}$ no b-tag loose iso',
	"et_nobtag_loosemt" : r'$e\tau_{h}$ no b-tag loose $m_T$',
	"et_nobtag_tight" : r'$e\tau_{h}$ no b-tag tight',
	"et_nobtag_inclusive" : r'$e\tau_{h}$ no b-tag',
	"mt_btag_looseiso" : r'$\mu\tau_{h}$ b-tag loose iso',
	"mt_btag_loosemt" : r'$\mu\tau_{h}$ b-tag loose $m_T$',
	"mt_btag_tight" : r'$\mu\tau_{h}$ b-tag tight',
	"mt_btag_inclusive" : r'$\mu\tau_{h}$ b-tag',
	"mt_nobtag_looseiso" : r'$\mu\tau_{h}$ no b-tag loose iso',
	"mt_nobtag_loosemt" : r'$\mu\tau_{h}$ no b-tag loose $m_T$',
	"mt_nobtag_tight" : r'$\mu\tau_{h}$ no b-tag tight',
	"mt_nobtag_inclusive" : r'$\mu\tau_{h}$ no b-tag'
}

intervals = {}
ztt_intervals = {}
ratios = {}


#with open("intervalls_one_DY.json") as iv:
#	intervals = json.load(iv)
#with open("ratios_one_DY.json") as r:
#	ratios = json.load(r)

with open("ztt_zmm_normalization/intervals.json") as iv:
	intervals = json.load(iv)
with open("ztt_zmm_normalization/ratios.json") as r:
	ratios = json.load(r)
with open("ztt_yields_comparison/intervals.json") as ivtt:
	ztt_intervals = json.load(ivtt)


#latex_tables_file = open("latex_tables_file_one_DY.tex","w")
#summary_table_file = open("summary_table_one_DY.tex","w")

latex_tables_file = open("latex_tables_file.tex","w")
summary_table_file = open("summary_table.tex","w")
ztt_summary_table_file = open("ztt_summary_table.tex","w")

def create_variation_matrix(weight):
	variations = ratios[weight]
	variation_matrix = {
		0.5 :  { 0.5 : '' , 1.0 : '', 2.0 : '' },
		1.0 :  { 0.5 : '' , 1.0 : '', 2.0 : '' },
		2.0 :  { 0.5 : '' , 1.0 : '', 2.0 : '' },
	}
	for v in variations:
		if not v in ["1","nlo","embedding"]:
			muR, muF = [ float(coord.replace("p",".")) for coord in v.replace("_weight","").replace("muR","").replace("muF","").split("_")]
			variation_matrix[muR][muF] = '%.3e' % Decimal(variations[v])
		elif v == "1":
			variation_matrix[1.0][1.0] = '%.3e' % Decimal(variations[v])
	return variation_matrix

def create_table(weight):
	var_mat = create_variation_matrix(weight)
	table = ""
	table += r'\begin{center}'+'\n'
	table += r'\begin{tabular}{c | c c c c }'+'\n'
	table += r' & $\mu_F$ & \textbf{0.5} & \textbf{1.0} & \textbf{2.0} \\'+'\n'
	table += r'\hline'+'\n'
	table += r'$\mu_R$ & & & & \\'+'\n'
	table += r' \textbf{0.5} & & \num{'+var_mat[0.5][0.5]+r'} & \num{'+var_mat[0.5][1.0]+r'} & \num{'+var_mat[0.5][2.0]+r'} \\'+'\n'
	table += r' \textbf{1.0} & & \num{'+var_mat[1.0][0.5]+r'} & \num{'+var_mat[1.0][1.0]+r'} & \num{'+var_mat[1.0][2.0]+r'} \\'+'\n'
	table += r' \textbf{2.0} & & \num{'+var_mat[2.0][0.5]+r'} & \num{'+var_mat[2.0][1.0]+r'} & \num{'+var_mat[2.0][2.0]+r'} \\'+'\n'
	table += r'\end{tabular}'+'\n'
	table += r'\end{center}'+'\n'
	return table

def create_slide(weight):
	slide = ""
	slide += r'\begin{frame}{'+weight_keys[weight]+'}\n'
	slide += r'Yield ratios $R^{Z\rightarrow\tau\tau}_{Z\rightarrow\mu\mu}$ for different scale variations'+'\n'
	slide += create_table(weight)
	slide += r'\end{frame}'+'\n'
	slide += '\n'
	return slide

def latex_number(number):
	return r'\num{'+'%.3e' % Decimal(number)+'}'

def latex_percentage(number):
	return '%.2f' % number + r'\%'

def create_summary():
	slide = ""
	slide += r'\begin{frame}{Summary on extrapolation uncertainties}'+'\n'
	slide += r'\vspace{-0.5cm}'+'\n'
	slide += r'\begin{center}'+'\n'
	slide += r'\begin{table}'+'\n'
	slide += r'\resizebox{0.85\textheight}{!}{'+'\n'
#	slide += r'\begin{tabular}{c | c c c c c c c c c}'+'\n'
#	slide += r'category & LO $R^{Z\rightarrow\tau\tau}_{Z\rightarrow\mu\mu}$ & $\Delta (scale)$ & $\Delta (stat.)$ & \textbf{NLO} $R^{Z\rightarrow\tau\tau}_{Z\rightarrow\mu\mu}$ & $\Delta^{\textbf{NLO}} (stat.)$ & $\Delta^{\textbf{NLO}} (\text{to LO})$ & \textbf{emb.} $R^{Z\rightarrow\tau\tau}_{Z\rightarrow\mu\mu}$ & $\Delta^{\textbf{emb.}} (stat.)$ & $\Delta^{\textbf{emb.}} (\text{to LO})$\\'+'\n'
	slide += r'\begin{tabular}{c | c c c c c c}'+'\n'
	slide += r'category & LO $R^{Z\rightarrow\tau\tau}_{Z\rightarrow\mu\mu}$ & $\Delta (scale)$ & $\Delta (stat.)$ & \textbf{NLO} $R^{Z\rightarrow\tau\tau}_{Z\rightarrow\mu\mu}$ & $\Delta^{\textbf{NLO}} (stat.)$ & $\Delta^{\textbf{NLO}} (\text{to LO})$\\'+'\n'
	slide += r'\hline'+'\n'
	for weight in sorted(weight_keys):
		slide += r'\rule{0pt}{2.7ex}'+'\n'
		slide += weight_keys[weight] + r' & '
		slide += latex_number(intervals[weight]["nominal"]) + r' & '
		slide += r'$^{+'+latex_percentage(intervals[weight]["percentage_up"])+r'}_{'+latex_percentage(intervals[weight]["percentage_down"])+r'}$ & '
		slide += r'$\pm$'+latex_percentage(intervals[weight]["percentage_stat_nominal"]) + r' & '
		slide += latex_number(intervals[weight]["nlo"]) + r' & '
		slide += r'$\pm$'+latex_percentage(intervals[weight]["percentage_stat_nlo"]) + r' & '
		#slide += latex_percentage(intervals[weight]["percentage_nlo"]) + r' & '
		slide += latex_percentage(intervals[weight]["percentage_nlo"]) + r'\\'+'\n'
		#if False:#"mt_" in weight:
		#	slide += latex_number(intervals[weight]["embedding"]) + r' & '
		#	slide += r'$\pm$'+latex_percentage(intervals[weight]["percentage_stat_embedding"]) + r' & '
		#	slide += latex_percentage(intervals[weight]["percentage_embedding"]) + r' \\'+'\n'
		#else:
		#	slide += r' & '
		#	slide += r' & '
		#	slide += r' \\'+'\n'
	slide += r'\end{tabular}}'+'\n'
	slide += r'\end{table}'+'\n'
	slide += r'\end{center}'+'\n'

	slide += r'\end{frame}'+'\n'
	slide += '\n'
	return slide


def create_ztt_summary():
	slide = ""
	slide += r'\begin{frame}{Summary on $Z\rightarrow\tau\tau$ ratios}'+'\n'
	slide += r'\vspace{-0.5cm}'+'\n'

	slide += r'\begin{center}'+'\n'
	slide += r'\begin{table}'+'\n'
	slide += r'\resizebox{\textwidth}{!}{'+'\n'
	slide += r'\begin{tabular}{c | c c c c c c c c c}'+'\n'
	slide += r'category & LO $R^{Z\rightarrow\tau\tau(cat.)}_{Z\rightarrow\tau\tau(inc.)}$ & $\Delta (scale)$ & $\Delta (stat.)$ & \textbf{NLO} $R^{Z\rightarrow\tau\tau(cat.)}_{Z\rightarrow\tau\tau(inc.)}$ & $\Delta^{\textbf{NLO}} (stat.)$ & $\Delta^{\textbf{NLO}} (\text{to LO})$ & \textbf{emb.} $R^{Z\rightarrow\tau\tau(cat.)}_{Z\rightarrow\tau\tau(inc.)}$ & $\Delta^{\textbf{emb.}} (stat.)$ & $\Delta^{\textbf{emb.}} (\text{to LO})$\\'+'\n'
	for weight in sorted(ztt_weight_keys):
		slide += r'\rule{0pt}{2.7ex}'+'\n'
		slide += ztt_weight_keys[weight] + r' & '
		slide += latex_number(ztt_intervals[weight]["nominal"]) + r' & '
		slide += r'$^{+'+latex_percentage(ztt_intervals[weight]["percentage_up"])+r'}_{'+latex_percentage(ztt_intervals[weight]["percentage_down"])+r'}$ & '
		slide += r'$\pm$'+latex_percentage(ztt_intervals[weight]["percentage_stat_nominal"]) + r' & '
		slide += latex_number(ztt_intervals[weight]["nlo"]) + r' & '
		slide += r'$\pm$'+latex_percentage(ztt_intervals[weight]["percentage_stat_nlo"]) + r' & '
		slide += latex_percentage(ztt_intervals[weight]["percentage_nlo"]) + r' & '
		slide += latex_number(ztt_intervals[weight]["embedding"]) + r' & '
		slide += r'$\pm$'+latex_percentage(ztt_intervals[weight]["percentage_stat_embedding"]) + r' & '
		slide += latex_percentage(ztt_intervals[weight]["percentage_embedding"]) + r' \\'+'\n'
	slide += r'\end{tabular}}'+'\n'
	slide += r'\end{table}'+'\n'
	slide += r'\end{center}'+'\n'

	slide += r'\end{frame}'+'\n'
	slide += '\n'
	return slide


for weight in sorted(weight_keys):
	latex_tables_file.write(create_slide(weight))
latex_tables_file.close()

summary_table_file.write(create_summary())
summary_table_file.close()

ztt_summary_table_file.write(create_ztt_summary())
ztt_summary_table_file.close()

