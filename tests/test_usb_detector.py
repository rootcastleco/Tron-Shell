"""Tests for USB detection module."""

from tron_shell.usb_detector import USBDevice, USBDetector


class TestUSBDevice:
    """Test USBDevice dataclass."""

    def test_device_creation(self):
        """Test creating a USB device."""
        device = USBDevice(
            port="/dev/ttyUSB0",
            vid=0x2341,
            pid=0x0043,
            serial_number="12345",
            manufacturer="Arduino",
            product="Uno",
            description="Arduino Uno",
        )

        assert device.port == "/dev/ttyUSB0"
        assert device.vid == 0x2341
        assert device.pid == 0x0043
        assert device.vid_pid == "2341:0043"

    def test_device_without_vid_pid(self):
        """Test device without VID/PID."""
        device = USBDevice(
            port="COM3",
            vid=None,
            pid=None,
            serial_number=None,
            manufacturer=None,
            product=None,
            description="Unknown Device",
        )

        assert device.vid_pid is None


class TestUSBDetector:
    """Test USB detector functionality."""

    def test_detect_devices(self):
        """Test device detection."""
        devices = USBDetector.detect_devices()
        assert isinstance(devices, list)
        # May be empty if no devices connected

    def test_identify_arduino(self):
        """Test Arduino device identification."""
        device = USBDevice(
            port="/dev/ttyUSB0",
            vid=0x2341,
            pid=0x0043,
            serial_number=None,
            manufacturer="Arduino",
            product="Uno",
            description="Arduino Uno",
        )

        device_type = USBDetector.identify_device_type(device)
        assert device_type == "Arduino"

    def test_identify_esp32(self):
        """Test ESP32 device identification."""
        device = USBDevice(
            port="/dev/ttyUSB1",
            vid=0x303A,
            pid=0x1001,
            serial_number=None,
            manufacturer="Espressif",
            product="ESP32-S3",
            description="ESP32-S3 Dev Module",
        )

        device_type = USBDetector.identify_device_type(device)
        assert device_type == "ESP32-S2/S3"

    def test_identify_unknown(self):
        """Test unknown device identification."""
        device = USBDevice(
            port="COM5",
            vid=0x1234,
            pid=0x5678,
            serial_number=None,
            manufacturer="Unknown",
            product="Device",
            description="Some Random Device",
        )

        device_type = USBDetector.identify_device_type(device)
        assert device_type == "Unknown"

    def test_find_device_by_port(self):
        """Test finding device by port."""
        # This will return None if no device on that port
        device = USBDetector.find_device_by_port("/dev/ttyNONEXISTENT")
        assert device is None

    def test_auto_detect(self):
        """Test auto-detection."""
        device = USBDetector.auto_detect_target()
        # May be None if no devices connected
        if device:
            assert isinstance(device, USBDevice)
