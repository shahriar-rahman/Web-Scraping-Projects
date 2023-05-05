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

    # Pagination
    def start_requests(self):
        # Access all links
        try:
            with open('direct_links.json', 'r') as file:
                links = json.load(file)

        except Exception as exc:
            print("!! Exception encountered while accessing json file. !!\n", exc)

        finally:
            urls = links['Links']

            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

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

        # Filter containers
        filtered_title = ''.join(self.wiki_item['title']).replace(' - Wikipedia', '')
        filtered_hq = ' '.join(self.wiki_item['hq']).replace('\n', '').replace(',', ' ')
        filtered_links = ''.join(self.wiki_item['link'])

        # Storage
        self.cmp_title.append(filtered_title)
        self.cmp_hq.append(filtered_hq)
        self.cmp_links.append(filtered_links)

        # System queue
        t.sleep(0.15)
        print('-' * 70, '\n')
        yield self.wiki_item

    # Post-crawl method
    def closed(self, response, **kwargs):
        # Firmographics dictionary
        print('\n\n', 'Operation successful, saving data to memory...\n')
        firmographics_json = {'title': self.cmp_title, 'hq': self.cmp_hq, 'link': self.cmp_links}

        # Save data to memory
        try:
            with open('firmographics.json', 'w') as fp:
                json.dump(firmographics_json, fp)

        except Exception as exc:
            print("!! Error encountered while saving. !!\n", exc)

        finally:
            print("○ Firmographics updated successfully")
        print('-' * 50, '\n')

        # Display characteristic properties
        print("◘ Length of lists:")
        print('•Company Title:', self.cmp_title)
        print('•Company HQ:', self.cmp_hq)
        print('•Company Link:', self.cmp_links)
        print('-' * 50, '\n')

        # Display data to terminal
        try:
            with open('firmographics.json', 'r') as fp:
                loader = json.load(fp)

        except Exception as exc:
            print("!! Error encountered while loading. !!\n", exc)

        finally:
            json_object = json.dumps(loader, indent=4)
            print(json_object)
