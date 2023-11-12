import logging
import struct
from time import sleep

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
        logger.exception("Parity is not implemented for TPS23881")
        raise Exception("Parity is not implemented for TPS23881")
    
    bus.write_byte_data(i2c_address, 0x60, 0xC0) # Keep CPU in reset and enable SRAM I2C write

    # prepare for RAM download
    bus.write_byte_data(i2c_address, 0x1D, 0xBC)
    bus.write_byte_data(i2c_address, 0xD7, 0x02)
    bus.write_byte_data(i2c_address, 0x91, 0x00)
    bus.write_byte_data(i2c_address, 0x90, 0x00)
    bus.write_byte_data(i2c_address, 0xD7, 0x00)
    bus.write_byte_data(i2c_address, 0x1D, 0x00)

    # load SRAM data
    sram_data = open('TPS23881_2_SRAM_v14.bin', 'rb').read()
    # offset 170 bytes to avoid unnecessary heading bytes
    sram_data = sram_data[170:]
    sram_data_bytes = list(struct.iter_unpack('c', sram_data))
    del sram_data_bytes[11-1::11] # remove space character bytes
    del sram_data_bytes[10-1::10] # remove newline character bytes
    del sram_data_bytes[9-1::9] # remove return character bytes

    sram_data: list[int] = []
    _sram_bytestr: str = ''
    for i, sram_data_byte in enumerate(sram_data_bytes):
        if i != 0 and i % 8 == 0:
            sram_data.append(int(_sram_bytestr, 2))
            _sram_bytestr = ''
        _sram_bytestr += sram_data_byte[0].decode("utf-8") 
    # write SRAM data to TPS23881
    bus.write_block_data(i2c_address, 0x61, sram_data)
    
    if is_parity_enabled:
        bus.write_byte_data(i2c_address, 0x60, 0x18) # Clears CPU reset and enables SRAM and Parity
    else:
        bus.write_byte_data(i2c_address, 0x60, 0x08) # Clears CPU reset and enables SRAM
    
    logger.info("Loaded SRAM data and enabled")
    sleep(0.20) # wait 0.20 seconds for the CPU to reset - minimum 0.012 seconds required

    firmware_revision = bus.read_byte_data(i2c_address, 0x41)
    logger.info(f"Firmware revision: {firmware_revision}")

