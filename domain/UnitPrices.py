from domain.Visualizer import Visualizer
from domain.Vit import Vit
import pandas as pd

class UnitPrices:
    def __init__(self, filepath):
        self.__filename = filepath
        self.__data = self.__extract_values_from_file()
        self.__time_index = range(1, len(self.__data) + 1)
        self.__visualizer = Visualizer(self.__to_time_series_data())

    def __extract_values_from_file(self):
        data = ""
        with open(self.__filename + '.txt', 'r') as reader:
            data = reader.readlines()

        return self.__parse_values(data[0])

    def __parse_values(self, string_values):
        return list(map(int, string_values.split(',')))
    
    def size(self):
        return len(self.__data)
    
    def get_vit(self, index):
        return Vit(self.__data[index])
    
    def visualize_data(self):
        self.__visualizer.visualize_data()

    def __to_time_series_data(self):
        return pd.DataFrame({'X': self.__time_index, 'Y': self.__data})
