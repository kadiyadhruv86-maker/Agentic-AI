"""General internet search tool for current external information and source links."""
from langchain_core.tools import tool
from ddgs import DDGS

@tool
def search_the_web(query: str) -> str:
    """Search the public internet for current information, explanations, tutorials, documentation, and source URLs. Use this for general web research, not for questions that should be answered only from the student's course notes and not as a replacement for the dedicated jobs/internships search tool."""
    query = query.strip()
    if not query:
        return "Please provide a search query."
    try:
        results = DDGS().text(query, max_results=6)
        if not results:
            return f"No web results found for: {query}. Try different keywords."
        lines = [f"Web search results for: **{query}**"]
        for index, item in enumerate(results, start=1):
            title = item.get("title", "Untitled result")
            url = item.get("href", "")
            snippet = item.get("body", "No preview available.")
            lines.append(f"\n{index}. **{title}**\n   - Summary: {snippet}\n   - Source: {url}")
        lines.append("\nUse these as search leads: open the original source to verify details, date, and reliability before relying on them.")
        return "\n".join(lines)
    except Exception as exc:
        return (f"Web search failed: {exc}. Check the internet connection and try again. "
                "The search service may also be temporarily unavailable.")
