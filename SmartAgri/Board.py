from I2C_device import *
import time
 
class Board:
    def __init__(self, addr=0x48, port=1):
        self.device = I2C_device(addr, port)
 
    def control(self):
        self.device.read_data(0x00)
        return self.device.read_data(0x00)
 
    def light(self):
        self.device.read_data(0x01)
        return self.device.read_data(0x01)
 
    def temperature(self):
        self.device.read_data(0x02)
        return self.device.read_data(0x02)
 
    def custom(self):
        self.device.read_data(0x03)
        return self.device.read_data(0x03)
 
    def output(self, val):
        self.device.write_cmd_arg(0x40, val)
 
def main():
    board = Board()
    while (True):
        print "%s: control:%d light:%d temp:%d custom:%d" % (time.asctime(),
                               board.control(),
                               board.light(),
                               board.temperature(),
                               board.custom())
        board.output(board.control())
        time.sleep(1)
if __name__ == "__main__":
    main()
