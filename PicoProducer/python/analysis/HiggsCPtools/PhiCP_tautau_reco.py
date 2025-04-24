import vector
import numpy as np
from TauFW.PicoProducer.analysis.HiggsCPtools.Utils import *

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

def PhiCP_tautau_reco(tau1, tau2, tau1Prod, tau2Prod):
    p1, lambda1, y1 = get_pion_and_lambda(tau1, tau1Prod)
    if p1 is None or lambda1 is None:
        return -1

    p2, lambda2, y2 = get_pion_and_lambda(tau2, tau2Prod)
    if p2 is None or lambda2 is None:
        return -1
    
    beta_zmf = find_restframe(p1+p2)

    lambda1_zmf = lambda1.boost(beta_zmf)
    lambda2_zmf = lambda2.boost(beta_zmf)
    p1_zmf = p1.boost(beta_zmf)
    p2_zmf = p2.boost(beta_zmf)

    lambda1_spatial = lambda1_zmf.to_xyz()
    lambda2_spatial = lambda2_zmf.to_xyz()
    p1_spatial = p1_zmf.to_xyz().unit()
    p2_spatial = p2_zmf.to_xyz().unit()

    # Perpendicular component (and normalization)
    lambda1_perp = get_perpendicular_component(lambda1_spatial, p1_spatial)
    lambda2_perp = get_perpendicular_component(lambda2_spatial, p2_spatial)

    y = y1*y2

    if tau1.charge == 1 and tau2.charge == -1:
        phi_cp = Calculate_PhiCP(lambda1_perp, lambda2_perp, p1_spatial, p2_spatial, y)
    elif tau1.charge == -1 and tau2.charge == 1:
        phi_cp = Calculate_PhiCP(lambda2_perp, lambda1_perp, p2_spatial, p1_spatial, y)
    else:
        return -1
    
    if isinstance(phi_cp, np.ndarray):
        phi_cp = phi_cp.item()
    return phi_cp

def Calculate_PhiCP(lambda1, lambda2, p1_zmf, p2_zmf, y):
    
    phi_zmf = np.arccos(lambda1.dot(lambda2))

    O_zmf = p2_zmf.dot(lambda1.cross(lambda2))
    phi_cp = np.where(O_zmf >= 0, phi_zmf, 2 * np.pi - phi_zmf)

    if y < 0:
        phi_cp += np.pi
        phi_cp %= 2 * np.pi

    return phi_cp

def find_restframe(momentum):
        beta = {
            "px": float(-momentum.px / momentum.E),
            "py": float(-momentum.py / momentum.E),
            "pz": float(-momentum.pz / momentum.E),
        }
        return vector.obj(**beta)


def get_pion_and_lambda(tau, tau_products):
    if tau.decayMode in [0, 1]:
        best_p = ZERO_4VECTOR
        for product in tau_products:
            if abs(product.pdgId) in [11, 13, 211, 10211]:
                test_p = get_chargedPion_4momentum(product)
                if test_p.E > best_p.E:
                    best_p = test_p

        if best_p.E == 0:
            return None, None, None

        if tau.decayMode == 0:
            lambda_vec = get_lambda(tau)
            y = 1
            if lambda_vec.mag == 0: ###TEMPORARY###
                print("No impact parameter!")
                return None, None, None
        elif tau.decayMode == 1:
            lambda_vec = get_neutralPion_4momentum(tau_products)
            y = best_p.E - lambda_vec.E

        return best_p, lambda_vec, y

    elif tau.decayMode == 10:
        p, lambda_vec = get_charged_pion_from_rho_decay(tau_products, tau.charge)
        if p is None:
            return None, None, None
        y = p.E - lambda_vec.E
        return p, lambda_vec, y

    else:
        return None, None, None
    
def get_neutralPion_4momentum(tau_products):
    energy = 0.0
    leading_momentum = [0.0, 0.0, 0.0] #normalized px, py, pz
    leading_energy = 0.0
    
    for product in tau_products:
        if abs(product.pdgId) == 11:
            product_energy = np.sqrt(product.pt**2 * np.cosh(product.eta)**2+ELECTRON_MASS**2)
            energy += product_energy
            if product_energy > leading_energy:
                leading_energy = product_energy
                leading_momentum[0] = np.cos(product.phi)/np.cosh(product.eta)
                leading_momentum[1] = np.sin(product.phi)/np.cosh(product.eta)
                leading_momentum[2] = np.tanh(product.eta)
        elif product.pdgId == 22:
            product_energy = product.pt * np.cosh(product.eta)
            energy += product_energy
            if product_energy > leading_energy:
                leading_energy = product_energy
                leading_momentum[0] = np.cos(product.phi)/np.cosh(product.eta)
                leading_momentum[1] = np.sin(product.phi)/np.cosh(product.eta)
                leading_momentum[2] = np.tanh(product.eta)
    total_momentum = np.sqrt(energy**2 - PI_ZERO_MASS**2)
    leading_momentum[0] *= total_momentum
    leading_momentum[1] *= total_momentum
    leading_momentum[2] *= total_momentum
    
    return vector.array(
    {
        "px": [leading_momentum[0]],
        "py": [leading_momentum[1]],
        "pz": [leading_momentum[2]],
        "E": [energy]
    }
)

def get_charged_pion_from_rho_decay(tau_products, tau_charge):
    pi_pluses = [p for p in tau_products if p.pdgId == 211]
    pi_minuses = [p for p in tau_products if p.pdgId == -211]

    best_pair = None
    min_mass_diff = float("inf")

    for pi_plus in pi_pluses:
        pi_plus_p = np.array([
            pi_plus.pt * np.cos(pi_plus.phi),
            pi_plus.pt * np.sin(pi_plus.phi),
            pi_plus.pt * np.sinh(pi_plus.eta)
        ])
        pi_plus_E = np.sqrt(pi_plus.pt**2 * np.cosh(pi_plus.eta)**2 + PI_PLUS_MASS**2)

        for pi_minus in pi_minuses:
            pi_minus_p = np.array([
                pi_minus.pt * np.cos(pi_minus.phi),
                pi_minus.pt * np.sin(pi_minus.phi),
                pi_minus.pt * np.sinh(pi_minus.eta)
            ])
            pi_minus_E = np.sqrt(pi_minus.pt**2 * np.cosh(pi_minus.eta)**2 + PI_PLUS_MASS**2)

            # Invariant mass of 'Rho_0 system' candidate
            rho_p = pi_plus_p + pi_minus_p
            rho_E = pi_plus_E + pi_minus_E
            rho_mass = np.sqrt(rho_E**2 - np.dot(rho_p, rho_p))

            #print(f"ρ⁰ mass candidate: {rho_mass:.4f} GeV")

            # Check wich mass is closest to Rho(770)
            mass_diff = abs(rho_mass - RHO_ZERO_MASS)
            if mass_diff < min_mass_diff:
                min_mass_diff = mass_diff
                best_pair = (
                    vector.obj(px=pi_plus_p[0], py=pi_plus_p[1], pz=pi_plus_p[2], E=pi_plus_E),
                    vector.obj(px=pi_minus_p[0], py=pi_minus_p[1], pz=pi_minus_p[2], E=pi_minus_E)
                )

    if best_pair is None:
        print("No valid pion pairs found!")
        return None, None

    return best_pair if tau_charge == 1 else best_pair[::-1]