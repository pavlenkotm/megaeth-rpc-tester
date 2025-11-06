"""
Advanced statistical analysis for RPC test results.

Provides detailed statistical metrics, distributions, and trend analysis.
"""

import statistics
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import math


@dataclass
class StatisticalSummary:
    """Statistical summary of test results."""
    mean: float
    median: float
    mode: Optional[float]
    std_dev: float
    variance: float
    min_value: float
    max_value: float
    range: float
    p25: float  # 25th percentile
    p50: float  # 50th percentile (median)
    p75: float  # 75th percentile
    p90: float  # 90th percentile
    p95: float  # 95th percentile
    p99: float  # 99th percentile
    p999: float  # 99.9th percentile
    iqr: float  # Interquartile range
    skewness: float
    kurtosis: float
    coefficient_of_variation: float


class StatisticalAnalyzer:
    """Perform advanced statistical analysis on test results."""

    @staticmethod
    def calculate_percentile(data: List[float], percentile: float) -> float:
        """
        Calculate specific percentile from data.

        Args:
            data: List of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not data:
            return 0.0

        sorted_data = sorted(data)
        k = (len(sorted_data) - 1) * (percentile / 100)
        f = math.floor(k)
        c = math.ceil(k)

        if f == c:
            return sorted_data[int(k)]

        d0 = sorted_data[int(f)] * (c - k)
        d1 = sorted_data[int(c)] * (k - f)
        return d0 + d1

    @staticmethod
    def calculate_summary(data: List[float]) -> StatisticalSummary:
        """
        Calculate comprehensive statistical summary.

        Args:
            data: List of values

        Returns:
            StatisticalSummary object
        """
        if not data:
            return StatisticalSummary(
                mean=0, median=0, mode=None, std_dev=0, variance=0,
                min_value=0, max_value=0, range=0,
                p25=0, p50=0, p75=0, p90=0, p95=0, p99=0, p999=0,
                iqr=0, skewness=0, kurtosis=0, coefficient_of_variation=0
            )

        mean = statistics.mean(data)
        median = statistics.median(data)

        try:
            mode = statistics.mode(data)
        except statistics.StatisticsError:
            mode = None

        std_dev = statistics.stdev(data) if len(data) > 1 else 0
        variance = statistics.variance(data) if len(data) > 1 else 0
        min_value = min(data)
        max_value = max(data)
        data_range = max_value - min_value

        p25 = StatisticalAnalyzer.calculate_percentile(data, 25)
        p50 = StatisticalAnalyzer.calculate_percentile(data, 50)
        p75 = StatisticalAnalyzer.calculate_percentile(data, 75)
        p90 = StatisticalAnalyzer.calculate_percentile(data, 90)
        p95 = StatisticalAnalyzer.calculate_percentile(data, 95)
        p99 = StatisticalAnalyzer.calculate_percentile(data, 99)
        p999 = StatisticalAnalyzer.calculate_percentile(data, 99.9)

        iqr = p75 - p25

        # Calculate skewness
        n = len(data)
        if std_dev > 0:
            skewness = sum((x - mean) ** 3 for x in data) / (n * std_dev ** 3)
        else:
            skewness = 0

        # Calculate kurtosis
        if std_dev > 0:
            kurtosis = sum((x - mean) ** 4 for x in data) / (n * std_dev ** 4) - 3
        else:
            kurtosis = 0

        # Calculate coefficient of variation
        cv = (std_dev / mean * 100) if mean > 0 else 0

        return StatisticalSummary(
            mean=mean,
            median=median,
            mode=mode,
            std_dev=std_dev,
            variance=variance,
            min_value=min_value,
            max_value=max_value,
            range=data_range,
            p25=p25,
            p50=p50,
            p75=p75,
            p90=p90,
            p95=p95,
            p99=p99,
            p999=p999,
            iqr=iqr,
            skewness=skewness,
            kurtosis=kurtosis,
            coefficient_of_variation=cv
        )

    @staticmethod
    def detect_outliers(data: List[float], method: str = "iqr") -> Tuple[List[float], List[int]]:
        """
        Detect outliers in data.

        Args:
            data: List of values
            method: Detection method ('iqr' or 'zscore')

        Returns:
            Tuple of (outliers, indices)
        """
        if not data:
            return [], []

        outliers = []
        indices = []

        if method == "iqr":
            q1 = StatisticalAnalyzer.calculate_percentile(data, 25)
            q3 = StatisticalAnalyzer.calculate_percentile(data, 75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            for i, value in enumerate(data):
                if value < lower_bound or value > upper_bound:
                    outliers.append(value)
                    indices.append(i)

        elif method == "zscore":
            mean = statistics.mean(data)
            std_dev = statistics.stdev(data) if len(data) > 1 else 0

            if std_dev > 0:
                for i, value in enumerate(data):
                    z_score = abs((value - mean) / std_dev)
                    if z_score > 3:  # 3 standard deviations
                        outliers.append(value)
                        indices.append(i)

        return outliers, indices

    @staticmethod
    def calculate_trend(data: List[float]) -> Dict[str, Any]:
        """
        Calculate trend in time series data.

        Args:
            data: List of values (time-ordered)

        Returns:
            Dictionary with trend information
        """
        if len(data) < 2:
            return {
                'direction': 'stable',
                'slope': 0,
                'strength': 0
            }

        # Simple linear regression
        n = len(data)
        x = list(range(n))
        x_mean = sum(x) / n
        y_mean = sum(data) / n

        numerator = sum((x[i] - x_mean) * (data[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))

        slope = numerator / denominator if denominator != 0 else 0

        # Calculate R-squared
        ss_tot = sum((data[i] - y_mean) ** 2 for i in range(n))
        ss_res = sum((data[i] - (slope * x[i] + (y_mean - slope * x_mean))) ** 2 for i in range(n))
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

        # Determine direction
        if abs(slope) < 0.01:
            direction = 'stable'
        elif slope > 0:
            direction = 'increasing'
        else:
            direction = 'decreasing'

        return {
            'direction': direction,
            'slope': slope,
            'strength': r_squared,
            'correlation': math.sqrt(r_squared) if r_squared >= 0 else 0
        }

    @staticmethod
    def calculate_histogram(data: List[float], bins: int = 10) -> Dict[str, List]:
        """
        Calculate histogram of data.

        Args:
            data: List of values
            bins: Number of bins

        Returns:
            Dictionary with histogram data
        """
        if not data:
            return {'bins': [], 'counts': [], 'edges': []}

        min_val = min(data)
        max_val = max(data)
        bin_width = (max_val - min_val) / bins if bins > 0 else 1

        edges = [min_val + i * bin_width for i in range(bins + 1)]
        counts = [0] * bins

        for value in data:
            for i in range(bins):
                if edges[i] <= value < edges[i + 1]:
                    counts[i] += 1
                    break
            else:
                # Handle edge case for max value
                if value == max_val:
                    counts[-1] += 1

        bin_centers = [(edges[i] + edges[i + 1]) / 2 for i in range(bins)]

        return {
            'bins': bin_centers,
            'counts': counts,
            'edges': edges
        }

    @staticmethod
    def compare_distributions(data1: List[float], data2: List[float]) -> Dict[str, Any]:
        """
        Compare two distributions.

        Args:
            data1: First dataset
            data2: Second dataset

        Returns:
            Comparison metrics
        """
        if not data1 or not data2:
            return {}

        summary1 = StatisticalAnalyzer.calculate_summary(data1)
        summary2 = StatisticalAnalyzer.calculate_summary(data2)

        mean_diff = summary2.mean - summary1.mean
        median_diff = summary2.median - summary1.median
        std_diff = summary2.std_dev - summary1.std_dev

        mean_change_pct = (mean_diff / summary1.mean * 100) if summary1.mean > 0 else 0
        median_change_pct = (median_diff / summary1.median * 100) if summary1.median > 0 else 0

        return {
            'mean_difference': mean_diff,
            'median_difference': median_diff,
            'std_dev_difference': std_diff,
            'mean_change_percent': mean_change_pct,
            'median_change_percent': median_change_pct,
            'data1_summary': summary1,
            'data2_summary': summary2
        }


class PerformanceMetrics:
    """Calculate performance-specific metrics."""

    @staticmethod
    def calculate_apdex(response_times: List[float],
                       threshold: float = 500.0,
                       tolerance_multiplier: float = 4.0) -> float:
        """
        Calculate APDEX (Application Performance Index) score.

        Args:
            response_times: List of response times in milliseconds
            threshold: Threshold for satisfied requests (ms)
            tolerance_multiplier: Multiplier for tolerating threshold

        Returns:
            APDEX score (0-1)
        """
        if not response_times:
            return 0.0

        satisfied = sum(1 for t in response_times if t <= threshold)
        tolerating = sum(1 for t in response_times
                        if threshold < t <= threshold * tolerance_multiplier)

        total = len(response_times)
        apdex = (satisfied + tolerating / 2) / total

        return apdex

    @staticmethod
    def calculate_sla_compliance(response_times: List[float],
                                 sla_threshold: float,
                                 target_percentile: float = 95.0) -> Dict[str, Any]:
        """
        Calculate SLA compliance.

        Args:
            response_times: List of response times
            sla_threshold: SLA threshold value
            target_percentile: Target percentile for SLA

        Returns:
            SLA compliance metrics
        """
        if not response_times:
            return {
                'compliant': False,
                'percentile_value': 0,
                'threshold': sla_threshold,
                'compliance_rate': 0
            }

        percentile_value = StatisticalAnalyzer.calculate_percentile(
            response_times, target_percentile
        )

        compliant = percentile_value <= sla_threshold
        compliance_rate = sum(1 for t in response_times if t <= sla_threshold) / len(response_times) * 100

        return {
            'compliant': compliant,
            'percentile_value': percentile_value,
            'threshold': sla_threshold,
            'target_percentile': target_percentile,
            'compliance_rate': compliance_rate
        }

    @staticmethod
    def calculate_availability(successful: int, total: int) -> Dict[str, Any]:
        """
        Calculate availability metrics.

        Args:
            successful: Number of successful requests
            total: Total number of requests

        Returns:
            Availability metrics
        """
        if total == 0:
            return {
                'availability_percent': 0,
                'uptime_sla': '0%',
                'nines': 0
            }

        availability = (successful / total) * 100

        # Calculate "nines" (e.g., 99.9% = "three nines")
        if availability >= 100:
            nines = float('inf')
        elif availability > 0:
            nines = -math.log10(100 - availability)
        else:
            nines = 0

        # SLA classification
        if availability >= 99.99:
            sla = "99.99% (Four Nines)"
        elif availability >= 99.9:
            sla = "99.9% (Three Nines)"
        elif availability >= 99:
            sla = "99% (Two Nines)"
        elif availability >= 90:
            sla = "90%"
        else:
            sla = "Below 90%"

        return {
            'availability_percent': availability,
            'uptime_sla': sla,
            'nines': nines,
            'successful': successful,
            'failed': total - successful,
            'total': total
        }
