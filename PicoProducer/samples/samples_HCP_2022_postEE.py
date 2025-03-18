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
    
    # Drell-Yan LO samples
    M('DY','DYto2L_M_10to50_madgraphMLM', "/DYto2L_M_10to50_madgraphMLM", store=storage, url=url, files=filelist, opts="useT1=False,zpt=True"),
    M('DY','DYto2L_M_50_madgraphMLM', "/DYto2L_M_50_madgraphMLM", store=storage, url=url, files=filelist, opts="useT1=False,zpt=True"),
    
    # W + Jets LO samples
    M('WJ','WtoLNu_madgraphMLM', "/WtoLNu_madgraphMLM", store=storage, url=url, files=filelist, opts="useT1=False"),
    M('WJ','WtoLNu_1J_madgraphMLM', "/WtoLNu_1J_madgraphMLM", store=storage, url=url, files=filelist, opts="useT1=False"),
    
    # TTbar
    M('TT','TTto2L2Nu', "/TTto2L2Nu", store=storage, url=url, files=filelist, opts="useT1=False,toppt=True"),
    M('TT','TTto4Q', "/TTto4Q", store=storage, url=url, files=filelist, opts="useT1=False,toppt=True"),
    
    # Diboson
    M('VV','WW', "/WW", store=storage, url=url, files=filelist, opts="useT1=False"),
    M('VV','WZ', "/WZ", store=storage, url=url, files=filelist, opts="useT1=False"),
    M('VV','ZZ', "/ZZ", store=storage, url=url, files=filelist, opts="useT1=False"),
    
    # Triboson
    M('VVV','WWW_4F', "/WWW_4F", store=storage, url=url, files=filelist, opts="useT1=False"),
    M('VVV','WWZ_4F', "/WWZ_4F", store=storage, url=url, files=filelist, opts="useT1=False"),
    
    # Single top
    M('ST','ST_t_channel_top_4f_InclusiveDecays', "/ST_t_channel_top_4f_InclusiveDecays", store=storage, url=url, files=filelist, opts="useT1=False"),
    M('ST','ST_t_channel_antitop_4f_InclusiveDecays', "/ST_t_channel_antitop_4f_InclusiveDecays", store=storage, url=url, files=filelist, opts="useT1=False"),
    
    # Data
    D('Data','EGamma_Run2022E', "/EGamma_Run2022E", store=storage, url=url, files=filelist, opts="useT1=False", channels=["skim*",'etau','ee']),
    D('Data','EGamma_Run2022F', "/EGamma_Run2022F", store=storage, url=url, files=filelist, opts="useT1=False", channels=["skim*",'etau','ee']),
]
