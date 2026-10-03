# Publishing plan: The Missing Minute

The goal is a permanent DOI now, a preprint where statisticians will see it, and then one peer-reviewed journal. Each step lists who does it and what it needs.

| # | Step | Who | Status |
|---|---|---|---|
| 1 | Create an ORCID iD and add it to Zenodo, arXiv and the journal account | You | To do |
| 2 | Zenodo DOI from a GitHub release | You (2 clicks), then me | Ready for the release |
| 3 | arXiv preprint, `stat.ME` (cross-list `stat.AP`) | You submit; I prepare the files | Needs an endorser |
| 4 | Journal: *The American Statistician* | You submit; I convert to LaTeX and trim | After arXiv |
| 5 | Popular version for *Significance* | Pitch after the preprint | Optional |

## 1. ORCID (10 minutes, free)

Register at https://orcid.org. Then add the iD to `CITATION.cff` and `.zenodo.json`; send it to me and I'll do it. Zenodo, arXiv and journals all link to it, and Google Scholar uses it to merge your work under one name.

## 2. Zenodo DOI

The order matters: turn the integration on *before* creating the release.

1. Sign in at https://zenodo.org with GitHub. Go to **Account → GitHub** and flip the switch next to `snvrk/missing-minute`.
2. On GitHub, open **Releases → Draft a new release**, type `v1.0` in the tag box, choose **Create new tag: v1.0 on publish**, target `main`, title it `The Missing Minute v1.0`, and publish.
3. Zenodo archives the release within a few minutes, using the title, abstract and keywords in `.zenodo.json`. Open the new record and check two fields:
   - **License:** choose "Other (Open)" and paste https://snvrkotics.com/licenses/w2fpl.
   - **Related works:** the data files are third-party; the record already points to the repo, which explains this.
4. Send me the DOI. I'll add the badge to the README, the DOI to `CITATION.cff`, and the DOI to the paper's front page, then push.

Every later GitHub release becomes a new version under the same concept DOI.

## 3. arXiv

- **Category:** `stat.ME` (Methodology), cross-listed to `stat.AP` (Applications). The theorems, the corrected test and the Old Faithful analysis all fit there.
- **Format:** arXiv accepts a PDF that was not produced from TeX, so `paper/missing-minute-v1.pdf` can go up as it is. If you would rather submit LaTeX source, I can convert the paper.
- **Endorsement:** first-time submitters need an endorsement for each category. When you start the submission, arXiv gives you an endorsement code. Send it to one researcher who has published in `stat.ME` and whose work this paper cites or builds on. Good candidates are authors working on circular statistics, point-process spectra or renewal processes. The draft below is ready to send.
- **AI disclosure:** arXiv holds authors responsible for all content and does not allow AI tools as authors. The paper's disclosure statement already meets that.

### Endorsement request (draft)

> **Subject:** arXiv endorsement request, stat.ME: "The Missing Minute" (point-process phase, Rayleigh test under dependence)
>
> Dear Dr. [Name],
>
> I am an independent researcher preparing my first arXiv submission, and I would be grateful if you would consider endorsing me for stat.ME. The paper, "The Missing Minute: Phase, Memory and Waiting in 'Every X Minutes' Claims," builds on [their topic: e.g. circular statistics / spectral analysis of point processes].
>
> In brief, it shows three things. A process has a well-defined "start minute" at period X exactly when its Bartlett spectrum has an atom at 1/X. The Rayleigh test, applied to a process with serial dependence but no spectral line, rejects at rate α^(1/τ), where τ is the continuum at 1/X; the paper gives a corrected test. And the 1985 Old Faithful record keeps time 2.6 times more precisely over two eruptions than over one. The paper, code and data are at https://github.com/snvrk/missing-minute, and every result reproduces from a seeded script.
>
> My endorsement code is [CODE]. If you would rather not endorse, I would still welcome any comments on the paper.
>
> With thanks,
> Caleb Gottfried
> SNVRKOTICS LLC

## 4. Journal: *The American Statistician*

**Why this journal.** The paper's subject is the communication of a statistic, its methods are classical probability made usable, and Old Faithful is one of the best-known teaching datasets. *The American Statistician* publishes exactly that mix, in its General and Statistical Practice sections.

**What I'll do before you submit:**
- Convert the paper to LaTeX in the journal's template.
- Trim it to the current length limit. It is about 7,700 words before references now; check the limit in the journal's instructions for authors when we start. The likely cuts: move Proposition 6 and the ring clocks to a supplement, and shorten Section 11.
- Write a cover letter, an abstract within the word limit, and a "data and code availability" statement pointing to the Zenodo DOI.

**Submission:** through the journal's online system (Taylor & Francis), after the arXiv preprint is up. Note the preprint in the cover letter; ASA journals accept submissions that are already posted as preprints.

**Backups, in order:**
1. *Journal of the Royal Statistical Society Series A (Statistics in Society)*
2. *Stat* (short format, which would need a much shorter version)
3. *Journal of Statistical Theory and Practice*

### Cover letter (draft)

> Dear Editor,
>
> Please consider "The Missing Minute: Phase, Memory and Waiting in 'Every X Minutes' Claims" for publication in *The American Statistician*.
>
> Statements that an event happens "every X minutes" are among the most common ways statistics reach the public, yet they cannot be checked against a clock, because they never say what minute the schedule starts. The paper resolves this exactly. A start minute exists if and only if the process has a spectral line at 1/X, and it then belongs to the realization, not to any statistic. The paper also identifies two quantities such claims should report: the coefficient of variation, which sets the mean wait through (X/2)(1 + c²) for any stationary process, and the phase memory, which sets how far ahead the schedule can be trusted.
>
> The paper has a practical result for anyone who tests for periodicity in event data. When intervals are serially dependent, the Rayleigh test's size becomes α^(1/τ), and it reports nonexistent periodicity up to 75% of the time in our simulations. We give a corrected test. Applied to the 1985 Old Faithful record, the theory shows that the geyser keeps time 2.6 times more precisely over two eruptions than over one, and that an apparent periodicity in the full record (p = 0.007) is an artifact of memory (corrected p = 0.46).
>
> All code and data are public, and every number in the paper reproduces from seeded scripts (DOI: [Zenodo DOI]). A preprint is on arXiv ([arXiv ID]). The manuscript is not under consideration elsewhere. An AI writing tool assisted with drafting, as the paper discloses; I am responsible for all content.
>
> Sincerely,
> Caleb Gottfried

## 5. *Significance* (optional)

*Significance*, the magazine of the Royal Statistical Society and the American Statistical Association, publishes short, illustrated articles for a general audience. Pitch a piece of about 2,500 words with the working title "Old Faithful keeps time in pairs." It would cover the start-minute paradox, the 2.6× precision in pairs, and why "one disaster every seven months" meant waiting eleven. Pitch it once the arXiv preprint is up, and say in the pitch that the research article is under review elsewhere.

## Timeline

| When | What |
|---|---|
| Week 1 | ORCID; Zenodo DOI; start the arXiv submission and request an endorsement |
| Week 2 | arXiv preprint live; I convert the paper to LaTeX and trim it |
| Week 3 | Submit to *The American Statistician*; pitch *Significance* |
| Months 2–6 | Peer review, typically 2–4 months to a first decision. I can draft responses to the reviewers. |
