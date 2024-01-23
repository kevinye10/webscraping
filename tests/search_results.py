from bs4 import BeautifulSoup


def get_results(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    search = soup.find_all("div", jsname="UWckNb")
    results = []
    for link in search:
        results.append(link.a.get("href"))
