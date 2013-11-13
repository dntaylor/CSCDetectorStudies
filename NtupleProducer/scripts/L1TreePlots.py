'''
Script to make plots using the L1Tree produced by the L1 Trigger DPG
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

tree  = ntuple_file.Get("l1NtupleProducer/L1Tree")

from plottingUtilities import *

if len(argv)>1:
   setSave('~/public_html/'+argv[2])

setn()

############################
#### Make plots ############
############################
selections = ["trPhi_02PI>80.*3.14159/180.&&trPhi_02PI<120*3.14159/180.","(trPhi_02PI>140.*3.14159/180.||trPhi_02PI<60.*3.14159/180.)"]
selections_sector = ["trSector==2","trSector!=2&&trEndcap==1"]
labels = ["ME4/2 Region","Non-ME4/2 Region"]
normalizations = [1./(40.*3.14159/180.),1./(280.*3.14159/180.)]
normalizations_sector = [1.,1./5.]

plot_n_hists(tree,"trNumLCTs",[6,0,6],"numLCTs",
             "trEta>1.25&&trEta<1.75&&trPt>0",
             selections,labels,normalizations,
             "Number of LCTs","LCTs")

plot_n_hists(tree,"trPt",[50,0,150],"pt_CSCTF",
             "trEta>1.25&&trEta<1.75&&trPt>0",
             selections,labels,normalizations,
             "CSCTF p_{T}","p_{T} (GeV/c)")

plot_n_hists(tree,"trPt",[50,0,150],"pt_CSCTF_3LCTto4LCT",
             "trEta>1.25&&trEta<1.75&&trPt>0"+
             "&&((trNumLCTs==4&&trME4ID!=0)"+
             "||(trNumLCTs==3&&trME4ID==0))",
             selections,labels,normalizations,
             "CSCTF p_{T}","p_{T} (GeV/c)")

plot_n_hists(tree,"trPt",[50,0,150],"pt_CSCTF_2LCTto3LCT",
             "trEta>1.25&&trEta<1.75&&trPt>0"+
             "&&((trNumLCTs==3&&trME4ID!=0)"+
             "||(trNumLCTs==2&&trME4ID==0))",
             selections,labels,normalizations,
             "CSCTF p_{T}","p_{T} (GeV/c)")


