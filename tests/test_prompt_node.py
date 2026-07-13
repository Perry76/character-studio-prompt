import sys
from pathlib import Path

import pytest

_PKG = Path(__file__).resolve().parents[1]
_REPO = _PKG.parents[1]
sys.path.insert(0, str(_PKG))           # flat-import van het node-pakket

import compose_logic as node_compose      # noqa: E402
import prompt_node                          # noqa: E402

# app-compose bestaat alleen binnen de Character Studio-monorepo; in een standalone repo overslaan.
try:
    sys.path.insert(0, str(_REPO / "orchestrator"))
    import compose as app_compose          # noqa: E402  (orchestrator/compose.py)
except Exception:  # noqa: BLE001
    app_compose = None

MINI_CB = {
    "template": "A {origin} {gender}. Wardrobe: {wardrobe}. {mood}.",
    "fields": [
        {"key": "origin", "type": "enum", "options": ["Dutch", "Japanese"], "default": "Dutch"},
        {"key": "gender", "type": "enum", "options": ["woman", "man"], "default": "woman"},
        {"key": "mood", "type": "text", "default": "calm"},
        {"key": "wardrobe", "type": "wardrobe"},
    ],
}


def test_ported_compose_form_fills_and_defaults():
    p = node_compose.compose_form(MINI_CB, {"fields": {"gender": "man"}, "wardrobe": {"mode": "free", "text": "a suit"}})
    assert p == "A Dutch man. Wardrobe: a suit. calm."


def test_ported_compose_form_empty_wardrobe_cleans_up():
    p = node_compose.compose_form(MINI_CB, {"fields": {}, "wardrobe": None})
    # leeg wardrobe → _cleanup verwijdert de spatie vóór de punt ("Wardrobe: ." → "Wardrobe:.")
    assert p == "A Dutch woman. Wardrobe:. calm."


def test_input_types_from_builds_widgets():
    it = prompt_node._input_types_from(MINI_CB)
    req = it["required"]
    assert req["origin"] == (["Dutch", "Japanese"], {"default": "Dutch"})
    assert req["mood"][0] == "STRING" and req["mood"][1]["default"] == "calm"
    assert req["wardrobe"][0] == "STRING"          # wardrobe = vrije tekst
    assert it["optional"]["extra"][0] == "STRING" and it["optional"]["extra"][1]["multiline"] is True


def test_input_types_no_manifest_shows_error():
    it = prompt_node._input_types_from(None)
    assert "error" in it["required"]


def test_wardrobe_default_fallback_and_override():
    cb = {"template": "Wardrobe: {wardrobe}.",
          "fields": [{"key": "wardrobe", "type": "wardrobe", "default": "casual everyday clothing"}]}
    # leeg → terugval op de default; eigen invoer overruled
    assert node_compose.compose_form(cb, {"fields": {}, "wardrobe": None}) == "Wardrobe: casual everyday clothing."
    assert node_compose.compose_form(cb, {"fields": {}, "wardrobe": {"mode": "free", "text": "a red gown"}}) == "Wardrobe: a red gown."


def test_compose_preserves_paragraph_breaks():
    cb = {"template": "{a}\n\n{b}\n\n{c}",
          "fields": [{"key": "a", "type": "text", "default": "first block"},
                     {"key": "b", "type": "text", "default": ""},
                     {"key": "c", "type": "text", "default": "third block"}]}
    # witregels blijven tussen blokken; een leeg blok wordt weggelaten
    assert node_compose.compose_form(cb, {"fields": {}, "wardrobe": None}) == "first block\n\nthird block"


@pytest.mark.skipif(app_compose is None, reason="orchestrator/compose.py niet beschikbaar (standalone repo)")
def test_parity_with_app_compose():
    # De geporte kopie moet exact hetzelfde produceren als orchestrator/compose.py.
    val = {"fields": {"origin": "Japanese", "gender": "man", "mood": "serious"},
           "wardrobe": {"mode": "free", "text": "a wool coat"}}
    assert node_compose.compose_form(MINI_CB, val) == app_compose.compose_form(MINI_CB, val)
