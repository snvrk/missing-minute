# Data

Both files are third-party data. They are included unmodified, only so the analysis can be reproduced. They are **not** covered by this repository's W2FPL license and keep their original terms.

## geyser.csv

Old Faithful geyser, Yellowstone National Park: 299 eruptions, observed continuously from 1 to 15 August 1985. `waiting` is the time in minutes since the previous eruption. `duration` is the eruption's length in minutes.

- **Original source:** Azzalini, A., and Bowman, A. W. "A look at some data on the Old Faithful geyser." *Applied Statistics* 39, no. 3 (1990): 357–365.
- **As distributed in:** the R package **MASS** (dataset `geyser`), which accompanies Venables, W. N., and Ripley, B. D., *Modern Applied Statistics with S*, 4th ed., Springer, 2002. Since MASS 7.3-30, `waiting` is the wait *before* each eruption. Some nocturnal durations were coded as 2, 3 or 4 minutes, from the original records of "short", "medium" or "long"; the paper excludes these from the duration analysis.
- **Obtained from:** the Rdatasets collection, https://github.com/vincentarelbundock/Rdatasets (`csv/MASS/geyser.csv`).
- **License:** MASS is distributed under GPL-2 | GPL-3.

The paper reconstructs event times by cumulating the `waiting` intervals.

## coal.csv

The dates of 191 explosions in British coal mines that killed ten or more people, from 15 March 1851 to 22 March 1962. Each `date` is a decimal year: the fraction is the share of the year that had elapsed on that day.

- **Original source:** Jarrett, R. G. "A note on the intervals between coal-mining disasters." *Biometrika* 66, no. 1 (1979): 191–193; also in Hand, D. J., et al., *A Handbook of Small Data Sets*, Chapman and Hall, 1994.
- **As distributed in:** the R package **boot** (dataset `coal`), which accompanies Davison, A. C., and Hinkley, D. V., *Bootstrap Methods and Their Application*, Cambridge University Press, 1997.
- **Obtained from:** the Rdatasets collection (`csv/boot/coal.csv`).
- **License:** as distributed with the boot package.

The paper converts dates to days at 365.25 days per year.
