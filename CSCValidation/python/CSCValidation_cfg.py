import FWCore.ParameterSet.Config as cms

process = cms.Process("TEST")

process.load("Configuration/StandardSequences/Geometry_cff")
process.load("Configuration/StandardSequences/MagneticField_cff")
process.load("Configuration/StandardSequences/FrontierConditions_GlobalTag_cff")
process.load("Configuration/StandardSequences/RawToDigi_Data_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")

process.GlobalTag.globaltag = 'START53_LV4::All'

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.options = cms.untracked.PSet( SkipEvent = cms.untracked.vstring('ProductNotFound') )
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()
process.source = cms.Source ("PoolSource",fileNames = readFiles,secondaryFileNames = secFiles)
readFiles.extend( [
	'/store/relval/CMSSW_5_3_11_patch5/RelValZMM/GEN-SIM-DIGI-RAW-HLTDEBUG/START53_LV4_24Jul2013-v1/00000/0C975EBE-7AF4-E211-B28E-003048FFD728.root',
	'/store/relval/CMSSW_5_3_11_patch5/RelValZMM/GEN-SIM-DIGI-RAW-HLTDEBUG/START53_LV4_24Jul2013-v1/00000/2AC3B0D9-81F4-E211-8729-00248C0BE005.root',
	'/store/relval/CMSSW_5_3_11_patch5/RelValZMM/GEN-SIM-DIGI-RAW-HLTDEBUG/START53_LV4_24Jul2013-v1/00000/4C308CC2-7EF4-E211-B77E-0025905964A6.root',
	'/store/relval/CMSSW_5_3_11_patch5/RelValZMM/GEN-SIM-DIGI-RAW-HLTDEBUG/START53_LV4_24Jul2013-v1/00000/905CE49B-87F4-E211-9E86-002618943958.root',
	'/store/relval/CMSSW_5_3_11_patch5/RelValZMM/GEN-SIM-DIGI-RAW-HLTDEBUG/START53_LV4_24Jul2013-v1/00000/AE2A4BB5-84F4-E211-AC26-002618943934.root',
	] );
secFiles.extend( [
	] );

process.MessageLogger = cms.Service("MessageLogger",
	cout = cms.untracked.PSet(
		default = cms.untracked.PSet( limit = cms.untracked.int32(0) ),
		FwkJob = cms.untracked.PSet( limit = cms.untracked.int32(0) )
	),
	categories = cms.untracked.vstring('FwkJob'),
	destinations = cms.untracked.vstring('cout')
)


process.cscValidation = cms.EDAnalyzer("CSCValidation",
	rootFileName = cms.untracked.string('RelValZmm_5_3_11_patch5.root'),
	isSimulation = cms.untracked.bool(False),
	writeTreeToFile = cms.untracked.bool(True),
	useDigis = cms.untracked.bool(True),
	detailedAnalysis = cms.untracked.bool(False),
	useTriggerFilter = cms.untracked.bool(False),
	useQualityFilter = cms.untracked.bool(False),
	makeStandalonePlots = cms.untracked.bool(False),
	makeTimeMonitorPlots = cms.untracked.bool(True),
	alctDigiTag = cms.InputTag("muonCSCDigis","MuonCSCALCTDigi"),
	clctDigiTag = cms.InputTag("muonCSCDigis","MuonCSCCLCTDigi"),
	corrlctDigiTag = cms.InputTag("muonCSCDigis","MuonCSCCorrelatedLCTDigi"),
	stripDigiTag = cms.InputTag("muonCSCDigis","MuonCSCStripDigi"),
	wireDigiTag = cms.InputTag("muonCSCDigis","MuonCSCWireDigi"),
	compDigiTag = cms.InputTag("muonCSCDigis","MuonCSCComparatorDigi"),
	cscRecHitTag = cms.InputTag("csc2DRecHits"),
	cscSegTag = cms.InputTag("cscSegments"),
	saMuonTag = cms.InputTag("standAloneMuons"),
	l1aTag = cms.InputTag("gtDigis"),
	hltTag = cms.InputTag("TriggerResults::HLT"),
	makeHLTPlots = cms.untracked.bool(True),
	simHitTag = cms.InputTag("g4SimHits", "MuonCSCHits")
)

process.load("L1Trigger.CSCTriggerPrimitives.cscTriggerPrimitiveDigis_cfi")
process.cscTriggerPrimitiveDigis.CSCComparatorDigiProducer = "muonCSCDigis:MuonCSCComparatorDigi"
process.cscTriggerPrimitiveDigis.CSCWireDigiProducer = "muonCSCDigis:MuonCSCWireDigi"
process.cscTriggerPrimitiveDigis.tmbParam.mpcBlockMe1a = 0
process.load("L1TriggerConfig.L1CSCTPConfigProducers.L1CSCTriggerPrimitivesConfig_cff")
process.l1csctpconf.alctParamMTCC2.alctNplanesHitPretrig = 3
process.l1csctpconf.alctParamMTCC2.alctNplanesHitAccelPretrig = 3
process.l1csctpconf.clctParam.clctNplanesHitPretrig = 3
process.l1csctpconf.clctParam.clctHitPersist = 4

process.lctreader = cms.EDAnalyzer("CSCTriggerPrimitivesReader",
	debug = cms.untracked.bool(False),
	dataLctsIn = cms.bool(True),
	emulLctsIn = cms.bool(True),
	isMTCCData = cms.bool(False),
	printps = cms.bool(False),
	CSCLCTProducerData = cms.untracked.string("muonCSCDigis"),
	CSCLCTProducerEmul = cms.untracked.string("cscTriggerPrimitiveDigis"),
	CSCSimHitProducer = cms.InputTag("g4SimHits", "MuonCSCHits"),  # Full sim.
	CSCComparatorDigiProducer = cms.InputTag("simMuonCSCDigis","MuonCSCComparatorDigi"),
	CSCWireDigiProducer = cms.InputTag("simMuonCSCDigis","MuonCSCWireDigi")
)

process.TFileService = cms.Service("TFileService",
	fileName = cms.string('TPEHists.root')
)

process.p = cms.Path(
	process.gtDigis * 
	process.muonCSCDigis * 
	process.csc2DRecHits * 
	process.cscSegments * 
	process.cscTriggerPrimitiveDigis * 
	process.lctreader * 
	process.cscValidation
)


