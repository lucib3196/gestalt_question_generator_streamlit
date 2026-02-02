from pydantic import BaseModel
from typing import Dict, Literal

ALLOWED_MODE = Literal["text", "file"]

CHAT_NAMES = Literal["gestalt_generate_module", "file_upload", "gestalt_build_module"]


class ChatOption(BaseModel):
    label: str
    url: str
    description: str
    mode: ALLOWED_MODE = "text"
    active: bool = False


CHAT_OPTIONS: Dict[CHAT_NAMES, ChatOption] = {
    "gestalt_generate_module": ChatOption(
        label="Generate Full Module (One-Shot)",
        url="agent_gestalt_module",
        description=(
            "Generate an entire Gestalt module in a single automated pass. "
            "This mode creates ALL required files at once "
            "(question.html, solution.html, server logic, and metadata). "
            "Best when inputs are finalized and no iteration is needed."
        ),
        active=True,
    ),
    "gestalt_build_module": ChatOption(
        label="Build Module File-by-File",
        url="agent_gestalt",
        description=(
            "Build a Gestalt module incrementally with full control over "
            "each file. This mode supports step-by-step generation, "
            "editing, validation, and refinement of individual files "
            "(question.html, solution.html, server logic, and metadata)."
        ),
        active=True,
    ),
    "file_upload": ChatOption(
        label="File Upload",
        url="agent_gestalt",
        description="File Upload",
        active=False,
        mode="file",
    ),
}
