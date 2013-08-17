// -*- C++ -*-
//
// Package:    CSCPerformance
// Class:      CSCPerformance
// 
/**\class CSCPerformance CSCPerformance.cc CSCDetectorStudies/CSCPerformance/src/CSCPerformance.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Devin Taylor
//         Created:  Sun Aug  4 03:52:35 CDT 2013
// $Id$
//
//
#ifndef _CSCPERFORMANCE_H_
#define _CSCPERFORMANCE_H_

// system include files
#include <memory>

// framework
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/ESHandle.h"
// Data formats
#include "DataFormats/CSCRecHit/interface/CSCRecHit2D.h"
#include "DataFormats/CSCRecHit/interface/CSCRecHit2DCollection.h"
#include "DataFormats/CSCRecHit/interface/CSCSegmentCollection.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/L1GlobalMuonTrigger/interface/L1MuGMTReadoutCollection.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/MuonDetId/interface/CSCDetId.h"
#include "DataFormats/MuonDetId/interface/RPCDetId.h"
#include "DataFormats/MuonDetId/interface/DTChamberId.h"
#include "DataFormats/L1CSCTrackFinder/interface/L1CSCTrackCollection.h"
#include "DataFormats/L1CSCTrackFinder/interface/L1Track.h"
#include "DataFormats/CSCDigi/interface/CSCCorrelatedLCTDigiCollection.h"
// Geometry
#include "Geometry/Records/interface/MuonGeometryRecord.h"
#include "Geometry/CSCGeometry/interface/CSCGeometry.h"
#include "Geometry/CSCGeometry/interface/CSCLayer.h"
// root
#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TMath.h"
//
// class declaration
//

class CSCPerformance : public edm::EDAnalyzer {
   public:
      explicit CSCPerformance(const edm::ParameterSet&);
      ~CSCPerformance();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      virtual void beginRun(edm::Run const&, edm::EventSetup const&);
      virtual void endRun(edm::Run const&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
      virtual void plotMatchedChambers(edm::Handle<reco::MuonCollection>);//, edm::ESHandle<CSCGeometry>);
      virtual void outputDetID(reco::Muon);
      virtual void outputDetID(DetId);
      virtual bool hasChamber(reco::Muon, int);
      virtual int numberOfMatchedCSCStations(reco::Muon);
      virtual int getHitPattern(reco::Muon);
      virtual bool isME42Region(L1CSCTrack);

      // ----------member data ---------------------------
      edm::InputTag cscRecHitTag;
      edm::InputTag cscSegmentTag;
      edm::InputTag saMuonTag;
      edm::InputTag allMuonsTag;

      std::map<std::string,TH1*> hists;
};

//
// constants, enums and typedefs
//

#endif // _CSCPERFORMANCE_H_
