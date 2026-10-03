"""Figures 1 and 2 for "The Missing Minute", from results2.json."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("svg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "paper" / "figures"
r = json.load(open(ROOT / "results" / "results2.json"))
BLUE, ORANGE, AQUA, INK, MUTED, GRID = "#2a78d6", "#eb6834", "#1baf7a", "#1a1a19", "#5c5b55", "#e4e3dd"
plt.rcParams.update({"font.family": "Liberation Serif", "font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "svg.fonttype": "none"})

def frame(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)

# Figure 1: phase memory by type (log scale)
m = r["phase_memory"]
k = list(range(1, 9))
fig, ax = plt.subplots(figsize=(5.6, 3.5))
series = [("Type I: scheduled, jitter σ = 2", m["typeI_jitter_s2"], BLUE, "o", "-"),
          ("Type II: renewal, c = 0.2", m["typeII_gamma_cv0.2"], ORANGE, "s", "--"),
          ("Type III: Poisson", m["typeIII_poisson"], AQUA, "^", ":")]
for label, d, col, mk, ls in series:
    ax.plot(k, d["theory"], color=col, linewidth=1.6, linestyle=ls, label=label + " (theory)")
    ax.plot(k, d["sim"], linestyle="none", marker=mk, markersize=5.5, markerfacecolor=col, markeredgecolor="white",
            markeredgewidth=0.8)
floor = m["noise_floor_1_over_sqrtN"]
ax.axhline(floor, color=MUTED, linewidth=0.8, linestyle=(0, (1, 2)))
ax.text(8.15, floor, "noise floor", va="center", fontsize=8, color=MUTED)
ax.text(8.15, m["typeI_jitter_s2"]["theory"][0], "Type I", va="center", fontsize=8, color=INK)
ax.text(2.25, m["typeII_gamma_cv0.2"]["theory"][1] * 1.15, "Type II", fontsize=8, color=INK)
ax.text(1.25, m["typeIII_poisson"]["theory"][0] * 0.62, "Type III", fontsize=8, color=INK)
ax.set_yscale("log")
ax.set_ylim(1e-3, 1.2)
ax.set_xlim(0.7, 9.1)
ax.set_xticks(k)
ax.set_xlabel("Events apart, k")
ax.set_ylabel("Phase coherence C(k)")
frame(ax)
ax.legend(frameon=False, fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, 1.28), ncol=2, handlelength=2.6)
fig.tight_layout()
fig.savefig(FIG / "fig1-memory.svg")

# Figure 2: Old Faithful
o = r["old_faithful"]
k = list(range(1, 7))
fig, ax = plt.subplots(figsize=(5.6, 3.1))
ax.axhspan(0, o["uniform_noise_floor"][0], color=GRID, alpha=0.7, linewidth=0)
ax.text(6.1, o["uniform_noise_floor"][0] / 2, "noise floor", va="center", fontsize=8, color=MUTED)
ax.plot(k, o["renewal_prediction_abs_psi_k"], color=ORANGE, linewidth=1.6, linestyle="--", marker="s", markersize=5,
        markerfacecolor=ORANGE, markeredgecolor="white", label=r"Renewal prediction $|\psi|^k$")
ax.plot(k, o["gaussian_diffusion_prediction_C_k"], color=AQUA, linewidth=1.6, linestyle=":", marker="^", markersize=5.5,
        markerfacecolor=AQUA, markeredgecolor="white", label="Phase-diffusion prediction")
ax.plot(k, o["coherence_C_k"], color=BLUE, linewidth=0, marker="o", markersize=6.5, markerfacecolor=BLUE,
        markeredgecolor="white", label="Observed, Old Faithful 1985")
ax.text(2.12, o["coherence_C_k"][1] + 0.025, "observed", fontsize=8, color=INK)
ax.text(3.1, o["renewal_prediction_abs_psi_k"][2] + 0.03, "renewal", fontsize=8, color=INK)
ax.set_ylim(0, 0.75)
ax.set_xlim(0.7, 6.9)
ax.set_xticks(k)
ax.set_xlabel("Eruptions apart, k")
ax.set_ylabel("Phase coherence C(k)")
frame(ax)
ax.legend(frameon=False, fontsize=7.5, loc="upper right")
fig.tight_layout()
fig.savefig(FIG / "fig2-old-faithful.svg")
print("ok")
