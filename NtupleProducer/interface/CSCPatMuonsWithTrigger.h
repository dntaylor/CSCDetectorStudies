

#ifndef __CSCANALYSIS_CSCPATMUONSWITHTRIGGER_H__
#define __CSCANALYSIS_CSCPATMUONSWITHTRIGGER_H__

#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/Event.h"

#include "CSCPatMuonsWithTriggerDataFormat.h"
#include <TMath.h>

namespace CSCAnalysis
{
  class CSCPatMuonsWithTrigger
  {

  public:
    CSCPatMuonsWithTrigger();
    ~CSCPatMuonsWithTrigger();

    void Set(const edm::Event& e, const edm::InputTag& muons_);
    CSCPatMuonsWithTriggerDataFormat* getData() {return &pmwt_;}
    void Reset() {pmwt_.Reset();}

  private:
    CSCAnalysis::CSCPatMuonsWithTriggerDataFormat pmwt_;

  };
}


#endif
