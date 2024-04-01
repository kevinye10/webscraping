from bs4 import BeautifulSoup
import random


def get_results(page_source, log_file_path):
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
    try:
        for i in range(5):  # obtain the css selectors of the first 5 links
            # in format: 'a[href="link"] h3.LC20lb.MBeuO.DKV0Md'
            a_selector = 'a[href="' + results["href"][i] + '"]'
            results["css"].append(a_selector + h3_selector)
    except IndexError as e:
        # not all 5 links exist
        pass

    return results


# scrolls and interacts with hrefs or buttons on a page
"""
def explore_page(self, log_file_path, number_links_to_find):
    current_url = self.get_current_url()
    self.sleep(3)
    # find up to 10 visible links
    links = self.find_visible_elements("a[href]", limit=number_links_to_find)
    clicked_on = random.randint(0, len(links) - 1)  # to click on 1 of the links we found
    # define css selector to click
    css_to_click = 'a[href="' + links[clicked_on].get_attribute("href") + '"]'  # in format a[href="link"]
    # write the visible links into a file
    with open(log_file_path, "a", encoding="utf-8") as file:
        file.write("searching " + self.get_current_url() + " for up to " + str(number_links_to_find) + " links:\n")
        for link in links:
            file.write(link.get_attribute("href") + "\n")
        counter = 0
        while self.get_current_url() == current_url and counter < len(links):
            try:
                file.write("Clicking on: " + css_to_click + "\n")
                counter += 1
                self.slow_click(css_to_click)
            except Exception as e:  # if clicking on the URL fails (most likely that element isn't visible)
                file.write("Exception: " + str(e) + "occurred while clicking" + css_to_click + "\n")
                # increment to click on the next link
                clicked_on += 1
                css_to_click = 'a[href="' + links[clicked_on % len(links)].get_attribute("href") + '"]'
"""


def explore_page(self, log_file_path, number_link_to_click):
    current_url = self.get_current_url()
    self.sleep(3)
    if number_link_to_click < 0:
        with open(log_file_path, "a", encoding="utf-8") as file:
            file.write("negative link indices are not allowed")
            return

    # continuously try clicking on links - if one doesn't work move onto a next one
    while self.get_current_url() == current_url and number_link_to_click > 0:
        with open(log_file_path, "a", encoding="utf-8") as file:
            file.write("Attempting to click on link " + str(number_link_to_click) + ": " + current_url + "\t...\t")
            try:
                self.click_nth_visible_element("a", number_link_to_click)
                file.write("Success!\n")
            except Exception as e:
                file.write("Exception: " + str(e) + "occurred\n")
                number_link_to_click += 1


def slow_scroll_down_up(self, percent):
    # scroll down percent% of the total page height
    total_height = self.execute_script("return document.body.scrollHeight") * percent

    for i in range(0, total_height, 50):  # Scrolls/100 pixels
        self.execute_script(f"window.scrollTo(0, {i})")
        # simulate user behavior
        if i % 2000 == 0:    # once every 2000 pixels wait extra long
            self.sleep(1)
        else:
            self.sleep(random.random() / 16)     # waits short amount of time

    self.sleep(random.random() * 2)  # wait for up to 2 seconds

    for i in range(total_height, 0, -50):  # Adjust the step/increment value as needed
        self.execute_script(f"window.scrollTo(0, {i})")
        # simulate user behavior
        if i % 2000 == 0:    # once every 2000 pixels wait extra long
            self.sleep(1)
        else:
            self.sleep(random.random() / 16)     # waits short amount of time
