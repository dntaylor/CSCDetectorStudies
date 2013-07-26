from PhysicsTools.PatAlgos.patTemplate_cfg import *
from PhysicsTools.PatAlgos.tools.coreTools import *
removeMCMatching(process, ['All'])
#removeAllPATObjectsBut(process, ['Muons'])

process.p = cms.Path(
	process.patDefaultSequence
)

process.maxEvents.input = 100

process.options.wantSummary = True

process.source.fileNames = cms.untracked.vstring(
		'/store/data/Run2012A/DoubleMu/RECO/13Jul2012-v1/00001/E0723268-B6D2-E111-A55E-001A92811732.root',
		)

process.out.fileName = 'patTuple_muon.root'
