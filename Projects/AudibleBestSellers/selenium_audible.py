# Objective: Scrape all the best-selling books from audible
import time as t
import pandas as pd
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By


class SeleniumDriver:
    def __init__(self):
        # Webdriver object with set-ups
        options = ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = Chrome(options=options)

        self.pages = 0
        self.current_page = 1
        self.titles = []
        self.authors = []
        self.regular_prices = []
        self.release_dates = []

        # DataFrame Initialization
        self.df = pd.DataFrame(columns=['titles', 'authors', 'regular_prices', 'release_dates'])

    def pagination_setup(self, url):
        # Establish Navigational Link
        self.driver.get(url)
        self.driver.maximize_window()

        # Locate indexed values
        page_index = self.driver.find_elements(By.XPATH, "//html/body/div[1]/div[5]/div[5]/div/div[2]/div[6]/form"
                                                         "/div/div/div[2]/div/span/ul/li")
        self.pages = int(page_index[-2].text)

    def scraping(self):
        while self.current_page <= self.pages:
            print('◘ Scraping page #', self.current_page, " - Progress: ", (self.current_page/self.pages)*100, "%")
            t.sleep(3)

            # Scrape all Titles
            titles = self.driver.find_elements(By.XPATH, "//h3[contains(@class, 'bc-heading')]")

            for title in titles:
                if title.text != '':
                    temp_title = title.text.strip().split('. ')
                    self.titles.append(temp_title[1])

            # Scrape all Authors
            authors = self.driver.find_elements(By.XPATH, "//li[contains(@class, 'authorLabel')]")

            for author in authors:
                if author.text != '':
                    self.authors.append(author.text.replace('By: ', '').strip())

            # Scrape all Prices
            regular_prices = self.driver.find_elements(By.XPATH, "//p[contains(@id, 'buybox-regular-price')]")

            for regular_price in regular_prices:
                if regular_price.text != '':
                    self.regular_prices.append(regular_price.text.split(' ')[-1])

            # Scrape all Dates
            release_dates = self.driver.find_elements(By.XPATH, "//li[contains(@class, 'releaseDateLabel')]")

            for release_date in release_dates:
                if release_date.text != '':
                    self.release_dates.append(release_date.text.split(' ')[-1])

            self.current_page += 1

            try:
                # Load next elements
                next_button = self.driver.find_element(By.XPATH, "//span[contains(@class, 'nextButton')]")

            except Exception as ex:
                print("Failed to locate the next page.", ex)

            else:
                next_button.click()

        t.sleep(5)
        self.driver.quit()

    def store_values(self):
        try:
            # Transfer to DataFrame
            for row in range(0, len(self.titles)):
                self.df.loc[len(self.df)] = {'titles': self.titles[row], 'authors': self.authors[row],
                                             'regular_prices': self.regular_prices[row],
                                             'release_dates': self.release_dates[row]}
            print(self.df)

        except Exception as ex:
            print("Transfer into the DataFrame Failed.", ex)

        else:
            # CSV, XML & JSON files
            self.df.to_csv('audible_best_sellers.csv', sep=',')
            self.df.to_xml('audible_best_sellers.xml')
            self.df.to_json('audible_best_sellers.json')
            print("DataFrame storage successful.\n")

        finally:
            # Confirmation / Diagnosis
            print('Size of Lists- \nTitles: ', len(self.titles), '\nAuthors', len(self.authors),
                  '\nPrices', len(self.regular_prices), '\nRelease Dates', len(self.release_dates))


if __name__ == "__main__":
    drv = SeleniumDriver()

    # Audible Site Link
    start_urls = 'https://www.audible.com/adblbestsellers?ref=a_hp_t1_navTop_pl0cg1c0r0&pf_rd_p=c592ea51-' \
                 'fd36-4dc9-b9af-f665ee88670b&pf_rd_r=ZZTKEW7RNC9WX81TKH8K&pageLoadId=FwsYKeyG8zKtt9sK&creativeId' \
                 '=711b5140-9c53-4812-acee-f4c553eb51fe'

    drv.pagination_setup(start_urls)
    drv.scraping()
    drv.store_values()


