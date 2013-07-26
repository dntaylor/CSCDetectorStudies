from PhysicsTools.PatAlgos.patTemplate_cfg import *
from PhysicsTools.PatAlgos.tools.coreTools import *
removeMCMatching(process, ['All'])
#removeAllPATObjectsBut(process, ['Muons'])

process.maxEvents.input = 1000
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.options.wantSummary = True

process.source.fileNames = cms.untracked.vstring(
	'/store/data/Run2012A/DoubleMu/RECO/13Jul2012-v1/00001/E0723268-B6D2-E111-A55E-001A92811732.root',
)

process.out.fileName = 'patTuple_muon.root'

process.filterME42 = cms.EDFilter("CandViewSelector",
	cut = cms.string('1.15 < eta < 1.85'),
	src = cms.InputTag("cleanPatMuons"),
	filter = cms.bool(True),
)

process.selectedPatMuons.cut = '1.15 < eta < 1.85'

process.muonEventFilter = cms.EDFilter('PATCandViewCountFilter',
	minNumber = cms.uint32(2),
	maxNumber = cms.uint32(1000),
	src = cms.InputTag('cleanPatMuons'),
)

process.p = cms.Path(
	process.patDefaultSequence *
	process.filterME42 *
	process.muonEventFilter
)

