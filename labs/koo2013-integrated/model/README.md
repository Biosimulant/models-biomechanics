# Koo2013 Integrated Shear-Stress Induced NO Production Model

This model is the integrated Koo et al. (2013) endothelial mechanotransduction system from BioModels source `BIOMD0000000468`. It combines the calcium-influx and NO-production modules into one SBML wrapper named `koo2013_integrated_shear_stress_no_production`.

The screenshots embedded in the parent lab README were checked against the visible lab title and run alias: they show `Koo2013 Integrated Shear-Stress Induced NO Production` / `Koo2013_integrated_shear_stress_no_production`, which matches this model package.

## What the Run Shows

A default Biosimulant run lasts 600 s and renders 10 result panels. The first panels show the mechanical-input/timer traces and the calcium subsystem, including extracellular, stored, cytosolic, buffered, IP3, and calmodulin-linked pools. Later panels expose the FAK/Src/Shc/Ras mechanosensor cascade, the PI3K/AKT signalling axis, nitric oxide accumulation, and the PP2A/PTEN regulatory phosphatases.

The summary diagnostics in the screenshot report 65 species observables. Stored calcium in the ER lumen is the largest-changing observable (`-2.41e+06`), its largest peak is `2.83e+06` substance, and 26 of 65 observables settled within 1% over the final 10% of the run.

## Lab Signals

Inputs:

- `stimulus_intensity` (`1/s`, default `0.0012`): IP3-production rate constant `k1`. This is the practical shear-stress stimulus surrogate for perturbation experiments.
- `integration_step` (`s`, default `1.0`): Tellurium output sampling step.

Outputs:

- `active_eNOS` (`substance`): active eNOS-CaM-Ca4 complex amount, averaged over the final headline window.
- `cytosolic_calcium` (`substance`): cytosolic calcium amount, averaged over the final headline window.
- `nitric_oxide` (`substance`): nitric oxide amount, averaged over the final headline window.
- `state` (`record`): latest values for the 65 tracked named species after filtering mass-balance placeholders.
- `summary` (`record`): final, peak, minimum, and excursion diagnostics for each observable.

## Files

| Path | Purpose |
|---|---|
| `model.yaml` | Model metadata, inputs, outputs, units, and runtime wiring. |
| `src/koo2013_integrated_shear_stress_no_production.py` | Tellurium-backed SBML wrapper and visual definitions. |
| `data/BIOMD0000000468.xml` | Curated BioModels SBML source. |
| `tests/` | Smoke coverage for model construction, stepping, and outputs. |

## Notes

The upstream SBML `Shear Stress` species is decorative in this wrapper; `stimulus_intensity` is the parameter that actually changes the IP3-production stimulus. This is the largest Koo2013 lab in this set: the source SBML has 79 species and 74 reactions, while the user-facing `state` filters down to 65 named species.
