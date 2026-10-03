"""
"The Missing Minute": theory checks and the Old Faithful analysis.
Every number in the paper's Tables 1-6 is produced here. Seeded; run:
    python3 code/analysis.py       (writes results/results2.json)
Data: geyser.csv, the 1985 Old Faithful record of Azzalini & Bowman (1990)
as distributed in R's MASS package (via the Rdatasets mirror).
"""
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
from scipy import stats

rng = np.random.default_rng(20261003)
TAU = 2 * np.pi
out = {}

def resultant(theta):
    z = np.exp(1j * theta).mean()
    return abs(z), np.angle(z)

def coherence(t, X, kmax):
    """C(k) = |mean_j exp(i w (t_{j+k} - t_j))|, w = 2 pi / X."""
    w = TAU / X
    return [float(abs(np.exp(1j * w * (t[k:] - t[:-k])).mean())) for k in range(1, kmax + 1)]

def wait_stats(t, m=200_000):
    u = rng.uniform(t[0], t[-1], m)
    i = np.searchsorted(t, u)
    return float((t[i] - u).mean()), float((t[i] - t[i - 1]).mean())

# ---------------------------------------------------------------- 1. phase precision
# Type I (scheduled + Gaussian jitter): rho = exp(-2 pi^2 s^2 / X^2), rho2 = rho^4.
# Cyclostationary Poisson, intensity l0 (1 + kappa cos(.)): rho = kappa/2, rho2 = 0.
# Prediction: SE(phi_hat) = (X / 2pi) sqrt((1 - rho2) / (2 N rho^2)).
X = 10.0
REPS = 400
prec = []
for kind, par in [("jitter", 1.0), ("jitter", 2.0), ("jitter", 3.0), ("modulated", 1.0), ("modulated", 0.5), ("modulated", 0.2)]:
    for N in (100, 1000):
        errs, Rs = [], []
        for _ in range(REPS):
            phi = rng.uniform(0, X)
            if kind == "jitter":
                t = phi + X * np.arange(N) + rng.normal(0, par, N)
                rho, rho2 = np.exp(-2 * np.pi**2 * par**2 / X**2), np.exp(-8 * np.pi**2 * par**2 / X**2)
            else:
                # sample N event phases from density (1 + kappa cos(theta - psi)) / 2pi by rejection
                psi = TAU * phi / X
                th = np.empty(0)
                while th.size < N:
                    c = rng.uniform(0, TAU, 4 * N)
                    keep = rng.uniform(0, 1 + par, c.size) < 1 + par * np.cos(c - psi)
                    th = np.concatenate([th, c[keep]])
                t = th[:N] / TAU * X + X * rng.integers(0, 10_000, N)
                rho, rho2 = par / 2, 0.0
            R, ang = resultant(TAU * np.mod(t, X) / X)
            est = (ang % TAU) / TAU * X
            errs.append((est - phi + X / 2) % X - X / 2)
            Rs.append(R)
        se_pred = X / TAU * np.sqrt((1 - rho2) / (2 * N * rho**2))
        prec.append({"kind": kind, "param": par, "N": N, "rho_theory": float(rho), "R_mean": float(np.mean(Rs)),
                     "se_sim": float(np.std(errs)), "se_theory": float(se_pred)})
out["phase_precision"] = prec

# ---------------------------------------------------------------- 2. detection threshold
# Rayleigh test, alpha = 0.05, power 0.8: noncentral chi2(2, delta = 2 N rho^2).
crit = stats.chi2.ppf(0.95, 2)
delta80 = float(next(d for d in np.arange(0.01, 40, 0.001) if stats.ncx2.sf(crit, 2, d) >= 0.8))
det = []
for rho in (0.5, 0.3, 0.17, 0.1):
    nstar = int(np.ceil(delta80 / (2 * rho**2)))
    hits = 0
    for _ in range(2000):
        # modulated process with mean resultant rho (kappa = 2 rho)
        th = np.empty(0)
        while th.size < nstar:
            c = rng.uniform(0, TAU, 4 * nstar + 8)
            keep = rng.uniform(0, 1 + 2 * rho, c.size) < 1 + 2 * rho * np.cos(c)
            th = np.concatenate([th, c[keep]])
        R, _ = resultant(th[:nstar])
        hits += (2 * nstar * R**2) > crit
    det.append({"rho": rho, "N_star": nstar, "power_sim": hits / 2000})
out["detection"] = {"delta_80": delta80, "N_star_formula": f"{delta80/2:.2f} / rho^2", "rows": det}

# ---------------------------------------------------------------- 3. phase memory
# Type I: C(k) = rho^2 for all k >= 1.  Type II (renewal, gamma intervals, shape a):
# C(k) = |psi|^k, |psi| = (1 + (2pi/a)^2)^(-a/2).  Type III (Poisson): a = 1.
K = 8
N = 20_000
mem = {}
s = 2.0
t1 = X * np.arange(N) + rng.normal(0, s, N); t1.sort()
rho1 = np.exp(-2 * np.pi**2 * s**2 / X**2)
mem["typeI_jitter_s2"] = {"sim": coherence(t1, X, K), "theory": [float(rho1**2)] * K}
for a in (25.0, 4.0):   # CV 0.2 and 0.5
    t2 = np.cumsum(rng.gamma(a, X / a, N))
    psi = (1 + (TAU / a) ** 2) ** (-a / 2)
    mem[f"typeII_gamma_cv{1/np.sqrt(a):.1f}"] = {"sim": coherence(t2, X, K), "theory": [float(psi**k) for k in range(1, K + 1)],
                                                "memory_length_events": float(-1 / np.log(psi))}
t3 = np.cumsum(rng.exponential(X, N))
psi3 = (1 + TAU**2) ** -0.5
mem["typeIII_poisson"] = {"sim": coherence(t3, X, K), "theory": [float(psi3**k) for k in range(1, K + 1)],
                          "memory_length_events": float(-1 / np.log(psi3))}
mem["noise_floor_1_over_sqrtN"] = float(1 / np.sqrt(N))
out["phase_memory"] = mem

# ---------------------------------------------------------------- 4. waiting identity beyond renewal
wi = {}
for name, t in [("typeI_jitter_s2", t1), ("typeII_cv0.5", np.cumsum(rng.gamma(4.0, X / 4.0, N))), ("typeIII_poisson", t3)]:
    gaps = np.diff(t)
    w, st = wait_stats(t)
    wi[name] = {"cv": float(gaps.std() / gaps.mean()), "wait_sim": w, "wait_theory": float((gaps**2).mean() / (2 * gaps.mean())),
                "straddle_sim": st, "straddle_theory": float((gaps**2).mean() / gaps.mean())}
out["waiting_identity"] = wi

# ---------------------------------------------------------------- 5. Old Faithful, 1985
g = np.genfromtxt(ROOT / "data" / "geyser.csv", delimiter=",", names=True)
iv = g["waiting"].astype(float)
t = np.concatenate([[0.0], np.cumsum(iv)])
Xg = iv.mean(); cv = iv.std() / Xg
w = TAU / Xg
psi_hat = np.exp(1j * w * iv).mean()
Rfull, _ = resultant(TAU * np.mod(t, Xg) / Xg)
Zfull = 2 * t.size * Rfull**2
wsim, stsim = wait_stats(t)
r1 = np.corrcoef(iv[:-1], iv[1:])[0, 1]
# bootstrap noise floor for C(k): coherence of the same intervals in shuffled order is the
# renewal prediction; the floor is the coherence of uniform phases with the same n.
Ck = coherence(t, Xg, 6)
floor = [float(np.sqrt(np.pi / (4 * (t.size - k)))) for k in range(1, 7)]  # E|mean of n unit phasors| ~ sqrt(pi/(4n))
out["old_faithful"] = {
    "eruptions": int(t.size), "intervals": int(iv.size), "record_days": float(t[-1] / 1440),
    "X_mean_interval_min": float(Xg), "interval_sd": float(iv.std()), "cv": float(cv),
    "interval_min": float(iv.min()), "interval_max": float(iv.max()),
    "share_under_65": float((iv < 65).mean()),
    "lag1_autocorr": float(r1),
    "inspection_multiplier_1_plus_c2": float(1 + cv**2),
    "wait_naive_X_over_2": float(Xg / 2), "wait_theory": float((iv**2).mean() / (2 * Xg)), "wait_sim": wsim,
    "straddle_theory": float((iv**2).mean() / Xg), "straddle_sim": stsim,
    "abs_psi": float(abs(psi_hat)), "memory_length_events": float(-1 / np.log(abs(psi_hat))),
    "coherence_C_k": Ck, "renewal_prediction_abs_psi_k": [float(abs(psi_hat) ** k) for k in range(1, 7)],
    "uniform_noise_floor": floor,
    "rayleigh_full_record_R": float(Rfull), "rayleigh_full_record_Z": float(Zfull), "rayleigh_full_record_p": float(np.exp(-Zfull / 2)),
}
# Phase diffusion: C(k) ~ exp(-w^2 Var(S_k) / 2), S_k = sum of k consecutive intervals.
Sx = t
vk = [float((Sx[k:] - Sx[:-k]).var()) for k in range(1, 31)]
of = out["old_faithful"]
of["autocorr_lag1_to_6"] = [float(np.corrcoef(iv[:-k], iv[k:])[0, 1]) for k in range(1, 7)]
of["var_S_k_1_to_6"] = vk[:6]
of["renewal_var_k_sigma2_1_to_6"] = [float(k * iv.var()) for k in range(1, 7)]
of["gaussian_diffusion_prediction_C_k"] = [float(np.exp(-w * w * v / 2)) for v in vk[:6]]
of["cv_two_eruption_span"] = float(np.sqrt(vk[1]) / (2 * Xg))
# long-run diffusion per eruption: slope of Var(S_k) over k = 10..30
slope = float(np.polyfit(np.arange(10, 31), vk[9:30], 1)[0])
of["long_run_diffusion_per_eruption_min2"] = slope
of["diffusion_ratio_vs_renewal"] = float(slope / iv.var())
of["memory_length_diffusion_events"] = float(2 / (w * w * slope))
of["memory_length_diffusion_hours"] = float(2 / (w * w * slope) * Xg / 60)
json.dump(out, open(ROOT / "results" / "results2.json", "w"), indent=1)
print(json.dumps(out, indent=1))
