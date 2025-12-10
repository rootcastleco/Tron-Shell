"""
Bootloader management functionality.
"""

import time
import serial


class BootloaderManager:
    """Manages bootloader interactions for various platforms."""

    @staticmethod
    def reset_device(port: str, method: str = "dtr") -> bool:
        """
        Reset device to enter bootloader mode.

        Args:
            port: Serial port
            method: Reset method (dtr, rts, 1200baud)

        Returns:
            True if reset successful
        """
        try:
            if method == "1200baud":
                # Arduino Leonardo/Micro style reset
                return BootloaderManager._reset_1200baud(port)
            else:
                # Standard DTR/RTS reset
                return BootloaderManager._reset_dtr_rts(port, method)
        except Exception as e:
            print(f"Reset failed: {e}")
            return False

    @staticmethod
    def _reset_dtr_rts(port: str, signal: str) -> bool:
        """Reset using DTR or RTS signal."""
        try:
            ser = serial.Serial(port, 9600, timeout=1)

            if signal == "dtr":
                ser.setDTR(False)
                time.sleep(0.1)
                ser.setDTR(True)
            elif signal == "rts":
                ser.setRTS(False)
                time.sleep(0.1)
                ser.setRTS(True)

            time.sleep(0.5)
            ser.close()
            return True

        except Exception as e:
            print(f"DTR/RTS reset error: {e}")
            return False

    @staticmethod
    def _reset_1200baud(port: str) -> bool:
        """Reset using 1200 baud touch (Arduino Leonardo/Micro)."""
        try:
            # Open at 1200 baud
            ser = serial.Serial(port, 1200, timeout=1)
            time.sleep(0.1)
            ser.close()

            # Wait for bootloader
            time.sleep(2)
            return True

        except Exception as e:
            print(f"1200 baud reset error: {e}")
            return False

    @staticmethod
    def wait_for_port(port: str, timeout: float = 10.0) -> bool:
        """
        Wait for a port to become available.

        Args:
            port: Serial port to wait for
            timeout: Maximum time to wait in seconds

        Returns:
            True if port becomes available
        """
        import serial.tools.list_ports

        start_time = time.time()

        while time.time() - start_time < timeout:
            ports = [p.device for p in serial.tools.list_ports.comports()]
            if port in ports:
                return True
            time.sleep(0.1)

        return False

    @staticmethod
    def enter_bootloader(port: str, platform: str = "auto") -> bool:
        """
        Enter bootloader mode for the specified platform.

        Args:
            port: Serial port
            platform: Platform type (arduino, esp32, stm32, auto)

        Returns:
            True if bootloader mode entered successfully
        """
        platform_lower = platform.lower()

        if platform_lower == "esp32" or platform_lower == "espressif":
            # ESP32 bootloader entry (GPIO0 low during reset)
            print("To enter ESP32 bootloader: Hold BOOT button, press RESET, release BOOT")
            return True
        elif platform_lower == "stm32":
            # STM32 bootloader entry (BOOT0 high during reset)
            print("To enter STM32 bootloader: Set BOOT0 high, reset device")
            return True
        else:
            # Generic reset attempt
            return BootloaderManager.reset_device(port, "dtr")
