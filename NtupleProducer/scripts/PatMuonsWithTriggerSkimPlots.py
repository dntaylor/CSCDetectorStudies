'''
Script to make plots using the RecoTree produced by my custom CSCAnalysis code
'''

#######################
### GET EVERYTHING ####
#######################
from sys import argv, stdout, stderr

import ROOT
from array import array


#######################
######## STYLE ########
#######################
ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

#######################
######## File #########
#######################
Infile = argv[1]
ntuple_file = ROOT.TFile(Infile)

tree  = ntuple_file.Get("skim/RecoTree")

from plottingUtilities import *

if len(argv)>1:
   setSave('~/public_html/'+argv[2])

setn()

############################
#### Make plots ############
############################
selections = ["muPhi>80.*3.14159/180.&&muPhi<120*3.14159/180.","(muPhi>140.*3.14159/180.||muPhi<60.*3.14159/180.)"]
labels = ["ME4/2 Region","Non-ME4/2 Region"]
normalizations = [1./(40.*3.14159/180.),1./(280.*3.14159/180.)]

#plot_n_hists(tree,"(muL1pt-muPt)/muPt",[164,-2,80],"ptResolution",
#             "muEta>1.25&&muEta<1.75&&muL1pt>0",
#             selections,labels,normalizations,
#             "CSCTF p_{T} Resolution","(L1p_{T}-p_{T})/p_{T}")
#
#plot_n_hists(tree,"(muL1pt-muPt)/muPt",[164,-2,80],"ptResolution_2LCTto3LCT",
#             "muEta>1.25&&muEta<1.75&&muL1pt>0"
#             +"&&((muNumberOfMatchedStations==2&&muLastStation!=4)"
#             +"||(muNumberOfMatchedStations==3&&muLastStation==4))",
#             selections,labels,normalizations,
#             "CSCTF p_{T} Resolution","(L1p_{T}-p_{T})/p_{T}")
#
#plot_n_hists(tree,"(muL1pt-muPt)/muPt",[164,-2,80],"ptResolution_3LCTto4LCT",
#             "muEta>1.25&&muEta<1.75&&muL1pt>0"
#             +"&&((muNumberOfMatchedStations==3&&muLastStation!=4)"
#             +"||(muNumberOfMatchedStations==4&&muLastStation==4))",
#             selections,labels,normalizations,
#             "CSCTF p_{T} Resolution","(L1p_{T}-p_{T})/p_{T}")

plot_n_hists(tree,"(muStandAlonePt-muPt)/muPt",[44,-2,20],"standalonePtResolution",
             "muEta>1.25&&muEta<1.75&&muStandAlonePt>0",
             selections,labels,normalizations,
             "Standalone p_{T} Resolution","(Standalone p_{T}-p_{T})/p_{T}")

plot_n_hists(tree,"(muStandAlonePt-muPt)/muPt",[44,-2,20],"standalonePtResolution_2LCTto3LCT",
             "muEta>1.25&&muEta<1.75&&muStandAlonePt>0"
             +"&&((muNumberOfMatchedStations==2&&muLastStation!=4)"
             +"||(muNumberOfMatchedStations==3&&muLastStation==4))",
             selections,labels,normalizations,
             "Standalone p_{T} Resolution","(Standalone p_{T}-p_{T})/p_{T}")

plot_n_hists(tree,"(muStandAlonePt-muPt)/muPt",[44,-2,20],"standalonePtResolution_3LCTto4LCT",
             "muEta>1.25&&muEta<1.75&&muStandAlonePt>0"
             +"&&((muNumberOfMatchedStations==3&&muLastStation!=4)"
             +"||(muNumberOfMatchedStations==4&&muLastStation==4))",
             selections,labels,normalizations,
             "Standalone p_{T} Resolution","(Standalone p_{T}-p_{T})/p_{T}")

#plot_hists_with_ratio(tree,"muL1pt",[75,0,150],"ptWithRatio",
#                      "muEta>1.25&&muEta<1.75&&muL1pt>0",
#                      selections,labels,normalizations,
#                      "CSCTF p_{T}","p_{T} (GeV/c)")

#L1ptValues = [2,2.5,3,3.5,4,4.5,5,6,7,8,10,12,14,16,18,20,25,30,35,40,45,50,60,70,80,90,100,120,140]
#plot_hists_with_ratio(tree,"muL1pt",[75,0,150],"ptWithRatio",
#                      "muEta>1.25&&muEta<1.75&&muL1pt>0",
#                      selections,labels,normalizations,
#                      "CSCTF p_{T}","p_{T} (GeV/c)")

#L1ptValues = [2,2.5,3,3.5,4,4.5,5,6,7,8,10,12,14,16,18,20,25,30,35,40,45,50,60,70,80,90,100,120,140]
#L1ptBins = [[2,5],[5,8],[8,20],[20,50],[50,100],[100,140]]
#for ptBins in L1ptBins:
#    plot_n_hists(tree,"(muL1pt-muPt)/muPt",[44,-2,20],"ptResolution_%0.1f_%0.1f" % (ptBins[0],ptBins[1]),
#                 "muEta>1.25&&muEta<1.75&&muL1pt>0"
#                 +"&&muL1pt>=%0.1f&&muL1pt<=%0.1f" % (ptBins[0],ptBins[1]),
#                 selections,labels,normalizations,
#                 "CSCTF p_{T} Resolution (L1p_{T}=[%0.1f,%0.1f])" % (ptBins[0],ptBins[1]),"(L1p_{T}-p_{T})/p_{T}")
#
#    plot_n_hists(tree,"(muL1pt-muPt)/muPt",[44,-2,20],"ptResolution_2LCTto3LCT_%0.1f_%0.1f" % (ptBins[0],ptBins[1]),
#                 "muEta>1.25&&muEta<1.75&&muL1pt>0"
#                 +"&&((muNumberOfMatchedStations==2&&muLastStation!=4)"
#                 +"||(muNumberOfMatchedStations==3&&muLastStation==4))"
#                 +"&&muL1pt>=%0.1f&&muL1pt<=%0.1f" % (ptBins[0],ptBins[1]),
#                 selections,labels,normalizations,
#                 "CSCTF p_{T} Resolution (L1p_{T}=[%0.1f,%0.1f])" % (ptBins[0],ptBins[1]),"(L1p_{T}-p_{T})/p_{T}")
#
#    plot_n_hists(tree,"(muL1pt-muPt)/muPt",[44,-2,20],"ptResolution_3LCTto4LCT_%0.1f_%0.1f" % (ptBins[0],ptBins[1]),
#                 "muEta>1.25&&muEta<1.75&&muL1pt>0"
#                 +"&&((muNumberOfMatchedStations==3&&muLastStation!=4)"
#                 +"||(muNumberOfMatchedStations==4&&muLastStation==4))"
#                 +"&&muL1pt>=%0.1f&&muL1pt<=%0.1f" % (ptBins[0],ptBins[1]),
#                 selections,labels,normalizations,
#                 "CSCTF p_{T} Resolution (L1p_{T}=[%0.1f,%0.1f])" % (ptBins[0],ptBins[1]),"(L1p_{T}-p_{T})/p_{T}")

