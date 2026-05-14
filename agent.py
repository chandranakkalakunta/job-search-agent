import os
from google import genai
from tools import web_search, wikipedia_search, search_documents
import json

# ── Configuration ──────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# ── Agent System Prompt ────────────────────────────────────
SYSTEM_PROMPT = """You are an expert AI Job Search Assistant 
specializing in Cloud, AI/ML, and technology roles in India, 
particularly Hyderabad.

You have access to three tools:
1. web_search — Search the web for latest job market info,
   company news, salary data, job openings
2. wikipedia_search — Get background info on companies 
   or technologies
3. search_documents — Search through user's uploaded 
   documents (resume, certifications, study materials)

DECISION RULES for which tools to use:
- Job openings, salaries, market trends → web_search
- Company background, tech definitions → wikipedia_search  
- User's resume, certifications → search_documents
- Complex questions → use MULTIPLE tools and combine!

Always:
- Cite your sources
- Be specific to Indian/Hyderabad job market when relevant
- Give actionable, practical advice
- Mention specific companies, roles, and salaries when available
"""

# ── Core Agent Function ────────────────────────────────────
def run_agent(question: str, chat_history: list = []) -> dict:
    """
    Agent that decides which tools to use and synthesizes answer
    Returns dict with answer and sources used
    """
    sources_used = []

    # Step 1 — Ask Gemini which tools to use
    planning_prompt = f"""
{SYSTEM_PROMPT}

User Question: {question}

First, decide which tools to use. Respond with JSON only:
{{
    "tools_needed": ["web_search", "wikipedia_search", 
                     "search_documents"],
    "web_query": "specific search query for web",
    "wiki_query": "specific search query for wikipedia",
    "doc_query": "specific search query for documents",
    "reasoning": "why these tools"
}}

Only include tools that are actually needed.
"""

    planning_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=planning_prompt
    )

    # Parse tool plan
    plan_text = planning_response.text.strip()
    plan_text = plan_text.replace("```json", "").replace("```", "").strip()

    try:
        plan = json.loads(plan_text)
    except:
        # Fallback — use web search if parsing fails
        plan = {
            "tools_needed": ["web_search"],
            "web_query": question,
            "reasoning": "fallback to web search"
        }

    print(f"🧠 Agent plan: {plan['reasoning']}")
    print(f"🔧 Tools: {plan['tools_needed']}")

    # Step 2 — Execute tools based on plan
    tool_results = []

    if "web_search" in plan["tools_needed"]:
        query = plan.get("web_query", question)
        result = web_search(query)
        tool_results.append(f"WEB SEARCH RESULTS:\n{result}")
        sources_used.append(f"🌐 Web: {query}")

    if "wikipedia_search" in plan["tools_needed"]:
        query = plan.get("wiki_query", question)
        result = wikipedia_search(query)
        tool_results.append(f"WIKIPEDIA RESULTS:\n{result}")
        sources_used.append(f"📚 Wikipedia: {query}")

    if "search_documents" in plan["tools_needed"]:
        query = plan.get("doc_query", question)
        result = search_documents(query)
        tool_results.append(f"DOCUMENT RESULTS:\n{result}")
        sources_used.append(f"📄 Your Documents: {query}")

    # Step 3 — Synthesize final answer
    context = "\n\n".join(tool_results)

    synthesis_prompt = f"""
{SYSTEM_PROMPT}

User Question: {question}

Information gathered from tools:
{context}

Now provide a comprehensive, well-structured answer.
Be specific, practical and actionable.
Cite sources where relevant.
Focus on Hyderabad/India market when applicable.
"""

    final_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=synthesis_prompt
    )

    return {
        "answer": final_response.text,
        "sources": sources_used,
        "tools_used": plan["tools_needed"],
        "reasoning": plan["reasoning"]
    }

# ── Test ───────────────────────────────────────────────────
if __name__ == "__main__":
    print("🤖 Testing Job Search Agent\n")
    print("="*50)

    question = "What are the top companies hiring \
Cloud Architects in Hyderabad right now?"

    result = run_agent(question)

    print(f"\n💡 ANSWER:\n{result['answer']}")
    print(f"\n📚 SOURCES USED: {result['sources']}")
    print(f"\n🔧 TOOLS USED: {result['tools_used']}")
