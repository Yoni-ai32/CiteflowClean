from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# allow the Streamlit app to call the API (cross-origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API is live"}

@app.get("/health")
def health():
    return {"ok": True}

# very simple prototype formatter (APA-like and Vancouver-like)
def format_apa(authors: str, year: str, title: str, journal: str, volume: str, issue: str, pages: str, doi_or_url: str):
    bits = []
    if authors: bits.append(authors.strip())
    bits.append(f"({year.strip() or 'n.d.'}).")
    bits.append(title.strip())
    if journal: bits.append(journal.strip())
    vol_issue = ""
    if volume: vol_issue += volume.strip()
    if issue: vol_issue += f"({issue.strip()})"
    if vol_issue: bits.append(vol_issue)
    if pages: bits.append(pages.strip())
    if doi_or_url: bits.append(doi_or_url.strip())
    return " ".join(bits)

def format_vancouver(authors: str, year: str, title: str, journal: str, volume: str, issue: str, pages: str, doi_or_url: str):
    bits = []
    if authors: bits.append(authors.strip() + ".")
    bits.append(title.strip())
    if journal: bits.append(journal.strip())
    if year: bits.append(year.strip())
    vi = ""
    if volume: vi += volume.strip()
    if issue: vi += f"({issue.strip()})"
    if vi: bits.append(vi)
    if pages: bits.append(pages.strip())
    if doi_or_url: bits.append(doi_or_url.strip())
    return " ".join(bits)

@app.post("/format")
def format_reference(
    style: str = Form(...),
    authors: str = Form("Smith, J.; Doe, A."),
    year: str = Form("2020"),
    title: str = Form("Example article title"),
    journal: str = Form("Journal of Things"),
    volume: str = Form("12"),
    issue: str = Form("3"),
    pages: str = Form("45-50"),
    doi_or_url: str = Form("https://doi.org/10.1000/xyz123"),
):
    style = style.lower().strip()
    if style in ["apa", "apa7", "apa-7"]:
        out = format_apa(authors, year, title, journal, volume, issue, pages, doi_or_url)
    else:
        out = format_vancouver(authors, year, title, journal, volume, issue, pages, doi_or_url)
    return {"formatted": out}
