import subprocess
import os
from .base_platform import BasePlatform

class PlatformATmega(BasePlatform):
    """ATmega platform implementation"""
    
    def __init__(self, port, baud, debug_logger):
        super().__init__(port, baud, debug_logger)
        self.mcu_map = {
            'atmega328p': 'm328p',
            'atmega2560': 'm2560'
        }
    
    def flash_firmware(self, filename):
        """Flash firmware to ATmega device"""
        mcu = self.mcu_map.get(self.platform, 'm328p')
        programmer = 'arduino'
        
        cmd = [
            'avrdude',
            '-c', programmer,
            '-p', mcu,
            '-P', self.port,
            '-b', str(self.baud),
            '-U', f'flash:w:{filename}:i',
            '-v'
        ]
        
        self.debug_logger.log_command(cmd)
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"Flashing failed: {result.stderr}")
        
        self.debug_logger.log_output(result.stdout)
    
    def verify_firmware(self, filename):
        """Verify firmware on device"""
        mcu = self.mcu_map.get(self.platform, 'm328p')
        
        cmd = [
            'avrdude',
            '-c', 'arduino',
            '-p', mcu,
            '-P', self.port,
            '-b', str(self.baud),
            '-U', f'flash:v:{filename}:i',
            '-v'
        ]
        
        self.debug_logger.log_command(cmd)
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if 'verification error' in result.stdout.lower():
            raise RuntimeError("Verification failed: Firmware mismatch")
    
    def enter_bootloader(self):
        """Enter bootloader mode"""
        # Toggle DTR line to reset into bootloader
        import serial
        with serial.Serial(self.port, self.baud, timeout=1) as ser:
            ser.setDTR(False)
            ser.setDTR(True)
            ser.setDTR(False)
        
        self.debug_logger.log("Entered bootloader mode via DTR toggle")