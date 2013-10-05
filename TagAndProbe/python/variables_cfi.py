import FWCore.ParameterSet.Config as cms

KinematicVariables = cms.PSet(
    pt = cms.string("pt"),
    p = cms.string("p"),
    eta = cms.string("eta"),
    phi = cms.string("phi"),
    abseta = cms.string("abs(eta)"),
    charge = cms.string("charge")
)

# Muon ID flags
MuonIDVariables = cms.PSet(
    isCaloMuon = cms.string("isCaloMuon"),
    isGlobalMuon = cms.string("isGlobalMuon"),
    isTrackerMuon = cms.string("isTrackerMuon"),
    isPFMuon = cms.string("isPFMuon"),
    #isLooseMuon = cms.string("isPFMuon() && (isGlobalMuon() || isTrackerMuon())"),
    #isTightMuon = cms.string("isPFMuon && numberOfMatchedStations > 1 && "+
    #    "track.hitPattern.trackerLayersWithMeasurement > 5 && track.hitPattern.numberOfValidPixelHits > 0"),
    #isTightMuon = cms.string("isGlobalMuon && isPFMuon" + \
    #    " && globalTrack().normalizedChi2<10.0" + \
    #    " && globalTrack().hitPattern().numberOfValidMuonHits > 0" + \
    #    " && globalTrack().hitPattern().numberOfValidPixelHits>0" + \
    #    " && numberOfMatchedStations>1" + \
    #    " && globalTrack().hitPattern().trackerLayersWithMeasurement>5"),
)

# standalone muon variables
standAloneVariables = cms.PSet(
    muonStationsWithValidHits = cms.string("? outerTrack.isNull() ? -1 : outerTrack.hitPattern.muonStationsWithValidHits()"),
)
