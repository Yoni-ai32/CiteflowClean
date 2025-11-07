import streamlit as st
import requests

st.set_page_config(page_title="Referencer Prototype", layout="centered")
st.title("🔧 Referencer – Prototype")

api_base = st.sidebar.text_input("API base URL", "https://YOUR-API.onrender.com")

st.caption("Enter the fields below, choose a style, and click **Format**.")

col1, col2 = st.columns(2)
with col1:
    authors = st.text_input("Authors (e.g., Smith, J.; Doe, A.)", "Smith, J.; Doe, A.")
    year = st.text_input("Year", "2020")
    title = st.text_input("Title", "Example article title")
    journal = st.text_input("Journal", "Journal of Things")
with col2:
    volume = st.text_input("Volume", "12")
    issue = st.text_input("Issue", "3")
    pages = st.text_input("Pages", "45-50")
    doi_or_url = st.text_input("DOI/URL", "https://doi.org/10.1000/xyz123")

style = st.radio("Style", ["APA", "Vancouver"], horizontal=True)

if st.button("Format"):
    try:
        data = {
            "style": "apa" if style.lower().startswith("apa") else "vancouver",
            "authors": authors,
            "year": year,
            "title": title,
            "journal": journal,
            "volume": volume,
            "issue": issue,
            "pages": pages,
            "doi_or_url": doi_or_url,
        }
        r = requests.post(f"{api_base}/format", data=data, timeout=15)
        r.raise_for_status()
        st.subheader("Result")
        st.code(r.json().get("formatted", ""), language="text")
    except Exception as e:
        st.error(f"Could not reach API: {e}")
