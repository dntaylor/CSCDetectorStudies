// -*- C++ -*-
//
// Package:    MuonME42CandidateProducer
// Class:      MuonME42CandidateProducer
// 
/**\class MuonME42CandidateProducer MuonME42CandidateProducer.cc CSCDetectorStudies/MuonME42CandidateProducer/src/MuonME42CandidateProducer.cc

 Description: Plugin to select candidates that pass through an ME4/2 detector element

 Implementation:
     Uses modified PropagateToMuon to propagate a track to the 4th muon station and then selects the eta/phi region of current setup
*/
//
// Original Author:  Devin Taylor
//         Created:  Tue Sep  3 14:15:46 CDT 2013
// $Id$
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"

#include "TrackingTools/TrajectoryState/interface/TrajectoryStateOnSurface.h"

#include "MagneticField/Engine/interface/MagneticField.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "Geometry/Records/interface/GlobalTrackingGeometryRecord.h"
#include "Geometry/CommonDetUnit/interface/GlobalTrackingGeometry.h"

#include "MuonAnalysis/MuonAssociators/interface/PropagateToMuon.h"

#include "TMath.h"


//
// class declaration
//

class MuonME42CandidateProducer : public edm::EDProducer {
   public:
      explicit MuonME42CandidateProducer(const edm::ParameterSet&);
      ~MuonME42CandidateProducer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual void produce(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      virtual void beginRun(edm::Run&, edm::EventSetup const&);
      virtual void endRun(edm::Run&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);

      virtual bool isME42(GlobalPoint);

      // ----------member data ---------------------------
      edm::InputTag src_;
      edm::ParameterSet muonPropagatorPSet_;

      edm::ESHandle<MagneticField> theMGField_;
      edm::ESHandle<GlobalTrackingGeometry> theTrackingGeometry_;
};

//
// constants, enums and typedefs
//


//
// static data member definitions
//

//
// constructors and destructor
//
MuonME42CandidateProducer::MuonME42CandidateProducer(const edm::ParameterSet& iConfig) :
   src_(iConfig.getParameter<edm::InputTag>("src")),
   muonPropagatorPSet_(iConfig.getParameter<edm::ParameterSet>("MuonPropagator"))
{
   //register your products
   produces<edm::ValueMap<float>>("isME42");
   produces<reco::CandidateBaseRefVector>();
}


MuonME42CandidateProducer::~MuonME42CandidateProducer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)
}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
MuonME42CandidateProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

   // Handles to physics objects
   Handle<View<reco::Candidate>> src;
   iEvent.getByLabel(src_,src);

   iSetup.get<IdealMagneticFieldRecord>().get(theMGField_);
   iSetup.get<GlobalTrackingGeometryRecord>().get(theTrackingGeometry_);

   // need to initialize the muon propagator at each event
   PropagateToMuon* muonPropagator = new PropagateToMuon(muonPropagatorPSet_);
   muonPropagator->init(iSetup);

   // vector to store outputs
   std::vector<float> outputME42;
   outputME42.reserve(src->size());
   std::auto_ptr<reco::CandidateBaseRefVector> output(new reco::CandidateBaseRefVector());

   for (size_t i=0, n=src->size(); i<n; ++i) {
      reco::CandidateBaseRef candRef = src->refAt(i);
      const reco::Candidate & cand = *candRef;
      if (candRef->eta() > 1.0 && candRef->eta() < 2.0) {
         TrajectoryStateOnSurface tsos = muonPropagator->extrapolate(cand);
         if (tsos.isValid()) {
            int result = isME42(tsos.globalPosition());
            outputME42.push_back(result);
            if (result) output->push_back(candRef);
         }
         else outputME42.push_back(0);
      }
      else {
         outputME42.push_back(0);
      }
   }


   // convert to ValueMap and store
   std::auto_ptr<ValueMap<float> > valMapME42(new ValueMap<float>());
   ValueMap<float>::Filler fillerME42(*valMapME42);
   fillerME42.insert(src, outputME42.begin(), outputME42.end());
   fillerME42.fill();
   iEvent.put(valMapME42,"isME42");

   iEvent.put(output);
   
   delete muonPropagator;
}

// ------------ method to determine if global point in ME4/2 region ------------
bool
MuonME42CandidateProducer::isME42(GlobalPoint point)
{
   return (point.phi()>75.*TMath::Pi()/180. &&
           point.phi()<125.*TMath::Pi()/180. &&
           point.eta()>1.2 && point.eta()<1.8);
}

// ------------ method called once each job just before starting event loop  ------------
void 
MuonME42CandidateProducer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
MuonME42CandidateProducer::endJob() {
}

// ------------ method called when starting to processes a run  ------------
void 
MuonME42CandidateProducer::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
MuonME42CandidateProducer::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
MuonME42CandidateProducer::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
MuonME42CandidateProducer::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
MuonME42CandidateProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(MuonME42CandidateProducer);
