# test_deeptau2018v2p5_sf.py for testing DeepTau2018v2p5 scale factors and energy scales

import os
import gzip
from correctionlib import _core
from TauFW.PicoProducer.corrections.DeepTau2018v2p5SFTool import DeepTau2018v2p5SFTool

fname = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/TAU/2022_Summer22EE/tau_DeepTau2018v2p5_2022_postEE.json.gz"

# tau variables
tau_pt = 45.0
tau_eta = 0.5
tau_dm = 11
tau_genmatch = 5
wp_vsjet = "Medium"
wp_vse = "VVLoose"
syst = "nom"

#Method 1: Directly from correctionlib CorrectionSet 
if fname.endswith(".json.gz"):
    with gzip.open(fname, 'rt') as file:
        data = file.read().strip()
    cset = _core.CorrectionSet.from_string(data)
else:
    cset = _core.CorrectionSet.from_file(fname)

sf_vsjet_direct = cset["DeepTau2018v2p5VSjet"].evaluate(
    tau_pt, tau_dm, tau_genmatch, wp_vsjet, wp_vse, syst, "pt"
)
tes_direct = cset["tau_energy_scale"].evaluate(
    tau_pt, tau_eta, tau_dm, tau_genmatch, "DeepTau2018v2p5", wp_vsjet, wp_vse, syst
)

print("Direct correctionlib:")
print("  SF vsjet:", sf_vsjet_direct)
print("  TES:", tes_direct)

#Method 2: Using DeepTau2018v2p5SFTool 
tool = DeepTau2018v2p5SFTool("2022EE")
sf_vsjet_tool = tool.sf_vsjet(tau_pt, tau_dm, tau_genmatch, wp_vsjet, wp_vse, syst, "pt")
tes_tool = tool.tes(tau_pt, tau_eta, tau_dm, tau_genmatch, wp_vsjet, wp_vse, syst)

print("Via DeepTau2018v2p5SFTool:")
print("  SF vsjet:", sf_vsjet_tool)
print("  TES:", tes_tool)