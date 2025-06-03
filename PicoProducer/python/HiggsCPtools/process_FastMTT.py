import sys
sys.path.append('/afs/cern.ch/user/w/wmatyszk/CMSSW_14_1_0_pre4/src/FastMTT')
from FastMTT import FastMTT
from FastMTT_utils import *
import numpy as np
import uproot

file_path = "/afs/cern.ch/user/w/wmatyszk/CMSSW_14_1_0_pre4/src/TauFW/PicoProducer/output/pico_mutau_2022_postEE_DYto2L_M_10to50_amcatnloFXFX.root"
new_file_path = "/afs/cern.ch/user/w/wmatyszk/CMSSW_14_1_0_pre4/src/TauFW/PicoProducer/output/pico_mutau_2022_postEE_DYto2L_M_10to50_amcatnloFXFX_with_FastMTT.root"
tree_name = "tree"

# Open the original file and read all branches
with uproot.open(file_path) as file:
    tree = file[tree_name]
    data = tree.arrays(library="np")

# Access the numpy arrays
shape = data["pt_1"].shape

measuredTauLeptons = np.array([
    [np.full(shape, 3), data["pt_1"], data["eta_1"], data["phi_1"], data["m_1"], np.full(shape, -1)],
    [np.full(shape, 1), data["pt_2"], data["eta_2"], data["phi_2"], data["m_2"], data["dm_2"]]
])

measuredTauLeptons = np.transpose(measuredTauLeptons, (2, 0, 1))

covMET = np.array([[data["metcov00"], data["metcov01"]], [data["metcov01"], data["metcov11"]]])

covMET = np.transpose(covMET, (2, 0, 1))

METx = data["met"] * np.cos(data["metphi"])
METy = data["met"] * np.sin(data["metphi"])

print("Input shapes: ", measuredTauLeptons.shape, covMET.shape, METx.shape, METy.shape)

fMTT = FastMTT.FastMTT()
fMTT.run(measuredTauLeptons, METx, METy, covMET)
mFast = fMTT.mass
ptFast = fMTT.pt
mFast, ptFast, tau1pt, tau2pt = process_FastMTT(measuredTauLeptons, METx, METy, covMET, batch_size = 10, num_workers = 8)
print("Output shape: ", mFast.shape, ptFast.shape)
print("Output means: ", np.mean(mFast), np.mean(ptFast))

# Add new branches to the data dictionary
data["mFast"] = mFast
data["ptFast"] = ptFast
data["tau1ptFast"] = tau1pt
data["tau2ptFast"] = tau2pt

# Save the results to a new ROOT file
with uproot.recreate(new_file_path) as file:
    file["tree"] = data