"""Compare stop rules for the app's "result ready" checkpoint.

Simulated respondents answer the fixed core then adaptive picks (as in the app).
From core+10 answers to the core+25 cap, a bootstrap with the app's default
+-1 jitter (0.25) estimates each candidate's share of first places. For each
rule we report when it fires and how often the top candidate is then right.
Usage: python3 analysis/stop_rules.py analysis/stop_rules.json
"""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, power as P
(names, C, W), ids, _ = P.load_matrix()
core = P.app_core(ids); K, J = C.shape
MIN, MAX, B, N, PJ = len(core) + 10, len(core) + 25, 200, 400, 0.25
rng = np.random.default_rng(11)
T = P.make_respondents(C, N); sigma = P.calibrate_sigma(0.65, T)
full = np.ones(J, bool); rows = []
for t in T:
    truth = P.scores(t, full, C, W); top = truth.argmax(); srt = np.sort(truth)
    obs = np.clip(np.round(t + rng.normal(0, sigma, J)), -2, 2)
    first = list(rng.permutation(core)); asked, order = set(), []
    for _ in range(MAX):
        j = P.next_adaptive(obs, asked, C, W, len(core), first); order.append(j); asked.add(j)
    per_n = {}
    for n in range(MIN, MAX + 1):
        items = np.array(order[:n]); wins = np.zeros(K)
        for _ in range(B):
            pick = rng.choice(items, n); m = np.zeros(J); np.add.at(m, pick, 1)
            o = obs.copy(); jit = rng.random(J) < PJ
            o[jit] = np.clip(o[jit] + rng.choice([-1, 1], jit.sum()), -2, 2)
            wins[P.scores(o, m > 0, C, W, item_w=m).argmax()] += 1
        mask = np.zeros(J, bool); mask[items] = True
        s = P.scores(obs, mask, C, W)
        per_n[n] = (np.sort(wins)[::-1] / B, int(s.argmax()), list(np.argsort(-s)[:2]))
    rows.append((top, srt[-1] - srt[-2] >= 0.05, per_n))
rules = {"top1>=.90": lambda p: p[0] >= .9, "top1>=.80": lambda p: p[0] >= .8, "top1>=.70": lambda p: p[0] >= .7,
         "top2>=.90": lambda p: p[0] + p[1] >= .9, "top2>=.95": lambda p: p[0] + p[1] >= .95}
out = {}
for name, rule in rules.items():
    stops, ok1, ok1d, ok2 = [], [], [], []
    for top, dec, per_n in rows:
        n = next((n for n in range(MIN, MAX + 1) if rule(per_n[n][0])), MAX)
        _, pick, top2 = per_n[n]
        stops.append(n); ok1.append(pick == top); ok2.append(top in top2)
        if dec: ok1d.append(pick == top)
    s = np.array(stops)
    out[name] = {"median": float(np.median(s)), "mean": round(float(s.mean()), 1), "at_20": round(float((s == MIN).mean()), 2),
                 "capped": round(float((s == MAX).mean()), 2), "top1_decisive": round(float(np.mean(ok1d)), 3),
                 "top1_all": round(float(np.mean(ok1)), 3), "truth_in_top2": round(float(np.mean(ok2)), 3)}
    print(name, out[name], flush=True)
json.dump(out, open(sys.argv[1], "w"), indent=1)
