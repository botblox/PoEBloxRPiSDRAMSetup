# Project Title

Set the TPS2388x PoE switch chip from Texas Instruments to auto mode and enable 4-pair 90W power mode (maximum power mode).

## Description

Run on Raspberry Pi 4B.

## Getting Started

### Enable I2C on Broadcom

By default, I2C on raspberry pi is disabled by default. Hence it must be enabled in the loadable kernel modules.

Edit `raspi-blacklist.conf` kernel modules file. E.g.

```
sudo nano /etc/modprobe.d/raspi-blacklist.conf
```

Comment out the blacklist for using i2c on Broadcom2708 CPU.

```bash
# blacklist spi and i2c by default (many users don't need them)

blacklist spi-bcm2708
#blacklist i2c-bcm2708
```

### Setup I2C kernel module

Edit `/etc/modules` to add I2C kernel module.

```
sudo nano /etc/modules
```

Add `i2c-dev` module

```bash
...
# add this at end of file
i2c-dev
```

### Dependencies

- Install `i2c-tools` with `sudo apt-get install i2c-tools`. If this fails, run `sudo apt-get update` and try again.
- Install `python-smbus` with `sudo apt-get install python-smbus`
- To configure the software, we need to add `pi` user to `i2c` access group.

```bash
sudo adduser pi i2c
```

- Reboot

### Quick test

- Connect up `SDA`, `SCL` and `GND` pins to TPS2388 line and confirm that the device can be found on the bus

```bash
i2cdetect -y 0
```

You should see a device with address 0x20 for channels 1-4 (or 0x21 for channels 5-8). Note that you can use 0x7F as a broadcast address for all TPS23881 devices on the I2C bus.

### Installing

- Clone this repo locally and `cd` into project root
- Create python virtualenv and activate

```bash
python3 -m venv .env
source .env/bin/activate
```

- Install project dependencies

```bash
pip install -r requirements.txt
```

### Execute program

- Run setup script

```
python3 tps23881_setup.py
```

## Help

## Authors

## Version History

## License

## Acknowledgments
