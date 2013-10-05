import FWCore.ParameterSet.Config as cms

###
# Defaults
###
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')

options.inputFiles = "file:SingleMu_Run2012C_RECO.root"
options.outputFile = "ME42TagAndProbeTree.root"
options.parseArguments()

###
# User configurable parameters
###
MCFLAG = False 				# MC not yet implemented

GLOBALTAG = "FT_R_53_V18::All" 		# 2012ABC re-reco

MUONCUT = "pt>20 && abs(eta)<2.4"

TAGCUT = MUONCUT + \
	" && isGlobalMuon && isPFMuon" + \
	" && globalTrack().normalizedChi2<10.0" + \
	" && globalTrack().hitPattern().numberOfValidMuonHits > 0" + \
	" && globalTrack().hitPattern().numberOfValidPixelHits>0" + \
	" && numberOfMatchedStations>1" + \
	" && globalTrack().hitPattern().trackerLayersWithMeasurement>5" #+ \
#	" && muonBestTrack.dxy(vertex().position())<0.2" + \
#	" && muonBestTrack.dz(vertex().position())<0.5"
PROBECUT = MUONCUT + \
	" && bestTrack().hitPattern().trackerLayersWithMeasurement>5" #+ \
#	" && dxy(pv)<=0.2 && dz(pv)<=0.5"
ETACUT = " && track.outerEta>1.25 && track.outerEta<1.75"
PHICUT = " && track.outerPhi>76.*3.14159/180. && track.outerPhi<124.*3.14159/180."
NOPHICUT = " && (track.outerPhi<74.*3.14159/180. || track.outerPhi>126.*3.14159/180.)"
TIGHTMUON = "isGlobalMuon && isPFMuon" + \
	" && globalTrack().normalizedChi2<10.0" + \
	" && globalTrack().hitPattern().numberOfValidMuonHits > 0" + \
	" && globalTrack().hitPattern().numberOfValidPixelHits>0" + \
	" && numberOfMatchedStations>1" + \
	" && globalTrack().hitPattern().trackerLayersWithMeasurement>5" #+ \
LOOSEMUON = "isPFMuon && (isGlobalMuon || isTrackerMuon)"

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

process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAny_cfi")
process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAlong_cfi")
process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorOpposite_cfi")
process.load("RecoMuon.DetLayers.muonDetLayerGeometry_cfi")

###
# options
###
process.options = cms.untracked.PSet( 
	wantSummary = cms.untracked.bool(True),
#	SkipEvent = cms.untracked.vstring('ProductNotFound')
)
process.MessageLogger.cerr.FwkReport.reportEvery = 100
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
#process.source.lumisToProcess = LumiList.LumiList(filename = './Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt').getVLuminosityBlockRange()

###
# vertex and trigger filters
###
process.goodVertexFilter = cms.EDFilter("VertexSelector",
	src = cms.InputTag("offlinePrimaryVertices"),
	cut = cms.string("!isFake && ndof > 4 && abs(z) <= 25 && position.Rho <= 2"),
	filter = cms.bool(True),
)
process.noScraping = cms.EDFilter("FilterOutScraping",
	applyfilter = cms.untracked.bool(True),
	debugOn = cms.untracked.bool(False), ## Or 'True' to get some per-event info
	numtrack = cms.untracked.uint32(10),
	thresh = cms.untracked.double(0.25)
)

process.load("HLTrigger.HLTfilters.triggerResultsFilter_cfi")
process.triggerResultsFilter.triggerConditions = cms.vstring( 'HLT_IsoMu24_v*', 'HLT_IsoMu24_eta2p1_v*', 'HLT_Mu40_v*', 'HLT_Mu40_eta2p1_v*' )

process.triggerResultsFilter.l1tResults = ''
process.triggerResultsFilter.throw = False
process.triggerResultsFilter.hltResults = cms.InputTag( "TriggerResults", "", "HLT" )

process.triggerResultsFilterFake = process.triggerResultsFilter.clone(
	triggerConditions = cms.vstring( 'HLT_Mu40_v*', 'HLT_Mu5_v*', 'HLT_Mu12_v*', 'HLT_Mu24_v*')
)

process.fastFilter     = cms.Sequence(process.goodVertexFilter + process.noScraping + process.triggerResultsFilter)
process.fastFilterFake = cms.Sequence(process.goodVertexFilter + process.noScraping + process.triggerResultsFilterFake)

###
# tag and probe selections
###
process.tags = cms.EDFilter("MuonRefSelector",
	src = cms.InputTag('muons'),
	cut = cms.string(TAGCUT),
	filter = cms.bool(True),
)

# convert tracks to charged candidates assuming muon
from  SimGeneral.HepPDTESSource.pythiapdt_cfi import *

# tracks into candidates
process.allTracks = cms.EDProducer("ConcreteChargedCandidateProducer",
	src = cms.InputTag("generalTracks"),
	particleType = cms.string("mu-"),
)

process.staTracks = cms.EDProducer("ConcreteChargedCandidateProducer",
	src = cms.InputTag("standAloneMuons","UpdatedAtVtx"),
	particleType = cms.string("mu-"),
)

# select track candidates
process.trkCands = cms.EDFilter("RecoChargedCandidateRefSelector",
	src = cms.InputTag("allTracks"),
	cut = cms.string(PROBECUT),
)

process.staCands = cms.EDFilter("RecoChargedCandidateRefSelector",
	src = cms.InputTag("staTracks"),
	cut = cms.string(MUONCUT),
)

###
# custom variables
###

process.ME42MuonCands = cms.EDProducer("MuonME42CandidateProducer",
	TrackCollection = cms.InputTag("allTracks"),
	VertexCollection = cms.InputTag("offlinePrimaryVertices"),
	BeamSpot = cms.InputTag("offlineBeamSpot"),
	MuonPropagator = cms.PSet(
		useSimpleGeometry = cms.bool(True),
		useStation2 = cms.bool(True),
		useStation4 = cms.bool(True),
		fallbackToME1 = cms.bool(False),
		fallback = cms.bool(False),
		useTrack = cms.string("tracker"),
		useState = cms.string("outermost"),
		cosmicPropagationHypothesis = cms.bool(False),
	),
)

# match tracks and standalone tracks
process.trkStaMatch = cms.EDProducer("TrivialDeltaRViewMatcher",
	src = cms.InputTag("allTracks"), 
	matched = cms.InputTag("staTracks"),
	distMin = cms.double(0.3),
)

# get candidates from matching
process.trkPassingSta = cms.EDProducer("RecoChargedCandidateMatchedProbeMaker",
	Matched = cms.untracked.bool(True),
	ReferenceSource = cms.untracked.InputTag("staCands"),
	ResMatchMapSource = cms.untracked.InputTag("trkStaMatch"),
	CandidateSource = cms.untracked.InputTag("trkCands"),
)

# make z tag probe map
process.ZTagProbe = cms.EDProducer("CandViewShallowCloneCombiner",
	decay = cms.string("tags@+ trkCands@-"),
	cut = cms.string(ZMASSCUT + ' && abs(daughter(0).vz - daughter(1).vz)<0.2' + \
	' && abs((daughter(0).vx^2 + daughter(0).vy^2)^0.5 - (daughter(1).vx^2 + daughter(1).vy^2)^0.5)<0.5'),
)

# with eta cut (temporary)
process.trkCandsEta = process.trkCands.clone(cut = cms.string(PROBECUT+ETACUT))
process.ZTagProbeEta = process.ZTagProbe.clone(decay = cms.string("tags@+ trkCandsEta@-"))

# with ME42 cut (temporary)
process.trkCandsME42 = process.trkCands.clone(cut = cms.string(PROBECUT+ETACUT+PHICUT))
process.ZTagProbeME42 = process.ZTagProbe.clone(decay = cms.string("tags@+ trkCandsME42@-"))

# eta without ME42 cut (temporary)
process.trkCandsEtaNoME42 = process.trkCands.clone(cut = cms.string(PROBECUT+ETACUT+NOPHICUT))
process.ZTagProbeEtaNoME42 = process.ZTagProbe.clone(decay = cms.string("tags@+ trkCandsEtaNoME42@-"))

from CSCDetectorStudies.TagAndProbe.variables_cfi import *

###
# produce tag and probe trees
###
process.tagAndProbeTree = cms.EDAnalyzer("TagProbeFitTreeProducer",
	tagProbePairs = cms.InputTag("ZTagProbe"),
	arbitration = cms.string("OneProbe"),
	variables = cms.PSet(
		KinematicVariables,
		#MuonIDVariables,
		#pt = cms.string("pt"),
		#eta = cms.string("eta"),
		#phi = cms.string("phi"),
		# external variable
		isME42 = cms.InputTag("ME42MuonCands","isME42"),
	),
	flags = cms.PSet(
		#MuonIDVariables,
		trkPassingSta = cms.InputTag("trkPassingSta"),
#		passingTightMuon = cms.InputTag("ME42MuonCands","isTightMuon"),
#		passingLooseMuon = cms.InputTag("ME42MuonCands","isLooseMuon"),
	),
	addRunLumiInfo = cms.bool(True),
	isMC = cms.bool(MCFLAG),
)

process.tagAndProbeTreeEta = process.tagAndProbeTree.clone(tagProbePairs="ZTagProbeEta")
process.tagAndProbeTreeME42 = process.tagAndProbeTree.clone(tagProbePairs="ZTagProbeME42")
process.tagAndProbeTreeEtaNoME42 = process.tagAndProbeTree.clone(tagProbePairs="ZTagProbeEtaNoME42")

###
# muon id efficiency
###
process.staProbes = cms.EDFilter("MuonRefSelector",
        src = cms.InputTag('muons'),
        cut = cms.string(PROBECUT + " && isStandAloneMuon"),
)


###
# path
###
process.TagAndProbe = cms.Path(
#	process.fastFilter
	process.tags
	* process.allTracks
	* process.staTracks
	* process.trkCands
	* process.staCands
	* process.ZTagProbe
	* process.trkStaMatch
	* process.trkPassingSta
	* process.ME42MuonCands
	* process.tagAndProbeTree

	* process.trkCandsEta
	* process.ZTagProbeEta
	* process.tagAndProbeTreeEta

	* process.trkCandsME42
	* process.ZTagProbeME42
	* process.tagAndProbeTreeME42

	* process.trkCandsEtaNoME42
	* process.ZTagProbeEtaNoME42
	* process.tagAndProbeTreeEtaNoME42
)

###
# output
###
process.TFileService = cms.Service("TFileService",
	fileName = cms.string(options.outputFile),
)

