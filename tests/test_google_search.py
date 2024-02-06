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
        search_query = "how to get a good score on the mcat"
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
                for css in results["css"]:
                    file.write(css + "\n")
                file.write("\n")

            # write to log that search was successful
            with open(log_file_path, "a", encoding="utf-8") as file:
                file.write(date + "\n" "Successfully found results for '" + search_query + "'\n")

            # scroll to last link and back up (50% of the time)
            if random.randint(0,1):
                self.slow_scroll_to(results["css"][-1])
                self.sleep(2)
                # since there is no self.slow_scroll_to_top(), we are going to slow scroll back to the first link
                self.slow_scroll_to(results["css"][0])

            # randomly click on one of the first 3 links
            css_to_click = results["css"][2]
            self.slow_scroll_to(css_to_click)
            self.slow_click(css_to_click)

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
        return
