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
#include "DataFormats/Common/interface/Ref.h"
#include "DataFormats/Common/interface/RefToBase.h"

#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/MuonDetId/interface/CSCDetId.h"
#include "DataFormats/MuonDetId/interface/DTChamberId.h"
#include "DataFormats/MuonDetId/interface/RPCDetId.h"
#include "DataFormats/TrackReco/interface/HitPattern.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"

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
      const reco::Vertex getPrimaryVertex(edm::Handle<reco::VertexCollection>&,edm::Handle<reco::BeamSpot>&);
      virtual bool isTightMuon(const reco::Muon&, const reco::Vertex&);
      virtual bool isLooseMuon(const reco::Muon&);
      virtual bool isTagMuon(const reco::Muon&, const reco::Vertex&);
      virtual bool isProbeMuon(const reco::Muon&, const reco::Vertex&);
      // ----------member data ---------------------------
      edm::InputTag muons_;
      edm::InputTag vertices_;
      edm::InputTag beamspot_;
      edm::ParameterSet serviceProxyParameters_;
      edm::ParameterSet refitterParameters_;
      edm::ParameterSet trackLoaderParameters_;
      edm::ParameterSet trackBuilderParameters_;

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
   muons_(iConfig.getParameter<edm::InputTag>("MuonCollection")),
   vertices_(iConfig.getParameter<edm::InputTag>("VertexCollection")),
   beamspot_(iConfig.getParameter<edm::InputTag>("BeamSpot")),
   serviceProxyParameters_(iConfig.getParameter<edm::ParameterSet>("ServiceParameters")),
   refitterParameters_(iConfig.getParameter<edm::ParameterSet>("RefitterParameters")),
   trackLoaderParameters_(iConfig.getParameter<edm::ParameterSet>("TrackLoaderParameters")),
   trackBuilderParameters_(iConfig.getParameter<edm::ParameterSet>("STATrajBuilderParameters"))
{
   //register your products
   produces<edm::ValueMap<float>>("isME42");
   produces<edm::RefToBaseVector<reco::Muon>>("isTightMuon");
   produces<edm::RefToBaseVector<reco::Muon>>("isLooseMuon");
   produces<reco::MuonCollection>("isTagMuon");
   produces<reco::MuonCollection>("isProbeMuon");
   //now do what ever other initialization is needed
   muonService_ = new MuonServiceProxy(serviceProxyParameters_);
   refitter_ = new StandAloneMuonRefitter(refitterParameters_, muonService_);
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
   Handle<View<reco::Muon>> muons;
   iEvent.getByLabel(muons_,muons);
   Handle<reco::VertexCollection> vertices;
   iEvent.getByLabel(vertices_,vertices);
   Handle<reco::BeamSpot> beamspot;
   iEvent.getByLabel(beamspot_,beamspot);

   const reco::Vertex & vertex = getPrimaryVertex(vertices,beamspot);

   // update muon service
   muonService_->update(iSetup);

   // vector to store outputs
   std::vector<float> outputME42;
   outputME42.reserve(muons->size());
   std::auto_ptr<RefToBaseVector<reco::Muon>> outputTight(new RefToBaseVector<reco::Muon>());
   std::auto_ptr<RefToBaseVector<reco::Muon>> outputLoose(new RefToBaseVector<reco::Muon>());
   std::auto_ptr<reco::MuonCollection> outputTag(new reco::MuonCollection());
   std::auto_ptr<reco::MuonCollection> outputProbe(new reco::MuonCollection());

         //bool isME42Hp = isME42HitPattern(track);
         //if (wantOutput(track->outerDetId())) {
         //if (output.back() || isME42Alt(track) || isME42Hp) {
         //   std::cout << "------------------------------" << std::endl;
         //   outputDetId(track->outerDetId());
         //   std::cout << std::endl;
         //   std::cout << "eta: " << muon->eta() << " phi: " << muon->phi() << std::endl;
         //   std::cout << "outerEta: " << track->outerEta() << " outerPhi: " << track->outerPhi() << std::endl;
         //   std::cout << "outerX: " << track->outerX() << " outerY: " << track->outerY() << " outerZ(): " << track->outerZ() << std::endl;
         //   std::cout << "isME42: " << output.back() << " isME42Alt: " << isME42Alt(track) << " isME42Hp: " << isME42Hp << std::endl;
         //}

   for (size_t i = 0, n = muons->size(); i<n; ++i) {
      RefToBase<reco::Muon> muonRef = muons->refAt(i);
      const reco::Muon & muon = *muonRef;
      // push variables
      if (isTightMuon(muon,vertex)) outputTight->push_back(muonRef);
      if (isLooseMuon(muon)) outputLoose->push_back(muonRef);
      if (isTagMuon(muon,vertex)) outputTag->push_back(muon);
      if (isProbeMuon(muon,vertex)) outputProbe->push_back(muon);
      if (muon.isStandAloneMuon()) {
         reco::TrackRef track = muon.outerTrack();
         // SWITCH from isME42Alt to isME42 to try track refitter
         outputME42.push_back(isME42Alt(track));
      }
      else { outputME42.push_back(0); }
   }

   // convert to ValueMap and store
   std::auto_ptr<ValueMap<float> > valMapME42(new ValueMap<float>());
   ValueMap<float>::Filler fillerME42(*valMapME42);
   fillerME42.insert(muons, outputME42.begin(), outputME42.end());
   fillerME42.fill();
   iEvent.put(valMapME42,"isME42");
 
   iEvent.put(outputTight,"isTightMuon");
   iEvent.put(outputLoose,"isLooseMuon");
   iEvent.put(outputTag,"isTagMuon");
   iEvent.put(outputProbe,"isProbeMuon");
}

// ------------ method to output detid regardless of type ---------------
void 
MuonME42CandidateProducer::outputDetId(DetId id)
{
   DetId::Detector det = id.det();
   int subdet = id.subdetId();
   if (det==2 && subdet==1) {
      std::cout << (DTChamberId)id;
   }
   else if (det==2 && subdet==2) {
      std::cout << (CSCDetId)id;
   }
   else if (det==2 && subdet==3) {
      std::cout << (RPCDetId)id;
   }
}

// ------------ method to determing if muon in ME4/2 with trajectory ----------
bool
MuonME42CandidateProducer::isME42(reco::TrackRef track)
{
   // take seed trajectory
   Trajectory seedTraj(*(track->seedRef()),track->seedDirection());
   //Trajectory seedTraj(*(track->seedRef()));
   // reun refit
   std::pair<bool,Trajectory> refitResult = refitter_->refit(seedTraj);
   if (refitResult.first) {
      Trajectory traj = refitResult.second;
      // get last measurement in trajectory
      TrajectoryMeasurement lastMeas = traj.lastMeasurement();
      // get forward predicted state from this measurement
      TrajectoryStateOnSurface fwdPredState = lastMeas.forwardPredictedState();
      // get global point of forward predicted state
      GlobalPoint fwdGlobalPoint = fwdPredState.globalPosition();
      // Test to see if corresponds to ME4 Z position, if not, propgate to next layer
      //if (fwdGlobalPoint.z()>1012.0) {  }
      //else {  }
      return isME42(fwdGlobalPoint);
   }
   return 0;
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

// ------------ method to get primary vertex ----------------
const reco::Vertex 
MuonME42CandidateProducer::getPrimaryVertex(edm::Handle<reco::VertexCollection> &vertices, edm::Handle<reco::BeamSpot> &beamSpot)
{
   reco::Vertex::Point posVertex;
   reco::Vertex::Error errVertex;

   bool hasPrimaryVertex = false;

   // iterate over the vertex collection
   if (vertices.isValid()) {
      for (reco::VertexCollection::const_iterator vertex = vertices->begin(); vertex != vertices->end(); ++vertex) {
         if (vertex->isValid() && !vertex->isFake()) {
            posVertex = vertex->position();
            errVertex = vertex->error();
            hasPrimaryVertex = true;
         }
      }
   }

   // if no valid vertex, use beam spot
   if (!hasPrimaryVertex) {
      posVertex = beamSpot->position();
      errVertex(0,0) = beamSpot->BeamWidthX();
      errVertex(1,1) = beamSpot->BeamWidthY();
      errVertex(2,2) = beamSpot->sigmaZ();
   }

   const reco::Vertex primaryVertex(posVertex,errVertex);

   return primaryVertex;
}

// ------------ method to determine if tight muon -------------
bool
MuonME42CandidateProducer::isTightMuon(const reco::Muon& muon, const reco::Vertex& vertex)
{
   //return muon::isTightMuon(muon,vertex)
   // what follows is a modified isTightMuon while i fix the probe selections to include vertex restrictions as well
   if (!muon.isGlobalMuon()) return false;
   bool type = (muon.isGlobalMuon() && muon.isPFMuon());
   bool global = (muon.globalTrack()->normalizedChi2() < 10. && muon.globalTrack()->hitPattern().numberOfValidMuonHits() > 0);
   bool inner = (muon.innerTrack()->hitPattern().numberOfValidPixelHits() > 0 && muon.innerTrack()->hitPattern().trackerLayersWithMeasurement() > 5);
   bool stations = (muon.numberOfMatchedStations() > 1);
   // for this, i need to remake my probe collection as well with the vertex cut, otherwise the dz is going to cause way too many fails
   bool vert = (fabs(muon.muonBestTrack()->dxy(vertex.position())) < 0.2);// && fabs(muon.muonBestTrack()->dz(vertex.position())) < 0.5);
   return (type && global && inner && stations && vert);
}

// ------------ method to determine if loose muon -------------
bool 
MuonME42CandidateProducer::isLooseMuon(const reco::Muon& muon)
{
   return muon::isLooseMuon(muon);
}

// ------------ method to determine if it is a tag muon ------------
bool
MuonME42CandidateProducer::isTagMuon(const reco::Muon& muon, const reco::Vertex& vertex)
{
   return (isTightMuon(muon,vertex));
}

// ------------ method to determine if it is a probe muon ------------
bool
MuonME42CandidateProducer::isProbeMuon(const reco::Muon& muon, const reco::Vertex& vertex)
{
   bool standalone = (muon.isStandAloneMuon());
   bool vert = (fabs(muon.muonBestTrack()->dxy(vertex.position())) < 0.2 && fabs(muon.muonBestTrack()->dz(vertex.position())) < 0.5);
   return (standalone && vert);
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
