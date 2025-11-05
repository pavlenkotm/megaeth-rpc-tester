"""
Results reporting and export functionality.
"""

import json
import csv
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from .core import EndpointStats, TestResult


class Reporter:
    """Generate reports from test results."""

    def __init__(self, output_dir: str = "results"):
        """Initialize reporter."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_json(
        self,
        stats: Dict[str, Dict[str, EndpointStats]],
        filename: str = None
    ) -> str:
        """Export results to JSON."""

        if filename is None:
            filename = f"rpc_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        filepath = self.output_dir / filename

        data = {}
        for url, methods in stats.items():
            data[url] = {}
            for method, stat in methods.items():
                data[url][method] = {
                    "total_requests": stat.total_requests,
                    "successful_requests": stat.successful_requests,
                    "failed_requests": stat.failed_requests,
                    "success_rate": stat.success_rate,
                    "avg_latency_ms": stat.avg_latency,
                    "min_latency_ms": stat.min_latency,
                    "max_latency_ms": stat.max_latency,
                    "p50_latency_ms": stat.p50_latency,
                    "p95_latency_ms": stat.p95_latency,
                    "p99_latency_ms": stat.p99_latency,
                    "errors": stat.errors[:10]  # Limit errors in output
                }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        return str(filepath)

    def export_csv(
        self,
        stats: Dict[str, Dict[str, EndpointStats]],
        filename: str = None
    ) -> str:
        """Export results to CSV."""

        if filename is None:
            filename = f"rpc_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        filepath = self.output_dir / filename

        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                "URL",
                "Method",
                "Total Requests",
                "Successful",
                "Failed",
                "Success Rate %",
                "Avg Latency (ms)",
                "Min Latency (ms)",
                "Max Latency (ms)",
                "P50 Latency (ms)",
                "P95 Latency (ms)",
                "P99 Latency (ms)"
            ])

            for url, methods in stats.items():
                for method, stat in methods.items():
                    writer.writerow([
                        url,
                        method,
                        stat.total_requests,
                        stat.successful_requests,
                        stat.failed_requests,
                        f"{stat.success_rate:.2f}",
                        f"{stat.avg_latency:.2f}",
                        f"{stat.min_latency:.2f}",
                        f"{stat.max_latency:.2f}",
                        f"{stat.p50_latency:.2f}",
                        f"{stat.p95_latency:.2f}",
                        f"{stat.p99_latency:.2f}"
                    ])

        return str(filepath)

    def export_html(
        self,
        stats: Dict[str, Dict[str, EndpointStats]],
        filename: str = None
    ) -> str:
        """Export results to HTML with styling."""

        if filename is None:
            filename = f"rpc_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

        filepath = self.output_dir / filename

        html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RPC Test Results</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }
        h2 {
            color: #555;
            margin-top: 30px;
            background: #f8f9fa;
            padding: 10px;
            border-left: 4px solid #4CAF50;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
        }
        th {
            background: #4CAF50;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }
        td {
            padding: 10px 12px;
            border-bottom: 1px solid #ddd;
        }
        tr:hover {
            background: #f5f5f5;
        }
        .success {
            color: #4CAF50;
            font-weight: bold;
        }
        .warning {
            color: #FF9800;
            font-weight: bold;
        }
        .error {
            color: #f44336;
            font-weight: bold;
        }
        .timestamp {
            color: #888;
            font-size: 14px;
        }
        .metric {
            display: inline-block;
            margin: 10px 20px 10px 0;
            padding: 10px 15px;
            background: #e3f2fd;
            border-radius: 5px;
            font-weight: 500;
        }
        .metric-value {
            color: #1976D2;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ MegaETH RPC Test Results</h1>
        <p class="timestamp">Generated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
"""

        for url, methods in stats.items():
            html += f"\n        <h2>🔗 {url}</h2>\n"

            for method, stat in methods.items():
                success_class = "success" if stat.success_rate >= 95 else "warning" if stat.success_rate >= 80 else "error"

                html += f"""
        <h3>Method: {method}</h3>
        <div class="metric">
            Total Requests: <span class="metric-value">{stat.total_requests}</span>
        </div>
        <div class="metric">
            Success Rate: <span class="metric-value {success_class}">{stat.success_rate:.2f}%</span>
        </div>
        <div class="metric">
            Avg Latency: <span class="metric-value">{stat.avg_latency:.2f}ms</span>
        </div>

        <table>
            <tr>
                <th>Metric</th>
                <th>Value</th>
            </tr>
            <tr>
                <td>Successful Requests</td>
                <td class="success">{stat.successful_requests}</td>
            </tr>
            <tr>
                <td>Failed Requests</td>
                <td class="{"error" if stat.failed_requests > 0 else ""}">{stat.failed_requests}</td>
            </tr>
            <tr>
                <td>Min Latency</td>
                <td>{stat.min_latency:.2f} ms</td>
            </tr>
            <tr>
                <td>Max Latency</td>
                <td>{stat.max_latency:.2f} ms</td>
            </tr>
            <tr>
                <td>P50 (Median)</td>
                <td>{stat.p50_latency:.2f} ms</td>
            </tr>
            <tr>
                <td>P95</td>
                <td>{stat.p95_latency:.2f} ms</td>
            </tr>
            <tr>
                <td>P99</td>
                <td>{stat.p99_latency:.2f} ms</td>
            </tr>
        </table>
"""

                if stat.errors:
                    html += f"""
        <details>
            <summary>Errors ({len(stat.errors)})</summary>
            <ul>
"""
                    for error in stat.errors[:10]:
                        html += f"                <li>{error}</li>\n"
                    html += """            </ul>
        </details>
"""

        html += """
    </div>
</body>
</html>
"""

        with open(filepath, 'w') as f:
            f.write(html)

        return str(filepath)

    def generate_comparison_table(
        self,
        stats: Dict[str, Dict[str, EndpointStats]]
    ) -> List[List[str]]:
        """Generate comparison table data."""

        headers = ["Method"] + list(stats.keys())
        rows = [headers]

        # Get all unique methods
        all_methods = set()
        for methods in stats.values():
            all_methods.update(methods.keys())

        for method in sorted(all_methods):
            row = [method]
            for url in stats.keys():
                if method in stats[url]:
                    stat = stats[url][method]
                    row.append(f"{stat.avg_latency:.1f}ms ({stat.success_rate:.0f}%)")
                else:
                    row.append("N/A")
            rows.append(row)

        return rows

    def export_markdown(
        self,
        stats: Dict[str, Dict[str, EndpointStats]],
        filename: str = None
    ) -> str:
        """Export results to Markdown."""

        if filename is None:
            filename = f"rpc_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        filepath = self.output_dir / filename

        md = f"# RPC Test Results\n\n"
        md += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        for url, methods in stats.items():
            md += f"## 🔗 {url}\n\n"

            # Create table
            md += "| Method | Requests | Success Rate | Avg Latency | Min | P50 | P95 | P99 | Max |\n"
            md += "|--------|----------|--------------|-------------|-----|-----|-----|-----|-----|\n"

            for method, stat in methods.items():
                success_emoji = "✅" if stat.success_rate >= 95 else "⚠️" if stat.success_rate >= 80 else "❌"

                md += f"| {method} | {stat.total_requests} | "
                md += f"{success_emoji} {stat.success_rate:.1f}% | "
                md += f"{stat.avg_latency:.2f}ms | "
                md += f"{stat.min_latency:.2f}ms | "
                md += f"{stat.p50_latency:.2f}ms | "
                md += f"{stat.p95_latency:.2f}ms | "
                md += f"{stat.p99_latency:.2f}ms | "
                md += f"{stat.max_latency:.2f}ms |\n"

            md += "\n"

            # Add errors if any
            has_errors = any(stat.errors for stat in methods.values())
            if has_errors:
                md += "### ⚠️ Errors\n\n"
                for method, stat in methods.items():
                    if stat.errors:
                        md += f"**{method}:**\n"
                        for error in stat.errors[:5]:
                            md += f"- {error}\n"
                        if len(stat.errors) > 5:
                            md += f"- ... and {len(stat.errors) - 5} more\n"
                        md += "\n"

        # Comparison section
        if len(stats) > 1:
            md += "## 📊 Comparison\n\n"
            md += "| Method | " + " | ".join(stats.keys()) + " |\n"
            md += "|--------|" + "|".join(["--------"] * len(stats)) + "|\n"

            # Get all methods
            all_methods = set()
            for methods in stats.values():
                all_methods.update(methods.keys())

            for method in sorted(all_methods):
                md += f"| {method} | "
                cells = []

                # Find best latency for this method
                latencies = []
                for url in stats.keys():
                    if method in stats[url]:
                        latencies.append(stats[url][method].avg_latency)
                best_latency = min(latencies) if latencies else None

                for url in stats.keys():
                    if method in stats[url]:
                        stat = stats[url][method]
                        cell = f"{stat.avg_latency:.1f}ms"

                        # Mark best performer
                        if best_latency and abs(stat.avg_latency - best_latency) < 0.1:
                            cell = f"**{cell}** ⚡"

                        # Add success indicator
                        if stat.success_rate >= 95:
                            cell += " ✅"
                        elif stat.success_rate >= 80:
                            cell += " ⚠️"
                        else:
                            cell += " ❌"

                        cells.append(cell)
                    else:
                        cells.append("N/A")

                md += " | ".join(cells) + " |\n"

            md += "\n"

        # Summary statistics
        md += "## 📈 Summary\n\n"
        md += "### Overall Statistics\n\n"

        total_requests = sum(
            stat.total_requests
            for methods in stats.values()
            for stat in methods.values()
        )
        total_successful = sum(
            stat.successful_requests
            for methods in stats.values()
            for stat in methods.values()
        )
        total_failed = sum(
            stat.failed_requests
            for methods in stats.values()
            for stat in methods.values()
        )

        md += f"- **Total Requests:** {total_requests}\n"
        md += f"- **Successful:** {total_successful} ({total_successful/total_requests*100:.1f}%)\n"
        md += f"- **Failed:** {total_failed} ({total_failed/total_requests*100:.1f}%)\n"
        md += f"- **Endpoints Tested:** {len(stats)}\n"
        md += f"- **Methods Tested:** {len(all_methods) if len(stats) > 1 else len(next(iter(stats.values())))}\n"

        with open(filepath, 'w') as f:
            f.write(md)

        return str(filepath)
