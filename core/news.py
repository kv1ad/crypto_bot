import requests
from bs4 import BeautifulSoup

def fetch_news():
    try:
        url = "https://www.coindesk.com/"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        headlines = soup.find_all("a", class_="headline")
        return [h.text.strip() for h in headlines if any(x in h.text.lower() for x in ["bitcoin", "ethereum", "hack", "regulation"])]
    except:
        return []