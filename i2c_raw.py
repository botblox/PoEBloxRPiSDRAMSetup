import fcntl
import io
import sys


def _b(x):
    return x if sys.hexversion < 0x03000000 else x.encode("latin-1")


class I2CRaw:
    I2C_SLAVE = 0x0703

    def __init__(self, device: int, bus: int):
        self.fr = io.open("/dev/i2c-" + str(bus), "rb", buffering=0)
        self.fw = io.open("/dev/i2c-" + str(bus), "wb", buffering=0)

        # set device address
        fcntl.ioctl(self.fr, self.I2C_SLAVE, device)
        fcntl.ioctl(self.fw, self.I2C_SLAVE, device)

    def write(self, data):
        if type(data) is list:
            data = bytearray(data)
        elif type(data) is str:
            data = _b(data)
        else:
            raise Exception("Invalid data type")
        self.fw.write(data)

    def read(self, count):
        return self.fr.read(count)

    def close(self):
        self.fw.close()
        self.fr.close()
