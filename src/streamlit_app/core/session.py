from typing import Any, List
from pydantic import BaseModel
import streamlit as st
from io import BytesIO
from .config import CHAT_NAMES
from services.llm_services import initialize_thread_id
from pydantic import BaseModel, ConfigDict
from typing import Dict


class DefaultState(BaseModel):
    messages: List[Any] = []
    thread_id: str | None = None
    chat_select: CHAT_NAMES | None
    files: Dict[str, BytesIO] = {}
    selected_file: BytesIO | None = None
    show_file_uploads: bool = False

    model_config = ConfigDict(arbitrary_types_allowed=True)


DEFAULT_STATE = DefaultState(
    messages=[],
    chat_select=None,
    thread_id=initialize_thread_id(),
)


def init_session():
    for key, value in DEFAULT_STATE.model_dump().items():
        if key not in st.session_state:
            st.session_state[key] = value
