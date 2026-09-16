# Arrow: coinwise

- **Style**: [Keel](../../../Keel/), the installable Python package template.
  The arrow is whole and governed by Keel's law; its named incompleteness is
  stated in [its own README](../../arrows/coinwise/README.md).
- **Serves**: the tie-breaking line of [the question](../QUESTION.md), by
  implementing both rounding strategies and the deterministic drift
  experiment.
- **Reproduce**: from `arrows/coinwise`, with the package installed, run
  `python -c "from coinwise import run_drift_experiment as r; print(r(10_000)); print(r(100_000))"`,
  which prints both strategies' rounded totals, exact totals, drift, and tie
  counts at both scales; a re-pin quotes those figures digit for digit.
- **Claims resting on it**:
  [0008, The tie rule moves the total by dollars, not cents](../claims/0008-the-tie-rule-moves-the-total-by-dollars-not-cents.md) and
  [0009, Half even cancels the drift that half up accumulates](../claims/0009-half-even-cancels-the-drift-that-half-up-accumulates.md).
- **Verified**: 0008 at e3dea6153997, 0009 at e3dea6153997.
