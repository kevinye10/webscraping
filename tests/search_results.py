from bs4 import BeautifulSoup


def get_results(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    # returns an 'bs4.element.ResultSet' (iterable) of <a> tags
    search = soup.find_all("a", jsname="UWckNb", href=True)
    results = {"href": [], "css": []}

    # let's iterate through all the <a> tags and find <img> tag if it has any 'data-atf' attribute, it is a visible
    # search result. The 'data-atf' attribute relates to the small icon in the top left of the website's logo.
    for tag in search:
        img_tag = tag.find("img")   # this is the <img> tag within each <a>
        if img_tag is not None and img_tag.has_attr("data-atf"):
            results["href"].append(tag["href"])
        '''else:
            svg_tag = tag.find("svg")
            if svg_tag is not None:
                results.append(tag["href"])'''
    h3_selector = ' h3.LC20lb.MBeuO.DKV0Md'
    for i in range(5):  # obtain the css selectors of the first 5 links
        # in format: 'a[href="link"] h3.LC20lb.MBeuO.DKV0Md'
        a_selector = 'a[href="' + results["href"][i] + '"]'
        results["css"].append(a_selector + h3_selector)

    return results
