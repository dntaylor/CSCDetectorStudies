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

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
//
// class declaration
//

class L1CSCTFMethods : public edm::EDAnalyzer {
   public:
      explicit L1CSCTFMethods(const edm::ParameterSet&);
      ~L1CSCTFMethods();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      virtual void beginRun(edm::Run const&, edm::EventSetup const&);
      virtual void endRun(edm::Run const&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

      // ----------member data ---------------------------
};

/
// constants, enums and typedefs
//

//
// static data member definitions
//
