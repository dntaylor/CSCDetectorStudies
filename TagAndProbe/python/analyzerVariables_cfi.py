import FWCore.ParameterSet.Config as cms

KinematicVariables = cms.PSet(
    p = cms.vstring("Probe p", "0", "500", "GeV/c"),
    pt = cms.vstring("Probe p_{T}", "0", "500", "GeV/c"),
    eta = cms.vstring("Probe #eta", "-2.4", "2.4", ""),
    phi = cms.vstring("Probe #phi", "-3.14159", "3.14159", ""),
    abseta = cms.vstring("Probe abs(#eta)", "0", "2.4", ""),
    charge = cms.vstring("Probe Charge","-1","1",""),
    outerEta = cms.vstring("Probe outer #eta", "-2.4", "2.4", ""),
    outerPhi = cms.vstring("Probe outer #phi", "-3.14159", "3.14159", ""),
)

MuonIDCategories = cms.PSet(
    isCaloMuon = cms.vstring("pass","dummy[true=1,false=0]"),
    isGlobalMuon = cms.vstring("pass","dummy[true=1,false=0]"),
    isTrackerMuon = cms.vstring("pass","dummy[true=1,false=0]"),
    isPFMuon = cms.vstring("pass","dummy[true=1,false=0]"),
    isLooseMuon = cms.vstring("pass","dummy[true=1,false=0]"),
    isTightMuon = cms.vstring("pass","dummy[true=1,false=0]"),
)

standAloneVariables = cms.PSet(
)
