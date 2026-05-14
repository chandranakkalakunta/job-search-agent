import streamlit as st
import tempfile
import os
from agent import run_agent
from tools import ingest_pdf

# ── Page Config ────────────────────────────────────────────
st.set_page_config(
    page_title="AI Job Search Agent",
    page_icon="🤖",
    layout="wide"
)

# ── Header ─────────────────────────────────────────────────
st.title("🤖 AI Job Search Agent")
st.caption("Your personal career intelligence assistant — searches web, Wikipedia, and your documents!")

# ── Sidebar — Document Upload ──────────────────────────────
with st.sidebar:
    st.header("📄 Your Documents")
    st.caption("Upload your resume, certifications, or any career documents")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type="pdf"
    )

    if uploaded_file:
        if st.button("📥 Ingest Document", type="primary"):
            with st.spinner("Processing document..."):
                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=".pdf"
                ) as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name

                result = ingest_pdf(tmp_path, uploaded_file.name)
                os.unlink(tmp_path)

            if "✅" in result:
                st.success(result)
                if "uploaded_docs" not in st.session_state:
                    st.session_state.uploaded_docs = []
                st.session_state.uploaded_docs.append(
                    uploaded_file.name
                )
            else:
                st.error(result)

    # Show uploaded docs
    if st.session_state.get("uploaded_docs"):
        st.divider()
        st.markdown("**📚 Ingested Documents:**")
        for doc in st.session_state.uploaded_docs:
            st.markdown(f"✅ {doc}")

    st.divider()

    # ── Tool Info ──────────────────────────────────────────
    st.markdown("**🔧 Available Tools:**")
    st.markdown("🌐 Web Search — live job market data")
    st.markdown("📚 Wikipedia — company backgrounds")
    st.markdown("📄 Your Docs — resume & certifications")

    st.divider()
    st.caption("Built with Google Gemini + LangChain + Tavily")

# ── Main Chat Interface ────────────────────────────────────
st.subheader("💬 Ask Me Anything About Your Job Search")

# Example questions
with st.expander("💡 Example Questions"):
    st.markdown("""
    - What companies in Hyderabad are hiring Cloud Architects?
    - What is the average salary for ML Engineers in India?
    - Tell me about Infosys AI strategy and open roles
    - What skills are most in demand for AI roles in 2025?
    - Compare my resume against current market demands
    - What certifications should I get for GCP roles?
    - Latest trends in enterprise AI adoption in India
    """)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander("📚 Sources Used"):
                for source in message["sources"]:
                    st.markdown(f"- {source}")
        if message.get("tools"):
            cols = st.columns(len(message["tools"]))
            for i, tool in enumerate(message["tools"]):
                icon = {"web_search": "🌐",
                        "wikipedia_search": "📚",
                        "search_documents": "📄"}.get(tool, "🔧")
                cols[i].caption(f"{icon} {tool}")

# Chat input
if question := st.chat_input(
    "Ask about jobs, companies, salaries, skills..."
):
    # Show user message
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("🤖 Agent thinking and searching..."):
            result = run_agent(question)

        st.markdown(result["answer"])

        # Show sources
        if result["sources"]:
            with st.expander("📚 Sources Used"):
                for source in result["sources"]:
                    st.markdown(f"- {source}")

        # Show tools used as badges
        if result["tools_used"]:
            tool_icons = {
                "web_search": "🌐 Web",
                "wikipedia_search": "📚 Wikipedia",
                "search_documents": "📄 Your Docs"
            }
            cols = st.columns(len(result["tools_used"]))
            for i, tool in enumerate(result["tools_used"]):
                cols[i].caption(tool_icons.get(tool, tool))

    # Save to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sources": result["sources"],
        "tools": result["tools_used"]
    })
