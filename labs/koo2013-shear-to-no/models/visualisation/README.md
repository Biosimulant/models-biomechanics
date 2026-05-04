# Koo2013 Shear-to-NO Visualisation

This embedded model owns the pathway-level charts and narrative logic for the composed Koo2013 shear-to-NO lab.

It consumes structured outputs from both sibling SBML wrappers:

- `calcium_influx`: upstream calcium, IP3, state, and summary signals from `BIOMD0000000464`.
- `no_production`: downstream active eNOS, nitric oxide, state, and summary signals from `BIOMD0000000467`.

The parent lab README embeds the captured Biosimulant screenshots. Those images show the expected three-node composition (`calcium_influx`, `no_production`, and `visualisation`) and the visualisation model's 10 panels, including mechanical inputs, calcium subsystem dynamics, PI3K/AKT signalling, eNOS activation, nitric oxide accumulation, largest-excursion diagnostics, and the What Happened table.
