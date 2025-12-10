# Tron Shell - Universal Microcontroller Flashing Tool

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Rootcastle Engineering](https://img.shields.io/badge/Engineered%20by-ROOTCASTLE%20ENGINEERING%20INNOVATION-brightgreen.svg)](https://rootcastle.com)
![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Platforms](https://img.shields.io/badge/Platforms-ATmega%2FESP%2FTron%2FARM-blue)

**Engineered by ROOTCASTLE ENGINEERING INNOVATION**

## Overview

Tron Shell is a next-generation command-line interface for flashing firmware to microcontrollers. Designed for professional embedded engineers and hobbyists alike, it provides unified access to multiple hardware platforms with advanced features like automatic USB detection, bootloader management, and comprehensive debugging capabilities.

## Key Features

- **Multi-Platform Support**: ATmega (AVR), ESP32/ESP8266, Tron series, and ARM Cortex-M devices
- **Hex/Binary Flashing**: Full support for `.hex`, `.bin`, and `.elf` firmware formats
- **Bootloader Management**: Automatic bootloader detection and recovery modes
- **USB Auto-Detection**: Smart port identification with vendor/product ID matching
- **Debug Mode**: Real-time protocol tracing and low-level communication logs
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Hardware Verification**: Post-flash memory verification and checksum validation
- **Secure Operations**: Firmware signature validation (optional)

## Supported Hardware Platforms

### ATmega Series (AVR)

The most widely used microcontroller family in embedded systems and education:

| Model | Flash | RAM | EEPROM | Bootloader | Common Use Cases |
|-------|-------|-----|--------|------------|------------------|
| ATmega328P | 32KB | 2KB | 1KB | Optiboot, Arduino | Arduino Uno, IoT devices |
| ATmega2560 | 256KB | 8KB | 4KB | Optiboot | Arduino Mega, CNC machines |
| ATmega32U4 | 32KB | 2.5KB | 1KB | Caterina | Arduino Leonardo, Micro |
| ATmega168P | 16KB | 1KB | 512B | Optiboot | Mini boards, sensors |
| ATmega644P | 64KB | 4KB | 2KB | Custom | Industrial automation |
| ATmega1284P | 128KB | 16KB | 4KB | Custom | Advanced projects |
| ATmega8 | 8KB | 1KB | 512B | None | Legacy systems |
| ATmega16 | 16KB | 1KB | 512B | None | Legacy systems |
| ATmega32 | 32KB | 2KB | 1KB | None | Legacy systems |
| ATmega64 | 64KB | 4KB | 2KB | None | Legacy systems |
| ATmega128 | 128KB | 4KB | 4KB | None | Legacy industrial use |
| ATmega256 | 256KB | 8KB | 4KB | None | Legacy industrial use |
| ATmega1280 | 128KB | 8KB | 4KB | Optiboot | Industrial applications |
| ATmega1281 | 128KB | 8KB | 4KB | Custom | Heavy-duty applications |
| ATmega640 | 64KB | 8KB | 4KB | Optiboot | Robotics, automation |
| ATmega88P | 8KB | 1KB | 512B | Custom | Embedded systems |
| ATmega88PA | 8KB | 1KB | 512B | Custom | Updated variant |
| ATmega48P | 4KB | 512B | 256B | Custom | Minimal systems |
| ATmega164P | 16KB | 1KB | 512B | Custom | Extended features |
| ATmega324P | 32KB | 2KB | 1KB | Custom | Enhanced capabilities |

### Other Supported Platforms

| Platform | Models | Flash Types | Bootloader Support |
|----------|--------|-------------|-------------------|
| **ESP** | ESP32, ESP8266, ESP32-C3 | .bin, .elf | esptool ROM |
| **Tron Series** | TR-100, TR-200, TRX | .hex, .bin | Custom UART Boot |
| **ARM** | STM32F1/F4, SAMD21, NRF52 | .hex, .bin, .uf2 | DFU, SWD |

## Prerequisites

### System Requirements

#### Linux (Debian/Ubuntu)
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip libusb-1.0-0-dev
pip install pyserial pyusb
```

#### macOS
```bash
brew install python libusb
pip install pyserial pyusb
```

#### Windows (PowerShell as Admin)
```powershell
# Install Python from python.org or use:
winget install Python.Python.3.10
pip install pyserial pyusb
```

### Optional Tools (for advanced operations)
```bash
# For AVR programming with avrdude
avrdude

# For ESP32/ESP8266
esptool.py

# For ARM devices with DFU
dfu-util
```

## Installation

### From PyPI (recommended)
```bash
pip install tron-shell
```

### From Source
```bash
git clone https://github.com/rootcastleco/Tron-Shell.git
cd Tron-Shell
pip install -e .
```

## Quick Start

### List Connected Devices
```bash
tron list
```

### Flash a Device
```bash
tron flash --port /dev/ttyUSB0 --file firmware.hex --platform atmega328p
```

### Reset Device to Bootloader Mode
```bash
tron reset --port /dev/ttyUSB0 --platform atmega328p
```

### Get Device Information
```bash
tron info --port /dev/ttyUSB0
```

### List Supported Platforms
```bash
tron platforms
```

## Advanced Usage

### Debug Mode
Enable detailed logging for troubleshooting:
```bash
tron flash --port /dev/ttyUSB0 --file firmware.hex --debug
```

### Verify After Flash
Perform post-flash verification:
```bash
tron flash --port /dev/ttyUSB0 --file firmware.hex --verify
```

### Specify Baud Rate
```bash
tron flash --port /dev/ttyUSB0 --file firmware.hex --baud 115200
```

## Configuration

Tron Shell can be configured via YAML configuration files. Default configuration is located at:
- Linux/macOS: `~/.config/tron/config.yaml`
- Windows: `%APPDATA%\tron\config.yaml`

Example configuration:
```yaml
serial:
  default_baud: 115200
  timeout: 2

devices:
  atmega328p:
    vid: "0x2341"
    pid: "0x0043"
    bootloader: "optiboot"

debug: false
verify_after_flash: true
```

## Troubleshooting

### Device Not Found
1. Check USB cable connection
2. Verify device drivers are installed
3. Run `tron list` to see all detected ports
4. Try different USB port on computer

### Permission Denied (Linux/macOS)
```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER
# Log out and back in, or:
newgrp dialout
```

### Failed Flash Verification
1. Reduce baud rate with `--baud 9600`
2. Add delay with `--delay 500`
3. Check device bootloader compatibility
4. Verify firmware file integrity

### Serial Port Issues
- Ensure no other application has the port open
- Restart the device
- Check device manager for unknown devices
- Update or reinstall device drivers

## Contributing

We welcome contributions from the community! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE) file for details.

## Support

For issues, feature requests, or questions:
- GitHub Issues: [Tron-Shell Issues](https://github.com/rootcastleco/Tron-Shell/issues)
- Documentation: Check the `/docs` folder
- Community: Join our discussions

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

---

**Created with dedication by ROOTCASTLE ENGINEERING INNOVATION**

