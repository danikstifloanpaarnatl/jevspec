# JevSpec (ex-JevTree)

Training-free, auditable **typed decision specs** for budgeted feature acquisition (AFA) under hard budgets.

Corresponding manuscript: *JevSpec: Training-Free, Auditable Typed Decision Specs for Budgeted Feature Acquisition* (Hazel Bloomer, preprint).

The framework couples budgeted feature acquisition with an ID3-style decision tree and exports an auditable typed decision spec (`tree.json`, a `DecisionSOP`, per-instance receipts) expressed in the `Choice` / `Noul` / `Score` primitives of the System One decision-model paradigm. Acquisition is **training-free**: policies consume an information-gain ranking computed once on quantile-binned training data; no learned acquisition model is called.

## Repository layout

```
jevtree/          Implementation (Python package, `pip install -e .`)
configs/         61 evaluation configurations (MiniBooNE / Diabetes / local cube; main + ablations)
data/            Aggregated experiment results
scripts/         Plotting and result-aggregation scripts
```

## Data files

| File | Meaning |
|---|---|
| `data/gen_results.json` | **Authoritative aggregate** of all 61 runs (serial re-run, 0 failures). Numbers in the paper's tables/figures come from this file. |
| `data/experiment_results.json` | Mirror of per-run summaries. **Caveat:** MiniBooNE split-0 entries were duplicated during an early parallel-run race and were re-run later; do **not** recompute means from this file alone. |
| `data/plot_data.json` | Aggregated table used by `scripts/make_exp_figs.py` (same numbers as the tables). |

## Reproducing the experiments

1. Install: `pip install -e jevtree/` (Python 3.13 venv; requires `paramiko` only for the internal SSH transport, not for evaluation).
2. Run one evaluation: `jevtree eval-afa --config configs/miniboone_ig_static_s0.json`
3. Repeat over the 61 configs (serial runner advised — parallel runs with same-second result dirs can overwrite each other).
4. Aggregate: `python scripts/plot_aggregate.py` → `plot_data.json`; figures: `python scripts/make_exp_figs.py`, `python scripts/make_overview_fig.py`.

### Protocol (as in the paper)

- Hard-budget episodes start fully unobserved; a policy acquires up to `B` features, then a **shared predictor** per dataset scores the instance.
- MiniBooNE (d=50, 4 splits) and Diabetes (OpenML 37, d=8, 3 splits): shared masked-logistic predictor (L2 logistic + mean imputation).
- Local 5-feature cube (256 rows, 3 match-majority splits): match-majority predictor for all policies. This cube is **not** the official AFABench CUBE-NM benchmark.
- Budgets: MiniBooNE {5,10,20,40}; Diabetes {5,10,20}; cube {1,2,3}.
- Defaults: `n_bins=4`, `min_samples=20`, `max_candidates=15`.

## Headline numbers (MiniBooNE, shared masked-logistic, accuracy)

| Policy | B=5 | B=10 | B=20 | B=40 |
|---|---|---|---|---|
| ig_static | **0.806** | **0.849** | 0.878 | 0.886 |
| ig_conditional | 0.767 | 0.819 | 0.867 | 0.896 |
| ig_discriminative (ELLG) | 0.729 | 0.732 | 0.746 | 0.756 |
| random | 0.722 | 0.747 | 0.760 | 0.877 |
| sequential | 0.735 | 0.795 | 0.829 | **0.905** |

Static IG leads at low budgets (+8.4 pts over random at B=5); ELLG collapses toward random under the lightweight linear backbone (documented negative result, see paper Section "ELLG collapse analysis").

## License / contact

No license is attached yet. For the implementation, data or manuscript details, contact the corresponding author.
