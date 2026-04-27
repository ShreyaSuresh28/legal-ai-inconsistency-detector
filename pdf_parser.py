from pypdf import PdfReader

def extract_clauses(pdf_file):
    reader = PdfReader(pdf_file)

    clauses = []
    pages = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()

        if text:
            pages.append((i, text))

            for line in text.split("\n"):
                if len(line.strip()) > 40:
                    clauses.append({
                        "page": i,
                        "clause": line.strip()
                    })

    return clauses, pages
