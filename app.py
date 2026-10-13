import streamlit as st
from agent import build_agent
from config import settings

st.set_page_config(page_title="Study & Career Companion", page_icon="🎓", layout="wide")
st.title("🎓 Personalized Learning & Career Agent")
st.caption("Ask questions grounded in your course material, find learning resources, or search for entry-level opportunities.")

with st.sidebar:
    st.header("Setup")
    st.write(f"**Ollama model:** `{settings.ollama_model}`")
    st.write(f"**Course folder:** `{settings.data_dir}`")
    st.info("Add PDFs or TXT/MD course files directly to the project root folder, then click Rebuild course index.")
    if st.button("Rebuild course index", use_container_width=True):
        from rag import build_vector_store
        with st.spinner("Reading course material and rebuilding Chroma index..."):
            build_vector_store(force_rebuild=True)
        st.success("Course index rebuilt.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Example: Explain RAG simply / Find Python internships")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking and checking the appropriate sources..."):
            try:
                agent = build_agent()
                result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
                answer = result["messages"][-1].content
                if isinstance(answer, list):
                    answer = "\n".join(str(part.get("text", part)) if isinstance(part, dict) else str(part) for part in answer)
                st.markdown(answer)
            except Exception as exc:
                answer = (
                    f"**Could not run the agent:** `{exc}`\n\n"
                    "Check that Ollama is running, the model is pulled, dependencies are installed, "
                    "and course files (for example, `course_notes.txt`) are present in the project root folder."
                )
                st.error(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
