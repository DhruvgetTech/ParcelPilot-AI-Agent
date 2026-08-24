from pathlib import Path
from pypdf import PdfReader

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_pdf_text():
    documents = []

    pdf_files = list(DATA_DIR.glob("*.pdf"))

    for pdf_file in pdf_files:
        try:
            reader = PdfReader(pdf_file)

            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            documents.append({
                "filename": pdf_file.name,
                "content": text
            })

            print(f"Loaded: {pdf_file.name}")

        except Exception as e:
            print(f"Error reading {pdf_file.name}: {e}")

    return documents


if __name__ == "__main__":
    docs = load_pdf_text()

    print(f"\nTotal PDFs loaded: {len(docs)}")

    for doc in docs:
        print("\n" + "=" * 60)
        print(doc["filename"])
        print(doc["content"][:500])