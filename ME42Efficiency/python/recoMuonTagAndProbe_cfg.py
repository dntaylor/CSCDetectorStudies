import FWCore.ParameterSet.Config as cms

###
# User configurable parameters
###
MCFLAG = False 				# MC not yet implemented

GLOBALTAG = "FT_R_53_V6::All" 		# 2012AB re-reco + prompt tag

OUTPUTFILENAME = "ME42TagAndProbeTree.root"

MUONCUT = "pt>20 && abs(eta)<2.4"
ME42CUT = " && 1.396<phi<2.269"
NOME42CUT = " && (phi<1.396 || phi>2.269)"
TAGMUONCOLLECTION = "muons"
PROBEMUONCOLLECTION = "muons"

TAGMUONCUT = MUONCUT + \
	" && isGlobalMuon && isPFMuon" #+ \
#	" && nChi2<10.0 && nValidMuonHits > 0" + \
#	" && nMatchedStations>1 && nValidPixelHits>0" + \
#	" && trackerLayersWithMeasurement>5" + \
#	" && dxy(pv)<=0.2 && dz(pv)<=0.2"
PROBEMUONCUT = MUONCUT #+ \
#	" && trackerLayersWithMeasurements>5" + \
#	" && dxy(pv)<=0.2 && dz(pv)<=0.2"
PASSPROBEMUONCUT = MUONCUT +\
	" && isGlobalMuon && isPFMuon && isTrackerMuon"

LOOSEMUON = "isPFMuon && (isGlobalMuon || isTrackerMuon)"
TIGHTMUON = "isPFMuon && isGlobalMuon" #+ \
#	" && nChi2<10.0 && nValidMuonHits>0" + \
#	" && nMatchedStations>1 && nValidPixelHits>0" + \
#	" && trackerLayersWithMeasurement>5"

PASSPROBEPSET = cms.PSet(
	passingPFMuon = cms.string("isPFMuon"),
	passingCaloMuon = cms.string("isCaloMuon"),
	passingTrackerMuon = cms.string("isTrackerMuon"),
	passingLooseMuon = cms.string(LOOSEMUON),
	passingGlobalMuon = cms.string("isGlobalMuon"),
	passingTightMuon = cms.string(TIGHTMUON),
	passingProbeMuonCut = cms.InputTag("passProbeMuons"),
)

ZMASSCUT = "60.0 < mass < 120.0"


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
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

###
# datasets
###
process.source = cms.Source("PoolSource",
	fileNames = cms.untracked.vstring(
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
	src = cms.InputTag(TAGMUONCOLLECTION),
	cut = cms.string(TAGMUONCUT),
)

process.probeMuons = cms.EDFilter("MuonRefSelector",
	src = cms.InputTag(PROBEMUONCOLLECTION),
	cut = cms.string(PROBEMUONCUT),
)

process.passProbeMuons = cms.EDFilter("MuonRefSelector",
	src = cms.InputTag(PROBEMUONCOLLECTION),
	cut = cms.string(PASSPROBEMUONCUT),
)

process.ZTagProbe = cms.EDProducer("CandViewShallowCloneCombiner",
	decay = cms.string("tagMuons@+ probeMuons@-"),
	cut = cms.string(ZMASSCUT),
)

process.probeMuonsWithME42 = process.probeMuons.clone( cut = PROBEMUONCUT + ME42CUT )
process.passProbeMuonsWithME42 = process.passProbeMuons.clone( cut = PASSPROBEMUONCUT + ME42CUT )
process.probeMuonsWithoutME42 = process.probeMuons.clone( cut = PROBEMUONCUT + NOME42CUT )
process.passProbeMuonsWithoutME42 = process.passProbeMuons.clone( cut = PASSPROBEMUONCUT + NOME42CUT )
process.ZTagProbeWithME42 = process.ZTagProbe.clone( decay = cms.string("tagMuons@+ probeMuonsWithME42@-") )
process.ZTagProbeWithoutME42 = process.ZTagProbe.clone( decay = cms.string("tagMuons@+ probeMuonsWithoutME42@-") )

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

process.tagAndProbeTreeWithME42 = process.tagAndProbeTree.clone( tagProbePairs = cms.InputTag("ZTagProbeWithME42") )
process.tagAndProbeTreeWithoutME42 = process.tagAndProbeTree.clone( tagProbePairs = cms.InputTag("ZTagProbeWithoutME42") )

###
# path
###
process.TagAndProbe = cms.Path(
	process.allMuons *
	(process.tagMuons + process.probeMuons) *
	(process.probeMuonsWithME42 + process.probeMuonsWithoutME42) *
	process.passProbeMuons *
	(process.passProbeMuonsWithME42 + process.passProbeMuonsWithoutME42) *
	process.ZTagProbe *
	(process.ZTagProbeWithME42 + process.ZTagProbeWithoutME42) *
	process.tagAndProbeTree *
	(process.tagAndProbeTreeWithME42 + process.tagAndProbeTreeWithoutME42)
	)

###
# output
###
process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string(OUTPUTFILENAME)
)