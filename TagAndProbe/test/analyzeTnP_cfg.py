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

###
# Create efficiencies
###
PTBINME42 = cms.PSet(
   isME42Region = cms.vstring("true"),
   eta = cms.vdouble(1.2,1.8),
   pt = cms.vdouble(20.0, 40.0, 60.0, 80.0, 100.0, 500.0),
)

PTBINNOME42 = PTBINME42.clone(isME42Region = cms.vstring("false"))

ISME42BIN = cms.PSet(
   eta = cms.vdouble(1.2,1.8),
   isME42 = cms.vdouble(-0.5,0.5,1.5),
)

EFFPSET = cms.PSet(
   EfficiencyCategoryAndState = cms.vstring(),
   UnbinnedVariables = cms.vstring("mass"),
   BinnedVariables = cms.PSet(),
   BinToPDFmap = cms.vstring("voigtianPlusExponential")
)

PTTIGHTME42 = EFFPSET.clone(EfficiencyCategoryAndState = cms.vstring("isTightMuon","true"), BinnedVariables = PTBINME42)
PTTIGHTNOME42 = PTTIGHTME42.clone(BinnedVariables = PTBINNOME42)
PTLOOSEME42 = PTTIGHTME42.clone(EfficiencyCategoryAndState = cms.vstring("isLooseMuon","true"))
PTLOOSENOME42 = PTLOOSEME42.clone(BinnedVariables = PTBINNOME42)

ISME42TIGHT = PTTIGHTME42.clone(BinnedVariables = ISME42BIN)
ISME42LOOSE = PTLOOSEME42.clone(BinnedVariables = ISME42BIN)

EFF = cms.PSet(
   pt_tight_ME42 = PTTIGHTME42,
   pt_tight_NoME42 = PTTIGHTNOME42,
   pt_loose_ME42 = PTLOOSEME42,
   pt_loose_NoME42 = PTLOOSENOME42,
   isME42_tight = ISME42TIGHT,
   isME42_loose = ISME42LOOSE,
)

# Prepare Efficiency PSet
Eff = cms.PSet(
    # pt
    pt_tight = cms.PSet(
        EfficiencyCategoryAndState = cms.vstring("isTightMuon","true"),
        UnbinnedVariables = cms.vstring("mass"),
        BinnedVariables = cms.PSet(
            isME42Region = cms.vstring("true"),
            eta = cms.vdouble(1.2,1.8),
            pt = cms.vdouble(20.0, 40.0, 60.0, 80.0, 100.0, 500.0),
        ),
        BinToPDFmap = cms.vstring("voigtianPlusExponential")
    ),
    pt_loose = cms.PSet(
        EfficiencyCategoryAndState = cms.vstring("isLooseMuon","true"),
        UnbinnedVariables = cms.vstring("mass"),
        BinnedVariables = cms.PSet(
            isME42Region = cms.vstring("true"),
            eta = cms.vdouble(1.2,1.8),
            pt = cms.vdouble(20.0, 40.0, 60.0, 80.0, 100.0, 500.0),
        ),
        BinToPDFmap = cms.vstring("voigtianPlusExponential")
    ),
    # isME42 
    isME42_tight = cms.PSet(
        EfficiencyCategoryAndState = cms.vstring("isTightMuon","true"),
        UnbinnedVariables = cms.vstring("mass"),
        BinnedVariables = cms.PSet(
            eta = cms.vdouble(1.2,1.8),
            isME42 = cms.vdouble(-0.5,0.5,1.5),
        ),
        BinToPDFmap = cms.vstring("voigtianPlusExponential")
    ),
    isME42_loose = cms.PSet(
        EfficiencyCategoryAndState = cms.vstring("isLooseMuon","true"),
        UnbinnedVariables = cms.vstring("mass"),
        BinnedVariables = cms.PSet(
            eta = cms.vdouble(1.2,1.8),
            isME42 = cms.vdouble(-0.5,0.5,1.5),
        ),
        BinToPDFmap = cms.vstring("voigtianPlusExponential")
    ),
)

###
# prepare analyzer
###

process = cms.Process("TagProbe")

process.load('FWCore.MessageService.MessageLogger_cfi')

process.source = cms.Source("EmptySource")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

from CSCDetectorStudies.TagAndProbe.analyzerVariables_cfi import *

process.TagProbeFitTreeAnalyzer = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
    InputFileNames = cms.vstring(options.inputFiles),
    InputDirectoryName = cms.string(options.inputDirectoryName),
    InputTreeName = cms.string("fitter_tree"),
    OutputFileName = cms.string(options.outputFile),
    NumCPU = cms.uint32(1),
    SaveWorkspace = cms.bool(True),
    Variables = cms.PSet(
       KinematicVariables,
       mass = cms.vstring("Tag-Probe Mass", "60.0", "120.0", "GeV/c^{2}"),
       isME42 = cms.vstring("Probe Region","0","2",""),
    ),
    Categories = cms.PSet(
       MuonIDCategories,
       isME42Region = cms.vstring("ME42 Region","dummy[true=1,false=0]"),
    ),
    Cuts = cms.PSet(
        eta12 = cms.vstring("lower ME42 cut","eta","1.2"),
        eta18 = cms.vstring("upper ME42 cut","eta","1.8"),
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
    Efficiencies = EFF
)

#process.TagProbeFitTreeAnalyzerSta = TagProbeFitTreeAnalyzer.clone(
#    InputFileNames = cms.vstring(options.inputFiles),
#    InputDirectoryName = cms.string("tagProbeTreeSta"),
#    InputTreeName = cms.string("fitter_tree"),
#    OutputFileName = cms.string("ME42TagAndProbeTreeAnalysisSta.root"),
#    NumCPU = cms.uint32(1),
#    SaveWorkspace = cms.bool(True),
#    Variables = cms.PSet(
#       KinematicVariables,
#    #   standAloneVariables,
#       mass = cms.vstring("Tag-Probe Mass", "60.0", "120.0", "GeV/c^{2}"),
#       isME42 = cms.vstring("Probe Region","0","2",""),
#    ),
#    Categories = cms.PSet(
#       MuonIDCategories,
#    #   hasTrack = cms.vstring("pass","dummy[true=1,false=0]"),
#    #   staPassingTrk = cms.vstring("pass","dummy[true=1,false=0]"),
#    ),
#    Efficiencies = Eff
#)

####
# Path
####
process.fitness = cms.Path(
    process.TagProbeFitTreeAnalyzer
)

