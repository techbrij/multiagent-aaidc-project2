# Tests for logger.py

import pytest
import logging
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.utils.logger import configure_logging


class TestConfigureLogging:
    """Tests for configure_logging function."""

    def test_returns_logger(self):
        """Test that configure_logging returns a logger instance."""
        logger = configure_logging(name="test_logger_1")
        
        assert isinstance(logger, logging.Logger)

    def test_logger_has_name(self):
        """Test that logger has correct name."""
        logger = configure_logging(name="test_logger_2")
        
        assert logger.name == "test_logger_2"

    def test_default_name(self):
        """Test default logger name is AAIDC."""
        # Clear handlers to allow fresh configuration
        existing_logger = logging.getLogger("AAIDC")
        existing_logger.handlers = []
        
        logger = configure_logging()
        
        assert logger.name == "AAIDC"

    def test_log_level_info(self):
        """Test logger level can be set to INFO."""
        logger = configure_logging(name="test_logger_info", log_level="INFO")
        
        assert logger.level == logging.INFO

    def test_log_level_debug(self):
        """Test logger level can be set to DEBUG."""
        logger = configure_logging(name="test_logger_debug", log_level="DEBUG")
        
        assert logger.level == logging.DEBUG

    def test_log_level_warning(self):
        """Test logger level can be set to WARNING."""
        logger = configure_logging(name="test_logger_warning", log_level="WARNING")
        
        assert logger.level == logging.WARNING

    def test_log_level_case_insensitive(self):
        """Test log level is case insensitive."""
        logger = configure_logging(name="test_logger_case", log_level="info")
        
        assert logger.level == logging.INFO

    def test_has_handlers(self):
        """Test logger has handlers configured."""
        logger = configure_logging(name="test_logger_handlers")
        
        assert len(logger.handlers) > 0

    def test_avoid_duplicate_handlers(self):
        """Test that calling configure_logging twice doesn't duplicate handlers."""
        logger1 = configure_logging(name="test_logger_dup")
        handler_count1 = len(logger1.handlers)
        
        logger2 = configure_logging(name="test_logger_dup")
        handler_count2 = len(logger2.handlers)
        
        assert handler_count1 == handler_count2

    def test_creates_log_directory(self, tmp_path, monkeypatch):
        """Test that log directory is created."""
        # This is tricky since the function uses Path("logs")
        # We can verify logs directory exists after function call
        log_dir = Path("logs")
        
        configure_logging(name="test_logger_dir")
        
        assert log_dir.exists()

    def test_logger_can_log(self, caplog):
        """Test that logger can actually log messages."""
        logger = configure_logging(name="test_logger_log", log_level="DEBUG")
        
        with caplog.at_level(logging.DEBUG, logger="test_logger_log"):
            logger.debug("Test debug message")
            logger.info("Test info message")
        
        assert "Test debug message" in caplog.text
        assert "Test info message" in caplog.text

    def test_file_handler_present(self):
        """Test that file handler is configured."""
        logger = configure_logging(name="test_logger_file")
        
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
        assert len(file_handlers) >= 1

    def test_stream_handler_present(self):
        """Test that stream (console) handler is configured."""
        logger = configure_logging(name="test_logger_stream")
        
        stream_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)]
        assert len(stream_handlers) >= 1
