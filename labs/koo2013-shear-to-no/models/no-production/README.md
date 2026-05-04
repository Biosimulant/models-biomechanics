        # Koo2013 Shear-Stress Induced NO Production Lab

        Once endothelial cells sense flow and elevate intracellular calcium, eNOS becomes phosphorylated and produces nitric oxide (NO), the principal vasodilator released by the endothelium. Koo et al. (2013) extended their calcium-influx model with the NO-producing arm to capture the full mechano-chemical conversion from shear stress to a NO output signal.

This lab wraps Model 4 of the Koo2013 series. With the bundled defaults the simulator runs for ten minutes, long enough to capture the rise of activated eNOS and the build-up of NO.

        ## What You'll See

        The canvas shows a single Koo2013 NO node feeding a Results panel. A default run produces three visuals: time series for every model species, a final-state bar of the dominant species, and a What Happened table.

        Screenshots will land in `assets/` once the first published run produces them.

        ## How to Read the Visualizations

        The trajectory plot shows every species variable as a line over time. The x-axis is in s; each line is one of the 20 variables tracked by the SBML model. Use it to see when the system reacts to a perturbation, when transients settle, and how the variables move relative to each other.

        The dominant-observable bar chart reorders the same data by the absolute value at the end of the run. The longest bars are the variables that carry the most signal in the final state, which is the right place to start when you want to know what the model is "saying" once the dynamics settle.

        The What Happened table is a plain-language summary of the run. It names the variable that changed the most, the variable that hit the largest peak, and a one-line steady-state assessment based on the last 10% of the trajectory. This is the fastest way to read a run without scrolling through every line.

        ## What This Lab Contains

        | Path | Purpose |
        |---|---|
        | `lab.yaml` | Lab controls, IO, and runtime defaults. |
        | `wiring-layout.json` | Single-node canvas layout. |
        | `model.yaml` | Model package, parameters, units, and IO. |
        | `src/koo2013_shear_stress_no_production.py` | Tellurium-backed SBML execution wrapper. |
        | `data/BIOMD0000000467.xml` | Curated SBML model file from BioModels EBI BIOMD0000000467. |
        | `tests/` | Smoke tests for instantiation, advance, and outputs. |

        ## Inputs

        | Input | Unit | Meaning |
        |---|---|---|
        | `integration_step` | s | Output sampling step for the tellurium simulator. |

        ## Outputs

        | Output | Meaning |
        |---|---|
        | `state` | Latest value of every tracked observable (species variables). |
        | `summary` | Final, peak, and minimum value per observable plus simulated duration. |

        ## Running with the Bundled Defaults

        ```bash
        python3 examples/run_example.py koo2013_shear_stress_no_production
        ```

        The example configuration lives at `examples/koo2013_shear_stress_no_production/config.yaml`.

        ## Running in Biosimulant Desktop

        ```bash
        biosimulant labs import /Volumes/dem-ssd/imp/projects/Nitoons/Biosimulant/models/models-biomechanics/labs/koo2013-no-production
        ```

        ## Notes

        Faithful re-export of BioModels EBI BIOMD0000000467. Tellurium amd64 sandbox is required.
## Inputs and Outputs (lab signals)

**Inputs** (settable on the canvas):

- **`cytosolic_calcium`** (substance, default 117.2): Cytosolic Ca²⁺ concentration (s3, declared with boundaryCondition=true in the SBML — explicitly an external input). Compose this lab with `koo2013-calcium-influx` to feed real calcium dynamics; or set a fixed value for steady-state experiments.
- **`integration_step`** (s, default 1.0): Tellurium output sampling step.

**Outputs** (visible in run results / wireable to other labs):

- **`nitric_oxide`** (substance): NO amount, averaged over the last 60 seconds.
- **`active_eNOS`** (substance): Active eNOS-CaM-Ca₄ complex amount, averaged over the last 60 seconds.
- **`state`** (record): Latest values of all 16 named species.
- **`summary`** (record): Run-level statistics.

Headline scalar outputs are computed as time-windowed means over the wrapper's `_HEADLINE_WINDOW_S` period to give a stable, phase-independent reading.

## Known model limitations

- **Downstream submodel only.** This lab covers eNOS activation and NO production downstream of cytosolic calcium. It does not include the calcium-influx pathway — for that, use `koo2013-calcium-influx` or compose the two.
- **Calcium is a boundary species** — the SBML treats Ca_c as fixed/external. Set it once via the input; the wrapper writes to the runner each integration window so the value persists.

## Composing with the koo2013-calcium-influx lab

This lab can be wired into the [`koo2013-shear-to-no`](../koo2013-shear-to-no/README.md) composed lab to recreate the full mechanotransduction chain (`stimulus → cytosolic_calcium → nitric_oxide`). See that lab's README for the wiring shape and packaging constraints.
