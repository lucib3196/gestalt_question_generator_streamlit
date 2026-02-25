import streamlit as st
from core import ChatOption, CHAT_OPTIONS
from type.types import ENV, IMAGETYPES, PDFTYPES
from services.llm_services import get_new_thread_id
from core.logger import logger



def render_title(
    title: str = "My Chat", env: ENV = ENV.LOCAL, thread_id: str | None = None
):
    if env == "local":
        title += " (Local DEV)"
    if thread_id:
        title += f" {thread_id}"

    st.set_page_config(page_title=title, layout="centered")
    st.title(title)


def render_select_box() -> str | None:
    # Renders the labele for the option
    options = [k for k, v in CHAT_OPTIONS.items() if v.active]

    add_radio = st.selectbox(
        label="Choose Chat Mode",
        options=options,
        index=None,
        key="chat_select",
        format_func=lambda k: CHAT_OPTIONS[k].label,
        on_change=handle_chatbot_change,
    )

    return add_radio


def render_chatbot_description():
    if "chat_data" not in st.session_state:
        return

    chat_data: ChatOption = st.session_state.chat_data

    st.subheader(chat_data.label)
    st.write(chat_data.description)

    # --- MODE HANDLING ---
    if chat_data.mode == "file":
        # Always show uploads
        st.session_state.show_file_uploads = True

    elif chat_data.mode == "both":
        toggle_label = (
            "Hide file uploads"
            if st.session_state.show_file_uploads
            else "Attach files"
        )

        if st.button(toggle_label):
            st.session_state.show_file_uploads = not st.session_state.show_file_uploads

    # --- BOTTOM RENDER ---
    if st.session_state.show_file_uploads:
        st.divider()
        render_file_uploads()


def render_file_uploads():
    uploaded_files = st.file_uploader(
        "File upload",
        accept_multiple_files=True,
        type=["jpg", "jpeg", "png"],
        key="file_uploader",
    )

    if uploaded_files:
        logger.info("Current uploaded files %s", uploaded_files)
        
        for f in uploaded_files:
            if f.name not in st.session_state.files:
                st.session_state.files[f.name] = {
                    "bytes": f.getvalue(),
                    "type": f.type,
                    "name": f.name,
                }

            if st.button(f.name, key=f"{f.name}_{st.session_state.thread_id}"):
                if st.session_state.selected_file == f.name:
                    st.session_state.selected_file = None
                else:
                    st.session_state.selected_file = f.name

    selected_name = st.session_state.get("selected_file")
    if selected_name:
        selected = st.session_state.files[selected_name]

        if selected["type"] in IMAGETYPES:
            st.image(selected["bytes"])
        elif selected["type"] in PDFTYPES:
            st.pdf(selected["bytes"])
        else:
            st.markdown(
                f"Cannot display file of type {selected['type']} {selected['name']}"
            )


def handle_chatbot_change():
    selected = st.session_state.chat_select
    if not selected:
        return
    chat_data = CHAT_OPTIONS[selected]
    st.session_state.chat_data = chat_data
    get_new_thread_id()
