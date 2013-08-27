import FWCore.ParameterSet.Config as cms
from RecoMuon.MuonIdentification.calomuons_cfi import calomuons;

###
# User configurable parameters
###
MCFLAG = False 				# MC not yet implemented

GLOBALTAG = "FT_R_53_V6::All" 		# 2012AB re-reco + prompt tag
HLTTRIGGER = cms.vstring( 'HLT_IsoMu24_v*', 'HLT_IsoMu24_eta2p1_v*', 'HLT_Mu40_v*', 'HLT_Mu40_eta2p1_v*' )

OUTPUTFILENAME = "ME42TagAndProbeTree.root"

MUONCUT = "pt>20 && abs(eta)<2.4"
PLUSME42ETACUT = " && eta>1.2 && eta<1.8"
MINUSME42ETACUT = " && eta<-1.2 && eta>-1.8"
ME42PHICUT = " && phi>75*3.14159/180 && phi<125*3.14159/180"
NOME42PHICUT = " && (phi<75*3.14159/180 || phi>125*3.14159/180)"
TAGMUONCOLLECTION = "muons"
PROBEMUONCOLLECTION = "muons" 

TAGMUONCUT = MUONCUT + \
	" && isGlobalMuon && isPFMuon" + \
	" && globalTrack().normalizedChi2<10.0" + \
	" && globalTrack().hitPattern().numberOfValidMuonHits > 0" + \
	" && globalTrack().hitPattern().numberOfValidPixelHits>0" + \
	" && numberOfMatchedStations>1" + \
	" && globalTrack().hitPattern().trackerLayersWithMeasurement>5" #+ \
#	" && abs(muonBestTrack().dxy(vertex.position()))<0.2" #+ \
#	" && abs(muonBestTrack().dz(vertex.position()))<0.5"
PROBEMUONCUT = MUONCUT + \
	" && isStandAloneMuon" #+ \
#	" && globalTrack().hitPattern().trackerLayersWithMeasurement>5" #+ \
#	" && dxy(pv)<=0.2 && dz(pv)<=0.2"
PASSPROBEMUONCUT = MUONCUT +\
	" && isGlobalMuon && isPFMuon && isTrackerMuon"

LOOSEMUON = "isPFMuon && (isGlobalMuon || isTrackerMuon)"
TIGHTMUON = "isPFMuon && isGlobalMuon" + \
	" && globalTrack().normalizedChi2<10.0" + \
	" && globalTrack().hitPattern().numberOfValidMuonHits>0" + \
	" && numberOfMatchedStations>1 && globalTrack().hitPattern().numberOfValidPixelHits>0" + \
	" && globalTrack().hitPattern().trackerLayersWithMeasurement>5" #+ \
#	" && abs(muonBestTrack().dxy(vertex.position()))<0.2" + \
#	" && abs(muonBestTrack().dz(vertex.position()))<0.5"

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
#		'/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/0028A003-E66E-E211-9D00-1CC1DE051060.root',
#		'/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/0093E911-5A6F-E211-99BF-0017A477041C.root',
#		'/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/00B9F1D4-3B6F-E211-BEC6-0017A4770C28.root',
#		'/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/00CBB6A4-5D6F-E211-AB8A-78E7D1E49B52.root',
#		'/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/00D0FB72-366F-E211-B3E0-0017A4771018.root',
#		'/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/00F428F5-E56E-E211-99B3-0017A4770C00.root',
#		'/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/02F5AC72-136F-E211-9185-AC162DABAF78.root',
#		'/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/043DDB54-FF6E-E211-93B0-00266CFFC550.root',
#		'/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/049A483F-E66E-E211-916E-1CC1DE05D2F8.root',
#		'/store/data/Run2012A/SingleMu/RECO/22Jan2013-v1/20000/04D14EC2-166F-E211-A932-1CC1DE046F00.root',
#		'/store/data/Run2012B/SingleMu/AOD/22Jan2013-v1/30000/FE606687-E570-E211-86FF-E0CB4E1A1182.root',
#                '/store/data/Run2012B/SingleMu/AOD/22Jan2013-v1/30000/FE3B6744-5D74-E211-941D-BCAEC50971F9.root',
#                '/store/data/Run2012B/SingleMu/AOD/22Jan2013-v1/30000/FE1140ED-B870-E211-8D82-485B39800B8D.root',
#                '/store/data/Run2012B/SingleMu/AOD/22Jan2013-v1/30000/FE98E065-5D72-E211-8D86-20CF305616D0.root',
#                '/store/data/Run2012B/SingleMu/AOD/22Jan2013-v1/30000/FE8A9D5D-7072-E211-82CB-00259073E36E.root',
		'file:SingleMu_Run2012A_RECO.root'
	)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

###
# only process good lumis
###
import FWCore.PythonUtilities.LumiList as LumiList
process.source.lumisToProcess = LumiList.LumiList(filename = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Reprocessing/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt').getVLuminosityBlockRange()

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

process.ZTagProbe = cms.EDProducer("CandViewShallowCloneCombiner",
	decay = cms.string("tagMuons@+ probeMuons@-"),
	cut = cms.string(ZMASSCUT),
)

# clones for various conditions
process.tagMuonsME42 = process.tagMuons.clone( cut = TAGMUONCUT + PLUSME42ETACUT + ME42PHICUT ) 
process.tagMuonsNoME42 = process.tagMuons.clone( cut = TAGMUONCUT + PLUSME42ETACUT + NOME42PHICUT ) 
process.tagMuonsME42Eta = process.tagMuons.clone( cut = TAGMUONCUT + PLUSME42ETACUT ) 
process.tagMuonsNoME42Eta = process.tagMuons.clone( cut = TAGMUONCUT + MINUSME42ETACUT ) 
process.tagMuonsME42Phi = process.tagMuons.clone( cut = TAGMUONCUT + ME42PHICUT ) 
process.tagMuonsNoME42Phi = process.tagMuons.clone( cut = TAGMUONCUT + NOME42PHICUT ) 

process.probeMuonsME42 = process.probeMuons.clone( cut = TAGMUONCUT + PLUSME42ETACUT + ME42PHICUT ) 
process.probeMuonsNoME42 = process.probeMuons.clone( cut = TAGMUONCUT + PLUSME42ETACUT + NOME42PHICUT )
process.probeMuonsME42Eta = process.probeMuons.clone( cut = TAGMUONCUT + PLUSME42ETACUT ) 
process.probeMuonsNoME42Eta = process.probeMuons.clone( cut = TAGMUONCUT + MINUSME42ETACUT ) 
process.probeMuonsME42Phi = process.probeMuons.clone( cut = TAGMUONCUT + ME42PHICUT ) 
process.probeMuonsNoME42Phi = process.probeMuons.clone( cut = TAGMUONCUT + NOME42PHICUT ) 

process.ZTagProbeME42 = process.ZTagProbe.clone( decay = cms.string("tagMuonsME42@+ probeMuonsME42@-"), )
process.ZTagProbeNoME42 = process.ZTagProbe.clone( decay = cms.string("tagMuonsNoME42@+ probeMuonsNoME42@-"), )
process.ZTagProbeME42Eta = process.ZTagProbe.clone( decay = cms.string("tagMuonsME42Eta@+ probeMuonsME42Eta@-"), )
process.ZTagProbeNoME42Eta = process.ZTagProbe.clone( decay = cms.string("tagMuonsNoME42Eta@+ probeMuonsNoME42Eta@-"), )
process.ZTagProbeME42Phi = process.ZTagProbe.clone( decay = cms.string("tagMuonsME42Phi@+ probeMuonsME42Phi@-"), )
process.ZTagProbeNoME42Phi = process.ZTagProbe.clone( decay = cms.string("tagMuonsNoME42Phi@+ probeMuonsNoME42Phi@-"), )

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
	flags = cms.PSet(
		passingTightMuon = cms.string(TIGHTMUON),
		passingLooseMuon = cms.string(LOOSEMUON),
	),
	addRunLumiInfo = cms.bool(True),
	isMC = cms.bool(MCFLAG),
)

# clone tag and probe trees
process.tagAndProbeTreeME42 = process.tagAndProbeTree.clone( tagProbePairs = cms.InputTag("ZTagProbeME42") )
process.tagAndProbeTreeNoME42 = process.tagAndProbeTree.clone( tagProbePairs = cms.InputTag("ZTagProbeNoME42") )
process.tagAndProbeTreeME42Eta = process.tagAndProbeTree.clone( tagProbePairs = cms.InputTag("ZTagProbeME42Eta") )
process.tagAndProbeTreeNoME42Eta = process.tagAndProbeTree.clone( tagProbePairs = cms.InputTag("ZTagProbeNoME42Eta") )
process.tagAndProbeTreeME42Phi = process.tagAndProbeTree.clone( tagProbePairs = cms.InputTag("ZTagProbeME42Phi") )
process.tagAndProbeTreeNoME42Phi = process.tagAndProbeTree.clone( tagProbePairs = cms.InputTag("ZTagProbeNoME42Phi") )

###
# path
###
process.TagAndProbe = cms.Path(
	process.tagMuons *
	(process.tagMuonsME42 + process.tagMuonsNoME42 + process.tagMuonsME42Eta + process.tagMuonsNoME42Eta + process.tagMuonsME42Phi + process.tagMuonsNoME42Phi) *
	process.probeMuons *
	(process.probeMuonsME42 + process.probeMuonsNoME42 + process.probeMuonsME42Eta + process.probeMuonsNoME42Eta + process.probeMuonsME42Phi + process.probeMuonsNoME42Phi) *
	process.ZTagProbe *
	(process.ZTagProbeME42 + process.ZTagProbeNoME42 + process.ZTagProbeME42Eta + process.ZTagProbeNoME42Eta + process.ZTagProbeME42Phi + process.ZTagProbeNoME42Phi) *
	process.tagAndProbeTree * 
	(process.tagAndProbeTreeME42 + process.tagAndProbeTreeNoME42 + process.tagAndProbeTreeME42Eta + process.tagAndProbeTreeNoME42Eta + process.tagAndProbeTreeME42Phi + process.tagAndProbeTreeNoME42Phi) 
)

###
# output
###
process.TFileService = cms.Service("TFileService",
	fileName = cms.string(OUTPUTFILENAME),
)

