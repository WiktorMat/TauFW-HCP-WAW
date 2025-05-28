import math
import ROOT
import numpy as np
from TauFW.PicoProducer.analysis.HiggsCPtools.Utils import *
from TauFW.PicoProducer.analysis.HiggsCPtools.Kinematics_reconstructions import *
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

MASS_TAU = 1.77686  # GeV/c^2

tau_lifetime_sec = 0.287 * 1e-12 # in seconds
h_bar = 6.582119569e-25 # in GeV*s
GeV_to_cm = 5.06e13

tau_lifetime = tau_lifetime_sec / h_bar / GeV_to_cm # in cm^-1

def Gotfried_Jackson_angle(E_tau, p_tau, E_vis, m_vis, p_vis): #p standing for total momentum, E for energy, m for mass
    cosGJ = (2*E_tau*E_vis - m_vis**2 - MASS_TAU**2) / 2 / p_tau / p_vis
    if cosGJ > 1:
        cosGJ = 1
    elif cosGJ < -1:
        cosGJ = -1
    return np.arccos(cosGJ)

def Tau_momentum_reconstruction(tau, tauP4_fMTT, tauProd):
    #4-vector from FastMTT
    tau_px, tau_py, tau_pz, tau_E = tauP4_fMTT
    tau_total_momentum = math.sqrt(tau_px**2 + tau_py**2 + tau_pz**2)

    vis_total_momentum = tau.pt * math.cosh(tau.eta)
    vis_energy = math.sqrt(vis_total_momentum**2 + tau.mass**2)

    GJ = Gotfried_Jackson_angle(tau_E, tau_total_momentum, vis_energy, tau.mass, vis_total_momentum)

    # Best charged pion from possible candidates
    chargedPion_momentum = ROOT.TLorentzVector()
    for product in tauProd:
        if abs(product.pdgId) in [11, 13, 211, 10211]:
            test_p = get_chargedPion_4momentum(product)
            if test_p.E() > chargedPion_momentum.E():
                chargedPion_momentum = test_p

    chargedPion_3momentum = chargedPion_momentum.Vect()

    # Vector IP
    IP_vec = ROOT.TVector3(tau.IPx, tau.IPy, tau.IPz)
    if IP_vec.Mag() == 0:
        print("No impact parameter!")
        return None, None, None

    # \pi - IP plane
    pion_IP_plane = chargedPion_3momentum.Cross(IP_vec)
    pion_IP_plane = pion_IP_plane.Unit()

    tau_3momentum = ROOT.TVector3(tau_px, tau_py, tau_pz)
    sine = abs(pion_IP_plane.Dot(tau_3momentum.Unit()))
    alfa = math.asin(sine)

    if alfa >= GJ:
        rotation_axis = pion_IP_plane.Cross(tau_3momentum).Unit()

        tau1 = rotate_vector(tau_3momentum, rotation_axis, GJ)
        tau2 = rotate_vector(tau_3momentum, rotation_axis, -GJ)

        dot1 = tau1.Dot(pion_IP_plane)
        dot2 = tau2.Dot(pion_IP_plane)

        tau_reconstructed = tau1 if dot1 < dot2 else tau2
        worse_tau = tau2 if dot1 < dot2 else tau1

    else:
        P = chargedPion_3momentum.Unit()
        R = get_perpendicular_component(IP_vec, P)

        #Cos theta = <(aP+bR), V> = a*pv + b*rv
        #pv = <P, V>
        #rv = <R, V>
        #V - visible tau 3-momentum
        #We are looking for a and b

        pv = P.Dot(tau_3momentum)
        rv = R.Dot(tau_3momentum)
        M = tau_3momentum.Mag()
        cosGJ = math.cos(GJ)

        # Second degree equation coefficients
        A = 1 + (pv / rv)**2
        B = -2 * (pv / rv) * (M**2 * cosGJ / rv)
        C = (M**2 * cosGJ / rv)**2 - M**2

        delta = B**2 - 4 * A * C
        if delta < 0:
            print("Delta < 0!")
            return None, None , None

        sqrt_delta = math.sqrt(delta)
        a1 = (-B + sqrt_delta) / (2 * A)
        a2 = (-B - sqrt_delta) / (2 * A)

        b1 = (M**2 * cosGJ - a1 * pv) / rv
        b2 = (M**2 * cosGJ - a2 * pv) / rv

        tau1 = P * a1 + R * b1
        tau2 = P * a2 + R * b2

        tau1_unit = tau1.Unit()
        tau2_unit = tau2.Unit()
        IP_unit = IP_vec.Unit()

        L1 = IP_vec.Mag() / tau1_unit.Dot(IP_unit)
        L2 = IP_vec.Mag() / tau2_unit.Dot(IP_unit)

        if L1 < 0 or L2 < 0:
            tau_reconstructed = tau1 if L1 > L2 else tau2
            worse_tau = tau2 if L1 > L2 else tau1
        else:
            def probabilities(L1, L2):
                L = tau_3momentum.Mag() / TAU_MASS * tau_lifetime
                P1 = 1 - math.exp(-L2 / L)
                P2 = math.exp(-L1 / L)

                return P1, P2

            if tau1_unit.Dot(IP_unit) > tau2_unit.Dot(IP_unit):
                P1, P2 = probabilities(L1, L2)
                tau_reconstructed = tau1 if P1 > P2 else tau2
                worse_tau = tau2 if P1 > P2 else tau1
            else:
                P1, P2 = probabilities(L2, L1)
                tau_reconstructed = tau2 if P1 > P2 else tau1
                worse_tau = tau1 if P1 > P2 else tau2

    return tau_reconstructed, worse_tau, chargedPion_momentum



def rotate_vector(vec, axis, angle):
    rotated = vec.Clone()
    rotated.Rotate(angle, axis)
    return rotated
