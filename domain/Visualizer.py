
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

class Visualizer:
    def __init__(self, data):
        self.__data = data
        
    def display_values(self):
        print(self.__data)

    def visualize_data(self):
        
        plt.figure(figsize=(10, 6))
        sns.lineplot(x='X', y='Y', data=self.__data)

        plt.xlabel('Time Index')
        plt.ylabel('Vit Unit Price')
        
        plt.title('Vit Unit Price Time Series Chart')
        plt.show()

