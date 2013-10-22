// -*- C++ -*-
//
// Package:    L1CSCTFMethods
// Class:      L1CSCTFMethods
// 
/**\class L1CSCTFMethods L1CSCTFMethods.cc CSCDetectorStudies/L1CSCTFMethods/src/L1CSCTFMethods.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Devin Taylor
//         Created:  Sat Aug 17 11:14:58 CDT 2013
// $Id$
//
//


// system include files
#include <memory>

// framework include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "PhysicsTools/UtilAlgos/interface/BasicAnalyzer.h"
// dataformat include files

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
class TFile;
class TTree;

class L1CSCTFMethods : public edm::BasicAnalyzer {
   public:
      L1CSCTFMethods(const edm::ParameterSet& pset, TFileDirectory& fs);
      ~L1CSCTFMethods();

      void beginJob();
      void analyze(const edm::Event& event);
      void endJob();

   private:

      // ----------member data ---------------------------
      edm::InputTag muons_;

      std::map<std::string, TH1*> hists_;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//
