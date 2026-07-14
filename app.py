import uuid
import streamlit as st
import streamlit.components.v1 as components
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Feng", page_icon="🎓", layout="wide")

TITLE_MAX_LEN = 30  # how many characters of the first message to show as chat title


# ---------------------------------------------------------------------------
# Model (cached so it's only created once per server process, not per rerun)
# ---------------------------------------------------------------------------
@st.cache_resource
def get_model():
    return ChatGroq(model="llama-3.3-70b-versatile")


model = get_model()

def _new_chat() -> str:
    """Create a fresh chat, make it current, and return its id."""
    chat_id = str(uuid.uuid4())
    st.session_state.chats[chat_id] = {
        "title": "New Chat",
        "messages": [],
    }
    st.session_state.current_chat_id = chat_id
    return chat_id


if "chats" not in st.session_state:
    st.session_state.chats = {}
    st.session_state.current_chat_id = None

if not st.session_state.chats:
    # First-ever load: create an initial empty chat so the UI isn't blank.
    _new_chat()


def get_current_messages():
    """Return the message list for the chat currently open."""
    return st.session_state.chats[st.session_state.current_chat_id]["messages"]


def make_title(text: str) -> str:
    """Turn a user's first message into a short sidebar label."""
    text = text.strip().replace("\n", " ")
    if len(text) <= TITLE_MAX_LEN:
        return text
    return text[:TITLE_MAX_LEN].rstrip() + "..."


# ---------------------------------------------------------------------------
# Sidebar: New Chat button + Recent Chats list + Clear Conversation
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("More")

    if st.button("➕ New Chat", use_container_width=True):
        _new_chat()
        st.rerun()

    st.markdown("---")
    st.subheader("Recent Chats")

    for chat_id in reversed(list(st.session_state.chats.keys())):
        chat = st.session_state.chats[chat_id]
        is_current = chat_id == st.session_state.current_chat_id

        col_select, col_delete = st.columns([5, 1])
 
        with col_select:
            button_label = f"💬 {chat['title']}"
            if st.button(
                button_label,
                key=f"select_{chat_id}",
                use_container_width=True,
                type="primary" if is_current else "secondary",  # highlight active chat
            ):
                st.session_state.current_chat_id = chat_id
                st.rerun()
 
        with col_delete:
            if st.button("✕", key=f"delete_{chat_id}", use_container_width=True):
                del st.session_state.chats[chat_id]
 
                if is_current:
                    if st.session_state.chats:
                        st.session_state.current_chat_id = list(st.session_state.chats.keys())[-1]
                    else:
                        _new_chat()
                st.rerun()
 
    st.markdown("---")
    # Clear Conversation only affects the chat currently open, exactly like
    # the original behaviour, just scoped to the active chat_id now.
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        current_id = st.session_state.current_chat_id
        st.session_state.chats[current_id]["messages"] = []
        st.session_state.chats[current_id]["title"] = "New Chat"
        st.rerun()


# ---------------------------------------------------------------------------
# Main chat window
# ---------------------------------------------------------------------------
st.title("Chat one!")

messages = get_current_messages()

# Render full history (system message is intentionally not shown to the user)
for msg in messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# An empty anchor element placed after the last message. The auto-scroll
# script below scrolls this element into view, which lands the viewport
# at the bottom of the conversation.
st.markdown('<div id="chat-bottom-anchor"></div>', unsafe_allow_html=True)

prompt = st.chat_input("Ask your AI teacher something...")

if prompt:
    # If this is the first user message in the chat, derive the sidebar title
    is_first_message = not any(isinstance(m, HumanMessage) for m in messages)

    # Store + display the user's message
    messages.append(HumanMessage(content=prompt))
    if is_first_message:
        st.session_state.chats[st.session_state.current_chat_id]["title"] = make_title(prompt)

    with st.chat_message("user"):
        st.markdown(prompt)

    # Get and display the assistant's reply
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = model.invoke(messages)  # full history gives conversational memory
            st.markdown(answer.content)

    messages.append(AIMessage(content=answer.content))


    st.rerun()


# ---------------------------------------------------------------------------
# Auto-scroll to the latest message.
# ---------------------------------------------------------------------------
components.html(
    """
    <script>
        function scrollChatToBottom(retries) {
            const doc = window.parent.document;
            const anchor = doc.getElementById("chat-bottom-anchor");
            if (anchor) {
                anchor.scrollIntoView({behavior: "smooth", block: "end"});
            } else if (retries > 0) {
                // The anchor may not be mounted yet on first paint; retry briefly.
                setTimeout(() => scrollChatToBottom(retries - 1), 100);
            }
        }
        scrollChatToBottom(10);
    </script>
    """,
    height=0,
)
