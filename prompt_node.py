"""ComfyUI-node die de Character-builder-prompt bouwt uit het gedeelde cast_character-manifest."""
import json
import os
from pathlib import Path

try:  # als package (ComfyUI) én flat (pytest) importeerbaar
    from .compose_logic import compose_form, _cleanup
except ImportError:  # pragma: no cover
    from compose_logic import compose_form, _cleanup

_HERE = Path(__file__).resolve().parent


def _resolve_manifest_path():
    """env CHARACTER_STUDIO_MANIFEST → repo-relatief app-pad → gebundelde kopie."""
    candidates = []
    env = os.environ.get("CHARACTER_STUDIO_MANIFEST")
    if env:
        candidates.append(Path(env))
    # comfy_nodes/character_studio_prompt/ → ../../orchestrator/workflows/... (bij symlink vanuit de repo)
    candidates.append(_HERE.parents[1] / "orchestrator" / "workflows" / "cast_character.manifest.json")
    candidates.append(_HERE / "cast_character.manifest.json")  # gebundelde fallback
    for p in candidates:
        try:
            if p and p.is_file():
                return p
        except OSError:
            continue
    return None


def _load_form_param():
    p = _resolve_manifest_path()
    if p is None:
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return next((x for x in data.get("params", []) if x.get("type") == "form_builder"), None)
    except Exception:  # noqa: BLE001 — kapot/onvindbaar manifest → node toont een foutmelding
        return None


def _input_types_from(cb: dict) -> dict:
    """Bouw de ComfyUI INPUT_TYPES-dict uit de manifest-velden (enum→dropdown, tekst/wardrobe→STRING)."""
    if not cb:
        return {"required": {"error": ("STRING", {"default": "cast_character.manifest.json niet gevonden", "multiline": True})}}
    required = {}
    for f in cb.get("fields", []):
        key = f["key"]
        if f.get("type") == "enum" and f.get("options"):
            options = list(f["options"])
            default = f.get("default") if f.get("default") in options else options[0]
            required[key] = (options, {"default": default})
        else:  # text, wardrobe, of onbekend type → vrije tekst
            required[key] = ("STRING", {"default": f.get("default", ""), "multiline": False})
    return {"required": required, "optional": {"extra": ("STRING", {"default": "", "multiline": True})}}


_CB = _load_form_param()


class CharacterStudioPrompt:
    """Character Studio — portret-prompt: vult de manifest-template met je gekozen velden."""

    @classmethod
    def INPUT_TYPES(cls):
        return _input_types_from(_CB)

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "build"
    CATEGORY = "Character Studio"

    def build(self, extra="", **kwargs):
        if not _CB:
            return (kwargs.get("error", "cast_character.manifest.json niet gevonden"),)
        wardrobe_text = kwargs.get("wardrobe", "")
        fields = {k: v for k, v in kwargs.items() if k != "wardrobe"}
        value = {"fields": fields, "wardrobe": {"mode": "free", "text": wardrobe_text}}
        prompt = compose_form(_CB, value)
        if extra and str(extra).strip():
            prompt = _cleanup(prompt + " " + str(extra).strip())
        return (prompt,)
