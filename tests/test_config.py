"""
Unit tests for configuration management.
"""

import pytest
import json
import yaml
from pathlib import Path
from rpc_tester.config import Config


def test_config_defaults():
    """Test default configuration values."""
    config = Config()

    assert config.num_requests == 10
    assert config.concurrent_requests == 5
    assert config.timeout == 30.0
    assert config.retry_attempts == 3
    assert len(config.test_methods) > 0


def test_config_custom_values():
    """Test custom configuration values."""
    config = Config(
        rpc_urls=["https://test1.com", "https://test2.com"],
        num_requests=50,
        concurrent_requests=10,
        timeout=60.0
    )

    assert config.rpc_urls == ["https://test1.com", "https://test2.com"]
    assert config.num_requests == 50
    assert config.concurrent_requests == 10
    assert config.timeout == 60.0


def test_config_to_json_file(tmp_path):
    """Test saving configuration to JSON file."""
    config = Config(
        rpc_urls=["https://test.com"],
        num_requests=25
    )

    json_file = tmp_path / "config.json"
    config.to_file(str(json_file))

    assert json_file.exists()

    with open(json_file, 'r') as f:
        data = json.load(f)

    assert data["rpc_urls"] == ["https://test.com"]
    assert data["num_requests"] == 25


def test_config_to_yaml_file(tmp_path):
    """Test saving configuration to YAML file."""
    config = Config(
        rpc_urls=["https://test.com"],
        num_requests=25
    )

    yaml_file = tmp_path / "config.yaml"
    config.to_file(str(yaml_file))

    assert yaml_file.exists()

    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)

    assert data["rpc_urls"] == ["https://test.com"]
    assert data["num_requests"] == 25


def test_config_from_json_file(tmp_path):
    """Test loading configuration from JSON file."""
    json_file = tmp_path / "config.json"

    data = {
        "rpc_urls": ["https://test.com"],
        "num_requests": 30,
        "timeout": 45.0
    }

    with open(json_file, 'w') as f:
        json.dump(data, f)

    config = Config.from_file(str(json_file))

    assert config.rpc_urls == ["https://test.com"]
    assert config.num_requests == 30
    assert config.timeout == 45.0


def test_config_from_yaml_file(tmp_path):
    """Test loading configuration from YAML file."""
    yaml_file = tmp_path / "config.yaml"

    data = {
        "rpc_urls": ["https://test.com"],
        "num_requests": 30,
        "timeout": 45.0
    }

    with open(yaml_file, 'w') as f:
        yaml.dump(data, f)

    config = Config.from_file(str(yaml_file))

    assert config.rpc_urls == ["https://test.com"]
    assert config.num_requests == 30
    assert config.timeout == 45.0


def test_config_from_nonexistent_file():
    """Test loading configuration from non-existent file."""
    with pytest.raises(FileNotFoundError):
        Config.from_file("nonexistent.yaml")


def test_config_unsupported_format(tmp_path):
    """Test unsupported configuration file format."""
    txt_file = tmp_path / "config.txt"
    txt_file.write_text("some text")

    with pytest.raises(ValueError):
        Config.from_file(str(txt_file))
