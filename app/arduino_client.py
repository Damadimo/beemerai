"""
Arduino Client
Handles serial communication with Arduino Nano for car control.
"""

import os
import logging
import serial
import time
from typing import Optional

logger = logging.getLogger(__name__)


class ArduinoClient:
    """
    Serial communication client for Arduino Nano car controller.
    """
    
    def __init__(self):
        """Initialize Arduino client."""
        self.ser: Optional[serial.Serial] = None
        self.port = os.getenv("ARDUINO_PORT", "/dev/cu.usbserial-14320")
        self.baud = int(os.getenv("ARDUINO_BAUD", "9600"))
        self.connected = False
    
    def connect(self) -> bool:
        """
        Connect to Arduino via serial port.
        
        Returns:
            bool: True if connected successfully
        """
        try:
            logger.info(f"Connecting to Arduino on {self.port} at {self.baud} baud...")
            
            self.ser = serial.Serial(self.port, self.baud, timeout=1)
            time.sleep(2)  # Allow time for Arduino reset
            
            self.connected = True
            logger.info("Arduino connected successfully")
            return True
        
        except serial.SerialException as e:
            logger.warning(f"Arduino not connected: {e}")
            self.connected = False
            return False
        except Exception as e:
            logger.error(f"Failed to connect to Arduino: {e}")
            self.connected = False
            return False
    
    def send_run(self) -> bool:
        """
        Send RUN command to Arduino to start the cafeteria route.
        
        Returns:
            bool: True if command sent successfully
        """
        return self._send_command("RUN")
    
    def send_dance(self) -> bool:
        """
        Send DANCE command to Arduino to start the dance routine.
        
        Returns:
            bool: True if command sent successfully
        """
        return self._send_command("DANCE")
    
    def _send_command(self, command: str) -> bool:
        """
        Send a command to Arduino and read responses.
        
        Args:
            command: Command string to send (e.g., "RUN", "DANCE")
        
        Returns:
            bool: True if command sent successfully
        """
        if not self.connected:
            # Try to connect if not already connected
            if not self.connect():
                logger.warning("Arduino not available - running in simulation mode")
                return False
        
        try:
            logger.info(f"Sending {command} command to Arduino...")
            self.ser.write(f"{command}\n".encode())
            logger.info(f"Sent: {command}")
            
            # Read Arduino response
            start_time = time.time()
            while time.time() - start_time < 2:  # Read for up to 2 seconds
                if self.ser.in_waiting:
                    line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        logger.info(f"Arduino: {line}")
            
            return True
        
        except Exception as e:
            logger.error(f"Failed to send {command} command: {e}")
            return False
    
    def disconnect(self) -> None:
        """Close serial connection to Arduino."""
        if self.ser and self.connected:
            try:
                self.ser.close()
                logger.info("Arduino disconnected")
            except Exception as e:
                logger.error(f"Error disconnecting Arduino: {e}")
            finally:
                self.connected = False
                self.ser = None


# Global Arduino client instance
_arduino_client: Optional[ArduinoClient] = None


def get_arduino_client() -> ArduinoClient:
    """
    Get or create the global Arduino client instance.
    
    Returns:
        ArduinoClient: Global client instance
    """
    global _arduino_client
    if _arduino_client is None:
        _arduino_client = ArduinoClient()
    return _arduino_client

