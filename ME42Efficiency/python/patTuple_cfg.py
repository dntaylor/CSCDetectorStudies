## import skeleton process
from PhysicsTools.PatAlgos.patTemplate_cfg import *

###
# Defaults
###
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')

options.inputFiles = "file:SingleMu_Run2012A_RECO.root"
options.outputFile = "SingleMu_Run2012A_PATTuple.root"
options.parseArguments()


## ------------------------------------------------------
#  NOTE: you can use a bunch of core tools of PAT to
#  taylor your PAT configuration; for a few examples
#  uncomment the lines below
## ------------------------------------------------------
from PhysicsTools.PatAlgos.tools.coreTools import *

## remove MC matching from the default sequence
removeMCMatching(process, ['All'])
#runOnData(process)

## remove certain objects from the default sequence
#removeAllPATObjectsBut(process, ['Muons'])
#removeSpecificPATObjects(process, ['Photons', 'Electrons', 'Muons', 'Taus', 'Jets', 'METs'])

# filter tracks to 1.0-2.0
# TODO: get track extras as well
process.filteredTracks = cms.EDFilter("TrackSelector",
    src = cms.InputTag("generalTracks"),
    cut = cms.string("eta>1.0 && eta<2.0 && pt>3.0")
)

process.RECOFilterSequence = cms.Sequence( process.filteredTracks )

## let it run
process.p = cms.Path(
    process.RECOFilterSequence
    * process.patDefaultSequence
    )

## ------------------------------------------------------
#  In addition you usually want to change the following
#  parameters:
## ------------------------------------------------------
process.GlobalTag.globaltag = cms.string("FT_R_53_V18::All")
process.source.fileNames = cms.untracked.vstring( options.inputFiles )
process.maxEvents.input = -1
process.out.outputCommands = [ 'drop *',
#    'keep *_generalTracks*_*_*',
    'keep *_filteredTracks_*_*',
    'keep *_offlinePrimaryVertices*_*_*',
    'keep *_offlineBeamSpot_*_*',
    'keep recoMuons_muons_*_*',
    'keep recoTracks_globalMuons_*_*',
    'keep *_standAloneMuons_*_*',
#    'keep *_refittedStandAloneMuons_*_*',
#    'keep *_ancientMuonSeed_*_*',
    'keep *_cscSegments_*_*',
    'keep *_csc2DRecHits_*_*',
#    'keep *_*_*_HLT',
#    'keep *_cleanPatMuons*_*_*',
]  ##  (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
process.out.fileName = options.outputFile
process.MessageLogger.cerr.FwkReport.reportEvery = 100
