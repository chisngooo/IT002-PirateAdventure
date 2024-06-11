class Data:
    '''
    Khoi tao class Data de luu tru thong tin ve so mang va so tien cua nguoi choi
    Trong do coins va health deu duoc dong private va duoc truy cap thong qua property de kiem soat gia tri cua chung 
    '''
    def __init__(self, ui):
        self.ui = ui
        self.__coins = 0
        self.__health = 3
        self.ui.create_health(self.__health)

    def get_health(self):
        '''
        phuong thuc getter de tra ve gia tri cua health. khi goi Data.health se tra ve gia tri cua health
        '''
        return self.__health

    def set_health(self, value):
        '''
        phuong thuc setter de thiet lap gia tri cho health. khi goi Data.health = value se thiet lap gia tri cho health
        '''
        self.__health = value
        self.ui.create_health(value)

    def get_coins(self):
        '''
        phuong thuc getter de tra ve gia tri cua coins. khi goi Data.coins se tra ve gia tri cua coins
        '''
        return self.__coins

    def set_coins(self, value):
        '''
        phuong thuc setter de thiet lap gia tri cho coins. khi goi Data.coins = value se thiet lap gia tri cho coins
        '''
        self.__coins = value
        self.ui.show_coins(value)
        
    # Tao property de truy cap vao gia tri cua health va coins
    health = property(get_health, set_health)
    coins = property(get_coins, set_coins)
