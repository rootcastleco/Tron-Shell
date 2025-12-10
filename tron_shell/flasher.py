"""
Platform-specific firmware flashing implementations.
"""

import subprocess
import sys
from abc import ABC, abstractmethod
from typing import Optional, List
from pathlib import Path


class FlashError(Exception):
    """Exception raised when firmware flashing fails."""
    pass


class PlatformFlasher(ABC):
    """Base class for platform-specific flashers."""
    
    def __init__(self, port: str, verbose: bool = False):
        self.port = port
        self.verbose = verbose
    
    @abstractmethod
    def flash(self, firmware_path: str, **kwargs) -> bool:
        """
        Flash firmware to the device.
        
        Args:
            firmware_path: Path to firmware file
            **kwargs: Platform-specific options
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def verify(self, firmware_path: str) -> bool:
        """
        Verify flashed firmware.
        
        Args:
            firmware_path: Path to firmware file
            
        Returns:
            True if verification successful
        """
        pass
    
    def _run_command(self, cmd: List[str]) -> tuple[bool, str]:
        """
        Run a shell command and return result.
        
        Args:
            cmd: Command and arguments as list
            
        Returns:
            Tuple of (success, output)
        """
        try:
            if self.verbose:
                print(f"Running: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            output = result.stdout + result.stderr
            
            if self.verbose:
                print(output)
            
            return result.returncode == 0, output
            
        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except Exception as e:
            return False, str(e)


class ArduinoFlasher(PlatformFlasher):
    """Flasher for Arduino-compatible boards."""
    
    def __init__(self, port: str, verbose: bool = False, board: str = "arduino:avr:uno"):
        super().__init__(port, verbose)
        self.board = board
    
    def flash(self, firmware_path: str, **kwargs) -> bool:
        """Flash using avrdude (Arduino bootloader)."""
        board = kwargs.get('board', self.board)
        baud = kwargs.get('baud', 115200)
        
        # This is a simulation - in real implementation would use avrdude
        if not Path(firmware_path).exists():
            raise FlashError(f"Firmware file not found: {firmware_path}")
        
        if self.verbose:
            print(f"Flashing {firmware_path} to {self.port}")
            print(f"Board: {board}, Baud: {baud}")
        
        # Simulate successful flash
        return True
    
    def verify(self, firmware_path: str) -> bool:
        """Verify firmware (simulation)."""
        return True


class ESP32Flasher(PlatformFlasher):
    """Flasher for ESP32/ESP8266 boards."""
    
    def flash(self, firmware_path: str, **kwargs) -> bool:
        """Flash using esptool."""
        baud = kwargs.get('baud', 460800)
        flash_mode = kwargs.get('flash_mode', 'dio')
        flash_freq = kwargs.get('flash_freq', '40m')
        flash_size = kwargs.get('flash_size', 'detect')
        
        if not Path(firmware_path).exists():
            raise FlashError(f"Firmware file not found: {firmware_path}")
        
        if self.verbose:
            print(f"Flashing {firmware_path} to {self.port}")
            print(f"Baud: {baud}, Mode: {flash_mode}, Freq: {flash_freq}")
        
        # Simulate successful flash
        return True
    
    def verify(self, firmware_path: str) -> bool:
        """Verify firmware (simulation)."""
        return True


class STM32Flasher(PlatformFlasher):
    """Flasher for STM32 boards."""
    
    def flash(self, firmware_path: str, **kwargs) -> bool:
        """Flash using st-flash or dfu-util."""
        method = kwargs.get('method', 'stlink')
        
        if not Path(firmware_path).exists():
            raise FlashError(f"Firmware file not found: {firmware_path}")
        
        if self.verbose:
            print(f"Flashing {firmware_path} to {self.port}")
            print(f"Method: {method}")
        
        # Simulate successful flash
        return True
    
    def verify(self, firmware_path: str) -> bool:
        """Verify firmware (simulation)."""
        return True


class GenericFlasher(PlatformFlasher):
    """Generic flasher for unknown platforms."""
    
    def flash(self, firmware_path: str, **kwargs) -> bool:
        """Generic flash attempt."""
        if not Path(firmware_path).exists():
            raise FlashError(f"Firmware file not found: {firmware_path}")
        
        if self.verbose:
            print(f"Attempting generic flash of {firmware_path} to {self.port}")
            print("Warning: Using generic flasher. Specify platform for better results.")
        
        # Simulate successful flash
        return True
    
    def verify(self, firmware_path: str) -> bool:
        """Verify firmware (simulation)."""
        return True


def get_flasher(platform: str, port: str, verbose: bool = False) -> PlatformFlasher:
    """
    Get appropriate flasher for the platform.
    
    Args:
        platform: Platform name (arduino, esp32, stm32, etc.)
        port: Serial port
        verbose: Enable verbose output
        
    Returns:
        Platform-specific flasher instance
    """
    platform_lower = platform.lower()
    
    if "arduino" in platform_lower:
        return ArduinoFlasher(port, verbose)
    elif "esp32" in platform_lower or "esp8266" in platform_lower or "espressif" in platform_lower:
        return ESP32Flasher(port, verbose)
    elif "stm32" in platform_lower or "stm" in platform_lower:
        return STM32Flasher(port, verbose)
    else:
        return GenericFlasher(port, verbose)
