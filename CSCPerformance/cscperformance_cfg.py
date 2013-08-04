import FWCore.ParameterSet.Config as cms

process = cms.Process("CSCPerformance")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
        'file:SingleMu_Run2012A_RECO.root'
    )
)

process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

import FWCore.PythonUtilities.LumiList as LumiList
process.source.lumisToProcess = LumiList.LumiList(filename = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Reprocessing/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt').getVLuminosityBlockRange()

MUONCUT = "pt>20 && abs(eta)<2.4" + \
        " && isGlobalMuon && isPFMuon" + \
        " && globalTrack().normalizedChi2<10.0" + \
        " && globalTrack().hitPattern().numberOfValidMuonHits > 0" + \
        " && globalTrack().hitPattern().numberOfValidPixelHits>0" + \
        " && numberOfMatchedStations>1" + \
        " && globalTrack().hitPattern().trackerLayersWithMeasurement>5" #+ \

process.goodMuons = cms.EDFilter("MuonRefSelector",
        src = cms.InputTag('muons'),
        cut = cms.string(MUONCUT),
        filter = cms.bool(True),
)

process.cscPerformance = cms.EDAnalyzer('CSCPerformance',
    cscRecHitTag = cms.InputTag("csc2DRecHits"),
    cscSegmentTag = cms.InputTag("cscSegments"),
    saMuonTag = cms.InputTag("standAloneMuons"),
    allMuonsTag = cms.InputTag("muons"),
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('cscPerformance.root')
)


process.p = cms.Path(process.goodMuons * process.cscPerformance)
