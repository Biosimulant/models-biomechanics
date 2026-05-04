# models-biomechanics

> Storage-only repo: each former root model now lives in `labs/<slug>/model/` and is wrapped by
> `labs/<slug>/lab.yaml`. This repo has no repo-level import catalog and no composed labs at the root.

Curated collection of **biomechanics** simulation models for the **biosim** platform. This repository contains computational models of mechanical and physical processes in biological systems, including muscle mechanics, fluid dynamics, stress responses, and biomechanical interactions.

## What's Inside

### Models (19 packages)

Each model is a self-contained simulation component with a `model.yaml` manifest.

**Biomechanics** — mechanical forces, stress responses, and physical processes in biological systems:

| Sublab | Description |
|-------|-------------|
| `biomechanics-sbml-aubry1995-multi-compartment-model-of-fluid-phase` | Multi-compartment fluid-phase endocytosis kinetics in Dictyostelium |
| `biomechanics-sbml-aubry1995-nine-compartment-model-of-fluid-phase` | Nine-compartment fluid-phase endocytosis kinetics model |
| `biomechanics-sbml-carpenter-2024-mechanical-control-of-growing` | Computational framework for predicting cell proliferation patterns |
| `biomechanics-sbml-erguler2013-unfolded-protein-stress-response` | Unfolded protein stress response dynamics |
| `heldt2002-circulation-pbpk` | Cardiovascular response to orthostatic stress (circulation PBPK) |
| `heldt2002-heart` | Cardiovascular response to orthostatic stress (heart model) |
| `heldt2002-lpc` | Cardiovascular response to orthostatic stress (LPC model) |
| `biomechanics-sbml-hunziker2010-p53-stressspecificresponse` | Stress-specific response of the p53-Mdm2 system |
| `biomechanics-sbml-irp1443reg-ralstonia-solanacearum-virulence` | Virulence regulatory network of R. solanacearum |
| `koo2013-integrated` | Integrated shear stress-induced NO production in endothelial cells |
| `koo2013-calcium-influx` | Shear stress-induced calcium influx dynamics |
| `koo2013-no-production` | Shear stress-induced nitric oxide production model |
| `biomechanics-sbml-ralser2007-carbohydrate-rerouting-ros` | Dynamic rerouting of carbohydrate flux and ROS response |
| `biomechanics-sbml-rong2020-grover-qm8-electronic-prediction` | GROVER embedding QM8 electronic property prediction |
| `biomechanics-sbml-russomanno2023-systems-approach-rat` | Simcyp PBPK models for rat species |
| `biomechanics-sbml-russomanno2023-systems-approach-mouse` | Simcyp PBPK models for mouse species |
| `shorten2007-muscle-fatigue` | Skeletal muscle fatigue (currently parked under `labs-orphan/` — see that folder's README; the upstream SBML has no settable stimulation parameter) |
| `biomechanics-sbml-sivery2016-mammalian-heat-shock-response` | Mammalian heat shock response under environmental stress |
| `biomechanics-sbml-soleimani2019-incudostapedial-mechanics` | Finite-element model of incudostapedial mechanics |

## Layout

```
models-biomechanics/
├── models/<model-slug>/     # One model package per folder, each with model.yaml
├── libs/                    # Shared helper code for curated models
├── templates/model-pack/    # Starter template for new model packs
├── scripts/                 # Manifest and entrypoint validation scripts
├── docs/                    # Governance documentation
└── .github/workflows/       # CI/CD pipeline
```

## How It Works

### Model Interface

Every model implements the `biosim.BioModule` interface:

- **`inputs()`** — declares named input signals the module consumes
- **`outputs()`** — declares named output signals the module produces
- **`advance_window(t)`** — advances the model's internal state to time `t`

Most curated models include Python source under `src/` and are wired together via `lab.yaml` in composed simulations without additional code.

### Model Standards

All models in this repository:
- Use SBML (Systems Biology Markup Language) format
- Are sourced from BioModels database and other curated repositories
- Include tellurium runtime for SBML execution
- Provide `state` output for monitoring simulation results
- Support configurable timesteps via `communication_step` parameter

### Running Models

Models are loaded and executed by the `biosim-platform`. The platform reads `model.yaml`, instantiates the model from its entrypoint, and runs the simulation loop at the configured timestep for the specified duration.

Individual models can be integrated into larger composed simulations (spaces) by wiring their outputs to other models' inputs.

## Getting Started

### Prerequisites

- Python 3.11+
- `biosim` framework

### Install biosim

```bash
pip install "biosim @ git+https://github.com/BioSimulant/biosim.git@main"
```

### Create a New Model

1. Copy `templates/model-pack/` to `models/<your-model-slug>/`
2. Edit `model.yaml` with metadata, entrypoint, and pinned dependencies
3. Implement your module (subclass `biosim.BioModule` or use a built-in pack)
4. Add biomechanics-specific tags and categorization
5. Validate: `python scripts/validate_manifests.py && python scripts/check_entrypoints.py`

### Using Models in Spaces

To integrate biomechanics models into larger simulations:

1. Reference models by `manifest_path` (e.g., `labs-orphan/shorten2007-muscle-fatigue/model/model.yaml`)
2. Wire model outputs to inputs of other models in your space configuration
3. Configure runtime parameters and simulation duration

## Linking in biosim-platform

- Root manifests can be linked with explicit paths:
  - `labs-orphan/shorten2007-muscle-fatigue/model/model.yaml`
- Models can be composed with other domain models (neuroscience, metabolism, etc.) in multi-scale simulations

## External Repos

External authors can keep models in independent repositories and link them directly in `biosim-platform`. This repository is curated, not exclusive.

## Validation & CI

Three scripts enforce repository integrity on every push:

| Script | Purpose |
|--------|---------|
| `scripts/validate_manifests.py` | Schema validation for all model.yaml files |
| `scripts/check_entrypoints.py` | Verifies Python entrypoints are importable and callable |
| `scripts/check_public_boundary.sh` | Prevents business-sensitive content in this public repo |

The CI pipeline (`.github/workflows/ci.yml`) runs: **secret scan** → **manifest validation** → **smoke sandbox** (Docker).

## Contributing

- All dependencies must use exact version pinning (`==`)
- Model slugs use kebab-case with domain prefix (`biomechanics-sbml-`)
- Models must follow the `biosim.BioModule` interface
- SBML models use tellurium runtime for execution
- Pre-commit hooks enforce trailing whitespace, EOF newlines, YAML syntax, and secret detection
- See [docs/PUBLIC_INTERNAL_BOUNDARY.md](docs/PUBLIC_INTERNAL_BOUNDARY.md) for content policy

## Domain-Specific Notes

**Biomechanics Focus Areas:**
- Muscle mechanics and fatigue
- Cardiovascular biomechanics and hemodynamics
- Cellular stress responses (heat shock, oxidative stress, protein folding)
- Fluid dynamics and transport processes
- Mechanical force transduction and signaling
- Physiologically-based pharmacokinetic (PBPK) modeling

## License

This repository is dual-licensed:

- **Code** (scripts, templates, Python modules): Apache-2.0 (`LICENSE-CODE.txt`)
- **Model/content** (manifests, docs, wiring/config): CC BY 4.0 (`LICENSE-CONTENT.txt`)

Attribution guidance: `ATTRIBUTION.md`
