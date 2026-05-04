# Koo2013 Shear-Stress Induced Calcium Influx and eNOS Activation Lab

This lab runs the Koo et al. (2013) endothelial mechanotransduction model for shear-stress induced calcium influx. It asks: when endothelial cells experience a shear-stress stimulus, how do IP3 production, calcium-store release, cytosolic calcium, and buffered calcium evolve over ten minutes?

The model wraps the BioModels EBI SBML asset [BIOMD0000000464](https://www.ebi.ac.uk/biomodels/BIOMD0000000464). This submodel is the calcium-influx/eNOS-activation entry point in the Koo2013 series. Its `models/core` package stays focused on SBML execution and stable numeric outputs, while `models/visualisation` owns internal grouped charts and narrative logic.

## What You'll See

The lab opens as a canvas with one Koo2013 calcium-influx node and a run-results panel. A default run lasts 600 s and produces grouped time-series panels for mechanical inputs/timers and calcium-subsystem species, plus a largest-excursions diagnostic and a What Happened table.

The first screenshot shows the canvas, the mechanical-input/timer panel, and the calcium-subsystem panel. The second scrolls down to the largest-excursions diagnostic and the What Happened table.

![Koo2013 calcium influx mechanical input and calcium subsystem results](assets/koo2013-calcium-inputs-calcium-results.png)

![Koo2013 calcium influx largest-excursions panel and What Happened table](assets/koo2013-calcium-summary-diagnostics.png)

## How to Read the Visualizations

The mechanical-input panel shows the model's internal step timer and the shear-stress input species. In this curated wrapper, the biologically useful stimulus knob is `stimulus_intensity`, which maps to the IP3-producing rate constant `k1`; the SBML shear-stress species itself is decorative and not kinetically wired.

The calcium-subsystem panel tracks extracellular calcium, stored calcium in the ER lumen, cytosolic calcium, buffered calcium, and IP3. In the shown run, stored calcium is the dominant changing pool, while IP3 and cytosolic calcium remain much smaller on the same scale.

The What Happened table summarizes the run without reading every trace. In the screenshot, it reports 7 tracked species observables, a 600 s run, stored calcium in the ER lumen as both the largest signed change and largest peak, and 3 of 7 observables settling within 1% over the final 10% of the run.

## What This Lab Contains

- `lab.yaml` describes the lab, runtime, inputs, outputs, and default model parameters.
- `wiring-layout.json` places the model on the canvas.
- `models/core/model.yaml` describes the SBML execution package, upstream source, parameters, and ports.
- `models/core/src/koo2013_shear_stress_calcium_influx.py` wraps the SBML model and publishes stable numeric outputs.
- `models/core/data/BIOMD0000000464.xml` is the curated SBML model file from BioModels EBI.
- `models/visualisation/` contains the internal presentation model for charts and narrative logic.
- `models/*/tests/` contains smoke tests for core execution and visualisation behavior.

## Inputs

- `stimulus_intensity` (`1/s`): IP3 production rate constant `k1`, used as the shear-stress-driven mechanotransduction knob.
- `integration_step` (`s`): output sampling step for the Tellurium simulator.

## Outputs

- `cytosolic_calcium`: cytosolic Ca2+ amount averaged over the model's headline window.
- `ip3`: IP3 amount averaged over the model's headline window.
- `state`: latest values of the observed species.
- `summary`: final, peak, minimum, and largest-change diagnostics for the run.

## Recreate and Run with the Biosim CLI

From this lab folder:

```bash
cd /path/to/models-biomechanics/labs/koo2013-calcium-influx
mkdir -p dist
python -m biosim pack build . --out dist/koo2013-calcium-influx.bsilab
python -m biosim pack run dist/koo2013-calcium-influx.bsilab
```

If you are working from this monorepo without installing `biosim`, use the local package environment instead:

```bash
mkdir -p dist
/path/to/bsim-active/biosim/.venv/bin/python -m biosim pack build . --out dist/koo2013-calcium-influx.bsilab
/path/to/bsim-active/biosim/.venv/bin/python -m biosim pack run dist/koo2013-calcium-influx.bsilab
```

## Run in the Desktop App

1. Open Biosimulant Desktop.
2. Go to Projects or Labs.
3. Choose the option to open or import an existing lab.
4. Select this folder's `lab.yaml`.
5. Open the lab and press Run.

The right side of the app should show the mechanical-input, calcium-subsystem, and summary diagnostic panels.

## How to Edit It

For scenario changes, start with `lab.yaml` and `models/core/model.yaml`.

- Change `runtime.duration` in `lab.yaml` for a longer or shorter simulation.
- Change `runtime.communication_step` if you want more or fewer reported points.
- Change `stimulus_intensity` to mimic weaker or stronger shear-stress-driven IP3 production.
- Change `integration_step` in `models/core/model.yaml` for finer or coarser Tellurium output sampling.

For downstream nitric-oxide production, wire this lab into `koo2013-no-production` or use the composed `koo2013-shear-to-no` lab.
