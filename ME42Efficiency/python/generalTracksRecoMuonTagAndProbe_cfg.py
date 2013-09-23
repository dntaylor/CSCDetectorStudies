import FWCore.ParameterSet.Config as cms

###
# Defaults
###
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')

options.inputFiles = "file:SingleMu_Run2012A_RECO.root"
options.outputFile = "ME42TagAndProbeTree.root"
options.parseArguments()

###
# User configurable parameters
###
MCFLAG = False 				# MC not yet implemented

GLOBALTAG = "FT_R_53_V6::All" 		# 2012AB re-reco + prompt tag

MUONCUT = "pt>20 && abs(eta)<2.4"

TAGCUT = MUONCUT + \
	" && isGlobalMuon && isPFMuon" + \
	" && globalTrack().normalizedChi2<10.0" + \
	" && globalTrack().hitPattern().numberOfValidMuonHits > 0" + \
	" && globalTrack().hitPattern().numberOfValidPixelHits>0" + \
	" && numberOfMatchedStations>1" + \
	" && globalTrack().hitPattern().trackerLayersWithMeasurement>5" #+ \
#	" && abs(muonBestTrack().dxy(vertex.position()))<0.2" #+ \
#	" && abs(muonBestTrack().dz(vertex.position()))<0.5"
PROBECUT = MUONCUT + \
	" && bestTrack().hitPattern().trackerLayersWithMeasurement>5" #+ \
#	" && dxy(pv)<=0.2 && dz(pv)<=0.5"

ZMASSCUT = "60.0 < mass < 120.0"


###
# includes
###
process = cms.Process("TagProbe")
process.load("Configuration.StandardSequences.Services_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.GlobalTag.globaltag = GLOBALTAG
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")
process.load("Configuration.StandardSequences.MagneticField_cff")

###
# options
###
process.options = cms.untracked.PSet( 
	wantSummary = cms.untracked.bool(True),
#	SkipEvent = cms.untracked.vstring('ProductNotFound')
)
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.suppressWarning = cms.untracked.vstring('ME42MuonCands')

###
# datasets
###
process.source = cms.Source("PoolSource",
	fileNames = cms.untracked.vstring(
		options.inputFiles
	)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

###
# only process good lumis
###
#import FWCore.PythonUtilities.LumiList as LumiList
#process.source.lumisToProcess = LumiList.LumiList(filename = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Reprocessing/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt').getVLuminosityBlockRange()

###
# tag and probe selections
###
process.tags = cms.EDFilter("MuonRefSelector",
	src = cms.InputTag('muons'),
	cut = cms.string(TAGCUT),
)

# convert tracks to charged candidates assuming muon
from  SimGeneral.HepPDTESSource.pythiapdt_cfi import *

# tracks into candidates
process.allTracks = cms.EDProducer("ConcreteChargedCandidateProducer",
	src = cms.InputTag("generalTracks"),
	particleType = cms.string("mu-"),
)

process.staTracks = cms.EDProducer("ConcreteChargedCandidateProducer",
	src = cms.InputTag("standAloneMuons"),
	particleType = cms.string("mu-"),
)

# select track candidates
process.trkCands = cms.EDFilter("RecoChargedCandidateRefSelector",
	src = cms.InputTag("allTracks"),
	cut = cms.string(PROBECUT),
)

process.staCands = cms.EDFilter("RecoChargedCandidateRefSelector",
	src = cms.InputTag("staTracks"),
	cut = cms.string(PROBECUT),
)

# make z tag probe map
process.ZTagProbe = cms.EDProducer("CandViewShallowCloneCombiner",
	decay = cms.string("tags@+ trkCands@-"),
	cut = cms.string(ZMASSCUT),
)

# match tracks and standalone tracks
process.trkStaMatch = cms.EDProducer("TrivialDeltaRViewMatcher",
	src = cms.InputTag("allTracks"), 
	matched = cms.InputTag("staTracks"),
	distMin = cms.double(0.1),
)

# get candidates from matching
process.trkPassingSta = cms.EDProducer("RecoChargedCandidateMatchedProbeMaker",
	Matched = cms.untracked.bool(True),
	ReferenceSource = cms.untracked.InputTag("staCands"),
	ResMatchMapSource = cms.untracked.InputTag("trkStaMatch"),
	CandidateSource = cms.untracked.InputTag("trkCands"),
)

###
# custom variables
###

process.ME42MuonCands = cms.EDProducer("MuonME42CandidateProducer",
	TrackCollection = cms.InputTag("allTracks"),
	VertexCollection = cms.InputTag("offlinePrimaryVertices"),
	BeamSpot = cms.InputTag("offlineBeamSpot"),
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
		# external variable
#		isME42 = cms.InputTag("ME42MuonCands","isME42"),
	),
	flags = cms.PSet(
		trkPassingSta = cms.InputTag("trkPassingSta"),
#		passingTightMuon = cms.InputTag("ME42MuonCands","isTightMuon"),
#		passingLooseMuon = cms.InputTag("ME42MuonCands","isLooseMuon"),
	),
	addRunLumiInfo = cms.bool(True),
	isMC = cms.bool(MCFLAG),
)

###
# path
###
process.TagAndProbe = cms.Path(
	process.tags
	* process.allTracks
	* process.staTracks
	* process.trkCands
	* process.staCands
	* process.ZTagProbe
	* process.trkStaMatch
	* process.trkPassingSta
#	* process.ME42MuonCands
	* process.tagAndProbeTree
)

###
# output
###
process.TFileService = cms.Service("TFileService",
	fileName = cms.string(options.outputFile),
)

