def find_true_tau(Tau, GenPart, GenVisTau):
    tau_idx = Tau.genPartIdx
    tau_flav = Tau.genPartFlav

    if tau_idx < 0:
        print("No gen-level match for this tau.")
        return None, []

    def climb_mother_genpart(idx):
        while idx >= 0:
            part = GenPart[idx]
            if abs(part.pdgId) == 15:
                return idx, part
            idx = part.genPartIdxMother
        return None, None

    if tau_flav in [1, 2]:
        matched = GenPart[tau_idx]
        ancestor_idx, ancestor = climb_mother_genpart(matched.genPartIdxMother)

    elif tau_flav in [3, 4]:
        matched = GenPart[tau_idx]
        ancestor_idx, ancestor = climb_mother_genpart(matched.genPartIdxMother)

    elif tau_flav == 5:
        if tau_idx >= len(GenVisTau):
            print("No gen-level match for this tau.")
            return None, []
        matched_vis = GenVisTau[tau_idx]
        ancestor_idx, ancestor = climb_mother_genpart(matched_vis.genPartIdxMother)

    else:
        print("Unknown or no match (flav =", tau_flav, ").")
        return None, []

    if ancestor is None:
        print("No tau ancestor found.")
        return None, []

    #print("Found ancestor tau!")

    # Teraz znajdujemy jego dzieci:
    daughters = []
    for idx, part in enumerate(GenPart):
        if part.genPartIdxMother == ancestor_idx:
            daughters.append(part)

    #print(f"Found {len(daughters)} daughters.")
    #for dau in daughters:
    #    print(f"Daughter pdgId: {dau.pdgId}, pt: {dau.pt}, eta: {dau.eta}, phi: {dau.phi}, mass: {dau.mass}")
    #    print(f"Ancestor pdgID: {ancestor.pdgId}, mass: {ancestor.mass}, pt: {ancestor.pt}, eta: {ancestor.eta}, phi: {ancestor.phi}")

    return ancestor, daughters
