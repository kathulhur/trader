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