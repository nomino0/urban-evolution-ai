"""Structured logging setup for Urban Evolution AI"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from loguru import logger as loguru_logger


class StructuredLogger:
    """Structured logging with JSON format support"""
    
    def __init__(self, name: str, log_file: str = None, level: str = "INFO"):
        self.name = name
        self.level = level
        self.log_file = log_file
        
        # Configure loguru
        self._configure_loguru()
    
    def _configure_loguru(self):
        """Configure loguru logger"""
        # Remove default handler
        loguru_logger.remove()
        
        # Add console handler with colored output
        loguru_logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level=self.level,
            colorize=True,
        )
        
        # Add file handler with JSON format if specified
        if self.log_file:
            log_path = Path(self.log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            loguru_logger.add(
                self.log_file,
                format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
                level=self.level,
                rotation="100 MB",
                retention="30 days",
                compression="zip",
                serialize=True,  # JSON format
            )
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        loguru_logger.bind(name=self.name, **kwargs).info(message)
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        loguru_logger.bind(name=self.name, **kwargs).debug(message)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        loguru_logger.bind(name=self.name, **kwargs).warning(message)
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        loguru_logger.bind(name=self.name, **kwargs).error(message)
    
    def exception(self, message: str, **kwargs):
        """Log exception with traceback"""
        loguru_logger.bind(name=self.name, **kwargs).exception(message)
    
    def critical(self, message: str, **kwargs):
        """Log critical message"""
        loguru_logger.bind(name=self.name, **kwargs).critical(message)


def setup_logger(name: str, log_file: str = None, level: str = "INFO") -> StructuredLogger:
    """
    Set up a structured logger
    
    Args:
        name: Logger name (usually __name__)
        log_file: Optional log file path
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        StructuredLogger instance
    """
    return StructuredLogger(name=name, log_file=log_file, level=level)


# Default application logger
app_logger = setup_logger(
    name="urban_evolution_ai",
    log_file="logs/urban_evolution.log",
    level="INFO",
)
