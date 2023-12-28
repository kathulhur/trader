class Trader:
    def __init__(self, day):
        self.__php_balance = 5000
        self.__vit_balance = 0
        self.__day = day
        self.__wallet_total = self.__calculate_wallet_total()

    def get_vit_balance(self):
        return self.__vit_balance

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

    def sell_all(self):
        self.sell(self.__vit_balance)

    def buy_all(self):
        number_of_units_to_buy = self.__php_balance // self.__day.get_vit().get_value()
        self.buy(number_of_units_to_buy)

    def has_vit_balance(self):
        return self.__vit_balance > 0
    
    def has_enough_balance_to_buy_vit(self):
        return self.__php_balance >= self.__day.get_vit().get_value()
    
    def reset(self):
        self.__vit_balance = 0
        self.__php_balance = 5000
        self.__wallet_total = self.__calculate_wallet_total()

    def __str__(self):
        return f"""
        
-----------Trader Stats--------------
Php_balance:  {self.__php_balance}
vit_balance:  {self.__vit_balance}
wallet_total: {self.get_wallet_total()}
------------------------------------
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
    
    def is_last_day(self):
        return self.__current_index == self.__unit_prices.size() - 1

    def reset(self):
        self.__current_index = 0


from enum import Enum


class VitUnitPriceProjection(Enum):
        Steady = 0
        Rise = 1
        Decline = 2

class Application:
    __valid_menu_input = 'abcd'

    def __init__(self):
        self.__trader = None
        self.__day = None
        self.__unit_prices = None
    
    def get_vit_unit_price_projection(self):

        tomorrow = self.__day.get_current_day() + 1
        unit_price_today = self.__day.get_vit().get_value()
        unit_price_tomorrow = self.__unit_prices.get_vit(tomorrow).get_value()

        if(unit_price_today < unit_price_tomorrow):
            return VitUnitPriceProjection.Rise
        elif(unit_price_today > unit_price_tomorrow):
            return VitUnitPriceProjection.Decline
        else:
            return VitUnitPriceProjection.Steady
        
    def __initialize(self):
        
        self.__unit_prices = self.__load_unit_prices()
        self.__day = Day(self.__unit_prices)
        self.__trader = Trader(self.__day)
        
    def __load_unit_prices(self):
        while(True):
            try:
                filename = self.__ask_filename_input()
                return UnitPrices(filename)
            except Exception:
                print("Invalid file input. Please remove file extension and ensure that values are comma separated.")
        


    def __ask_filename_input(self):
        return input("Please input file name (w/o file extension): ")
    

    def start(self):
        self.__initialize()
        while(True):
            self.__display_menu()
            user_choice = self.__ask_valid_menu_input()

            if(user_choice == 'a'):
                self.__unit_prices.visualize_data()

            elif (user_choice == 'b'): # Execute Trade
                self.__execute_trade()

            elif(user_choice == 'c'):
                self.__load_unit_prices()
                self.__reset()

            elif(user_choice == 'd'):
                self.__exit()

    def __execute_trade(self):
        while(not(self.__day.is_last_day())):
            projection = self.get_vit_unit_price_projection()

            if(projection == VitUnitPriceProjection.Decline):
                if(self.__trader.has_vit_balance()): # sell all vit once it is projected that there will be a decline
                    print(f"You have sold {self.__trader.get_vit_balance()} vits")
                    self.__trader.sell_all()
                    print(self.__trader)

            elif(projection == VitUnitPriceProjection.Rise): # buy vit with all the money the first time there's a projected rise in vit price
                if(self.__trader.has_enough_balance_to_buy_vit()):
                    self.__trader.buy_all()
                    print(f"You have bought {self.__trader.get_vit_balance()} vits")
                    print(self.__trader)

            self.__day.next_day()

        if(self.__trader.has_vit_balance()): # Handle the case where all days had gone and there's vit balance available
            self.__trader.sell_all()
            print(self.__trader)

        self.__reset()


    def __reset(self):
        self.__day.reset()
        self.__trader.reset()
  

    def __ask_valid_menu_input(self):
        while(True):
            user_input = input()
            if(user_input in self.__valid_menu_input):
                return user_input
            else:
                print("Invalid input. Please try again.")


    def __display_menu(self):
        print(f"""
________________________________    
              
Hello Trader!
(Choose from the options)
              
(a) Display Time Series Chart
(b) Execute Trade
(c) Choose a new file
(d) Exit
________________________________
            
""")

    def __exit(self):
        print("-------------------END-----------------------")
        exit()

if __name__ == '__main__':

    app = Application()
    app.start()







    

