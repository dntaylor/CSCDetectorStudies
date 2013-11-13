'''
Plotting utilities for ME4/2 trigger and reconstruction studies
'''

#######################
### GET EVERYTHING ####
#######################
from sys import argv, stdout, stderr

import ROOT
from array import array

#############################
## Save (to be overridden) ##
#############################
saveWhere='~/public_html/'
canvas = ROOT.TCanvas("asdf", "adsf", 800, 600)

def setn():
   global n #stupid hack to make profiles work correctly
   n=0

def setSave(save):
   global saveWhere
   saveWhere = save

################################################################################
#  make_plot uses draw() method to draw                                        #
################################################################################

def make_plot(tree, variable, selection, binning, color=ROOT.EColor.kBlue, markerStyle=20, xaxis='', title='', calFactor=1):
    ''' Plot a variable using draw and return the histogram '''
    global n
    draw_string = "%s>>htemp%i(%s)" % (variable, n, ", ".join(str(x) for x in binning))
    print draw_string
    print selection
    tree.Draw(draw_string, selection, "goff")
    output_histo = ROOT.gDirectory.Get("htemp%i"%(n)).Clone()
    output_histo.GetXaxis().SetTitle(xaxis)
    output_histo.SetTitle(title)
    output_histo.SetLineColor(color)
    output_histo.SetMarkerStyle(markerStyle)
    output_histo.SetMarkerColor(color)
    n = n+1
    return output_histo

#def make_plot(tree, variable, selection, binning, xaxis='', title=''):
#    return make_plot(tree, variable, selection, binning, ROOT.Ecolor.kblue, markerStyle=20, xaxis, title, 1)

def make_ratio(denom, num):
    ratio = ROOT.TGraphAsymmErrors(num, denom)
    return ratio

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

def make_rate(pt, color, markerStyle):
    ''' Make a rate plot with speficied color and marker style '''
    numBins = pt.GetXaxis().GetNbins()
    rate = pt.Clone()

    for i in range(1, numBins+1):
        rate.SetBinContent(i, pt.Integral(i, numBins))

    rate.SetLineColor(color)
    rate.SetMarkerStyle(markerStyle)
    rate.SetMarkerColor(color)

    return rate


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


############################################################################
#     plotRates method will be used to Draw rates. Calls make_plot         #
#
#        l1_pt[pt plot used to calculate rate] = make_plot( [function above]    #
#        l1ntuple [l1 or uct], 'pt'[variable name],                             # 
#        "", [selection such as eta cut goes here]                              #
#        binning, [used later]                                                  #
#        '','', [axis titles]                                                   #
#        L1_CALIB_FACTOR [Calibration factor, default is now zero]              #
#        )                                                                      #
#################################################################################
def plot_n_rates(ntuple, varName, binning, filename, selection, selections=[""], labels=[""], normalization=[1], title='', xaxis=''):
    ''' Save a rate Plot '''

    plots = []
    rates = []
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
            '',''
            )
        )
        rates.append(make_rate(plots[i],colors[i],styles[i]))

    canvas.SetLogy()
    legend = ROOT.TLegend(0.7, 0.78, 0.89, 0.89, "", "brNDC")
    legend.SetFillColor(ROOT.EColor.kWhite)
    legend.SetBorderSize(1)
    for i in range(len(selections)):
        if i == 0:
            rates[i].SetTitle(title)
            rates[i].GetXaxis().SetTitle(xaxis)
            rates[i].GetYaxis().SetTitle("Events")
            temp_norm = rates[i].Integral()
            rates[i].Scale(normalization[i])
            rates[i].Draw('ph')
        else:
            temp_norm = rates[i].Integral()
            rates[i].Scale(normalization[i])
            rates[i].Draw('phsame')
        legend.AddEntry(rates[i],labels[i], "p")

    legend.Draw("same")
    saveas = saveWhere+filename+'.png'
    print 'will be saved as %s'%saveas
    canvas.SaveAs(saveas)

def plot_hists_with_ratio(ntuple, varName, binning, filename, selection, selections=[""], labels=[""], normalization=[1], title='', xaxis=''):
    
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

    # make two pads, one for hist, one for ratio
    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1)
    pad1.SetBottomMargin(0)
    pad1.Draw()
    pad1.cd()
    pad1.SetLogy()
    
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

    canvas.cd()
    pad2 = ROOT.TPad("pad2", "pad2", 0, 0, 1, 0.3)
    pad2.SetTopMargin(0)
    pad2.Draw()
    pad2.cd()

    #ratio = make_ratio(plots[1],plots[0])
    ratio = plots[0].Clone()
    ratio.Sumw2()
    ratio.SetStats(0)
    ratio.Divide(plots[1])
    ratio.SetMarkerStyle(21)
    ratio.SetMarkerColor(ROOT.EColor.kBlack)
    ratio.SetLineColor(ROOT.EColor.kBlack)
    ratio.Draw("ep")
    canvas.cd()

    saveas = saveWhere+filename+'.png'
    print 'will be saved as %s'%saveas
    canvas.SaveAs(saveas)
