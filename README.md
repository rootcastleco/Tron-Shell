#Tron Shell - Universal Microcontroller Flashing Tool

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Rootcastle Engineering](https://img.shields.io/badge/Engineered%20by-ROOTCASTLE%20ENGINEERING%20INNOVATION-brightgreen.svg)](https://rootcastle.engineering)
![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Platforms](https://img.shields.io/badge/Platforms-ATmega%2FESP%2FTron%2FARM-blue)

**Engineered by ROOTCASTLE ENGINEERING INNOVATION**  
*Precision tools for embedded systems mastery*

##Overview
Tron Shell is a next-generation command-line interface for flashing firmware to microcontrollers. Designed for professional embedded engineers and hobbyists alike, it provides unified access to multiple hardware platforms with advanced features like automatic USB detection, bootloader management, and comprehensive debugging capabilities.

##Key Features
- **Multi-Platform Support**: ATmega (AVR), ESP32/ESP8266, Tron series, and ARM Cortex-M devices
- **Hex/Binary Flashing**: Full support for `.hex`, `.bin`, and `.elf` firmware formats
- **Bootloader Management**: Automatic bootloader detection and recovery modes
- **USB Auto-Detection**: Smart port identification with vendor/product ID matching
- **Debug Mode**: Real-time protocol tracing and low-level communication logs
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Hardware Verification**: Post-flash memory verification and checksum validation
- **Secure Operations**: Firmware signature validation (optional)

##Supported Hardware Platforms
| Platform       | Models                          | Flash Types       | Bootloader Support |
|----------------|---------------------------------|-------------------|--------------------|
| **ATmega**     | 328P, 2560, 32U4                | .hex, .bin        | Optiboot, Caterina |
| **ESP**        | ESP32, ESP8266, ESP32-C3        | .bin, .elf        | esptool ROM        |
| **Tron Series**| TR-100, TR-200, TRX             | .hex, .bin        | Custom UART Boot   |
| **ARM**        | STM32F1/F4, SAMD21, NRF52       | .hex, .bin, .uf2  | DFU, SWD           |

##Installation

### Prerequisites
```bash
# Linux/macOS
sudo apt install avrdude esptool dfu-util libusb-1.0-0-dev  # Debian/Ubuntu
brew install avrdude esptool dfu-util libusb                 # macOS

# Windows (PowerShell as Admin)
winget install python
pip install pyserial pyusb esptool
