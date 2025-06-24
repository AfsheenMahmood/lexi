from extract import extract_sections_from_pdf

sections = extract_sections_from_pdf("E:/legal/panelcode.pdf")

print(f"Extracted {len(sections)} sections.\n")
for section in sections[:500]:
    print(f"Section: {section['section']}")
    print(section['text'][:500], "...")
    print("-" * 40)