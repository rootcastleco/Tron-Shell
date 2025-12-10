import logging
import sys
import time
import binascii
from colorama import Fore, Style

class DebugLogger:
    """Multi-level debug logging system"""
    
    LEVELS = {
        1: "BASIC",
        2: "PROTOCOL",
        3: "HEX_DUMP",
        4: "USB_PACKET"
    }
    
    def __init__(self, config):
        self.level = 0
        self.protocol_log = config.get('protocol_log', False)
        self.verbose_errors = config.get('verbose_errors', True)
        self.keep_temp_files = config.get('keep_temp_files', False)
        self.start_time = time.time()
        
        # Setup logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler("tron_debug.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger("TronShell")
    
    def set_level(self, level):
        """Set debug level (1-4)"""
        self.level = level
        self.logger.info(f"Debug level set to {self.LEVELS.get(level, 'UNKNOWN')}")
    
    def log(self, message, level=1):
        """Log message with level requirement"""
        if self.level >= level:
            prefix = f"[{self.LEVELS.get(level, 'DEBUG')}] "
            elapsed = time.time() - self.start_time
            formatted = f"{prefix}{elapsed:.3f}s: {message}"
            
            if level == 1:
                print(f"{Fore.CYAN}{formatted}{Style.RESET_ALL}")
            elif level == 2:
                print(f"{Fore.YELLOW}{formatted}{Style.RESET_ALL}")
            elif level >= 3:
                print(f"{Fore.MAGENTA}{formatted}{Style.RESET_ALL}")
            
            self.logger.debug(formatted)
    
    def log_command(self, cmd):
        """Log executed command"""
        self.log(f"Executing: {' '.join(cmd)}", level=2)
    
    def log_output(self, output):
        """Log command output"""
        if self.level >= 2:
            self.log(f"Command Output:\n{output}", level=2)
    
    def log_hex(self, data, address=0, level=3):
        """Log hex dump of binary data"""
        if self.level >= level:
            self.log(f"Hex dump starting at 0x{address:08X}:", level)
            self.logger.debug(self._format_hex(data, address))
    
    def _format_hex(self, data, start_address=0):
        """Format binary data as hex dump"""
        lines = []
        for i in range(0, len(data), 16):
            chunk = data[i:i+16]
            hex_values = ' '.join(f'{b:02X}' for b in chunk)
            ascii_values = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
            address = start_address + i
            lines.append(f"{address:08X}  {hex_values.ljust(47)}  {ascii_values}")
        return '\n'.join(lines)
    
    def log_usb_packet(self, packet_type, data):
        """Log USB packet capture (level 4)"""
        if self.level >= 4:
            self.log(f"USB {packet_type}:", level=4)
            self.log_hex(data, level=4)
    
    def log_exception(self, exception):
        """Log exception with stack trace"""
        if self.verbose_errors:
            import traceback
            self.logger.error("Exception occurred:", exc_info=True)
            traceback.print_exception(type(exception), exception, exception.__traceback__)