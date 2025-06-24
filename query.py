import re
import logging
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

# === Logging Setup ===
logger = logging.getLogger(__name__)

# === Load Vector DB & Embedding Model ===
def initialize_vectordb(persist_directory="chroma_db"):
    embedding_model = HuggingFaceEmbeddings(
        model_name="intfloat/e5-base-v2",
        encode_kwargs={"normalize_embeddings": True}
    )
    return Chroma(persist_directory=persist_directory, embedding_function=embedding_model)

vectordb = initialize_vectordb()

# === LLM ===
def get_llm(api_key: str):
    return ChatOpenAI(
        model_name="deepseek/deepseek-r1:free",
        temperature=0.3,
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1"
    )

import os
api_key = os.getenv("OPENROUTER_API_KEY")
llm = get_llm(api_key)

# === Prompt Template ===
def build_prompt(context: str, question: str) -> str:
    return f"""You are a legal assistant trained on the Pakistan Penal Code.
Use ONLY the sections below to answer.
If nothing is relevant, reply: 'No relevant section found in Pakistan Penal Code.'

---
LAW EXTRACTS:
{context or 'None'}
---

Question: {question.strip()}
Answer:"""

# === Main Function ===
def query_law(question: str) -> dict:
    normalized_question = question.strip().lower()
    search_query = f"query: {normalized_question}"

    # Extract section number if mentioned
    match = re.search(r'\b(?:section|sec|s\.?)\s*([\d]+[a-zA-Z\-]*)', normalized_question)
    section_ref = match.group(1).lower() if match else None
    logger.debug(f"[DEBUG] Parsed section ID: {section_ref or 'None'}")

    # Step 1: Vector Search
    docs = vectordb.similarity_search_with_score(search_query, k=10)

    if not docs:
        return {
            "result": "No relevant section found in Pakistan Penal Code.",
            "source_documents": []
        }

    # Step 2: Score thresholding
    filtered = [(doc, score) for doc, score in docs if score < 0.35]
    filtered_docs = [doc for doc, _ in filtered] or [doc for doc, _ in docs[:3]]  # fallback if none pass

    # Step 3: Prioritize by section if matched
    if section_ref:
        section_matches = [doc for doc in filtered_docs if section_ref in doc.metadata.get("section", "").lower()]
        final_docs = section_matches + [doc for doc in filtered_docs if doc not in section_matches]
    else:
        final_docs = filtered_docs

    # Step 4: Prompt the LLM
    context = "\n\n".join(doc.page_content for doc in final_docs[:4])
    prompt = build_prompt(context, question)

    try:
        response = llm.invoke(prompt)
        return {
            "result": response.content.strip(),
            "source_documents": final_docs[:4]
        }
    except Exception as e:
        logger.exception("LLM invocation failed.")
        return {
            "result": f"❌ LLM Error: {e}",
            "source_documents": []
        }

# === Example Usage ===
if __name__ == "__main__":
    user_question = input("Enter your legal question: ")
    result = query_law(user_question)

    print("\n📘 Answer:")
    print(result["result"])
    print("\n📎 Source Documents Used:")
    for i, doc in enumerate(result["source_documents"], 1):
        print(f"--- Document {i} ---")
        print(doc.page_content[:300], "...\n")
