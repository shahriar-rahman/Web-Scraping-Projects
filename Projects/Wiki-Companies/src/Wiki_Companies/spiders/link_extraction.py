# Files Associated: region_links.json, direct_links.json
import scrapy
import json


class SpiderWiki(scrapy.Spider):
    # Set ups
    name = 'spider_extraction'
    root_link = 'https://en.wikipedia.org/'
    direct_links = []

    # Pagination
    def start_requests(self):
        with open('region_links.json', 'r') as file:
            links = json.load(file)
        urls = links['Links']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        # Load files
        file_type = "direct links"
        try:
            with open('direct_links.json', 'r') as file:
                loader = json.load(file)

        except Exception as exc:
            print(f"!! Failed to load the {file_type} file. !!\n", exc)

        else:
            print(f"{file_type} load successful.")

        self.direct_links = loader['Links']
        print("◘ Size of Direct Links:", len(self.direct_links))

        # Iteration variables
        index = 0
        max_tables = 5
        headers = ''
        links_tabular = []
        links_italics = []

        # Localize tabular links
        for table in range(1, max_tables):
            print('\n\n', '-' * 75)
            print("◘ Extraction from Table #", table, ":")

            tabular_keyword = f'//*[@id="mw-content-text"]/div[1]/table[{table}]'
            try:
                headers = response.xpath(tabular_keyword + '/tbody/tr/th/text()').extract()

            except Exception as exc:
                print("!! Exception encountered while accessing headers. !!\n", exc)

            # Localize index columns
            col_num = 0
            for header in headers:
                col_num += 1
                header = header.strip()
                header = header.replace('\n', '')

                if header == "Name":
                    index = col_num
                    print(index)

            # Extract all types of links from the appropriate column
            try:
                links_tabular = response.xpath(
                    f'//*[@id="mw-content-text"]/div[1]/table[{table}]/tbody/tr/td[{index}]/a/@href') \
                    .extract()
            except Exception as exc:
                print("!! Exception encountered while accessing table. !!\n", exc)

            try:
                links_italics = response.xpath(
                    f'//*[@id="mw-content-text"]/div[1]/table[{table}]/tbody/tr/td[{index}]/i/a/@href') \
                    .extract()

            except Exception as exc:
                print("!! Exception encountered while accessing table. !!\n", exc)

            # Root concatenations
            if not links_tabular == []:
                for link in links_tabular:
                    if link != '':
                        self.direct_links.append(self.root_link + link)
                        print(self.root_link + link)

            if not links_italics == []:
                for link in links_italics:
                    if link != '':
                        self.direct_links.append(self.root_link + link)
                        print(self.root_link + link)
            print('\n')
        print('\n\n', '-' * 75)

        # Categorical links
        links_categorical_1 = []
        links_categorical_2 = []

        print('\n◘ Extraction from Categorical groupings:')
        categorical_keyword = '//*[@id="mw-content-text"]/div'

        try:
            links_categorical_1 = response.xpath(categorical_keyword + '/ul/li/a/@href').extract()

        except Exception as exc:
            print("!! Exception caught while processing categorical columns. !!\n", exc)

        try:
            links_categorical_2 = response.xpath(categorical_keyword + '/div/ul/li/a/@href').extract()

        except Exception as exc:
            print("!! Exception caught while processing categorical multi-columns. !!\n", exc)

        # Root concatenations
        if not links_categorical_1 == []:
            for link in links_categorical_1:
                if link != '':
                    self.direct_links.append(self.root_link + link)
                    print(self.root_link + link)
            print('\n')

        if not links_categorical_2 == []:
            for link in links_categorical_2:
                if link != '':
                    self.direct_links.append(self.root_link + link)
                    print(self.root_link + link)
            print('\n')
        print('\n\n', '-' * 75)

        # Json ops
        data_object = {'Links': self.direct_links}

        try:
            with open('direct_links.json', 'w') as fp:
                json.dump(data_object, fp)

        except Exception as exc:
            print("!! Saving Failed. !!\n", exc)

        else:
            print("○ Links update successful!\n\n")
