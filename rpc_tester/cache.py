"""
Caching mechanism for RPC test results.
"""

import hashlib
import json
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class CacheEntry:
    """Represents a cached test result."""

    key: str
    data: Any
    timestamp: float
    ttl: float  # Time to live in seconds

    def is_expired(self) -> bool:
        """Check if cache entry has expired."""
        return time.time() - self.timestamp > self.ttl


class ResultCache:
    """In-memory cache for RPC test results."""

    def __init__(self, default_ttl: float = 3600):
        """
        Initialize cache.

        Args:
            default_ttl: Default time-to-live in seconds (default: 1 hour)
        """
        self._cache: Dict[str, CacheEntry] = {}
        self.default_ttl = default_ttl
        self.hits = 0
        self.misses = 0

    def _generate_key(self, url: str, method: str, params: Optional[list] = None) -> str:
        """Generate cache key from request parameters."""
        key_data = {"url": url, "method": method, "params": params or []}
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_str.encode()).hexdigest()

    def get(self, url: str, method: str, params: Optional[list] = None) -> Optional[Any]:
        """
        Get cached result.

        Args:
            url: RPC endpoint URL
            method: RPC method name
            params: Method parameters

        Returns:
            Cached data if available and not expired, None otherwise
        """
        key = self._generate_key(url, method, params)

        if key in self._cache:
            entry = self._cache[key]
            if not entry.is_expired():
                self.hits += 1
                return entry.data
            else:
                # Remove expired entry
                del self._cache[key]

        self.misses += 1
        return None

    def set(
        self,
        url: str,
        method: str,
        data: Any,
        params: Optional[list] = None,
        ttl: Optional[float] = None,
    ):
        """
        Store result in cache.

        Args:
            url: RPC endpoint URL
            method: RPC method name
            data: Data to cache
            params: Method parameters
            ttl: Custom time-to-live (uses default if not specified)
        """
        key = self._generate_key(url, method, params)
        entry = CacheEntry(key=key, data=data, timestamp=time.time(), ttl=ttl or self.default_ttl)
        self._cache[key] = entry

    def clear(self):
        """Clear all cached entries."""
        self._cache.clear()
        self.hits = 0
        self.misses = 0

    def clear_expired(self):
        """Remove expired entries from cache."""
        expired_keys = [key for key, entry in self._cache.items() if entry.is_expired()]
        for key in expired_keys:
            del self._cache[key]

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0

        return {
            "size": len(self._cache),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
            "total_requests": total_requests,
        }


class PersistentCache(ResultCache):
    """File-based persistent cache for RPC test results."""

    def __init__(self, cache_dir: str = ".cache", default_ttl: float = 3600):
        """
        Initialize persistent cache.

        Args:
            cache_dir: Directory for cache files
            default_ttl: Default time-to-live in seconds
        """
        super().__init__(default_ttl)
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._load_cache()

    def _get_cache_file(self) -> Path:
        """Get cache file path."""
        return self.cache_dir / "rpc_results.json"

    def _load_cache(self):
        """Load cache from disk."""
        cache_file = self._get_cache_file()
        if cache_file.exists():
            try:
                with open(cache_file, "r") as f:
                    data = json.load(f)
                    for key, entry_data in data.items():
                        entry = CacheEntry(**entry_data)
                        if not entry.is_expired():
                            self._cache[key] = entry
            except Exception:
                # If cache file is corrupted, start fresh
                pass

    def _save_cache(self):
        """Save cache to disk."""
        cache_file = self._get_cache_file()
        data = {}
        for key, entry in self._cache.items():
            if not entry.is_expired():
                data[key] = asdict(entry)

        with open(cache_file, "w") as f:
            json.dump(data, f)

    def set(
        self,
        url: str,
        method: str,
        data: Any,
        params: Optional[list] = None,
        ttl: Optional[float] = None,
    ):
        """Store result in cache and persist to disk."""
        super().set(url, method, data, params, ttl)
        self._save_cache()

    def clear(self):
        """Clear cache and remove cache file."""
        super().clear()
        cache_file = self._get_cache_file()
        if cache_file.exists():
            cache_file.unlink()
