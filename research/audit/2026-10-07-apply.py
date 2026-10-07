import json, sys
R, POS = sys.argv[1], "data/positions.json"
F = {x["id"]: x for x in json.load(open(f"{R}/findings.json"))}
APPLY = "F01 F02 F03 F04 F05 F06 F07 F09 F10 F11 F12 F13 F14 F15 F16 F17 F18 F19".split()
PS = "https://www.publicsenat.fr/actualites/politique/reculer-ou-avancer-lage-legal-avec-ou-sans-capitalisation-ce-que-proposent-les-principaux-candidats-a-lelection-presidentielle-sur-les-retraites"
# Displayed notes: evidence only, no auditor commentary or cross-candidate bookkeeping.
NUANCE = {
 "F01": ("62 would remain a 'minimum protection' in a 43-year contribution system, so some people would retire later.",
         "62 ans resterait une « protection minimale » dans un système à 43 annuités : certains partiraient plus tard."),
 "F03": ("Her alternative (an IFF replacing the IFI) is a different instrument and does not soften her explicit rejection of a 2% minimum tax above EUR 100m.",
         "Son alternative (un IFF remplaçant l'IFI) est un autre dispositif et n'atténue pas son rejet explicite d'un impôt minimum de 2 % au-delà de 100 millions."),
 "F04": ("Personal roll-call vote (Datan).", "Vote nominatif personnel (Datan)."),
 "F05": ("Group votes: Roussel has not been a deputy since 2024. His protectionist line (mirror clauses) accompanies the ban rather than contradicting it.",
         "Votes de groupe : Roussel n'est plus député depuis 2024. Sa ligne protectionniste (clauses miroirs) accompagne l'interdiction plutôt qu'elle ne la contredit."),
 "F06": ("LCP's report of his 29 September 2026 video only says 'mixed, pay-as-you-go and funded'; the mandatory character is reported by Public Sénat (30 September 2026) and by the economy minister's reaction.",
         "Le compte rendu de LCP de sa vidéo du 29 septembre 2026 ne dit que « mixte, répartition et capitalisation » ; le caractère obligatoire est rapporté par Public Sénat (30 septembre 2026) et par la réaction du ministre de l'Économie."),
 "F09": ("Party programme, no personal quote from Faure.", "Programme de parti, sans citation personnelle de Faure."),
 "F11": ("Party programme, no personal quote from Faure.", "Programme de parti, sans citation personnelle de Faure."),
 "F13": ("The citizens' convention step rules out +2, but the text presents legalisation as the intended outcome.",
         "L'étape de la convention citoyenne empêche un +2, mais le texte présente la légalisation comme l'issue visée."),
 "F14": ("Group vote (Tondelier is not a deputy). No repeal or restriction is proposed.",
         "Vote de groupe (Tondelier n'est pas députée). Aucune abrogation ni restriction n'est proposée."),
 "F17": ("2024 coalition programme; explicit on selection itself, not only on the platform.",
         "Programme de coalition de 2024 ; explicite sur la sélection elle-même et pas seulement sur la plateforme."),
 "F19": ("Opposition at the time of the vote, later acceptance by the party president, no commitment to repeal: an explicitly mixed position, hence 0.",
         "Opposition au moment du vote, acceptation ultérieure par le président du parti, pas d'engagement d'abrogation : position mitigée, d'où 0."),
}
# Quotes must be verbatim from the page; table readings and summaries are marked as paraphrase.
QUOTE = {
 PS + "|F01": "Olivier Faure se dit pour sa part favorable à l'abrogation de la réforme de 2023 et à un retour à 62 ans",
 PS + "|F06": "d'abord par un fonds collectif obligatoire, « neutre sur le coût du travail »",
 "https://www.publicsenat.fr/actualites/economie/budget-2026-le-rn-seloigne-de-la-gauche-sur-la-fiscalite|F03": "ce que Marine Le Pen qualifiait il y a quelques jours de proposition « stupide et nocive »",
}
d = json.load(open(POS)); C = d["candidates"]
for fid in APPLY:
    x = F[fid]; p = dict(x["proposed"]); cell = C[x["candidate_id"]]["positions"][x["statement_id"]]
    if fid in NUANCE: p["nuance"], p["nuance_fr"] = NUANCE[fid]
    srcs = []
    for s in p.get("sources", []):
        s = dict(s); q = QUOTE.get(f"{s['url']}|{fid}")
        if q: s["quote"] = q
        elif "datan.fr" in s["url"] or fid in ("F03",) and "lcp.fr" in s["url"] or "MoneyVox" in s.get("outlet", ""):
            s["quote"] = s["quote"] if s["quote"].startswith("Paraphrase") else "Paraphrase: " + s["quote"]
        s["quote"] = s["quote"].replace(" (headline)", "").replace(" (same op-ed)", "")
        srcs.append(s)
    if fid == "F01": srcs = [s for s in srcs if "entrevue" not in s["url"]]
    p["sources"] = srcs
    for k in ("position", "confidence", "evidence_type", "summary", "summary_fr", "nuance", "nuance_fr", "sources"): cell[k] = p[k]
    print(fid, x["candidate_id"], x["statement_id"], cell["position"], cell["confidence"])
json.dump(d, open(POS, "w"), ensure_ascii=False, indent=1)
