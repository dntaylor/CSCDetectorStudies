from PhysicsTools.PatAlgos.patTemplate_cfg import *
from PhysicsTools.PatAlgos.tools.coreTools import *
removeMCMatching(process, ['All'])
#removeAllPATObjectsBut(process, ['Muons'])

process.maxEvents.input = 1000
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.options.wantSummary = True

process.source.fileNames = cms.untracked.vstring(
#	'/store/data/Run2012A/DoubleMu/RECO/13Jul2012-v1/00001/E0723268-B6D2-E111-A55E-001A92811732.root',
	'/store/data/Run2012A/DoubleMu/RECO/22Jan2013-v1/20000/002CEA8B-AC81-E211-A79A-002618943951.root',
	'/store/data/Run2012A/DoubleMu/RECO/22Jan2013-v1/20000/00DC7B9F-B681-E211-9E4B-00304867BEC0.root',
	'/store/data/Run2012A/DoubleMu/RECO/22Jan2013-v1/20000/009A6B2F-B081-E211-8B8B-0025905964BC.root',
	'/store/data/Run2012A/DoubleMu/RECO/22Jan2013-v1/20000/08127CBE-B381-E211-8925-0026189438AF.root',
	'/store/data/Run2012A/DoubleMu/RECO/22Jan2013-v1/20000/0631B914-B881-E211-8DA4-003048FFD79C.root',
	'/store/data/Run2012A/DoubleMu/RECO/22Jan2013-v1/20000/0A1AE15C-BA81-E211-88B2-0025905964BA.root',
	'/store/data/Run2012A/DoubleMu/RECO/22Jan2013-v1/20000/0A03D151-B581-E211-AE9A-002618943869.root',
	'/store/data/Run2012A/DoubleMu/RECO/22Jan2013-v1/20000/0AB0DD40-B281-E211-9D53-002618FDA207.root',
	'/store/data/Run2012A/DoubleMu/RECO/22Jan2013-v1/20000/0A848EB0-B381-E211-ACED-003048678C3A.root',
	'/store/data/Run2012A/DoubleMu/RECO/22Jan2013-v1/20000/0AE7CF87-C481-E211-94FA-002618FDA279.root',
)

process.out.fileName = 'patTuple_muon.root'

#process.filterME42 = cms.EDFilter("CandViewSelector",
#	cut = cms.string('1.15 < eta < 1.85'),
#	src = cms.InputTag("cleanPatMuons"),
#	filter = cms.bool(True),
#)

#process.selectedPatMuons.cut = '1.15 < eta < 1.85'

process.muonEventFilter = cms.EDFilter('PATCandViewCountFilter',
	minNumber = cms.uint32(2),
	maxNumber = cms.uint32(1000),
	src = cms.InputTag('cleanPatMuons'),
)

process.out.outputCommands = cms.untracked.vstring(
	'drop *',
	'keep *_cleanPatMuons*_*_*',
)

process.p = cms.Path(
	process.patDefaultSequence *
#	process.filterME42 *
	process.muonEventFilter
)

