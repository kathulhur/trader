from domain.Day import Day 
from domain.Trader import Trader
from domain.UnitPrices import UnitPrices
from enum import Enum

from os import path

class VitUnitPriceProjection(Enum):
        Steady = 0
        Rise = 1
        Decline = 2

class Application:
    __valid_menu_input = 'abcd'

    def __init__(self, main_file):
        self.__trader = None
        self.__day = None
        self.__unit_prices = None
        self.__main_path = path.dirname(main_file)
    
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
                filepath = path.join(self.__main_path, filename)
                print(filepath)
                return UnitPrices(filepath)
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
                print('----------------Start of Transactions-------------------')
                self.__execute_trade()
                print('-----------------End of Transactions-------------------')

            elif(user_choice == 'c'):
                self.__initialize()

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