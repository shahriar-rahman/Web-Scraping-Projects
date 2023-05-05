import pandas as pd
import json


class DataFrame:
    def __init__(self):
        self.file_name = '../firmographics.json'
        self.df = []

    def dataframe_conversion(self):
        # Access Json
        try:
            with open(self.file_name, 'r') as fp:
                loader = json.load(fp)

        except Exception as exc:
            print("!! Failed to load the json file. !!\n", exc)

        # Dataframe observation
        finally:
            self.df = pd.DataFrame(loader)
            print("◘ Dataframe information", self.df.info())
            print('-' * 75, '\n')
            print("◘ Dataframe description", self.df.describe())
            print('-' * 75, '\n')
            print("◘ Dataframe:", self.df.head(), '\n', self.df.tail())

    def csv_conversion(self):
        print(type(self.df))
        self.df.to_csv("firmographics.csv", sep=",")
        self.df.to_excel("firmographics.xlsx")


if __name__ == "__main__":
    dfo = DataFrame()
    dfo.dataframe_conversion()
    dfo.csv_conversion()

