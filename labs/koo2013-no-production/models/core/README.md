# Koo2013 Shear-Stress Induced NO Production Model

This core model package wraps the Koo et al. (2013) downstream nitric oxide production arm from BioModels source `BIOMD0000000467`. It receives cytosolic calcium as an external input and follows PI3K/AKT signalling, eNOS-complex assembly, and NO production.

User-facing charts, summaries, and plain-language explanations live in the sibling [`../visualisation`](../visualisation/README.md) model package.

## What the Run Shows

A default Biosimulant run lasts 600 s and renders six result panels. The captured views show calcium and calmodulin species, the PI3K/AKT signalling axis, eNOS activation-chain complexes, nitric oxide accumulation, largest-excursion diagnostics, and the What Happened summary table.

In the summary table, the run tracks 16 species observables. Nitric oxide is the largest-changing observable (`+1.3e+04`), Hsp90 is the largest peak (`2e+05` substance), and 15 of 16 observables settled within 1% over the final 10% of the run.

## Lab Signals

Inputs:

- `cytosolic_calcium` (`substance`, default `117.2`): cytosolic calcium amount, represented by the SBML boundary species `Ca_c`.
- `integration_step` (`s`, default `1.0`): Tellurium output sampling step.

Outputs:

- `active_eNOS` (`substance`): active eNOS-CaM-Ca4 complex amount, averaged over the final headline window.
- `nitric_oxide` (`substance`): nitric oxide amount, averaged over the final headline window.
- `state` (`record`): latest values for the 16 tracked named species.
- `summary` (`record`): final, peak, minimum, and excursion diagnostics for each observable.

## Files

| Path | Purpose |
|---|---|
| `model.yaml` | Model metadata, inputs, outputs, units, and runtime wiring. |
| `src/koo2013_shear_stress_no_production.py` | Tellurium-backed SBML execution wrapper. |
| `data/BIOMD0000000467.xml` | Curated BioModels SBML source. |
| `tests/` | Smoke coverage for model construction, stepping, and outputs. |

## Notes

This is a downstream submodel. It does not simulate the calcium-influx pathway directly; feed `cytosolic_calcium` from `koo2013-calcium-influx`, set it manually for fixed-input experiments, or use `koo2013-integrated` for the full shear-stress-to-NO pathway.
