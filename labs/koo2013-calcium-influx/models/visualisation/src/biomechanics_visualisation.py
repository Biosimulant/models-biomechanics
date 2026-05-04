# SPDX-FileCopyrightText: 2026-present Biosimulant Team
# SPDX-License-Identifier: Apache-2.0
"""Dedicated visualisation model for biomechanics labs."""

from __future__ import annotations

from copy import deepcopy
import importlib.util
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, TYPE_CHECKING
import xml.etree.ElementTree as ET

import yaml

from biosim import BioModule
from biosim.signals import AcceptedSignalProfile, BioSignal, SignalSpec

if TYPE_CHECKING:  # pragma: no cover
    from biosim.visuals import VisualSpec


_GROUP_META = {
    "cardiac_chambers": ("Cardiac chamber volumes", "How do atrial and ventricular volumes evolve?"),
    "central_vessels": ("Central vessel volumes", "How do the proximal vessel compartments fill and empty?"),
    "systemic_arteries": ("Systemic arterial volumes", "How do arterial compartments respond through the run?"),
    "peripheral_tissue": ("Peripheral tissue volumes", "Where does blood pool through the run?"),
    "veins": ("Venous return volumes", "How does the venous reservoir respond?"),
    "aortic_flow": ("Aortic flow", "How does aortic flow evolve across the run?"),
    "substrate_concentration": ("Substrate concentrations", "How is the PBPK tracer redistributed?"),
    "koo_input": ("Mechanical inputs and timers", "How does the shear-stress drive change over time?"),
    "koo_calcium": ("Calcium subsystem", "How do calcium pools, IP3, and calmodulin shift?"),
    "koo_mechano": ("Mechanosensor cascade", "How does the FAK/Src/Shc/Ras cascade respond?"),
    "koo_pi3k_akt": ("PI3K / AKT signalling", "How does PI3K signalling activate AKT?"),
    "koo_mapk": ("MAPK cascade", "How does the MAPK branch activate downstream responses?"),
    "koo_enos_chain": ("eNOS activation chain", "How does eNOS assemble into its active complexes?"),
    "koo_no": ("Nitric oxide production", "How quickly does nitric oxide accumulate?"),
    "koo_phosphatase": ("Regulatory phosphatases", "How do the deactivating phosphatases respond?"),
    "lpc_central_vessels": ("Aortic and pulmonary trunk volumes", "How do the proximal and distal trunks fill?"),
    "lpc_pulmonary_perfusion": ("Pulmonary perfusion", "How do pulmonary capillaries and veins fill?"),
    "lpc_systemic_perfusion": ("Systemic perfusion", "How does systemic perfusion redistribute?"),
    "lpc_coronary_perfusion": ("Coronary perfusion", "How does coronary microcirculation redistribute?"),
    "lpc_blood_flows": ("Aortic and pulmonary flows", "How do the major flow waveforms evolve?"),
    "lpc_blood_pressures": ("Pressure waveforms", "How do the main pressure waveforms evolve?"),
    "other": ("Other observables", "How do the remaining observed variables evolve?"),
}

_KOO2013_GROUP_LOOKUP = {
    "Shear Stress": "koo_input",
    "Time": "koo_input",
    "TimeT": "koo_input",
    "pre_time": "koo_input",
    "Ca_ex": "koo_calcium",
    "Ca_s": "koo_calcium",
    "Ca_c": "koo_calcium",
    "Ca_B": "koo_calcium",
    "IP3": "koo_calcium",
    "PIP2": "koo_calcium",
    "Calmodulin": "koo_calcium",
    "CaM-Ca2": "koo_calcium",
    "CaM-Ca4": "koo_calcium",
    "FAK": "koo_mechano",
    "p-FAK": "koo_mechano",
    "p-FAK:Shc": "koo_mechano",
    "p-FAK:p-Shc": "koo_mechano",
    "p-FAK:p-Shc:Grb2:Sos": "koo_mechano",
    "Shc": "koo_mechano",
    "p-Shc": "koo_mechano",
    "p-Shc:Grb2:Sos": "koo_mechano",
    "Grb2:Sos": "koo_mechano",
    "Ras:GDP": "koo_mechano",
    "Ras:GTP": "koo_mechano",
    "Src": "koo_mechano",
    "p-Src": "koo_mechano",
    "PI3K": "koo_pi3k_akt",
    "p-PI3K": "koo_pi3k_akt",
    "PI3P": "koo_pi3k_akt",
    "AKT": "koo_pi3k_akt",
    "AKT:PI3P": "koo_pi3k_akt",
    "p-AKT:PI3P": "koo_pi3k_akt",
    "pp-AKT:PI3P": "koo_pi3k_akt",
    "PDK1": "koo_pi3k_akt",
    "PDK1_cyto": "koo_pi3k_akt",
    "PDK2": "koo_pi3k_akt",
    "MEKK1": "koo_mapk",
    "p-MEKK1": "koo_mapk",
    "JNKK": "koo_mapk",
    "p-JNKK": "koo_mapk",
    "pp-JNKK": "koo_mapk",
    "JNK": "koo_mapk",
    "p-JNK": "koo_mapk",
    "pp-JNK": "koo_mapk",
    "AP-1": "koo_mapk",
    "aAP-1": "koo_mapk",
    "KLF2": "koo_mapk",
    "eNOS": "koo_enos_chain",
    "eNOS-CaM-Ca2": "koo_enos_chain",
    "eNOS-CaM-Ca4": "koo_enos_chain",
    "eNOS-Cav-1": "koo_enos_chain",
    "Hsp90": "koo_enos_chain",
    "Hsp90-eNOS": "koo_enos_chain",
    "Hsp90-eNOS-CaM-Ca2": "koo_enos_chain",
    "Hsp90-eNOS-CaM-Ca4": "koo_enos_chain",
    "Hsp90-p-eNOS": "koo_enos_chain",
    "Hsp90-p-eNOS-CaM-Ca2": "koo_enos_chain",
    "Hsp90-p-eNOS-CaM-Ca4": "koo_enos_chain",
    "NO": "koo_no",
    "L-Arg": "koo_no",
    "PP2A": "koo_phosphatase",
    "PTEN": "koo_phosphatase",
}

_KOO2013_LABELS = {
    "Ca_ex": "Extracellular calcium",
    "Ca_s": "Stored calcium",
    "Ca_c": "Cytosolic calcium",
    "Ca_B": "Buffered calcium",
    "Calmodulin": "Calmodulin",
    "CaM-Ca2": "Calmodulin Ca2 complex",
    "CaM-Ca4": "Calmodulin Ca4 complex",
    "PIP2": "PIP2",
    "IP3": "IP3",
    "PI3K": "PI3K",
    "p-PI3K": "Phosphorylated PI3K",
    "PI3P": "PI3P",
    "AKT": "AKT",
    "AKT:PI3P": "AKT PI3P complex",
    "p-AKT:PI3P": "Phosphorylated AKT PI3P complex",
    "pp-AKT:PI3P": "Active AKT PI3P complex",
    "PDK1": "PDK1",
    "PDK1_cyto": "Cytosolic PDK1",
    "PDK2": "PDK2",
    "eNOS": "eNOS",
    "NO": "Nitric oxide",
    "L-Arg": "L-arginine",
    "FAK": "FAK",
    "p-FAK": "Phosphorylated FAK",
    "Shc": "Shc",
    "p-Shc": "Phosphorylated Shc",
    "Src": "Src",
    "p-Src": "Phosphorylated Src",
    "Ras:GDP": "Inactive Ras",
    "Ras:GTP": "Active Ras",
    "MEKK1": "MEKK1",
    "p-MEKK1": "Phosphorylated MEKK1",
    "JNKK": "JNKK",
    "p-JNKK": "Phosphorylated JNKK",
    "pp-JNKK": "Active JNKK",
    "JNK": "JNK",
    "p-JNK": "Phosphorylated JNK",
    "pp-JNK": "Active JNK",
    "AP-1": "AP-1",
    "aAP-1": "Active AP-1",
    "KLF2": "KLF2",
    "PP2A": "PP2A",
    "PTEN": "PTEN",
    "Shear Stress": "Shear stress",
    "Time": "Simulation time",
    "TimeT": "Step timer",
    "pre_time": "Pre-step time",
}

_COMPARTMENT_NAMES = {
    "LA": "Left Atrium",
    "LV": "Left Ventricle",
    "RA": "Right Atrium",
    "RV": "Right Ventricle",
    "AO": "Aorta",
    "AR": "Systemic Arteries",
    "AD": "Abdominal Bed",
    "CO": "Coronary Trunk",
    "CR": "Coronary Arterioles",
    "CRtissue": "Coronary Microvasculature",
    "MU": "Muscle",
    "GI": "Gastrointestinal Bed",
    "LI": "Liver",
    "KI": "Kidney",
    "SK": "Skin",
    "OT": "Other Tissue",
    "VE": "Systemic Veins",
    "VC": "Vena Cava",
    "PA": "Pulmonary Artery",
    "Pa": "Pulmonary Arterioles",
    "PC": "Pulmonary Capillaries",
    "PV": "Pulmonary Veins",
}

_HELDT2002_LABELS = {
    "hrf": "Heart rate frequency",
    "beattime": "Beat phase time",
    "Ts": "Systolic duration",
    "E_LV": "Left ventricle elastance",
    "Faod": "Aortic flow distal",
    "Faop": "Aortic flow proximal",
    "Fpad": "Pulmonary artery flow distal",
    "Fpap": "Pulmonary artery flow proximal",
    "MAP": "Mean arterial pressure",
    "Paopc": "Aortic pressure",
    "Vla": "Left atrium volume",
    "Vlv": "Left ventricle volume",
    "Vra": "Right atrium volume",
    "Vrv": "Right ventricle volume",
    "Vaod": "Aorta volume distal",
    "Vaop": "Aorta volume proximal",
    "Vpa": "Pulmonary artery volume",
    "Vpad": "Pulmonary artery volume distal",
    "Vpap": "Pulmonary artery volume proximal",
    "Vpc": "Pulmonary capillary volume",
    "Vpv": "Pulmonary vein volume",
    "Vsa": "Systemic artery volume",
    "Vsap": "Systemic artery volume proximal",
    "Vsc": "Systemic capillary volume",
    "Vsv": "Systemic vein volume",
    "Vvc": "Vena cava volume",
    "Vcorao": "Coronary arterial volume",
    "Vcorea": "Coronary epicardial arteriolar volume",
    "Vcorcap": "Coronary capillary volume",
    "Vcorev": "Coronary epicardial venular volume",
    "Vcorla": "Coronary left atrial perfusion",
    "Vcorlv": "Coronary left ventricular perfusion",
    "Vcorsa": "Coronary subendocardial arteriolar volume",
    "Vcorsv": "Coronary subendocardial venular volume",
}

_LPC_GROUP_LOOKUP = {
    "Vla": "cardiac_chambers",
    "Vlv": "cardiac_chambers",
    "Vra": "cardiac_chambers",
    "Vrv": "cardiac_chambers",
    "Vaod": "lpc_central_vessels",
    "Vaop": "lpc_central_vessels",
    "Vpa": "lpc_central_vessels",
    "Vpad": "lpc_central_vessels",
    "Vpap": "lpc_central_vessels",
    "Vpc": "lpc_pulmonary_perfusion",
    "Vpv": "lpc_pulmonary_perfusion",
    "Vsa": "lpc_systemic_perfusion",
    "Vsap": "lpc_systemic_perfusion",
    "Vsc": "lpc_systemic_perfusion",
    "Vsv": "lpc_systemic_perfusion",
    "Vvc": "lpc_systemic_perfusion",
    "Vcorao": "lpc_coronary_perfusion",
    "Vcorcap": "lpc_coronary_perfusion",
    "Vcorea": "lpc_coronary_perfusion",
    "Vcorev": "lpc_coronary_perfusion",
    "Vcorla": "lpc_coronary_perfusion",
    "Vcorlv": "lpc_coronary_perfusion",
    "Vcorsa": "lpc_coronary_perfusion",
    "Vcorsv": "lpc_coronary_perfusion",
    "Faod": "lpc_blood_flows",
    "Faop": "lpc_blood_flows",
    "Fpad": "lpc_blood_flows",
    "Fpap": "lpc_blood_flows",
    "MAP": "lpc_blood_pressures",
    "Paopc": "lpc_blood_pressures",
}


def _signal_value(signal: BioSignal | None) -> Any:
    if signal is None:
        return None
    value = getattr(signal, "value", None)
    if isinstance(value, dict) and set(value.keys()) == {"payload"}:
        return value["payload"]
    return value


def _load_yaml(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text())
    return loaded if isinstance(loaded, dict) else {}


def _load_entrypoint(model_dir: Path, entrypoint: str):
    module_name, _, attr_name = entrypoint.partition(":")
    if not module_name or not attr_name:
        raise ValueError(f"Invalid entrypoint: {entrypoint}")
    module_path = model_dir / (module_name.replace(".", "/") + ".py")
    if not module_path.exists():
        module_path = model_dir / module_name.replace(".", "/") / "__init__.py"
    unique_name = f"biomechanics_visualisation__{abs(hash(str(module_path)))}"
    spec = importlib.util.spec_from_file_location(unique_name, module_path)
    if spec is None or spec.loader is None:
        raise ValueError(f"Unable to load entrypoint module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, attr_name)


def _discover_observables_from_xml(xml_path: Path, strategy: str) -> tuple[list[str], dict[str, Optional[str]], dict[str, str]]:
    try:
        tree = ET.parse(xml_path)
    except (ET.ParseError, OSError):
        return [], {}, {}
    root = tree.getroot()
    suffix_species = "}species"
    suffix_rate = "}rateRule"
    suffix_param = "}parameter"
    observables: list[str] = []
    units: dict[str, Optional[str]] = {}
    display: dict[str, str] = {}
    if strategy == "species":
        for el in root.iter():
            if not el.tag.endswith(suffix_species):
                continue
            sid = el.attrib.get("id")
            sbo = el.attrib.get("sboTerm", "")
            if sid and sbo != "SBO:0000291" and sid != "dummy":
                observables.append(sid)
                units[sid] = el.attrib.get("substanceUnits") or el.attrib.get("units")
                name = el.attrib.get("name")
                if name and name != sid:
                    display[sid] = name
        return observables, units, display
    param_names: dict[str, str] = {}
    for el in root.iter():
        if el.tag.endswith(suffix_param):
            pid = el.attrib.get("id")
            pname = el.attrib.get("name")
            if pid and pname and pname != pid:
                param_names[pid] = pname
    for el in root.iter():
        if el.tag.endswith(suffix_rate):
            var = el.attrib.get("variable")
            if var and var != "dummy":
                observables.append(var)
                units[var] = None
                if var in param_names:
                    display[var] = param_names[var]
    if observables:
        return observables, units, display
    suffix_assign = "}assignmentRule"
    for el in root.iter():
        if el.tag.endswith(suffix_assign):
            var = el.attrib.get("variable")
            if var and var != "dummy":
                observables.append(var)
                units[var] = None
                if var in param_names:
                    display[var] = param_names[var]
    return observables, units, display


def _group_observable(name: str, display_name: Optional[str]) -> str:
    if display_name and display_name in _KOO2013_GROUP_LOOKUP:
        return _KOO2013_GROUP_LOOKUP[display_name]
    if name.startswith("sub_X_"):
        return "substrate_concentration"
    if name.startswith("F_AO"):
        return "aortic_flow"
    if name.startswith("V_"):
        suffix = name[2:]
        if suffix in {"LA", "LV", "RA", "RV"}:
            return "cardiac_chambers"
        if suffix in {"AO", "PA", "CO", "CR", "CRtissue"}:
            return "central_vessels"
        if suffix in {"AR", "AD"}:
            return "systemic_arteries"
        if suffix in {"MU", "GI", "LI", "KI", "SK", "OT"}:
            return "peripheral_tissue"
        if suffix in {"VE", "VC", "Pa", "PC", "PV"}:
            return "veins"
    if name in _LPC_GROUP_LOOKUP:
        return _LPC_GROUP_LOOKUP[name]
    return "other"


def _humanize_from_compartment_code(name: str) -> Optional[str]:
    if name.startswith("sub_X_"):
        readable = _COMPARTMENT_NAMES.get(name[len("sub_X_"):], name[len("sub_X_"):])
        return f"Tracer amount in {readable}"
    if name.startswith("conc_X_"):
        readable = _COMPARTMENT_NAMES.get(name[len("conc_X_"):], name[len("conc_X_"):])
        return f"Tracer concentration in {readable}"
    if name.startswith("V_"):
        readable = _COMPARTMENT_NAMES.get(name[2:])
        if readable:
            return f"{readable} volume"
    if name.startswith("P_"):
        readable = _COMPARTMENT_NAMES.get(name[2:])
        if readable:
            return f"{readable} pressure"
    return None


def _display_name(name: str, display_names: Mapping[str, str]) -> str:
    bio_key = display_names.get(name, name)
    if bio_key in _KOO2013_LABELS:
        return _KOO2013_LABELS[bio_key]
    if name in _HELDT2002_LABELS:
        return _HELDT2002_LABELS[name]
    if bio_key in _HELDT2002_LABELS:
        return _HELDT2002_LABELS[bio_key]
    if bio_key != name:
        return bio_key
    compartment_label = _humanize_from_compartment_code(name)
    return compartment_label or name


class BiomechanicsVisualisationModel(BioModule):
    """Render user-facing visuals and explanations from core model signals."""

    def __init__(
        self,
        *,
        lab_title: str,
        sources: list[dict[str, Any]],
        integration_step: float = 1.0,
    ) -> None:
        self.lab_title = str(lab_title)
        self.integration_step = float(integration_step)
        self._model_root = Path(__file__).resolve().parent.parent
        self._inputs: dict[str, BioSignal] = {}
        self._time = 0.0
        self._history: dict[str, list[dict[str, Any]]] = {}
        self._latest_summary: dict[str, dict[str, Any]] = {}
        self._latest_headlines: dict[str, dict[str, float]] = {}
        self._source_meta = self._load_sources(sources)

    def _load_sources(self, sources: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
        loaded: dict[str, dict[str, Any]] = {}
        for source in sources:
            alias = str(source["alias"])
            model_dir = (self._model_root / str(source["path"])).resolve()
            manifest = _load_yaml(model_dir / "model.yaml")
            bsim = manifest.get("biosim") or {}
            factory = _load_entrypoint(model_dir, str(bsim["entrypoint"]))
            init_kwargs = dict(bsim.get("init_kwargs") or {})
            module = factory(**init_kwargs)
            outputs = module.outputs()
            model_path = model_dir / str(init_kwargs.get("model_path", ""))
            observables, units, display_names = _discover_observables_from_xml(
                model_path,
                str(source.get("observable_strategy", "species")),
            )
            scalar_outputs = [
                name for name, spec in outputs.items()
                if name not in {"state", "summary", "visualisation_aux"} and spec.signal_type == "scalar"
            ]
            loaded[alias] = {
                "alias": alias,
                "manifest": manifest,
                "outputs": outputs,
                "title": str(manifest.get("title") or alias),
                "observables": observables,
                "units": units,
                "display_names": display_names,
                "scalar_outputs": scalar_outputs,
                "phase_portrait": deepcopy(source.get("phase_portrait")),
            }
        return loaded

    def inputs(self) -> dict[str, SignalSpec]:
        specs: dict[str, SignalSpec] = {}
        for alias, meta in self._source_meta.items():
            outputs = meta["outputs"]
            for output_name in ("state", "summary", "visualisation_aux"):
                if output_name not in outputs:
                    continue
                source_spec = outputs[output_name]
                if source_spec.signal_type != "record":
                    continue
                specs[f"{alias}_{output_name}"] = SignalSpec.record(
                    schema=dict(source_spec.schema or {"payload": "json"}),
                    accepted_profiles=(
                        AcceptedSignalProfile(
                            signal_type="record",
                            schema=dict(source_spec.schema or {"payload": "json"}),
                        ),
                    ),
                    description=f"{alias} {output_name} feed for the visualisation model.",
                )
            for output_name in meta["scalar_outputs"]:
                source_spec = outputs[output_name]
                specs[f"{alias}_{output_name}"] = SignalSpec.scalar(
                    dtype=source_spec.dtype or "float64",
                    accepted_profiles=(
                        AcceptedSignalProfile(
                            signal_type="scalar",
                            dtype=source_spec.dtype or "float64",
                            accepted_units=(source_spec.emitted_unit,) if source_spec.emitted_unit else None,
                        ),
                    ),
                    description=f"{alias} {output_name} headline signal for the visualisation model.",
                )
        return specs

    def outputs(self) -> dict[str, SignalSpec]:
        return {}

    def setup(self, config: Optional[dict[str, Any]] = None) -> None:
        self.reset()

    def reset(self) -> None:
        self._inputs = {}
        self._time = 0.0
        self._history = {alias: [] for alias in self._source_meta}
        self._latest_summary = {}
        self._latest_headlines = {alias: {} for alias in self._source_meta}

    def set_inputs(self, inputs: dict[str, BioSignal]) -> None:
        self._inputs = dict(inputs or {})

    def advance_window(self, start: float, end: float) -> None:
        self._time = float(end)
        for alias in self._source_meta:
            self._capture_source(alias, self._time)

    def get_outputs(self) -> dict[str, BioSignal]:
        return {}

    def visualize(self) -> Optional[list["VisualSpec"]]:
        visuals: list["VisualSpec"] = []
        for alias, meta in self._source_meta.items():
            history = self._history.get(alias) or []
            if not history:
                continue
            visuals.extend(self._grouped_timeseries_visuals(alias, meta, history))
            visuals.append(self._largest_changes_visual(meta, history))
            visuals.append(self._what_happened_visual(meta, history, self._latest_summary.get(alias, {})))
            portrait = self._phase_portrait_visual(meta, history)
            if portrait is not None:
                visuals.append(portrait)
        return visuals or None

    def _capture_source(self, alias: str, emitted_at: float) -> None:
        meta = self._source_meta[alias]
        state_value = _signal_value(self._inputs.get(f"{alias}_state"))
        if isinstance(state_value, Mapping):
            row = {"t": float(getattr(self._inputs.get(f"{alias}_state"), "emitted_at", emitted_at))}
            row.update(dict(state_value))
            aux_value = _signal_value(self._inputs.get(f"{alias}_visualisation_aux"))
            if isinstance(aux_value, Mapping):
                row.update(dict(aux_value))
            history = self._history.setdefault(alias, [])
            if not history or float(history[-1].get("t", -1.0)) != float(row["t"]):
                history.append(row)
        summary_value = _signal_value(self._inputs.get(f"{alias}_summary"))
        if isinstance(summary_value, Mapping):
            self._latest_summary[alias] = dict(summary_value)
        for output_name in meta["scalar_outputs"]:
            value = _signal_value(self._inputs.get(f"{alias}_{output_name}"))
            if isinstance(value, (int, float)):
                self._latest_headlines.setdefault(alias, {})[output_name] = float(value)

    def _grouped_timeseries_visuals(
        self,
        alias: str,
        meta: Mapping[str, Any],
        history: list[dict[str, Any]],
    ) -> list["VisualSpec"]:
        groups: dict[str, list[str]] = {}
        for name in meta["observables"]:
            if name not in history[-1]:
                continue
            display = meta["display_names"].get(name)
            groups.setdefault(_group_observable(name, display), []).append(name)
        visuals: list["VisualSpec"] = []
        for key, (title_suffix, description) in _GROUP_META.items():
            names = groups.get(key)
            if not names:
                continue
            visuals.append(
                {
                    "render": "timeseries",
                    "description": description,
                    "data": {
                        "title": f"{meta['title']} - {title_suffix}",
                        "x_unit": "s",
                        "series": [
                            {
                                "name": _display_name(name, meta["display_names"]),
                                "points": [[point["t"], point[name]] for point in history if name in point],
                            }
                            for name in names
                        ],
                    },
                }
            )
        return visuals

    def _largest_changes_visual(self, meta: Mapping[str, Any], history: list[dict[str, Any]]) -> "VisualSpec":
        ranges: dict[str, float] = {}
        for name in meta["observables"]:
            values = [float(point.get(name, 0.0)) for point in history if name in point]
            if values:
                ranges[name] = max(values) - min(values)
        ranked = sorted(ranges.items(), key=lambda pair: pair[1], reverse=True)[:8]
        return {
            "render": "bar",
            "description": "Which observables shifted the most during the run?",
            "data": {
                "title": f"{meta['title']} - largest excursions during the run",
                "categories": [_display_name(name, meta["display_names"]) for name, _ in ranked],
                "values": [value for _, value in ranked],
            },
        }

    def _what_happened_visual(
        self,
        meta: Mapping[str, Any],
        history: list[dict[str, Any]],
        summary: Mapping[str, Any],
    ) -> "VisualSpec":
        first = history[0]
        last = history[-1]
        biggest_change = str(summary.get("largest_change_observable", ""))
        biggest_peak = str(summary.get("peak_observable", ""))
        rows = [
            ["What did this run track?", f"{len(meta['observables'])} observables in {meta['title']}"],
            ["How long did it run?", f"{float(last.get('t', 0.0)) - float(first.get('t', 0.0)):.3g} s"],
            ["Which observable changed the most?", _display_name(biggest_change, meta["display_names"]) if biggest_change else "Unavailable"],
            ["Largest peak?", _display_name(biggest_peak, meta["display_names"]) if biggest_peak else "Unavailable"],
        ]
        return {
            "render": "table",
            "description": "What did this simulation actually show, in plain language?",
            "data": {"title": "What Happened", "columns": ["Question", "Answer"], "rows": rows},
        }

    def _phase_portrait_visual(self, meta: Mapping[str, Any], history: list[dict[str, Any]]) -> Optional["VisualSpec"]:
        config = meta.get("phase_portrait")
        if not isinstance(config, Mapping):
            return None
        x_key = str(config.get("x_key", "phase_x"))
        y_key = str(config.get("y_key", "phase_y"))
        points = [
            {"x": float(point[x_key]), "y": float(point[y_key]), "series": str(config.get("series", "cycle"))}
            for point in history
            if x_key in point and y_key in point
        ]
        if len(points) < 2:
            return None
        return {
            "render": "scatter",
            "description": str(config.get("description", "Phase portrait for the latest cycle.")),
            "data": {
                "title": str(config.get("title", "Phase portrait")),
                "x_label": str(config.get("x_label", "x")),
                "y_label": str(config.get("y_label", "y")),
                "x_unit": str(config.get("x_unit", "")),
                "y_unit": str(config.get("y_unit", "")),
                "connect_points": True,
                "points": points,
            },
        }
