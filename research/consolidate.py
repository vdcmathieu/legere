"""Merge workflow journal results into data/positions.json.

For each job (candidate x {A,B,R}) the verified result wins over the draft.
Usage: python3 research/consolidate.py <journal.jsonl> [<journal2.jsonl> ...]
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANDS = {
    "lepen": ("Marine Le Pen", "Rassemblement national", "Le Pen"),
    "melenchon": ("Jean-Luc Mélenchon", "La France insoumise", "Mélenchon"),
    "philippe": ("Édouard Philippe", "Horizons", "Philippe"),
    "attal": ("Gabriel Attal", "Renaissance", "Attal"),
    "retailleau": ("Bruno Retailleau", "Les Républicains", "Retailleau"),
    "zemmour": ("Éric Zemmour", "Reconquête", "Zemmour"),
    "glucksmann": ("Raphaël Glucksmann", "Place publique", "Glucksmann"),
    "faure": ("Olivier Faure", "Parti socialiste", "Faure"),
    "tondelier": ("Marine Tondelier", "Les Écologistes", "Tondelier"),
    "roussel": ("Fabien Roussel", "Parti communiste français", "Roussel"),
    "ruffin": ("François Ruffin", "Debout !", "Ruffin"),
    "lisnard": ("David Lisnard", "Nouvelle Énergie", "Lisnard"),
}


def read_journals(paths):
    labels, results = {}, {}
    for p in paths:
        for line in open(p):
            d = json.loads(line)
            if d.get("type") == "started":
                labels[d["key"]] = d["label"]
            elif d.get("type") == "result" and d.get("result"):
                results[d["key"]] = d["result"]
    jobs = {}
    for key, res in results.items():
        lab = labels.get(key, "")
        if ":" not in lab:
            continue
        stage, job = lab.split(":", 1)
        jobs.setdefault(job, {})[stage] = res
    return jobs


def main():
    jobs = read_journals(sys.argv[1:])
    raw = ROOT / "research" / "matrix"
    raw.mkdir(exist_ok=True)
    out = {"candidates": {}}
    report = []
    for cid, (name, party, short) in CANDS.items():
        c = {"name": name, "party": party, "short": short, "positions": {}, "record": {}, "verification_notes": []}
        for part in "ABRC":
            j = jobs.get(f"{cid}_{part}", {})
            best = j.get("verify") or j.get("collect")
            status = "verified" if j.get("verify") else ("draft" if j.get("collect") else "missing")
            report.append((cid, part, status))
            if not best:
                continue
            json.dump(j, open(raw / f"{cid}_{part}.json", "w"), ensure_ascii=False, indent=1)
            c["verification_notes"] += best.get("verification_notes", [])
            if part == "R":
                c["record"] = {k: v for k, v in best.items() if k != "verification_notes"}
            else:
                for e in best["positions"]:
                    c["positions"][e["id"]] = e
        out["candidates"][cid] = c
    json.dump(out, open(ROOT / "data" / "positions.json", "w"), ensure_ascii=False, indent=1)
    for r in report:
        if r[2] != "verified":
            print("NOT VERIFIED:", r)
    n = sum(1 for c in out["candidates"].values() for e in c["positions"].values() if e.get("position") is not None)
    tot = sum(len(c["positions"]) for c in out["candidates"].values())
    print(f"{n}/{tot} cells coded; {sum(len(c['verification_notes']) for c in out['candidates'].values())} verifier corrections")


if __name__ == "__main__":
    main()
