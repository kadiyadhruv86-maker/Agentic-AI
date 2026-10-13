"""LangChain tool that retrieves passages from indexed course documents."""
from langchain_core.tools import tool
from rag import retrieve_course_material

@tool
def retrieve_course_content(question: str) -> str:
    """Retrieve relevant passages from the student's syllabus, lecture notes, or textbook. Use this to answer course questions grounded in provided material, not to search for jobs."""
    return retrieve_course_material(question)
