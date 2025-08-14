import json
import logging
import os
import requests


from datetime import datetime as dt, timedelta
from typing import Dict, Any, Optional
from time import sleep

from pydantic_settings import BaseSettings
from pydantic import BaseModel

from src.config import app_config


class HomeAssistantSettings(BaseSettings):
    """
    Home Assistant configuration settings loaded from environment variables.
    
    All environment variables are prefixed with HA_.
    """
    # Home Assistant connection settings
    url: str
    token: str
    
    upload_interval_minutes: int = 5
    run_once: bool = False
    
    sensor_prefix: str | None = "solarman"
    
    class Config:
        env_prefix = "HA_"

class HomeAssistantUploader(BaseModel):
    settings: HomeAssistantSettings

    ha_url: str | None = None
    ha_token: str | None = None
    ha_headers: Dict[str, str] = {}

    def model_post_init(self, context):
        self.ha_url = self.settings.url.rstrip('/')
        self.ha_token = self.settings.token
        self.ha_headers = {
            'Authorization': f'Bearer {self.ha_token}',
            'Content-Type': 'application/json'
        }
        logging.getLogger(__name__).setLevel(logging.INFO)

    def get_latest_data_file(self) -> Optional[str]:
        """Find the most recent data file"""
        storage_path = app_config.storage_folder_path
        
        if not os.path.exists(storage_path):
            logging.error(f"Storage path does not exist: {storage_path}")
            return None
            
        # Look for today's file first, then yesterday's
        for days_back in range(2):
            date = dt.now() - timedelta(days=days_back)
            year_month = date.strftime('%Y-%m')
            file_name = date.strftime('%Y-%m-%d.json')
            
            folder_path = os.path.join(storage_path, year_month)
            file_path = os.path.join(folder_path, file_name)
            
            if os.path.exists(file_path):
                logging.info(f"Found data file: {file_path}")
                return file_path
                
        logging.warning("No recent data files found")
        return None

    def load_raw_data(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Load raw JSON data from file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            logging.info(f"Loaded data from {file_path}")
            return data
        except Exception as e:
            logging.error(f"Error loading data from {file_path}: {e}")
            return None

    def extract_sensor_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract sensor data from raw Solarman data
        
        You'll need to adapt this based on your actual data structure
        """
        if not raw_data:
            return {}
            
        # Get the latest record or aggregate data as needed
        records = raw_data.get('stationDataItems', [])
        if not records:
            # Try different possible data structures
            if 'data' in raw_data:
                records = raw_data['data'] if isinstance(raw_data['data'], list) else [raw_data['data']]
            else:
                # If it's a single record, wrap it in a list
                records = [raw_data]
        
        # Get the most recent record
        latest_record = records[-1] if records else {}
        
        # Extract sensor values - adapt these keys based on your actual data structure
        sensors = {
            'power_generation': self._safe_get(latest_record, ['power_generation', 'generationPower', 'currentPower'], 0),
            'daily_generation': self._safe_get(latest_record, ['daily_generation', 'todayGeneration', 'dailyEnergy'], 0),
            'total_generation': self._safe_get(latest_record, ['total_generation', 'totalGeneration', 'totalEnergy'], 0),
            'inverter_temperature': self._safe_get(latest_record, ['inverter_temperature', 'temperature', 'temp'], 0),
            'grid_voltage': self._safe_get(latest_record, ['grid_voltage', 'voltage', 'gridVoltage'], 0),
            'grid_frequency': self._safe_get(latest_record, ['grid_frequency', 'frequency', 'gridFrequency'], 0),
            'efficiency': self._safe_get(latest_record, ['efficiency', 'eff'], 0),
            'status': self._safe_get(latest_record, ['status', 'deviceStatus'], 'unknown')
        }
        
        return sensors

    def _safe_get(self, data: Dict, keys: list, default=None):
        """Safely get value from dict using multiple possible keys"""
        for key in keys:
            if key in data:
                return data[key]
        return default

    def create_ha_sensor_state(self, entity_id: str, state: Any, attributes: Dict[str, Any] = None) -> bool:
        """
        Send sensor state to Home Assistant
        
        Args:
            entity_id: The entity ID (e.g., 'sensor.solarman_power_generation')
            state: The state value
            attributes: Additional attributes for the sensor
        """
        url = f"{self.ha_url}/api/states/{entity_id}"
        
        payload = {
            'state': state,
            'attributes': attributes or {}
        }
        
        try:
            response = requests.post(url, headers=self.ha_headers, json=payload)
            response.raise_for_status()
            logging.debug(f"Updated {entity_id}: {state}")
            return True
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Error updating {entity_id}: {e}")
            return False

    def upload_sensor_data(self, sensors: Dict[str, Any]) -> bool:
        """Upload all sensor data to Home Assistant"""
        if not sensors:
            logging.warning("No sensor data to upload")
            return False
            
        success_count = 0
        total_sensors = len(sensors)
        
        # Sensor configuration with units and device classes
        sensor_config = {
            'power_generation': {'unit': 'kW', 'device_class': 'power'},
            'daily_generation': {'unit': 'kWh', 'device_class': 'energy'},
            'total_generation': {'unit': 'kWh', 'device_class': 'energy'},
            'inverter_temperature': {'unit': '°C', 'device_class': 'temperature'},
            'grid_voltage': {'unit': 'V', 'device_class': 'voltage'},
            'grid_frequency': {'unit': 'Hz', 'device_class': 'frequency'},
            'efficiency': {'unit': '%', 'device_class': None},
            'status': {'unit': None, 'device_class': None}
        }
        
        timestamp = dt.now().isoformat()
        
        for sensor_name, value in sensors.items():
            if value is None:
                continue
                
            entity_id = f"sensor.{self.settings.sensor_prefix}_{sensor_name}"
            config = sensor_config.get(sensor_name, {})
            
            attributes = {
                'friendly_name': f"{self.settings.sensor_prefix.title()} {sensor_name.replace('_', ' ').title()}",
                'station_id': app_config.station_id,
                'last_updated': timestamp
            }
            
            if config.get('unit'):
                attributes['unit_of_measurement'] = config['unit']
            if config.get('device_class'):
                attributes['device_class'] = config['device_class']
                
            if self.create_ha_sensor_state(entity_id, value, attributes):
                success_count += 1
                
        logging.info(f"Successfully uploaded {success_count}/{total_sensors} sensors")
        return success_count == total_sensors

    def test_ha_connection(self) -> bool:
        """Test connection to Home Assistant"""
        try:
            response = requests.get(f"{self.ha_url}/api/", headers=self.ha_headers)
            response.raise_for_status()
            logging.info("Successfully connected to Home Assistant")
            return True
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to connect to Home Assistant: {e}")
            return False

    def run_once(self) -> bool:
        """Run a single upload cycle"""
        # Test connection first
        if not self.test_ha_connection():
            return False
            
        # Get latest data file
        data_file = self.get_latest_data_file()
        if not data_file:
            return False
            
        # Load and process data
        raw_data = self.load_raw_data(data_file)
        if not raw_data:
            return False
            
        sensors = self.extract_sensor_data(raw_data)
        if not sensors:
            logging.warning("No sensors extracted from data")
            return False
            
        # Upload to Home Assistant
        return self.upload_sensor_data(sensors)

    def run_continuous(self, interval_minutes: int = None):
        """Run continuous upload with specified interval"""
        interval = interval_minutes or self.settings.upload_interval_minutes
        logging.info(f"Starting continuous upload (interval: {interval} min)")
        
        while True:
            try:
                self.run_once()
            except Exception as e:
                logging.error(f"Error in upload cycle: {e}")
            
            sleep(interval * 60)
