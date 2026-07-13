# Character Studio — Prompt (ComfyUI custom node)

A ComfyUI custom node that assembles a natural-language **character portrait prompt** from structured
fields (origin, age, build, skin, face, hair, wardrobe, camera & lens, …).

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

<img width="1217" height="803" alt="image" src="https://github.com/user-attachments/assets/b19ece06-8de9-428f-80b2-d8fa1cf65c19" />


## Usage

1. Add the node **Character Studio — Portret-prompt**.
2. Pick the character traits in the dropdowns / text fields. Every field has a sensible default, so an
   untouched node still produces a coherent, fully-clothed portrait prompt.
3. (Optional) type anything into **extra** — it is appended to the end of the prompt.
4. **Connect it to a CLIP Text Encode.** The node's `prompt` output is a `STRING`, but a CLIP Text Encode's
   `text` field is a widget by default. Right-click the **CLIP Text Encode (Prompt)** node →
   **Convert Widget to Input → text** (older ComfyUI: *Convert text to input*), then drag the node's
   **`prompt`** output onto that new **text** input.
5. Wire the CLIP Text Encode's `CONDITIONING` output into your sampler's positive input, as usual.

Tip: to see the exact prompt the node produced, add any "Show Text" / string-preview node and connect
`prompt` to it.

## Fields & manifest

The fields, options, defaults and the prompt template all come from `cast_character.manifest.json`, which is
**bundled with this node** — after `git clone` it works out of the box, nothing to configure. Edit that file
(and restart ComfyUI) to change the available options.

### Optional — sync with a running Character Studio app

Only relevant if you *also* run the Character Studio app and want this node to follow the app's **live**
manifest (so edits you make to the character fields in the app show up here automatically): set the
environment variable `CHARACTER_STUDIO_MANIFEST` to the full path of the app's `cast_character.manifest.json`.

Resolution order: `CHARACTER_STUDIO_MANIFEST` → the bundled copy. **Restart ComfyUI after changing the
manifest** to load new options.

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
