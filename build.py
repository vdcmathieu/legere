"""Assemble data files into the single-page app dist/legere.html.

Inputs (data/):
  statements.json      statement bank (+ optional context from audit.json)
  questionnaire.json   other modules
  positions.json       verified candidate codings (from research/consolidate.py)
  profiles.json        per-candidate profile codes for the leadership score
  meta.json            as-of date, polls
  method.html          methodology page body
Core set: the statements shown to everyone before adaptive selection,
chosen greedily for discrimination under area and axis coverage constraints.
"""
import json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
D = ROOT / "data"
CONF = {"high": 1.0, "medium": 0.8, "low": 0.5, "none": 0.0}
CORE_N = 24


def jload(name, default=None):
    p = D / name
    return json.load(open(p)) if p.exists() else default


def discrimination(sid, cands):
    xs = [(c["positions"][sid]["p"], CONF.get(c["positions"][sid]["conf"], .5))
          for c in cands if sid in c["positions"] and c["positions"][sid]["p"] is not None]
    if len(xs) < 2:
        return 0.0
    w = sum(c for _, c in xs)
    mu = sum(p * c for p, c in xs) / w
    var = sum(c * (p - mu) ** 2 for p, c in xs) / w
    return var * len(xs) / len(cands)


def french_record(r):
    """Prefer the French translation of every displayed text field, keep the English as fallback."""
    if not r:
        return {}
    fr = lambda o, k: o.get(k + "_fr") or o.get(k, "")
    return {
        "bio": fr(r, "bio"),
        "offices": [{**o, "office": fr(o, "office")} for o in r.get("offices", [])],
        "legal": [{**l, "case": fr(l, "case")} for l in r.get("legal", [])],
        "reversals": [{**x, **{k: fr(x, k) for k in ("topic", "before", "after")}} for x in r.get("reversals", [])],
        "delivery": [{**x, **{k: fr(x, k) for k in ("what", "assessment")}} for x in r.get("delivery", [])],
        "media_portrayal": r.get("media_portrayal_fr") or r.get("media_portrayal", {}),
    }


def pick_core(statements, cands, n=CORE_N):
    """Greedy: highest discrimination, but every area at least once and
    each keyed axis at least 4 items, with keying balanced where possible."""
    disc = {s["id"]: discrimination(s["id"], cands) for s in statements}
    by = sorted(statements, key=lambda s: -disc[s["id"]])
    core = []
    for a in {s["area"] for s in statements}:
        best = next(s for s in by if s["area"] == a)
        core.append(best)
    for axis in ("econ", "cult", "eu"):
        for key in (1, -1):
            have = [s for s in core if s["axis"] == axis and s["key"] == key]
            for s in by:
                if len(have) >= 2:
                    break
                if s["axis"] == axis and s["key"] == key and s not in core:
                    core.append(s); have.append(s)
    for s in by:
        if len(core) >= n:
            break
        if s not in core:
            core.append(s)
    return [s["id"] for s in core], disc


def main():
    st = jload("statements.json")
    q = jload("questionnaire.json")
    pos = jload("positions.json")
    profiles = jload("profiles.json", {})
    meta = jload("meta.json", {"asof": "2026-10-05", "asof_fr": "5 octobre 2026", "polls": {}})
    audit = jload("audit.json", {})
    context = {c["id"]: c for c in audit.get("context", [])}
    context.update({c["id"]: c for c in jload("context_update.json", [])})

    cands = []
    for cid, c in pos["candidates"].items():
        cands.append({
            "id": cid, "name": c["name"], "party": c["party"], "short": c.get("short"),
            "positions": {sid: {"p": e.get("position"), "conf": e.get("confidence", "low"),
                                "type": e.get("evidence_type"), "summary": e.get("summary_fr") or e.get("summary", ""),
                                "nuance": e.get("nuance_fr") or e.get("nuance", ""),
                                "sources": [{"url": s.get("url"), "outlet": s.get("outlet"), "lean": s.get("outlet_lean")}
                                            for s in e.get("sources", [])][:4]}
                          for sid, e in c["positions"].items()},
            "record": french_record(c.get("record", {})),
            "profile": profiles.get(cid, {}),
        })
    core, disc = pick_core(st["statements"], cands)
    method = (D / "method.html").read_text() if (D / "method.html").exists() else "<h2>Méthode</h2><p>À venir.</p>"
    n_corr = sum(len(c.get("verification_notes", [])) for c in pos["candidates"].values())
    power = (D / "power_section.html").read_text() if (D / "power_section.html").exists() else "<p>Analyse en cours.</p>"
    for k, v in {"{{N_STATEMENTS}}": str(len(st["statements"])), "{{N_CORRECTIONS}}": f"{n_corr:,}".replace(",", "\u202f"),
                 "{{ASOF}}": meta.get("asof_fr", ""), "{{POWER_SECTION}}": power}.items():
        method = method.replace(k, v)
    method = method.replace("{{N_CORE}}", str(CORE_N))
    data = {"meta": meta, "areas": st["areas"], "statements": st["statements"], "questionnaire": q,
            "candidates": cands, "core": core, "context": context, "method_html": method}
    html = (ROOT / "src" / "app.html").read_text().replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False))
    (ROOT / "dist").mkdir(exist_ok=True)
    (ROOT / "dist" / "legere.html").write_text(html)
    json.dump({"core": core, "discrimination": disc}, open(D / "core.json", "w"), indent=1)
    print(f"built dist/legere.html ({len(html)//1024} KB), {len(cands)} candidates, core={len(core)}")


if __name__ == "__main__":
    main()
