from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

# === Step 1: Setup Embeddings ===
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# === Step 2: Load Vector Store ===
vectordb = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)

# === Step 3: Test Search ===
retriever = vectordb.as_retriever(search_kwargs={"k": 5})
query = "What does section 511 say?"
results = retriever.invoke(query)  # invoke is now the recommended API

# === Step 4: Show Results ===
print("\n==== Retrieved Chunks ====")
for i, doc in enumerate(results):
    print(f"\n📄 Result {i+1}")
    print(f"Section: {doc.metadata.get('section', 'N/A')}")
    print(f"Chunk #: {doc.metadata.get('chunk', 'N/A')}")
    print(doc.page_content[:300] + "...")
