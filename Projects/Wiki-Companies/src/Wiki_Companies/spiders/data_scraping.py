# Files Associated: region_links.json, direct_links.json
import scrapy
import json
import time as t
from ..items import WikiCompaniesItem


class SpiderWiki(scrapy.Spider):
    # Set ups
    name = 'spider_scraping'
    keyword = '//*[@id="mw-content-text"]/div[1]/table/tbody/'
    wiki_item = WikiCompaniesItem()

    # Storage
    cmp_title = []
    cmp_hq = []
    cmp_links = []
    cmp_rev = []
    cmp_emp = []

    # DOM Keywords
    key_txt = '/text()'
    key_a = '/a/text()'

    key_div = '/div/text()'
    key_div_a = '/div/a/text()'

    key_span = '/span/text()'
    key_span_a = '/span/a/text()'

    key_span_2 = '/span/span/text()'
    key_span_2_a = '/span/span/a/text()'

    key_div_span = '/div/span/text()'
    key_div_span_a = '/div/span/a/text()'

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

    def attribute_search(self, response):
        attribute_cols = ''
        list_rev = []

        # Search & scrape attribute headers
        for row in range(1, 31):
            try:
                attribute_cols = response.xpath(self.keyword + f'tr[{row}]/th' + self.key_txt).extract()

            except Exception as exc:
                print("!! Failed to extract revenue attribute. !!\n", exc)

            # Alternate DOM structures
            if not attribute_cols != []:
                try:
                    attribute_cols = response.xpath(self.keyword + f'tr[{row}]/th' + self.key_a).extract()
                except Exception as exc:
                    print("!! Alternate extraction of revenue failed. !!\n", exc)

            if not attribute_cols != []:
                try:
                    attribute_cols = response.xpath(self.keyword + f'tr[{row}]/th' + self.key_div).extract()
                except Exception as exc:
                    print("!! Alternate extraction of revenue failed. !!\n", exc)

            if not attribute_cols != []:
                try:
                    attribute_cols = response.xpath(self.keyword + f'tr[{row}]/th' + self.key_div_a).extract()
                except Exception as exc:
                    print("!! Alternate extraction of revenue failed. !!\n", exc)

            if not attribute_cols != []:
                try:
                    attribute_cols = response.xpath(self.keyword + f'tr[{row}]/th' + self.key_span).extract()
                except Exception as exc:
                    print("!! Alternate extraction of revenue failed. !!\n", exc)

            if not attribute_cols != []:
                try:
                    attribute_cols = response.xpath(self.keyword + f'tr[{row}]/th' + self.key_span_a).extract()
                except Exception as exc:
                    print("!! Alternate extraction of revenue failed. !!\n", exc)

            attribute_cols = ''.join(attribute_cols).replace('\n', '')
            list_rev.append(attribute_cols.lower())
        return list_rev

    def attribute_scraping(self, response, row):
        accumulated_value = 0

        try:
            revenue = response.xpath(self.keyword + f'tr[{row}]/td' + self.key_span).extract()

        except Exception as exc:
            print("Clause #1 failed. Transitioning to the next clause.\n", exc)

        else:
            accumulated_value = ''.join(revenue)

        try:
            revenue = response.xpath(self.keyword + f'tr[{row}]/td' + self.key_txt).extract()

        except Exception as exc:
            print("Clause #2 failed. Transitioning to the next clause.\n", exc)

        else:
            accumulated_value = accumulated_value + ' '.join(revenue).replace('  ', ' ')

        try:
            revenue = response.xpath(self.keyword + f'tr[{row}]/td' + self.key_div).extract()

        except Exception as exc:
            print("Clause #3 failed. Transitioning to the next clause.\n", exc)

        else:
            accumulated_value = accumulated_value + ' '.join(revenue).replace('  ', ' ')

        try:
            revenue = response.xpath(self.keyword + f'tr[{row}]/td' + self.key_div_a).extract()

        except Exception as exc:
            print("Clause #4 failed. Transitioning to the next clause.\n", exc)

        else:
            accumulated_value = accumulated_value + ' '.join(revenue).replace('  ', ' ')

        try:
            revenue = response.xpath(self.keyword + f'tr[{row}]/td' + self.key_a).extract()

        except Exception as exc:
            print("Clause #5 failed. Transitioning to the next clause.\n", exc)

        else:
            accumulated_value = accumulated_value + ' '.join(revenue).replace('  ', ' ')

        try:
            revenue = response.xpath(self.keyword + f'tr[{row}]/td' + self.key_span_a).extract()

        except Exception as exc:
            print("Clause #6 failed. Transitioning to the next clause.\n", exc)

        else:
            accumulated_value = accumulated_value + ' '.join(revenue).replace('  ', ' ')

        try:
            revenue = response.xpath(self.keyword + f'tr[{row}]/td' + self.key_span_2).extract()

        except Exception as exc:
            print("Clause #7 failed. Transitioning to the next clause.\n", exc)

        else:
            accumulated_value = accumulated_value + ' '.join(revenue).replace('  ', ' ')

        try:
            revenue = response.xpath(self.keyword + f'tr[{row}]/td' + self.key_span_2_a).extract()

        except Exception as exc:
            print("Clause #8 failed. Transitioning to the next clause.\n", exc)

        else:
            accumulated_value = accumulated_value + ' '.join(revenue).replace('  ', ' ')

        try:
            revenue = response.xpath(self.keyword + f'tr[{row}]/td' + self.key_div_span).extract()

        except Exception as exc:
            print("Clause #9 failed. Transitioning to the next clause.\n", exc)

        else:
            accumulated_value = accumulated_value + ' '.join(revenue).replace('  ', ' ')

        try:
            revenue = response.xpath(self.keyword + f'tr[{row}]/td' + self.key_div_span_a).extract()

        except Exception as exc:
            print("Clause #10 failed. Value could not be parsed.\n", exc)

        else:
            accumulated_value = accumulated_value + ' '.join(revenue).replace('  ', ' ')

        return accumulated_value

    # Page parsing
    def parse(self, response, **kwargs):
        attribute_hq = []

        # Title
        try:
            self.wiki_item['title'] = response.xpath('//title/text()').extract()

        except Exception as exc:
            print("!! Title in the page cannot be scraped. !!\n", exc)

        # Link
        try:
            self.wiki_item['link'] = response.xpath('/html/head/link[4]/@href').extract()

        except Exception as exc:
            print("!! Link in the page cannot be scraped. !!\n", exc)

        # Search & scrape headquarters
        for row in range(1, 12):
            # Access attribute
            try:
                attribute_hq = response.xpath(self.keyword + f'tr[{row}]/th/text()').extract()
            except Exception as exc:
                print("!! Error encountered while scraping 'HQ' attribute. !!\n", exc)

            # Access attribute alternate
            if not attribute_hq != []:
                attribute_hq = response.xpath(self.keyword + f'tr[{row}]/th/a/text()').extract()

            # Deviants
            error_types = [[], [', '], [' ']]
            hq_formats = ['Headquarters', ['Headquarters'], ['Headquarters', 'Location'], ['Headquarters', '\n', '\n'],
                          ['Headquarters location', 'Nonfiction topics'], ['Headquarters location'],
                          ['Headquarters', 'Emergency Vehicle', '\n', '3000\n'], ['Hubs']]

            # Scraping code
            if attribute_hq in hq_formats or 'Headquarters' in attribute_hq:
                print('-' * 75)
                print("◘ Headquarters located in row #", row)
                self.wiki_item['hq'] = response.xpath(self.keyword + f'tr[{row}]/td/a/text()').extract()

                if self.wiki_item['hq'] in error_types:
                    try:
                        self.wiki_item['hq'] = response.xpath(self.keyword + f'tr[{row}]/td/div/span/a/text()')\
                            .extract()

                    except Exception as exc:
                        print("!! Operation #1 failed, skipping to the next instruction. !!\n", exc)

                if self.wiki_item['hq'] in error_types:
                    try:
                        self.wiki_item['hq'] = response.xpath(self.keyword + f'tr[{row}]/td/div/a/text()').extract()

                    except Exception as exc:
                        print("!! Operation #2 failed, skipping to the next instruction. !!\n", exc)

                if self.wiki_item['hq'] in error_types:
                    try:
                        self.wiki_item['hq'] = response.xpath(self.keyword + f'tr[{row}]/td/div/text()').extract()

                    except Exception as exc:
                        print("!! Operation #3 failed, skipping to the next instruction. !!\n", exc)

                if self.wiki_item['hq'] in error_types:
                    try:
                        self.wiki_item['hq'] = response.xpath(self.keyword + f'tr[{row}]/td/span/a/text()').extract()

                    except Exception as exc:
                        print("!! Operation #4 failed, skipping to the next instruction. !!\n", exc)

                if self.wiki_item['hq'] in error_types:
                    try:
                        self.wiki_item['hq'] = response.xpath(self.keyword + f'tr[{row}]/td/text()').extract()

                    except Exception as exc:
                        print("!! Operation #5 failed, data could be unavailable. !!\n", exc)

        attribute_cols = self.attribute_search(response)

        # Debugging
        print('◘ Columns info: \n', attribute_cols, '\n')

        # Revenue
        row = 0
        filtered_rev = ''

        # Detect rows
        if 'revenue' in ''.join(attribute_cols).lower():
            try:
                row = attribute_cols.index('revenue') + 1

            except Exception as exc:
                print("!! Revenue could not be located. !!\n", exc)
                self.wiki_item['revenue'] = ''

            else:
                print('-' * 75)
                print("Revenue located in row #", row)

                # Scraping method
                self.wiki_item['revenue'] = self.attribute_scraping(response, row)

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
                    print("!! Employees could not be located in the second attempt. !!\n", exc)

                else:
                    print('-' * 75)
                    print("Employee located at row #", row)

                    # Scraping method
                    self.wiki_item['employee'] = self.attribute_scraping(response, row)

            else:
                print('-' * 75)
                print("Employee located at row #", row)

                # Scraping method
                self.wiki_item['employee'] = self.attribute_scraping(response, row)

        else:
            self.wiki_item['employee'] = ''

        # Filter containers
        try:
            filtered_title = ''.join(self.wiki_item['title']).replace(' - Wikipedia', '')

        except Exception as exc:
            filtered_title = ''
            print("!! The Page is missing title. !!\n", exc)

        try:
            filtered_hq = ' '.join(self.wiki_item['hq']).replace('\n', '').replace(',', ' ')

        except Exception as exc:
            filtered_hq = ''
            print("!! Hq does not exist in this page. !!\n", exc)

        try:
            filtered_links = ''.join(self.wiki_item['link'])

        except Exception as exc:
            filtered_links = ''
            print("!! Link does not exist in this page. !!\n", exc)

        try:
            filtered_rev = ''.join(self.wiki_item['revenue']).lstrip().replace('  ', ' ').replace('\n', '')
            filtered_rev = filtered_rev.replace('\n', ' ')

        except Exception as exc:
            filtered_rev = ''
            print("!! Revenue does not exist in this page. !!\n", exc)

        finally:
            self.wiki_item['revenue'] = filtered_rev

        try:
            filtered_emp = ''.join(self.wiki_item['employee']).lstrip().replace('  ', ' ').replace('\n', '')
            filtered_emp = filtered_emp.replace('\n', ' ')

        except Exception as exc:
            filtered_emp = ''
            print("!! Employee does not exist in this page. !!\n", exc)

        finally:
            self.wiki_item['employee'] = filtered_emp

        # Storage ----------->>
        self.cmp_title.append(filtered_title)
        self.cmp_hq.append(filtered_hq)
        self.cmp_links.append(filtered_links)
        self.cmp_rev.append(filtered_rev)
        self.cmp_emp.append(filtered_emp)

        # System queue
        t.sleep(0.15)
        print('-' * 70, '\n')
        yield self.wiki_item

    # Post-crawl condition
    def closed(self, response, **kwargs):
        # Firmographics dictionary 
        print('\n\n', 'Operation successful, saving data to memory...\n')
        firmographics_json = {'title': self.cmp_title, 'hq': self.cmp_hq, 'link': self.cmp_links,
                              'revenue': self.cmp_rev, 'employee': self.cmp_emp}

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
