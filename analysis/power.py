"""Power analysis for the 2027 matching questionnaire.

Question: how many answered statements does a respondent need before the
top-ranked candidate is, with high probability, the one they are truly
closest to?

Approach (Monte Carlo, plus a closed-form per-pair bound):
- Candidates: K x J matrix of positions in {-2..2} (NaN = unknown) and
  confidence weights, from data/positions.json (or a synthetic stand-in).
- Synthetic respondents: a "true" answer vector t, either near a candidate
  (perturbed on a share of items) or drawn from the item marginals.
- Measurement noise: observed answer = round(t + N(0, sigma)), clipped, with
  sigma calibrated so single-item test-retest correlation ~ r_tt
  (issue items: 0.5-0.7 in the survey literature; 0.65 is the default).
- Ground truth: the candidate with the best score on the noise-free t over
  all J statements.
- For n = 5..J answered items, under three orderings (random, static
  discrimination order, adaptive), measure how often the top-ranked
  candidate matches the truth.
"""
import json, math, sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
RNG = np.random.default_rng(2027)
CONF_W = {"high": 1.0, "medium": 0.8, "low": 0.5, "none": 0.0}
PRIOR_K = 2.0  # shrinkage: pseudo-items at 50% agreement


# ---------------------------------------------------------------- data
def load_matrix():
    p = ROOT / "data" / "positions.json"
    st = json.load(open(ROOT / "data" / "statements.json"))["statements"]
    ids = [s["id"] for s in st]
    if not p.exists():
        return synthetic(ids), ids, True
    d = json.load(open(p))
    names = list(d["candidates"].keys())
    C = np.full((len(names), len(ids)), np.nan)
    W = np.zeros_like(C)
    for k, n in enumerate(names):
        for j, sid in enumerate(ids):
            e = d["candidates"][n]["positions"].get(sid)
            if e and e.get("position") is not None:
                C[k, j] = e["position"]
                W[k, j] = CONF_W.get(e.get("confidence", "low"), 0.5)
    return (names, C, W), ids, False


def synthetic(ids):
    """12 candidates on 3 latent axes; items load on one axis with noise."""
    K, J = 12, len(ids)
    axes = RNG.normal(0, 1, (K, 3))
    load = np.zeros((J, 3))
    load[np.arange(J), RNG.integers(0, 3, J)] = RNG.choice([-1, 1], J) * RNG.uniform(0.6, 1.2, J)
    raw = axes @ load.T + RNG.normal(0, 0.5, (K, J))
    C = np.clip(np.round(raw * 1.3), -2, 2)
    C[RNG.random((K, J)) < 0.12] = np.nan
    W = np.where(np.isnan(C), 0, RNG.choice([1.0, 0.8, 0.5], (K, J), p=[.5, .35, .15]))
    return [f"cand{k}" for k in range(K)], C, W


# ---------------------------------------------------------------- scoring
def scores(u, mask, C, W, item_w=None):
    """City-block agreement in [0,1], confidence-weighted, shrunk to 0.5."""
    iw = np.ones(C.shape[1]) if item_w is None else item_w
    valid = mask[None, :] & ~np.isnan(C)
    w = np.where(valid, W * iw[None, :], 0.0)
    agree = 1 - np.abs(np.nan_to_num(C) - u[None, :]) / 4
    return ((w * agree).sum(1) + PRIOR_K * 0.5) / (w.sum(1) + PRIOR_K)


def discrimination(C, W):
    """Per-item spread of candidate positions (confidence-weighted variance)."""
    out = np.zeros(C.shape[1])
    for j in range(C.shape[1]):
        m = ~np.isnan(C[:, j])
        if m.sum() < 2:
            continue
        w = W[m, j]
        x = C[m, j]
        mu = (w * x).sum() / w.sum()
        out[j] = (w * (x - mu) ** 2).sum() / w.sum() * (m.sum() / C.shape[0])
    return out


# ---------------------------------------------------------------- respondents
def calibrate_sigma(r_tt, T):
    """Find sigma such that corr(obs1, obs2) ~ r_tt across items/respondents."""
    best, err = 0.5, 9
    for s in np.linspace(0.1, 2.0, 60):
        o1 = np.clip(np.round(T + RNG.normal(0, s, T.shape)), -2, 2)
        o2 = np.clip(np.round(T + RNG.normal(0, s, T.shape)), -2, 2)
        r = np.corrcoef(o1.ravel(), o2.ravel())[0, 1]
        if abs(r - r_tt) < err:
            best, err = s, abs(r - r_tt)
    return best


def make_respondents(C, n, p_near=0.7, deviate=0.35):
    K, J = C.shape
    T = np.empty((n, J))
    fill = np.nan_to_num(np.nanmean(C, 0))
    for i in range(n):
        if RNG.random() < p_near:
            base = C[RNG.integers(K)].copy()
            nanm = np.isnan(base)
            base[nanm] = np.round(fill[nanm] + RNG.normal(0, 1, nanm.sum()))
            dev = RNG.random(J) < deviate
            base[dev] += RNG.choice([-2, -1, 1, 2], dev.sum(), p=[.15, .35, .35, .15])
        else:
            col = RNG.integers(K, size=J)
            base = C[col, np.arange(J)]
            nanm = np.isnan(base)
            base[nanm] = RNG.integers(-2, 3, nanm.sum())
        T[i] = np.clip(base, -2, 2)
    return T


# ---------------------------------------------------------------- orderings
def order_static(C, W):
    return list(np.argsort(-discrimination(C, W)))


def next_adaptive(u, asked, C, W, n_core, static):
    """After a fixed core, pick the item that best separates current contenders."""
    if len(asked) < n_core:
        return next(j for j in static if j not in asked)
    mask = np.zeros(C.shape[1], bool); mask[list(asked)] = True
    s = scores(u, mask, C, W)
    se = 0.25 / math.sqrt(max(len(asked), 1))       # rough SE of a score
    post = np.exp((s - s.max()) / se); post /= post.sum()
    best, bj = -1, None
    for j in range(C.shape[1]):
        if j in asked:
            continue
        m = ~np.isnan(C[:, j])
        if m.sum() < 2:
            continue
        p = post[m] * W[m, j]
        if p.sum() == 0:
            continue
        x = C[m, j]
        mu = (p * x).sum() / p.sum()
        v = (p * (x - mu) ** 2).sum() / p.sum()
        if v > best:
            best, bj = v, j
    return bj if bj is not None else next(j for j in static if j not in asked)


# ---------------------------------------------------------------- simulation
def app_core(ids):
    """The fixed core the app shows first (data/core.json), as column indices."""
    p = ROOT / "data" / "core.json"
    if not p.exists():
        return None
    core = json.load(open(p))["core"]
    return [ids.index(c) for c in core if c in ids]


def simulate(C, W, n_resp=1500, r_tt=0.65, ns=None, strategies=("random", "static", "adaptive"), n_core=15, core=None):
    K, J = C.shape
    ns = ns or [5, 10, 15, 20, 25, 30, 35, 40, 50, 60, J]
    T = make_respondents(C, n_resp)
    sigma = calibrate_sigma(r_tt, T)
    full = np.ones(J, bool)
    truth = np.array([scores(t, full, C, W) for t in T])
    top = truth.argmax(1)
    srt = np.sort(truth, 1)
    margin = srt[:, -1] - srt[:, -2]
    static = order_static(C, W)
    res = {s: {n: [] for n in ns} for s in strategies}
    for i, t in enumerate(T):
        obs = np.clip(np.round(t + RNG.normal(0, sigma, J)), -2, 2)
        for strat in strategies:
            if strat == "random":
                order = list(RNG.permutation(J))
            elif strat == "static":
                order = static
            else:
                # what the app does: its fixed core in random order, then adaptive picks
                first = list(RNG.permutation(core)) if core else static
                k0 = len(core) if core else n_core
                order, asked = [], set()
                for _ in range(max(ns)):
                    j = next_adaptive(obs, asked, C, W, k0, first)
                    order.append(j); asked.add(j)
            for n in ns:
                mask = np.zeros(J, bool); mask[order[:n]] = True
                s = scores(obs, mask, C, W)
                pick = s.argmax()
                res[strat][n].append((pick == top[i], truth[i, top[i]] - truth[i, pick], margin[i]))
    return res, sigma, margin


def summarise(res, margin_cut=0.05):
    out = {}
    for strat, byn in res.items():
        out[strat] = {}
        for n, rows in byn.items():
            a = np.array(rows, dtype=float)
            dec = a[:, 2] >= margin_cut
            out[strat][n] = {
                "top1": a[:, 0].mean(),
                "top1_decisive": a[dec, 0].mean() if dec.any() else float("nan"),
                "near_top_2pts": (a[:, 1] <= 0.02).mean(),
                "mean_regret_pts": 100 * a[:, 1].mean(),
            }
    return out


# ---------------------------------------------------------------- closed form
def pair_n(C, W, sigma, deltas=(0.05, 0.10), z=1.282, n_resp=300):
    """Items needed to rank two candidates correctly with prob >= Phi(z) (0.90).

    For a respondent whose true agreement with A exceeds B by `delta` (score
    scale 0-1, i.e. delta=0.05 is 5 points), the estimated gap after n of the
    J statements has two variance sources:
      - which statements were asked (sampling WITHOUT replacement from J,
        so finite-population corrected):  v_item / n * (J - n) / (J - 1)
      - the respondent's own answer noise:  v_noise / n
    Solve  delta / sqrt(Var(n)) >= z  for the smallest n <= J. If even n = J
    fails, the pair is not separable at that gap for that respondent: the
    tool must then present them as tied rather than ranked.
    Respondents are sampled as per-item mixtures of A and B (plus off-pair
    deviations), which is where separation is hardest.
    """
    K, J = C.shape
    out = []
    for a in range(K):
        for b in range(a + 1, K):
            both = ~np.isnan(C[a]) & ~np.isnan(C[b])
            if both.sum() < 3:
                continue
            Jab = int(both.sum())
            v_item, v_noise = [], []
            for _ in range(n_resp):
                base = np.where(RNG.random(J) < RNG.uniform(0.3, 0.7), C[a], C[b])
                dev = RNG.random(J) < 0.25
                base = np.where(dev, base + RNG.choice([-1, 1], J), base)
                t = np.clip(np.nan_to_num(base), -2, 2)[both]
                d_true = (np.abs(t - C[b][both]) - np.abs(t - C[a][both])) / 4
                v_item.append(d_true.var())
                noisy = [np.clip(np.round(t + RNG.normal(0, sigma, t.size)), -2, 2) for _ in range(20)]
                dn = np.array([(np.abs(o - C[b][both]) - np.abs(o - C[a][both])) / 4 for o in noisy])
                v_noise.append(dn.var(0).mean())
            vi, vn = float(np.mean(v_item)), float(np.mean(v_noise))
            row = {"a": a, "b": b, "coded_both": Jab,
                   "items_differing": int((C[a][both] != C[b][both]).sum()),
                   "mean_abs_gap": float(np.abs(C[a] - C[b])[both].mean())}
            for delta in deltas:
                need = None
                for n in range(1, Jab + 1):
                    var = vi / n * (Jab - n) / max(Jab - 1, 1) + vn / n
                    if delta / math.sqrt(var) >= z:
                        need = n
                        break
                row[f"n_for_{int(delta*100)}pt_gap"] = need  # None = not separable
            out.append(row)
    return sorted(out, key=lambda r: -(r["n_for_5pt_gap"] or 999))


if __name__ == "__main__":
    (names, C, W), ids, synth = load_matrix()
    print(f"{'SYNTHETIC' if synth else 'REAL'} matrix: {C.shape[0]} candidates x {C.shape[1]} statements, "
          f"{np.isnan(C).mean():.0%} uncoded")
    n_resp = int(sys.argv[1]) if len(sys.argv) > 1 else 800
    report = {"synthetic": synth, "candidates": names}
    for r_tt in (0.55, 0.65, 0.75):
        res, sigma, margin = simulate(C, W, n_resp=n_resp, r_tt=r_tt, core=app_core(ids))
        summ = summarise(res)
        report[f"r_tt={r_tt}"] = {"sigma": sigma, "share_decisive": float((margin >= 0.05).mean()),
                                  "curves": {s: {str(n): v for n, v in d.items()} for s, d in summ.items()}}
        print(f"\nr_tt={r_tt} sigma={sigma:.2f}  share of respondents with true margin>=5pts: {(margin>=.05).mean():.0%}")
        print("strategy   n   top1  top1|decisive  within2pts  regret(pts)")
        for s, d in summ.items():
            for n, v in d.items():
                print(f"{s:9s} {n:3d}  {v['top1']:.2f}   {v['top1_decisive']:.2f}          {v['near_top_2pts']:.2f}       {v['mean_regret_pts']:.1f}")
    sigma = report["r_tt=0.65"]["sigma"]
    pairs = pair_n(C, W, sigma)
    for r in pairs:
        r["a"], r["b"] = names[r["a"]], names[r["b"]]
    report["pairs"] = pairs
    report["hardest_pairs"] = pairs[:12]
    print("\nHardest pairs (items needed for 90% correct ordering at a true 5/10-point gap; None = not separable):")
    for p in report["hardest_pairs"]:
        print(p)
    json.dump(report, open(ROOT / "analysis" / ("power_synthetic.json" if synth else "power_real.json"), "w"), indent=1, default=float)
