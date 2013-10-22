#include "FWCore/Framework/interface/MakerMacros.h"

/*
  This is an example of using the PatMuonAnalyzer class to do a simple analysis of muons 
  using the full framework and cmsRun. You can find the example to use this code in 
  PhysicsTools/PatExamples/test/....
*/
#include "PhysicsTools/UtilAlgos/interface/EDAnalyzerWrapper.h"
#include "CSCDetectorStudies/L1CSCTFMethods/interface/L1CSCTFMethods.h"

typedef edm::AnalyzerWrapper<L1CSCTFMethods> L1CSCTFMethodsPlugin;
DEFINE_FWK_MODULE(L1CSCTFMethodsPlugin);
