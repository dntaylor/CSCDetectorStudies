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
#include "DataFormats/MuonDetId/interface/DTChamberId.h"
#include "DataFormats/MuonDetId/interface/RPCDetId.h"
#include "DataFormats/TrackReco/interface/HitPattern.h"

#include "TrackingTools/PatternTools/interface/Trajectory.h"
#include "TrackingTools/PatternTools/interface/TrajectoryMeasurement.h"
#include "TrackingTools/TrajectoryState/interface/TrajectoryStateOnSurface.h"

#include "RecoMuon/TrackingTools/interface/MuonServiceProxy.h"
#include "RecoMuon/TrackingTools/interface/MuonTrackFinder.h"
#include "RecoMuon/TrackingTools/interface/MuonTrackLoader.h"
#include "RecoMuon/StandAloneTrackFinder/interface/StandAloneMuonRefitter.h"
#include "RecoMuon/StandAloneTrackFinder/interface/StandAloneTrajectoryBuilder.h"

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

      virtual bool isME42(reco::TrackRef);
      virtual bool isME42HitPattern(reco::TrackRef);
      virtual bool isME42(GlobalPoint);
      virtual bool isME42Alt(reco::TrackRef);
      virtual bool isCSCDetId(DetId);
      virtual bool wantOutput(DetId);
      virtual void outputDetId(DetId);
      // ----------member data ---------------------------
      edm::InputTag muons_;
      edm::ParameterSet serviceProxyParameters_;
      edm::ParameterSet refitterParameters_;
      edm::ParameterSet trackLoaderParameters_;
      edm::ParameterSet trajectoryBuilderParameters_;

      MuonServiceProxy* muonService_;
      StandAloneMuonRefitter* refitter_;
      MuonTrackLoader* trackLoader_;
      MuonTrajectoryBuilder* trajectoryBuilder_;
      MuonTrackFinder* trackFinder_;
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
   muons_(iConfig.getParameter<edm::InputTag>("src")),
   serviceProxyParameters_(iConfig.getParameter<edm::ParameterSet>("ServiceParameters")),
   refitterParameters_(iConfig.getParameter<edm::ParameterSet>("RefitterParameters")),
   trackLoaderParameters_(iConfig.getParameter<edm::ParameterSet>("TrackLoaderParameters")),
   trajectoryBuilderParameters_(iConfig.getParameter<edm::ParameterSet>("STATrajBuilderParameters"))
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
   muonService_ = new MuonServiceProxy(serviceProxyParameters_);
   refitter_ = new StandAloneMuonRefitter(refitterParameters_, muonService_);
   trackLoader_ = new MuonTrackLoader(trackLoaderParameters_, muonService_);
   trajectoryBuilder_ = new StandAloneMuonTrajectoryBuilder(trajectoryBuilderParameters_, muonService_);
   trackFinder_ = new MuonTrackFinder(trajectoryBuilder_, trackLoader_);
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
   std::cout << "getting physics objects" << std::endl;
   Handle<reco::MuonCollection> muons;
   iEvent.getByLabel(muons_,muons);

   // update muon service
   std::cout << "updating muon service" << std::endl;
   muonService_->update(iSetup);
   std::cout << "setting event in traj builder" << std::endl;
   trajectoryBuilder_->setEvent(iEvent);

   // vector to store outputs
   std::vector<float> output;
   output.reserve(muons->size());

   for (reco::MuonCollection::const_iterator muon = muons->begin(); muon != muons->end(); ++muon) {
      if (muon->isStandAloneMuon()) {
         reco::TrackRef track = muon->outerTrack();
         output.push_back(isME42(track));
         bool isME42Hp = isME42HitPattern(track);
         //if (wantOutput(track->outerDetId())) {
         if (output.back() || isME42Alt(track) || isME42Hp) {
            std::cout << "------------------------------" << std::endl;
            outputDetId(track->outerDetId());
            std::cout << std::endl;
            std::cout << "eta: " << muon->eta() << " phi: " << muon->phi() << std::endl;
            std::cout << "outerEta: " << track->outerEta() << " outerPhi: " << track->outerPhi() << std::endl;
            std::cout << "outerX: " << track->outerX() << " outerY: " << track->outerY() << " outerZ(): " << track->outerZ() << std::endl;
            std::cout << "isME42: " << output.back() << " isME42Alt: " << isME42Alt(track) << " isME42Hp: " << isME42Hp << std::endl;
         }
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

// ------------ method to output detid regardless of type ---------------
void 
MuonME42CandidateProducer::outputDetId(DetId id)
{
   DetId::Detector det = id.det();
   int subdet = id.subdetId();
   if (det==2 && subdet==1) {
      std::cout << (DTChamberId)id << std::endl;
   }
   else if (det==2 && subdet==2) {
      std::cout << (CSCDetId)id << std::endl;
   }
   else if (det==2 && subdet==3) {
      std::cout << (RPCDetId)id << std::endl;
   }
}

// ------------ method to determing if muon in ME4/2 with trajectory ----------
bool
MuonME42CandidateProducer::isME42(reco::TrackRef track)
{
   // take seed trajectory
   //Trajectory seedTraj(*(track->seedRef()),track->seedDirection());
   //Trajectory seedTraj(*(track->seedRef()));
   // reun refit
   //std::pair<bool,Trajectory> refitResult = refitter_->refit(seedTraj);
   // run trajectorBuilder
   std::cout << "building trajectories" << std::endl;
   std::vector<Trajectory*> trajs = trajectoryBuilder_->trajectories(*(track->seedRef()));
   //if (refitResult.first) {
   //Trajectory traj = refitResult.second;
   // iterate over trajectories
   std::cout << "getting trajectories" << std::endl;
   if (trajs.size()==0) return 0;
   Trajectory* traj = trajs[0];
   // get last measurement in trajectory
   std::cout << "get last measurement" << std::endl;
   TrajectoryMeasurement lastMeas = traj->lastMeasurement();
   // get forward predicted state from this measurement
   std::cout << "get TSOS" << std::endl;
   TrajectoryStateOnSurface fwdPredState = lastMeas.forwardPredictedState();
   // get global point of forward predicted state
   std::cout << "get global point" << std::endl;
   GlobalPoint fwdGlobalPoint = fwdPredState.globalPosition();
   // Test to see if corresponds to ME4 Z position, if not, propgate to next layer
   //if (fwdGlobalPoint.z()>1012.0) {  }
   //else {  }
   std::cout << "check is ME42" << std::endl;
   return isME42(fwdGlobalPoint);
   //}
   //return 0;
}

// ------------ method to determine if muon is in ME4/2 region with hitpatter --------
bool
MuonME42CandidateProducer::isME42HitPattern(reco::TrackRef track)
{
   // Hit pattern structure
   // - consists of a 10 bit uint32
   // bit # | val  | meaning
   // 10    | 0    | muon (0)
   // 9-7   | 010  | CSC (2)
   // 6-3   | 1101 | 4*(station-1)+(ring-1) (ME4/2: 13)
   // 2     |      | rphi/stereo (0/1)
   // 1-0   |      | valid/missing/inactive/bad (0/1/2/3)
   reco::HitPattern hp = track->hitPattern();
   // we want to iterate over patterns, and check if it is an ME4/2
   int result = 0;
   int numMissing = 0;
   for (int i = 0; i<hp.numberOfHits(); i++) {
      uint32_t pattern = hp.getHitPattern(i);
      if (hp.muonCSCHitFilter(pattern)) {
         if (hp.type_2_HitFilter(pattern)) { numMissing++; }
         if (hp.getMuonStation(pattern)==4 && hp.getCSCRing(pattern)==2) { result = 1; }
      }
   }
   std::cout << "Number muon missing: " << numMissing << std::endl;
   return result;
}

// ------------ method to determine if global point in ME4/2 region ------------
bool
MuonME42CandidateProducer::isME42(GlobalPoint point)
{
   return (point.phi()>75.*TMath::Pi()/180. &&
           point.phi()<125.*TMath::Pi()/180. &&
           point.eta()>1.2 && point.eta()<1.8);
}

// ------------ method to see if track in ME4/2 region ------------
bool
MuonME42CandidateProducer::isME42Alt(reco::TrackRef track)
{
   return (track->outerPhi()>75.*TMath::Pi()/180. &&
           track->outerPhi()<125.*TMath::Pi()/180. &&
           track->outerEta()>1.2 && track->outerEta()<1.8);
}

// ------------ method to determine if DetId is CSCDetId -----------------
bool
MuonME42CandidateProducer::isCSCDetId(DetId id)
{
   DetId::Detector det = id.det();
   int subdet = id.subdetId();
   return (det==2 && subdet==2);
}

// ------------ method to decide to output properties ------------------
bool
MuonME42CandidateProducer::wantOutput(DetId id)
{
   if (isCSCDetId(id)) {
      CSCDetId cscId = (CSCDetId)id;
      return (cscId.endcap()==1 && cscId.station()==4 && cscId.ring()==2);
   }
   return 0;
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
