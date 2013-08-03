import FWCore.ParameterSet.Config as cms

process = cms.Process("PickEvent")

process.source = cms.Source ("PoolSource",
	fileNames = cms.untracked.vstring (
#		'/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/0028A003-E66E-E211-9D00-1CC1DE051060.root',
#                '/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/0093E911-5A6F-E211-99BF-0017A477041C.root',
#                '/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/00B9F1D4-3B6F-E211-BEC6-0017A4770C28.root',
#                '/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/00CBB6A4-5D6F-E211-AB8A-78E7D1E49B52.root',
#                '/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/00D0FB72-366F-E211-B3E0-0017A4771018.root',
#                '/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/00F428F5-E56E-E211-99B3-0017A4770C00.root',
#                '/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/02F5AC72-136F-E211-9185-AC162DABAF78.root',
#                '/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/043DDB54-FF6E-E211-93B0-00266CFFC550.root',
#                '/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/049A483F-E66E-E211-916E-1CC1DE05D2F8.root',
#                '/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/04D14EC2-166F-E211-A932-1CC1DE046F00.root',
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
	input = cms.untracked.int32 (10000)
)

process.Out = cms.OutputModule("PoolOutputModule",
	fileName = cms.untracked.string ("SingleMu_Run2012A_RAW.root")
)

process.end = cms.EndPath(process.Out)
