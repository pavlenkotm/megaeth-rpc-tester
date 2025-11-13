"""
Benchmark scoring and ranking system for RPC endpoints.

Compare and rank endpoints based on multiple performance criteria.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class ScoringCriteria(Enum):
    """Criteria for scoring endpoints."""

    LATENCY = "latency"
    SUCCESS_RATE = "success_rate"
    CONSISTENCY = "consistency"  # Low variance
    AVAILABILITY = "availability"
    THROUGHPUT = "throughput"


@dataclass
class BenchmarkScore:
    """Benchmark score for an endpoint."""

    endpoint: str
    overall_score: float
    criteria_scores: Dict[str, float]
    rank: int
    grade: str  # A, B, C, D, F
    details: Dict[str, Any]


class BenchmarkScorer:
    """Calculate benchmark scores for RPC endpoints."""

    def __init__(self, weights: Optional[Dict[ScoringCriteria, float]] = None):
        """
        Initialize benchmark scorer.

        Args:
            weights: Custom weights for scoring criteria (must sum to 1.0)
        """
        self.weights = weights or {
            ScoringCriteria.LATENCY: 0.35,
            ScoringCriteria.SUCCESS_RATE: 0.30,
            ScoringCriteria.CONSISTENCY: 0.20,
            ScoringCriteria.AVAILABILITY: 0.10,
            ScoringCriteria.THROUGHPUT: 0.05,
        }

        # Validate weights sum to 1.0
        total = sum(self.weights.values())
        if abs(total - 1.0) > 0.001:
            raise ValueError(f"Weights must sum to 1.0, got {total}")

    def calculate_score(
        self,
        endpoint: str,
        results: Dict[str, Any],
        reference_values: Optional[Dict[str, float]] = None,
    ) -> BenchmarkScore:
        """
        Calculate benchmark score for endpoint.

        Args:
            endpoint: Endpoint URL
            results: Test results
            reference_values: Reference values for normalization

        Returns:
            BenchmarkScore object
        """
        criteria_scores = {}

        # Calculate individual criteria scores
        criteria_scores["latency"] = self._score_latency(
            results, reference_values.get("latency", 1000.0) if reference_values else 1000.0
        )

        criteria_scores["success_rate"] = self._score_success_rate(results)

        criteria_scores["consistency"] = self._score_consistency(results)

        criteria_scores["availability"] = self._score_availability(results)

        criteria_scores["throughput"] = self._score_throughput(results)

        # Calculate weighted overall score
        overall_score = sum(
            criteria_scores[criterion.value] * weight for criterion, weight in self.weights.items()
        )

        # Normalize to 0-100 scale
        overall_score = max(0, min(100, overall_score))

        # Determine grade
        grade = self._calculate_grade(overall_score)

        return BenchmarkScore(
            endpoint=endpoint,
            overall_score=overall_score,
            criteria_scores=criteria_scores,
            rank=0,  # Will be set during ranking
            grade=grade,
            details=results,
        )

    def _score_latency(self, results: Dict[str, Any], target_latency: float) -> float:
        """
        Score based on latency (lower is better).

        Args:
            results: Test results
            target_latency: Target latency in ms

        Returns:
            Score from 0-100
        """
        avg_latency = results.get("avg_latency_ms", float("inf"))

        if avg_latency == 0:
            return 100

        # Score decreases as latency increases relative to target
        ratio = target_latency / avg_latency
        score = ratio * 100

        return max(0, min(100, score))

    def _score_success_rate(self, results: Dict[str, Any]) -> float:
        """
        Score based on success rate.

        Args:
            results: Test results

        Returns:
            Score from 0-100
        """
        success_rate = results.get("success_rate", 0)
        return success_rate  # Already 0-100

    def _score_consistency(self, results: Dict[str, Any]) -> float:
        """
        Score based on consistency (low variance).

        Args:
            results: Test results

        Returns:
            Score from 0-100
        """
        # Use coefficient of variation as consistency metric
        avg_latency = results.get("avg_latency_ms", 0)
        std_dev = results.get("std_dev_latency_ms", 0)

        if avg_latency == 0:
            return 0

        cv = (std_dev / avg_latency) * 100  # Coefficient of variation

        # Lower CV is better
        # CV < 10% is excellent, CV > 50% is poor
        if cv < 10:
            score = 100
        elif cv < 20:
            score = 90
        elif cv < 30:
            score = 70
        elif cv < 50:
            score = 50
        else:
            score = max(0, 50 - (cv - 50))

        return score

    def _score_availability(self, results: Dict[str, Any]) -> float:
        """
        Score based on availability.

        Args:
            results: Test results

        Returns:
            Score from 0-100
        """
        total = results.get("total_requests", 0)
        successful = results.get("successful_requests", 0)

        if total == 0:
            return 0

        availability = (successful / total) * 100
        return availability

    def _score_throughput(self, results: Dict[str, Any]) -> float:
        """
        Score based on throughput.

        Args:
            results: Test results

        Returns:
            Score from 0-100
        """
        # Throughput = requests per second
        total_requests = results.get("total_requests", 0)
        total_time = results.get("total_time_seconds", 1)

        if total_time == 0:
            return 0

        throughput = total_requests / total_time

        # Normalize: 100+ req/s = 100 score, 0 req/s = 0 score
        target_throughput = 100
        score = (throughput / target_throughput) * 100

        return min(100, score)

    def _calculate_grade(self, score: float) -> str:
        """Calculate letter grade from score."""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def rank_endpoints(self, scores: List[BenchmarkScore]) -> List[BenchmarkScore]:
        """
        Rank endpoints by score.

        Args:
            scores: List of benchmark scores

        Returns:
            Ranked list of scores
        """
        # Sort by overall score (descending)
        sorted_scores = sorted(scores, key=lambda x: x.overall_score, reverse=True)

        # Assign ranks
        for i, score in enumerate(sorted_scores):
            score.rank = i + 1

        return sorted_scores


class BenchmarkComparator:
    """Compare multiple endpoints and generate comparison reports."""

    @staticmethod
    def compare_endpoints(
        results: Dict[str, Dict[str, Any]], scorer: Optional[BenchmarkScorer] = None
    ) -> List[BenchmarkScore]:
        """
        Compare multiple endpoints.

        Args:
            results: Dictionary of endpoint -> results
            scorer: Custom scorer (optional)

        Returns:
            Ranked list of benchmark scores
        """
        if scorer is None:
            scorer = BenchmarkScorer()

        scores = []

        for endpoint, endpoint_results in results.items():
            # Aggregate results across all methods
            aggregated = BenchmarkComparator._aggregate_results(endpoint_results)
            score = scorer.calculate_score(endpoint, aggregated)
            scores.append(score)

        return scorer.rank_endpoints(scores)

    @staticmethod
    def _aggregate_results(method_results: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregate results across multiple methods."""
        if not method_results:
            return {}

        # Calculate averages across all methods
        total_requests = 0
        successful_requests = 0
        all_latencies = []
        total_time = 0

        for method_stats in method_results.values():
            total_requests += method_stats.get("total_requests", 0)
            successful_requests += method_stats.get("successful_requests", 0)
            all_latencies.append(method_stats.get("avg_latency_ms", 0))

        avg_latency = sum(all_latencies) / len(all_latencies) if all_latencies else 0
        success_rate = (successful_requests / total_requests * 100) if total_requests > 0 else 0

        # Calculate standard deviation of latencies
        if len(all_latencies) > 1:
            mean = avg_latency
            variance = sum((x - mean) ** 2 for x in all_latencies) / len(all_latencies)
            std_dev = variance**0.5
        else:
            std_dev = 0

        return {
            "avg_latency_ms": avg_latency,
            "success_rate": success_rate,
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "std_dev_latency_ms": std_dev,
            "total_time_seconds": total_time or 1,
        }

    @staticmethod
    def generate_comparison_table(scores: List[BenchmarkScore]) -> str:
        """Generate ASCII comparison table."""
        if not scores:
            return "No benchmark scores available."

        lines = ["=" * 100, "ENDPOINT BENCHMARK COMPARISON", "=" * 100, ""]

        # Header
        header = f"{'Rank':<6} {'Grade':<7} {'Score':<8} {'Endpoint':<40} {'Details':<30}"
        lines.append(header)
        lines.append("-" * 100)

        # Rows
        for score in scores:
            details = (
                f"Latency: {score.criteria_scores.get('latency', 0):.1f} | "
                f"Success: {score.criteria_scores.get('success_rate', 0):.1f}"
            )

            row = (
                f"#{score.rank:<5} "
                f"{score.grade:<7} "
                f"{score.overall_score:<7.2f} "
                f"{score.endpoint[:38]:<40} "
                f"{details[:28]:<30}"
            )
            lines.append(row)

        lines.append("=" * 100)

        return "\n".join(lines)

    @staticmethod
    def find_best_endpoint(
        scores: List[BenchmarkScore], criterion: Optional[ScoringCriteria] = None
    ) -> Optional[BenchmarkScore]:
        """
        Find best endpoint overall or by specific criterion.

        Args:
            scores: List of benchmark scores
            criterion: Specific criterion to optimize for

        Returns:
            Best benchmark score
        """
        if not scores:
            return None

        if criterion:
            return max(scores, key=lambda x: x.criteria_scores.get(criterion.value, 0))
        else:
            return max(scores, key=lambda x: x.overall_score)

    @staticmethod
    def generate_recommendations(scores: List[BenchmarkScore]) -> List[str]:
        """Generate recommendations based on benchmark results."""
        if not scores:
            return ["No data available for recommendations."]

        recommendations = []

        # Find best overall
        best = max(scores, key=lambda x: x.overall_score)
        recommendations.append(
            f"Best overall endpoint: {best.endpoint} (Score: {best.overall_score:.2f}, Grade: {best.grade})"
        )

        # Find best by criteria
        criteria_leaders = {
            "Lowest Latency": max(scores, key=lambda x: x.criteria_scores.get("latency", 0)),
            "Highest Success Rate": max(
                scores, key=lambda x: x.criteria_scores.get("success_rate", 0)
            ),
            "Most Consistent": max(scores, key=lambda x: x.criteria_scores.get("consistency", 0)),
        }

        for criterion_name, leader in criteria_leaders.items():
            recommendations.append(f"{criterion_name}: {leader.endpoint}")

        # Identify underperformers
        poor_performers = [s for s in scores if s.grade in ["D", "F"]]
        if poor_performers:
            recommendations.append(
                f"\nWarning: {len(poor_performers)} endpoint(s) with poor performance (Grade D/F)"
            )

        return recommendations
