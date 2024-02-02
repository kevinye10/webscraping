from seleniumbase import BaseCase
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from .search_results import get_results


class GoogleSearchTest(BaseCase):

    def setUp(self, masterqa_mode=False):
        super().setUp()

        # get new driver logged into a chrome profile
        self.get_new_driver(switch_to=True, undetectable=True,
                            user_data_dir=r"/Users/kye10/Library/Application Support/Google/Chrome/User Data")

    def test_google_search(self):
        log_file_path = r"/Users/kye10/School/pythonProjects/results/log.txt"
        results_file_path = r"/Users/kye10/School/pythonProjects/results/results.txt"
        search_query = "knfbgljkshoimweurhmcoimsdjrglkjdfhmgcorwiejkrchgmclsdkjflhgmc"
        now = datetime.now()
        date = now.strftime("%m/%d/%Y;%H:%M:%S")

        try:
            self.maximize_window()

            # open google.com
            self.driver.get("https://google.com")

            # assert that the search box is there
            self.assert_element("//*[@id='APjFqb']")

            # type the search_query into the search box
            self.type("//*[@id='APjFqb']", search_query + Keys.RETURN)

            # obtain all links
            results = get_results(self.get_page_source())

            if len(results) == 0:
                raise ValueError("No results found")
            # put results in a file
            with open(results_file_path, "a", encoding="utf-8") as file:
                file.write(search_query + ";" + date + "\n")
                for result in results:
                    file.write(str(result) + "\n")
                file.write("\n")

            # write to log that search was successful
            with open(log_file_path, "a", encoding="utf-8") as file:
                file.write(date + "\n" "Successfully found results for '" + search_query + "'\n")

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
