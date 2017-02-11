import time
import smbus
bus = smbus.SMBus(1)

class oled:
    addr = 0x3c # i2c address
    def __init__(self,val):
        time.sleep(0.001)
        bus.write_byte_data(self.addr,0,0x01)
        time.sleep(0.001)
        bus.write_byte_data(self.addr,0,0x02)
        time.sleep(0.001)
        bus.write_byte_data(self.addr,0,0x0c)
        time.sleep(0.001)
        bus.write_byte_data(self.addr,0,0x20)
    def write_word(self,word):
        for ch in word:
            time.sleep(0.1)
            bus.write_byte_data(self.addr,0x40,ord(ch))
    def scroll(self,n):
        for i in range(n*20):
            time.sleep(0.01)
            bus.write_byte_data(self.addr,0x20,0x1b)
    def clear(self):
        time.sleep(0.001)
        bus.write_byte_data(self.addr,0,0x01)
        time.sleep(0.001)
        bus.write_byte_data(self.addr,0,0x02)
        time.sleep(0.001)
        bus.write_byte_data(self.addr,0,0x0c)
        time.sleep(0.001)
        bus.write_byte_data(self.addr,0,0x20)


