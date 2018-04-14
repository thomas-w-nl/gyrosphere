import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import time


class Battery:
    def __init__(self):
        SPI_PORT = 0
        SPI_DEVICE = 0
        self.mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

    def __get_measurement(self):
        return self.mcp.read_adc(3)  # battery is on pin 3

    def get_spanning(self):
        """
        Read battery voltage.
        :return: Battery voltage
        """
        meetwaarde = self.__get_measurement()
        spanning = (meetwaarde * 3.3) / 512  # 1024 voor pre-voltage divider waarden. (aka x2)
        return spanning

    def print_spanning(self):
        """
        Print battery voltage.
        """
        spanning = self.get_spanning()
        print('{:.6f}v'.format(spanning))
