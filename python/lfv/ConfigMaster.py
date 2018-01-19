import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
import Artus.Utility.jsonTools as jsonTools

### Enumeration class for possible plotting/analysis modules

class Plotmodule():
	control_plot = 0
	sum_of_hists = 1
	efficiency_plot = 2
	shape_plot = 3
	datacard = 4
	bkg_reduction_plot = 5
	cutflow_plot = 6
	ratio = 7
	limit = 8

### Class to create harry plotter configs for your special desire. All configs are safed as dictionaries and can be combined to the final config which is needed	

class ConfigMaster(object):

	##Constructor

	def __init__(self, base_values, sample_values = None):

		self._config = {}

		###Config which is initiliazed with information for each sample from samples_run2_201X.py if wished
		if sample_values != None:
			sample_settings = samples.Samples()	
			sample_list, channel, category, no_plot, nick_suffix, weight, estimationMethod, cut_type = sample_values

			self._config = sample_settings.get_config(samples=[getattr(samples.Samples, sample) for sample in sample_list], channel = channel, category = category, no_plot = no_plot, nick_suffix = nick_suffix, weight = weight, estimationMethod = estimationMethod, cut_type = cut_type)

		###Fill config with basic information

		for (key, value) in self.__base__(*base_values).iteritems():
			self._config[key] = value


		###Dictionary with all possible plotting/analysis modules

		self._modules_dict = {
					Plotmodule.control_plot:		self.__controlplot__,
					Plotmodule.sum_of_hists:		self.__sumofhists__,
					Plotmodule.efficiency_plot:		self.__efficiencyplot__,
					Plotmodule.shape_plot:			self.__shapeplot__,
					Plotmodule.datacard: 			self.__datacard__,
					Plotmodule.bkg_reduction_plot:		self.__bkgreductionplot__,
					Plotmodule.cutflow_plot:		self.__cutflowplot__,
					Plotmodule.ratio:			self.__ratio__,
					Plotmodule.limit:			self.__limitplot__
		}

	###Dictionaries for information for each plotting/analysis modules

	def __base__(self, input_dir, output_dir, output_file, formats, www, www_nodate, x_expressions, x_bins):
	
		self._base = {
					"directories":			input_dir,
					"output_dir":			output_dir,
					"filename":			output_file,
					"formats":			formats,
					"www":				www,
					"www_nodate":			www_nodate,
					"x_expressions":		x_expressions,
					"x_bins":			x_bins,
		}

		return self._base

		
	def __controlplot__(self, x_label, title, legend, lumis, energies, year, www):
		
		self._controlplot = {
					"x_label":			x_label,
					"legend":			legend,
					"lumis"	:			lumis,
					"energies":			energies,
					"title"	:			title,
					"year":				year,
					"www":				www
		}

		return self._controlplot


	def __sumofhists__(self, analysis_mod, sum_nicks, result_nicks):
	
		self._sumofhists = {
					"analysis_modules":		analysis_mod,
					"sum_nicks":			sum_nicks,
					"sum_result_nicks":		result_nicks
		}

		return self._sumofhists

	def __efficiencyplot__(self, analysis_mod, bkg_nicks, sig_nicks, cut_modes, cut_nicks, whitelist, markers,  y_label, lower_cut, plot_modules, output_dir):
		
		self._efficiencyplot = {
					"analysis_modules":		analysis_mod,
					"output_dir":			output_dir,
					"cut_efficiency_bkg_nicks":	bkg_nicks,
					"cut_efficiency_sig_nicks":	sig_nicks,
					"cut_efficiency_nicks":		cut_nicks,
					"cut_efficiency_modes":		cut_modes,
					"nicks_whitelist":		whitelist,
					"markers":			markers,
					"y_label":			y_label,
					"select_lower_values":		lower_cut,
					"plot_modules":			plot_modules
		}

		return self._efficiencyplot

	def __shapeplot__(self, y_label, analysis_mod):
		
		self._shapeplot = {
					"y_label":			y_label,
					"analysis_modules":		analysis_mod					
		}

		return self._shapeplot


	def __datacard__(self, labels, plot_modules, file_mode):

		self._datacard = {
					"labels":			labels,
					"plot_modules":			plot_modules,
					"file_mode":			file_mode
		}

		return self._datacard

	def __bkgreductionplot__(self, numerator_nicks, denominator_nicks, result_nicks, no_errors, analysis_modules, y_lims, markers, colors, labels, legend, legend_markers, y_label):

		self._bkgreductionplot = {
					"divide_numerator_nicks":	numerator_nicks,
					"divide_denominator_nicks":	denominator_nicks,
					"divide_result_nicks":		result_nicks,
					"divide_denominator_no_errors":	no_errors,
					"analysis_modules":		analysis_modules,
					"y_lims":			y_lims,
					"markers":			markers,
					"colors":			colors, 
					"labels":			labels, 
					"legend":			legend, 
					"legend_markers":		legend_markers,
					"y_label":			y_label
		}	
	
		return self._bkgreductionplot

	def __cutflowplot__(self, files, markers, nicks, x_tick_labels, stacks): 

		self._cutflowplot = {
				
					"files":			files,
					"markers":			markers, 
					"nicks":			nicks, 
					"x_tick_labels":		x_tick_labels, 
					"stacks":			stacks,
		}
		
		return self._cutflowplot

	def __ratio__(self, ratio_numerator_nicks, ratio_denominator_nicks, ratio_result_nicks, analysis_modules, markers, stacks):
		
		self._ratio = {
					"ratio_numerator_nicks":	ratio_numerator_nicks, 
					"ratio_denominator_nicks":	ratio_denominator_nicks,
					"ratio_result_nicks":		ratio_result_nicks, 
					"analysis_modules":		analysis_modules,
					"markers":			markers,
					"stacks":			stacks
		}

		return self._ratio


	def __limitplot__(self, y_label, files, folders, y_expressions, markers, colors, fill_styles, marker_styles, line_widths, tree_draw_options, y_tick_labels, nicks, x_lims, y_lims):

		self._limitplot = {
					"y_label":			y_label,
					"files":			files,
					"folders":			folders,
					"y_expressions":		y_expressions,
					"markers":			markers,
					"colors":			colors,
					"fill_styles":			fill_styles,
					"marker_styles":		marker_styles,
					"line_widths":			line_widths,
					"tree_draw_options":		tree_draw_options,
					"y_tick_labels":		y_tick_labels,
					"nicks":			nicks,
					"x_lims":			x_lims,
					"y_lims":			y_lims
					
		}

		return self._limitplot

	###Function for adding information to the config

	def add_config_info(self, module_values, module):
		
		###Fill config will all module information checking if values are already avaible as list or string
		for (key, value) in self._modules_dict[module](*module_values).iteritems():
			try:
				if type(value) == list:
					self._config[key].extend(value)
				
				else:
					self._config[key].append(value)

			except AttributeError:
				self._config[key] += value

			except KeyError:
				self._config[key] = value

	##Change specific values or add new key by hand

	def change_config_info(self, keys, values):
		if type(keys) == list:
			for (key, value) in zip(keys, values):
				try:
					if type(value) == list:
						self._config[key].extend(value)
				
					else:
						self._config[key].append(value)

				except AttributeError:
					self._config[key] += value

				except KeyError:
					self._config[key] = value	
		else:
			try:
				if type(values) == list:
					self._config[keys].extend(values)
				
				else:
					self._config[keys].append(values)


			except AttributeError:
				self._config[keys] += values

			except KeyError:		
				self._config[keys] = values		


	##Function for deleting entries in the dictionary
	
	def pop(self, config_keys):
		if type(config_keys) == list:
			for key in config_keys:
				self._config.pop(key)

		else:
			self._config.pop(config_keys)
		

	##Merges merge config into the config of the configmaster by keys you give the function

	def merge_by_keys(self, merge_config, keys):
		for key in keys:
			if type(merge_config[key]) == list:
				self._config[key].extend(merge_config[key])
			
			else: 
				self._config[key].append(merge_config[key])

	##Using pretty print to print actual config

	def print_config(self):
		import pprint
		pprint.pprint(self._config)

	###Returns build config
			
	def return_config(self):
		return self._config

