"""Character Studio ComfyUI-nodes — registratie."""
try:
    from .prompt_node import CharacterStudioPrompt
except ImportError:  # pragma: no cover
    from prompt_node import CharacterStudioPrompt

NODE_CLASS_MAPPINGS = {"CharacterStudioPrompt": CharacterStudioPrompt}
NODE_DISPLAY_NAME_MAPPINGS = {"CharacterStudioPrompt": "Character Studio — Portret-prompt"}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
