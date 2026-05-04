from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import yaml


_MODEL_DIR = Path(__file__).resolve().parents[1]
_WRAPPER_PATH = _MODEL_DIR / "src" / "biomechanics_visualisation.py"


def _find_bsim_src(start: Path) -> Path | None:
    for parent in [start, *start.parents]:
        for candidate in (parent / "biosim" / "src", parent / "bsim-active" / "biosim" / "src"):
            if (candidate / "biosim").is_dir():
                return candidate
    return None


_BSIM_SRC = _find_bsim_src(_MODEL_DIR)
if _BSIM_SRC is not None and str(_BSIM_SRC) not in sys.path:
    sys.path.insert(0, str(_BSIM_SRC))


from biosim.signals import RecordSignal, ScalarSignal


def _load_wrapper():
    bsim_src = _find_bsim_src(_MODEL_DIR)
    if bsim_src is not None and str(bsim_src) not in sys.path:
        sys.path.insert(0, str(bsim_src))
    unique_name = f"biomechanics_visualisation__{_MODEL_DIR.parent.parent.name}"
    spec = importlib.util.spec_from_file_location(unique_name, _WRAPPER_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[unique_name] = module
    spec.loader.exec_module(module)
    return module


def _load_model():
    manifest = yaml.safe_load((_MODEL_DIR / "model.yaml").read_text())
    init_kwargs = dict(manifest["biosim"]["init_kwargs"])
    module_cls = _load_wrapper().BiomechanicsVisualisationModel
    return module_cls(**init_kwargs), float(manifest["biosim"]["communication_step"])


def _sample_record(schema: dict[str, str]) -> dict[str, object]:
    payload: dict[str, object] = {}
    for key, kind in schema.items():
        if kind == "str":
            payload[key] = key
        elif kind == "int":
            payload[key] = 0
        elif kind == "list":
            payload[key] = []
        else:
            payload[key] = 0.0
    return payload


def test_visualisation_model_stays_internal_and_renders_visuals():
    module, step = _load_model()
    specs = module.inputs()
    inputs = {}
    for name, spec in specs.items():
        if spec.signal_type == "record":
            payload = _sample_record(dict(spec.schema or {}))
            inputs[name] = RecordSignal(source="test", name=name, value=payload, emitted_at=step, spec=spec)
        else:
            inputs[name] = ScalarSignal(source="test", name=name, value=0.0, emitted_at=step, spec=spec)
    module.set_inputs(inputs)
    module.advance_window(0.0, step)

    assert module.outputs() == {}
    assert module.get_outputs() == {}
    visuals = module.visualize()
    assert isinstance(visuals, list) and visuals
    renders = {visual["render"] for visual in visuals}
    assert {"timeseries", "bar", "table"}.issubset(renders)
