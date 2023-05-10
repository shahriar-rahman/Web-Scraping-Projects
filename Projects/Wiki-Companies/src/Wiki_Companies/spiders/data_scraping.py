# Files Associated: region_links.json, direct_links.json
import scrapy
import json
import time as t
from ..items import WikiCompaniesItem


class SpiderWiki(scrapy.Spider):
    # Set ups
    name = 'spider_scraping'
    keyword = '//*[@id="mw-content-text"]/div[1]/table/tbody/'
    keyword_title = '//title'
    keyword_link = '/html/head/link[4]'
    wiki_item = WikiCompaniesItem()

    # Storage
    cmp_title = []
    cmp_hq = []
    cmp_links = []
    cmp_rev = []
    cmp_emp = []
    cmp_op_inc = []
    cmp_net_inc = []
    cmp_total_assets = []
    cmp_total_equity = []
    cmp_website = []

    # DOM Keywords
    key_txt = '/text()'
    key_href = '/@href'

    key_a = '/a'

    key_div = '/div'
    key_div_a = '/div/a'

    key_span = '/span'
    key_span_a = '/span/a'

    key_span_2 = '/span/span'
    key_span_2_a = '/span/span/a'

    key_div_span = '/div/span'
    key_div_span_a = '/div/span/a'

    key_div_ul_li_span = '/div/ul/li/span'

    # Deviants
    hq_deviants = ['headquarter', 'headquarters', 'location', 'headquarterslocation', 'hubs', 'headquarters location',
                   'emergency vehicle', 'headquartersemergency vehicle3000', 'nonfiction topics',
                   'headquarters locationnonfiction topics', 'headquarterscompleted', 'hq', 'hub']

    asset_deviants = ['total assets', 'total asset', 'asset', 'assets']

    site_deviants = ['website', 'site', 'url', 'sites', 'web site', 'websites']

    # Pagination
    def start_requests(self):
        # Access all links
        try:
            with open('direct_links.json', 'r') as file:
                links = json.load(file)

        except Exception as exc:
            print("!! Exception encountered while accessing json file. !!\n", exc)

        else:
            urls = links['Links']

            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def attribute_search(self, response, ext):
        attribute_cols = ''
        list_rev = []

        # Search & scrape attribute headers
        for row in range(1, 35):
            try:
                attribute_cols = response.xpath(self.keyword + f'tr[{row}]/th' + ext).extract()

            except Exception as exc:
                print("!! Failed to extract revenue attribute. !!\n", exc)

            # Alternate DOM structures
            if not attribute_cols != []:
                try:
                    attribute_cols = response.xpath(self.keyword + f'tr[{row}]/th' + self.key_a + ext).extract()
                except Exception as exc:
                    print("!! Alternate extraction of revenue failed. !!\n", exc)

            if not attribute_cols != []:
                try:
                    attribute_cols = response.xpath(self.keyword + f'tr[{row}]/th' + self.key_div + ext).extract()
                except Exception as exc:
                    print("!! Alternate extraction of revenue failed. !!\n", exc)

            if not attribute_cols != []:
                try:
                    attribute_cols = response.xpath(self.keyword + f'tr[{row}]/th' + self.key_div_a + ext).extract()
                except Exception as exc:
                    print("!! Alternate extraction of revenue failed. !!\n", exc)

            if not attribute_cols != []:
                try:
                    attribute_cols = response.xpath(self.keyword + f'tr[{row}]/th' + self.key_span + ext).extract()
                except Exception as exc:
                    print("!! Alternate extraction of revenue failed. !!\n", exc)

            if not attribute_cols != []:
                try:
                    attribute_cols = response.xpath(self.keyword + f'tr[{row}]/th' + self.key_span_a + ext).extract()
                except Exception as exc:
                    print("!! Alternate extraction of revenue failed. !!\n", exc)

            attribute_cols = ''.join(attribute_cols).replace('\n', '')
            list_rev.append(attribute_cols.lower())
        return list_rev

    def attribute_scraping(self, response, row, ext):
        accumulated_value = 0

        try:
            scraped_value = response.xpath(self.keyword + f'tr[{row}]/td' + self.key_span + ext).extract()

        except Exception as exc:
            print("!! Clause #1 failed. Transitioning to the next clause. !!\n", exc)

        else:
            accumulated_value = ' '.join(scraped_value)

        try:
            scraped_value = response.xpath(self.keyword + f'tr[{row}]/td' + ext).extract()

        except Exception as exc:
            print("!! Clause #2 failed. Transitioning to the next clause. !!\n", exc)

        else:
            accumulated_value = accumulated_value + ' '.join(scraped_value).replace('  ', ' ')

        try:
            scraped_value = response.xpath(self.keyword + f'tr[{row}]/td' + self.key_div + ext).extract()

        except Exception as exc:
            print("!! Clause #3 failed. Transitioning to the next clause. !!\n", exc)

        else:
            accumulated_value = accumulated_value + ' '.join(scraped_value).replace('  ', ' ')

        try:
            scraped_value = response.xpath(self.keyword + f'tr[{row}]/td' + self.key_div_a + ext).extract()

        except Exception as exc:
            print("!! Clause #4 failed. Transitioning to the next clause. !!\n", exc)

        else:
            accumulated_value = accumulated_value + ' '.join(scraped_value).replace('  ', ' ')

        try:
            scraped_value = response.xpath(self.keyword + f'tr[{row}]/td' + self.key_a + ext).extract()

        except Exception as exc:
            print("!! Clause #5 failed. Transitioning to the next clause. !!\n", exc)

        else:
            accumulated_value = accumulated_value + ' '.join(scraped_value).replace('  ', ' ')

        try:
            scraped_value = response.xpath(self.keyword + f'tr[{row}]/td' + self.key_span_a + ext).extract()

        except Exception as exc:
            print("!! Clause #6 failed. Transitioning to the next clause. !!\n", exc)

        else:
            accumulated_value = accumulated_value + ' '.join(scraped_value).replace('  ', ' ')

        try:
            scraped_value = response.xpath(self.keyword + f'tr[{row}]/td' + self.key_span_2 + ext).extract()

        except Exception as exc:
            print("!! Clause #7 failed. Transitioning to the next clause. !!\n", exc)

        else:
            accumulated_value = accumulated_value + ' '.join(scraped_value).replace('  ', ' ')

        try:
            scraped_value = response.xpath(self.keyword + f'tr[{row}]/td' + self.key_span_2_a + ext).extract()

        except Exception as exc:
            print("!! Clause #8 failed. Transitioning to the next clause. !!\n", exc)

        else:
            accumulated_value = accumulated_value + ' '.join(scraped_value).replace('  ', ' ')

        try:
            scraped_value = response.xpath(self.keyword + f'tr[{row}]/td' + self.key_div_span + ext).extract()

        except Exception as exc:
            print("!! Clause #9 failed. Transitioning to the next clause. !!\n", exc)

        else:
            accumulated_value = accumulated_value + ' '.join(scraped_value).replace('  ', ' ')

        try:
            scraped_value = response.xpath(self.keyword + f'tr[{row}]/td' + self.key_div_span_a + ext).extract()

        except Exception as exc:
            print("!! Clause #10 failed. Value could not be parsed. !!\n", exc)

        else:
            accumulated_value = accumulated_value + ' '.join(scraped_value).replace('  ', ' ')

        try:
            scraped_value = response.xpath(self.keyword + f'tr[{row}]/td' + self.key_div_ul_li_span + ext).extract()

        except Exception as exc:
            print("!! Clause #11 failed. Value could not be parsed. !!\n", exc)

        else:
            accumulated_value = accumulated_value + ' '.join(scraped_value).replace('  ', ' ')

        return accumulated_value

    # Page parsing
    def parse(self, response, **kwargs):
        # Title
        try:
            self.wiki_item['title'] = response.xpath(self.keyword_title + self.key_txt).extract()

        except Exception as exc:
            print("!! ", exc, " !!")

        # Link
        try:
            self.wiki_item['link'] = response.xpath(self.keyword_link + self.key_href).extract()

        except Exception as exc:
            print("!! ", exc, " !!")

        # Columns inspection
        attribute_cols = self.attribute_search(response, self.key_txt)
        print('◘ Columns info: \n', attribute_cols, '\n')

        # Hq
        row = 0
        filtered_hq = ''

        # Detect rows
        condition = ''.join(attribute_cols).lower()
        if 'headquarter' in condition or 'hub' in condition or 'location' in condition:

            for element in self.hq_deviants:
                try:
                    row = attribute_cols.index(element) + 1

                except Exception as exc:
                    print("!! ", exc, " !!")

                else:
                    print('-' * 75)
                    print("• HQ located in row #", row)

                    # Scraping method
                    self.wiki_item['hq'] = self.attribute_scraping(response, row, self.key_txt)
                    break

        else:
            self.wiki_item['hq'] = ''

        # Revenue
        row = 0
        filtered_rev = ''

        # Detect rows
        if 'revenue' in ''.join(attribute_cols).lower():
            try:
                row = attribute_cols.index('revenue') + 1

            except Exception as exc:
                print("!! ", exc, " !!")
                self.wiki_item['revenue'] = ''

            else:
                print('-' * 75)
                print("• Revenue located in row #", row)

                # Scraping method
                self.wiki_item['revenue'] = self.attribute_scraping(response, row, self.key_txt)

        else:
            self.wiki_item['revenue'] = ''

        # Number of employees
        row = 0
        filtered_emp = ''

        # Detect rows
        if 'employee' in ''.join(attribute_cols):
            try:
                row = attribute_cols.index('number of employees') + 1

            except Exception as exc:
                print("!! Employees could not be located in the first attempt. !!\n", exc)

                # Refined search
                try:
                    row = attribute_cols.index('employees') + 1

                except Exception as exc:
                    print("!! ", exc, " !!")
                    self.wiki_item['employee'] = ''

                else:
                    print('-' * 75)
                    print("Employee located at row #", row)

                    # Scraping method
                    self.wiki_item['employee'] = self.attribute_scraping(response, row, self.key_txt)

            else:
                print('-' * 75)
                print("• Employee located at row #", row)

                # Scraping method
                self.wiki_item['employee'] = self.attribute_scraping(response, row, self.key_txt)

        else:
            self.wiki_item['employee'] = ''

        # Operating income
        row = 0
        filtered_op_income = ''

        # Detect rows
        if 'operating income' in ''.join(attribute_cols).lower():
            try:
                row = attribute_cols.index('operating income') + 1

            except Exception as exc:
                print("!! ", exc, " !!")
                self.wiki_item['op_income'] = ''

            else:
                print('-' * 75)
                print("• Operating Income located in row #", row)

                # Scraping method
                self.wiki_item['op_income'] = self.attribute_scraping(response, row, self.key_txt)

        else:
            self.wiki_item['op_income'] = ''

        # Net income
        row = 0
        filtered_net_income = ''

        # Detect rows
        if 'net income' in ''.join(attribute_cols).lower():
            try:
                row = attribute_cols.index('net income') + 1

            except Exception as exc:
                print("!! ", exc, " !!")
                self.wiki_item['net_income'] = ''

            else:
                print('-' * 75)
                print("• Net Income located in row #", row)

                # Scraping method
                self.wiki_item['net_income'] = self.attribute_scraping(response, row, self.key_txt)

        else:
            self.wiki_item['net_income'] = ''

        # Total assets
        row = 0
        filtered_total_assets = ''

        # Detect rows
        if 'asset' in ''.join(attribute_cols):

            for element in self.asset_deviants:
                try:
                    row = attribute_cols.index(element) + 1

                except Exception as exc:
                    print("!! ", exc, " !!")
                    self.wiki_item['total_assets'] = ''

                else:
                    print('-' * 75)
                    print("• Total assets located in row #", row)

                    # Scraping method
                    self.wiki_item['total_assets'] = self.attribute_scraping(response, row, self.key_txt)
                    break

        else:
            self.wiki_item['total_assets'] = ''

        # Total equity
        row = 0
        filtered_total_equity = ''

        # Detect rows
        if 'equity' in ''.join(attribute_cols):
            try:
                row = attribute_cols.index('total equity') + 1

            except Exception as exc:
                print("!! ", exc, " !!")
                self.wiki_item['total_equity'] = ''

            else:
                print('-' * 75)
                print("• Total equity located in row #", row)

                # Scraping method
                self.wiki_item['total_equity'] = self.attribute_scraping(response, row, self.key_txt)

        else:
            self.wiki_item['total_equity'] = ''

        # Website
        row = 0
        filtered_site = ''

        # Detect rows
        condition = ''.join(attribute_cols)
        if 'site' in condition:

            for element in self.site_deviants:
                try:
                    row = attribute_cols.index(element) + 1

                except Exception as exc:
                    print("!! ", exc, " !!")

                else:
                    print('-' * 75)
                    print("• Website located in row #", row)

                    # Scraping method
                    self.wiki_item['website'] = self.attribute_scraping(response, row, self.key_href)
                    break

        else:
            self.wiki_item['website'] = ''

        # Filter containers
        # Title
        try:
            filtered_title = ''.join(self.wiki_item['title']).replace(' - Wikipedia', '')

        except Exception as exc:
            filtered_title = ''
            print("!! The Page is missing title. !!\n", exc)

        # Links
        try:
            filtered_links = ''.join(self.wiki_item['link'])

        except Exception as exc:
            filtered_links = ''
            print("!! Link does not exist in this page. !!\n", exc)

        # Hq
        try:
            filtered_hq = ''.join(self.wiki_item['hq']).replace('\n', ' ')
            filtered_hq = filtered_hq.replace(',', ' ').strip().replace('  ', ' ')
            filtered_hq = filtered_hq.replace('United States', '').replace('U.S.', '').replace('USA', '')\
                .replace('US', '')
            filtered_hq = ''.join(' ' + char if char.isupper() else char.strip() for char in filtered_hq).strip()

        except Exception as exc:
            filtered_hq = ''
            print("!! HQ does not exist in this page. !!\n", exc)

        finally:
            self.wiki_item['hq'] = filtered_hq

        # Revenue
        try:
            filtered_rev = ''.join(self.wiki_item['revenue']).lstrip().replace('  ', ' ').replace('\n', '')
            filtered_rev = filtered_rev.replace('\n', ' ')

        except Exception as exc:
            filtered_rev = ''
            print("!! Revenue does not exist in this page. !!\n", exc)

        finally:
            self.wiki_item['revenue'] = filtered_rev

        # Employee
        try:
            filtered_emp = ''.join(self.wiki_item['employee']).lstrip().replace('  ', ' ').replace('\n', '')
            filtered_emp = filtered_emp.replace('\n', ' ')

        except Exception as exc:
            filtered_emp = ''
            print("!! Employee does not exist in this page. !!\n", exc)

        finally:
            self.wiki_item['employee'] = filtered_emp

        # Operating Income
        try:
            filtered_op_income = ''.join(self.wiki_item['op_income']).lstrip().replace('  ', ' ')
            filtered_op_income = filtered_op_income.replace('\n', ' ')

        except Exception as exc:
            filtered_op_income = ''
            print("!! Operating Income does not exist in this page. !!\n", exc)

        finally:
            self.wiki_item['op_income'] = filtered_op_income

        # Net income
        try:
            filtered_net_income = ''.join(self.wiki_item['net_income']).lstrip().replace('  ', ' ')
            filtered_net_income = filtered_net_income.replace('\n', ' ')

        except Exception as exc:
            filtered_net_income = ''
            print("!! Net Income does not exist in this page. !!\n", exc)

        finally:
            self.wiki_item['net_income'] = filtered_net_income

        # Total Assets
        try:
            filtered_total_assets = ''.join(self.wiki_item['total_assets']).lstrip().replace('  ', ' ')
            filtered_total_assets = filtered_total_assets.replace('\n', ' ')

        except Exception as exc:
            filtered_total_assets = ''
            print("!! Total assets does not exist in this page. !!\n", exc)

        finally:
            self.wiki_item['total_assets'] = filtered_total_assets

        # Total Equity
        try:
            filtered_total_equity = ''.join(self.wiki_item['total_equity']).lstrip().replace('  ', ' ')
            filtered_total_equity = filtered_total_equity.replace('\n', ' ')

        except Exception as exc:
            filtered_total_equity = ''
            print("!! Total equity does not exist in this page. !!\n", exc)

        finally:
            self.wiki_item['total_equity'] = filtered_total_equity

        # Website
        try:
            filtered_site = ''.join(self.wiki_item['website']).lstrip().replace('  ', ' ')
            filtered_site = filtered_site.replace('\n', ' ')

        except Exception as exc:
            filtered_site = ''
            print("!! This company does not have a web page. !!\n", exc)

        finally:
            self.wiki_item['website'] = filtered_site

        # Storage
        self.cmp_title.append(filtered_title)
        self.cmp_links.append(filtered_links)
        self.cmp_hq.append(filtered_hq)
        self.cmp_rev.append(filtered_rev)
        self.cmp_emp.append(filtered_emp)
        self.cmp_op_inc.append(filtered_op_income)
        self.cmp_net_inc.append(filtered_net_income)
        self.cmp_total_assets.append(filtered_total_assets)
        self.cmp_total_equity.append(filtered_total_equity)
        self.cmp_website.append(filtered_site)

        # System queue
        t.sleep(0.15)
        print('-' * 70, '\n')
        yield self.wiki_item

    # Post-crawl condition
    def closed(self, response, **kwargs):
        # Firmographics dictionary
        print('\n\n', '• Operation successful, saving data to memory...\n')
        firmographics_json = {'title': self.cmp_title, 'hq': self.cmp_hq, 'link': self.cmp_links,
                              'revenue': self.cmp_rev, 'employee': self.cmp_emp, 'operating income': self.cmp_op_inc,
                              'net income': self.cmp_net_inc, 'total assets': self.cmp_total_assets,
                              'total equity': self.cmp_total_equity, 'website': self.cmp_website}

        # Save data to memory
        try:
            with open('firmographics.json', 'w') as fp:
                json.dump(firmographics_json, fp)

        except Exception as exc:
            print("!! Error encountered while saving. !!\n", exc)

        else:
            print("○ Firmographics updated successfully")
        print('-' * 50, '\n')

        # Display characteristic properties
        print("◘ Length of lists:")
        print('•Company Title:', self.cmp_title)
        print('•Company HQ:', self.cmp_hq)
        print('•Company Link:', self.cmp_links)
        print('•Company Revenue:', self.cmp_rev)
        print('•Company Employees:', self.cmp_emp)
        print('•Company Operating Income:', self.cmp_op_inc)
        print('•Company Net Income:', self.cmp_net_inc)
        print('•Company Total Assets:', self.cmp_total_assets)
        print('•Company Total Equity:', self.cmp_total_equity)
        print('•Company Website:', self.cmp_website)
        print('-' * 50, '\n')

        # Display data to terminal
        try:
            with open('firmographics.json', 'r') as fp:
                loader = json.load(fp)

        except Exception as exc:
            print("!! Error encountered while loading. !!\n", exc)

        else:
            json_object = json.dumps(loader, indent=4)
            print(json_object)
