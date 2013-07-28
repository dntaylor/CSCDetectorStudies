import FWCore.ParameterSet.Config as cms
#from PhysicsTools.PatAlgos.patTemplate_cfg import *

###
# User configurable parameters
###
MCFLAG = False 				# MC not yet implemented

GLOBALTAG = "FT_R_53_V6::All" 		# 2012AB re-reco + prompt tag

MUONCOLLECTION = "allMuons"
MUONCUT = "pt>20 && abs(eta)<2.4"

TAGMUONCUT = MUONCUT + " && isGlobalMuon && isPFMuon"
PROBEMUONCUT = MUONCUT + "&& isTrackerMuon"
PASSPROBEMUONCUT = MUONCUT + " && isGlobalMuon && isPFMuon && isTrackerMuon"

PASSPROBEPSET = cms.PSet(
	passingPFMuon = cms.string("isPFMuon"),
	passingGlobalMuonOrTrackerMuon = cms.string("isGlobalMuon || isTrackerMuon"),
	passingProbeMuonCut = cms.InputTag("passProbeMuons"),
)

ZMASSCUT = "60.0 < mass < 120.0"

OUTPUTFILENAME = "ME42TagAndProbeTree.root"



###
# includes
###
process = cms.Process("TagProbe")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.GlobalTag.globaltag = GLOBALTAG
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.MessageLogger.cerr.FwkReport.reportEvery = 100

###
# datasets
###
process.source = cms.Source("PoolSource",
	fileNames = cms.untracked.vstring(
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
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

###
# merge muons with calomuons
###
from RecoMuon.MuonIdentification.calomuons_cfi import calomuons;
process.allMuons = cms.EDProducer("CaloMuonMerger",
	muons = cms.InputTag("muons"), 
	caloMuons = cms.InputTag("calomuons"),
	minCaloCompatibility = calomuons.minCaloCompatibility,
)

###
# tag and probe selections
###
process.tagMuons = cms.EDFilter("MuonRefSelector",
	src = cms.InputTag(MUONCOLLECTION),
	cut = cms.string(TAGMUONCUT),
)

process.probeMuons = cms.EDFilter("MuonRefSelector",
	src = cms.InputTag(MUONCOLLECTION),
	cut = cms.string(PROBEMUONCUT),
)

process.passProbeMuons = cms.EDFilter("MuonRefSelector",
	src = cms.InputTag(MUONCOLLECTION),
	cut = cms.string(PASSPROBEMUONCUT),
)

process.ZTagProbe = cms.EDProducer("CandViewShallowCloneCombiner",
	decay = cms.string("tagMuons@+ probeMuons@-"),
	cut = cms.string(ZMASSCUT),
)

###
# produce tag and probe trees
###
process.tagAndProbeTree = cms.EDAnalyzer("TagProbeFitTreeProducer",
	tagProbePairs = cms.InputTag("ZTagProbe"),
	arbitration = cms.string("OneProbe"),
	variables = cms.PSet(
		pt = cms.string("pt"),
		eta = cms.string("eta"),
		phi = cms.string("phi"),
	),
	flags = PASSPROBEPSET,
	addRunLumiInfo = cms.bool(True),
	isMC = cms.bool(MCFLAG),
)

###
# path
###
process.TagAndProbe = cms.Path(
	process.allMuons *
	(process.tagMuons + process.probeMuons) *
	process.passProbeMuons *
	process.ZTagProbe *
	process.tagAndProbeTree
	)

###
# output
###
process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string(OUTPUTFILENAME)
)
