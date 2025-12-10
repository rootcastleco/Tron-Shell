# Tron Shell

Tron Shell is a next-generation command-line interface for flashing firmware to microcontrollers. Designed for professional embedded engineers and hobbyists alike, it provides unified access to multiple hardware platforms with advanced features like automatic USB detection, bootloader management, and comprehensive debugging capabilities.

## Features

✨ **Multi-Platform Support**
- Arduino (AVR-based boards)
- ESP32/ESP8266 (Espressif)
- STM32 (ARM Cortex-M)
- Generic microcontroller support

🔌 **Automatic USB Detection**
- Auto-detect connected devices
- Identify board types automatically
- List all available USB devices

⚡ **Advanced Flashing**
- Automatic bootloader entry
- Device reset management
- Firmware verification
- Verbose debugging output

🛠️ **Developer Friendly**
- Simple, intuitive CLI
- Rich terminal output with colors
- Comprehensive error messages
- Detailed device information

## Installation

### From PyPI (when published)
```bash
pip install tron-shell
```

### From Source
```bash
git clone https://github.com/rootcastleco/Tron-Shell.git
cd Tron-Shell
pip install -e .
```

### Development Installation
```bash
git clone https://github.com/rootcastleco/Tron-Shell.git
cd Tron-Shell
pip install -e ".[dev]"
```

## Quick Start

### List Connected Devices
```bash
tron list
```

### Flash Firmware
```bash
# Auto-detect device and flash
tron flash firmware.hex

# Specify port
tron flash firmware.bin --port /dev/ttyUSB0

# Specify platform
tron flash sketch.hex --platform arduino

# ESP32 with custom baud rate
tron flash app.bin --platform esp32 --baud 460800
```

### Get Device Information
```bash
tron info /dev/ttyUSB0
```

### Reset Device
```bash
tron reset /dev/ttyUSB0
```

## Usage

### Commands

#### `tron list`
List all connected USB devices with automatic type detection.

**Options:**
- `-v, --verbose` - Show detailed device information

**Example:**
```bash
tron list -v
```

#### `tron flash`
Flash firmware to a microcontroller.

**Arguments:**
- `FIRMWARE` - Path to firmware file (.hex, .bin, .elf)

**Options:**
- `-p, --port PORT` - Serial port (auto-detected if not specified)
- `-b, --board BOARD` - Board type (default: arduino:avr:uno)
- `--baud RATE` - Baud rate for flashing
- `--platform PLATFORM` - Platform type (arduino, esp32, stm32, auto)
- `-v, --verbose` - Enable verbose output
- `--verify/--no-verify` - Verify after flashing (default: yes)
- `--reset/--no-reset` - Reset device before flashing (default: yes)

**Examples:**
```bash
# Auto-detect everything
tron flash firmware.hex

# Arduino Mega
tron flash sketch.hex --platform arduino --board arduino:avr:mega

# ESP32 with specific port
tron flash app.bin --port /dev/ttyUSB0 --platform esp32

# No verification
tron flash firmware.bin --no-verify
```

#### `tron info`
Show detailed information about a device.

**Arguments:**
- `PORT` - Serial port of the device

**Options:**
- `-v, --verbose` - Show detailed information

**Example:**
```bash
tron info /dev/ttyUSB0 --verbose
```

#### `tron reset`
Reset a device to enter bootloader mode.

**Arguments:**
- `PORT` - Serial port of the device

**Options:**
- `--method METHOD` - Reset method (dtr, rts, 1200baud)

**Example:**
```bash
tron reset /dev/ttyUSB0 --method dtr
```

#### `tron platforms`
List all supported platforms and their details.

**Example:**
```bash
tron platforms
```

## Supported Platforms

### Arduino
- **Boards:** Uno, Mega, Nano, Leonardo, Micro
- **Bootloader:** AVR bootloader via avrdude
- **File Types:** .hex

### ESP32/ESP8266
- **Boards:** ESP32-DevKit, NodeMCU, ESP-WROOM, ESP8266
- **Bootloader:** ROM bootloader via esptool
- **File Types:** .bin

### STM32
- **Boards:** Blue Pill, Nucleo, Discovery boards
- **Bootloader:** ST-LINK or DFU
- **File Types:** .bin, .elf, .hex

### Generic
- **Boards:** Other microcontrollers
- **Description:** Fallback support for custom boards

## Development

### Running Tests
```bash
pytest
```

### With Coverage
```bash
pytest --cov=tron_shell --cov-report=html
```

### Code Formatting
```bash
black tron_shell tests
```

### Linting
```bash
flake8 tron_shell tests
```

### Type Checking
```bash
mypy tron_shell
```

## Architecture

Tron Shell is built with a modular architecture:

- **cli.py** - Main CLI interface using Click
- **usb_detector.py** - USB device detection and identification
- **flasher.py** - Platform-specific firmware flashing
- **bootloader.py** - Bootloader management and device reset

## Requirements

- Python 3.8+
- pyserial - Serial port communication
- click - CLI framework
- rich - Rich terminal output
- pyusb - USB device access

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Troubleshooting

### No devices found
- Ensure your device is connected via USB
- Check that drivers are installed for your device
- Try running with sudo/admin privileges on Linux/macOS

### Permission denied on Linux
```bash
sudo usermod -a -G dialout $USER
# Log out and log back in
```

### Flash failed
- Verify the firmware file is correct for your board
- Try specifying the platform explicitly with `--platform`
- Use `--verbose` for detailed error messages
- Ensure no other program is using the serial port

## Acknowledgments

Tron Shell builds upon the excellent work of:
- avrdude (Arduino flashing)
- esptool (ESP32/ESP8266 flashing)
- st-flash (STM32 flashing)

## Support

For issues, questions, or contributions, please visit:
https://github.com/rootcastleco/Tron-Shell/issues
