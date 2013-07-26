import FWCore.ParameterSet.Config as cms
#from PhysicsTools.PatAlgos.patTemplate_cfg import *

process = cms.Process("TagProbe")

###
# User configurable parameters
###
MCFLAG = False 				# MC not yet implemented

GLOBALTAG = "FT_R_53_V6::All" 		# 2012AB re-reco + prompt tag

MUONCOLLECTION = "cleanPatMuons"
MUONCUT = "pt>20 && 1.2<eta<1.8" 	# ME42 current eta position

TAGMUONCUT = MUONCUT + " && isGlobalMuon"
PROBEMUONCUT = MUONCUT + " && isTrackerMuon"
PASSPROBEMUONCUT = ""

PASSPROBEPSET = cms.PSet(
	isGlobalMuon = cms.string("isGlobalMuon"),
)

ZMASSCUT = "60.0 < mass < 120.0"	# currently only Z T&P
JPSIMASSCUT = "2.5 < mass < 3.8"

OUTPUTFILENAME = "ME42TagAndProbeTree.root"

###
# includes
###
process = cms.Process("TagProbe")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.GlobalTag.globaltag = GLOBALTAG
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1

###
# datasets
###
process.source = cms.Source("PoolSource",
	fileNames = cms.untracked.vstring(
		'file:patTuple_muon.root',
	)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
process.source.inputCommands = cms.untracked.vstring("keep *")

###
# tag and probe selections
###
process.tagMuons = cms.EDFilter("MuonRefSelector",
	src = cms.InputTag(MUONCOLLECTION),
	cut = cms.string(TAGMUONCUT),
)

process.probeMuons = cms.EDFilter("MuonRefSelector",
	src = cms.InputTag(MUONCOLLECTION),
	cut = cms.string(PROBEMUONCUT),
)

process.passProbeMuons = cms.EDFilter("MuonRefSelector",
	src = cms.InputTag(MUONCOLLECTION),
	cut = cms.string(PASSPROBEMUONCUT),
)

process.ZTagProbe = cms.EDProducer("CandViewShallowCloneCombiner",
	decay = cms.string("tagMuons@+ probeMuons@-"),
	cut = cms.string(ZMASSCUT),
)

###
# produce tag and probe trees
###
process.tagAndProbeTree = cms.EDAnalyzer("TagProbeFitTreeProducer",
	tagProbePairs = cms.InputTag("ZTagProbe"),
	arbitration = cms.string("OneProbe"),
	variables = cms.PSet(
		pt = cms.string("pt"),
		eta = cms.string("eta"),
		phi = cms.string("phi"),
	),
	flags = PASSPROBEPSET,
	addRunLumiInfo = cms.bool(True),
	isMC = cms.bool(MCFLAG),
)

###
# path
###
process.TagAndProbe = cms.Path(
	(process.tagMuons + process.probeMuons) *
	process.passProbeMuons *
	process.ZTagProbe *
	process.tagAndProbeTree
	)

###
# output
###
process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string(OUTPUTFILENAME)
)

process.options.SkipEvent = cms.untracked.vstring('ProductNotFound')
