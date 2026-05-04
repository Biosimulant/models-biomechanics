from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from typing import Any

import yaml


_LAB_DIR = Path(__file__).resolve().parents[1]


def _find_bsim_src(start: Path) -> Path | None:
    for parent in [start, *start.parents]:
        for candidate in (parent / "biosim" / "src", parent / "bsim-active" / "biosim" / "src"):
            if (candidate / "biosim").is_dir():
                return candidate
    return None


def _ensure_biosim_on_path() -> None:
    bsim_src = _find_bsim_src(_LAB_DIR)
    if bsim_src is not None and str(bsim_src) not in sys.path:
        sys.path.insert(0, str(bsim_src))


def _load_entrypoint(model_dir: Path, entrypoint: str):
    _ensure_biosim_on_path()
    module_name, _, attr_name = entrypoint.partition(":")
    if not module_name or not attr_name:
        raise ValueError(f"Invalid entrypoint: {entrypoint}")
    module_path = model_dir / (module_name.replace(".", "/") + ".py")
    if not module_path.exists():
        module_path = model_dir / module_name.replace(".", "/") / "__init__.py"
    unique_name = f"koo2013_shear_to_no_test_{abs(hash(str(module_path)))}"
    spec = importlib.util.spec_from_file_location(unique_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[unique_name] = module
    spec.loader.exec_module(module)
    return getattr(module, attr_name)


def _load_lab_manifest() -> dict[str, Any]:
    manifest = yaml.safe_load((_LAB_DIR / "lab.yaml").read_text())
    return manifest if isinstance(manifest, dict) else {}


def _resolve_visualisation_sources(
    *,
    init_kwargs: dict[str, Any],
    model_paths_by_alias: dict[str, str],
) -> dict[str, Any]:
    sources = init_kwargs.get("sources")
    if not isinstance(sources, list):
        return init_kwargs
    resolved_sources: list[dict[str, Any]] = []
    for source in sources:
        source_alias = str(source["alias"])
        resolved = dict(source)
        resolved["resolved_path"] = model_paths_by_alias[source_alias]
        resolved_sources.append(resolved)
    return {**init_kwargs, "sources": resolved_sources}


def _instantiate_lab_modules() -> tuple[dict[str, Any], dict[str, Any]]:
    manifest = _load_lab_manifest()
    model_paths_by_alias = {
        str(entry["alias"]): str((_LAB_DIR / str(entry["path"])).resolve())
        for entry in manifest["models"]
    }
    modules: dict[str, Any] = {}
    for entry in manifest["models"]:
        alias = str(entry["alias"])
        model_dir = Path(model_paths_by_alias[alias])
        model_manifest = yaml.safe_load((model_dir / "model.yaml").read_text())
        bsim = model_manifest["biosim"]
        init_kwargs = _resolve_visualisation_sources(
            init_kwargs=dict(bsim.get("init_kwargs") or {}),
            model_paths_by_alias=model_paths_by_alias,
        )
        factory = _load_entrypoint(model_dir, str(bsim["entrypoint"]))
        modules[alias] = factory(**init_kwargs)
    return manifest, modules


def test_lab_manifest_uses_embedded_visualisation_model():
    manifest = _load_lab_manifest()
    model_aliases = [entry["alias"] for entry in manifest["models"]]
    assert "visualisation" in model_aliases
    assert all(str(entry["path"]).startswith("models/") for entry in manifest["models"])

    public_outputs = {entry["name"] for entry in manifest["io"]["outputs"]}
    assert {"visualisation_story", "visualisation_next_questions", "visualisation_metadata"}.isdisjoint(public_outputs)
    assert not any(str(entry["maps_to"]).startswith("visualisation.") for entry in manifest["io"]["outputs"])

    wiring_targets = {
        target
        for entry in manifest["wiring"]
        for target in entry["to"]
    }
    assert any(target.startswith("visualisation.") for target in wiring_targets)


def test_calcium_output_matches_no_production_input_profile():
    _ensure_biosim_on_path()
    from biosim.signals import validate_connection_specs

    _manifest, modules = _instantiate_lab_modules()
    source = modules["calcium_influx"].outputs()["cytosolic_calcium"]
    target = modules["no_production"].inputs()["cytosolic_calcium"]

    assert source.emitted_unit == "substance"
    assert modules["calcium_influx"].outputs()["ip3"].emitted_unit == "substance"
    assert modules["no_production"].outputs()["active_eNOS"].emitted_unit == "substance"
    assert modules["no_production"].outputs()["nitric_oxide"].emitted_unit == "substance"
    validate_connection_specs(source, target)


def test_lab_yaml_wiring_specs_apply_without_runtime_setup():
    _ensure_biosim_on_path()
    from biosim import BioWorld
    from biosim.wiring import WiringBuilder

    manifest, modules = _instantiate_lab_modules()
    world = BioWorld(communication_step=float(manifest["runtime"]["communication_step"]))
    builder = WiringBuilder(world)
    for alias, module in modules.items():
        builder.add(alias, module)
    for entry in manifest["wiring"]:
        builder.connect(entry["from"], entry["to"])

    builder.apply()
