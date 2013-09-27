import FWCore.ParameterSet.Config as cms
from ROOT import TMath

###
# Defaults
###
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')

options.inputFiles = "file:ME42TagAndProbeTree.root"
options.outputFile = "ME42TagAndProbeTreeAnalysis.root"
options.register ('analysisVar', 1, VarParsing.multiplicity.singleton, VarParsing.varType.int, "Select analyzer to run")
options.register ('inputDirectoryName', 'tagAndProbeTree', VarParsing.multiplicity.singleton, VarParsing.varType.string, "Analyzer input directory")
options.parseArguments()


# Choose analysis to run
#ANALYSIS = 0 # (not coded)
#ANALYSIS = 1 # all
#ANALYSIS = 2 # ME42
#ANALYSIS = 3 # Eta
#ANALYSIS = 4 # EtaNoME42

# file variables
if options.analysisVar==0:
	pass # not coded
elif options.analysisVar==1:
	options.inputDirectoryName = "tagAndProbeTree"
	options.outputFile = "ME42TagAndProbeTreeAnalysis.root"
elif options.analysisVar==2:
	options.inputDirectoryName = "tagAndProbeTreeME42"
	options.outputFile = "ME42TagAndProbeTreeAnalysisME42.root"
elif options.analysisVar==3:
	options.inputDirectoryName = "tagAndProbeTreeEta"
	options.outputFile = "ME42TagAndProbeTreeAnalysisEta.root"
elif options.analysisVar==4:
	options.inputDirectoryName = "tagAndProbeTreeEtaNoME42"
	options.outputFile = "ME42TagAndProbeTreeAnalysisEtaNoME42.root"

# Prepare Efficiency PSet
EFFICIENCIES = cms.PSet( 
	# pt muon cuts
	pt = cms.PSet(
		EfficiencyCategoryAndState = cms.vstring("trkPassingSta","true"),
		UnbinnedVariables = cms.vstring("mass"),
		BinnedVariables = cms.PSet(
			pt = cms.vdouble(20.0, 40.0, 60.0, 80.0, 100.0, 500.0),
		),
		BinToPDFmap = cms.vstring("voigtianPlusExponential")
	),
	# ME4/2 muon cut
	ME42 = cms.PSet(
		EfficiencyCategoryAndState = cms.vstring("trkPassingSta","true"),
		UnbinnedVariables = cms.vstring("mass"),
		BinnedVariables = cms.PSet(
			isME42 = cms.vdouble(-0.5, 0.5, 1.5),
		),
		BinToPDFmap = cms.vstring("voigtianPlusExponential")
	),
)

process = cms.Process("TagProbe")

process.load('FWCore.MessageService.MessageLogger_cfi')

process.source = cms.Source("EmptySource")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )   

process.TagProbeFitTreeAnalyzer = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
	InputFileNames = cms.vstring(options.inputFiles),
	InputDirectoryName = cms.string(options.inputDirectoryName),
	InputTreeName = cms.string("fitter_tree"),
	OutputFileName = cms.string(options.outputFile),
	NumCPU = cms.uint32(1),
	SaveWorkspace = cms.bool(True),
	Variables = cms.PSet(
		mass = cms.vstring("Tag-Probe Mass", "60.0", "120.0", "GeV/c^{2}"),
		pt = cms.vstring("Probe p_{T}", "0", "500", "GeV/c"),
		eta = cms.vstring("Probe #eta", "-2.4", "2.4", ""),
		phi = cms.vstring("Probe #phi", "-3.14159", "3.14159", ""),
		isME42 = cms.vstring("Probe Region","0","2",""),
	),
	Categories = cms.PSet(
		trkPassingSta = cms.vstring("pass","dummy[true=1,false=0]"),
		#passingTightMuon = cms.vstring("tight", "dummy[true=1,false=0]"),
                #passingLooseMuon = cms.vstring("loose", "dummy[true=1,false=0]"),
	),
	Cuts = cms.PSet(
	),
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

        Efficiencies = EFFICIENCIES 
)

####
# Path
####
process.fitness = cms.Path(
	process.TagProbeFitTreeAnalyzer 
)
	
