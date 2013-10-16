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
# Includes
###
process = cms.Process("TagProbe")

process.load("Configuration.StandardSequences.Services_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")

process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAny_cfi")
process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAlong_cfi")
process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorOpposite_cfi")
process.load("RecoMuon.DetLayers.muonDetLayerGeometry_cfi")

###
# options
###
process.GlobalTag.globaltag = "FT_R_53_V18::All" 

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
#    SkipEvent = cms.untracked.vstring('ProductNotFound')
)
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        options.inputFiles
    )
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.TFileService = cms.Service("TFileService",
    fileName = cms.string(options.outputFile),
)


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
    debugOn = cms.untracked.bool(False),
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
# Tag and probe selections
###
from RecoMuon.MuonIdentification.calomuons_cfi import calomuons;
process.mergedMuons = cms.EDProducer("CaloMuonMerger",
    mergeTracks = cms.bool(True),
    mergeCaloMuons = cms.bool(False), # AOD
    muons     = cms.InputTag("muons"), 
    caloMuons = cms.InputTag("calomuons"),
    tracks    = cms.InputTag("generalTracks"),
    minCaloCompatibility = calomuons.minCaloCompatibility,
    ## Apply some minimal pt cut
    muonsCut     = cms.string("pt > 3 && track.isNonnull"),
    caloMuonsCut = cms.string("pt > 3"),
    tracksCut    = cms.string("pt > 3"),
)

process.load("MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff")
## with some customization
process.muonMatchHLTL2.maxDeltaR = 0.3 # Zoltan tuning - it was 0.5
process.muonMatchHLTL3.maxDeltaR = 0.1
from MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff import *
changeRecoMuonInput(process, "mergedMuons")
#useExtendedL1Match(process)
#addHLTL1Passthrough(process)

from CSCDetectorStudies.TagAndProbe.variables_cfi import *

process.tagMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTrigger"),
    cut = cms.string("pt > 20 && abs(eta)<2.4 && " + MuonIDVariables.isTightMuon.value()+\
        " && !triggerObjectMatchesByCollection('hltL3MuonCandidates').empty()"),
)

process.oneTag  = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("tagMuons"),
    minNumber = cms.uint32(1)
)

process.probeMuons = cms.EDFilter("PATMuonSelector", # select tracker tracks
    src = cms.InputTag("patMuonsWithTrigger"),
    cut = cms.string("innerTrack.isNonnull && abs(eta)>1.0 && abs(eta)<2.4 && bestTrack.hitPattern.trackerLayersWithMeasurement>5"),
)

process.ZTagProbe = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("tagMuons@+ probeMuons@-"),
    cut = cms.string('60 < mass < 120 && abs(daughter(0).vz - daughter(1).vz)<0.2' + \
        ' && abs((daughter(0).vx^2 + daughter(0).vy^2)^0.5 - (daughter(1).vx^2 + daughter(1).vy^2)^0.5)<0.5'),
)

###
# custom variables
###

process.ME42MuonCands = cms.EDProducer("MuonME42CandidateProducer",
    src = cms.InputTag("probeMuons"),
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

###
# produce tag and probe trees
###
process.tagAndProbeTree = cms.EDAnalyzer("TagProbeFitTreeProducer",
    tagProbePairs = cms.InputTag("ZTagProbe"),
    arbitration = cms.string("OneProbe"),
    variables = cms.PSet(
        KinematicVariables,
        TriggerVariables,
        # external variable
        isME42 = cms.InputTag("ME42MuonCands","isME42"),
    ),
    flags = cms.PSet(
        MuonIDVariables,
        isME42Region = cms.InputTag("ME42MuonCands"), 
    ),
    addRunLumiInfo = cms.bool(True),
    isMC = cms.bool(False),
)

process.tnpTrkSequence = cms.Sequence(
    process.tagMuons
    * process.oneTag
    * process.probeMuons
    * process.ZTagProbe
    * process.ME42MuonCands
    * process.tagAndProbeTree
)

###
# standalone/tracker tnp
###
process.probeMuonsSta = cms.EDFilter("PATMuonSelector", # select standalone tracks
    src = cms.InputTag("patMuonsWithTrigger"),
    cut = cms.string("outerTrack.isNonnull && abs(eta)>1.0 && abs(eta)<2.4"),
)

process.ZTagProbeSta = process.ZTagProbe.clone(decay = "tagMuons@+ probeMuonsSta@-", cut = '60 < mass < 120')

process.ME42MuonCandsSta = cms.EDProducer("MuonME42CandidateProducer",
    src = cms.InputTag("probeMuonsSta"),
    MuonPropagator = cms.PSet(
        useSimpleGeometry = cms.bool(True),
        useStation2 = cms.bool(True),
        useStation4 = cms.bool(True),
        fallbackToME1 = cms.bool(False),
        fallback = cms.bool(False),
        useTrack = cms.string("muon"),
        useState = cms.string("outermost"),
        cosmicPropagationHypothesis = cms.bool(False),
    ),
)

process.tagAndProbeTreeSta = cms.EDAnalyzer("TagProbeFitTreeProducer",
    tagProbePairs = cms.InputTag("ZTagProbeSta"),
    arbitration = cms.string("OneProbe"),
    variables = cms.PSet(
        KinematicVariables,
        TriggerVariables,
        standAloneVariables,
        # external variable
        isME42 = cms.InputTag("ME42MuonCandsSta","isME42"),
    ),
    flags = cms.PSet(
        MuonIDVariables,
        isME42Region = cms.InputTag("ME42MuonCandsSta"),
    ),
    addRunLumiInfo = cms.bool(True),
    isMC = cms.bool(False),
)

process.tnpStaSequence = cms.Sequence(
    process.probeMuonsSta
    * process.ZTagProbeSta
    * process.ME42MuonCandsSta
    * process.tagAndProbeTreeSta
)


#process.pCutTracks = cms.EDFilter("TrackSelector", 
#    src = cms.InputTag("generalTracks"),      
#    cut = cms.string("pt > 3"),
#)
#
#process.trkTracks = cms.EDProducer("ConcreteChargedCandidateProducer", 
#    src = cms.InputTag("pCutTracks"),
#    particleType = cms.string("mu+"),
#)
#
#process.staTracks = cms.EDProducer("ConcreteChargedCandidateProducer",
#    src = cms.InputTag("standAloneMuons"),
#    particleType = cms.string("mu+"),
#)
#
#process.trkCands = cms.EDFilter("RecoChargedCandidateRefSelector",
#    src = cms.InputTag("trkTracks"),
#    cut = cms.string("pt>20 && abs(eta)<2.4"),
#)
#
#process.staCands = cms.EDFilter("RecoChargedCandidateRefSelector",
#    src = cms.InputTag("staTracks"),
#    cut = cms.string("pt>20 && abs(eta)<2.4"),
#)
#
#process.staTrkMatch = cms.EDProducer("TrivialDeltaRViewMatcher",
#    src = cms.InputTag("staTracks"),
#    matched = cms.InputTag("trkTracks"),
#    distMin = cms.double(0.3),
#)
#
#process.trkStaMatch = process.staTrkMatch.clone( src = "trkTracks", matched = "staTracks")
#
#process.staPassingTrk = cms.EDProducer("RecoChargedCandidateMatchedProbeMaker",
#    Matched = cms.untracked.bool(True),
#    ReferenceSource = cms.untracked.InputTag("trkCands"),
#    ResMatchMapSource = cms.untracked.InputTag("staTrkMatch"),
#    CandidateSource = cms.untracked.InputTag("staCands"),
#)
#
#process.trkPassingSta = process.staPassingTrk.clone( ReferenceSource = "staCands", ResMatchMapSource = "trkStaMatch", CandidateSource = "trkCands")
#
#process.tpPairsSta = process.ZTagProbe.clone(decay = "tagMuons@+ staCands@-", cut = '60 < mass < 120')
#process.tpPairsTrk = process.ZTagProbe.clone(decay = "tagMuons@+ trkCands@-", cut = '60 < mass < 120')
#
#process.ME42MuonCandsSta = cms.EDProducer("MuonME42CandidateProducer",
#    src = cms.InputTag("staTracks"),
#    MuonPropagator = cms.PSet(
#       useSimpleGeometry = cms.bool(True),
#       useStation2 = cms.bool(True),
#       useStation4 = cms.bool(True),
#       fallbackToME1 = cms.bool(False),
#       fallback = cms.bool(False),
#       useTrack = cms.string("tracker"),
#       useState = cms.string("outermost"),
#       cosmicPropagationHypothesis = cms.bool(False),
#    ),
#)
#
#process.ME42MuonCandsTrk = process.ME42MuonCandsSta.clone(src = "trkTracks")
#
#
#process.tagAndProbeTreeSta = process.tagAndProbeTree.clone(
#    tagProbePairs = "tpPairsSta",
#    variables = cms.PSet(
#        KinematicVariables, 
#        #standAloneVariables,
#        # external variable
#        isME42 = cms.InputTag("ME42MuonCandsSta","isME42"),
#    ),
#    flags = cms.PSet(
#    #    MuonIDVariables,
#    #    hasTrack = cms.string("track.isNonnull"),
#        staPassingTrk = cms.InputTag("staPassingTrk"),
#        isME42Region = cms.InputTag("ME42MuonCandsSta"),
#    ),
#)
#
#process.tagAndProbeTreeTrk = process.tagAndProbeTree.clone(
#    tagProbePairs = "tpPairsTrk",
#    variables = cms.PSet(
#        KinematicVariables,
#        #standAloneVariables,
#        # external variable
#        isME42 = cms.InputTag("ME42MuonCandsTrk","isME42"),
#    ),
#    flags = cms.PSet(
#    #    MuonIDVariables,
#    #    hasTrack = cms.string("track.isNonnull"),
#        trkPassingSta = cms.InputTag("trkPassingSta"),
#        isME42Region = cms.InputTag("ME42MuonCandsTrk"),
#    ),
#)

#process.tnpStaSequence = cms.Sequence(
#    #process.probeMuonsSta
#    process.pCutTracks
#    * process.trkTracks
#    * process.staTracks
#    * process.trkCands
#    * process.staCands
#    * process.staTrkMatch
#    * process.staPassingTrk
#    * process.tpPairsSta
#    * process.ME42MuonCandsSta
#    * process.tagAndProbeTreeSta
#
#    * process.trkStaMatch
#    * process.trkPassingSta
#    * process.tpPairsTrk
#    * process.ME42MuonCandsTrk
#    * process.tagAndProbeTreeTrk
#)

###
# path
###

process.TagAndProbe = cms.Path(
    process.fastFilter
    * process.mergedMuons
    * process.patMuonsWithTriggerSequence
    * process.tnpTrkSequence
    * process.tnpStaSequence
)
