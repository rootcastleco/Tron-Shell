# Example Firmware Files

This directory can contain example firmware files for testing Tron Shell.

## Creating Test Firmware

### Arduino (.hex)
Compile your Arduino sketch and locate the .hex file in the build directory.

### ESP32 (.bin)
Use Arduino IDE or PlatformIO to build ESP32 projects and get the .bin file.

### STM32 (.bin, .elf)
Use STM32CubeIDE or similar tools to build firmware for STM32 boards.

## Usage with Tron Shell

```bash
# Flash an example Arduino firmware
tron flash examples/blink.hex --platform arduino

# Flash an example ESP32 firmware
tron flash examples/app.bin --platform esp32
```
