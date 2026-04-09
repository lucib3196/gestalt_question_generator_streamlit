from core.session import init_session
from core.settings import get_settings
from ui import (
    render_title,
    render_select_box,
    render_chatbot_description,
    render_chat,
    render_chat_input,
)
import streamlit as st

init_session()
settings = get_settings()

def render_ui():
    # Header Section
    render_title(
        title=settings.name,
        env=settings.env.value,
        thread_id=st.session_state.thread_id,
    )
    render_select_box()
    render_chatbot_description()

    # Actual Chat Component
    render_chat()
    render_chat_input()

render_ui()
