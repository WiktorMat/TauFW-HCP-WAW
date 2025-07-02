import ROOT
import math
from TauFW.PicoProducer.analysis.HiggsCPtools.Utils import *
from TauFW.PicoProducer.analysis.HiggsCPtools.Kinematics_reconstructions import *

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

def PhiCP_reco(particle_1, particle_2, tau1Prod = None, tau2Prod = None, channel1 = 'tau', channel2 = 'tau'):
    p1, lambda1, y1 = get_pion_and_lambda(particle_1, tau1Prod, channel1)
    if p1 is None or lambda1 is None:
        return -1

    p2, lambda2, y2 = get_pion_and_lambda(particle_2, tau2Prod, channel2)
    if p2 is None or lambda2 is None:
        return -1
    
    y = y1*y2
    
    firstNeg = particle_1.charge < 0
    
    phi_cp = acoCP(p1, p2, lambda1, lambda2, firstNeg, y)
    
    return phi_cp

### FROM ALIAKSEI RASPIAREZA: https://github.com/raspereza/CPHiggs/blob/main/IP/python/pv_utils.py#L473-L486 ###
def acoCP(P1, P2, R1, R2, firstNeg, y):

    Prongsum = P1 + P2
    boost = -Prongsum.BoostVector()
    
    P1.Boost(boost)
    P2.Boost(boost)
    R1.Boost(boost)
    R2.Boost(boost)
    
    vecP1 = P1.Vect().Unit()
    vecP2 = P2.Vect().Unit()
    vecR1 = R1.Vect()
    vecR2 = R2.Vect()

    R1transv = vecR1 - vecP1*(vecP1.Dot(vecR1))
    R2transv = vecR2 - vecP2*(vecP2.Dot(vecR2))

    n1 = R1transv.Unit()
    n2 = R2transv.Unit()

    cos_phi = n1.Dot(n2)
    
    if cos_phi > 1.0:
        cos_phi = 1.0
    elif cos_phi < -1.0:
        cos_phi = -1.0

    acop = math.acos(cos_phi)

    sign = vecP2.Dot(n1.Cross(n2))
    
    if firstNeg:
        sign = vecP1.Dot(n2.Cross(n1))

    if y<0:
        acop = acop + ROOT.TMath.Pi()

    if sign<0:
        acop = 2.0*ROOT.TMath.Pi() - acop
    
    acop %= 2.0*ROOT.TMath.Pi()

    return acop


def get_pion_and_lambda(particle, tau_products = None, channel='tau'):

    '''Get the 4-momentum of the charged pion and the lambda vector for the given tau particle.
    Particle -- either mu, electron or tau Collection from NanoAOD
    tau_products -- also collection from NanoAOD, needed only for tau channel
    channel -- either 'mu', 'tau' or 'ele' (default is 'tau')
    
    Three return values:
    p -- 4-vector used as a reference for the ZMF (e.g. charged pion momentum)
    lambda -- second 4-vector used for the PhiCP calculation (e.g. polarimetric vector)
    y -- relevant only in the DecayPlane method, otherwise shoud be set to 1'''

    if channel == 'mu':
        p = ROOT.TLorentzVector()
        p.SetPtEtaPhiM(particle.pt, particle.eta, particle.phi, MUON_MASS)
        lambda_vec = ROOT.TLorentzVector()
        lambda_vec.SetPxPyPzE(particle.IPx, particle.IPy, particle.IPz, 0.0)
        return p, lambda_vec, 1

    elif channel == 'tau':
        if particle.decayMode in [0, 1, 2]:
            best_p = ROOT.TLorentzVector(0, 0, 0, 0)
            
            for product in tau_products:
                if abs(product.pdgId) in [11, 13, 211, 10211]:
                    test_p = get_chargedPion_4momentum(product)  # returns TLorentzVector
                    if test_p.E() > best_p.E():
                        best_p = test_p

            if best_p.E() == 0:
                return None, None, None

            if particle.decayMode == 0:
                lambda_vec = get_lambda(particle)  # returns TLorentzVector
                y = 1
                if lambda_vec.Vect().Mag() == 0:
                    print("No impact parameter!")
                    return None, None, None
            elif particle.decayMode in [1, 2] and particle.decayModePNet == 1:
                lambda_vec = get_neutralPion_4momentum(tau_products)  # returns TLorentzVector
                y = best_p.E() - lambda_vec.E()
            else:
                return None, None, None #We suspect these are wrongly reconstructed as rho- channel (dm=1)

            return best_p, lambda_vec, y

        elif particle.decayMode == 10:
            p, lambda_vec = get_charged_pion_from_rho_decay(tau_products, particle.charge)
            if p is None:
                return None, None, None
            y = p.E() - lambda_vec.E()
            return p, lambda_vec, y

        else:
            return None, None, None
    else:
        return None, None, None