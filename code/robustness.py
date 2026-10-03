"""
"The Missing Minute": uncertainty, robustness and extensions.
  - Old Faithful: block-bootstrap intervals, shuffle-surrogate test of renewal,
    the phase-memory-corrected Rayleigh test, the eruption-duration mechanism,
    and a line-free AR model check of the observed coherence.
  - Size of the naive and corrected Rayleigh tests under phase memory.
  - Spectral line (Theorem 1): R against N for the three types.
  - Coal-mining disasters, 1851-1962: a pooled ("Type III") record.
  - Brownian ring clocks: phase memory against the thermodynamic bound.
Seeded; run:  python3 code/robustness.py   (writes results/results3.json)
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import toeplitz, solve

ROOT = Path(__file__).resolve().parent.parent
rng = np.random.default_rng(20261004)
TAU = 2 * np.pi
out = {}

# ------------------------------------------------------------------ helpers
def times(iv):
    return np.concatenate([[0.0], np.cumsum(iv)])

def coherence_c(t, X, kmax):
    """Complex mean of exp(i w S_k) over all spans of k intervals, k = 1..kmax."""
    w = TAU / X
    return np.array([np.exp(1j * w * (t[k:] - t[:-k])).mean() for k in range(1, kmax + 1)])

def rayleigh(t, X):
    z = np.exp(1j * TAU * t / X).mean()
    return abs(z), 2 * t.size * abs(z) ** 2

def tau_hat(t, X, L=None):
    """Variance inflation of the resultant, 1 + 2 sum_{k<=L} Re E[exp(i w S_k)], truncated at L = N/10."""
    L = L or max(1, t.size // 10)
    return max(1.0, 1 + 2 * float(coherence_c(t, X, L).real.sum()))

def acf(x, kmax):
    x = x - x.mean()
    n = x.size
    return np.array([(x[: n - j] * x[j:]).sum() / n for j in range(kmax + 1)])

def ar_fit(x, p):
    r = acf(x, p)
    a = solve(toeplitz(r[:p]), r[1:])
    return a, float(r[0] - a @ r[1:])

def ar_aic(x, pmax=8):
    n = x.size
    best = min(range(1, pmax + 1), key=lambda p: n * np.log(ar_fit(x, p)[1]) + 2 * p)
    return best, *ar_fit(x, best)

def ar_sim(a, resid, mean, n, burn=300):
    p = a.size
    e = rng.choice(resid, n + burn)
    x = np.zeros(n + burn)
    for i in range(p, n + burn):
        x[i] = a @ x[i - p:i][::-1] + e[i]
    return mean + x[burn:]

def D_slope(iv):
    t = times(iv)
    v = [(t[k:] - t[:-k]).var() for k in range(10, 31)]
    return float(np.polyfit(np.arange(10, 31), v, 1)[0])

def D_bartlett(iv, L=10):
    r = acf(iv, L)
    return float(r[0] + 2 * sum((1 - j / (L + 1)) * r[j] for j in range(1, L + 1)))

def D_ar(iv):
    p, a, s2 = ar_aic(iv)
    return float(s2 / (1 - a.sum()) ** 2), p

def wait_stats(t, m=200_000):
    u = rng.uniform(t[0], t[-1], m)
    i = np.searchsorted(t, u, side="right")
    return float((t[i] - u).mean()), float((t[i] - t[i - 1]).mean())

def ci(a):
    return [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]

# ------------------------------------------------------------------ 1. Old Faithful
g = np.genfromtxt(ROOT / "data" / "geyser.csv", delimiter=",", names=True)
iv = g["waiting"].astype(float)      # waiting[i]: time from the previous eruption to eruption i
dur = g["duration"].astype(float)
t = times(iv)
X = iv.mean()
w = TAU / X

def of_stats(iv):
    t = times(iv)
    X = iv.mean()
    w = TAU / X
    s2 = iv.var()
    c = np.abs(coherence_c(t, X, 2))
    v2 = (t[2:] - t[:-2]).var()
    Dd = D_bartlett(iv)
    return {"cv": iv.std() / X, "r1": np.corrcoef(iv[:-1], iv[1:])[0, 1], "C1": c[0], "C2": c[1],
            "precision_gain_two_eruptions": (iv.std() / X) / (np.sqrt(v2) / (2 * X)),
            "D_bartlett": Dd, "ell_bartlett": 2 / (w * w * Dd), "renewal_over_D": s2 / Dd}

point = of_stats(iv)
B = 4000
# AR-sieve bootstrap: resample residuals of the fitted AR model (order by AIC), which keeps the
# alternation of the intervals; basic intervals 2*theta_hat - quantiles. A moving-block bootstrap
# (block 20) is kept as a sensitivity check: block joins break the alternation, biasing it toward renewal.
p0, a0, _ = ar_aic(iv)
xc = iv - iv.mean()
res0 = xc[p0:] - np.array([a0 @ xc[i - p0:i][::-1] for i in range(p0, iv.size)])
sieve = {k: [] for k in point}
for _ in range(B):
    x = np.clip(ar_sim(a0, res0, iv.mean(), iv.size), 1.0, None)
    for k, v in of_stats(x).items():
        sieve[k].append(v)
mbb = {k: [] for k in point}
nb = int(np.ceil(iv.size / 20))
for _ in range(B):
    starts = rng.integers(0, iv.size - 20 + 1, nb)
    x = np.concatenate([iv[s:s + 20] for s in starts])[: iv.size]
    for k, v in of_stats(x).items():
        mbb[k].append(v)
of = {"point": {k: float(v) for k, v in point.items()},
      "sieve_bootstrap_95ci_basic": {k: [float(2 * point[k] - np.percentile(v, 97.5)), float(2 * point[k] - np.percentile(v, 2.5))] for k, v in sieve.items()},
      "block20_bootstrap_95ci_percentile": {k: ci(v) for k, v in mbb.items()},
      "bootstrap_reps": B, "sieve_ar_order": p0}
D_s, (D_a, p_ar) = D_slope(iv), D_ar(iv)
of["D_estimators_min2"] = {"slope_k10_30": D_s, "bartlett_L10": point["D_bartlett"], f"ar_aic_p{p_ar}": D_a}
of["ell_estimators_events"] = {k: float(2 / (w * w * v)) for k, v in of["D_estimators_min2"].items()}
of["renewal_ell_gaussian_events"] = float(2 / (w * w * iv.var()))

# Shuffle surrogates: same intervals, random order = renewal null with the same marginal.
S = 10_000
c2s, ratio_s = np.empty(S), np.empty(S)
for i in range(S):
    x = rng.permutation(iv)
    tt = times(x)
    c2s[i] = abs(np.exp(1j * w * (tt[2:] - tt[:-2])).mean())
    ratio_s[i] = (tt[2:] - tt[:-2]).var() / x.var()
c2_obs = point["C2"]
ratio_obs = float((t[2:] - t[:-2]).var() / iv.var())
of["shuffle_test"] = {"surrogates": S, "C2_observed": float(c2_obs), "C2_surrogate_mean": float(c2s.mean()),
                      "C2_surrogate_max": float(c2s.max()), "p_C2": float((1 + (c2s >= c2_obs).sum()) / (S + 1)),
                      "varS2_over_varS1_observed": ratio_obs, "varS2_over_varS1_surrogate_95": ci(ratio_s),
                      "p_ratio": float((1 + (ratio_s <= ratio_obs).sum()) / (S + 1))}

# Rayleigh over the full record: naive vs corrected for phase memory.
R, Z = rayleigh(t, X)
th = tau_hat(t, X)
p_ar_order, a_ar, s2_ar = ar_aic(iv)
resid = (iv - iv.mean())[p_ar_order:] - np.array([a_ar @ (iv - iv.mean())[i - p_ar_order:i][::-1] for i in range(p_ar_order, iv.size)])
Rnull = []
for _ in range(4000):
    x = ar_sim(a_ar, resid, iv.mean(), iv.size)
    x = np.clip(x, 1.0, None)
    Rnull.append(rayleigh(times(x), x.mean())[0])
Rnull = np.array(Rnull)
of["rayleigh_full_record"] = {"R": float(R), "Z": float(Z), "p_naive": float(np.exp(-Z / 2)),
                              "tau_hat": th, "Z_corrected": float(Z / th), "p_corrected": float(np.exp(-Z / th / 2)),
                              "p_ar_parametric_bootstrap": float((1 + (Rnull >= R).sum()) / (Rnull.size + 1)),
                              "ar_null_R_median": float(np.median(Rnull)), "ar_order": p_ar_order}

# Mechanism: the wait after an eruption depends on that eruption's length.
nxt, cur = iv[1:], dur[:-1]
coded = np.isin(cur, [2.0, 3.0, 4.0])      # nocturnal durations recorded only as short/medium/long
slope, icpt = np.polyfit(cur[~coded], nxt[~coded], 1)
resid_m = nxt[~coded] - (icpt + slope * cur[~coded])
of["mechanism"] = {"corr_duration_next_wait": float(np.corrcoef(cur, nxt)[0, 1]),
                   "corr_duration_next_wait_exact_only": float(np.corrcoef(cur[~coded], nxt[~coded])[0, 1]),
                   "slope_min_per_min": float(slope), "intercept_min": float(icpt),
                   "resid_sd_min": float(resid_m.std()), "n_exact": int((~coded).sum()), "n_coded": int(coded.sum()),
                   "duration_lag1_corr": float(np.corrcoef(dur[:-1], dur[1:])[0, 1]),
                   "share_long_eruptions_over_3min": float((dur > 3).mean())}

# A line-free stationary model (AR, order by AIC) reproduces the observed coherence.
K = 6
sims = []
for _ in range(2000):
    x = np.clip(ar_sim(a_ar, resid, iv.mean(), iv.size), 1.0, None)
    sims.append(np.abs(coherence_c(times(x), x.mean(), K)))
sims = np.array(sims)
of["ar_model"] = {"order": p_ar_order, "coef": [float(v) for v in a_ar], "innov_var": s2_ar,
                  "C_k_observed": [float(v) for v in np.abs(coherence_c(t, X, K))],
                  "C_k_model_median": [float(v) for v in np.median(sims, 0)],
                  "C_k_model_90": [[float(np.percentile(sims[:, k], 5)), float(np.percentile(sims[:, k], 95))] for k in range(K)]}
out["old_faithful"] = of

# ------------------------------------------------------------------ 2. Rayleigh size under phase memory
# No spectral line in any design; intervals are AR(1) around X = 10 with CV 0.2.
size = {}
N, REPS, Xs = 300, 2000, 10.0
for name, phi in [("ar1_phi_-0.7", -0.7), ("ar1_phi_-0.4", -0.4), ("renewal_phi_0", 0.0), ("ar1_phi_+0.4", 0.4)]:
    sd_e = 0.2 * Xs * np.sqrt(1 - phi**2)
    naive = corr = 0
    taus = []
    for _ in range(REPS):
        e = rng.normal(0, sd_e, N + 200)
        x = np.zeros(N + 200)
        for i in range(1, N + 200):
            x[i] = phi * x[i - 1] + e[i]
        x = np.clip(Xs + x[200:], 0.5, None)
        tt = times(x)
        Xh = x.mean()
        _, Zs = rayleigh(tt, Xh)
        th_ = tau_hat(tt, Xh)
        taus.append(th_)
        naive += np.exp(-Zs / 2) < 0.05
        corr += np.exp(-Zs / th_ / 2) < 0.05
    D = (0.2 * Xs) ** 2 * (1 + phi) / (1 - phi)
    ell = 2 / ((TAU / Xs) ** 2 * D)
    size[name] = {"phi": phi, "ell_theory": float(ell), "tau_theory_approx_2ell": float(2 * ell),
                  "tau_hat_mean": float(np.mean(taus)), "size_naive": naive / REPS, "size_corrected": corr / REPS}
out["rayleigh_size"] = {"N": N, "reps": REPS, "alpha": 0.05, "designs": size}

# ------------------------------------------------------------------ 3. Spectral line: R against N
Ns = [30, 100, 300, 1000, 3000, 10000, 30000]
line = {}
designs = {
    "typeI_jitter_s2": lambda n: Xs * np.arange(n) + rng.normal(0, 2.0, n),
    "typeII_gamma_cv0.2": lambda n: times(rng.gamma(25.0, Xs / 25.0, n - 1)),
    "typeIII_poisson": lambda n: times(rng.exponential(Xs, n - 1)),
}
def of_like(n):
    x = np.clip(ar_sim(a_ar, resid, iv.mean(), n - 1), 1.0, None)
    return times(x * Xs / iv.mean())
designs["old_faithful_ar_model"] = of_like
for name, f in designs.items():
    line[name] = []
    for n in Ns:
        reps = 200 if n <= 3000 else 60
        Rs = [rayleigh(np.sort(f(n)), Xs)[0] for _ in range(reps)]
        line[name].append(float(np.mean(Rs)))
line["N"] = Ns
line["typeI_theory_rho"] = float(np.exp(-2 * np.pi**2 * 4 / Xs**2))
out["spectral_line"] = line

# ------------------------------------------------------------------ 4. Coal-mining disasters
c = np.genfromtxt(ROOT / "data" / "coal.csv", delimiter=",", names=True)["date"]
tc = np.sort(c) * 365.25
ivc = np.diff(tc)
Xc = ivc.mean()
cvc = ivc.std() / Xc
wc, stc = wait_stats(tc)
Rc, Zc = rayleigh(tc, Xc)
thc = tau_hat(tc, Xc)
Cc = np.abs(coherence_c(tc, Xc, 6))
cut = 1890.0
pre, post = np.diff(tc[c < cut]), np.diff(tc[c >= cut])
out["coal"] = {"events": int(tc.size), "first_year": float(c.min()), "last_year": float(c.max()),
               "X_days": float(Xc), "cv": float(cvc), "inspection_multiplier": float(1 + cvc**2),
               "wait_naive_days": float(Xc / 2), "wait_theory_days": float((ivc**2).mean() / (2 * Xc)), "wait_sim_days": wc,
               "straddle_theory_days": float((ivc**2).mean() / Xc), "straddle_sim_days": stc,
               "lag1_autocorr": float(np.corrcoef(ivc[:-1], ivc[1:])[0, 1]),
               "C_k": [float(v) for v in Cc], "noise_floor": [float(np.sqrt(np.pi / (4 * (tc.size - k)))) for k in range(1, 7)],
               "rayleigh_R": float(Rc), "rayleigh_p_naive": float(np.exp(-Zc / 2)), "tau_hat": thc,
               "rayleigh_p_corrected": float(np.exp(-Zc / thc / 2)),
               "split_year": cut, "pre_X_days": float(pre.mean()), "pre_cv": float(pre.std() / pre.mean()), "pre_n": int(pre.size),
               "post_X_days": float(post.mean()), "post_cv": float(post.std() / post.mean()), "post_n": int(post.size)}

# ------------------------------------------------------------------ 5. Brownian ring clocks vs. the thermodynamic bound
# M-state unicycle, forward rate f, backward b; a tick is the first completion of each new net cycle.
ring = []
for M, r in [(1, 20.0), (5, 20.0), (20, 20.0), (20, 3.0), (100, 3.0)]:
    f, bk = 1.0, 1.0 / r
    n_steps = 400_000 if M <= 20 else 2_000_000
    steps = np.where(rng.uniform(size=n_steps) < f / (f + bk), 1, -1)
    pos = np.cumsum(steps)
    dt = rng.exponential(1 / (f + bk), n_steps)
    tm = np.cumsum(dt)
    # first-passage times of pos to M, 2M, 3M, ...
    level = np.maximum.accumulate(pos)
    hit = np.flatnonzero(np.diff(level // M, prepend=0) > 0)
    tk = tm[hit]
    ivr = np.diff(tk)
    Xr = ivr.mean()
    Fano = (f + bk) / (M * (f - bk))
    ell_exact = 1 / (2 * np.pi**2 * Fano)
    ds = M * np.log(r)
    Cr = np.abs(coherence_c(tk, Xr, 3))
    ring.append({"M": M, "f_over_b": r, "entropy_per_tick_kB": float(ds), "ticks": int(tk.size),
                 "ell_theory": float(ell_exact), "ell_bound": float(ds / (4 * np.pi**2)),
                 "C1_sim": float(Cr[0]), "C1_theory": float(np.exp(-1 / ell_exact)),
                 "ell_from_sim_D": float(2 / ((TAU / Xr) ** 2 * D_bartlett(ivr, 20)))})
out["ring_clocks"] = ring

json.dump(out, open(ROOT / "results" / "results3.json", "w"), indent=1)
print(json.dumps(out, indent=1))
