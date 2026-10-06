"""Split / merge the English research text for French translation.

  python3 research/translate.py split   -> research/fr/in/<cid>.json (text fields only)
  python3 research/translate.py merge   -> writes *_fr fields into data/positions.json
Quotes and outlet names are never translated (they are evidence).
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POS = ROOT / "data" / "positions.json"
IN, OUT = ROOT / "research" / "fr" / "in", ROOT / "research" / "fr" / "out"


def split():
    IN.mkdir(parents=True, exist_ok=True); OUT.mkdir(parents=True, exist_ok=True)
    d = json.load(open(POS))
    for cid, c in d["candidates"].items():
        r = c.get("record", {})
        doc = {
            "positions": [{"id": k, "summary": e.get("summary", ""), "nuance": e.get("nuance", "")}
                          for k, e in c["positions"].items() if e.get("summary") or e.get("nuance")],
            "record": {
                "bio": r.get("bio", ""),
                "offices": [o.get("office", "") for o in r.get("offices", [])],
                "legal": [l.get("case", "") for l in r.get("legal", [])],
                "reversals": [{"topic": x.get("topic", ""), "before": x.get("before", ""), "after": x.get("after", "")} for x in r.get("reversals", [])],
                "delivery": [{"what": x.get("what", ""), "assessment": x.get("assessment", "")} for x in r.get("delivery", [])],
                "media_portrayal": r.get("media_portrayal", {}),
            },
        }
        json.dump(doc, open(IN / f"{cid}.json", "w"), ensure_ascii=False, indent=1)
    print("split", len(d["candidates"]))


def merge():
    d = json.load(open(POS))
    n = 0
    for cid, c in d["candidates"].items():
        p = OUT / f"{cid}.json"
        if not p.exists():
            print("missing translation", cid); continue
        t = json.load(open(p))
        for e in t.get("positions", []):
            if e["id"] in c["positions"]:
                c["positions"][e["id"]]["summary_fr"] = e.get("summary", "")
                c["positions"][e["id"]]["nuance_fr"] = e.get("nuance", "")
                n += 1
        r, tr = c.get("record", {}), t.get("record", {})
        if r and tr:
            r["bio_fr"] = tr.get("bio", "")
            for o, f in zip(r.get("offices", []), tr.get("offices", [])): o["office_fr"] = f
            for l, f in zip(r.get("legal", []), tr.get("legal", [])): l["case_fr"] = f
            for x, f in zip(r.get("reversals", []), tr.get("reversals", [])):
                x.update({k + "_fr": v for k, v in f.items()})
            for x, f in zip(r.get("delivery", []), tr.get("delivery", [])):
                x.update({k + "_fr": v for k, v in f.items()})
            r["media_portrayal_fr"] = tr.get("media_portrayal", {})
    json.dump(d, open(POS, "w"), ensure_ascii=False, indent=1)
    print("merged", n, "position texts")


if __name__ == "__main__":
    {"split": split, "merge": merge}[sys.argv[1]]()
