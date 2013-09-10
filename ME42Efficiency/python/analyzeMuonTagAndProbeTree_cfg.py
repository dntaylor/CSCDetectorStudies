import FWCore.ParameterSet.Config as cms
from ROOT import TMath

# Choose analysis to run
#ANALYSIS = 0 # all (not coded)
#ANALYSIS = 1 # basic
#ANALYSIS = 2 # ME42
#ANALYSIS = 3 # ME42With3Of4
#ANALYSIS = 4 # NoME42
#ANALYSIS = 5 # ME42Eta
#ANALYSIS = 6 # ME42With3Of4Eta
ANALYSIS = 7 # NoME42Eta
#ANALYSIS = 8 # ME42Phi
#ANALYSIS = 9 # ME42With3Of4Phi
#ANALYSIS = 10# NoME42Phi

# file variables
if ANALYSIS==0:
	pass # not coded
elif ANALYSIS==1:
	INPUTDIRECTORYNAME = "tagAndProbeTree"
	OUTPUTFILENAME = "ME42TagAndProbeTreeAnalysis.root"
elif ANALYSIS==2:
	INPUTDIRECTORYNAME = "tagAndProbeTreeME42"
	OUTPUTFILENAME = "ME42TagAndProbeTreeAnalysisME42.root"
elif ANALYSIS==3:
	INPUTDIRECTORYNAME = "tagAndProbeTreeME42With3Of4"
	OUTPUTFILENAME = "ME42TagAndProbeTreeAnalysisME42With3Of4.root"
elif ANALYSIS==4:
	INPUTDIRECTORYNAME = "tagAndProbeTreeNoME42"
	OUTPUTFILENAME = "ME42TagAndProbeTreeAnalysisNoME42.root"
elif ANALYSIS==5:
	INPUTDIRECTORYNAME = "tagAndProbeTreeME42Eta"
	OUTPUTFILENAME = "ME42TagAndProbeTreeAnalysisME42Eta.root"
elif ANALYSIS==6:
	INPUTDIRECTORYNAME = "tagAndProbeTreeME42With3Of4Eta"
	OUTPUTFILENAME = "ME42TagAndProbeTreeAnalysisME42With3Of4Eta.root"
elif ANALYSIS==7:
	INPUTDIRECTORYNAME = "tagAndProbeTreeNoME42Eta"
	OUTPUTFILENAME = "ME42TagAndProbeTreeAnalysisNoME42Eta.root"
elif ANALYSIS==8:
	INPUTDIRECTORYNAME = "tagAndProbeTreeME42Phi"
	OUTPUTFILENAME = "ME42TagAndProbeTreeAnalysisME42Phi.root"
elif ANALYSIS==9:
	INPUTDIRECTORYNAME = "tagAndProbeTreeME42With3Of4Phi"
	OUTPUTFILENAME = "ME42TagAndProbeTreeAnalysisME42With3Of4Phi.root"
elif ANALYSIS==10:
	INPUTDIRECTORYNAME = "tagAndProbeTreeNoME42Phi"
	OUTPUTFILENAME = "ME42TagAndProbeTreeAnalysisNoME42Phi.root"

# Prepare Efficiency PSet
EFFICIENCIES = cms.PSet( 
	# Tight pt muon cuts
	tight_pt = cms.PSet(
		EfficiencyCategoryAndState = cms.vstring("passingTightMuon","true"),
		UnbinnedVariables = cms.vstring("mass"),
		BinnedVariables = cms.PSet(
			pt = cms.vdouble(20.0, 40.0, 60.0, 80.0, 100.0, 500.0),
		),
		BinToPDFmap = cms.vstring("voigtianPlusExponential")
	),
	# loost muon pt cuts
	loose_pt = cms.PSet(
		EfficiencyCategoryAndState = cms.vstring("passingLooseMuon","true"),
		UnbinnedVariables = cms.vstring("mass"),
		BinnedVariables = cms.PSet(
			pt = cms.vdouble(20.0, 40.0, 60.0, 80.0, 100.0, 500.0),
		),
		BinToPDFmap = cms.vstring("voigtianPlusExponential")
	),
#	# tight muon eta cuts
#	tight_eta = cms.PSet(
#		EfficiencyCategoryAndState = cms.vstring("passingTightMuon","true"),
#		UnbinnedVariables = cms.vstring("mass"),
#		BinnedVariables = cms.PSet(
#			eta = cms.vdouble(-2.4, -1.8, -1.2, 0.0, 1.2, 1.8, 2.4),
#		),
#		BinToPDFmap = cms.vstring("voigtianPlusExponential")
#	),
#	# loose muon eta cuts
#	loose_eta = cms.PSet(
#		EfficiencyCategoryAndState = cms.vstring("passingLooseMuon","true"),
#		UnbinnedVariables = cms.vstring("mass"),
#		BinnedVariables = cms.PSet(
#			eta = cms.vdouble(-2.4, -1.8, -1.2, 0.0, 1.2, 1.8, 2.4),
#		),
#		BinToPDFmap = cms.vstring("voigtianPlusExponential")
#	),
#	# tight muon phi cuts
#	tight_phi = cms.PSet(
#		EfficiencyCategoryAndState = cms.vstring("passingTightMuon","true"),
#		UnbinnedVariables = cms.vstring("mass"),
#		BinnedVariables = cms.PSet(
#			phi = cms.vdouble(-TMath.Pi(), -2.0/3.0*TMath.Pi(), -TMath.Pi()/3.0, 0, TMath.Pi()/3.0, 2.0/3.0*TMath.Pi(), TMath.Pi()),
#		),
#		BinToPDFmap = cms.vstring("voigtianPlusExponential")
#	),
#	# loose muon phi cuts
#	loose_phi = cms.PSet(
#		EfficiencyCategoryAndState = cms.vstring("passingLooseMuon","true"),
#		UnbinnedVariables = cms.vstring("mass"),
#		BinnedVariables = cms.PSet(
#			phi = cms.vdouble(-TMath.Pi(), -2.0/3.0*TMath.Pi(), -TMath.Pi()/3.0, 0, TMath.Pi()/3.0, 2.0/3.0*TMath.Pi(), TMath.Pi()),
#		),
#		BinToPDFmap = cms.vstring("voigtianPlusExponential")
#	),
	# ME4/2 tight muon cut
	tight_ME42 = cms.PSet(
		EfficiencyCategoryAndState = cms.vstring("passingTightMuon","true"),
		UnbinnedVariables = cms.vstring("mass"),
		BinnedVariables = cms.PSet(
			isME42 = cms.vdouble(-0.5, 0.5, 1.5),
		),
		BinToPDFmap = cms.vstring("voigtianPlusExponential")
	),
	# ME4/2 loose muon cut
	loose_ME42 = cms.PSet(
		EfficiencyCategoryAndState = cms.vstring("passingLooseMuon","true"),
		UnbinnedVariables = cms.vstring("mass"),
		BinnedVariables = cms.PSet(
			isME42 = cms.vdouble(-0.5, 0.5, 1.5),
		),
		BinToPDFmap = cms.vstring("voigtianPlusExponential")
	),
)

#ALL = [1,2,3]
#ETA = [4,5]
#PHI = [6,7]
#
#EFFICIENCIESALL = cms.PSet(tight_pt,loose_pt,tight_eta,loose_eta,tight_phi,loose_phi)
#EFFICIENCIESETA = cms.PSet(tight_pt,loose_pt,tight_phi,loose_phi)
#EFFICIENCIESPHI = cms.PSet(tight_pt,loose_pt,tight_eta,loose_eta)
#
#if ANALYSIS in ALL:
#	EFFICIENCIES = EFFICIENCIESALL
#elif ANALYSIS in ETA:
#	EFFICIENCIES = EFFICIENCIESETA
#elif ANALYSIS in PHI:
#	EFFICIENCIES = EFFICIENCIESPHI

process = cms.Process("TagProbe")

process.load('FWCore.MessageService.MessageLogger_cfi')

process.source = cms.Source("EmptySource")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )   

process.TagProbeFitTreeAnalyzer = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
	InputFileNames = cms.vstring("ME42TagAndProbeTree.root"),
	InputDirectoryName = cms.string(INPUTDIRECTORYNAME),
	InputTreeName = cms.string("fitter_tree"),
	OutputFileName = cms.string(OUTPUTFILENAME),
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
		passingTightMuon = cms.vstring("tight", "dummy[true=1,false=0]"),
                passingLooseMuon = cms.vstring("loose", "dummy[true=1,false=0]"),
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
# analyzer clones
####
#process.TagProbeFitTreeAnalyzerME42 = process.TagProbeFitTreeAnalyzer.clone( 
#	InputDirectoryName = cms.string("tagAndProbeTreeME42"),
#        OutputFileName = cms.string("ME42TagAndProbeTreeAnalysisME42.root"),
#)
#process.TagProbeFitTreeAnalyzerNoME42 = process.TagProbeFitTreeAnalyzer.clone( 
#	InputDirectoryName = cms.string("tagAndProbeTreeNoME42"),
#        OutputFileName = cms.string("ME42TagAndProbeTreeAnalysisNoME42.root"),
#)
#process.TagProbeFitTreeAnalyzerME42Eta = process.TagProbeFitTreeAnalyzer.clone( 
#	InputDirectoryName = cms.string("tagAndProbeTreeME42Eta"),
#        OutputFileName = cms.string("ME42TagAndProbeTreeAnalysisME42Eta.root"),
#)
#process.TagProbeFitTreeAnalyzerNoME42Eta = process.TagProbeFitTreeAnalyzer.clone( 
#	InputDirectoryName = cms.string("tagAndProbeTreeNoME42Eta"),
#        OutputFileName = cms.string("ME42TagAndProbeTreeAnalysisNoME42Eta.root"),
#)
#process.TagProbeFitTreeAnalyzerME42Phi = process.TagProbeFitTreeAnalyzer.clone( 
#	InputDirectoryName = cms.string("tagAndProbeTreeME42Phi"),
#        OutputFileName = cms.string("ME42TagAndProbeTreeAnalysisME42Phi.root"),
#)
#process.TagProbeFitTreeAnalyzerNoME42Phi = process.TagProbeFitTreeAnalyzer.clone( 
#	InputDirectoryName = cms.string("tagAndProbeTreeNoME42Phi"),
#        OutputFileName = cms.string("ME42TagAndProbeTreeAnalysisNoME42Phi.root"),
#)

####
# Path
####
process.fitness = cms.Path(
	process.TagProbeFitTreeAnalyzer #*
#	(process.TagProbeFitTreeAnalyzerME42 + process.TagProbeFitTreeAnalyzerNoME42 + process.TagProbeFitTreeAnalyzerME42Eta + process.TagProbeFitTreeAnalyzerNoME42Eta + process.TagProbeFitTreeAnalyzerME42Phi + process.TagProbeFitTreeAnalyzerNoME42Phi)
)
	
