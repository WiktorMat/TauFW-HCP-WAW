from TauFW.PicoProducer.storage.Sample import MC as M
from TauFW.PicoProducer.storage.Sample import Data as D

storage  = "/eos/cms/store/group/phys_higgs/HLepRare/skim_2024_v2/Run3_2022EE/$DAS"
url      = "root://cms-xrd-global.cern.ch/"
filelist = None 

samples  = [
    # Drell-Yan NLO samples
    M('DY','DYto2L_M_10to50_amcatnloFXFX', "/DYto2L_M_10to50_amcatnloFXFX", store=storage, url=url, files=filelist, opts="useT1=False,zpt=True"),
    M('DY','DYto2L_M_50_amcatnloFXFX', "/DYto2L_M_50_amcatnloFXFX", store=storage, url=url, files=filelist, opts="useT1=False,zpt=True"),
    M('DY','DYto2L_M_50_amcatnloFXFX_ext1', "/DYto2L_M_50_amcatnloFXFX_ext1", store=storage, url=url, files=filelist, opts="useT1=False,zpt=True"),
    M('DY','DYto2L_M_50_0J_amcatnloFXFX', "/DYto2L_M_50_0J_amcatnloFXFX", store=storage, url=url, files=filelist, opts="useT1=False,zpt=True"),
    M('DY','DYto2L_M_50_1J_amcatnloFXFX', "/DYto2L_M_50_1J_amcatnloFXFX", store=storage, url=url, files=filelist, opts="useT1=False,zpt=True"),
    M('DY','DYto2L_M_50_2J_amcatnloFXFX', "/DYto2L_M_50_2J_amcatnloFXFX", store=storage, url=url, files=filelist, opts="useT1=False,zpt=True"),
    M('DY','DYto2L_M_50_PTLL_40to100_1J_amcatnloFXFX', "/DYto2L_M_50_PTLL_40to100_1J_amcatnloFXFX", store=storage, url=url, files=filelist, opts="useT1=False,zpt=True"),
    M('DY','DYto2L_M_50_PTLL_100to200_1J_amcatnloFXFX', "/DYto2L_M_50_PTLL_100to200_1J_amcatnloFXFX", store=storage, url=url, files=filelist, opts="useT1=False,zpt=True"),
    M('DY','DYto2L_M_50_PTLL_200to400_1J_amcatnloFXFX', "/DYto2L_M_50_PTLL_200to400_1J_amcatnloFXFX", store=storage, url=url, files=filelist, opts="useT1=False,zpt=True"),
    M('DY','DYto2L_M_50_PTLL_400to600_1J_amcatnloFXFX', "/DYto2L_M_50_PTLL_400to600_1J_amcatnloFXFX", store=storage, url=url, files=filelist, opts="useT1=False,zpt=True"),
    M('DY','DYto2L_M_50_PTLL_600_1J_amcatnloFXFX', "/DYto2L_M_50_PTLL_600_1J_amcatnloFXFX", store=storage, url=url, files=filelist, opts="useT1=False,zpt=True"),
    M('DY','DYto2L_M_50_PTLL_40to100_2J_amcatnloFXFX', "/DYto2L_M_50_PTLL_40to100_2J_amcatnloFXFX", store=storage, url=url, files=filelist, opts="useT1=False,zpt=True"),
    M('DY','DYto2L_M_50_PTLL_100to200_2J_amcatnloFXFX', "/DYto2L_M_50_PTLL_100to200_2J_amcatnloFXFX", store=storage, url=url, files=filelist, opts="useT1=False,zpt=True"),
    M('DY','DYto2L_M_50_PTLL_200to400_2J_amcatnloFXFX', "/DYto2L_M_50_PTLL_200to400_2J_amcatnloFXFX", store=storage, url=url, files=filelist, opts="useT1=False,zpt=True"),
    M('DY','DYto2L_M_50_PTLL_400to600_2J_amcatnloFXFX', "/DYto2L_M_50_PTLL_400to600_2J_amcatnloFXFX", store=storage, url=url, files=filelist, opts="useT1=False,zpt=True"),
    M('DY','DYto2L_M_50_PTLL_600_2J_amcatnloFXFX', "/DYto2L_M_50_PTLL_600_2J_amcatnloFXFX", store=storage, url=url, files=filelist, opts="useT1=False,zpt=True"),

    
    # Drell-Yan LO samples
    M('DY','DYto2L_M_10to50_madgraphMLM', "/DYto2L_M_10to50_madgraphMLM", store=storage, url=url, files=filelist, opts="useT1=False,zpt=True"),
    M('DY','DYto2L_M_50_madgraphMLM', "/DYto2L_M_50_madgraphMLM", store=storage, url=url, files=filelist, opts="useT1=False,zpt=True"),
    M('DY','DYto2L_M_50_madgraphMLM_ext1', "/DYto2L_M_50_madgraphMLM_ext1", store=storage, url=url, files=filelist, opts="useT1=False,zpt=True"),
    M('DY','DYto2L_M_50_1J_madgraphMLM', "/DYto2L_M_50_1J_madgraphMLM", store=storage, url=url, files=filelist, opts="useT1=False,zpt=True"),
    M('DY','DYto2L_M_50_2J_madgraphMLM', "/DYto2L_M_50_2J_madgraphMLM", store=storage, url=url, files=filelist, opts="useT1=False,zpt=True"),
    M('DY','DYto2L_M_50_3J_madgraphMLM', "/DYto2L_M_50_3J_madgraphMLM", store=storage, url=url, files=filelist, opts="useT1=False,zpt=True"),
    M('DY','DYto2L_M_50_4J_madgraphMLM', "/DYto2L_M_50_4J_madgraphMLM", store=storage, url=url, files=filelist, opts="useT1=False,zpt=True"),

    
    # W + Jets LO samples
    M('WJ','WtoLNu_madgraphMLM', "/WtoLNu_madgraphMLM", store=storage, url=url, files=filelist, opts="useT1=False"),
    M('WJ','WtoLNu_1J_madgraphMLM', "/WtoLNu_1J_madgraphMLM", store=storage, url=url, files=filelist, opts="useT1=False"),
    M('WJ','WtoLNu_madgraphMLM_ext1', "/WtoLNu_madgraphMLM_ext1", store=storage, url=url, files=filelist, opts="useT1=False"),
    M('WJ','WtoLNu_2J_madgraphMLM', "/WtoLNu_2J_madgraphMLM", store=storage, url=url, files=filelist, opts="useT1=False"),
    M('WJ','WtoLNu_3J_madgraphMLM', "/WtoLNu_3J_madgraphMLM", store=storage, url=url, files=filelist, opts="useT1=False"),
    M('WJ','WtoLNu_4J_madgraphMLM', "/WtoLNu_4J_madgraphMLM", store=storage, url=url, files=filelist, opts="useT1=False"),
    
    # TTbar
    M('TT','TTto2L2Nu', "/TTto2L2Nu", store=storage, url=url, files=filelist, opts="useT1=False,toppt=True"),
    M('TT','TTto4Q', "/TTto4Q", store=storage, url=url, files=filelist, opts="useT1=False,toppt=True"),
    M('TT','TTto2L2Nu_ext1', "/TTto2L2Nu_ext1", store=storage, url=url, files=filelist, opts="useT1=False,toppt=True"),
    M('TT','TTtoLNu2Q', "/TTtoLNu2Q", store=storage, url=url, files=filelist, opts="useT1=False,toppt=True"),
    M('TT','TTtoLNu2Q_ext1', "/TTtoLNu2Q_ext1", store=storage, url=url, files=filelist, opts="useT1=False,toppt=True"),
    M('TT','TTto4Q_ext1', "/TTto4Q_ext1", store=storage, url=url, files=filelist, opts="useT1=False,toppt=True"),

    
    # Diboson
    M('VV','WW', "/WW", store=storage, url=url, files=filelist, opts="useT1=False"),
    M('VV','WZ', "/WZ", store=storage, url=url, files=filelist, opts="useT1=False"),
    M('VV','ZZ', "/ZZ", store=storage, url=url, files=filelist, opts="useT1=False"),
    
    # Triboson
    ##M('VVV','WWW_4F', "/WWW_4F", store=storage, url=url, files=filelist, opts="useT1=False"),
    ##M('VVV','WWZ_4F', "/WWZ_4F", store=storage, url=url, files=filelist, opts="useT1=False"),
    ##M('VVV','WZZ', "/WZZ", store=storage, url=url, files=filelist, opts="useT1=False"),
    ##M('VVV','ZZZ', "/ZZZ", store=storage, url=url, files=filelist, opts="useT1=False"),

    
    # Single top
    M('ST','ST_t_channel_top_4f_InclusiveDecays', "/ST_t_channel_top_4f_InclusiveDecays", store=storage, url=url, files=filelist, opts="useT1=False"),
    M('ST','ST_t_channel_antitop_4f_InclusiveDecays', "/ST_t_channel_antitop_4f_InclusiveDecays", store=storage, url=url, files=filelist, opts="useT1=False"),
    M('ST','ST_tW_top_2L2Nu', "/ST_tW_top_2L2Nu", store=storage, url=url, files=filelist, opts="useT1=False"),
    M('ST','ST_tW_top_2L2Nu_ext1', "/ST_tW_top_2L2Nu_ext1", store=storage, url=url, files=filelist, opts="useT1=False"),
    M('ST','ST_tW_antitop_2L2Nu', "/ST_tW_antitop_2L2Nu", store=storage, url=url, files=filelist, opts="useT1=False"),
    M('ST','ST_tW_antitop_2L2Nu_ext1', "/ST_tW_antitop_2L2Nu_ext1", store=storage, url=url, files=filelist, opts="useT1=False"),
    M('ST','ST_tW_top_4Q', "/ST_tW_top_4Q", store=storage, url=url, files=filelist, opts="useT1=False"),
    M('ST','ST_tW_top_4Q_ext1', "/ST_tW_top_4Q_ext1", store=storage, url=url, files=filelist, opts="useT1=False"),
    M('ST','ST_tW_antitop_4Q', "/ST_tW_antitop_4Q", store=storage, url=url, files=filelist, opts="useT1=False"),
    M('ST','ST_tW_antitop_4Q_ext1', "/ST_tW_antitop_4Q_ext1", store=storage, url=url, files=filelist, opts="useT1=False"),
    M('ST','ST_tW_top_LNu2Q', "/ST_tW_top_LNu2Q", store=storage, url=url, files=filelist, opts="useT1=False"),
    M('ST','ST_tW_top_LNu2Q_ext1', "/ST_tW_top_LNu2Q_ext1", store=storage, url=url, files=filelist, opts="useT1=False"),
    M('ST','ST_tW_antitop_LNu2Q', "/ST_tW_antitop_LNu2Q", store=storage, url=url, files=filelist, opts="useT1=False"),
    M('ST','ST_tW_antitop_LNu2Q_ext1', "/ST_tW_antitop_LNu2Q_ext1", store=storage, url=url, files=filelist, opts="useT1=False"),

    # Data
    D('Data','EGamma_Run2022G', "/EGamma_Run2022G", store=storage, url=url, files=filelist, opts="useT1=False", channels=["skim*",'etau','ee']),
    D('Data','Tau_Run2022E', "/Tau_Run2022E", store=storage, url=url, files=filelist, opts="useT1=False"),
    D('Data','Tau_Run2022F', "/Tau_Run2022F", store=storage, url=url, files=filelist, opts="useT1=False"),
    D('Data','Tau_Run2022G', "/Tau_Run2022G", store=storage, url=url, files=filelist, opts="useT1=False"),
    D('Data','Muon_Run2022E', "/Muon_Run2022E", store=storage, url=url, files=filelist, opts="useT1=False"),
    D('Data','Muon_Run2022F', "/Muon_Run2022F", store=storage, url=url, files=filelist, opts="useT1=False"),
    D('Data','Muon_Run2022G', "/Muon_Run2022G", store=storage, url=url, files=filelist, opts="useT1=False"),
    D('Data','MuonEG_Run2022E', "/MuonEG_Run2022E", store=storage, url=url, files=filelist, opts="useT1=False"),
    D('Data','MuonEG_Run2022F', "/MuonEG_Run2022F", store=storage, url=url, files=filelist, opts="useT1=False"),
    D('Data','MuonEG_Run2022G', "/MuonEG_Run2022G", store=storage, url=url, files=filelist, opts="useT1=False"),
]

