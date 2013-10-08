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
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Common/interface/Ref.h"
#include "DataFormats/Common/interface/RefToBase.h"
#include "DataFormats/Common/interface/RefVector.h"

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
#include "DataFormats/RecoCandidate/interface/RecoChargedCandidate.h"

#include "TrackingTools/PatternTools/interface/Trajectory.h"
#include "TrackingTools/PatternTools/interface/TrajectoryMeasurement.h"
#include "TrackingTools/TrajectoryState/interface/TrajectoryStateOnSurface.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"

#include "MagneticField/Engine/interface/MagneticField.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "Geometry/Records/interface/GlobalTrackingGeometryRecord.h"
#include "Geometry/CommonDetUnit/interface/GlobalTrackingGeometry.h"
#include "Geometry/CommonDetUnit/interface/GeomDet.h"

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

      virtual bool isME42Trans(reco::TrackRef);
      virtual bool isME42HitPattern(reco::TrackRef);
      virtual bool isME42(GlobalPoint);
      virtual bool isCSCDetId(DetId);
      virtual void outputDetId(DetId);
      const reco::Vertex getPrimaryVertex(edm::Handle<reco::VertexCollection>&, edm::Handle<reco::BeamSpot>&);
      virtual bool isTightMuon(const reco::Muon&, edm::Handle<reco::VertexCollection>&);

      // ----------member data ---------------------------
      edm::InputTag tracks_;
      edm::InputTag vertices_;
      edm::InputTag beamspot_;
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
   tracks_(iConfig.getParameter<edm::InputTag>("TrackCollection")),
   vertices_(iConfig.getParameter<edm::InputTag>("VertexCollection")),
   beamspot_(iConfig.getParameter<edm::InputTag>("BeamSpot")),
   muonPropagatorPSet_(iConfig.getParameter<edm::ParameterSet>("MuonPropagator"))
{
   //register your products
   produces<edm::ValueMap<float>>("isME42");
   //produces<edm::RefToBaseVector<reco::RecoChargedCandidate>>("isTightMuon");
   //produces<edm::RefToBaseVector<reco::RecoChargedCandidate>>("isLooseMuon");
   //produces<edm::RefVector<std::vector<reco::RecoChargedCandidate>>>("ME42EtaRegion");
   //produces<edm::RefToBaseVector<reco::RecoChargedCandidate>>("ME42EtaRegion");

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

   // Handles to physics objects
   Handle<View<reco::RecoCandidate>> tracks;
   iEvent.getByLabel(tracks_,tracks);
   Handle<reco::VertexCollection> vertices;
   iEvent.getByLabel(vertices_,vertices);
   Handle<reco::BeamSpot> beamspot;
   iEvent.getByLabel(beamspot_,beamspot);

   iSetup.get<IdealMagneticFieldRecord>().get(theMGField_);
   iSetup.get<GlobalTrackingGeometryRecord>().get(theTrackingGeometry_);

   // need to initialize the muon propagator at each event
   PropagateToMuon* muonPropagator = new PropagateToMuon(muonPropagatorPSet_);
   muonPropagator->init(iSetup);

   //const reco::Vertex & vertex = getPrimaryVertex(vertices,beamspot);

   // vector to store outputs
   std::vector<float> outputME42;
   outputME42.reserve(tracks->size());
   //std::auto_ptr<RefToBaseVector<reco::RecoChargedCandidate>> outputTight(new RefToBaseVector<reco::RecoChargedCandidate>());
   //std::auto_ptr<RefToBaseVector<reco::RecoChargedCandidate>> outputLoose(new RefToBaseVector<reco::RecoChargedCandidate>());
   //std::auto_ptr< edm::RefVector< std::vector<reco::RecoChargedCandidate> > > outputME42EtaRegion( new edm::RefVector< std::vector<reco::RecoChargedCandidate> > );
   //std::auto_ptr< edm::RefToBaseVector<reco::RecoChargedCandidate> > outputME42EtaRegion( new edm::RefToBaseVector<reco::RecoChargedCandidate> );

   for (size_t i = 0, n = tracks->size(); i<n; ++i) {
      RefToBase<reco::RecoCandidate> trackRef = tracks->refAt(i);
      //const edm::Ref< std::vector<reco::RecoChargedCandidate> > CandRef = (*tracks)[i];
      const reco::RecoCandidate & track = *trackRef;
      // push variables
      //if (isTightMuon(muon,vertices)) outputTight->push_back(trackRef);
      //if (muon::isLooseMuon(muon)) outputLoose->push_back(trackRef);
      //outputME42.push_back(isME42Trans(track.track())); 
      
      // what follows is an attempt to adapt to using PropagateToMuon class
      if (trackRef->eta() > 1.0 && trackRef->eta() < 2.0) {
         TrajectoryStateOnSurface tsos = muonPropagator->extrapolate(track);
         if (tsos.isValid()) {
            //std::cout << "---------------------------------------" << std::endl
            //          << "propagation successful" << std::endl
            //          << "eta: " << tsos.globalPosition().eta() << " phi: " << tsos.globalPosition().phi() << std::endl
            //          << "x: " << tsos.globalPosition().x() << " y: " << tsos.globalPosition().y() << " z: " << tsos.globalPosition().z() << std::endl
            //          << "isME42: " << isME42(tsos.globalPosition()) << std::endl;
            outputME42.push_back(isME42(tsos.globalPosition()));
            //if (tsos.globalPosition().eta()>1.2 && tsos.globalPosition().eta()<1.8) outputME42EtaRegion->push_back(trackRef);
         }
         else outputME42.push_back(0);
      }
      else {
         //std::cout << "---------------------------------------" << std::endl
         //          << "propagation failed" << std::endl;
         outputME42.push_back(0);
      }
   }


   // convert to ValueMap and store
   std::auto_ptr<ValueMap<float> > valMapME42(new ValueMap<float>());
   ValueMap<float>::Filler fillerME42(*valMapME42);
   fillerME42.insert(tracks, outputME42.begin(), outputME42.end());
   fillerME42.fill();
   iEvent.put(valMapME42,"isME42");

   //iEvent.put(outputTight,"isTightMuon");
   //iEvent.put(outputLoose,"isLooseMuon");
   //iEvent.put(outputME42EtaRegion,"ME42EtaRegion");
   
   delete muonPropagator;
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
MuonME42CandidateProducer::isME42Trans(reco::TrackRef track)
{
   // hacked solution
   reco::TransientTrack transTrack(track,&*theMGField_,theTrackingGeometry_);
   TrajectoryStateOnSurface outerTSOS = transTrack.outermostMeasurementState();
   GlobalPoint oldPoint1 = outerTSOS.globalPosition();
   GlobalPoint oldPoint2 = outerTSOS.globalPosition();
   if (oldPoint1.z()>0) {
      for (int j = 0; j<10; j++) {
         GlobalPoint newPoint1(oldPoint1.x(),oldPoint1.y(),1012.5);
         GlobalPoint newPoint2(oldPoint2.x(),oldPoint2.y(),1037.5);
         TrajectoryStateClosestToPoint traj1 = transTrack.trajectoryStateClosestToPoint(newPoint1);
         TrajectoryStateClosestToPoint traj2 = transTrack.trajectoryStateClosestToPoint(newPoint2);
         if (traj1.isValid() && traj2.isValid()) {
            GlobalPoint closestPoint1 = traj1.position();
            GlobalPoint closestPoint2 = traj2.position();
            bool closest1 = fabs(closestPoint1.z()-1012.5)<1.0;
            bool closest2 = fabs(closestPoint2.z()-1037.5)<1.0;
            if (closest1 || closest2) {
               if (isME42HitPattern(track) || isME42(closestPoint1) || isME42(closestPoint2)) { 
                  std::cout << "-----------" << std::endl
                            << "ME4/2 hit pattern?: " << isME42HitPattern(track) << std::endl
                            << "isME42: " << isME42(closestPoint1) << " " << isME42(closestPoint2) << std::endl
                            << "outerEta: " << (*track).outerEta() << " outerPhi: " << (*track).outerPhi() << std::endl
                            << "outerX: " << (*track).outerX() << " outerY: " << (*track).outerY() << " outerZ: " << (*track).outerZ() << std::endl
                            << "pointEta: " << closestPoint1.eta() << " pointPhi: " << closestPoint1.phi() << std::endl
                            << "pointX: " << closestPoint1.x() << " pointY: " << closestPoint1.y() << " pointZ: " << closestPoint1.z() << std::endl
                            << "pointEta: " << closestPoint2.eta() << " pointPhi: " << closestPoint2.phi() << std::endl
                            << "pointX: " << closestPoint2.x() << " pointY: " << closestPoint2.y() << " pointZ: " << closestPoint2.z() << std::endl;
               }
               return closest1 ? isME42(closestPoint1) : isME42(closestPoint2);
            }
            oldPoint1 = closestPoint1;
            oldPoint2 = closestPoint2;
         }
      }
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
   //std::cout << "Number muon missing: " << numMissing << std::endl;
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

// ------------ method to determine if DetId is CSCDetId -----------------
bool
MuonME42CandidateProducer::isCSCDetId(DetId id)
{
   DetId::Detector det = id.det();
   int subdet = id.subdetId();
   return (det==2 && subdet==2);
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
MuonME42CandidateProducer::isTightMuon(const reco::Muon& muon, edm::Handle<reco::VertexCollection> &vertices)
{
   // iterate over the vertex collection
   if (vertices.isValid()) {
      for (reco::VertexCollection::const_iterator vertex = vertices->begin(); vertex != vertices->end(); ++vertex) {
         if (vertex->isValid() && !vertex->isFake()) {
            if (muon::isTightMuon(muon,*vertex)) return true;   
         }
      }
   }

   // beamspot check
   return false;
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
