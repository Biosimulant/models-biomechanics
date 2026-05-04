# Heldt2002 Orthostatic Stress - Heart Model

This core model package wraps BioModels EBI `MODEL1006230103`, the Heldt2002 isolated heart submodel. It exposes the time-varying left-ventricular elastance waveform and cardiac timing helpers used by the larger circulation models.

User-facing charts, summaries, and phase portraits live in the sibling [`../visualisation`](../visualisation/README.md) model package.

## What You'll See

![Heldt2002 heart elastance timing plot and summary table](../assets/heldt2002-heart-elastance-summary.png)

![Heldt2002 heart What Happened table and LV elastance phase portrait](../assets/heldt2002-heart-phase-portrait.png)

## How to Read the Visualizations

The elastance/timing plot shows heart-rate frequency, beat phase time, systolic duration, and left-ventricular elastance. The elastance waveform rises rapidly during systole, peaks near the configured systolic elastance, then relaxes toward the diastolic baseline.

The What Happened table summarizes the same run. In the shown screenshot, it reports 4 tracked observables, a 5 s duration, left-ventricular elastance as the largest-changing observable, and a peak elastance of 5.6 mmHg/mL.

The LV elastance phase portrait plots elastance against cardiac phase. This is a phase view of the contraction driver, not a pressure-volume loop; the heart-only SBML does not include LV pressure or volume states.

## What This Model Contains

| Path | Purpose |
|---|---|
| `model.yaml` | Model package, parameters, units, IO, and upstream metadata. |
| `src/heldt2002_orthostaticstress_heart.py` | Tellurium-backed SBML execution wrapper. |
| `data/MODEL1006230103.xml` | Curated SBML model file from BioModels EBI. |
| `tests/` | Smoke tests for instantiation, simulation advance, and published outputs. |

## Inputs

| Input | Unit | Meaning |
|---|---|---|
| `heart_rate` | 1/min | Cardiac pacing rate. |
| `systolic_elastance` | mmHg/mL | Peak systolic LV elastance; higher values model stronger contractility. |
| `diastolic_elastance` | mmHg/mL | Diastolic LV elastance; lower values model better filling compliance. |
| `integration_step` | s | Output sampling step for the Tellurium simulator. |

## Outputs

| Output | Meaning |
|---|---|
| `elastance` | Cycle-averaged left-ventricular elastance. |
| `state` | Latest values of the observed timing and elastance variables. |
| `summary` | Final, peak, minimum, and largest-change diagnostics. |

## Notes

This is a minimal isolated heart submodel. It is useful for inspecting the elastance driver before composing with circulation models, but it does not include chamber pressures, flows, or volumes. Use `heldt2002-lpc` for a full LV pressure-volume loop.
