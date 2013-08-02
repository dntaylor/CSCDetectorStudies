import FWCore.ParameterSet.Config as cms

process = cms.Process("PickEvent")

process.source = cms.Source ("PoolSource",
	fileNames = cms.untracked.vstring (
		'/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/0028A003-E66E-E211-9D00-1CC1DE051060.root',
                '/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/0093E911-5A6F-E211-99BF-0017A477041C.root',
                '/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/00B9F1D4-3B6F-E211-BEC6-0017A4770C28.root',
                '/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/00CBB6A4-5D6F-E211-AB8A-78E7D1E49B52.root',
                '/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/00D0FB72-366F-E211-B3E0-0017A4771018.root',
                '/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/00F428F5-E56E-E211-99B3-0017A4770C00.root',
                '/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/02F5AC72-136F-E211-9185-AC162DABAF78.root',
                '/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/043DDB54-FF6E-E211-93B0-00266CFFC550.root',
                '/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/049A483F-E66E-E211-916E-1CC1DE05D2F8.root',
                '/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/04D14EC2-166F-E211-A932-1CC1DE046F00.root',
	)
)

process.maxEvents = cms.untracked.PSet(
	input = cms.untracked.int32 (10000)
)

process.Out = cms.OutputModule("PoolOutputModule",
	fileName = cms.untracked.string ("SingleMu_Run2012A_RECO.root")
)

process.end = cms.EndPath(process.Out)
