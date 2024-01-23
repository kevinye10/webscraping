from seleniumbase import BaseCase
from selenium.webdriver.common.keys import Keys
from tests.search_results import get_results
from datetime import datetime


class GoogleSearchTest(BaseCase):

    def setUp(self, masterqa_mode=False):
        super().setUp()

        # get new driver logged into a chrome profile
        self.get_new_driver(switch_to=True, undetectable=True,
                            user_data_dir=r"C:\Users\Kevin\AppData\Local\Google\Chrome\User Data\Profile 1")

    def test_google_search(self):

        self.maximize_window()

        # open google.com
        self.driver.get("https://google.com")

        # assert that the search box is there
        self.assert_element("//*[@id='APjFqb']")

        # type the search_query into the search box
        search_query = 'korean food'
        self.type("//*[@id='APjFqb']", search_query + Keys.RETURN)

        # obtain all links
        results = get_results(self.get_page_source())
        print(results)

        # put results in a file
        file = open(r"C:\Users\Kevin\Desktop\CGroup\results\results.txt", "a")
        now = datetime.now()
        date = now.strftime("%m/%d/%Y;%H:%M:%S")
        file.write(search_query + ";" + date + "\n")

        file.close()

        # pause for 3s
        self.sleep(3)

        # driver is automatically quit by SeleniumBase
