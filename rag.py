"""Course document loading, chunking, Chroma persistence, and retrieval."""
from pathlib import Path
import shutil
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from config import settings

SUPPORTED_TEXT = {".txt", ".md"}

def load_course_documents():
    docs = []
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    for path in sorted(settings.data_dir.iterdir()):
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix == ".pdf":
            loaded = PyPDFLoader(str(path)).load()
        elif suffix in SUPPORTED_TEXT:
            loaded = TextLoader(str(path), encoding="utf-8", autodetect_encoding=True).load()
        else:
            continue
        for doc in loaded:
            doc.metadata["source"] = str(path.relative_to(settings.data_dir))
        docs.extend(loaded)
    if not docs:
        raise FileNotFoundError(
            f"No PDF, TXT, or MD course files found directly in {settings.data_dir}. "
            "Place your syllabus/notes in the project root folder."
        )
    return docs

def get_embeddings():
    return OllamaEmbeddings(model=settings.embedding_model, base_url=settings.ollama_base_url)

def build_vector_store(force_rebuild=False):
    if force_rebuild and settings.chroma_dir.exists():
        shutil.rmtree(settings.chroma_dir)
    docs = load_course_documents()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=850,
        chunk_overlap=160,
        separators=["\\n## ", "\\n### ", "\\n\\n", "\\n", ". ", " ", ""],
        add_start_index=True,
    )
    chunks = splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        persist_directory=str(settings.chroma_dir),
        collection_name="course_material",
    )
    return vectorstore

def get_vector_store():
    if not settings.chroma_dir.exists() or not any(settings.chroma_dir.iterdir()):
        return build_vector_store()
    return Chroma(
        persist_directory=str(settings.chroma_dir),
        embedding_function=get_embeddings(),
        collection_name="course_material",
    )

def get_retriever():
    return get_vector_store().as_retriever(search_type="similarity", search_kwargs={"k": 4})

def retrieve_course_material(question: str) -> str:
    """Return relevant passages from the student's indexed syllabus, notes, or textbook."""
    docs = get_retriever().invoke(question)
    if not docs:
        return "No matching course passages were retrieved."
    return "\n\n".join(
        f"[Source: {d.metadata.get('source', 'course material')} | page: {d.metadata.get('page', 'n/a')}]\n{d.page_content}"
        for d in docs
    )

def test_retriever():
    """Run one narrow factual and one broad conceptual retrieval check."""
    retriever = get_retriever()
    questions = [
        "What is a text splitter?",
        "Explain how Retrieval-Augmented Generation (RAG) works and why retrieval is useful.",
    ]
    for question in questions:
        print(f"\\nQUESTION: {question}")
        for doc in retriever.invoke(question):
            print(f"- {doc.metadata.get('source', 'unknown')}: {doc.page_content[:260].replace(chr(10), ' ')}...")

if __name__ == "__main__":
    test_retriever()
