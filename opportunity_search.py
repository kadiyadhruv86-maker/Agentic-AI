"""External opportunity search. Adzuna is used when API credentials are configured."""
import requests
from langchain_core.tools import tool
from config import settings

def _search_adzuna(topic: str, location: str, results: int):
    url = f"https://api.adzuna.com/v1/api/jobs/{settings.country}/search/1"
    params = {
        "app_id": settings.adzuna_app_id,
        "app_key": settings.adzuna_app_key,
        "what": topic,
        "where": location or "India",
        "results_per_page": results,
        "content-type": "application/json",
    }
    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    data = response.json()
    found = []
    for item in data.get("results", []):
        title = item.get("title", "Untitled role")
        company = (item.get("company") or {}).get("display_name", "Company not listed")
        description = (item.get("description") or "").strip()
        found.append({
            "title": title,
            "company": company,
            "location": (item.get("location") or {}).get("display_name", location or "Not specified"),
            "url": item.get("redirect_url", ""),
            "description": description[:500],
            "source": "Adzuna",
        })
    return found

def _search_remotive(topic: str, results: int):
    # Public API fallback; mostly remote roles, and availability/eligibility varies by listing.
    response = requests.get(
        "https://remotive.com/api/remote-jobs",
        params={"search": topic, "limit": results},
        timeout=20,
        headers={"User-Agent": "PersonalizedLearningCareerAgent/1.0"},
    )
    response.raise_for_status()
    data = response.json()
    found = []
    for item in data.get("jobs", []):
        found.append({
            "title": item.get("title", "Untitled role"),
            "company": item.get("company_name", "Company not listed"),
            "location": item.get("candidate_required_location", "Remote location not specified"),
            "url": item.get("url", ""),
            "description": (item.get("description") or "").replace("<br>", " ")[:500],
            "source": "Remotive",
        })
    return found

def search_opportunities(topic: str, location: str = "India", results: int = 6) -> str:
    topic = topic.strip()
    if not topic:
        return "Please provide a study topic or role keyword, such as Python, networking, or data analysis."
    try:
        if settings.adzuna_app_id and settings.adzuna_app_key:
            items = _search_adzuna(topic, location, results)
        else:
            items = _search_remotive(topic, results)
    except Exception as exc:
        return (
            f"Opportunity search failed: {exc}. "
            "Check your internet connection/API credentials, then try again."
        )
    if not items:
        return f"No listings matched '{topic}' in the current search. Try a broader keyword."
    output = [f"External opportunity results for **{topic}** (source: {items[0]['source']}):"]
    for i, item in enumerate(items, 1):
        output.append(
            f"\n{i}. **{item['title']}** — {item['company']}\n"
            f"   - Location: {item['location']}\n"
            f"   - Why it may match: the listing was returned for the search topic **{topic}**. "
            "Check its requirements and responsibilities to confirm fit.\n"
            f"   - Summary: {item['description'] or 'No description provided.'}\n"
            f"   - Apply/details: {item['url']}"
        )
    output.append("\nListings can expire or change. Check eligibility, experience level, location, and the original listing before applying.")
    return "\n".join(output)

@tool
def find_jobs_and_internships(topic: str, location: str = "India") -> str:
    """Search EXTERNAL job and internship listings matching a student's study topic, e.g. Python, IT support, or data analysis. Use this for opportunities, not for explaining course concepts."""
    return search_opportunities(topic, location)
