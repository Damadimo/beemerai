"""
Radio Player
Manages background radio playback using sounddevice.
"""

import os
import json
import logging
import threading
from pathlib import Path
from typing import Optional
import sounddevice as sd
import soundfile as sf
import requests
import tempfile
import time

logger = logging.getLogger(__name__)


class RadioPlayer:
    """
    Background radio player using subprocess for streaming audio.
    """
    
    def __init__(self):
        """Initialize the radio player."""
        self.thread: Optional[threading.Thread] = None
        self.stop_flag = threading.Event()
        self.current_station: Optional[str] = None
        self.stations = self._load_stations()
    
    def _load_stations(self) -> dict:
        """
        Load radio stations from demo/stations.json.
        
        Returns:
            dict: Stations configuration
        """
        try:
            stations_path = Path(__file__).parent.parent / "demo" / "stations.json"
            with open(stations_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load stations: {e}")
            return {"stations": [], "default": None}
    
    def is_playing(self) -> bool:
        """
        Check if radio is currently playing.
        
        Returns:
            bool: True if radio is playing
        """
        return self.thread is not None and self.thread.is_alive()
    
    def _play_stream(self, station_url: str):
        """
        Background thread function to play radio stream.
        
        Args:
            station_url: URL of radio stream
        """
        try:
            import subprocess
            
            # Use ffplay with minimal output (it's already available via sounddevice dependencies)
            process = subprocess.Popen(
                ['ffplay', '-nodisp', '-autoexit', '-loglevel', 'quiet', station_url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # Wait for stop signal or process to end
            while not self.stop_flag.is_set():
                if process.poll() is not None:
                    # Process ended
                    break
                time.sleep(0.1)
            
            # Terminate process if still running
            if process.poll() is None:
                process.terminate()
                process.wait(timeout=2)
        
        except Exception as e:
            logger.error(f"Radio playback error: {e}")
    
    def play(self, station_name: Optional[str] = None) -> bool:
        """
        Start playing a radio station.
        
        If already playing, stops current station first.
        
        Args:
            station_name: Name of station to play (uses default if None)
        
        Returns:
            bool: True if playback started successfully
        """
        # Stop current playback if any
        if self.is_playing():
            logger.info("Stopping current radio playback")
            self.stop()
        
        # Get station to play
        if station_name is None:
            station_name = self.stations.get("default")
        
        # Find station URL
        station_url = None
        for station in self.stations.get("stations", []):
            if station["name"] == station_name:
                station_url = station["url"]
                break
        
        if not station_url:
            logger.error(f"Station not found: {station_name}")
            return False
        
        try:
            logger.info(f"Starting radio: {station_name}")
            
            # Clear stop flag and start playback thread
            self.stop_flag.clear()
            self.thread = threading.Thread(
                target=self._play_stream,
                args=(station_url,),
                daemon=True
            )
            self.thread.start()
            
            self.current_station = station_name
            logger.info(f"Radio playing: {station_name}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to start radio: {e}")
            return False
    
    def stop(self) -> None:
        """Stop radio playback."""
        if self.thread and self.thread.is_alive():
            try:
                logger.info(f"Radio stopped: {self.current_station}")
                self.stop_flag.set()
                self.thread.join(timeout=2)
            except Exception as e:
                logger.error(f"Error stopping radio: {e}")
            finally:
                self.thread = None
                self.current_station = None
    
    def get_current_station(self) -> Optional[str]:
        """
        Get the name of currently playing station.
        
        Returns:
            str: Station name, or None if not playing
        """
        return self.current_station if self.is_playing() else None


# Global radio player instance
_radio_player: Optional[RadioPlayer] = None


def get_radio_player() -> RadioPlayer:
    """
    Get or create the global radio player instance.
    
    Returns:
        RadioPlayer: Global player instance
    """
    global _radio_player
    if _radio_player is None:
        _radio_player = RadioPlayer()
    return _radio_player

