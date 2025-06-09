import os

from pydantic_settings import BaseSettings

class SolarmanSettings(BaseSettings):
    """
    Solarman configuration settings loaded from environment variables.
    
    All environment variables are prefixed with SOLARMAN_.
    """
    # API credentials
    APP_ID: str
    APP_SECRET: str
    PASSWORD: str
    EMAIL: str
    
    # System identifiers
    INVERTER_SN: str
    STATION_ID: str
    
    # File paths
    WORKING_DIR: str
    CHECKPOINT_FOLDER: str
    STORAGE_PATH: str
    LOGS_PATH: str
    
    # Device and endpoint information
    DEVICE_NAME: str
    ENDPOINT_URL: str
    ENDPOINT_PORT: int

    class Config:
        env_prefix = "SOLARMAN_"

    @property
    def checkpoint_folder_path(self) -> str:
        """Returns the full path to the checkpoint folder."""
        return os.path.join(self.WORKING_DIR, self.CHECKPOINT_FOLDER)
        
    @property
    def storage_path(self) -> str:
        """Returns the full path to the storage directory."""
        return os.path.join(self.WORKING_DIR, self.STORAGE_PATH)
        
    @property
    def logs_path(self) -> str:
        """Returns the full path to the logs directory."""
        return os.path.join(self.WORKING_DIR, self.LOGS_PATH)
    
    def model_post_init(self, *args, **kwargs):
        """Create required directories after initialization."""
        os.makedirs(self.checkpoint_folder_path, exist_ok=True)
        os.makedirs(self.storage_path, exist_ok=True)
        os.makedirs(self.logs_path, exist_ok=True)

    @property
    def date_format(self) -> str:
        """Returns the date format used in the application."""
        return '%Y-%m-%d'

app_config = SolarmanSettings()