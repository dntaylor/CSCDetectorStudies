import FWCore.ParameterSet.Config as cms

# make L1 ntuples from RAW+RECO

process = cms.Process("L1NTUPLE")

# import of standard configurations
process.load('Configuration/StandardSequences/Services_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('Configuration/StandardSequences/MagneticField_38T_cff')
process.load('Configuration/StandardSequences/SimL1Emulator_cff')
process.load("Configuration.StandardSequences.RawToDigi_Data_cff")
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration/StandardSequences/EndOfProcess_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
process.load('Configuration/EventContent/EventContent_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')


process.mergedSuperClusters = cms.EDFilter("EgammaSuperClusterMerger",
#src = cms.VInputTag(cms.InputTag("correctedHybridSuperClusters"),cms.InputTag("correctedMulti5x5SuperClustersWithPreshower"))
src = cms.VInputTag(cms.InputTag("hybridSuperClusters"),cms.InputTag("multi5x5SuperClustersWithPreshower"))
)



# global tag
process.GlobalTag.globaltag = 'GR_R_53_V21::All'

# output file
process.TFileService = cms.Service("TFileService",
    fileName = cms.string('L1Tree_SingleMu_Run2012A_RAW.root')
)

# analysis
process.load("L1Trigger.Configuration.L1Extra_cff")
process.load("UserCode.L1TriggerDPG.l1NtupleProducer_cfi")
process.load("UserCode.L1TriggerDPG.l1RecoTreeProducer_cfi")
process.load("UserCode.L1TriggerDPG.l1ExtraTreeProducer_cfi")
process.load("UserCode.L1TriggerDPG.l1MenuTreeProducer_cfi")
process.load("UserCode.L1TriggerDPG.l1MuonRecoTreeProducer_cfi")
process.load("JetMETCorrections.Configuration.JetCorrectionServices_cff")

process.p = cms.Path(
    process.gtDigis
    +process.gtEvmDigis
    +process.gctDigis
    +process.dttfDigis
    +process.csctfDigis
    +process.l1NtupleProducer
#    +process.l1extraParticles
#    +process.l1ExtraTreeProducer
#    +process.l1MenuTreeProducer
#    +process.l1RecoTreeProducer
#    +process.l1MuonRecoTreeProducer
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
process.source = cms.Source ("PoolSource",
                             fileNames = readFiles,
                             secondaryFileNames = secFiles
                             )

readFiles.extend( [
#    'file:SingleMu_Run2012A_RAW.root',
] )

secFiles.extend( [
] )
