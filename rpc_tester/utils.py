"""
Utility functions for RPC Tester.
"""

import re
from typing import List, Optional, Any, Dict
from urllib.parse import urlparse
import statistics


def validate_url(url: str) -> bool:
    """
    Validate URL format.

    Args:
        url: URL to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except Exception:
        return False


def validate_ethereum_address(address: str) -> bool:
    """
    Validate Ethereum address format.

    Args:
        address: Ethereum address to validate

    Returns:
        True if valid, False otherwise
    """
    if not address:
        return False

    # Check if it starts with 0x and has 40 hex characters
    pattern = r'^0x[a-fA-F0-9]{40}$'
    return bool(re.match(pattern, address))


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string
    """
    if seconds < 1:
        return f"{seconds * 1000:.2f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def calculate_percentile(data: List[float], percentile: float) -> float:
    """
    Calculate percentile using proper quantile method.

    Args:
        data: List of values
        percentile: Percentile to calculate (0.0 to 1.0)

    Returns:
        Calculated percentile value
    """
    if not data:
        return 0.0

    try:
        return statistics.quantiles(data, n=100)[int(percentile * 100) - 1]
    except (IndexError, statistics.StatisticsError):
        # Fallback to simple method
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile)
        return sorted_data[min(index, len(sorted_data) - 1)]


def format_bytes(num_bytes: int) -> str:
    """
    Format bytes in human-readable format.

    Args:
        num_bytes: Number of bytes

    Returns:
        Formatted string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if num_bytes < 1024.0:
            return f"{num_bytes:.2f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.2f} PB"


def truncate_string(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate string to maximum length.

    Args:
        text: String to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncated

    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def get_rpc_method_params(method: str, **kwargs) -> Optional[List[Any]]:
    """
    Get default parameters for RPC methods.

    Args:
        method: RPC method name
        **kwargs: Additional parameters

    Returns:
        List of parameters or None
    """
    method_params = {
        'eth_blockNumber': [],
        'eth_chainId': [],
        'eth_gasPrice': [],
        'eth_maxPriorityFeePerGas': [],
        'net_version': [],
        'web3_clientVersion': [],
        'net_listening': [],
        'net_peerCount': [],
        'eth_protocolVersion': [],
        'eth_syncing': [],
        'eth_coinbase': [],
        'eth_mining': [],
        'eth_hashrate': [],
        'eth_accounts': [],
    }

    if method in method_params:
        return method_params[method]

    # Methods with parameters
    if method == 'eth_getBalance':
        address = kwargs.get('address', '0x0000000000000000000000000000000000000000')
        block = kwargs.get('block', 'latest')
        return [address, block]

    if method == 'eth_getBlockByNumber':
        block = kwargs.get('block', 'latest')
        full_tx = kwargs.get('full_tx', False)
        return [block, full_tx]

    if method == 'eth_getBlockByHash':
        block_hash = kwargs.get('block_hash')
        full_tx = kwargs.get('full_tx', False)
        if block_hash:
            return [block_hash, full_tx]

    if method == 'eth_getTransactionByHash':
        tx_hash = kwargs.get('tx_hash')
        if tx_hash:
            return [tx_hash]

    if method == 'eth_getTransactionReceipt':
        tx_hash = kwargs.get('tx_hash')
        if tx_hash:
            return [tx_hash]

    if method == 'eth_call':
        call_data = kwargs.get('call_data', {
            'to': '0x0000000000000000000000000000000000000000',
            'data': '0x'
        })
        block = kwargs.get('block', 'latest')
        return [call_data, block]

    if method == 'eth_estimateGas':
        tx_data = kwargs.get('tx_data', {
            'to': '0x0000000000000000000000000000000000000000',
            'data': '0x'
        })
        return [tx_data]

    if method == 'eth_getLogs':
        filter_params = kwargs.get('filter_params', {
            'fromBlock': 'latest',
            'toBlock': 'latest'
        })
        return [filter_params]

    if method == 'eth_getCode':
        address = kwargs.get('address', '0x0000000000000000000000000000000000000000')
        block = kwargs.get('block', 'latest')
        return [address, block]

    if method == 'eth_getStorageAt':
        address = kwargs.get('address')
        position = kwargs.get('position', '0x0')
        block = kwargs.get('block', 'latest')
        if address:
            return [address, position, block]

    return []


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters.

    Args:
        filename: Filename to sanitize

    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    return filename


def calculate_statistics(values: List[float]) -> Dict[str, float]:
    """
    Calculate comprehensive statistics for a list of values.

    Args:
        values: List of numeric values

    Returns:
        Dictionary with statistical measures
    """
    if not values:
        return {
            'count': 0,
            'mean': 0.0,
            'median': 0.0,
            'min': 0.0,
            'max': 0.0,
            'std_dev': 0.0,
            'variance': 0.0,
            'p50': 0.0,
            'p75': 0.0,
            'p90': 0.0,
            'p95': 0.0,
            'p99': 0.0
        }

    sorted_values = sorted(values)

    stats = {
        'count': len(values),
        'mean': statistics.mean(values),
        'median': statistics.median(values),
        'min': min(values),
        'max': max(values),
    }

    if len(values) > 1:
        stats['std_dev'] = statistics.stdev(values)
        stats['variance'] = statistics.variance(values)
    else:
        stats['std_dev'] = 0.0
        stats['variance'] = 0.0

    # Calculate percentiles
    stats['p50'] = calculate_percentile(values, 0.50)
    stats['p75'] = calculate_percentile(values, 0.75)
    stats['p90'] = calculate_percentile(values, 0.90)
    stats['p95'] = calculate_percentile(values, 0.95)
    stats['p99'] = calculate_percentile(values, 0.99)

    return stats
