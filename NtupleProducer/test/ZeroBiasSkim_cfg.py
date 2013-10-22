import FWCore.ParameterSet.Config as cms

###
# Defaults
###
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')

options.inputFiles = "file:ZeroBias_Run2012D_RAW.root"
options.outputFile = "L1CSCTFNTuple_RAW.root"
#options.secondaryInputFiles =  "file:ZeroBias_Run2012D_RECO.root"
options.register ('RAWRECO', "RAW", VarParsing.multiplicity.singleton, VarParsing.varType.string, "Select RAW or RECO source files")
options.parseArguments()


###
# L1Ntuple
###

from UserCode.L1TriggerDPG.l1Ntuple_cfg import *

if options.RAWRECO=="RAW":
    process.p.remove(process.l1RecoTreeProducer)
    process.p.remove(process.l1MuonRecoTreeProducer)
    process.p.remove(process.l1MenuTreeProducer)

    # remove non CSCTF stuff
    process.p.remove(process.l1extraParticles)
    process.p.remove(process.l1ExtraTreeProducer)
    process.p.remove(process.siPixelDigis)
    process.p.remove(process.siStripDigis)
    process.p.remove(process.ecalDigis)
    process.p.remove(process.ecalPreshowerDigis)
    process.p.remove(process.hcalDigis)
    process.p.remove(process.castorDigis)
    
    process.l1NtupleProducer.gtEvmSource          = cms.InputTag("none")
    process.l1NtupleProducer.gtSource             = cms.InputTag("none")
    process.l1NtupleProducer.gctCentralJetsSource = cms.InputTag("none")
    process.l1NtupleProducer.gctNonIsoEmSource    = cms.InputTag("none")
    process.l1NtupleProducer.gctForwardJetsSource = cms.InputTag("none")
    process.l1NtupleProducer.gctIsoEmSource       = cms.InputTag("none")
    process.l1NtupleProducer.gctEnergySumsSource  = cms.InputTag("none")
    process.l1NtupleProducer.gctTauJetsSource     = cms.InputTag("none")
    process.l1NtupleProducer.rctSource            = cms.InputTag("none")
    process.l1NtupleProducer.dttfSource           = cms.InputTag("none")
    process.l1NtupleProducer.ecalSource           = cms.InputTag("none")
    process.l1NtupleProducer.hcalSource           = cms.InputTag("none")

if options.RAWRECO=="RECO":
    process.p.remove(process.RawToDigi)
    process.p.remove(process.l1GtTriggerMenuLite)
    process.p.remove(process.l1MenuTreeProducer)
    
    #process.l1NtupleProducer.gmtSource            = cms.InputTag("none")
    process.l1NtupleProducer.gtEvmSource          = cms.InputTag("none")
    process.l1NtupleProducer.gtSource             = cms.InputTag("none")
    process.l1NtupleProducer.gctCentralJetsSource = cms.InputTag("none")
    process.l1NtupleProducer.gctNonIsoEmSource    = cms.InputTag("none")
    process.l1NtupleProducer.gctForwardJetsSource = cms.InputTag("none")
    process.l1NtupleProducer.gctIsoEmSource       = cms.InputTag("none")
    process.l1NtupleProducer.gctEnergySumsSource  = cms.InputTag("none")
    process.l1NtupleProducer.gctTauJetsSource     = cms.InputTag("none")
    process.l1NtupleProducer.rctSource            = cms.InputTag("none")
    process.l1NtupleProducer.dttfSource           = cms.InputTag("none")
    process.l1NtupleProducer.csctfTrkSource       = cms.InputTag("none")
    process.l1NtupleProducer.csctfLCTSource       = cms.InputTag("none")
    process.l1NtupleProducer.csctfStatusSource    = cms.InputTag("none")
    process.l1NtupleProducer.csctfDTStubsSource   = cms.InputTag("none")
    
    process.l1RecoTreeProducer.superClustersBarrelTag  = cms.untracked.InputTag("none")
    process.l1RecoTreeProducer.superClustersEndcapTag  = cms.untracked.InputTag("none")
    process.l1RecoTreeProducer.basicClustersBarrelTag  = cms.untracked.InputTag("none")
    process.l1RecoTreeProducer.basicClustersEndcapTag  = cms.untracked.InputTag("none")

if options.RAWRECO=="RAWRECO":
    process.p.remove(process.l1RecoTreeProducer)
    process.p.remove(process.l1GtTriggerMenuLite)
    process.p.remove(process.l1MenuTreeProducer)

    # remove non CSCTF stuff
    process.p.remove(process.l1extraParticles)
    process.p.remove(process.l1ExtraTreeProducer)
    process.p.remove(process.siPixelDigis)
    process.p.remove(process.siStripDigis)
    process.p.remove(process.ecalDigis)
    process.p.remove(process.ecalPreshowerDigis)
    process.p.remove(process.hcalDigis)
    process.p.remove(process.castorDigis)

    process.l1NtupleProducer.gtEvmSource          = cms.InputTag("none")
    process.l1NtupleProducer.gtSource             = cms.InputTag("none")
    process.l1NtupleProducer.gctCentralJetsSource = cms.InputTag("none")
    process.l1NtupleProducer.gctNonIsoEmSource    = cms.InputTag("none")
    process.l1NtupleProducer.gctForwardJetsSource = cms.InputTag("none")
    process.l1NtupleProducer.gctIsoEmSource       = cms.InputTag("none")
    process.l1NtupleProducer.gctEnergySumsSource  = cms.InputTag("none")
    process.l1NtupleProducer.gctTauJetsSource     = cms.InputTag("none")
    process.l1NtupleProducer.rctSource            = cms.InputTag("none")
    process.l1NtupleProducer.dttfSource           = cms.InputTag("none")
    process.l1NtupleProducer.ecalSource           = cms.InputTag("none")
    process.l1NtupleProducer.hcalSource           = cms.InputTag("none")

###
# options
###
process.GlobalTag.globaltag = "GR_P_V42::All"
#process.GlobalTag.globaltag = ''

SkipEvent = cms.untracked.vstring('ProductNotFound')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        options.inputFiles
    ),
    secondaryFileNames = cms.untracked.vstring(
#        options.secondaryInputFiles
    )
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string(options.outputFile),
)


