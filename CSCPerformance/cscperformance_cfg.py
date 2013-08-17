import FWCore.ParameterSet.Config as cms

process = cms.Process("CSCPerformance")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Geometry.MuonNumbering.muonNumberingInitialization_cfi")
process.load("Geometry.MuonCommonData.muonEndcapIdealGeometryXML_cfi")
process.load("Geometry.CSCGeometry.cscGeometry_cfi")
# import of standard configurations
process.load('Configuration/StandardSequences/Services_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
process.load('Configuration/StandardSequences/SimL1Emulator_cff')
process.load("Configuration.StandardSequences.RawToDigi_Data_cff")
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration/StandardSequences/EndOfProcess_cff')
process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('Configuration/StandardSequences/MagneticField_AutoFromDBCurrent_cff')
process.load("JetMETCorrections.Configuration.DefaultJEC_cff")
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
#        'file:SingleMu_Run2012A_RECO.root'
#        '/store/data/Run2012D/SingleMu/RECO/22Jan2013-v1/30007/061C121C-7C8B-E211-B022-00259073E4E2.root',
#        '/store/data/Run2012D/SingleMu/RECO/22Jan2013-v1/30007/065B7233-F484-E211-9225-20CF3027A5B5.root',
#        '/store/data/Run2012D/SingleMu/RECO/22Jan2013-v1/30007/067ADBD0-EC84-E211-9A27-001EC9D7FA38.root',
#        '/store/data/Run2012D/SingleMu/RECO/22Jan2013-v1/30007/084435D7-ED84-E211-AF65-20CF3056171C.root',
#        '/store/data/Run2012D/SingleMu/RECO/22Jan2013-v1/30007/08B60E94-708B-E211-B7E6-90E6BA19A22E.root',
#        '/store/data/Run2012D/SingleMu/RECO/22Jan2013-v1/30007/08D649BB-7F8B-E211-BF21-00259073E466.root',
#        '/store/data/Run2012D/SingleMu/RECO/22Jan2013-v1/30007/08E2D9FD-6E8B-E211-951B-20CF3027A5AD.root',
#        '/store/data/Run2012D/SingleMu/RECO/22Jan2013-v1/30007/0A0E4A35-F084-E211-AB8C-90E6BA19A22D.root',
#        '/store/data/Run2012D/SingleMu/RECO/22Jan2013-v1/30007/0A17F60A-7D8B-E211-917A-20CF305B04D1.root',
#        '/store/data/Run2012D/SingleMu/RECO/22Jan2013-v1/30007/0A4266A1-738B-E211-B6DF-00259073E3C0.root',
    )
)

process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

#import FWCore.PythonUtilities.LumiList as LumiList
#process.source.lumisToProcess = LumiList.LumiList(filename = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Reprocessing/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt').getVLuminosityBlockRange()

MUONCUT = "pt>3 && abs(eta)<2.4" + \
        " && isGlobalMuon && isPFMuon" #+ \
#        " && globalTrack().normalizedChi2<10.0" + \
#        " && globalTrack().hitPattern().numberOfValidMuonHits > 0" + \
#        " && globalTrack().hitPattern().numberOfValidPixelHits>0" + \
#        " && numberOfMatchedStations>1" + \
#        " && globalTrack().hitPattern().trackerLayersWithMeasurement>5" #+ \

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


process.p = cms.Path(
    process.goodMuons * 
    process.cscPerformance
)
