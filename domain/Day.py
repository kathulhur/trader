class Day:
    def __init__(self, unit_prices):
        self.__unit_prices = unit_prices
        self.__current_index = 0

    def get_vit(self):
        return self.__unit_prices.get_vit(self.__current_index)

    def next_day(self):
        self.__current_index += 1

    def get_current_day(self):
        return self.__current_index
    
    def is_last_day(self):
        return self.__current_index == self.__unit_prices.size() - 1

    def reset(self):
        self.__current_index = 0

