# Heldt2002 Orthostatic Stress - Lumped Parameter Circulation Model

This model package wraps BioModels EBI `MODEL1006230113`, the Heldt2002 lumped-parameter circulation submodel. It tracks rate-rule observables, exposes headline cardiac output and mean arterial pressure outputs, and groups the raw traces into physiology-facing visual panels.

With the bundled lab defaults, the simulator runs for 60 s and reports chamber volumes, aortic and pulmonary volumes, flow waveforms, pressure waveforms, summary diagnostics, and an LV pressure-volume loop.

## What You'll See

![Heldt2002 lumped circulation chamber and trunk volume result panels](../assets/heldt2002-lpc-chamber-trunk-results.png)

![Heldt2002 lumped circulation flow and pressure result panels](../assets/heldt2002-lpc-flow-pressure-results.png)

![Heldt2002 lumped circulation summary diagnostics and LV pressure-volume loop](../assets/heldt2002-lpc-summary-pv-loop.png)

## How to Read the Visualizations

The grouped time-series panels split the 30 SBML rate-rule observables into views for cardiac chambers, aortic and pulmonary trunk volumes, pulmonary/systemic/coronary perfusion, blood-flow signals, and pressure waveforms.

The What Happened table summarizes the same run. In the shown screenshot, it reports systemic vein volume as the largest signed change and largest peak, with no observable settling within 1% over the final 10% of the run.

The LV pressure-volume loop shows the last cardiac cycle as pressure against volume. Loop area encodes stroke work, x-extent encodes preload, and the upper pressure plateau encodes afterload.

## What This Model Contains

| Path | Purpose |
|---|---|
| `model.yaml` | Model package, parameters, units, IO, and upstream metadata. |
| `src/heldt2002_orthostaticstress_lpc.py` | Tellurium-backed SBML wrapper and visualization builder. |
| `data/MODEL1006230113.xml` | Curated SBML model file from BioModels EBI. |
| `tests/` | Smoke tests for instantiation, simulation advance, visuals, and lab IO. |

## Inputs

| Input | Unit | Meaning |
|---|---|---|
| `heart_rate` | 1/min | Cardiac pacing rate. |
| `peak_lv_elastance` | mmHg/mL | Peak left-ventricle elastance; higher values model stronger contractility. |
| `integration_step` | s | Output sampling step for the Tellurium simulator. |

## Outputs

| Output | Meaning |
|---|---|
| `cardiac_output` | Cycle-averaged cardiac output. |
| `mean_arterial_pressure` | Cycle-averaged mean arterial pressure. |
| `state` | Latest values of tracked rate-rule observables. |
| `summary` | Final, peak, minimum, and largest-change diagnostics. |

## Notes

This is the lumped circulation lab. Use the circulation-PBPK lab when you need PBPK/tracer compartment redistribution rather than hemodynamic chamber, flow, pressure, and PV-loop diagnostics.
