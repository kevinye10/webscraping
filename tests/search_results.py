from bs4 import BeautifulSoup


def get_results(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    search = soup.find_all("a", jsname="UWckNb", href=True)
    results = []
    for tag in search:
        results.append(tag["href"])
    return results
