from bs4 import BeautifulSoup


def get_results(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    # returns an 'bs4.element.ResultSet' (iterable) of <a> tags
    search = soup.find_all("a", jsname="UWckNb", href=True)
    results = []

    # let's iterate through all of the <a> tags and find <img> tag
    # if it has any 'data-atf' attribute, it is a visible search result
    for tag in search:
        img_tag = tag.find("img")   # this is the <img> tag within each <a>
        if img_tag is not None and img_tag.has_attr("data-atf"):
            results.append(tag["href"])
    return results
