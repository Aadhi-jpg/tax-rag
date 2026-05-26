import requests
from bs4 import BeautifulSoup
import os
import time

CBIC_URL = "https://www.cbic.gov.in/htdocs-cbec/gst/notfctn-lst-gst.htm"
IT_URL = "https://www.incometax.gov.in/iec/foportal/help/rules-regulations-and-other-statutory-references/circulars-1"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

def scrape_cbic():
    print("Scraping CBIC...")
    try:
        response = requests.get(CBIC_URL, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", href=True)
        pdf_links = [
            "https://www.cbic.gov.in" + a["href"]
            for a in links
            if a["href"].endswith(".pdf")
        ]
        print(f"Found {len(pdf_links)} PDF links on CBIC")
        return pdf_links
    except Exception as e:
        print(f"CBIC scrape failed: {e}")
        return []

def scrape_it_dept():
    print("Scraping Income Tax dept...")
    try:
        response = requests.get(IT_URL, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", href=True)
        pdf_links = [
            a["href"] for a in links
            if a["href"].endswith(".pdf")
        ]
        print(f"Found {len(pdf_links)} PDF links on IT dept")
        return pdf_links
    except Exception as e:
        print(f"IT dept scrape failed: {e}")
        return []
if __name__ == "__main__":
    cbic_links = scrape_cbic()
    it_links = scrape_it_dept()
    print("\nTotal PDFs found:", len(cbic_links) + len(it_links))
    print("\nIT dept links found:")
    for link in it_links:
        print(link)