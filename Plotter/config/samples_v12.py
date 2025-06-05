# Description: Common configuration file for creating pico sample set plotting scripts
import re
from TauFW.Plotter.sample.utils import LOG, STYLE, ensuredir, repkey, joincuts, joinweights, ensurelist,\
                                       setera, getyear, loadmacro, Sel, Var
from TauFW.Plotter.sample.utils import getsampleset as _getsampleset
import json

f = open("../PicoProducer/samples/nanoaod_sumw_2022_postEE.json") #for 2022postEE
f_new = open("../PicoProducer/samples/nanoaod_info_2022EE.json") #for 2022EE
nevts_json_new = json.load(f_new)
nevts_json = json.load(f)

def getsampleset(channel,era,**kwargs):
  verbosity = LOG.getverbosity(kwargs)
  year     = getyear(era) # get integer year
  fname    = kwargs.get('fname', "$PICODIR/$SAMPLE_$CHANNEL$TAG.root" ) # file name pattern of pico files
  split    = kwargs.get('split',    ['DY', 'TT', 'ST'] if 'tau' in channel else [ ] ) # split samples (e.g. DY) into genmatch components
  join     = kwargs.get('join',     ['VV','Top', 'VVV','HTT'] if era=='2022EE' else ['VV','Top'] ) # join samples (e.g. VV, top)
  rmsfs    = ensurelist(kwargs.get('rmsf', [ ])) # remove the tau ID SF, e.g. rmsf=['idweight_2','ltfweight_2']
  addsfs   = ensurelist(kwargs.get('addsf', [ ])) # add extra weight to all samples
  weight   = kwargs.get('weight',   None         ) # weight for all MC samples
  dyweight = kwargs.get('dyweight', 'zptweight'  ) # weight for DY samples
  ttweight = kwargs.get('ttweight', 'ttptweight' ) # weight for ttbar samples
  filter   = kwargs.get('filter',   None         ) # only include these MC samples
  vetoes   = kwargs.get('vetoes',   None         ) # veto these MC samples
  #tag      = kwargs.get('tag',      ""           ) # extra tag for sample file names
  table    = kwargs.get('table',    True         ) # print sample set table
  setera(era,cme=13.6) # set era for plot style and lumi-xsec normalization
  if 'TT' in split and 'Top' in join: # don't join TT & ST
    join.remove('Top')
    join += ['TT','ST']
  
  # SM BACKGROUND MC SAMPLES
  if '2022_preEE' in era or '2022_postEE' in era or '2022EE' in era or '2023'in era: # so far same samples and cross sections are used for preEE and postEE, if event numbers are set elsewhere then we don't need to add seperate numbers for both eras
    # for now nevts is set to 1 so it isn't taken into account in the scaling of the samples as this will be done elsewhere
    
    kfactor_dy=6282.6/5455.0 # LO->NNLO+NLO_EW k-factor computed for 13.6 TeV [https://twiki.cern.ch/twiki/bin/viewauth/CMS/MATRIXCrossSectionsat13p6TeV]
    kfactor_wj=63425.1/55300 # LO->NNLO+NLO_EW k-factor computed for 13.6 TeV
    kfactor_ttbar=923.6/762.1 # NLO->NNLO k-factor computed for 13.6 TeV
    kfactor_ww=1.524 # LO->NNLO+NLO_EW computed for 13.6 TeV
    kfactor_zz=1.524 # LO->NNLO+NLO_EW computed for 13.6 TeV
    kfactor_wz=1.414 # LO->NNLO+NLO_EW computed for 13.6 TeV 


    cme=13.6

    if '2023'in era:
      expsamples = [ # table of MC samples to be converted to Sample objects
        # GROUP NAME                     TITLE                 XSEC      EXTRA OPTIONS
        #( 'DY', "DYJetsToLL_M-50",       "Drell-Yan 50",        5455.0*kfactor_dy, {'extraweight': dyweight }),#, "nevts":nevts_json["DYJetsToLL_M-50"]} ), # LO times kfactor, commenting this one out as it is the same as the one below but in principle it should be possible to conbine this sample with the inclusive one below 
        ( 'DY', "DYto2L-4Jets_MLL-50",   "Drell-Yan 50",        5455.0*kfactor_dy, {'extraweight': dyweight } ), # LO times kfactor
        ( 'DY', "DYto2L-4Jets_MLL-50_1J",      "Drell-Yan 1J 50",      978.3*kfactor_dy, {'extraweight': dyweight} ), # LO times kfactor currently not available
        ( 'DY', "DYto2L-4Jets_MLL-50_2J",      "Drell-Yan 2J 50",      315.1*kfactor_dy, {'extraweight': dyweight} ), # LO times kfactor
        ( 'DY', "DYto2L-4Jets_MLL-50_3J",      "Drell-Yan 3J 50",      93.7*kfactor_dy, {'extraweight': dyweight} ), # LO times kfactor
        ( 'DY', "DYto2L-4Jets_MLL-50_4J",      "Drell-Yan 4J 50",      45.4*kfactor_dy, {'extraweight': dyweight} ), # LO times kfactor
        ( 'WJ', "WtoLNu-4Jets",            "W + jets",           55300.*kfactor_wj ), # LO times kfactor
        ( 'WJ', "WtoLNu-4Jets_1J",           "W + 1J",              9128.*kfactor_wj), # LO times kfactor
        ( 'WJ', "WtoLNu-4Jets_2J",           "W + 2J",              2922.*kfactor_wj  ), # LO times kfactor
        ( 'WJ', "WtoLNu-4Jets_3J",           "W + 3J",               861.3*kfactor_wj ), # LO times kfactor
        ( 'WJ', "WtoLNu-4Jets_4J",           "W + 4J",               415.4*kfactor_wj), # LO times kfactor
   
        ( 'VV', "WW",             "WW",                    80.23*kfactor_ww ), # LO times kfactor
        ( 'VV', "WZ",             "WZ",                    29.1*kfactor_wz), # LO times kfactor
        ( 'VV', "ZZ",             "ZZ",                    12.75*kfactor_zz ), # LO times kfactor

        ( 'TT', "TTto2L2Nu",             "ttbar 2l2#nu",          80.9*kfactor_ttbar, {'extraweight': ttweight} ), # NLO times BR times kfactor
        ( 'TT', "TTto4Q",                "ttbar hadronic",       346.4*kfactor_ttbar, {'extraweight': ttweight} ), # NLO times BR times kfactor
        ( 'TT', "TTtoLNu2Q",             "ttbar semileptonic",   334.8*kfactor_ttbar, {'extraweight': ttweight} ), # NLO times BR times kfactor
        #( 'ST', "TBbarQ_t-channel",      "ST t-channel t",       123.8), # NLO
        #( 'ST', "TbarBQ_t-channel",      "ST t-channel at",      75.47), # NLO
        ( 'ST', "TWminustoLNu2Q",             "ST tW semileptonic",         15.8 ), # NLO (36.0) times LNu2Q BR
        ( 'ST', "TWminusto2L2Nu",             "ST tW 2l2#nu",               3.8 ), # NLO (36.0) times 2L2Nu BR
        #( 'ST', "TbarWplustoLNu2Q",         "ST atW semileptonic",          15.9 ), # NLO (36.1) times LNu2Q BR
        #( 'ST', "TbarWplusto2L2Nu",         "ST atW 2l2#nu",                3.8 ), # NLO (36.1) times 2L2Nu BR
      ]
    
    if '2022_preEE' in era:
      expsamples = [ # table of MC samples to be converted to Sample objects
        # GROUP NAME                     TITLE                 XSEC      EXTRA OPTIONS
        #( 'DY', "DYJetsToLL_M-50",       "Drell-Yan 50",        5455.0*kfactor_dy, {'extraweight': dyweight }),#, "nevts":nevts_json["DYJetsToLL_M-50"]} ), # LO times kfactor, commenting this one out as it is the same as the one below but in principle it should be possible to conbine this sample with the inclusive one below 
        ( 'DY', "DYto2L-4Jets_MLL-50",   "Drell-Yan 50",        5455.0*kfactor_dy, {'extraweight': dyweight } ), # LO times kfactor
        ( 'DY', "DYto2L-4Jets_MLL-50_1J",      "Drell-Yan 1J 50",      978.3*kfactor_dy, {'extraweight': dyweight} ), # LO times kfactor currently not available
        ( 'DY', "DYto2L-4Jets_MLL-50_2J",      "Drell-Yan 2J 50",      315.1*kfactor_dy, {'extraweight': dyweight} ), # LO times kfactor
        ( 'DY', "DYto2L-4Jets_MLL-50_3J",      "Drell-Yan 3J 50",      93.7*kfactor_dy, {'extraweight': dyweight} ), # LO times kfactor
        ( 'DY', "DYto2L-4Jets_MLL-50_4J",      "Drell-Yan 4J 50",      45.4*kfactor_dy, {'extraweight': dyweight} ), # LO times kfactor
        ( 'WJ', "WJetsToLNu-4Jets",            "W + jets",           55300.*kfactor_wj ), # LO times kfactor
        ( 'WJ', "WJetsToLNu-4Jets_1J",           "W + 1J",              9128.*kfactor_wj), # LO times kfactor
        ( 'WJ', "WJetsToLNu-4Jets_2J",           "W + 2J",              2922.*kfactor_wj  ), # LO times kfactor
        ( 'WJ', "WJetsToLNu-4Jets_3J",           "W + 3J",               861.3*kfactor_wj ), # LO times kfactor
        ( 'WJ', "WJetsToLNu-4Jets_4J",           "W + 4J",               415.4*kfactor_wj), # LO times kfactor
   
        ( 'VV', "WW",             "WW",                    80.23*kfactor_ww ), # LO times kfactor
        ( 'VV', "WZ",             "WZ",                    29.1*kfactor_wz), # LO times kfactor
        ( 'VV', "ZZ",             "ZZ",                    12.75*kfactor_zz ), # LO times kfactor

        ( 'TT', "TTTo2L2Nu",             "ttbar 2l2#nu",          80.9*kfactor_ttbar, {'extraweight': ttweight} ), # NLO times BR times kfactor
        ( 'TT', "TTto4Q",                "ttbar hadronic",       346.4*kfactor_ttbar, {'extraweight': ttweight} ), # NLO times BR times kfactor
        ( 'TT', "TTtoLNu2Q",             "ttbar semileptonic",   334.8*kfactor_ttbar, {'extraweight': ttweight} ), # NLO times BR times kfactor
        ( 'ST', "TBbarQ_t-channel",      "ST t-channel t",       123.8), # NLO
        ( 'ST', "TbarBQ_t-channel",      "ST t-channel at",      75.47), # NLO
        ( 'ST', "TWminustoLNu2Q",             "ST tW semileptonic",         15.8 ), # NLO (36.0) times LNu2Q BR
        ( 'ST', "TWminusto2L2Nu",             "ST tW 2l2#nu",               3.8 ), # NLO (36.0) times 2L2Nu BR
        ( 'ST', "TbarWplustoLNu2Q",         "ST atW semileptonic",          15.9 ), # NLO (36.1) times LNu2Q BR
        ( 'ST', "TbarWplusto2L2Nu",         "ST atW 2l2#nu",                3.8 ), # NLO (36.1) times 2L2Nu BR
      ]

     # if 'mutau' in channel:
     #   expsamples.append(('DY',"DYto2TautoMuTauh_M-50","Drell-Yan 50 -> tautau -> mu+tauh",5455.0*kfactor_dy,{'extraweight': dyweight})) # LO (using same cross section as inclusive samples), apply correct normalization in stitching
     #   # the cross section for this exact samples is 1885.0 which is ~ 1/3 the total DY->LL cross section (expected since it only selects taus and not electrons and muons)
     #   # the filter efficiency for this sample (due to tau BRs + kinematic cuts on tau decay products) is 2.865e-02 
    if '2022_postEE' in era:
       expsamples = [ # table of MC samples to be converted to Sample objects
        # GROUP NAME                     TITLE                 XSEC      EXTRA OPTIONS
        #( 'DY', "DYJetsToLL_M-50",       "Drell-Yan 50",        5455.0*kfactor_dy, {'extraweight': dyweight }),#, "nevts":nevts_json["DYJetsToLL_M-50"]} ), # LO times kfactor, commenting this one out as it is the same as the one below but in principle it should be possible to conbine this sample with the inclusive one below 
        ( 'DY', "DYto2L-4Jets_MLL-50",   "Drell-Yan 50",        5455.0*kfactor_dy, {'extraweight': dyweight } ), # LO times kfactor
        ( 'DY', "DYto2L-4Jets_MLL-50_1J",      "Drell-Yan 1J 50",      978.3*kfactor_dy, {'extraweight': dyweight} ), # LO times kfactor currently not available
        ( 'DY', "DYto2L-4Jets_MLL-50_2J",      "Drell-Yan 2J 50",      315.1*kfactor_dy, {'extraweight': dyweight} ), # LO times kfactor
        ( 'DY', "DYto2L-4Jets_MLL-50_3J",      "Drell-Yan 3J 50",      93.7*kfactor_dy, {'extraweight': dyweight} ), # LO times kfactor
        ( 'DY', "DYto2L-4Jets_MLL-50_4J",      "Drell-Yan 4J 50",      45.4*kfactor_dy, {'extraweight': dyweight} ), # LO times kfactor
        ( 'WJ', "WtoLNu-4Jets",            "W + jets",           55300.*kfactor_wj ), # LO times kfactor
        ( 'WJ', "WJetstoLNu-4Jets_1J",           "W + 1J",              9128.*kfactor_wj), # LO times kfactor
        ( 'WJ', "WJetstoLNu-4Jets_2J",           "W + 2J",              2922.*kfactor_wj  ), # LO times kfactor
        ( 'WJ', "WJetstoLNu-4Jets_3J",           "W + 3J",               861.3*kfactor_wj ), # LO times kfactor
        ( 'WJ', "WtoLNu-4Jets_4J",           "W + 4J",               415.4*kfactor_wj), # LO times kfactor
   
        ( 'VV', "WW",             "WW",                    80.23*kfactor_ww ), # LO times kfactor
        ( 'VV', "WZ",             "WZ",                    29.1*kfactor_wz), # LO times kfactor
        ( 'VV', "ZZ",             "ZZ",                    12.75*kfactor_zz ), # LO times kfactor

        ( 'TT', "TTTo2L2Nu",             "ttbar 2l2#nu",          80.9*kfactor_ttbar, {'extraweight': ttweight} ), # NLO times BR times kfactor
        ( 'TT', "TTto4Q",                "ttbar hadronic",       346.4*kfactor_ttbar, {'extraweight': ttweight} ), # NLO times BR times kfactor
        ( 'TT', "TTtoLNu2Q",             "ttbar semileptonic",   334.8*kfactor_ttbar, {'extraweight': ttweight} ), # NLO times BR times kfactor
        ( 'ST', "TBbarQ_t-channel",      "ST t-channel t",       123.8), # NLO
        ( 'ST', "TbarBQ_t-channel",      "ST t-channel at",      75.47), # NLO
        ( 'ST', "TWminustoLNu2Q",             "ST tW semileptonic",         15.8 ), # NLO (36.0) times LNu2Q BR
        ( 'ST', "TWminusto2L2Nu",             "ST tW 2l2#nu",               3.8 ), # NLO (36.0) times 2L2Nu BR
        ( 'ST', "TbarWplustoLNu2Q",         "ST atW semileptonic",          15.9 ), # NLO (36.1) times LNu2Q BR
        ( 'ST', "TbarWplusto2L2Nu",         "ST atW 2l2#nu",                3.8 ), # NLO (36.1) times 2L2Nu BR
      ]
     # if 'mutau' in channel:
     #   expsamples.append(('DY',"DYto2TautoMuTauh_M-50","Drell-Yan 50 -> tautau -> mu+tauh",5455.0*kfactor_dy,{'extraweight': dyweight})) # LO (using same cross section as inclusive samples), apply correct normalization in stitching
     #   # the cross section for this exact samples is 1885.0 which is ~ 1/3 the total DY->LL cross section (expected since it only selects taus and not electrons and muons)
     #   # the filter efficiency for this sample (due to tau BRs + kinematic cuts on tau decay products) is 2.865e-02 
    if '2022EE' in era:
      Higgs_amplify= 1
      expsamples = [ # table of MC samples to be converted to Sample objects
      # GROUP NAME                     TITLE                 XSEC      EXTRA OPTIONS
      # CP_Signal H->tau tau
      # Filter efficiencies: https://gitlab.cern.ch/dwinterb/HiggsDNA/-/blob/lr_updates/scripts/ditau/config/Run3_2022/filter_efficiencies.yaml?ref_type=heads
      # ('HTT','GluGluHTo2Tau_UncorrelatedDecay_CPodd_UnFiltered_ProdAndDecay', "ggH CPodd UnFiltered", 3.2759*Higgs_amplify, {"nevts":nevts_json_new["GluGluHTo2Tau_UncorrelatedDecay_CPodd_UnFiltered_ProdAndDecay"]}),
      # ('HTT','GluGluHTo2Tau_UncorrelatedDecay_MM_UnFiltered_ProdAndDecay', "ggH MM UnFiltered", 3.2759*Higgs_amplify, {"nevts":nevts_json_new["GluGluHTo2Tau_UncorrelatedDecay_MM_UnFiltered_ProdAndDecay"]}),
      # ('HTT','GluGluHTo2Tau_UncorrelatedDecay_SM_UnFiltered_ProdAndDecay', "ggH SM UnFiltered", 3.2759*Higgs_amplify, {"nevts":nevts_json_new["GluGluHTo2Tau_UncorrelatedDecay_SM_UnFiltered_ProdAndDecay"]}),
      # ('HTT','ZHToTauTau_UncorrelatedDecay_UnFiltered', "ZH UnFiltered", 0.05920*Higgs_amplify, {"nevts":nevts_json_new["ZHToTauTau_UncorrelatedDecay_UnFiltered"]}),
      # ('HTT','GluGluHTo2Tau_UncorrelatedDecay_UnFiltered', "ggH UnFiltered", 3.2759*Higgs_amplify, {"nevts":nevts_json_new["GluGluHTo2Tau_UncorrelatedDecay_UnFiltered"]}),
      # ('HTT','WplusHToTauTau_UncorrelatedDecay_UnFiltered', "WplusH UnFiltered", 0.05575*Higgs_amplify, {"nevts":nevts_json_new["WplusHToTauTau_UncorrelatedDecay_UnFiltered"]}),
      # ('HTT','WminusHToTauTau_UncorrelatedDecay_UnFiltered', "WminusH UnFiltered", 0.03561*Higgs_amplify, {"nevts":nevts_json_new["WminusHToTauTau_UncorrelatedDecay_UnFiltered"]}),
      # ('HTT','VBFHToTauTau_UncorrelatedDecay_UnFiltered', "VBFH UnFiltered", 0.2558*Higgs_amplify, {"nevts":nevts_json_new["VBFHToTauTau_UncorrelatedDecay_UnFiltered"]}),
      # ('HTT','GluGluHTo2Tau_UncorrelatedDecay_CPodd_Filtered_ProdAndDecay', "ggH CPodd Filtered", 3.2759*Higgs_amplify, {'extraweight': 0.3848 ,"nevts":nevts_json_new["GluGluHTo2Tau_UncorrelatedDecay_CPodd_Filtered_ProdAndDecay"]}),
      # ('HTT','GluGluHTo2Tau_UncorrelatedDecay_MM_Filtered_ProdAndDecay', "ggH MM Filtered", 3.2759*Higgs_amplify, {'extraweight':0.3848 ,"nevts":nevts_json_new["GluGluHTo2Tau_UncorrelatedDecay_MM_Filtered_ProdAndDecay"]}),
      ('HTT','GluGluHTo2Tau_UncorrelatedDecay_SM_Filtered_ProdAndDecay', "ggH SM Filtered", 3.2759*Higgs_amplify, {'extraweight':0.3847 ,"nevts":nevts_json_new["GluGluHTo2Tau_UncorrelatedDecay_SM_Filtered_ProdAndDecay"]}),
      ('HTT','ZHToTauTau_UncorrelatedDecay_Filtered', "ZH Filtered", 0.05920*Higgs_amplify, {'extraweight':0.3933 ,"nevts":nevts_json_new["ZHToTauTau_UncorrelatedDecay_Filtered"]}),
      # ('HTT','GluGluHTo2Tau_UncorrelatedDecay_Filtered', "ggH Filtered", 3.2759*Higgs_amplify, {"nevts":nevts_json_new["GluGluHTo2Tau_UncorrelatedDecay_Filtered"]}),
      ('HTT','WplusHToTauTau_UncorrelatedDecay_Filtered', "WplusH Filtered", 0.05575*Higgs_amplify, {'extraweight':0.3743 ,"nevts":nevts_json_new["WplusHToTauTau_UncorrelatedDecay_Filtered"]}),
      ('HTT','WminusHToTauTau_UncorrelatedDecay_Filtered', "WminusH Filtered", 0.03561*Higgs_amplify, {'extraweight':0.3944 ,"nevts":nevts_json_new["WminusHToTauTau_UncorrelatedDecay_Filtered"]}),
      ('HTT','VBFHToTauTau_UncorrelatedDecay_Filtered', "VBFH Filtered", 0.2558*Higgs_amplify, {'extraweight':0.4091 ,"nevts":nevts_json_new["VBFHToTauTau_UncorrelatedDecay_Filtered"]}),
      # DY LO samples
      ('DY', "DYto2L_M_50_madgraphMLM", "Drell-Yan 50", 5455.0 * kfactor_dy, { 'extraweight': dyweight, "nevts":nevts_json_new["DYto2L_M_50_madgraphMLM"]}),
      ('DY', "DYto2L_M_50_1J_madgraphMLM", "Drell-Yan 1J 50", 978.3 * kfactor_dy, {'extraweight': dyweight, "nevts":nevts_json_new["DYto2L_M_50_1J_madgraphMLM"]}),
      ('DY', "DYto2L_M_50_2J_madgraphMLM", "Drell-Yan 2J 50", 315.1 * kfactor_dy, {'extraweight': dyweight, "nevts":nevts_json_new["DYto2L_M_50_2J_madgraphMLM"]}),
      ('DY', "DYto2L_M_50_3J_madgraphMLM", "Drell-Yan 3J 50", 93.7 * kfactor_dy, {'extraweight': dyweight, "nevts":nevts_json_new["DYto2L_M_50_3J_madgraphMLM"]}),
      ('DY', "DYto2L_M_50_4J_madgraphMLM", "Drell-Yan 4J 50", 45.4 * kfactor_dy, {'extraweight': dyweight, "nevts":nevts_json_new["DYto2L_M_50_4J_madgraphMLM"]}),
      # DY 10-50 samples
      # ('DY', "DYto2L_M_10to50_amcatnloFXFX", "Drell-Yan 10-50 NLO", 20950.0, {'extraweight': dyweight, "nevts": nevts_json_new["DYto2L_M_10to50_amcatnloFXFX"]}),
      ('DY', "DYto2L_M_10to50_madgraphMLM", "Drell-Yan 10-50", 17380.0, {'extraweight': dyweight, "nevts": nevts_json_new["DYto2L_M_10to50_madgraphMLM"]}),
      # W + Jets LO samples
      ('WJ', "WtoLNu_madgraphMLM", "W + jets", 55300.0 * kfactor_wj, {"nevts":nevts_json_new["WtoLNu_madgraphMLM"]}),
      ('WJ', "WtoLNu_1J_madgraphMLM", "W + 1J", 9128.0 * kfactor_wj, {"nevts":nevts_json_new["WtoLNu_1J_madgraphMLM"]}),
      ('WJ', "WtoLNu_2J_madgraphMLM", "W + 2J", 2922.0 * kfactor_wj, {"nevts":nevts_json_new["WtoLNu_2J_madgraphMLM"]}),
      ('WJ', "WtoLNu_3J_madgraphMLM", "W + 3J", 861.3 * kfactor_wj, {"nevts":nevts_json_new["WtoLNu_3J_madgraphMLM"]}),
      ('WJ', "WtoLNu_4J_madgraphMLM", "W + 4J", 415.4 * kfactor_wj, {"nevts":nevts_json_new["WtoLNu_4J_madgraphMLM"]}),
      # TTbar
      ('TT', "TTto2L2Nu", "ttbar 2l2#nu", 80.9 * kfactor_ttbar, {'extraweight': ttweight, "nevts":nevts_json_new["TTto2L2Nu"]}),
      ('TT', "TTto4Q", "ttbar hadronic", 346.4 * kfactor_ttbar, {'extraweight': ttweight, "nevts":nevts_json_new["TTto4Q"]}),
      ('TT', "TTtoLNu2Q", "ttbar semileptonic", 334.8 * kfactor_ttbar, {'extraweight': ttweight, "nevts":nevts_json_new["TTtoLNu2Q"]}),
      #('TT', "TTtoLNu2Q_ext1", "ttbar semileptonic ext1", 334.8 * kfactor_ttbar, {'extraweight': ttweight, "nevts":nevts_json_new["TTtoLNu2Q_ext1"]}),
      #('TT', "TTto4Q_ext1", "ttbar hadronic ext1", 346.4 * kfactor_ttbar, {'extraweight': ttweight, "nevts":nevts_json_new["TTto4Q_ext1"]}),
      #('TT', "TTto2L2Nu_ext1", "ttbar 2l2#nu ext1", 80.9 * kfactor_ttbar, {'extraweight': ttweight, "nevts":nevts_json_new["TTto2L2Nu_ext1"]}),
      # Diboson
      ('VV', "WW", "WW", 80.23 * kfactor_ww, {"nevts":nevts_json_new["WW"]}),
      ('VV', "WZ", "WZ", 29.1 * kfactor_wz, {"nevts":nevts_json_new["WZ"]}),
      ('VV', "ZZ", "ZZ", 12.75 * kfactor_zz, {"nevts":nevts_json_new["ZZ"]}),
      # Single top NLO samples
      # ('ST', "ST_t_channel_top_4f_InclusiveDecays", "ST t-channel t", 123.8, {"nevts":nevts_json_new["ST_t_channel_top_4f_InclusiveDecays"]}),
      # ('ST', "ST_t_channel_antitop_4f_InclusiveDecays", "ST t-channel at", 75.47, {"nevts":nevts_json_new["ST_t_channel_antitop_4f_InclusiveDecays"]}),
      # ('ST', "ST_tW_top_2L2Nu", "ST tW semileptonic", 3.8, {"nevts":nevts_json_new["ST_tW_top_2L2Nu"]}),
      # ('ST', "ST_tW_top_2L2Nu_ext1", "ST tW 2l2#nu ext1", 3.8, {"nevts":nevts_json_new["ST_tW_top_2L2Nu_ext1"]}),
      # ('ST', "ST_tW_antitop_2L2Nu", "ST atW semileptonic", 3.8, {"nevts":nevts_json_new["ST_tW_antitop_2L2Nu"]}),
      # ('ST', "ST_tW_antitop_2L2Nu_ext1", "ST atW 2l2#nu ext1", 3.8, {"nevts":nevts_json_new["ST_tW_antitop_2L2Nu_ext1"]}),
      # ('ST', "ST_tW_top_LNu2Q", "ST tW top LNu2Q", 15.8, {"nevts":nevts_json_new["ST_tW_top_LNu2Q"]}),
      # ('ST', "ST_tW_top_LNu2Q_ext1", "ST tW top LNu2Q ext1", 15.8, {"nevts":nevts_json_new["ST_tW_top_LNu2Q_ext1"]}),
      # ('ST', "ST_tW_antitop_LNu2Q", "ST atW antitop LNu2Q", 15.9, {"nevts":nevts_json_new["ST_tW_antitop_LNu2Q"]}),
      # ('ST', "ST_tW_antitop_LNu2Q_ext1", "ST atW antitop LNu2Q ext1", 15.9, {"nevts":nevts_json_new["ST_tW_antitop_LNu2Q_ext1"]}),
      # Single top LO samples
      ('ST', "ST_tW_top_4Q", "ST tW top 4Q", 35.99, {"nevts":nevts_json_new["ST_tW_top_4Q"]}),
      # ('ST', "ST_tW_top_4Q_ext1", "ST tW top 4Q ext1", 35.99, {"nevts":nevts_json_new["ST_tW_top_4Q_ext1"]}),
      ('ST', "ST_tW_antitop_4Q", "ST tW antitop 4Q", 36.05, {"nevts":nevts_json_new["ST_tW_antitop_4Q"]}),
      # ('ST', "ST_tW_antitop_4Q_ext1", "ST tW antitop 4Q ext1", 36.05, {"nevts":nevts_json_new["ST_tW_antitop_4Q_ext1"]}),
      # Triboson 
      ('VVV', "WWW_4F", "WWW 4F", 0.2328, {"nevts":nevts_json_new["WWW_4F"]}),
      ('VVV', "WWZ_4F", "WWZ 4F", 0.1851, {"nevts":nevts_json_new["WWZ_4F"]}),
      ('VVV', "WZZ", "WZZ", 0.06206, {"nevts":nevts_json_new["WZZ"]}),
      ('VVV', "ZZZ", "ZZZ", 0.01591, {"nevts":nevts_json_new["ZZZ"]}),
      
      # DY NLO samples
      # ('DY', "DYto2L_M_50_amcatnloFXFX", "Drell-Yan 50 NLO", 6748.0 * kfactor_dy_NLO, {'extraweight': dyweight, "nevts": nevts_json_new["DYto2L_M_50_amcatnloFXFX"]}),
      # ('DY', "DYto2L_M_50_amcatnloFXFX_ext1", "Drell-Yan 50 NLO ext1", 6748.0 * kfactor_dy_NLO, {'extraweight': dyweight, "nevts": nevts_json_new["DYto2L_M_50_amcatnloFXFX_ext1"]}),
      # ('DY', "DYto2L_M_50_0J_amcatnloFXFX", "Drell-Yan 0J 50 NLO", 5364.0 * kfactor_dy_NLO, {'extraweight': dyweight, "nevts": nevts_json_new["DYto2L_M_50_0J_amcatnloFXFX"]}),
      # ('DY', "DYto2L_M_50_1J_amcatnloFXFX", "Drell-Yan 1J 50 NLO", 1019.0 * kfactor_dy_NLO, {'extraweight': dyweight, "nevts": nevts_json_new["DYto2L_M_50_1J_amcatnloFXFX"]}),
      # ('DY', "DYto2L_M_50_2J_amcatnloFXFX", "Drell-Yan 2J 50 NLO", 375.3 * kfactor_dy_NLO, {'extraweight': dyweight, "nevts": nevts_json_new["DYto2L_M_50_2J_amcatnloFXFX"]}),
      # ('DY', "DYto2L_M_50_PTLL_40to100_1J_amcatnloFXFX", "Drell-Yan 50 1J 40-100 NLO", 475.3 * kfactor_dy_NLO, {'extraweight': dyweight, "nevts": nevts_json_new["DYto2L_M_50_PTLL_40to100_1J_amcatnloFXFX"]}),
      # ('DY', "DYto2L_M_50_PTLL_100to200_1J_amcatnloFXFX", "Drell-Yan 50 1J 100-200 NLO", 45.42 * kfactor_dy_NLO, {'extraweight': dyweight, "nevts": nevts_json_new["DYto2L_M_50_PTLL_100to200_1J_amcatnloFXFX"]}),
      # ('DY', "DYto2L_M_50_PTLL_200to400_1J_amcatnloFXFX", "Drell-Yan 50 1J 200-400 NLO", 3.382 * kfactor_dy_NLO, {'extraweight': dyweight, "nevts": nevts_json_new["DYto2L_M_50_PTLL_200to400_1J_amcatnloFXFX"]}),
      # ('DY', "DYto2L_M_50_PTLL_400to600_1J_amcatnloFXFX", "Drell-Yan 50 1J 400-600 NLO", 0.1162 * kfactor_dy_NLO, {'extraweight': dyweight, "nevts": nevts_json_new["DYto2L_M_50_PTLL_400to600_1J_amcatnloFXFX"]}),
      # ('DY', "DYto2L_M_50_PTLL_600_1J_amcatnloFXFX", "Drell-Yan 50 1J 600+ NLO", 0.01392 * kfactor_dy_NLO, {'extraweight': dyweight, "nevts": nevts_json_new["DYto2L_M_50_PTLL_600_1J_amcatnloFXFX"]}),
      # ('DY', "DYto2L_M_50_PTLL_40to100_2J_amcatnloFXFX", "Drell-Yan 50 2J 40-100 NLO", 179.3 * kfactor_dy_NLO, {'extraweight': dyweight, "nevts": nevts_json_new["DYto2L_M_50_PTLL_40to100_2J_amcatnloFXFX"]}),
      # ('DY', "DYto2L_M_50_PTLL_100to200_2J_amcatnloFXFX", "Drell-Yan 50 2J 100-200 NLO", 51.68 * kfactor_dy_NLO, {'extraweight': dyweight, "nevts": nevts_json_new["DYto2L_M_50_PTLL_100to200_2J_amcatnloFXFX"]}),
      # ('DY', "DYto2L_M_50_PTLL_200to400_2J_amcatnloFXFX", "Drell-Yan 50 2J 200-400 NLO", 7.159 * kfactor_dy_NLO, {'extraweight': dyweight, "nevts": nevts_json_new["DYto2L_M_50_PTLL_200to400_2J_amcatnloFXFX"]}),
      # ('DY', "DYto2L_M_50_PTLL_400to600_2J_amcatnloFXFX", "Drell-Yan 50 2J 400-600 NLO", 0.4157 * kfactor_dy_NLO, {'extraweight': dyweight, "nevts": nevts_json_new["DYto2L_M_50_PTLL_400to600_2J_amcatnloFXFX"]}),
      # ('DY', "DYto2L_M_50_PTLL_600_2J_amcatnloFXFX", "Drell-Yan 50 2J 600+ NLO", 0.07019 * kfactor_dy_NLO, {'extraweight': dyweight, "nevts": nevts_json_new["DYto2L_M_50_PTLL_600_2J_amcatnloFXFX"]}),
    ]   

  else:
    LOG.throw(IOError,"Did not recognize era %r!"%(era))
  
  # OBSERVED DATA SAMPLES
  if   'tautau' in channel: dataset = "Tau_Run%d?"%year
  elif 'mutau'  in channel or 'mumu' in channel:
    if era=='2022_preEE':
      dataset = "*Muon_Run%d?"%year
      print("dataset = ", dataset) 
      #dataset = "SingleMuon_Run%d?"%year # need this one as well for C
      # TODO: need to somehow handle that we need SingleMuonC, MuonC, and MuonD for preEE
    elif era=='2022EE': dataset = "Muon_Run%d*" % year  
    elif era=='2022_postEE': dataset = "Muon_Run%d?"%year
    elif '2023' in era: dataset = "Muon*"
    else: dataset = "SingleMuon_Run%d?"%year
    
  elif 'etau' in channel or 'ee' in channel: 
    if (year==2018 or year==2022):
      dataset = "EGamma_Run%d?"%year
    elif '2023' in era: dataset = "EGamma*" 
    else: "SingleElectron_Run%d?"%year

  elif 'emu'    in channel: dataset = "SingleMuon_Run%d?"%year
  else:
    LOG.throw(IOError,"Did not recognize channel %r!"%(channel))
  datasample = ('Data',dataset) # GROUP, NAME
  
  # FILTER
  if filter:
    expsamples = [s for s in expsamples if any(f in s[0] for f in filter)]
  if vetoes:
    expsamples = [s for s in expsamples if not any(v in s[0] for v in vetoes)]
  
  # SAMPLE SET
  if weight=="":
    weight = ""
  #elif channel in ['mutau','etau']:
  if 'mutau' in channel or 'etau' in channel:
    weight = "sign(genweight)*trigweight*puweight*idisoweight_1*idweight_2*ltfweight_2*idweight_dm_2" # "*sign(genweight)" 
  elif channel in ['tautau','ditau']:
    weight = "genweight*trigweight*puweight*idweight_1*idweight_2*ltfweight_1*ltfweight_2"
  else: # mumu, emu, ...
    weight = "genweight*trigweight*puweight*idisoweight_1*idisoweight_2"
  for sf in rmsfs: # remove (old) SFs, e.g. for SF measurement
    weight = weight.replace(sf,"").replace("**","*").strip('*')
  for sf in addsfs:  # add extra SFs, e.g. for SF measurement
    weight = joinweights(weight,sf)
  kwargs.setdefault('weight',weight) # common weight for MC
  kwargs.setdefault('fname', fname)  # default filename pattern
  print(expsamples)
  sampleset = _getsampleset(datasample,expsamples,channel=channel,era=era,**kwargs)
  LOG.verb("weight = %r"%(weight),verbosity,1)
  
  # STITCH
  # Note: titles are set via STYLE.sample_titles
  #sampleset.stitch("W*LNu*",    incl='WJ',  name='WJ', cme=cme     ) # W + jets
  #sampleset.stitch("DYto2L-4Jets_MLL-50*", incl='DYJ', name="DY_M50", cme=cme ) # Drell-Yan, M > 50 GeV
  if '2022_postEE' in era or '2023' in era:
      sampleset.stitch("W*LNu*Jets*",    incl='WtoLNu-4Jets',  name='WJ', cme=cme) # W + jets
  elif '2022_preEE' in era:
      sampleset.stitch("W*LNu*Jets*",    incl='WJetsToLNu-4Jets',  name='WJ', cme=cme) # W + jets
  if '2022EE' in era:
    sampleset.stitch("W*LNu*",    incl='WtoLNu_madgraphMLM',  name='WJ', cme=cme) # W + jets
    sampleset.stitch("DYto2L*", incl='DYto2L_M_50_madgraphMLM', name="DY", cme=cme)
    #sampleset.stitch("DYto2L*amcatnloFXFX*", incl='DYto2L_M_50_amcatnloFXFX_ext1', name="DY", cme=cme) # Drell-Yan NLO
  else:
      sampleset.stitch("DYto2L-4Jets_MLL-50*", incl='DYto2L-4Jets_MLL-50', name="DY_M50", cme=cme)  
  # JOIN
  if '2022EE' in era:
    if 'HTT' in join:
      if Higgs_amplify==1:
        sampleset.join('HTT', '*UncorrelatedDecay*', name='Higgs')
      else:
        sampleset.join('HTT', '*UncorrelatedDecay*', name=f'{Higgs_amplify} x Higgs') 
    sampleset.join('VV','WZ','WW','ZZ','VVV','WWW_4F','WWZ_4F','WZZ','ZZZ',name='Multi-boson') # Multi-boson #     
  else:
    if 'VV' in join:
      sampleset.join('VV','WZ','WW','ZZ', name='VV' ) # Diboson
  sampleset.join('DY', name='DY' ) # Drell-Yan, M < 50 GeV + M > 50 GeV
  if 'TT' in join and era!='year':
    sampleset.join('TT', name='TT' ) # ttbar
  if 'ST' in join:
    sampleset.join('ST', name='ST' ) # single top
  if 'Top' in join:
    sampleset.join('TT','ST', name='Top' ) # ttbar + single top
  # sampleset.join('Multi-boson', 'DY', 'WJ', 'Top' ,name='MC')  # MC samples test
  sampleset.printtable(merged=True, split=True)
  
  # SPLIT
  # Note: titles are set via STYLE.sample_titles
  if split and channel.count('tau')==1:
    ZTT = STYLE.sample_titles.get('ZTT',"Z -> %s"%channel) # title
    if channel.count('tau')==1:
      ZTT = ZTT.replace("{l}","{mu}" if "mu" in channel else "{e}")
      GMR = "genmatch_2==5"
      GML = "genmatch_2>0 && genmatch_2<5"
      GMJ = "genmatch_2==0"
      GMF = "genmatch_2<5"
    elif channel.count('tau')==2:
      ZTT = ZTT.replace("{l}","{h}")
      GMR = "genmatch_1==5 && genmatch_2==5"
      GML = "(genmatch_1<5 || genmatch_2<5) && genmatch_1>0 && genmatch_2>0"
      GMJ = "(genmatch_1==0 || genmatch_2==0)"
      GMF = "(genmatch_1<5 || genmatch_2<5)"
    else:
      LOG.throw(IOError,"Did not recognize channel %r!"%(channel))
    if 'DM' in split: # split DY by decay modes
      samples.split('DY', [('ZTTDM0', ZTT+", h^{#pm}",                   GMR+" && dm_2==0"),
                           ('ZTTDM1', ZTT+", h^{#pm}h^{0}",              GMR+" && dm_2==1"),
                           ('ZTTDM10',ZTT+", h^{#pm}h^{#mp}h^{#pm}",     GMR+" && dm_2==10"),
                           ('ZTTDM11',ZTT+", h^{#pm}h^{#mp}h^{#pm}h^{0}",GMR+" && dm_2==11"),
                           ('ZL',GML),('ZJ',GMJ),])
    elif 'DY' in split:
      sampleset.split('DY',[('ZTT',ZTT,GMR),('ZL',GML),('ZJ',GMJ),])
    if 'TT' in split:
      sampleset.split('TT',[('TTT',GMR),('TTJ',GMF),('TTL',"genmatch_2>0 && genmatch_2<5")])
    if 'ST' in split:
      sampleset.split('ST',[('TTT',"genmatch_2==5 && genmatch_2<5"),('STJ',"genmatch_2<5")])
    # if 'TT' in split:
    #   sampleset.split('TT',[('TTT',GMR),('TTJ',GMF),])
  
  if table:
    sampleset.printtable(merged=True,split=True)
  print(">>> common weight: %r"%(weight))
  return sampleset
  
