# Koo2013 Shear-to-NO Composed Pathway

This lab is a **composed lab** — it does not bundle its own model code. Instead it wires together two existing single-model labs in this repository to recreate the full Koo et al. (2013) endothelial mechanotransduction chain:

```
stimulus_intensity --> [koo2013-calcium-influx] --cytosolic_calcium--> [koo2013-no-production] --nitric_oxide-->
```

This is the canonical composition use case the boundary-condition design enables: the no-production submodel declares `s3 (Ca_c)` with `boundaryCondition="true"` precisely so an external upstream submodel can drive it.

## What you'll see

A canvas with two nodes — calcium influx (left), NO production (right) — connected by a single wire from the upstream calcium output to the downstream calcium input. Setting `stimulus_intensity` (the IP3 production rate constant in the upstream submodel) drives the entire chain through to NO production.

## Inputs

- **`stimulus_intensity`** (1/s, default 0.0006): IP3 production rate constant. The published Koo2013 SBML for the calcium-influx submodel does not kinetically wire its `Shear Stress` species, so this rate constant is the modeller's de-facto stimulus surrogate. Setting it to 0 quiesces the cell; setting it above the baseline mimics stronger shear stress.
- **`integration_step`** (s, default 1.0): tellurium output sampling step.

## Outputs

- **`cytosolic_calcium`** (substance): cytosolic Ca²⁺ amount from the upstream calcium-influx submodel (windowed mean).
- **`ip3`** (substance): IP₃ amount from the upstream submodel.
- **`nitric_oxide`** (substance): NO amount from the downstream NO-production submodel (windowed mean) — the headline output of the full chain.
- **`active_eNOS`** (substance): active eNOS-CaM-Ca₄ complex from the downstream submodel.
- **`calcium_influx_state`** (record): full state of the upstream submodel (7 named species).
- **`no_production_state`** (record): full state of the downstream submodel (16 named species).

## Why this lab exists

The Koo2013 series ships three SBML files at BioModels: calcium-influx (Model 1), NO-production (Model 4), and integrated (Model 7). The integrated lab is a single SBML that encodes the full pathway in one file. This composed lab is an **alternative** that builds the same pathway from the two submodels by wiring at the BioSignal level. It demonstrates:

1. The composition pattern — two labs, one wire.
2. That the boundary-condition design on `koo2013-no-production` works as advertised: external upstream calcium dynamics drive downstream NO production.
3. A debugging path — if the integrated lab produces unexpected behavior, comparing this composed version isolates which submodel's kinetics is responsible.

## Trade-offs versus the integrated lab

| | Composed (this lab) | Integrated (`koo2013-integrated`) |
|---|---|---|
| Model count | 2 | 1 |
| Source SBMLs | 2 (loaded independently) | 1 |
| Coupling | Explicit BioSignal wire | Built into one SBML's reaction network |
| Debuggability | High — can inspect each submodel's state separately | Lower — full state is one record |
| Faithfulness to published model | Captures the mechanistic chain but with the cytosolic-calcium boundary; the published integrated SBML may have subtle kinetic differences | Most faithful to the published `BIOMD0000000468` integrated formulation |

## Layout

The lab is self-contained. The two submodel directories are bundled inside `model/`:

```
koo2013-shear-to-no/
├── lab.yaml                         # composition + wiring
├── wiring-layout.json               # canvas placement
├── README.md                        # this file
└── model/
    ├── calcium_influx/              # full copy of koo2013-calcium-influx/model
    │   ├── model.yaml
    │   ├── data/BIOMD0000000464.xml
    │   ├── src/...
    │   └── tests/...
    └── no_production/               # full copy of koo2013-no-production/model
        ├── model.yaml
        ├── data/BIOMD0000000467.xml
        ├── src/...
        └── tests/...
```

The `model/calcium_influx` and `model/no_production` directories are full byte-for-byte copies of the matching single-model labs at the time this composed lab was created. They are intentionally self-contained so the lab packs cleanly via `biosim.pack` (which rejects `..` traversal in embedded paths). If you change one of the source labs, you'll need to refresh the corresponding subdirectory here.

## Notes

- Both subs use tellurium and need the amd64 sandbox image (libroadrunner has no arm64 wheel).
- The wiring is unidirectional. Calcium drives NO production, but NO does not feed back to calcium in this composition. The published Koo2013 paper does include feedback in its full formulation; this composed lab captures the dominant forward path only.
