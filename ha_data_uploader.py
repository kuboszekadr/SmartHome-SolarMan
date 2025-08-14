#!/usr/bin/env python3
"""
Home Assistant Data Uploader for Solarman
Reads raw data from storage and uploads to Home Assistant via REST API
"""

from src.home_assistant_uploader import HomeAssistantUploader, HomeAssistantSettings
   
ha_settings = HomeAssistantSettings()
uploader = HomeAssistantUploader(
    settings=ha_settings
    )
uploader.run_once()
