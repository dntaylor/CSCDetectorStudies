import FWCore.ParameterSet.Config as cms

###
# Defaults
###
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')

options.inputFiles = "file:SingleMu_Run2012A_RECO.root"
options.outputFile = "SingleMu_Run2012A_PATTuple.root"
options.parseArguments()

###
# PAT Sequence
###
from PhysicsTools.PatAlgos.patTemplate_cfg import *

# add trigger information (trigTools)
from PhysicsTools.PatAlgos.tools.trigTools import *

switchOnTrigger(process,sequence='patDefaultSequence',hltProcess = '*')

isMC = False

# load the coreTools of PAT
from PhysicsTools.PatAlgos.tools.coreTools import *
removeMCMatching(process, ['All'])

process.load('Configuration.StandardSequences.Reconstruction_cff') # to define ak5PFJets
process.load('Configuration.StandardSequences.Services_cff')
process.load("RecoLuminosity.LumiProducer.lumiProducer_cff") 
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')


### muonTriggerMatchHLT ################################################################

process.muonTriggerMatchHLT = cms.EDProducer( 'PATTriggerMatcherDRDPtLessByR',
    src     = cms.InputTag( 'patMuons' ),
    matched = cms.InputTag( 'patTrigger' ),
    andOr          = cms.bool( False ),
    filterIdsEnum  = cms.vstring( '*' ),
    filterIds      = cms.vint32( 0 ),
    filterLabels   = cms.vstring( '*' ),
    pathNames      = cms.vstring( '*' ),
    matchedCuts = cms.string('coll("hltL3MuonCandidates")'),
    maxDPtRel = cms.double( 0.5 ),
    maxDeltaR = cms.double( 0.1 ),
    resolveAmbiguities    = cms.bool( True ),
    resolveByMatchQuality = cms.bool( False )
)

### patMuonsWithTrigger ############################################################
process.patMuonsWithTrigger = cms.EDProducer( 'PATTriggerMatchMuonEmbedder',
    src     = cms.InputTag(  'patMuons' ),
    matches = cms.VInputTag('muonTriggerMatchHLT')
)

process.patMuons.embedPFCandidate = False
process.patMuons.embedTrack = True

process.preMuonSequence = cms.Sequence(
    process.patTrigger
)

process.patDefaultSequence.replace(
    process.patMuons,
    process.patMuons *process.muonTriggerMatchHLT *process.patMuonsWithTrigger
)

process.prePATSequence= cms.Sequence(
    process.preMuonSequence
)

process.skim = cms.EDAnalyzer("L1CSCTFMethods",
    muons = cms.InputTag("patMuonsWithTrigger"),
)

## let it run
process.p = cms.Path(
    process.prePATSequence
    * process.patDefaultSequence
    * process.skim
)

## ------------------------------------------------------
#  In addition you usually want to change the following
#  parameters:
## ------------------------------------------------------
process.GlobalTag.globaltag = cms.string("FT_R_53_V18::All")
process.source.fileNames = cms.untracked.vstring( options.inputFiles )
process.maxEvents.input = 100
process.out.outputCommands = [ 'drop *',

        # pat candidate -------------
        'keep *_patMuons_*_*',
        'keep *_patMuonsWithTrigger_*_*',
        
        # Trigger ---------------------
        'keep *_patTrigger*_*_*',
        'keep *_TriggerResults_*_*',
        'keep *_vertexMapProd_*_*',
 ]
process.out.fileName = options.outputFile
process.MessageLogger.cerr.FwkReport.reportEvery = 100
