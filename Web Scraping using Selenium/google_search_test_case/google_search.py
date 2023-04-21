# Objective: Search the keyword "Python" in Google and list all items from the first 3 pages.
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains as Ac
from selenium.webdriver.common.keys import Keys as Ky
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time as t
import pandas as pd

global pages, exec_st, prc_st 
pages = 3


class SeleniumDriver:
    def __init__(self):
        # Chrome Set-ups: Control browser closing
        options = ChromeOptions()
        options.add_experimental_option("detach", True)

        # Create the webdriver object
        self.driver = Chrome(options=options)
        self.driver.maximize_window()

        # Create DataFrame
        self.df = pd.DataFrame(columns=['title'])
        self.titles = []

    def test_case(self, url):
        # Establish Navigational Link
        self.driver.get(url)
        self.driver.implicitly_wait(5)

        # Locate Text box & conduct the search
        text_box = self.driver.find_element(By.XPATH, "//*[@id='APjFqb']")
        text_box.clear()
        text_box.send_keys("Python")
        text_box.send_keys(Ky.ENTER)

        # Suspend the execution of the program
        t.sleep(3)

        # Scrape items from the specified number of pages
        for page in range(1, pages + 1):
            if not page == 1:
                try:
                    # Explicitly Wait, halting the program execution, until the condition is resolved
                    next_page = WebDriverWait(self.driver, 12).until(
                        ec.presence_of_element_located((By.XPATH, "//*[@id='pnnext']"))
                    )
                    next_page.click()
                    self.driver.implicitly_wait(6)

                except:
                    print('Error: Synchronization failed due to timeout')

            # Locate contents of the 'Next' Button
            x = self.driver.find_elements(By.CLASS_NAME, "LC20lb")

            # Append into the list
            for i in x:
                print(i.text.strip())
                self.titles.append(i.text.strip())

        # Suspend before closing the browser
        t.sleep(5)
        self.driver.quit()

        # Filter the results and remove irrelevant results
        for title in self.titles:
            if not title == '':
                self.df.loc[len(self.df)] = {'title': title}

        print(self.df)

        # Save the DataFrame
        self.df.to_csv('google_search.csv', sep=',')
        self.df.to_json('google_search.json')
        self.df.to_xml('google_search.xml')

        # Measure Execution & Process Time
        exec_et = t.time()
        prc_et = t.process_time()
        exec_time = round(exec_et - exec_st, 2)
        prc_time = round(prc_et - prc_st, 2)

        content = "\n" + "Execution Time: " + str(exec_time) + ",  Process Time: " + str(prc_time)
        print(content)
        f = open("performance_history.txt", "a")
        f.write(content)
        f.close()


if __name__ == "__main__":
    exec_st = t.time()
    prc_st = t.process_time()
    drv = SeleniumDriver()
    start_urls = 'https://www.google.com/'
    drv.test_case(start_urls)
