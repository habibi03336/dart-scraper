import abc

class DataScraper(abc.ABC):
    @abc.abstractclassmethod
    def __init__(self, html):
        pass

    @abc.abstractclassmethod
    def retreive_currency(self):
        pass


    @abc.abstractclassmethod
    def retreive_period_standard(self):
        pass

    @abc.abstractclassmethod
    def retreive_period_length(self):
        pass 

    @abc.abstractclassmethod
    def is_3month_data(self):
        pass 

    @abc.abstractclassmethod
    def retreive_sales(self):
        pass

    @abc.abstractclassmethod
    def retreive_operating_profit(self):
        pass
    
    @abc.abstractclassmethod
    def retreive_net_profit(self):
        pass

    @abc.abstractclassmethod
    def retreive_equity(self):
        pass

    @abc.abstractclassmethod
    def retreive_debt(self):
        pass
    
    @abc.abstractclassmethod
    def retreive_cash(self):
        pass