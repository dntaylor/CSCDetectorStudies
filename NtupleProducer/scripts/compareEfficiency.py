'''

Script to make some quick efficiency and resolution plots

Author: Evan K. Friis, UW Madison; modified by Nate Woods, Devin Taylor

Usage: python compareEfficiency.py TnPFitTree.root ME42RegionCut NonME42RegionCut label[optional]

E.G.
python compareEfficiency.py TAVGPUFILE.root NOPUFILE.root v3_
will produce rate plots in ~/www/v3_filename.png

python compareEfficiency.py TAVGPUFILE.root NOPUFILE.root UCT2015/test_  
will produce rate plots in ~/www/UCT2015/test_filename.png 

python compareEfficiency.py TAVGPUFILE.root NOPUFILE.root
will produce rate plots in ~/www/filename.png


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
if len(argv) < 3:
   print 'Usage:python compareEfficiency.py ME42TagAndProbeTree.root label[optional]'
   exit()

Infile = argv[1]
ntuple_file = ROOT.TFile(Infile)

def setn():
   global n #stupid hack to make profiles work correctly
   n=0

####################################
######## LABEL & SAVE WHERE ########
####################################

if len(argv)>2:
   saveWhere='~/public_html/'+argv[2]
else:
   saveWhere='~/public_html/'

### Get fitter trees
tnpFit = ntuple_file.Get("tagAndProbeTree/fitter_tree")
tnpFitSta = ntuple_file.Get("tagAndProbeTreeSta/fitter_tree")

canvas = ROOT.TCanvas("asdf", "adsf", 800, 600)

####################################
######## Plotting defs #############
####################################
def make_plot(tree, variable, selection, binning, xaxis='', title=''):
    ''' Plot a variable using draw and return the histogram '''
    global n
    draw_string = "%s>>htemp%i(%s)" % (variable, n, ", ".join(str(x) for x in binning))
    #bin_string = str(len(binning)-1)+", ["+", ".join(str(x) for x in binning)+"]"
    #draw_string = "%s>>htemp%i(%s)" % (variable, n, bin_string)

    print draw_string
    print selection
    tree.Draw(draw_string, selection, "goff")
    output_histo = ROOT.gDirectory.Get("htemp%i"%(n)).Clone()
    output_histo.GetXaxis().SetTitle(xaxis)
    output_histo.SetTitle(title)
    n=n+1
    return output_histo

def make_efficiency(denom, num, color, markerStyle):
    ''' Make an efficiency graph '''
    eff = ROOT.TGraphAsymmErrors(num, denom)
    eff.SetMarkerStyle(markerStyle)
    eff.SetMarkerColor(color)
    eff.SetMarkerSize(1.)
    eff.SetLineColor(color)
    return eff

def make_profile(Ntuple, variables, binning, selection, color, markerStyle, min, max, file_title="profile", title='',xaxis='',yaxis=''):
   ''' Make and save a legit profile '''
   plot = make_plot(Ntuple, variables, selection, binning, xaxis, title)
   prof = plot.ProfileX()
   prof.SetMarkerSize(1.5)
   prof.SetMarkerStyle(markerStyle)
   prof.SetMarkerColor(color)
   prof.SetLineColor(color)
   prof.SetMinimum(min)
   prof.SetMaximum(max)

   framebins = binning[0:3]

   frame = ROOT.TH1F("frame", "frame", *framebins)
   frame.SetMaximum(max)
   frame.SetMinimum(min)
   frame.SetTitle(title)
   frame.GetXaxis().SetTitle(xaxis)
   frame.GetYaxis().SetTitle(yaxis)
   frame.Draw()
   prof.Draw('e')
   filename = saveWhere + file_title + '.png'
   canvas.SaveAs(filename)

def make_many_profiles(NtupleList, variableList, xVariable, binning, selectionList, colorList, markerList, min, max, nameList, file_title="many_profiles", title='',xaxis='',yaxis=''):
   ''' Make and save an arbitrary number of profiles '''
   if not (len(NtupleList) == len(colorList) and len(NtupleList) == len(colorList) and len(NtupleList) == len(nameList) and len(NtupleList) == len(variableList) and len(NtupleList) == len(selectionList)):
      print "List arguments to make_many_profiles must be the same size"
      return

   profList=[]
   legend = ROOT.TLegend(0.3, 0.7, 0.5, 0.9, "", "brNDC")
   legend.SetFillColor(ROOT.EColor.kWhite)
   legend.SetBorderSize(1)

   for i in range(len(NtupleList)):
      plot = make_plot(NtupleList[i], variableList[i]+":"+xVariable, selectionList[i], binning, xaxis, title)
      prof = plot.ProfileX()
      prof.SetMarkerSize(1.5)
      prof.SetMarkerStyle(markerList[i])
      prof.SetMarkerColor(colorList[i])
      prof.SetLineColor(colorList[i])
      prof.SetMinimum(min)
      prof.SetMaximum(max)
      profList.append(prof)
      legend.AddEntry(profList[i], nameList[i], "pe")

   framebins = binning[0:3]

   frame = ROOT.TH1F("frame", "frame", *framebins)
   frame.SetMaximum(max)
   frame.SetMinimum(min)
   frame.SetTitle(title)
   frame.GetXaxis().SetTitle(xaxis)
   frame.GetYaxis().SetTitle(yaxis)
   frame.Draw()
   for prof in profList:
      prof.Draw('esame')
   legend.Draw()
   filename = saveWhere + file_title + '.png'
   canvas.SaveAs(filename)

def compare_n_efficiencies(Ntuple, variable, ptCut,
                         etaCut, binning,
                         selection="",effSelections=[""],passSelection="",
                         file_title="plot",
                         title='', xaxis='', labels=[""]):
   ''' Creates plot of ntuple of TGraphAsymmErrors '''
   selection_string = "pt>"+str(ptCut)
   selection_string += ("&&eta>"+etaCut[0]+"&&eta<"+etaCut[1])
   var = variable
   if selection != "":
      selection_string += ("&&" + selection)
   denom = []
   num = []
   for effSel in effSelections:
      selection_temp = selection_string
      if effSel != "":
          selection_temp += ("&&"+effSel)
      denom.append(make_plot(
         Ntuple, var,
         selection_temp,
         binning
         )
      )
      selection_temp += ("&&"+passSelection)
      num.append(make_plot(
         Ntuple, var,
         selection_temp,
         binning
         )
      )

   frame = ROOT.TH1F("frame", "frame", *binning)
   frame.SetMaximum(1.1)
   frame.SetMinimum(0.7)
   frame.SetTitle(title)
   frame.GetXaxis().SetTitle(xaxis)
   frame.GetYaxis().SetTitle("Efficiency ("+passSelection+")")
   legend = ROOT.TLegend(0.7, 0.78, 0.89, 0.89, "", "brNDC")
   legend.SetFillColor(ROOT.EColor.kWhite)
   legend.SetBorderSize(1)

   eff = []
   colors = [ROOT.EColor.kRed,ROOT.EColor.kBlue,ROOT.EColor.kGreen,ROOT.EColor.kBlack]
   styles = [22,21,20,19]
   for i in range(len(denom)):
      eff.append(make_efficiency(denom[i],num[i],colors[i],styles[i]))
   frame.Draw()
   for i in range(len(eff)):
      eff[i].Draw('pe')
      legend.AddEntry(eff[i],labels[i],"pe")
   legend.Draw()
   line = ROOT.TLine(binning[1],1,binning[2],1)
   line.Draw()
   filename = saveWhere + file_title + '.png'
   canvas.SaveAs(filename)

###########################################
########### Make selected plots ###########
###########################################

setn()

selections = ["phi>80.*3.14159/180.&&phi<120*3.14159/180.","(phi>140.*3.14159/180.||phi<60.*3.14159/180.)"]
labels = ["ME4/2 Region","Non-ME4/2 Region"]

# l1pt
compare_n_efficiencies(tnpFitSta,
                     "l1pt",
                     0,
                     ["1.2","1.8"],
                     [16,0,150],
                     "",
                     selections,
                     "isTightMuon",
                     "l1pt_plot",
                     "L1 p_{T} Tight Muon",
                     "L1 p_{T} (GeV/c)",
                     labels)
# pt
compare_n_efficiencies(tnpFitSta,
                     "pt",
                     0,
                     ["1.2","1.8"],
                     [8,0,150],
                     "",
                     selections,
                     "isTightMuon",
                     "pt_plot",
                     "p_{T} Tight Muon",
                     "p_{T} (GeV/c)",
                     labels)
# l1pt with quality
compare_n_efficiencies(tnpFitSta,
                     "l1pt",
                     0,
                     ["1.2","1.8"],
                     [16,0,150],
                     "l1q>5",
                     selections,
                     "isTightMuon",
                     "l1pt_q_plot",
                     "L1 p_{T} Tight Muon (GMT qualtiy=6,7)",
                     "L1 p_{T} (GeV/c)",
                     labels)
# pt with quality
compare_n_efficiencies(tnpFitSta,
                     "pt",
                     0,
                     ["1.2","1.8"],
                     [8,0,150],
                     "l1q>5",
                     selections,
                     "isTightMuon",
                     "pt_q_plot",
                     "p_{T} Tight Muon (GMT quality=6,7)",
                     "p_{T} (GeV/c)",
                     labels)
# l1pt with quality req 7
compare_n_efficiencies(tnpFitSta,
                     "l1pt",
                     0,
                     ["1.2","1.8"],
                     [16,0,150],
                     "l1q==7",
                     selections,
                     "isTightMuon",
                     "l1pt_q7_plot",
                     "L1 p_{T} Tight Muon (GMT qualtiy=7)",
                     "L1 p_{T} (GeV/c)",
                     labels)
# pt with quality req 7
compare_n_efficiencies(tnpFitSta,
                     "pt",
                     0,
                     ["1.2","1.8"],
                     [8,0,150],
                     "l1q==7",
                     selections,
                     "isTightMuon",
                     "pt_q7_plot",
                     "p_{T} Tight Muon (GMT quality=7)",
                     "p_{T} (GeV/c)",
                     labels)
# l1pt with quality req 6
compare_n_efficiencies(tnpFitSta,
                     "l1pt",
                     0,
                     ["1.2","1.8"],
                     [16,0,150],
                     "l1q==6",
                     selections,
                     "isTightMuon",
                     "l1pt_q6_plot",
                     "L1 p_{T} Tight Muon (GMT quality=6)",
                     "L1 p_{T} (GeV/c)",
                     labels)
# pt with quality req 6
compare_n_efficiencies(tnpFitSta,
                     "pt",
                     0,
                     ["1.2","1.8"],
                     [8,0,150],
                     "l1q==6",
                     selections,
                     "isTightMuon",
                     "pt_q6_plot",
                     "p_{T} Tight Muon (GMT quality=6)",
                     "p_{T} (GeV/c)",
                     labels)
# lq1
compare_n_efficiencies(tnpFitSta,
                     "l1q",
                     0,
                     ["1.2","1.8"],
                     [8,-0.5,7.5],
                     "",
                     selections,
                     "isTightMuon",
                     "l1q_plot",
                     "L1 Quality Tight Muon",
                     "L1 Quality",
                     labels)
# phi
compare_n_efficiencies(tnpFitSta,
                     "phi",
                     0,
                     ["1.2","1.8"],
                     [6,-3.14159,3.14159],
                     "",
                     ["","l1q==6","l1q==7","l1q>5"],
                     "isTightMuon",
                     "phi_plot",
                     "Phi Tight Muon",
                     "#phi",
                     ["Overall","GMT q=6","GMT q=7","GMT q=6,7"])
