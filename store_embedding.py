from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from extract import extract_sections_from_pdf
from tqdm import tqdm

# === Config ===
pdf_path = Path("E:/legal/panelcode.pdf")
persist_dir = Path("chroma_db")
persist_dir.mkdir(parents=True, exist_ok=True)

# === Step 1: Extract PDF Sections ===
sections = extract_sections_from_pdf(str(pdf_path))

# === Step 2: Setup Embedding Model ===
embedding_model = HuggingFaceEmbeddings(
    model_name="intfloat/e5-base-v2",
    encode_kwargs={"normalize_embeddings": True}
)

# === Step 3: Text Splitter for long sections only ===
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)

# === Step 4: Chunk + Embed with Prefixes ===
texts = []
metadatas = []

for sec in tqdm(sections, desc="📖 Processing sections"):
    section_id = str(sec.get("section", "unknown")).strip().lower()
    section_text = sec["text"].strip()
    page_estimate = sec.get("page_estimate", None)

    # Split only if section is long
    chunks = text_splitter.split_text(section_text) if len(section_text) > 1500 else [section_text]

    for i, chunk in enumerate(chunks):
        formatted_chunk = f"passage: {chunk.strip()}"  # Required by e5 models
        texts.append(formatted_chunk)
        metadatas.append({
            "section": section_id,
            "chunk": i,
            "page_estimate": page_estimate
        })

# === Step 5: Store in Chroma Vector DB ===
vectordb = Chroma.from_texts(
    texts=texts,
    embedding=embedding_model,
    metadatas=metadatas,
    persist_directory=str(persist_dir)
)
vectordb.persist()

print(f"✅ Stored {len(texts)} chunks into ChromaDB at '{persist_dir}'.")