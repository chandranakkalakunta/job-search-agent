import os
import chromadb
import wikipediaapi
from PyPDF2 import PdfReader
from google import genai
from tavily import TavilyClient

# ── Configuration ──────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "job_docs"

# ── Initialize clients ─────────────────────────────────────
gemini_client = genai.Client(api_key=GEMINI_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='JobSearchAgent/1.0'
)

# ── Tool 1 — Web Search ────────────────────────────────────
def web_search(query: str) -> str:
    """Search the web for latest job market information"""
    print(f"🌐 Web searching: {query}")
    try:
        results = tavily_client.search(
            query=query,
            max_results=5,
            search_depth="advanced"
        )
        output = []
        for r in results["results"]:
            output.append(f"Source: {r['url']}\n{r['content']}")
        return "\n\n".join(output)
    except Exception as e:
        return f"Web search failed: {str(e)}"

# ── Tool 2 — Wikipedia Search ──────────────────────────────
def wikipedia_search(query: str) -> str:
    """Search Wikipedia for company or technology information"""
    print(f"📚 Wikipedia searching: {query}")
    try:
        page = wiki.page(query)
        if page.exists():
            # Return first 1000 chars to keep it concise
            return f"Wikipedia — {query}:\n{page.summary[:1000]}"
        else:
            # Try search with modified query
            return f"No Wikipedia page found for '{query}'"
    except Exception as e:
        return f"Wikipedia search failed: {str(e)}"

# ── Tool 3 — Ingest PDF ────────────────────────────────────
def ingest_pdf(pdf_path: str, filename: str) -> str:
    """Ingest a PDF document into ChromaDB"""
    print(f"📄 Ingesting PDF: {filename}")
    try:
        # Read PDF
        reader = PdfReader(pdf_path)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"

        # Chunk text
        chunks = []
        chunk_size = 500
        overlap = 50
        start = 0
        while start < len(full_text):
            end = start + chunk_size
            chunk = full_text[start:end]
            if chunk.strip():
                chunks.append(chunk)
            start = end - overlap

        # Setup ChromaDB
        chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        try:
            collection = chroma_client.get_collection(COLLECTION_NAME)
        except:
            collection = chroma_client.create_collection(COLLECTION_NAME)

        # Embed and store
        existing = collection.count()
        for i, chunk in enumerate(chunks):
            response = gemini_client.models.embed_content(
                model="gemini-embedding-001",
                contents=[chunk]
            )
            embedding = response.embeddings[0].values
            collection.add(
                documents=[chunk],
                embeddings=[embedding],
                ids=[f"{filename}_chunk_{existing+i}"],
                metadatas=[{"source": filename}]
            )

        return f"✅ Successfully ingested {filename} ({len(chunks)} chunks, {len(reader.pages)} pages)"
    except Exception as e:
        return f"PDF ingestion failed: {str(e)}"

# ── Tool 4 — Search Documents ──────────────────────────────
def search_documents(query: str) -> str:
    """Search through uploaded PDF documents"""
    print(f"📄 Searching documents: {query}")
    try:
        chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        collection = chroma_client.get_collection(COLLECTION_NAME)

        if collection.count() == 0:
            return "No documents uploaded yet."

        # Embed query
        response = gemini_client.models.embed_content(
            model="gemini-embedding-001",
            contents=[query]
        )
        query_embedding = response.embeddings[0].values

        # Search
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )

        output = []
        for i, doc in enumerate(results["documents"][0]):
            source = results["metadatas"][0][i]["source"]
            output.append(f"From {source}:\n{doc}")

        return "\n\n".join(output)
    except Exception as e:
        return f"Document search failed: {str(e)}"

# ── Test ───────────────────────────────────────────────────
if __name__ == "__main__":
    print("Testing tools...\n")

    # Test web search
    result = web_search("Cloud Architect jobs Hyderabad 2025")
    print("WEB SEARCH RESULT:")
    print(result[:500])
    print("\n" + "="*50 + "\n")

    # Test Wikipedia
    result = wikipedia_search("Infosys")
    print("WIKIPEDIA RESULT:")
    print(result[:500])
