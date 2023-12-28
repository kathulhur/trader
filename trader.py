class Trader:
    def __init__(self, day):
        self.__php_balance = 5000
        self.__vit_balance = 0
        self.__day = day
        self.__wallet_total = self.__calculate_wallet_total()

    def get_wallet_total(self):
        return self.__wallet_total
    
    def __calculate_wallet_total(self):
        return self.__php_balance + self.__vit_balance * self.__day.get_vit().get_value()

    def buy(self, number_of_units):
        # increment vit_balance and 
        # correspondingly decrease Php_balance depending on the current_price
        total_price = self.__day.get_vit().get_value() * number_of_units
        if (total_price > self.__php_balance):
            raise ValueError("You don't have enough balance")
            
        self.__vit_balance += number_of_units
        self.__php_balance -= total_price
        self.__wallet_total = self.__calculate_wallet_total()
    

    

    def sell(self, number_of_units):
        # Decrease vit_balance and 
        #   correspondingly increase Php_balance depending on the current_price
        if(number_of_units > self.__vit_balance):
            raise ValueError("You don't have enough vit balance to perform the operation")
        
        total_price = self.__day.get_vit().get_value() * number_of_units
        self.__php_balance += total_price
        self.__vit_balance -= number_of_units
        self.__wallet_total = self.__calculate_wallet_total()

    def has_vit_balance(self):
        return self.__vit_balance > 0
    
    def __str__(self):
        return f"""
------------------------------
Php_balance:  {self.__php_balance}
vit_balance:  {self.__vit_balance}
wallet_total: {self.get_wallet_total()}
------------------------------
        """


class Vit:
    def __init__(self, value):
        self.__value = value

    # returns the php equivalent of a unit of vit
    def get_value(self):
        return self.__value
    

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


class UnitPrices:
    def __init__(self, filename):
        self.__filename = filename
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
    

    def reset(self):
        self.__current_index = 0


from enum import Enum


class VitUnitPriceProjection(Enum):
        Steady = 0
        Rise = 1
        Decline = 2

class Application:
    __valid_menu_input = 'abcd'
    __valid_trade_input = 'abc'

    def __init__(self):
        self.__trader = None
        self.__day = None
        self.__unit_prices = None

    
    def get_vit_unit_price_projection(self):

        tomorrow = self.__day.get_current_day() + 1
        unit_price_today = self.__day.get_vit().get_value()
        unit_price_tomorrow = self.__unit_prices.get_vit(tomorrow).get_value()
        print(unit_price_today, unit_price_tomorrow)

        if(unit_price_today < unit_price_tomorrow):
            return VitUnitPriceProjection.Rise
        elif(unit_price_today > unit_price_tomorrow):
            return VitUnitPriceProjection.Decline
        else:
            return VitUnitPriceProjection.Steady
        


    def __initialize(self):
        file_valid = False
        while(not(file_valid)):
            try:
                filename = self.__ask_filename_input()
                self.__unit_prices = UnitPrices(filename)
                file_valid = True
            except Exception:
                print("Invalid file input. Please remove file extension and ensure that values are comma separated.")
        
        self.__day = Day(self.__unit_prices)
        self.__trader = Trader(self.__day)
        

    def __ask_filename_input(self):
        return input("Please input file name (w/o file extension): ")
    

    def start(self):
        self.__initialize()
        while(True):
            self.__display_menu()
            user_choice = self.__ask_valid_menu_input()

            if(user_choice == 'a'):
                self.__unit_prices.visualize_data()
            elif (user_choice == 'b'):
                print(self.__trader)
                self.__display_trade_menu()
                user_choice = None

                while(user_choice != 'c'):
                    user_choice = self.__ask_valid_trade_input()
                    if(user_choice == 'a'):
                        self.__trader.buy(1)
                        print(self.__trader)
                        self.__display_trade_menu()
                         
                    elif(user_choice == 'b'):
                        try:
                            self.__trader.sell(1)
                            print(self.__trader)
                            self.__display_trade_menu()
                        except ValueError as e:
                            print(e)

                    elif(user_choice == 'c'):
                        break

            elif (user_choice == 'c'):
                self.__day.next_day()
            elif(user_choice == 'd'):
                self.__exit()

    def __display_trade_menu(self):
        projection = self.get_vit_unit_price_projection()
        print(
f"""
(a) Buy {"(Not Recommended, Vit value is projected to decline)" if projection == VitUnitPriceProjection.Decline else ""}
(b) Sell {"(Not Recommended) Vit value is projected to rise" if projection == VitUnitPriceProjection.Rise else ""}
(c) Go back
"""
        )
  
    def __ask_valid_menu_input(self):
        while(True):
            user_input = input()
            if(user_input in self.__valid_menu_input):
                return user_input
            else:
                print("Invalid input. Please try again.")


    def __ask_valid_trade_input(self):
        while(True):
            user_input = input()
            if(user_input in self.__valid_trade_input):
                return user_input
            else:
                print("Invalid input. Please try again.")


    def __display_menu(self):
        print(f"""
_______________________________    
Hello Trader
(Choose from the options)
    
Vit Value Today: {self.__day.get_vit().get_value()}
-------------------------------
(a) Display Time Series Chart
(b) Execute Trade
(c) Next Day
(d) Exit
________________________________
            
                """
              )

    def __exit(self):
        print("-------------------END-----------------------")
        exit()

if __name__ == '__main__':

    app = Application()
    app.start()







    

