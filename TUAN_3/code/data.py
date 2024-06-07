class Data:
    '''
    Khởi tạo class Data để luu trữ thông tin về số mạng và số tiền của người chơi
    Trong đó coins và health đều được đóng private và được truy cập thông qua property để kiểm soát giá trị của chúng 
    '''
    def __init__(self, ui):
        self.ui = ui
        self.__coins = 0
        self.__health = 3
        self.ui.create_health(self.__health)

    def get_health(self):
        '''
        phương thức getter để trả về giá trị của health. khi gọi Data.health sẽ trả về giá trị của health
        '''
        return self.__health

    def set_health(self, value):
        '''
        phương thức setter để thiết lập giá trị cho health. khi gọi Data.health = value sẽ thiết lập giá trị cho health
        '''
        self.__health = value
        self.ui.create_health(value)

    def get_coins(self):
        '''
        phương thức getter để trả về giá trị của coins. khi gọi Data.coins sẽ trả về giá trị của coins
        '''
        return self.__coins

    def set_coins(self, value):
        '''
        phương thức setter để thiết lập giá trị cho coins. khi gọi Data.coins = value sẽ thiết lập giá trị cho coins
        
        '''
        self.__coins = value
        self.ui.show_coins(value)
    # Tạo property để truy cập vào giá trị của health và coins
    health = property(get_health, set_health)
    coins = property(get_coins, set_coins)
