'''
Script to compare L1 and reco resoltions

Author: D. Taylor

Usage:

E.G.

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
if len(argv) < 2:
   print 'Usage:python compareResolutionL1CSCTF.py L1NTuple.root label[optional]'
   exit()

Infile = argv[1]
ntuple_file = ROOT.TFile(Infile)

####################################
####### LABEL & SAVE WHERE #########
####################################

if len(argv)>1:
   saveWhere='~/public_html/'+argv[2]
else:
   saveWhere='~/public_html/'

######################################
####### Get NTuples ##################
######################################
tree  = ntuple_file.Get("skim/RecoTree")

canvas = ROOT.TCanvas("asdf", "adsf", 800, 600)

################################################################################
#  make_plot uses draw() method to draw                                        #
################################################################################

def make_plot(tree, variable, selection, binning, color=ROOT.EColor.kBlue, markerStyle=20, xaxis='', title='', calFactor=1):
    ''' Plot a variable using draw and return the histogram '''
    draw_string = "%s * %0.2f>>htemp(%s)" % (variable, calFactor, ", ".join(str(x) for x in binning))
    print draw_string
    tree.Draw(draw_string, selection, "goff")
    output_histo = ROOT.gDirectory.Get("htemp").Clone()
    output_histo.GetXaxis().SetTitle(xaxis)
    output_histo.SetTitle(title)
    output_histo.SetLineColor(color)
    output_histo.SetMarkerStyle(markerStyle)
    output_histo.SetMarkerColor(color)
    return output_histo


#################################################################################
#     plot_n_hists method will be used to draw resolutions                      #
#################################################################################
def plot_n_hists(ntuple, varName, binning, filename, selection, selections=[""], labels=[""], normalization=[1], title='', xaxis=''):
    ''' Save a rate Plot '''

    plots = []
    colors = [ROOT.EColor.kRed,ROOT.EColor.kBlue,ROOT.EColor.kGreen]
    styles = [22,21,20]
    for i in range(len(selections)):
        selection_temp = selection
        if selections[i]!="":
          selection_temp += "&&"+selections[i]
        plots.append(make_plot(
            ntuple, varName,
            selection_temp,
            binning,
            colors[i],styles[i],
            '',''
            )
        )

    canvas.SetLogy()
    legend = ROOT.TLegend(0.7, 0.78, 0.89, 0.89, "", "brNDC")
    legend.SetFillColor(ROOT.EColor.kWhite)
    legend.SetBorderSize(1)
    for i in range(len(selections)):
        if i == 0:
            plots[i].SetTitle(title)
            plots[i].GetXaxis().SetTitle(xaxis)
            plots[i].GetYaxis().SetTitle("Events")
            #plots[i].Scale(1)
            size = plots[i].GetEntries()
            #plots[i].Scale(normalization[i])
            plots[i].Draw('ph')
        else:
            curSize = plots[i].GetEntries()
            plots[1].Scale(size/curSize)
            #plots[i].Scale(normalization[i])
            plots[i].Draw('phsame')
        legend.AddEntry(plots[i],labels[i], "p")

    legend.Draw("same")
    saveas = saveWhere+filename+'.png'
    print 'will be saved as %s'%saveas
    canvas.SaveAs(saveas)



# some variables
selections = ["muPhi>80.*3.14159/180.&&muPhi<120*3.14159/180.","(muPhi>140.*3.14159/180.||muPhi<60.*3.14159/180.)"]
labels = ["ME4/2 Region","Non-ME4/2 Region"]
normalizations = [1./(40.*3.14159/180.),1./(280.*3.14159/180.)]
normalizations1 = [1,1]

#plot_n_hists(tree,"(muL1pt-muPt)/muPt",[44,-2,20],"ptResolution","muEta>1.25&&muEta<1.75&&muL1pt>0",
#             selections,labels,normalizations,
#             "CSCTF p_{T} Resolution","(L1p_{T}-p_{T})/p_{T}")
#

#plot_n_hists(tree,"(muL1pt-muPt)/muPt",[44,-2,20],"ptResolution_3LCTto4LCT",
#             "muEta>1.25&&muEta<1.75&&muL1pt>0"
#             +"&&((muNumberOfMatchedStations==3&&muLastStation!=4)"
#             +"||(muNumberOfMatchedStations==4&&muLastStation==4))",
#             selections,labels,normalizations,
#             "CSCTF p_{T} Resolution","(L1p_{T}-p_{T})/p_{T}")
#
#plot_n_hists(tree,"(muL1pt-muPt)/muPt",[44,-2,20],"ptResolution_2LCTto3LCT",
#             "muEta>1.25&&muEta<1.75&&muL1pt>0"
#             +"&&((muNumberOfMatchedStations==2&&muLastStation!=4)"
#             +"||(muNumberOfMatchedStations==3&&muLastStation==4))",
#             selections,labels,normalizations,
#             "CSCTF p_{T} Resolution","(L1p_{T}-p_{T})/p_{T}")

plot_n_hists(tree,"muPt",[50,0,150],"pt_tracker_3LCTto4LCT",
             "muEta>1.25&&muEta<1.75&&muL1pt>0"
             +"&&((muNumberOfMatchedStations==3&&muLastStation!=4)"
             +"||(muNumberOfMatchedStations==4&&muLastStation==4))",
             selections,labels,normalizations,
             "Tracker p_{T}","p_{T} (GeV/c)")

plot_n_hists(tree,"muPt",[50,0,150],"pt_tracker_2LCTto3LCT",
             "muEta>1.25&&muEta<1.75&&muL1pt>0"
             +"&&((muNumberOfMatchedStations==2&&muLastStation!=4)"
             +"||(muNumberOfMatchedStations==3&&muLastStation==4))",
             selections,labels,normalizations,
             "Tracker p_{T}","p_{T} (GeV/c)")

plot_n_hists(tree,"muL1pt",[50,0,150],"pt_CSCTF_3LCTto4LCT",
             "muEta>1.25&&muEta<1.75&&muL1pt>0"
             +"&&((muNumberOfMatchedStations==3&&muLastStation!=4)"
             +"||(muNumberOfMatchedStations==4&&muLastStation==4))",
             selections,labels,normalizations,
             "CSCTF p_{T}","p_{T} (GeV/c)")

plot_n_hists(tree,"muL1pt",[50,0,150],"pt_CSCTF_2LCTto3LCT",
             "muEta>1.25&&muEta<1.75&&muL1pt>0"
             +"&&((muNumberOfMatchedStations==2&&muLastStation!=4)"
             +"||(muNumberOfMatchedStations==3&&muLastStation==4))",
             selections,labels,normalizations,
             "CSCTF p_{T}","p_{T} (GeV/c)")
