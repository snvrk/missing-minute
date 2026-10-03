# The Missing Minute

**Phase, Memory and Waiting in "Every X Minutes" Claims**
SNVRK (Caleb Gottfried) · Version 1.0 · October 3, 2026 · ORCID [0009-0000-1948-412X](https://orcid.org/0009-0000-1948-412X)

📄 [Paper (PDF)](paper/missing-minute-v1.pdf) · [HTML](paper/missing-minute.html)

> "An event happens every X minutes" reads like a timetable. But a timetable needs two numbers, an interval and the minute it starts, and the second is never given. This paper resolves that paradox exactly and shows what such claims leave out.

## Key results

| Result | Statement |
|---|---|
| **Theorem 1: when the start minute exists** | A start minute exists exactly when the process has a **spectral line** at frequency 1/X, that is, an atom in its Bartlett spectrum. When it exists, it belongs to each realization and is uniform across realizations. No statistic can state it, but it can be read off the events. Poisson, renewal and pooled processes have no line, so they have no start minute. |
| **Theorem 2: recovering it** | SE(φ̂) = (X/2π)·√[(1−ρ₂)/(2Nρ²)]. Detecting the phase takes about 4.8/ρ² events. |
| **Proposition 3 and Theorem 3: phase memory** | Span variance is the interval noise spectrum seen through a Fejér filter. The memory length is ℓ = 2/(ω²D) = 1/(2π²F), where F is the long-run Fano factor. Memory never fades **exactly** when the process is a schedule plus stationary errors. |
| **Proposition 4: a corrected periodicity test** | When phase memory is present, the naive Rayleigh test rejects at rate α^(1/τ) instead of α, with τ ≈ 2ℓ when memory is long. The paper gives a corrected test. |
| **Proposition 5: waiting** | For **any** stationary process, the mean wait from a random moment is (X/2)(1 + c²). |
| **Proposition 6: cost** | A Markovian clock's memory is bounded by the entropy it produces per tick: ℓ ≤ Δs/4π². |
| **Old Faithful, 1985** | Intervals alternate (lag-1 correlation −0.70; renewal rejected, p < 10⁻⁴). The geyser keeps time **2.6×** more precisely over two eruptions than one (95% CI 2.2–3.0), an "echo" from the two-interval filter. Phase memory is **≈ 5 eruptions** (95% CI 2.3–6.4), against 1.4 under renewal. The apparent full-record periodicity (naive p = 0.007) vanishes once memory is accounted for (p = 0.46). |
| **Coal-mining disasters, 1851–1962** | The pooled type: no phase and no memory. "One every 213 days" means a mean wait of **336** days, not 107. |

Every "every X minutes" claim should come with two more numbers: its coefficient of variation and its phase memory.

## Repository layout

```
paper/        missing-minute-v1.pdf, missing-minute.html, figures/
code/         sim.py         Table 1 (four "one every 10 minutes" processes)
              analysis.py    theory checks and core Old Faithful analysis (Tables 2, 4, 5; Figure 2)
              robustness.py  bootstrap, surrogate and corrected tests, size study, spectral line,
                             coal record, ring clocks (Tables 3, 6, 7; Figures 1, 3)
              figures.py     Figures 1–3 (SVG)
data/         geyser.csv     Azzalini & Bowman Old Faithful record (see data/README.md)
              coal.csv       Jarrett coal-mining disasters (see data/README.md)
results/      results.json, results2.json, results3.json   every number in the paper
```

## Reproduce

```sh
python3 -m pip install -r requirements.txt
python3 code/sim.py          # results/results.json
python3 code/analysis.py     # results/results2.json
python3 code/robustness.py   # results/results3.json
python3 code/figures.py      # paper/figures/*.svg
```

All randomness is seeded (20261003 and 20261004), so a clean run reproduces every `results/*.json` file exactly. The full run takes a few minutes on a laptop.

## Cite

See [`CITATION.cff`](CITATION.cff), or use GitHub's "Cite this repository" button.

## License

[![W2FPL](https://snvrkotics.com/brand/licenses/w2fpl/w2fpl-88x31.png)](https://snvrkotics.com/licenses/w2fpl)

The code, results, figures and paper are released under the [W2FPL, Version 1](LICENSE) (DO WHAT THE FUCK YOU WANT TO, WHEN YOU WANT TO PUBLIC LICENSE). See https://snvrkotics.com/w2fpl.

**Exception:** the files in `data/` are third-party data. They are not covered by the W2FPL and keep their original terms. See [`data/README.md`](data/README.md).
