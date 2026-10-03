# The Missing Minute

**Phase, Memory and Waiting in "Every X Minutes" Claims**
Caleb Gottfried · Version 2.0 · October 2026

📄 [Paper (PDF)](paper/missing-minute.pdf) · [HTML](paper/missing-minute.html) · [Version 1](paper/v1/missing-minute-v1.pdf)

> "An event happens every X minutes" reads as a timetable, but a timetable needs two numbers: an interval and the minute it starts. The second is never given, so a claim that sounds testable cannot be checked against a clock. This paper resolves that paradox and shows it hides two measurable quantities such claims always leave out.

## Key results

| Result | Statement |
|---|---|
| **Theorem 1: when the start minute exists** | A well-defined phase exists exactly when the first Fourier coefficient of the intensity at period X is nonzero. For every stationary process, including the pooled processes behind public statistics, it is zero, so the start minute does not exist. |
| **Recovering it** | When it exists, phase is recoverable from event times alone. The standard error is SE(φ̂) = (X/2π)·√[(1−ρ₂)/(2Nρ²)], and detection needs about 4.8/ρ² events. Both are confirmed by simulation. |
| **Phase memory** | This is how many events ahead an "every X" schedule stays predictable. It is set by Var(S_k), the variance of the time spanned by k consecutive intervals. That splits processes into three types. **Scheduled** processes never fade. **Renewal** processes fade geometrically. **Pooled** processes are gone after one event. |
| **Old Faithful (1985, 299 intervals)** | The record is not a renewal process (lag-1 autocorrelation −0.70). It keeps time 2.6× more regularly over two eruptions than over one. It remembers its phase for about **5.4 eruptions (6.6 h)**, against the renewal prediction of 1.2. The phase-diffusion law C(k) ≈ exp(−ω²Var(S_k)/2) matches the observed coherence at every lag. |
| **Proposition 4: waiting** | By Palm inversion, the mean wait from a random moment is (X/2)(1 + c²) for **any** stationary process, renewal or not. |

The conclusion is that every "every X minutes" claim should come with two more numbers: its coefficient of variation and its phase memory.

## Repository layout

```
paper/        missing-minute.html / .pdf (v2), figures/, v1/
code/         sim.py       Table 1 (the four "one every 10 minutes" processes)
              analysis.py  theory checks, Old Faithful analysis (Tables 2–4)
              figures.py   Figures 1–2 (SVG)
data/         geyser.csv   Azzalini & Bowman Old Faithful record (see data/README.md)
results/      results.json, results2.json  every number reported in the paper
```

## Reproduce

```sh
python3 -m pip install -r requirements.txt
python3 code/sim.py         # writes results/results.json
python3 code/analysis.py    # writes results/results2.json
python3 code/figures.py     # writes paper/figures/*.svg
```

All randomness uses the fixed seed 20261003, so a clean run reproduces both `results/*.json` files exactly. The full run takes a few minutes on a laptop.

## Versions

- **v2.0** (this version) adds Theorems 1–2 and Propositions 3–4, phase memory with the three-type classification, the Old Faithful analysis, figures, and proofs (Appendix A).
- **v1.0** is the original paper, kept unchanged in [`paper/v1/`](paper/v1/).

On Zenodo, both versions sit under one concept DOI. Each version also has its own DOI.

## Cite

See [`CITATION.cff`](CITATION.cff), or use GitHub's "Cite this repository" button.

## License

The code, results, figures and paper are released under the [W2FPL, Version 1](LICENSE) (DO WHAT THE FUCK YOU WANT TO, WHEN YOU WANT TO PUBLIC LICENSE). See https://snvrkotics.com/w2fpl.

**Exception:** `data/geyser.csv` is not covered by the W2FPL. It is third-party data distributed under GPL-2 | GPL-3 and keeps its original terms. See [`data/README.md`](data/README.md).
