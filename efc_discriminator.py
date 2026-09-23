#!/usr/bin/env python3
"""Second EFC function: name the sample from G_target that would retire each case.

If more n from G_cal cannot close the gap, the honest closer is a draw from
G_target. This function turns that rule into a pre-registered discriminator
per eligible remainder. It does not claim the outcome.
"""

from __future__ import annotations

import json
from pathlib import Path

from efc_engine import CANDIDATES, efc_score, more_n_closes, rank

OUT = Path("/workspace/artifacts")


def generator_split_discriminator(c) -> dict:
    """Return the G_target draw that would retire this EFC instance.

    Validation:
      - Eligible rows only.
      - more_n_closes(G_cal) must be False, else this was not EFC.
      - Must name a concrete observable, a kill result, and a confirm result.
    """
    if c.status != "ELIGIBLE":
        raise ValueError(f"{c.id} is not eligible")
    if more_n_closes(c, c.g_cal):
        raise ValueError(f"{c.id}: G_cal more-n would close it; not EFC")

    catalog = {
        "iso-3i-atlas": {
            "draw": "The 4th confirmed interstellar object with JWST-grade water D/H and carbon isotopes.",
            "kill_efc": "D/H and 12C/13C fall inside Solar System comet envelopes. Then 3I/ATLAS was a tail event, not a generator split.",
            "confirm_efc": "A second ISO lies many-σ from the Solar System envelope, in the 3I direction or another non-local direction. Then local ices are the wrong prior for ISO chemistry.",
            "do_not_claim": "That 3I/ATLAS is typical of all interstellar ices. n=1 isotope-grade ISO cannot mint a population.",
        },
        "asgard-oxic": {
            "draw": "Independent phylogenomic trees (not only Appler 2026) of Heimdallarchaeia from oxic vs anoxic sites, plus expression — not just presence — of aerobic ETC genes in situ.",
            "kill_efc": "Oxic Heimdallarchaeia are a derived recent adaptation, phylogenetically distal to eukaryotes. Then the anoxic catalogue was the right ancestor-generator.",
            "confirm_efc": "The closest eukaryotic relatives remain oxic-enriched across new coasts, and aerobic pathways are expressed. Ancestor-was-aerobic still needs paleo-redox, not just living descendants.",
            "do_not_claim": "That the eukaryotic ancestor itself respired oxygen. Living descendants ≠ the ancestor.",
        },
        "dive-geography": {
            "draw": "ODL's 10,000 stratified sites actually observed, compared against a same-effort random sample from the historical 5-country fleet.",
            "kill_efc": "Community composition and habitat statistics match the historical 3-country EEZ sample. Then it was n, not generator.",
            "confirm_efc": "Stratified new basins yield communities outside the historical envelope at pre-registered effect size. Then filled cells were a different process.",
            "do_not_claim": "That the 10,000-site list has been observed. It is a plan as of 1 Apr / 23 Sep 2026.",
        },
        "shale-fungi": {
            "draw": "Biomass conversion factors measured in situ in the same shale, not borrowed from oceanic systems, plus independent basins.",
            "kill_efc": "Fungal:bacterial biomass collapses toward surface-scarcity once local conversion factors are used. Then the surface prior held; the ratio was a borrowed unit.",
            "confirm_efc": "Fungi remain a first-class biomass term across basins with local conversion. Then the scarcity prior was the wrong generator.",
            "do_not_claim": "That 13 candidate taxa are named species, or that fungi dominate the deep biosphere.",
        },
        "hwo-template": {
            "draw": "A biosignature false-positive library that includes non-Earth generators (ISO ice chemistry, anoxic/oxic Asgard metabolisms, radiolytic O2) as first-class entries, not footnotes.",
            "kill_efc": "Earth-photic O2/CH4/vegetation templates still recover injected non-Earth atmospheres without systematic false positives. Then G_cal was enough.",
            "confirm_efc": "Non-Earth generators produce false positives the Earth library misses. Then the prior is provincial.",
            "do_not_claim": "That any exoplanet is inhabited.",
        },
        "tno-small-end": {
            "draw": "A completeness-corrected faint-end size distribution from the same Hubble+Webb selection function, compared to models trained only on ground-based bright TNOs.",
            "kill_efc": "After completeness, the faint end matches bright-end-trained models. Then it was undersampling.",
            "confirm_efc": "The deficit of small bodies survives completeness. Then the bright-end generator is the wrong prior.",
            "do_not_claim": "That planet-formation theory is falsified. One survey's faint end is not the Kuiper belt.",
        },
        "ocean-carbon-interface": {
            "draw": "Air-sea flux products that do not pool gyre floats with unsampled ice/river/coast nodes, plus a published residual after the gyre generator is removed.",
            "kill_efc": "The 10–20% model divergence vanishes inside gyre-only evaluations. Then interfaces were a sampling hole (undersampling/JAC), not a second generator.",
            "confirm_efc": "Interface nodes carry a residual the gyre generator cannot absorb. Then global-mean carbon is the wrong prior for those coasts.",
            "do_not_claim": "A new carbon-sink number.",
        },
        "human-cry": {
            "draw": "Pre-registered human magnetoreception tests that do not treat bird CRY4 or pigeon vestibular circuits as the human sensor.",
            "kill_efc": "Independent labs fail to replicate Chae 2025 frequency-specific effects. Then there is no human G_target to mismatch.",
            "confirm_efc": "A human-specific circuit, not borrowed from birds or pigeons, survives replication. Then animal generators were the wrong prior.",
            "do_not_claim": "That humans navigate magnetically. UPRC/CMC already forbade that leap.",
        },
    }
    if c.id not in catalog:
        raise KeyError(c.id)
    spec = catalog[c.id]
    return {
        "id": c.id,
        "realm": c.realm,
        "score": efc_score(c),
        "g_cal": c.g_cal,
        "g_target": c.g_target,
        **spec,
    }


def main() -> None:
    ranked = rank(CANDIDATES)
    eligible = [c for c in ranked if c.status == "ELIGIBLE" and efc_score(c) > 0]
    reports = [generator_split_discriminator(c) for c in eligible]
    path = OUT / "efc_discriminators.json"
    path.write_text(json.dumps(reports, indent=2), encoding="utf-8")
    print(f"discriminators: {len(reports)}")
    for r in reports:
        print(f"  {r['score']:7.3f}  {r['id']:<22}  DRAW: {r['draw'][:88]}")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
