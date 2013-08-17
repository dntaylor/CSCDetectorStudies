import FWCore.ParameterSet.Config as cms

process = cms.Process("PickEvent")

process.source = cms.Source ("PoolSource",
	fileNames = cms.untracked.vstring (
#		'/store/data/Run2012D/SingleMu/RECO/22Jan2013-v1/30019/A8724061-438A-E211-A996-00259073E4CC.root',
#		'/store/data/Run2012D/SingleMu/RECO/22Jan2013-v1/30019/AC3224F8-318A-E211-82C6-20CF3019DEFB.root',
#		'/store/data/Run2012D/SingleMu/RECO/22Jan2013-v1/30019/AEBBE055-418A-E211-900A-001EC9D825A9.root',
#		'/store/data/Run2012D/SingleMu/RECO/22Jan2013-v1/30019/B005E48C-428A-E211-8F83-00259073E3E4.root',
#		'/store/data/Run2012D/SingleMu/RECO/22Jan2013-v1/30019/B0A21146-418A-E211-89F0-00259073E4C8.root',
#		'/store/data/Run2012D/SingleMu/RECO/22Jan2013-v1/30019/B2DF77DB-428A-E211-8A52-90E6BA442F41.root',
#		'/store/data/Run2012D/SingleMu/RECO/22Jan2013-v1/30019/B2EE34CF-418A-E211-9E55-20CF3019DF17.root',
#		'/store/data/Run2012D/SingleMu/RECO/22Jan2013-v1/30019/B4F448C2-418A-E211-B031-20CF305616DC.root',
		'/store/data/Run2012A/SingleMu/RAW/v1/000/191/277/A6205402-3287-E111-B6C4-0025901D629C.root',
		'/store/data/Run2012A/SingleMu/RAW/v1/000/191/226/0C9553B4-2486-E111-9A2F-001D09F2A690.root',
		'/store/data/Run2012A/SingleMu/RAW/v1/000/191/811/8AC87474-608A-E111-B002-001D09F2527B.root',
		'/store/data/Run2012A/SingleMu/RAW/v1/000/191/202/3CECAD65-8885-E111-B5A3-5404A63886EC.root',
		'/store/data/Run2012A/SingleMu/RAW/v1/000/190/949/D041AE2E-0E84-E111-BD0B-001D09F29114.root',
		'/store/data/Run2012A/SingleMu/RAW/v1/000/190/705/320E0BB9-BE81-E111-94FE-003048D37666.root',
		'/store/data/Run2012A/SingleMu/RAW/v1/000/190/949/B824CDBF-2984-E111-8985-0030486730C6.root',
	)
)

process.maxEvents = cms.untracked.PSet(
	input = cms.untracked.int32 (1000)
)

process.Out = cms.OutputModule("PoolOutputModule",
	fileName = cms.untracked.string ("SingleMu_Run2012A_RAW.root")
)

process.end = cms.EndPath(process.Out)
