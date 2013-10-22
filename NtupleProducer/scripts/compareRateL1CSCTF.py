'''

Script to make rate plots for both PU methods and compare them

Author: D. Taylor,  N. Woods, M.Cepeda, S. Dasu, L. Dodd, E. Friis    UW Madison


Usage: python compareRateL1CSCTF.py L1NTuple.root label[optional] 

 
E.G.
python compareRateL1CSCTF.py L1NTuple.root v3
will produce rate plots in ~/public_html/v3_filename.png

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
   print 'Usage:python compareRateL1CSCTF.py L1NTuple.root label[optional]'
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
tree  = ntuple_file.Get("l1NtupleProducer/L1Tree")

canvas = ROOT.TCanvas("asdf", "adsf", 800, 600)


################################################################################
#  make_plot uses draw() method to draw pt to be used in make_ _rate method    #
################################################################################

def make_plot(tree, variable, selection, binning, xaxis='', title='', calFactor=1):
    ''' Plot a variable using draw and return the histogram '''
    if len(binning)==3:
        draw_string = "%s * %0.2f>>htemp(%s)" % (variable, calFactor, ", ".join(str(x) for x in binning))
    else:
        draw_string = "%s * %0.2f>>htemp()" % (variable, calFactor)
    print draw_string
    tree.Draw(draw_string, selection, "goff")
    output_histo = ROOT.gDirectory.Get("htemp").Clone()
    if len(binning)!=3:
        output_histo.Rebin(len(binning)-1,"hnew",array('d',binning))
        output_histo = ROOT.gDirectory.Get("hnew").Clone()
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

##################################
####### Draw plots ###############
##################################

# some variables
selections = ["trPhi_02PI>80.*3.14159/180.&&trPhi_02PI<120*3.14159/180.","(trPhi_02PI>140.*3.14159/180.||trPhi_02PI<60.*3.14159/180.)"]
selections_sector = ["trSector==2","trSector!=2&&trEndcap==1"]
labels = ["ME4/2 Region","Non-ME4/2 Region"]
normalizations = [1./(40.*3.14159/180.),1./(280.*3.14159/180.)]
normalizations_sector = [1.,1./5.]

bins = [0,2,2.5,3,3.5,4,4.5,5,6,7,8,10,12,14,16,18,20,25,30,35,40,45,50,60,70,80,90,100,120,140]

plot_n_rates(tree,"trPt",[50,0,150],"trPt","trEta>1.2&&trEta<1.8",
             selections_sector,labels,normalizations_sector,
             "CSCTF p_{T} Rate","p_{T} (GeV/c)")
