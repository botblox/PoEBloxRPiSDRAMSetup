import logging

from smbus2 import SMBus

logger = logging.getLogger(__name__)

bus = SMBus(0)
# 0x21 for channels 5-8 if device is in I2C 'Configuration B'
# Default is Configuration A where device is addressed as a single I2C device with A0=0.
# Note that SRAM and parity programming for upper channels 5-8 does not program SRAM or parity.
i2c_address = 0x20 
is_parity_enabled = False

if __name__ == '__main__':
    logger.info("SRAM and Parity programming steps for TPS23881")
    logger.info(f"Parity enabled: {is_parity_enabled}")

    bus.write_byte_data(i2c_address, 0x60, 0x01) # Reset the memory address pointer
    bus.write_byte_data(i2c_address, 0x62, 0x00) # Set start address LSB
    bus.write_byte_data(i2c_address, 0x63, 0x80) # Set start address MSB

    if is_parity_enabled:
        ...
    
    bus.write_byte_data(i2c_address, 0x60, 0xC0) # Keep CPU in reset and enable SRAM I2C write

    # prepare for RAM download
    bus.write_byte_data(i2c_address, 0x1D, 0xBC)
    bus.write_byte_data(i2c_address, 0xD7, 0x02)
    bus.write_byte_data(i2c_address, 0x91, 0x00)
    bus.write_byte_data(i2c_address, 0x90, 0x00)
    bus.write_byte_data(i2c_address, 0xD7, 0x00)
    bus.write_byte_data(i2c_address, 0x1D, 0x00)

    # load SRAM data
