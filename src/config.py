import os
import logging

from pydantic_settings import BaseSettings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class SolarmanSettings(BaseSettings):
    """
    Solarman configuration settings loaded from environment variables.
    
    All environment variables are prefixed with SOLARMAN_.
    """
    # API credentials
    app_id: str
    app_secret: str
    password: str
    email: str
    
    # System identifiers
    inverter_sn: str
    station_id: str
    
    # File paths
    working_dir: str
    checkpoint_folder: str
    storage_folder: str
    logs_folder: str
    
    # Device and endpoint information
    device_name: str
    endpoint_url: str
    endpoint_port: int

    class Config:
        env_prefix = "SOLARMAN_"

    @property
    def checkpoint_folder_path(self) -> str:
        """Returns the full path to the checkpoint folder."""
        return os.path.join(self.working_dir, self.checkpoint_folder)
        
    @property
    def storage_folder_path(self) -> str:
        """Returns the full path to the storage directory."""
        return os.path.join(self.working_dir, self.storage_folder)
        
    @property
    def logs_folder_path(self) -> str:
        """Returns the full path to the logs directory."""
        return os.path.join(self.working_dir, self.logs_folder)
    
    def model_post_init(self, *args, **kwargs):
        """Create required directories after initialization."""
        os.makedirs(self.checkpoint_folder_path, exist_ok=True)
        os.makedirs(self.storage_folder_path, exist_ok=True)
        os.makedirs(self.logs_folder, exist_ok=True)

    @property
    def date_format(self) -> str:
        """Returns the date format used in the application."""
        return '%Y-%m-%d'

app_config = SolarmanSettings()