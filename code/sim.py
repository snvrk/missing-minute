"""
Simulations for "The Missing Minute": four processes that all satisfy
"an event every X minutes" on average, and what an observer can measure.
Reproducible: fixed seed. Run from the repository root: python3 code/sim.py
"""
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent

SEED = 20261003
X = 10.0            # the stated interval, minutes
T = 100_000.0       # observation window, minutes (~69.4 days)
M = 200_000         # random inspection times for the waiting-time measures
DAY = 1440.0
rng = np.random.default_rng(SEED)

def periodic(phi):
    return np.arange(phi, T, X)

def poisson(rate):
    n = rng.poisson(rate * T)
    return np.sort(rng.uniform(0, T, n))

def superposition(k=50):
    # k independent periodic sources, each about k*X apart, random phases
    out = []
    for _ in range(k):
        p = rng.uniform(0.9, 1.1) * k * X
        out.append(np.arange(rng.uniform(0, p), T, p))
    return np.sort(np.concatenate(out))

def diurnal(amp=0.5):
    # inhomogeneous Poisson by thinning; mean rate 1/X, daily cycle
    lam_max = (1 + amp) / X
    cand = poisson(lam_max)
    lam = (1 + amp * np.sin(2 * np.pi * cand / DAY)) / X
    keep = rng.uniform(0, 1, cand.size) < lam / lam_max
    return cand[keep]

def rayleigh(t, period):
    th = 2 * np.pi * np.mod(t, period) / period
    c, s = np.cos(th).sum(), np.sin(th).sum()
    n = t.size
    R = np.hypot(c, s) / n
    Z = 2 * n * R**2                      # ~ chi2(2) under uniform phase
    p = float(np.exp(-Z / 2))
    phase = (np.arctan2(s, c) % (2 * np.pi)) / (2 * np.pi) * period
    return R, Z, p, phase

def inspection(t):
    u = rng.uniform(t[0], t[-1], M)
    i = np.searchsorted(t, u)             # index of next event
    wait = t[i] - u
    straddle = t[i] - t[i - 1]
    return float(wait.mean()), float(straddle.mean())

results = {}
phi_true = float(rng.uniform(0, X))
procs = {
    "A_periodic": periodic(phi_true),
    "B_poisson": poisson(1 / X),
    "C_superposition_50": superposition(50),
    "D_diurnal_poisson": diurnal(0.5),
}
for name, t in procs.items():
    gaps = np.diff(t)
    R, Z, p, phase = rayleigh(t, X)
    w, s = inspection(t)
    r = {
        "events": int(t.size),
        "stated_X": X,
        "estimated_X_T_over_N": float(T / t.size),
        "interval_mean": float(gaps.mean()),
        "interval_cv": float(gaps.std() / gaps.mean()),
        "rayleigh_R_at_X": float(R),
        "rayleigh_Z_at_X": float(Z),
        "rayleigh_p_at_X": p,
        "recovered_phase_min": float(phase),
        "mean_wait_from_random_moment": w,
        "mean_interval_containing_random_moment": s,
    }
    if name == "D_diurnal_poisson":
        Rd, Zd, pd, phd = rayleigh(t, DAY)
        r.update({"rayleigh_R_at_1day": float(Rd), "rayleigh_Z_at_1day": float(Zd), "rayleigh_p_at_1day": pd})
    results[name] = r
results["A_periodic"]["true_phase_min"] = phi_true
results["meta"] = {"seed": SEED, "X": X, "T": T, "inspection_samples": M}

# Phase recovery with timing noise: periodic events with Gaussian jitter.
jit = {}
for sd in (0.5, 1.0, 2.0, 3.0):
    phi = float(rng.uniform(0, X))
    t = np.sort(periodic(phi) + rng.normal(0, sd, int(np.ceil((T - phi) / X))))
    t = t[(t >= 0) & (t < T)]
    R, Z, p, ph = rayleigh(t, X)
    err = (ph - phi + X / 2) % X - X / 2
    jit[str(sd)] = {"true_phase": phi, "recovered": float(ph), "error_min": float(err), "R": float(R), "p": p}
results["jittered_periodic"] = jit

json.dump(results, open(ROOT / "results" / "results.json", "w"), indent=2)
for k, v in results.items():
    print(k, json.dumps(v, indent=1) if k != "meta" else v)
