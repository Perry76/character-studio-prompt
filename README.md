# Character Studio — Prompt (ComfyUI custom node)

A ComfyUI custom node that assembles a natural-language **character portrait prompt** from structured
fields (origin, age, build, skin, face, hair, wardrobe, camera & lens, …). It reproduces the prompt builder
of the [Character Studio](https://github.com/Perry76) character builder, so you can generate the exact same
prompt directly inside a ComfyUI graph.

The node exposes every field as a widget (dropdowns for the enumerated options, text inputs for the rest) and
outputs a single `STRING` — connect it to a **CLIP Text Encode**.

![node](https://img.shields.io/badge/ComfyUI-custom%20node-6b46c1) ![license](https://img.shields.io/badge/license-MIT-blue)

## Why

Character consistency is easier when the description is complete and deterministic. Leaving traits out
creates a prompt "vacuum" that the model fills with its own prior; this node uses positive, template-driven
defaults (e.g. `clean-shaven`, `no freckles`, a fallback wardrobe) so every field is stated explicitly.

## Install

Clone into your ComfyUI `custom_nodes` folder and restart ComfyUI:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/Perry76/character-studio-prompt.git
```

No extra dependencies (Python standard library only). Restart ComfyUI — the node appears under
**Add Node → Character Studio → Portret-prompt**. Connect its `prompt` output to a **CLIP Text Encode**.

## Usage

1. Add the node **Character Studio — Portret-prompt**.
2. Pick the character traits in the dropdowns / text fields. Every field has a sensible default, so an
   untouched node still produces a coherent, fully-clothed portrait prompt.
3. (Optional) type anything into **extra** — it is appended to the end of the prompt.
4. Wire `prompt` into a CLIP Text Encode.

## Fields & manifest

The fields, options, defaults and the prompt template all come from `cast_character.manifest.json`, which is
bundled with this node. If you also run the Character Studio app, point the node at the app's live manifest so
the two stay in sync:

- Set the environment variable `CHARACTER_STUDIO_MANIFEST` to the full path of the app's
  `cast_character.manifest.json`, **or**
- install this node as a symlink from the app repo (`comfy_nodes/character_studio_prompt`) so the relative
  path to the app manifest resolves.

Resolution order: `CHARACTER_STUDIO_MANIFEST` → app-relative path → the bundled copy. **Restart ComfyUI after
changing the manifest** to load new options.

## Notes / limits

- Enums are dropdowns; for one-off additions use the optional **extra** field.
- **Wardrobe** is a free-text field. Leave it empty and a default outfit (`casual everyday clothing`) is used
  so the subject is never rendered nude; type your own outfit to override it.
- The structured wardrobe builder, per-field custom values, and other Character Studio flows are app-only.

## Development

```bash
python -m pytest tests/ -q
```

The tests cover the ported assembly logic, the dynamic widget builder, and the empty-wardrobe fallback. A
parity test (node output == the Character Studio app's `compose.py`) runs only when the app is present and is
skipped otherwise.

## License

MIT — see [LICENSE](LICENSE).
