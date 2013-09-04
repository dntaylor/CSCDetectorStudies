// -*- C++ -*-
//
// Package:    MuonME42CandidateProducer
// Class:      MuonME42CandidateProducer
// 
/**\class MuonME42CandidateProducer MuonME42CandidateProducer.cc CSCDetectorStudies/MuonME42CandidateProducer/src/MuonME42CandidateProducer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
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
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/ValueMap.h"

#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/MuonDetId/interface/CSCDetId.h"

#include "TrackingTools/TransientTrack/interface/TrackTransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"

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

      virtual bool isME42(reco::TrackRef, TransientTrackBuilder);
      virtual bool isME42(GlobalPoint);
      // ----------member data ---------------------------
      edm::InputTag muons_;
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
   muons_(iConfig.getParameter<edm::InputTag>("src"))
{
   //register your products
/* Examples
   produces<ExampleData2>();

   //if do put with a label
   produces<ExampleData2>("label");
 
   //if you want to put into the Run
   produces<ExampleData2,InRun>();
*/
   produces<edm::ValueMap<float>>();
   //now do what ever other initialization is needed
  
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
/* This is an event example
   //Read 'ExampleData' from the Event
   Handle<ExampleData> pIn;
   iEvent.getByLabel("example",pIn);

   //Use the ExampleData to create an ExampleData2 which 
   // is put into the Event
   std::auto_ptr<ExampleData2> pOut(new ExampleData2(*pIn));
   iEvent.put(pOut);
*/

/* this is an EventSetup example
   //Read SetupData from the SetupRecord in the EventSetup
   ESHandle<SetupData> pSetup;
   iSetup.get<SetupRecord>().get(pSetup);
*/

   // Handles to physics objects
   Handle<reco::MuonCollection> muons;
   iEvent.getByLabel(muons_,muons);

   // handle to transient track builder
   edm::ESHandle<TransientTrackBuilder> transTrackBuilder;
   iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",transTrackBuilder);

   // vector to store outputs
   std::vector<float> output;
   output.reserve(muons->size());

   for (reco::MuonCollection::const_iterator muon = muons->begin(); muon != muons->end(); ++muon) {
      if (muon->isStandAloneMuon()) {
         reco::TrackRef track = muon->outerTrack();
         output.push_back(isME42(track,*transTrackBuilder));
      }
      else { output.push_back(0); }
   }

   // convert to ValueMap and store
   std::auto_ptr<ValueMap<float> > valMap(new ValueMap<float>());
   ValueMap<float>::Filler filler(*valMap);
   filler.insert(muons, output.begin(), output.end());
   filler.fill();
   iEvent.put(valMap);
 
}

// ------------ method to determine if muon is in ME4/2 region ---------
bool
MuonME42CandidateProducer::isME42(reco::TrackRef track, TransientTrackBuilder builder)
{
   // build transient track
   reco::TransientTrack transTrack = builder.build(track);
   // create global point in center of ME42 region
   // get geometry 
   edm::ESHandle<GlobalTrackingGeometry> theGeometry = builder.trackingGeometry();
   // create DetID for ME+4/2
   std::vector<CSCDetId> ME42Chambers;
   ME42Chambers.reserve(5);
   for (int id=8; id<13; id++) { ME42Chambers.push_back(CSCDetId(1,4,2,id)); }
   GlobalPoint point(1.0,1.0,1.0);
   // get track position closest to point (in 3d space?)
   TrajectoryStateClosestToPoint trajectory = transTrack.trajectoryStateClosestToPoint(point);
   // check if point is in ME42 region
   return isME42(trajectory.position());
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
