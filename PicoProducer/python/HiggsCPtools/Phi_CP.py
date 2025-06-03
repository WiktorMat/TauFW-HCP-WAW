import uproot
import vector
import numpy as np
import warnings
warnings.simplefilter("ignore", UserWarning)


def read_root(file_path, tree_name):
    with uproot.open(file_path) as file:
        tree = file[tree_name]
        data = tree.arrays(library="np")
    return data

def calculate_zmf(p1, p2):
    total_p = p1 + p2
    beta = vector.array(
        {
            "px": -total_p.px / total_p.E,
            "py": -total_p.py / total_p.E,
            "pz": -total_p.pz / total_p.E,
        }
    )
    return beta

def get_perpendicular_component(v, ref):
    projection = (v.dot(ref)) * ref
    perpendicular = v - projection
    return perpendicular.unit()

def calculate(file_path, tree_name):
    data = read_root(file_path, tree_name)

    p1 = vector.array(
        {
            "pt": data["pt_1"],
            "eta": data["eta_1"],
            "phi": data["phi_1"],
            "M": data["m_1"],
        }
    )

    p2 = vector.array(
        {
            "pt": data["pt_2"],
            "eta": data["eta_2"],
            "phi": data["phi_2"],
            "M": data["m_2"],
        }
    )

    beta = calculate_zmf(p1, p2)

    lambda1 = vector.array(
        {
            "px": data["tau1_IP0"],
            "py": data["tau1_IP1"],
            "pz": data["tau1_IP2"],
            "E": np.zeros_like(data["tau1_IP0"]),
        }
    )

    lambda2 = vector.array(
        {
            "px": data["tau2_IP0"],
            "py": data["tau2_IP1"],
            "pz": data["tau2_IP2"],
            "E": np.zeros_like(data["tau2_IP0"]),
        }
    )

    # Boost to ZMF
    lambda1_zmf = lambda1.boost(beta)
    lambda2_zmf = lambda2.boost(beta)
    p1_zmf = p1.boost(beta)
    p2_zmf = p2.boost(beta)

    lambda1_spatial = lambda1_zmf.to_xyz()
    lambda2_spatial = lambda2_zmf.to_xyz()
    p1_spatial = p1_zmf.to_xyz().unit()
    p2_spatial = p2_zmf.to_xyz().unit()

    # Perpendicular component (and normalization)
    lambda1_perp = get_perpendicular_component(lambda1_spatial, p1_spatial)
    lambda2_perp = get_perpendicular_component(lambda2_spatial, p2_spatial)

    phi_cp = Calculate_PhiCP(lambda1_perp, lambda2_perp, p1_spatial, p2_spatial)

    return data, p1_zmf, p2_zmf, lambda1_perp, lambda2_perp, phi_cp

def Calculate_PhiCP(lambda1, lambda2, p1_zmf, p2_zmf):
    lambda1_3d = vector.array({"px": lambda1.px, "py": lambda1.py, "pz": lambda1.pz}).unit()
    lambda2_3d = vector.array({"px": lambda2.px, "py": lambda2.py, "pz": lambda2.pz}).unit()
    p2_3d = p2_zmf
    
    phi_zmf = np.arccos(lambda1_3d.dot(lambda2_3d))

    O_zmf = p2_3d.dot(lambda1_3d.cross(lambda2_3d))
    phi_cp = np.where(O_zmf >= 0, phi_zmf, 2 * np.pi - phi_zmf)

    return phi_cp

def save_to_root(output_file, data, lambda1, lambda2, p1, p2, phi_cp):
    new_data = {**data,
                "lambda1_zmf_px": lambda1.px,
                "lambda1_zmf_py": lambda1.py,
                "lambda1_zmf_pz": lambda1.pz,
                "lambda2_zmf_px": lambda2.px,
                "lambda2_zmf_py": lambda2.py,
                "lambda2_zmf_pz": lambda2.pz,
                "p1_zmf_px": p1.px,
                "p1_zmf_py": p1.py,
                "p1_zmf_pz": p1.pz,
                "p2_zmf_px": p2.px,
                "p2_zmf_py": p2.py,
                "p2_zmf_pz": p2.pz,
                "phi_cp": phi_cp}

    # Saving to new ROOT file
    with uproot.recreate(output_file) as file:
        file["tree"] = new_data

file_path = "/afs/cern.ch/user/w/wmatyszk/CMSSW_14_1_0_pre4/src/TauFW/PicoProducer/output/pico_mutau_2022_postEE_DYto2L_M_10to50_amcatnloFXFX.root"
output_file = "/afs/cern.ch/user/w/wmatyszk/CMSSW_14_1_0_pre4/src/TauFW/PicoProducer/output/pico_mutau_2022_postEE_DYto2L_M_10to50_amcatnloFXFX_phiCP.root"
tree_name = "tree;1"

data, p1_zmf, p2_zmf, lambda1_zmf, lambda2_zmf, phi_cp = calculate(file_path, tree_name)

#print("Sanity check of zmf:", np.mean(p1_zmf.px+p1_zmf.py+p1_zmf.pz+p2_zmf.px+p2_zmf.py+p2_zmf.pz))
print("Phi_CP:", phi_cp)

save_to_root(output_file, data, lambda1_zmf, lambda2_zmf, p1_zmf, p2_zmf, phi_cp)