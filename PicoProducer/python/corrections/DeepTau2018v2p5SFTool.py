# Author: Hagop Awedikian (May 2025)
# Description: DeepTau2018v2p5SFTool class for tau SFs and TES from correctionlib
import os
from correctionlib import _core

class DeepTau2018v2p5SFTool:
    YEAR_TO_JSON = {
        "2018UL": "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/TAU/2018_UL/tau_DeepTau2018v2p5_2018_UL.json.gz",
        "2022_preEE": "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/TAU/2022_Summer22/tau_DeepTau2018v2p5_2022_preEE.json.gz",
        "2022EE": "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/TAU/2022_Summer22EE/tau_DeepTau2018v2p5_2022_postEE.json.gz",
        "2022_postEE": "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/TAU/2022_Summer22EE/tau_DeepTau2018v2p5_2022_postEE.json.gz",
        "2023": "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/TAU/2023_Summer23/tau_DeepTau2018v2p5_2023_preBPix.json.gz",
        "2023BPix": "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/TAU/2023_Summer23BPix/tau_DeepTau2018v2p5_2023_postBPix.json.gz",
    }

    def __init__(self, year):
        year = str(year)
        if year not in self.YEAR_TO_JSON:
            raise ValueError(f"Unknown year '{year}'. Available: {list(self.YEAR_TO_JSON.keys())}")
        fname = self.YEAR_TO_JSON[year]
        if fname.endswith(".json.gz"):
            import gzip
            with gzip.open(fname, 'rt') as file:
                data = file.read().strip()
            self.cset = _core.CorrectionSet.from_string(data)
        else:
            self.cset = _core.CorrectionSet.from_file(fname)

    def sf_vsjet(self, pt, dm, genmatch, wp_vsjet="Medium", wp_vse="VVLoose", syst="nom", mode="pt"):
        return self.cset["DeepTau2018v2p5VSjet"].evaluate(pt, dm, genmatch, wp_vsjet, wp_vse, syst, mode)

    def sf_vse(self, eta, dm, genmatch, wp_vse="VVLoose", syst="nom"):
        return self.cset["DeepTau2018v2p5VSe"].evaluate(eta, dm, genmatch, wp_vse, syst)

    def sf_vsmu(self, eta, genmatch, wp_vsmu="Tight", syst="nom"):
        return self.cset["DeepTau2018v2p5VSmu"].evaluate(eta, genmatch, wp_vsmu, syst)

    def tes(self, pt, eta, dm, genmatch, wp_vsjet="Medium", wp_vse="VVLoose", syst="nom"):
        return self.cset["tau_energy_scale"].evaluate(pt, eta, dm, genmatch, "DeepTau2018v2p5", wp_vsjet, wp_vse, syst)

    def sf_trigger(self, pt, eta, dm, genmatch, wp="Medium", syst="nom"):
        return self.cset["tau_trigger"].evaluate(pt, eta, dm, genmatch, wp, syst)
