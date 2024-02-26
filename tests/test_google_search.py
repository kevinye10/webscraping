from seleniumbase import BaseCase
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from .search_results import get_results
import random


class GoogleSearchTest(BaseCase):

    def setUp(self, masterqa_mode=False):
        super().setUp()

        # get new driver logged into a chrome profile
        self.get_new_driver(switch_to=True, undetectable=True,
                            user_data_dir=r"/Users/kye10/Library/Application Support/Google/Chrome/User Data")

    def test_google_search(self):
        log_file_path = r"/Users/kye10/School/pythonProjects/results/log.txt"
        results_file_path = r"/Users/kye10/School/pythonProjects/results/results.txt"
        now = datetime.now()
        date = now.strftime("%m/%d/%Y;%H:%M:%S")
        search_query = "cnn"
        link_explore_depth = 1

        try:
            self.maximize_window()

            # open google.com
            self.driver.get("https://google.com")

            # assert that the search box is there
            self.assert_element("//*[@id='APjFqb']")

            # type the search_query into the search box
            self.type("//*[@id='APjFqb']", search_query + Keys.RETURN)

            # obtain all links and css selectors to the links
            # returns a dictionary where {"href": links[], "css": css selectors[]}
            results = get_results(self.get_page_source())

            # were there any results?
            if len(results["href"]) == 0:
                raise ValueError("No results found")

            # put hrefs in a file
            links = results["href"]

            with open(results_file_path, "a", encoding="utf-8") as file:
                file.write(search_query + ";" + date + "\n")
                for link in links:
                    file.write(str(link) + "\n")
                '''for css in results["css"]:
                    file.write(css + "\n")'''
                file.write("\n")

            # write to log that search was successful
            with open(log_file_path, "a", encoding="utf-8") as file:
                file.write(date + "\n" "Successfully found results for '" + search_query + "'\n")

            # scroll to last link and back up (50% of the time)
            if random.randint(0,1):
                self.slow_scroll_to(results["css"][-1])
                self.sleep(random.randint(1,200) / 100) # wait between 0.00 and 2.00 seconds
                # since there is no self.slow_scroll_to_top(), we are going to slow scroll back to the first link
                self.slow_scroll_to(results["css"][0])

            # randomly click on one of the first 3 links
            css_to_click = results["css"][0]
            self.slow_scroll_to(css_to_click)
            self.slow_click(css_to_click)
            with open(log_file_path, "a", encoding="utf-8") as file:
                file.write("Opened link " + css_to_click + "\n\n")

            # explore the link
            self.explore_page()

        # no results found error
        except ValueError:
            with open(log_file_path, "a", encoding="utf-8") as file:
                file.write(date + "\n" + "Unable to find any results while searching for '" + search_query + "'\n")

            with open(results_file_path, "a", encoding="utf-8") as file:
                file.write(search_query + ";" + date + "\n")
                file.write("The search for '" + search_query + "' resulted in an error. Please check log.txt")

        # any other error
        except Exception as e:
            with open(log_file_path, "a", encoding="utf-8") as file:
                file.write(date + "\n" + str(e) + " occurred while searching for '" + search_query + "'\n")

            with open(results_file_path, "a", encoding="utf-8") as file:
                file.write(search_query + ";" + date + "\n")
                file.write("The search for '" + search_query + "' resulted in an error. Please check log.txt")

        # pause for 3s
        self.sleep(3)

        # driver is automatically quit by SeleniumBase

    # helper function(s)

    # scrolls and interacts with hrefs or buttons on a page
    def explore_page(self):
        log_file_path = r"/Users/kye10/School/pythonProjects/results/log.txt"
        number_links_to_find = 10

        clicked_on = random.randint(0,number_links_to_find - 1) # to click on 1 of the 10 links
        css_to_click = "" # in format a[href="link"]
        # find 10 visible links
        links = self.find_visible_elements("a[href]", limit=10)
        # write the visible links into a file
        with open(log_file_path, "a", encoding="utf-8") as file:
            file.write("searching " + self.get_current_url() + " for " + str(number_links_to_find) + " links:\n")
            for link in links:
                if clicked_on == 0:
                    css_to_click = 'a[href="' + link.get_attribute("href") + '"]'
                clicked_on -= 1
                file.write(link.get_attribute("href") + "\n")
            file.write("clicking on " + css_to_click + "\n")
        self.slow_click(css_to_click)

