"""
USB device detection and management module.
"""

import serial.tools.list_ports
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class USBDevice:
    """Represents a USB device."""

    port: str
    vid: Optional[int]
    pid: Optional[int]
    serial_number: Optional[str]
    manufacturer: Optional[str]
    product: Optional[str]
    description: str

    def __str__(self) -> str:
        return f"{self.port} - {self.description}"

    @property
    def vid_pid(self) -> Optional[str]:
        """Return VID:PID string if available."""
        if self.vid is not None and self.pid is not None:
            return f"{self.vid:04X}:{self.pid:04X}"
        return None


class USBDetector:
    """Handles USB device detection and enumeration."""

    # Common microcontroller VID:PID pairs
    KNOWN_DEVICES = {
        (0x2341, None): "Arduino",  # Arduino VID
        (0x1A86, 0x7523): "CH340 Serial",
        (0x0403, 0x6001): "FTDI FT232",
        (0x10C4, 0xEA60): "CP210x UART Bridge",
        (0x0483, 0x5740): "STM32 Virtual COM Port",
        (0x1A86, 0x55D4): "ESP32-C3",
        (0x303A, 0x1001): "ESP32-S2/S3",
        (0x303A, None): "Espressif",
    }

    @staticmethod
    def detect_devices() -> List[USBDevice]:
        """
        Detect all connected USB serial devices.

        Returns:
            List of USBDevice objects representing connected devices.
        """
        devices = []
        ports = serial.tools.list_ports.comports()

        for port in ports:
            device = USBDevice(
                port=port.device,
                vid=port.vid,
                pid=port.pid,
                serial_number=port.serial_number,
                manufacturer=port.manufacturer,
                product=port.product,
                description=port.description,
            )
            devices.append(device)

        return devices

    @staticmethod
    def identify_device_type(device: USBDevice) -> str:
        """
        Identify the type of microcontroller/device.

        Args:
            device: USBDevice to identify

        Returns:
            String describing the device type
        """
        # Check exact VID:PID match
        if device.vid and device.pid:
            key = (device.vid, device.pid)
            if key in USBDetector.KNOWN_DEVICES:
                return USBDetector.KNOWN_DEVICES[key]

        # Check VID-only match
        if device.vid:
            key = (device.vid, None)
            if key in USBDetector.KNOWN_DEVICES:
                return USBDetector.KNOWN_DEVICES[key]

        # Check description for known patterns
        desc_lower = device.description.lower()
        if "arduino" in desc_lower:
            return "Arduino"
        elif "esp32" in desc_lower or "esp8266" in desc_lower:
            return "Espressif"
        elif "stm32" in desc_lower or "stlink" in desc_lower:
            return "STM32"

        return "Unknown"

    @staticmethod
    def find_device_by_port(port: str) -> Optional[USBDevice]:
        """
        Find a specific device by port name.

        Args:
            port: Port name (e.g., /dev/ttyUSB0, COM3)

        Returns:
            USBDevice if found, None otherwise
        """
        devices = USBDetector.detect_devices()
        for device in devices:
            if device.port == port:
                return device
        return None

    @staticmethod
    def auto_detect_target() -> Optional[USBDevice]:
        """
        Attempt to auto-detect a suitable flash target.

        Returns:
            First detected microcontroller device, or None
        """
        devices = USBDetector.detect_devices()

        # Prefer known microcontroller devices
        for device in devices:
            device_type = USBDetector.identify_device_type(device)
            if device_type != "Unknown":
                return device

        # Return first device if any
        if devices:
            return devices[0]

        return None
