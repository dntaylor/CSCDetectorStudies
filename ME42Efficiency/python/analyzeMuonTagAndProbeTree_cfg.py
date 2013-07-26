import FWCore.ParameterSet.Config as cms

process = cms.Process("TagProbe")

process.load('FWCore.MessageService.MessageLogger_cfi')

process.source = cms.Source("EmptySource")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )   

process.TagProbeFitTreeAnalyzer = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
	# IO parameters:
	InputFileNames = cms.vstring("ME42TagAndProbeTree.root"),
	InputDirectoryName = cms.string("tagAndProbeTree"),
	InputTreeName = cms.string("fitter_tree"),
	OutputFileName = cms.string("ME42TagAndProbeTreeAnalysis.root"),
	#numbrer of CPUs to use for fitting
	NumCPU = cms.uint32(1),
	# specifies wether to save the RooWorkspace containing the data for each bin and
	# the pdf object with the initial and final state snapshots
	SaveWorkspace = cms.bool(True),
	# defines all the real variables of the probes available in the input tree and intended for use in the efficiencies
	Variables = cms.PSet(
		mass = cms.vstring("Tag-Probe Mass", "60.0", "120.0", "GeV/c^{2}"),
		pt = cms.vstring("Probe p_{T}", "0", "500", "GeV/c"),
		eta = cms.vstring("Probe #eta", "1.2", "1.8", ""),
	),
	# defines all the discrete variables of the probes available in the input tree and intended for use in the efficiency calculations
	Categories = cms.PSet(
		mcTrue = cms.vstring("MC true", "dummy[true=1,false=0]"),
		Glb = cms.vstring("isGlobalMuon", "dummy[true=1,false=0]"),
#		TM = cms.vstring("isTrackerMuon", "dummy[true=1,false=0]"),
	),
	# defines all the PDFs that will be available for the efficiency calculations; uses RooFit's "factory" syntax;
	# each pdf needs to define "signal", "backgroundPass", "backgroundFail" pdfs, "efficiency[0.9,0,1]" and "signalFractionInPassing[0.9]" are used for initial values  
	PDFs = cms.PSet(
		gaussPlusLinear = cms.vstring(
			"Gaussian::signal(mass, mean[3.1,3.0,3.2], sigma[0.03,0.01,0.05])",
			"Chebychev::backgroundPass(mass, cPass[0,-1,1])",
			"Chebychev::backgroundFail(mass, cFail[0,-1,1])",
			"efficiency[0.9,0,1]",
			"signalFractionInPassing[0.9]"
		),
		gaussPlusQuadratic = cms.vstring(
			"Gaussian::signal(mass, mean[3.1,3.0,3.2], sigma[0.03,0.01,0.05])",
			"Chebychev::backgroundPass(mass, {cPass1[0,-1,1], cPass2[0,-1,1]})",
		        "Chebychev::backgroundFail(mass, {cFail1[0,-1,1], cFail2[0,-1,1]})",
			"efficiency[0.9,0,1]",
			"signalFractionInPassing[0.9]"
		),
		voigtianPlusExponential = cms.vstring(
			"Voigtian::signalPass(mass, meanP[90,80,100], width[2.495], sigmaP[3,1,20])",
			"Voigtian::signalFail(mass, meanF[90,80,100], width[2.495], sigmaF[3,1,20])",
			"Exponential::backgroundPass(mass, lp[0,-5,5])",
			"Exponential::backgroundFail(mass, lf[0,-5,5])",
			"efficiency[0.9,0,1]",
			"signalFractionInPassing[0.9]"
		),
	),

	# defines a set of efficiency calculations, what PDF to use for fitting and how to bin the data;
	# there will be a separate output directory for each calculation that includes a simultaneous fit, side band subtraction and counting. 
        Efficiencies = cms.PSet(
		#the name of the parameter set becomes the name of the directory
#		Glb_pt_eta = cms.PSet(
#			#specifies the efficiency of which category and state to measure 
#			EfficiencyCategoryAndState = cms.vstring("Glb","true"),
#			#specifies what unbinned variables to include in the dataset, the mass is needed for the fit
#			UnbinnedVariables = cms.vstring("mass"),
#			#specifies the binning of parameters
#			BinnedVariables = cms.PSet(
#				pt = cms.vdouble(20.0, 60.0, 100.0),
#				eta = cms.vdouble(1.2, 1.5, 1.8),
#			),
#			#first string is the default followed by binRegExp - PDFname pairs
#			BinToPDFmap = cms.vstring("voigtianPlusExponential")
#		),
#		Glb_pt_abseta_mcTrue = cms.PSet(
#			EfficiencyCategoryAndState = cms.vstring("Glb","true"),
#			UnbinnedVariables = cms.vstring("mass"),
#			BinnedVariables = cms.PSet(
#				mcTrue = cms.vstring("true"),
#				pt = cms.vdouble(3.0, 6.0, 20.0),
#				eta = cms.vdouble(0.0, 1.2, 2.4),
#			)
#			#unspecified binToPDFmap means no fitting
#		),
		Glb_pt = cms.PSet(
			EfficiencyCategoryAndState = cms.vstring("Glb","true"),
		        UnbinnedVariables = cms.vstring("mass"),
			BinnedVariables = cms.PSet(
				pt = cms.vdouble(20.0, 60.0, 100.0),
			),
			BinToPDFmap = cms.vstring("voigtianPlusExponential")
		),
#		Glb_pt_mcTrue = cms.PSet(
#			EfficiencyCategoryAndState = cms.vstring("Glb","true"),
#		        UnbinnedVariables = cms.vstring("mass"),
#			BinnedVariables = cms.PSet(
#				mcTrue = cms.vstring("true"),
#				pt = cms.vdouble(3.0, 6.0, 20.0),
#			)
#		),
	)
)

process.fitness = cms.Path(
	process.TagProbeFitTreeAnalyzer
)
	
