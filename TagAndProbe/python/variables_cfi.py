import FWCore.ParameterSet.Config as cms

KinematicVariables = cms.PSet(
    pt = cms.string("pt"),
    p = cms.string("p"),
    eta = cms.string("eta"),
    phi = cms.string("phi"),
    abseta = cms.string("abs(eta)"),
    charge = cms.string("charge"),
#    outerEta = cms.string("track.outerEta"),
#    outerPhi = cms.string("track.outerPhi"),
)

# Muon ID flags
MuonIDVariables = cms.PSet(
    isCaloMuon = cms.string("isCaloMuon"),
    isGlobalMuon = cms.string("isGlobalMuon"),
    isTrackerMuon = cms.string("isTrackerMuon"),
    isPFMuon = cms.string("isPFMuon"),
    isLooseMuon = cms.string("isPFMuon && (isGlobalMuon || isTrackerMuon)"),
    isTightMuon = cms.string("isGlobalMuon && isPFMuon" + \
        " && globalTrack().normalizedChi2<10.0" + \
        " && globalTrack().hitPattern().numberOfValidMuonHits > 0" + \
        " && globalTrack().hitPattern().numberOfValidPixelHits>0" + \
        " && numberOfMatchedStations>1" + \
        " && globalTrack().hitPattern().trackerLayersWithMeasurement>5"),
)

# standalone muon variables
standAloneVariables = cms.PSet(
   # muonStationsWithValidHits = cms.string("? outerTrack.isNull() ? -1 : outerTrack.hitPattern.muonStationsWithValidHits()"),
)

# trigger variables
L1Variables = cms.PSet(
    l1pt = cms.string("? userCand('muonL1Info').isNull ? 0 : userCand('muonL1Info').pt"),
    l1q  = cms.string("userInt('muonL1Info:quality')"),
    l1dr = cms.string("userFloat('muonL1Info:deltaR')"),
    #l1ptByQ = cms.string("? userCand('muonL1Info:ByQ').isNull ? 0 : userCand('muonL1Info:ByQ').pt"),
    #l1qByQ  = cms.string("userInt('muonL1Info:qualityByQ')"),
    #l1drByQ = cms.string("userFloat('muonL1Info:deltaRByQ')"),
)

L2Variables = cms.PSet(
    l2pt  = cms.string("? triggerObjectMatchesByCollection('hltL2MuonCandidates').empty() ? 0 : triggerObjectMatchesByCollection('hltL2MuonCandidates').at(0).pt"),
    l2eta = cms.string("? triggerObjectMatchesByCollection('hltL2MuonCandidates').empty() ? 0 : triggerObjectMatchesByCollection('hltL2MuonCandidates').at(0).eta"),
    l2dr  = cms.string("? triggerObjectMatchesByCollection('hltL2MuonCandidates').empty() ? 999 : "+
                      " deltaR( eta, phi, " +
                      "         triggerObjectMatchesByCollection('hltL2MuonCandidates').at(0).eta, "+
                      "         triggerObjectMatchesByCollection('hltL2MuonCandidates').at(0).phi ) ")
)

L3Variables = cms.PSet(
    l3pt = cms.string("? triggerObjectMatchesByCollection('hltL3MuonCandidates').empty() ? 0 : triggerObjectMatchesByCollection('hltL3MuonCandidates').at(0).pt"),
    l3dr = cms.string("? triggerObjectMatchesByCollection('hltL3MuonCandidates').empty() ? 999 : "+
                      " deltaR( eta, phi, " +
                      "         triggerObjectMatchesByCollection('hltL3MuonCandidates').at(0).eta, "+
                      "         triggerObjectMatchesByCollection('hltL3MuonCandidates').at(0).phi ) ")
)

TriggerVariables = cms.PSet(L1Variables, L2Variables, L3Variables)
