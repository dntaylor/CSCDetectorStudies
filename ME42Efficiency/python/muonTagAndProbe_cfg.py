import FWCore.ParameterSet.Config as cms

MCFLAG = False

GLOBALTAG = "FT_R_53_V6::All" # 2012AB re-reco + prompt tag

MUONCOLLECTION = "muons"
MUONCUT = ""

TAGMUONCUT = ""
PROBEMUONCUT = ""
PASSPROBEMUONCUT = ""

PASSPROBEPSET = cms.PSet(
	isGlobalMuon = cms.string("isGlobalMuon"),
)

ZMASSCUT = "60.0 < mass < 120.0"
JPSIMASSCUT = "2.5 < mass < 3.8"

# includes
process = cms.Process("TagProbe")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.GlobalTag.globaltag = GLOBALTAG
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1

# datasets
process.source = cms.Source("PoolSource",
	fileNames = cms.untracked.vstring(
		'/store/data/Run2012A/DoubleMu/AOD/08Jun2012-v2/0000/005C23C4-11B3-E111-AF38-003048678A78.root',
	)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
process.source.inputCommands = cms.untracked.vstring("keep *")

# tag and probe selections
process.goodMuons = cms.EDFilter("MuonRefSelector",
	src = cms.InputTag(MUONCOLLECTION),
	cut = cms.string(MUONCUT),
)

process.tagMuons = cms.EDFilter("MuonRefSelector",
	src = cms.InputTag("goodMuons"),
	cut = cms.string(TAGMUONCUT),
)

from RecoMuon.MuonIdentification.calomuons_cfi import calomuons;
process.goodCaloMuons = cms.EDFilter("MuonRefSelector",
	src = cms.InputTag("calomuons"),
	cut = cms.string(MUONCUT),
)

process.mergedMuons = cms.EDProducer("CaloMuonMerger",
	muons     = cms.InputTag("goodMuons"), 
	caloMuons = cms.InputTag("goodCaloMuons"),
	minCaloCompatibility = calomuons.minCaloCompatibility
)

process.probeMuons = cms.EDFilter("MuonRefSelector",
	src = cms.InputTag("mergedMuons"),
	cut = cms.string(PROBEMUONCUT),
)

process.passProbeMuons = cms.EDFilter("MuonRefSelector",
	src = cms.InputTag("mergedMuons"),
	cut = cms.string(PASSPROBEMUONCUT),
)

process.ZTagProbe = cms.EDProducer("CandViewShallowCombiner",
	decay = cms.string("tagMuons@+ probeMuons@-"),
	cut = cms.string(ZMASSCUT),
)

# produce tag and probe trees
process.tagAndProbeTree = cms.EDAnalyzer("TagProbeFitTreeProducer",
	tagProbePairs = cms.InputTag("ZTagProbe"),
	arbitration = cms.string("OneProbe"),
	variables = cms.PSet(
		pt = cms.string("pt"),
		abseta = cms.string("abs(eta)"),
	),
	flags = PASSPROBEPSET,
	addRunLumiInfo = cms.bool(True),
	isMC = cms.bool(MCFLAG),
)


