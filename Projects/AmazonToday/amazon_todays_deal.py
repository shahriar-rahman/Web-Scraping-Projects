# Objective: Scrape 10 pages of Amazon's 'Today's deal' section
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WdW
from selenium.webdriver.support import expected_conditions as ec
import time as t
import pandas as pd


class SeleniumDriver:
    def __init__(self):
        # Set-ups
        start_urls = 'https://www.amazon.com/'
        options = ChromeOptions()
        options.add_experimental_option("detach", True)

        # Driver object
        self.driver = Chrome(options=options)
        self.driver.get(start_urls)
        self.driver.maximize_window()
        self.driver.implicitly_wait(7)

        # Storage initialization
        self.current_page = 1
        self.pages = 10
        self.items = []
        self.deal_types = []
        self.img_links = []
        self.df = pd.DataFrame(columns=['items', 'deal_types', 'img_links'])

    def load_page(self):
        try:
            # Supress initial Popup
            try:
                popup = self.driver.find_element(By.XPATH, "//*[@id='nav-main']/div[1]/div/div/div[3]/span[1]"
                                                           "/span/input")

            except Exception as exc:
                print('• Popup did not appear.\n', exc)

            else:
                popup.click()

            finally:
                self.driver.implicitly_wait(5)

            # Locate page link
            get_link = WdW(self.driver, 10).until(
                ec.presence_of_element_located((By.XPATH, "//*[@id='nav-xshop']/a[1]"))
            )

        except Exception as exc:
            print('• Failed to locate the link.\n', exc)

        else:
            get_link.click()

        finally:
            self.driver.implicitly_wait(10)

    def scrape_items(self):
        while self.current_page <= self.pages:
            # Load new page
            print('\n◘ Accessing Page #', self.current_page, ' - Progress: ', (self.current_page/self.pages)*100, '%')
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            t.sleep(5)

            # Scrape items
            try:
                items = WdW(self.driver, 5).until(
                    ec.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'DealContent-module')]"))
                )

            except Exception as exc:
                print('• Item extraction unsuccessful.\n', exc)

            else:
                # Append items
                for item in items:
                    if not item.text == '':
                        print('\n○ Displaying items:\n', item.text.strip())
                        self.items.append(item.text.strip())

            # Scrape deals
            try:
                deal_types = WdW(self.driver, 5).until(
                    ec.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'BadgeAutomatedLabel-')]"))
                )

            except Exception as exc:
                print("• Deal Types extraction unsuccessful.\n", exc)

            else:
                # Append deals
                for deal in deal_types:
                    if not deal.text == '':
                        print('\n○ Displaying deals:\n', deal.text.strip())
                        self.deal_types.append(deal.text.strip())

            # Scrape Links
            try:
                img_links = WdW(self.driver, 5).until(
                    ec.presence_of_all_elements_located((By.XPATH, "//img[contains(@class,'DealImage-module')]"))
                )

            except Exception as exc:
                print("• Links extraction unsuccessful.\n", exc)

            else:
                # Append links
                for link in img_links:
                    print('\n○ Displaying image links:\n', link.get_attribute('src'))
                    self.img_links.append(link.get_attribute('src'))

            self.current_page += 1

            try:
                # Pagination
                next_elements = WdW(self.driver, 5).until(
                    ec.presence_of_element_located((By.XPATH, "//li[contains(@class, 'a-last')]"))
                )

            except Exception as exc:
                print("• Failed to locate next elements.\n", exc)

            else:
                next_elements.click()

            finally:
                self.driver.implicitly_wait(10)

        t.sleep(2.5)
        self.driver.quit()

    def store_items(self):
        # Validating data structure
        list_size = [len(self.items), len(self.deal_types), len(self.img_links)]
        print('\n◘ Attribute characteristics\nitems:', list_size[0], ' - ', 'deal_types:', list_size[1], ' - ',
              'img_links:', list_size[2])

        # Transfer to DataFrame
        if len(set(list_size)) == 1:
            for row in range(0, len(self.items)):
                try:
                    self.df.loc[len(self.df)] = {'items': self.items[row], 'deal_types': self.deal_types[row],
                                                 'img_links': self.img_links[row]}

                except Exception as exc:
                    print('• Error at Row #', row, '\n', exc)

        # Store to memory
        self.df.to_csv('today_deal.csv', sep=',')
        self.df.to_excel('today_deal.xlsx')
        self.df.to_xml('today_deal.xml')
        self.df.to_json('today_deal.json')


if __name__ == "__main__":
    drv = SeleniumDriver()
    drv.load_page()
    drv.scrape_items()
    drv.store_items()
