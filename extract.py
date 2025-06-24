import fitz  # PyMuPDF
import re

def clean_text(text):
    text = text.replace("-\n", "")  # Remove hyphenated line breaks
    text = text.replace("\n", " ")  # Flatten line breaks
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    return text.strip()

def is_italic(span):
    # Check if font flags indicate italic (2 is the italic flag in MuPDF)
    return (span.get("flags", 0) & 2) != 0

def extract_sections_from_pdf(pdf_path, start_page=21):
    doc = fitz.open(pdf_path)
    full_text_parts = []

    for page_num in range(start_page, len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    if not text:
                        continue

                    if is_italic(span) and text.lower().startswith("of "):
                        continue  # skip italic headings like "Of Hijacking"
                    full_text_parts.append(text)

    full_text = clean_text(" ".join(full_text_parts))

    # Improved regex to match section numbers like 302., 402A., 10-B.
    pattern = re.compile(r'\b(\d{1,4}(?:[A-Z]{0,2}|-[A-Z]{1,2})?)\. (?=[A-Z\[])')

    parts = pattern.split(full_text)

    sections = []
    for i in range(1, len(parts), 2):
        section_num = parts[i]
        section_text = parts[i + 1].strip()
        full_section = f"{section_num}. {section_text}"

        if not section_text or len(section_text) < 30:
            continue

        sections.append({
            "section": section_num,
            "text": full_section,
            "page_estimate": start_page + (i // 2)
        })

    return sections
