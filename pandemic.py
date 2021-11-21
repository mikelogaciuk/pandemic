from core.database import SqlServer
import logging

logging.basicConfig(
    level=logging.DEBUG,
    # For more deep logging use this below:
    # format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)
