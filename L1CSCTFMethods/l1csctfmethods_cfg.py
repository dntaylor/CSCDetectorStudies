import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
        'file:L1Tree_Run2012C_SingleMuOpen_RAW-RECO.root'
    )
)

process.demo = cms.EDAnalyzer('L1CSCTFMethods'
)


process.p = cms.Path(process.demo)
