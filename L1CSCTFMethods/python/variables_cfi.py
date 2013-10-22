import FWCore.ParameterSet.Config as cms

variables = cms.VPSet(
    cms.PSet(
        tag = cms.untracked.string("Pt"),
        quantity = cms.untracked.string("pt"),
    ),
    cms.PSet(
        tag = cms.untracked.string("P"),
        quantity = cms.untracked.string("p"),
    ),
    cms.PSet(
        tag = cms.untracked.string("Px"),
        quantity = cms.untracked.string("px"),
    ),
    cms.PSet(
        tag = cms.untracked.string("Py"),
        quantity = cms.untracked.string("py"),
    ),
    cms.PSet(
        tag = cms.untracked.string("Pz"),
        quantity = cms.untracked.string("pz"),
    ),
    cms.PSet(
        tag = cms.untracked.string("Eta"),
        quantity = cms.untracked.string("eta"),
    ),
    cms.PSet(
        tag = cms.untracked.string("Abseta"),
        quantity = cms.untracked.string("abs(eta)"),
    ),
    cms.PSet(
        tag = cms.untracked.string("Phi"),
        quantity = cms.untracked.string("phi"),
    ),
    cms.PSet(
        tag = cms.untracked.string("Theta"),
        quantity = cms.untracked.string("theta"),
    ),
    # L1
    cms.PSet(
        tag = cms.untracked.string("L1pt"),
        quantity = cms.untracked.string("? userCand('muonL1Info').isNull ? 0 : userCand('muonL1Info').pt"),
    ),
    cms.PSet(
        tag = cms.untracked.string("L1q"),
        quantity = cms.untracked.string("userInt('muonL1Info:quality')"),
    ),
    cms.PSet(
        tag = cms.untracked.string("L1dr"),
        quantity = cms.untracked.string("userFloat('muonL1Info:deltaR')"),
    ),
    # L2
    cms.PSet(
        tag = cms.untracked.string("L2pt"),
        quantity = cms.untracked.string("? triggerObjectMatchesByCollection('hltL2MuonCandidates').empty() ? 0 : triggerObjectMatchesByCollection('hltL2MuonCandidates').at(0).pt"),
    ),
    cms.PSet(
        tag = cms.untracked.string("L2eta"),
        quantity = cms.untracked.string("? triggerObjectMatchesByCollection('hltL2MuonCandidates').empty() ? 0 : triggerObjectMatchesByCollection('hltL2MuonCandidates').at(0).eta"),
    ),
    cms.PSet(
        tag = cms.untracked.string("L2dr"),
        quantity = cms.untracked.string("? triggerObjectMatchesByCollection('hltL2MuonCandidates').empty() ? 999 : "+
                      " deltaR( eta, phi, " +
                      "         triggerObjectMatchesByCollection('hltL2MuonCandidates').at(0).eta, "+
                      "         triggerObjectMatchesByCollection('hltL2MuonCandidates').at(0).phi ) "),
    ),
    # L3
    cms.PSet(
        tag = cms.untracked.string("L3pt"),
        quantity = cms.untracked.string("? triggerObjectMatchesByCollection('hltL3MuonCandidates').empty() ? 0 : triggerObjectMatchesByCollection('hltL3MuonCandidates').at(0).pt"),
    ),
    cms.PSet(
        tag = cms.untracked.string("L3dr"),
        quantity = cms.untracked.string("? triggerObjectMatchesByCollection('hltL3MuonCandidates').empty() ? 999 : "+
            " deltaR( eta, phi, " +
            "         triggerObjectMatchesByCollection('hltL3MuonCandidates').at(0).eta, "+
            "         triggerObjectMatchesByCollection('hltL3MuonCandidates').at(0).phi ) "),
    ),
    # Muon ID variables
    cms.PSet(
        tag = cms.untracked.string("CaloMuon"),
        quantity = cms.untracked.string("isCaloMuon"),
    ),
    cms.PSet(
        tag = cms.untracked.string("TrackerMuon"),
        quantity = cms.untracked.string("isTrackerMuon"),
    ),
    cms.PSet(
        tag = cms.untracked.string("GlobalMuon"),
        quantity = cms.untracked.string("isGlobalMuon"),
    ),
    cms.PSet(
        tag = cms.untracked.string("PFMuon"),
        quantity = cms.untracked.string("isPFMuon"),
    ),
#    cms.PSet(
#        tag = cms.untracked.string("LooseMuon"),
#        quantity = cms.untracked.string("isPFMuon && (isGlobalMuon || isTrackerMuon)"),
#    ),
#    cms.PSet(
#        tag = cms.untracked.string("TightMuon"),
#        quantity = cms.untracked.string("isGlobalMuon && isPFMuon" + \
#            " && globalTrack().normalizedChi2<10.0" + \
#            " && globalTrack().hitPattern().numberOfValidMuonHits > 0" + \
#            " && globalTrack().hitPattern().numberOfValidPixelHits>0" + \
#            " && numberOfMatchedStations>1" + \
#            " && globalTrack().hitPattern().trackerLayersWithMeasurement>5"),
#    ),
)
