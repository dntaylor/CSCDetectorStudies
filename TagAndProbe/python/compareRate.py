'''

Script to make rate plots for both PU methods and compare them

Author: N. Woods, M.Cepeda, S. Dasu, L. Dodd, E. Friis            UW Madison


Usage: python comparePURates.py TAVGPUFILE.root XAVGPUFILE.root label[optional] 

 
E.G.
python allRatePlots.py TAVGPUFILE.root XAVGPUFILE.root v3
will produce rate plots in ~/www/v3_filename.png

python alRatesPlots.py TAVGPUFILE.root XAVGPUFILE.root UCT2015/test  
will produce rate plots in ~/www/UCT2015/test_filename.png 

python allRatePlots.py TAVGPUFILE.root XAVGPUFILE.root
will produce rate plots in ~/www/filename.png


'''

#######################
### GET EVERYTHING ####
#######################
from sys import argv, stdout, stderr

import ROOT


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
   print 'Usage:python allRatePlots.py tAvgPUFile.root xAvgPUFile.root label[optional]'
   exit()

Infile = argv[1]
ntuple_file = ROOT.TFile(Infile)


####################################
####### LABEL & SAVE WHERE #########
####################################

if len(argv)>2:
   saveWhere='~/public_html/'+argv[2]
else:
   saveWhere='~/public_html/'

######################################
####### Get NTuples ##################
######################################
tnpFit = ntuple_file.Get("tagAndProbeTree/fitter_tree")
tnpFitSta = ntuple_file.Get("tagAndProbeTreeSta/fitter_tree")

canvas = ROOT.TCanvas("asdf", "adsf", 800, 600)


################################################################################
#  make_plot uses draw() method to draw pt to be used in make_ _rate method    #
################################################################################

def make_plot(tree, variable, selection, binning, xaxis='', title='', calFactor=1):
    ''' Plot a variable using draw and return the histogram '''
    draw_string = "%s * %0.2f>>htemp(%s)" % (variable, calFactor, ", ".join(str(x) for x in binning))
    print draw_string
    tree.Draw(draw_string, selection, "goff")
    output_histo = ROOT.gDirectory.Get("htemp").Clone()
    output_histo.GetXaxis().SetTitle(xaxis)
    output_histo.SetTitle(title)
    return output_histo

######################################################################################
#  make_ _rate method calculates rate given a pt histogram and returns histogram     #
######################################################################################

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
def plot_n_rates(ntuple, varName, binning, filename, selection, selections=[""], title='', xaxis='', labels=[""], normalization=[1]):
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
            rates[i].Scale(normalization[i])
            rates[i].Draw('ph')
        else:
            rates[i].Scale(normalization[i])
            rates[i].Draw('phsame')
        legend.AddEntry(rates[i],labels[i], "p")

    legend.Draw("same")
    saveas = saveWhere+filename+'.png'
    print 'will be saved as %s'%saveas
    canvas.SaveAs(saveas)

##################################
####### Draw plots ###############
##################################

# some variables
selections = ["phi>80.*3.14159/180.&&phi<120*3.14159/180.","(phi>140.*3.14159/180.||phi<60.*3.14159/180.)"]
labels = ["ME4/2 Region","Non-ME4/2 Region"]
normalizations = [1./(40.*3.14159/180.),1./(280.*3.14159/180.)]

plot_n_rates(tnpFitSta,
             "l1pt",
             [16,0,150],
             "l1pt_rate",
             "eta>1.2&&eta<1.8",
             selections,
             "L1 p_{T} Rate",
             "L1 p_{T} (GeV/c)",
             labels,
             normalizations)

plot_n_rates(tnpFitSta,
             "pt",
             [16,0,150],
             "pt_rate",
             "eta>1.2&&eta<1.8",
             selections,
             "p_{T} Rate",
             "p_{T} (GeV/c)",
             labels,
             normalizations)

plot_n_rates(tnpFitSta,
             "l1pt",
             [16,0,150],
             "l1pt_q_rate",
             "eta>1.2&&eta<1.8&&l1q>5",
             selections,
             "L1 p_{T} Rate (GMT quality 6,7)",
             "L1 p_{T} (GeV/c)",
             labels,
             normalizations)

plot_n_rates(tnpFitSta,
             "pt",
             [16,0,150],
             "pt_q_rate",
             "eta>1.2&&eta<1.8&&l1q>5",
             selections,
             "p_{T} Rate (GMT quality 6,7)",
             "p_{T} (GeV/c)",
             labels,
             normalizations)

plot_n_rates(tnpFitSta,
             "l1pt",
             [16,0,150],
             "l1pt_q6_rate",
             "eta>1.2&&eta<1.8&&l1q==6",
             selections,
             "L1 p_{T} Rate (GMT quality 6)",
             "L1 p_{T} (GeV/c)",
             labels,
             normalizations)

plot_n_rates(tnpFitSta,
             "pt",
             [16,0,150],
             "pt_q6_rate",
             "eta>1.2&&eta<1.8&&l1q==6",
             selections,
             "p_{T} Rate (GMT quality 6)",
             "p_{T} (GeV/c)",
             labels,
             normalizations)

plot_n_rates(tnpFitSta,
             "l1pt",
             [16,0,150],
             "l1pt_q7_rate",
             "eta>1.2&&eta<1.8&&l1q==7",
             selections,
             "L1 p_{T} Rate (GMT quality 7)",
             "L1 p_{T} (GeV/c)",
             labels,
             normalizations)

plot_n_rates(tnpFitSta,
             "pt",
             [16,0,150],
             "pt_q7_rate",
             "eta>1.2&&eta<1.8&&l1q==7",
             selections,
             "p_{T} Rate (GMT quality 7)",
             "p_{T} (GeV/c)",
             labels,
             normalizations)



