import fitz  #pymypdf

#extract metadata from a PDF file using pymupdf
#returns a dict with keys: title, author, keywords, summary, created_at
def extract_pdf_metadata(filepath: str) -> dict:
    doc = fitz.open(filepath)

    meta = doc.metadata
    #meta keys: 'title', 'author', 'subject', 'keywords', 'creationDate', etc
    summary_value = meta.get("summary")
    if summary_value:
        summary = summary_value
    else:
        summary = "None"

    #parse creation date from meta if available
    created_at = None
    if meta.get("creationDate"):
        try:
            #pymupdf creationDate format example: "D:20210807123000Z"
            from datetime import datetime
            date_str = meta["creationDate"]
            #clean string to parse, remove prefix 'D:' and 'Z' suffix
            if date_str.startswith("D:"):
                date_str = date_str[2:]
            if date_str.endswith("Z"):
                date_str = date_str[:-1]

            created_at = datetime.strptime(date_str, "%Y%m%d%H%M%S")
        except Exception:
            created_at = None

    full_text = ""
    for page in doc:
        full_text += page.get_text()
    
    doc.close()

    return {
        "title": meta.get("title") or "Unknown",
        "author": meta.get("author") or "Unknown",
        "keywords": meta.get("keywords").split(",") if meta.get("keywords") else ["None"],
        "summary":summary,
        "created_at": created_at,
        "full_text": full_text.strip() 
    }
