import logging

from smbus2 import SMBus

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

bus = SMBus(1)
i2c_address = 0x20

device_id_silicon_revision = bus.read_byte_data(i2c_address, 0x43)
logger.info(f"Device ID: {device_id_silicon_revision}")
