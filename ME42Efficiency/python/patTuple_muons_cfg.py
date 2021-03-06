import FWCore.ParameterSet.Config as cms

###
# Defaults
###
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')

options.inputFiles = "file:SingleMu_Run2012C_RECO.root"
options.outputFile = "SingleMu_Run2012C_Skim.root"
options.parseArguments()

###
# Includes
###
process = cms.Process("SingleMuSkim")

process.load("Configuration.StandardSequences.Services_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')

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

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )


from PhysicsTools.PatAlgos.patTemplate_cfg import *
from PhysicsTools.PatAlgos.tools.coreTools import *
removeMCMatching(process, ['All'])
#removeAllPATObjectsBut(process, ['Muons'])

from RecoMuon.MuonIdentification.calomuons_cfi import calomuons;
process.mergedMuons = cms.EDProducer("CaloMuonMerger",
    mergeTracks = cms.bool(True),
    mergeCaloMuons = cms.bool(False), # AOD
    muons     = cms.InputTag("muons"),
    caloMuons = cms.InputTag("calomuons"),
    tracks    = cms.InputTag("generalTracks"),
    minCaloCompatibility = calomuons.minCaloCompatibility,
    ## Apply some minimal pt cut
    muonsCut     = cms.string("pt > 2 && track.isNonnull"),
    caloMuonsCut = cms.string("pt > 2"),
    tracksCut    = cms.string("pt > 2"),
)

process.load("MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff")
## with some customization
process.muonMatchHLTL2.maxDeltaR = 0.3 # Zoltan tuning - it was 0.5
process.muonMatchHLTL3.maxDeltaR = 0.1
from MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff import *
changeRecoMuonInput(process, "mergedMuons")
#useExtendedL1Match(process)
#addHLTL1Passthrough(process)


process.out.outputCommands = cms.untracked.vstring(
	'keep *',
)

process.p = cms.Path(
	process.patDefaultSequence *
	process.mergedMuons
)

