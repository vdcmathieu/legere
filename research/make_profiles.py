"""Build data/profiles.json from verified records + two blind profile coders."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
pos = json.load(open(ROOT / "data" / "positions.json"))
coders = [json.load(open(ROOT / "research" / f)) for f in ("profile_coder_fable.json", "profile_coder_opus.json")
          if (ROOT / "research" / f).exists()]
PROBITY = re.compile(r"embezzl|détourn|corrupt|fraud|fictiti|fictif|emplois? fictif|prise illégale|favoritisme|abus de bien", re.I)
OTHER_FIRST = re.compile(r"rebell|rébell|violence envers|outrage", re.I)
SPEECH = re.compile(r"defam|diffam|injur|insult|haine|hatred|provocation|contestation|négation|discrimination raciale", re.I)
out = {}
for cid, c in pos["candidates"].items():
    r = c.get("record", {})
    conv = []
    for l in r.get("legal", []):
        if l["status"] not in ("convicted_final", "convicted_appeal_pending"):
            continue
        case = l["case"]
        cat = ("probity" if PROBITY.search(case) else "other" if OTHER_FIRST.search(case)
               else "speech" if SPEECH.search(case) else "other")
        conv.append({"cat": cat, "status": l["status"], "case": l["case"][:160], "date": l["date"]})
    p = {"exec_years": r.get("executive_experience_years"), "convictions": conv}
    vals = [x[cid] for x in coders if cid in x]
    for k in ("style", "continuity", "reversals"):
        v = [x[k] for x in vals if isinstance(x.get(k), (int, float))]
        if v:
            p[k] = sum(v) / len(v)
            p[k + "_spread"] = max(v) - min(v)
    p["coder_notes"] = [{"style_why": x.get("style_why"), "continuity_why": x.get("continuity_why"), "reversal_list": x.get("reversal_list")} for x in vals]
    out[cid] = p
json.dump(out, open(ROOT / "data" / "profiles.json", "w"), ensure_ascii=False, indent=1)
for cid, p in out.items():
    print(cid, p.get("exec_years"), [(x["cat"], x["status"]) for x in p["convictions"]], {k: p.get(k) for k in ("style", "continuity", "reversals", "style_spread", "continuity_spread")})
