# Heldt2002 Orthostatic Stress - Circulation PBPK Model

This model package wraps BioModels EBI `MODEL1006230084`, the Heldt2002 circulation PBPK submodel. It tracks 44 rate-rule observables and groups the raw traces into physiology-facing panels for chamber volumes, vessels, tissue beds, venous return, flow, and tracer-like compartment redistribution.

## What You'll See

![Heldt2002 circulation PBPK cardiac chamber and central vessel result panels](../assets/heldt2002-circpbpk-chamber-central-results.png)

![Heldt2002 circulation PBPK substrate redistribution and largest-excursions panel](../assets/heldt2002-circpbpk-substrate-excursions.png)

![Heldt2002 circulation PBPK What Happened table and LV pressure-volume loop](../assets/heldt2002-circpbpk-summary-pv-loop.png)

## How to Read the Visualizations

The grouped time-series panels split the SBML rate-rule variables into physiology-facing views for cardiac chambers, central vessels, systemic arteries, peripheral tissue beds, venous return, aortic flow, substrate/tracer redistribution, and other observables.

The What Happened table summarizes the same run by reporting the number of tracked observables, simulated duration, largest signed change, largest peak, and a steady-state assessment over the final 10% of the run.

The LV pressure-volume loop is included as a final-cycle diagnostic for the exported LV pressure and volume variables. The default PBPK loop is nearly collapsed; use `heldt2002-lpc` for a more complete pressure-volume loop.

## What This Model Contains

| Path | Purpose |
|---|---|
| `model.yaml` | Model package, parameters, units, IO, and upstream metadata. |
| `src/heldt2002_orthostaticstress_circpbpk.py` | Tellurium-backed SBML wrapper and visualization builder. |
| `data/MODEL1006230084.xml` | Curated SBML model file from BioModels EBI. |
| `tests/` | Smoke tests for instantiation, simulation advance, visuals, and lab IO. |

## Inputs

| Input | Unit | Meaning |
|---|---|---|
| `heart_rate` | 1/min | Cardiac pacing rate. |
| `peripheral_resistance_scale` | dimensionless | Multiplier for systemic peripheral resistances. |
| `compliance_scale` | dimensionless | Multiplier for unstressed compartment volumes, used as a compliance-like perturbation. |
| `integration_step` | s | Output sampling step for the Tellurium simulator. |

## Outputs

| Output | Meaning |
|---|---|
| `aortic_flow` | Cycle-averaged aortic flow. |
| `aortic_pressure` | Cycle-averaged aortic pressure. |
| `state` | Latest values of tracked rate-rule observables. |
| `summary` | Final, peak, minimum, and largest-change diagnostics. |

## Notes

This is the circulation-PBPK lab. Use the lumped-parameter circulation (`heldt2002-lpc`) lab for chamber, pressure, flow, and pressure-volume-loop diagnostics without PBPK compartment redistribution.
