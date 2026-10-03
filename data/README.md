# data/geyser.csv

This file holds 299 eruption intervals (`waiting`, minutes) and eruption durations (`duration`, minutes) for Old Faithful geyser, Yellowstone National Park. The eruptions were observed continuously from 1 to 15 August 1985.

- **Original source:** Azzalini, A., and Bowman, A. W. "A look at some data on the Old Faithful geyser." *Applied Statistics* 39, no. 3 (1990): 357–365.
- **As distributed in:** the R package **MASS** (dataset `geyser`), which accompanies Venables, W. N., and Ripley, B. D., *Modern Applied Statistics with S*, 4th ed., Springer, 2002.
- **Obtained from:** the Rdatasets collection, https://github.com/vincentarelbundock/Rdatasets (`csv/MASS/geyser.csv`).
- **License:** MASS is distributed under **GPL-2 | GPL-3**. This file is included unmodified, only so the analysis can be reproduced. It is **not** covered by this repository's W2FPL license.

The paper reconstructs event times by cumulating the `waiting` intervals.
