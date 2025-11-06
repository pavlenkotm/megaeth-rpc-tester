"""
Plugin system for extending RPC tester functionality.

Allows custom plugins for pre/post-test hooks, custom metrics, and exporters.
"""

from typing import Dict, List, Optional, Any, Callable
from abc import ABC, abstractmethod
import asyncio
import importlib.util
import sys
from pathlib import Path


class Plugin(ABC):
    """Base class for all plugins."""

    def __init__(self, name: str, version: str = "1.0.0"):
        """
        Initialize plugin.

        Args:
            name: Plugin name
            version: Plugin version
        """
        self.name = name
        self.version = version
        self.enabled = True

    @abstractmethod
    async def initialize(self, config: Dict[str, Any]):
        """
        Initialize plugin with configuration.

        Args:
            config: Plugin configuration
        """
        pass

    @abstractmethod
    async def cleanup(self):
        """Cleanup plugin resources."""
        pass


class TestHookPlugin(Plugin):
    """Plugin that provides test lifecycle hooks."""

    async def on_test_start(self, endpoint: str, method: str, config: Dict[str, Any]):
        """Called before test starts."""
        pass

    async def on_test_complete(self, endpoint: str, method: str, results: Dict[str, Any]):
        """Called after test completes."""
        pass

    async def on_request_start(self, endpoint: str, method: str, request_data: Dict[str, Any]):
        """Called before each request."""
        pass

    async def on_request_complete(self, endpoint: str, method: str,
                                  response_data: Dict[str, Any], latency: float):
        """Called after each request."""
        pass

    async def on_request_error(self, endpoint: str, method: str, error: Exception):
        """Called when request fails."""
        pass


class MetricsPlugin(Plugin):
    """Plugin that provides custom metrics collection."""

    @abstractmethod
    async def collect_metrics(self, endpoint: str, method: str,
                             results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect custom metrics.

        Args:
            endpoint: RPC endpoint
            method: RPC method
            results: Test results

        Returns:
            Dictionary of custom metrics
        """
        pass


class ExporterPlugin(Plugin):
    """Plugin that exports results in custom formats."""

    @abstractmethod
    async def export(self, results: Dict[str, Any], output_path: str):
        """
        Export results to file.

        Args:
            results: Test results
            output_path: Output file path
        """
        pass


class PluginManager:
    """Manage plugins and their lifecycle."""

    def __init__(self):
        """Initialize plugin manager."""
        self.plugins: Dict[str, Plugin] = {}
        self.hook_plugins: List[TestHookPlugin] = []
        self.metrics_plugins: List[MetricsPlugin] = []
        self.exporter_plugins: List[ExporterPlugin] = []

    def register_plugin(self, plugin: Plugin):
        """
        Register a plugin.

        Args:
            plugin: Plugin instance
        """
        self.plugins[plugin.name] = plugin

        # Categorize plugin
        if isinstance(plugin, TestHookPlugin):
            self.hook_plugins.append(plugin)
        if isinstance(plugin, MetricsPlugin):
            self.metrics_plugins.append(plugin)
        if isinstance(plugin, ExporterPlugin):
            self.exporter_plugins.append(plugin)

    def unregister_plugin(self, plugin_name: str):
        """Unregister a plugin."""
        if plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]

            # Remove from category lists
            if isinstance(plugin, TestHookPlugin):
                self.hook_plugins = [p for p in self.hook_plugins if p.name != plugin_name]
            if isinstance(plugin, MetricsPlugin):
                self.metrics_plugins = [p for p in self.metrics_plugins if p.name != plugin_name]
            if isinstance(plugin, ExporterPlugin):
                self.exporter_plugins = [p for p in self.exporter_plugins if p.name != plugin_name]

            del self.plugins[plugin_name]

    async def initialize_all(self, config: Dict[str, Any]):
        """Initialize all plugins."""
        tasks = []
        for plugin in self.plugins.values():
            if plugin.enabled:
                plugin_config = config.get('plugins', {}).get(plugin.name, {})
                tasks.append(plugin.initialize(plugin_config))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def cleanup_all(self):
        """Cleanup all plugins."""
        tasks = []
        for plugin in self.plugins.values():
            tasks.append(plugin.cleanup())

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def trigger_test_start(self, endpoint: str, method: str, config: Dict[str, Any]):
        """Trigger test start hooks."""
        tasks = []
        for plugin in self.hook_plugins:
            if plugin.enabled:
                tasks.append(plugin.on_test_start(endpoint, method, config))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def trigger_test_complete(self, endpoint: str, method: str, results: Dict[str, Any]):
        """Trigger test complete hooks."""
        tasks = []
        for plugin in self.hook_plugins:
            if plugin.enabled:
                tasks.append(plugin.on_test_complete(endpoint, method, results))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def trigger_request_start(self, endpoint: str, method: str, request_data: Dict[str, Any]):
        """Trigger request start hooks."""
        tasks = []
        for plugin in self.hook_plugins:
            if plugin.enabled:
                tasks.append(plugin.on_request_start(endpoint, method, request_data))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def trigger_request_complete(self, endpoint: str, method: str,
                                      response_data: Dict[str, Any], latency: float):
        """Trigger request complete hooks."""
        tasks = []
        for plugin in self.hook_plugins:
            if plugin.enabled:
                tasks.append(plugin.on_request_complete(endpoint, method, response_data, latency))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def trigger_request_error(self, endpoint: str, method: str, error: Exception):
        """Trigger request error hooks."""
        tasks = []
        for plugin in self.hook_plugins:
            if plugin.enabled:
                tasks.append(plugin.on_request_error(endpoint, method, error))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def collect_all_metrics(self, endpoint: str, method: str,
                                 results: Dict[str, Any]) -> Dict[str, Any]:
        """Collect metrics from all metrics plugins."""
        all_metrics = {}

        for plugin in self.metrics_plugins:
            if plugin.enabled:
                try:
                    metrics = await plugin.collect_metrics(endpoint, method, results)
                    all_metrics[plugin.name] = metrics
                except Exception as e:
                    print(f"Error collecting metrics from plugin {plugin.name}: {e}")

        return all_metrics

    async def export_all(self, results: Dict[str, Any], output_dir: str):
        """Export results using all exporter plugins."""
        tasks = []

        for plugin in self.exporter_plugins:
            if plugin.enabled:
                output_path = f"{output_dir}/{plugin.name}_export"
                tasks.append(plugin.export(results, output_path))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    def load_plugin_from_file(self, file_path: str) -> Optional[Plugin]:
        """
        Load plugin from Python file.

        Args:
            file_path: Path to plugin file

        Returns:
            Plugin instance or None
        """
        try:
            path = Path(file_path)
            spec = importlib.util.spec_from_file_location(path.stem, file_path)

            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[path.stem] = module
                spec.loader.exec_module(module)

                # Look for Plugin class in module
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and
                        issubclass(attr, Plugin) and
                        attr != Plugin and
                        attr != TestHookPlugin and
                        attr != MetricsPlugin and
                        attr != ExporterPlugin):

                        plugin_instance = attr()
                        self.register_plugin(plugin_instance)
                        return plugin_instance

        except Exception as e:
            print(f"Error loading plugin from {file_path}: {e}")

        return None

    def load_plugins_from_directory(self, directory: str):
        """Load all plugins from directory."""
        path = Path(directory)

        if not path.exists() or not path.is_dir():
            return

        for file_path in path.glob("*.py"):
            if file_path.stem.startswith("_"):
                continue  # Skip private modules

            self.load_plugin_from_file(str(file_path))


# Example built-in plugins

class LoggingPlugin(TestHookPlugin):
    """Example plugin that logs test events."""

    def __init__(self):
        super().__init__("logging_plugin")
        self.log_file = None

    async def initialize(self, config: Dict[str, Any]):
        """Initialize plugin."""
        log_path = config.get('log_path', 'test_events.log')
        self.log_file = open(log_path, 'a')

    async def cleanup(self):
        """Cleanup plugin."""
        if self.log_file:
            self.log_file.close()

    async def on_test_start(self, endpoint: str, method: str, config: Dict[str, Any]):
        """Log test start."""
        if self.log_file:
            self.log_file.write(f"[TEST START] {endpoint} - {method}\n")
            self.log_file.flush()

    async def on_test_complete(self, endpoint: str, method: str, results: Dict[str, Any]):
        """Log test completion."""
        if self.log_file:
            success_rate = results.get('success_rate', 0)
            self.log_file.write(
                f"[TEST COMPLETE] {endpoint} - {method} - Success Rate: {success_rate}%\n"
            )
            self.log_file.flush()


class CustomMetricsPlugin(MetricsPlugin):
    """Example plugin for collecting custom metrics."""

    def __init__(self):
        super().__init__("custom_metrics")

    async def initialize(self, config: Dict[str, Any]):
        """Initialize plugin."""
        pass

    async def cleanup(self):
        """Cleanup plugin."""
        pass

    async def collect_metrics(self, endpoint: str, method: str,
                             results: Dict[str, Any]) -> Dict[str, Any]:
        """Collect custom metrics."""
        # Example: Calculate additional custom metrics
        latencies = results.get('latencies', [])

        if latencies:
            # Calculate geometric mean
            geometric_mean = (
                sum(latencies) / len(latencies)
            ) if latencies else 0

            return {
                'geometric_mean_latency': geometric_mean,
                'total_data_points': len(latencies)
            }

        return {}
