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

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
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

      // ----------member data ---------------------------
};

//
// constants, enums and typedefs
//

#endif // _CSCPERFORMANCE_H_
