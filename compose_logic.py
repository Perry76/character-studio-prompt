"""Geporte prompt-assembly uit orchestrator/compose.py — verbatim gehouden (pariteitstest bewaakt dit)."""
import re


def compose_wardrobe(value: dict | None) -> str:
    if not value:
        return ""
    if value.get("mode") == "structured":
        parts = []
        for item in value.get("items", []):
            phrase = " ".join(
                w for w in (item.get("color", ""), item.get("material", ""), item.get("type", "")) if w
            ).strip()
            if not phrase:
                continue
            piece = f"a {phrase}"
            details = (item.get("details") or "").strip()
            if details:
                piece += f", {details}"
            parts.append(piece)
        return ", ".join(parts)
    return (value.get("text") or "").strip()


def _cleanup(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.])", r"\1", text)
    text = re.sub(r",\s*,", ",", text)
    text = re.sub(r"\(\s*\)", "", text)
    return text.strip()


def compose_form(cb_param: dict, value: dict) -> str:
    fields = value.get("fields", {})
    subs = {}
    for f in cb_param["fields"]:
        key = f["key"]
        if key == "wardrobe":
            continue
        v = fields.get(key)
        if v is None or v == "":
            v = f.get("default", "")
        subs[key] = str(v)
    wardrobe = compose_wardrobe(value.get("wardrobe"))
    if not wardrobe:  # leeg → terugval op de wardrobe-default (voorkomt een prompt-vacuum → naakt)
        wf = next((f for f in cb_param["fields"] if f.get("key") == "wardrobe"), {})
        wardrobe = wf.get("default", "")
    subs["wardrobe"] = wardrobe
    prompt = cb_param["template"]
    for k, v in subs.items():
        prompt = prompt.replace("{" + k + "}", v)
    return _cleanup(prompt)
