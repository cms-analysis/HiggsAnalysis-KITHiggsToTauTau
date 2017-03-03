import os
import argparse


if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description="Make Embedding control plots and scale to data or ztt.")
	parser.add_argument("-s", "--scale-to", required=False, default = "ztt", help="Scale Embedding to ztt. Note: data option not implemented yet. [Default: %(default)s]")
	parser.add_argument("-i", "--input",dest='inp', required=False, default = "/storage/a/akhmet/htautau/artus/2017-02-09_00-10_analysis/merged/", help="Input files. [Default: %(default)s]")
	parser.add_argument("-o", "--output",dest='outp', required=False, default = ".", help="Output dir for plots. Default: [Default: %(default)s]")
	parser.add_argument("-c", "--channel", nargs='*', required=False, default = ['mt'], help="Tau decay channels. [Default: %(default)s]")
	parser.add_argument("-x", "--quantities", nargs="*",
	                    default=["integral",
	                             "pt_1", "eta_1", "phi_1", "m_1", "iso_1", "mt_1",
	                             "pt_2", "eta_2", "phi_2", "m_2", "iso_2", "mt_2",
	                             "pt_sv", "eta_sv", "phi_sv", "m_sv", "m_vis", "ptvis",
	                             "met", "metphi", "metcov00", "metcov01", "metcov10", "metcov11",
	                             "mvamet", "mvametphi", "mvacov00", "mvacov01", "mvacov10", "mvacov11",
	                             "pZetaMissVis", "pzetamiss", "pzetavis",
	                             "jpt_1", "jeta_1", "jphi_1",
	                             "jpt_2", "jeta_2", "jphi_2",
	                             "njetspt30", "mjj", "jdeta", "njetingap20", "njetingap",
	                             "trigweight_1", "trigweight_2", "puweight",
	                             "npv", "npu", "rho"],
	                    help="Quantities. [Default: %(default)s]")
	parser.add_argument("--cache",dest='cache', required=False, action='store_true', default = False, help="Use cached integral file from previous plotting. [Default: %(default)s]")
	parser.add_argument("-b","--background", required=False, default = 'emb_scaled', help="Background estimation to plot. [Default: %(default)s]. Options: emb_scaled, emb_unscaled, ztt")
	parser.add_argument("-d","--decaymode", nargs="*",required=False, default = [''], help="Optionally split plots in decay modes. Select 'split' to create four folders with all individual decay modes or select decay modes to plot. Embedded samples will be scaled for each individual decay mode. [Default: inclusive].  Options: inclusive, split, 1prong, 1prongpi0, 3prong")
	parser.add_argument("-w","--weight", required=False, default = '', help="Add custom weights.")

	args = parser.parse_args()
	cache1=False
	cache2=False
	if not args.cache:
		if os.path.exists('IntegralValues.txt'):
			os.remove('IntegralValues.txt')
		if os.path.exists('IntegralValues_Embedded.txt'):
			os.remove('IntegralValues_Embedded.txt')
	else:
		if os.path.exists('IntegralValues.txt'):
			cache1=True
		if os.path.exists('IntegralValues_Embedded.txt'):
			cache2=True		
	emb_weights=['1.0','1.0','1.0','1.0']
	nthreads=len(args.quantities) if len(args.quantities)<20 else 20
	if args.weight is not '':
		args.weight="*"+args.weight
	if 'split' in args.decaymode:
		args.decaymode=['inclusive', '1prong', '1prongpi0', '3prong']
	
	for channel in args.channel:
		for decay_mode in args.decaymode:
			if channel=='mt':
				title='#mu#tau_{h}'
			elif channel=='et':
				title='e#tau_{h}'
			elif channel=='tt':
				title='#tau_{h}#tau_{h}'
			elif channel=='em':
				title=='e#mu'
				args.decaymode=['']
			else:
				print 'Channel not implemented.'
				exit()
			if decay_mode=='inclusive' or decay_mode=='':
				decay_weight=''
			elif decay_mode=='1prong':
				decay_weight='*(decayMode_2==0)'
				title+=' Single Prong'
			elif decay_mode=='1prongpi0':
				decay_weight='*(decayMode_2==1)'
				title+=' Single Prong+#pi^{0}'
			elif decay_mode=='3prong':
				decay_weight='*(decayMode_2==10)'
				title+=' Three Prong'
			else:
				print 'Decay Mode '+decay_mode+' not implemented.'
				exit()
			print 'Plotting '+channel+' '+decay_mode+'...'
			
			'''
			Create plot of default ztt integral. By selection -b ztt not only integral but all quantities specified by -x [...] are plotted.
			'''
			command=os.environ["CMSSW_BASE"]+'/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py'
			command+=' -i '+args.inp
			command+=' -c '+channel
			command+=' -w \"(1.0)'+args.weight+decay_weight+'\"'
			command+=' -n '+str(nthreads)+' --era 2016 -r '
			command+='-x integral '
			if args.background=='ztt':
				for x in args.quantities:
					command+=' '+x
			command+=' --full-integral'
			command+=' -a \'--y-subplot-lims 0.5 1.5 -t \" '+title+'\"\''
			command+=' -o '+os.path.join(args.outp,channel,decay_mode,args.scale_to)
			if not cache1 and not args.background=='emb_unscaled':
				os.system(command)
			if args.background=='ztt':
				continue
			
			'''
			Read out ztt integral.
			'''
			with open('IntegralValues.txt','r') as integralfile:
				if args.scale_to=='ztt':
					for line in integralfile.readlines():
						if 'nick: ztt' in line:
							value_ztt=float(line.strip('nick: ztt category: None integral: '))
							break
				elif args.scale_to=='data':
					for line in integralfile.readlines():
						if 'nick: data' in line:
							value_ztt=float(line.strip('nick: data category: None integral: '))
							break
				else:
					print 'Possible options for --scale-to: [data,ztt]'
					exit()
		
			'''
			Create plot of unscaled embedding integral. By selecting -b ztt not only integral but all quantities specified by -x [...] are plotted.
			'''
			command=command.replace(os.path.join(args.outp,channel,decay_mode,args.scale_to),os.path.join(args.outp,channel,decay_mode,'emb'))
			title_emb=title+(' embedded' if decay_mode=='inclusive' else ' emb')
			command=command.replace(' -a \'--y-subplot-lims 0.5 1.5 -t \" '+title+'\"\'',' -a \'--y-subplot-lims 0.5 1.5 -t \" '+title_emb+'\"\'')
			command+=' --emb'
			if not cache2:
				os.system(command)
			if args.background=='emb_unscaled':
				continue
				
			'''Calculate scale factors and save in scale_factor.txt in output dir.'''
			with open('IntegralValues_Embedded.txt','r') as integralfile:
				for line in integralfile.readlines():
					if 'nick: ztt' in line:
						value_emb=float(line.strip('nick: ztt category: None integral: '))
			scale_factor=value_ztt/value_emb
			
			with open(os.path.join(args.outp,channel,decay_mode,'scale_factor.txt'),'w') as scalefile:
				scalefile.write('Scalefactor: '+str(scale_factor))
		
			if args.scale_to=='ztt':
				print "Embedded samples will be scaled by "+str(scale_factor)+" to match default ztt background."
			elif args.scale_to=='data':
				print "Embedded samples will be scaled by "+str(scale_factor)+" to match data."
			if channel=='mt':
				emb_weights[0]=str(scale_factor)
			if channel=='et':
				emb_weights[1]=str(scale_factor)
			if channel=='em':
				emb_weights[2]=str(scale_factor)
			if channel=='tt':
				emb_weights[3]=str(scale_factor)

			'''
			Create plots of scaled embedding. By selecting -b emb (set by default) all quantities specified by -x [...] are plotted.
			'''
			command=command.replace(os.path.join(args.outp,channel,decay_mode,'emb'),os.path.join(args.outp,channel,decay_mode,'emb_scaled'))
			command+=' -x'
			for x in args.quantities:
				command+=' '+x
			command+=' --embedded-weights'
			for w in emb_weights:
				command+=' '+w
			command=command.replace('--full-integral','')
			os.system(command)
			if len(args.decaymode)>1 or not args.cache:
				os.remove('IntegralValues.txt')
				os.remove('IntegralValues_Embedded.txt')

