        # Koo2013 Shear-Stress Induced Calcium Influx and eNOS Activation Lab

        Endothelial cells lining blood vessels sense the mechanical shear stress of flowing blood and convert it into intracellular calcium and signalling activity. Koo and colleagues (2013) built a quantitative model of this mechanotransduction pathway, focusing on how a step in shear stress opens calcium channels at the membrane and activates endothelial nitric oxide synthase (eNOS) through calcium and phosphorylation.

This lab wraps Model 1 of the Koo2013 series, the simplest formulation that links shear stress to calcium influx and eNOS activation. With the bundled defaults the simulator runs for ten minutes of physiological time, long enough to see the calcium transient and the rise of activated eNOS.

        ## What You'll See

        The canvas shows a single Koo2013 calcium node feeding a Results panel. A default run produces three visuals: time series for every model species, a final-state bar of the dominant species, and a What Happened table.

        Screenshots will land in `assets/` once the first published run produces them.

        ## How to Read the Visualizations

        The trajectory plot shows every species variable as a line over time. The x-axis is in s; each line is one of the 14 variables tracked by the SBML model. Use it to see when the system reacts to a perturbation, when transients settle, and how the variables move relative to each other.

        The dominant-observable bar chart reorders the same data by the absolute value at the end of the run. The longest bars are the variables that carry the most signal in the final state, which is the right place to start when you want to know what the model is "saying" once the dynamics settle.

        The What Happened table is a plain-language summary of the run. It names the variable that changed the most, the variable that hit the largest peak, and a one-line steady-state assessment based on the last 10% of the trajectory. This is the fastest way to read a run without scrolling through every line.

        ## What This Lab Contains

        | Path | Purpose |
        |---|---|
        | `lab.yaml` | Lab controls, IO, and runtime defaults. |
        | `wiring-layout.json` | Single-node canvas layout. |
        | `model/model.yaml` | Model package, parameters, units, IO. |
        | `model/src/koo2013_shear_stress_calcium_influx.py` | Tellurium-backed SBML wrapper and visuals. |
        | `model/data/BIOMD0000000464.xml` | Curated SBML model file from BioModels EBI BIOMD0000000464. |
        | `model/tests/` | Smoke tests for instantiation, advance, and visuals. |

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
        python3 examples/run_example.py koo2013_shear_stress_calcium_influx
        ```

        The example configuration lives at `examples/koo2013_shear_stress_calcium_influx/config.yaml`.

        ## Running in Biosimulant Desktop

        ```bash
        biosimulant labs import /Volumes/dem-ssd/imp/projects/Nitoons/Biosimulant/models/models-biomechanics/labs/koo2013-calcium-influx
        ```

        ## Notes

        Faithful re-export of BioModels EBI BIOMD0000000464. Tellurium amd64 sandbox is required.
## Inputs and Outputs (lab signals)

**Inputs** (settable on the canvas):

- **`stimulus_intensity`** (1/s, default 0.0006): IP3 production rate constant (k1 in re5). The published BioModels SBML for this submodel does NOT kinetically wire the 'Shear Stress' species — k1 is the parameter the modeller used as a surrogate for shear-stress-driven mechanotransduction. Setting k1=0 produces a quiescent cell; values above 0.0006 mimic stronger shear stress.
- **`integration_step`** (s, default 1.0): Tellurium output sampling step.

**Outputs** (visible in run results / wireable to other labs):

- **`cytosolic_calcium`** (substance): Cytosolic Ca²⁺ amount, averaged over the last 60 seconds.
- **`ip3`** (substance): IP₃ amount, averaged over the last 60 seconds.
- **`state`** (record): Latest values of all 7 named species (mass-balance placeholders filtered out).
- **`summary`** (record): Run-level statistics.

Headline scalar outputs are computed as time-windowed means over the wrapper's `_HEADLINE_WINDOW_S` period to give a stable, phase-independent reading.

## Known model limitations

- **`Shear Stress` species is decorative.** The BioModels SBML (BIOMD0000000464) declares `s119` named 'Shear Stress' but never references it in any kinetic law or rule. The shear-stress effect is encoded indirectly through the `k1` rate constant. Use `stimulus_intensity` (→k1), not the species, as the experimental knob.
- **Empty-set placeholders filtered.** Species marked with SBO:0000291 (s5, s7-s11, s13) are mass-balance bookkeeping artifacts with no biological meaning; the wrapper drops them from outputs.
- **Compose with `koo2013-no-production`** to drive realistic NO production from the calcium output (or use the integrated lab for the same chain in a single SBML).

## Composing with the koo2013-no-production lab

This lab can be wired into the [`koo2013-shear-to-no`](../koo2013-shear-to-no/README.md) composed lab to recreate the full mechanotransduction chain (`stimulus → cytosolic_calcium → nitric_oxide`). See that lab's README for the wiring shape and packaging constraints.
