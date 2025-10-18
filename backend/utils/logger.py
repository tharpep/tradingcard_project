import logging
import sys
from pathlib import Path

def setup_logging(level: str = "INFO") -> logging.Logger:
    """Set up logging configuration for the application"""
    
    # Create logs directory if it doesn't exist
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "trading_cards.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger("trading_cards")
    logger.info("Logging initialized")
    return logger
