from PhysicsTools.PatAlgos.patTemplate_cfg import *

process.p = cms.Path(
	process.patDefaultSequence
)

process.maxEvents.input = 100

process.options.wantSummary = True

process.source.fileNames = cms.untracked.vstring('file:Run2012A-DoubleMuon.root')

from PhysicsTools.PatAlgos.patEventContent_cff import patEventContent
process.out = cms.OutputModule("PoolOutputModule",
                fileName = cms.untracked.string('patTuple_muon.root'), # save only events passing the full path 
                SelectEvents = cms.untracked.PSet(
                        SelectEvents = cms.vstring('p')
                        ),  
                outputCommands = cms.untracked.vstring('drop *', *patEventContent )
                )
process.outpath = cms.EndPath(process.out)
