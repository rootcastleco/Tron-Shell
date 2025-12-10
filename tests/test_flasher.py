"""Tests for firmware flasher module."""

import pytest
from tron_shell.flasher import (
    ArduinoFlasher,
    ESP32Flasher,
    STM32Flasher,
    GenericFlasher,
    get_flasher,
    FlashError,
)


class TestFlashers:
    """Test flasher implementations."""

    def test_arduino_flasher(self, tmp_path):
        """Test Arduino flasher."""
        # Create a temporary firmware file
        firmware = tmp_path / "firmware.hex"
        firmware.write_text("fake firmware content")

        flasher = ArduinoFlasher("/dev/ttyUSB0", verbose=False)
        result = flasher.flash(str(firmware))
        assert result is True

        verify_result = flasher.verify(str(firmware))
        assert verify_result is True

    def test_esp32_flasher(self, tmp_path):
        """Test ESP32 flasher."""
        firmware = tmp_path / "firmware.bin"
        firmware.write_text("fake firmware content")

        flasher = ESP32Flasher("/dev/ttyUSB1", verbose=False)
        result = flasher.flash(str(firmware), baud=460800)
        assert result is True

    def test_stm32_flasher(self, tmp_path):
        """Test STM32 flasher."""
        firmware = tmp_path / "firmware.bin"
        firmware.write_text("fake firmware content")

        flasher = STM32Flasher("/dev/ttyUSB2", verbose=False)
        result = flasher.flash(str(firmware))
        assert result is True

    def test_generic_flasher(self, tmp_path):
        """Test generic flasher."""
        firmware = tmp_path / "firmware.bin"
        firmware.write_text("fake firmware content")

        flasher = GenericFlasher("COM3", verbose=False)
        result = flasher.flash(str(firmware))
        assert result is True

    def test_flash_nonexistent_file(self):
        """Test flashing nonexistent file raises error."""
        flasher = ArduinoFlasher("/dev/ttyUSB0")

        with pytest.raises(FlashError):
            flasher.flash("/nonexistent/firmware.hex")

    def test_get_flasher_arduino(self):
        """Test getting Arduino flasher."""
        flasher = get_flasher("Arduino", "/dev/ttyUSB0")
        assert isinstance(flasher, ArduinoFlasher)

    def test_get_flasher_esp32(self):
        """Test getting ESP32 flasher."""
        flasher = get_flasher("ESP32", "/dev/ttyUSB1")
        assert isinstance(flasher, ESP32Flasher)

        flasher = get_flasher("Espressif", "/dev/ttyUSB1")
        assert isinstance(flasher, ESP32Flasher)

    def test_get_flasher_stm32(self):
        """Test getting STM32 flasher."""
        flasher = get_flasher("STM32", "/dev/ttyUSB2")
        assert isinstance(flasher, STM32Flasher)

    def test_get_flasher_unknown(self):
        """Test getting flasher for unknown platform."""
        flasher = get_flasher("Unknown", "COM5")
        assert isinstance(flasher, GenericFlasher)
