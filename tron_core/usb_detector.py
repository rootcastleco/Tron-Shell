import usb.core
import usb.util
import platform
import serial.tools.list_ports

class USBDetector:
    """Intelligent USB device detection engine"""
    
    def __init__(self, usb_rules):
        self.usb_rules = usb_rules
        self.os_type = platform.system().lower()
    
    def detect_devices(self, verbose=False):
        """Detect all compatible USB devices"""
        detected = []
        
        # Get all serial ports
        ports = serial.tools.list_ports.comports()
        
        for port in ports:
            # Extract USB IDs where available
            vid = pid = None
            if hasattr(port, 'hwid'):
                for part in port.hwid.split():
                    if part.startswith('VID:'):
                        vid = part[4:].zfill(4)
                    elif part.startswith('PID:'):
                        pid = part[4:].zfill(4)
            
            # Match against rules
            for rule in self.usb_rules:
                if self._match_rule(rule, vid, pid, port.device, port.description):
                    device_info = {
                        'port': port.device,
                        'description': port.description,
                        'vendor_id': vid or 'unknown',
                        'product_id': pid or 'unknown',
                        'platform': rule['platform'],
                        'rule_match': rule.get('description', 'Custom Rule')
                    }
                    detected.append(device_info)
                    break
        
        if verbose:
            self._print_verbose_info(detected, ports)
        
        return detected
    
    def detect_by_platform(self, platform_name):
        """Detect devices matching specific platform"""
        devices = self.detect_devices()
        for dev in devices:
            if dev['platform'] == platform_name:
                return dev
        return None
    
    def _match_rule(self, rule, vid, pid, port_path, description):
        """Match device against detection rule"""
        # VID/PID match
        if 'vendor_id' in rule and rule['vendor_id'] != vid:
            return False
        if 'product_id' in rule and rule['product_id'] != pid:
            return False
        
        # OS-specific path matching
        if 'path_contains' in rule:
            if self.os_type in rule['path_contains']:
                if rule['path_contains'][self.os_type] not in port_path.lower():
                    return False
        
        # Description keywords
        if 'description_keywords' in rule:
            desc_lower = description.lower()
            if not any(kw in desc_lower for kw in rule['description_keywords']):
                return False
        
        return True
    
    def _print_verbose_info(self, detected, all_ports):
        """Print detailed detection information"""
        print("\n=== USB DETECTION REPORT ===")
        print(f"OS: {platform.system()} {platform.release()}")
        print(f"Total serial ports found: {len(all_ports)}")
        
        if not detected:
            print("No compatible devices found with current rules")
            print("\nAll detected ports:")
            for port in all_ports:
                print(f"- {port.device}: {port.description} ({port.hwid})")
        
        else:
            print(f"\nCompatible devices found: {len(detected)}")
            for i, dev in enumerate(detected, 1):
                print(f"\nDevice #{i}:")
                print(f"  Port: {dev['port']}")
                print(f"  Description: {dev['description']}")
                print(f"  VID:PID: {dev['vendor_id']}:{dev['product_id']}")
                print(f"  Platform: {dev['platform']}")
                print(f"  Matched rule: {dev['rule_match']}")
        
        print("\nDetection rules in use:")
        for i, rule in enumerate(self.usb_rules, 1):
            print(f"Rule #{i}:")
            print(f"  Platform: {rule.get('platform', 'N/A')}")
            print(f"  VID:PID: {rule.get('vendor_id', 'any')}:{rule.get('product_id', 'any')}")
            if 'description_keywords' in rule:
                print(f"  Keywords: {', '.join(rule['description_keywords'])}")
            if 'path_contains' in rule:
                print(f"  Path rules: {rule['path_contains']}")