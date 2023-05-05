# Files Associated: region_links.json, direct_links.json
import scrapy
import json


class SpiderWiki(scrapy.Spider):
    # Set ups
    name = 'spider_collection'
    root_link = 'https://en.wikipedia.org/'
    start_urls = {'https://en.wikipedia.org/wiki/List_of_companies_of_the_United_States_by_state'}
    keyword_link = '//*[@id="mw-content-text"]/div[1]/div/'

    # Storage
    region_links = []
    direct_links = []
    type = ''

    def parse(self, response, **kwargs):
        region_temp = []
        direct_temp = []

        # Scraping code
        text = 'region links'
        print('\n\n', '-' * 75)
        try:
            region_temp = response.xpath(self.keyword_link + 'a/@href').extract()

        except Exception as exc:
            print(f"!! Exception encountered while scraping {text}. !!\n", exc)

        text = 'direct links'
        try:
            direct_temp = response.xpath(self.keyword_link + 'ul/li/a/@href').extract()

        except Exception as exc:
            print(f"!! Exception encountered while scraping {text}. !!\n", exc)

        # Links based on region
        self.type = "regional links"
        for link in region_temp:
            self.region_links.append(self.root_link+link)

        # Json Ops
        region_link_json = {'Links': self.region_links}

        try:
            with open('region_links.json', 'w') as file:
                json.dump(region_link_json, file)

        except Exception as exc:
            print(f"!! Failed to save {self.type}. !!\n", exc)

        finally:
            print(f"○ Json file storage for {self.type} is successful!")

        # Links directed for company
        self.type = "direct links"
        for link in direct_temp:
            self.direct_links.append(self.root_link+link)

        # Json Ops
        direct_links_json = {'Links': self.direct_links}

        try:
            with open('direct_links.json', 'w') as file:
                json.dump(direct_links_json, file)

        except Exception as exc:
            print(f"!! Failed to save {self.type}. !!\n", exc)

        finally:
            print(f"○ Json file storage for {self.type} is successful!")

        # Display characteristic for regional links
        print('\n\n', '-' * 75)
        print("◘ Length of list containing regional links: ", len(self.region_links))
        self.type = "regional links"
        print(f"◘ Displaying all {self.type}:")

        try:
            with open('region_links.json', 'r') as file:
                loader = json.load(file)

        except Exception as exc:
            print(f"!! Failed to load {self.type}. !!\n", exc)

        finally:
            json_object = json.dumps(loader, indent=4)
            print(json_object)

        # Display json for direct company links
        print('\n\n', '-' * 75)
        print("◘ Length of list containing direct links: ", len(self.direct_links))
        self.type = "direct links"
        print(f"◘ Displaying all {self.type}:")

        try:
            with open('direct_links.json', 'r') as file:
                loader = json.load(file)

        except Exception as exc:
            print(f"!! Failed to load {self.type}. !!\n", exc)

        finally:
            json_object = json.dumps(loader, indent=4)
            print(json_object)
        print('\n\n', '-' * 75)
