import streamlit as st
from core import client
from .async_wrappers import run_async
import base64


async def get_thread_id():
    return await client.threads.create()


def initialize_thread_id() -> str:
    if "thread_id" not in st.session_state:
        thread = run_async(get_thread_id())
        st.session_state.thread_id = thread["thread_id"]
    return st.session_state.thread_id


async def stream_langgraph(messages, thread_id: str | None, assistant_id: str):
    async for chunk in client.runs.stream(
        thread_id,
        assistant_id=assistant_id,
        input={"messages": messages},
        stream_mode="updates",
    ):
        if chunk.event != "updates":
            continue
        model_data = chunk.data.get("model")
        if not model_data:
            continue
        messages_list = model_data.get("messages", [])

        if not messages_list:
            continue
        last_msg = messages_list[-1]
        # print("Last message in stream", last_msg)
        if last_msg:
            yield last_msg


def send_message(prompt: str):
    image_payload = []
    ai_message = []
    files = st.session_state.files
    if not prompt:
        return
    st.chat_message("user").markdown(prompt)

    if files:
        for _, f in files.items():
            file_bytes = f.getvalue()
            image_data = base64.b64encode(file_bytes).decode("utf-8")
            mime_type = f.type
            image_payload.append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime_type};base64,{image_data}"},
                }
            )
    default_message = {"role": "user", "content": prompt}
    if len(image_payload) > 0:
        ai_message = {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                *image_payload,
            ],
        }
    else:
        ai_message = default_message
    st.session_state.messages.append(default_message)
    assistant_box = st.chat_message("assistant")
    placeholder = assistant_box.empty()
    tool_placeholder = assistant_box.container()

    # Reset files
    files = st.session_state.files = {}

    async def consume():
        buffer = ""
        tool_calls_rendered = set()
        thread_id = None
        if "thread_id" in st.session_state:
            thread_id = st.session_state.thread_id

        async for token in stream_langgraph(
            [ai_message],
            thread_id,
            st.session_state.chat_data.url,
        ):
            content = token.get("content")
            if content:
                buffer += content
                placeholder.markdown(buffer)
            tool_calls = token.get("tool_calls")
            if tool_calls:
                for call in tool_calls:
                    call_id = call.get("id")
                    if call_id in tool_calls_rendered:
                        continue
                    tool_calls_rendered.add(call_id)
                    with tool_placeholder:
                        with st.expander(
                            f"Tool call: `{call['name']}`", expanded=False
                        ):
                            st.json(call["args"])
            st.session_state.messages.append({"role": "assistant", "content": buffer})


    run_async(consume())
