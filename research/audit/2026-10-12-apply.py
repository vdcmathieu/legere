"""Mélenchon int1 and ins5 -> unknown (maintainer decision, 2026-10-12).

int1 (-2, medium) rested on 2022 statements and a non-binding 2024 vote; the 2027 programme is silent on military aid.
ins5 (+1, low) was inferred from his general RIC, while imm2 (-1, low) read the same evidence the other way.
Summaries and sources are kept as the record of what was found; the app shows a null cell as "no documented position".
Usage: python3 research/audit/2026-10-12-apply.py
"""
import json

POS = "data/positions.json"
NUANCE = {
 "int1": ("The 2027 programme is silent on military aid; the evidence against it dates from 2022 and from a non-binding 2024 vote, so no current position is coded.",
          "Le programme 2027 ne dit rien de l'aide militaire ; les éléments contre datent de 2022 et d'un vote non contraignant de 2024 : aucune position actuelle n'est donc codée."),
 "ins5": ("His RIC could reach any subject, but no statement backs a referendum on immigration or justice as such, so no position is coded.",
          "Son RIC pourrait porter sur tout sujet, mais aucune déclaration ne soutient en tant que tel un référendum sur l'immigration ou la justice : aucune position n'est donc codée."),
}
d = json.load(open(POS))
for sid, (en, fr) in NUANCE.items():
    cell = d["candidates"]["melenchon"]["positions"][sid]
    print(sid, cell["position"], cell["confidence"], "-> None none")
    cell.update(position=None, confidence="none", nuance=en, nuance_fr=fr)
json.dump(d, open(POS, "w"), ensure_ascii=False, indent=1)
