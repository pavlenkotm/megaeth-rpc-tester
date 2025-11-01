"""
Results reporting and export functionality with enhanced HTML reports.
"""

import json
import csv
from pathlib import Path
from typing import Dict, List
from datetime import datetime

from .core import EndpointStats, TestResult
from .logger import get_logger
from .exceptions import ExportError

logger = get_logger(__name__)


class Reporter:
    """Generate comprehensive reports from test results."""

    def __init__(self, output_dir: str = "results"):
        """
        Initialize reporter.

        Args:
            output_dir: Directory to save reports
        """
        self.output_dir = Path(output_dir)
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Initialized reporter with output directory: {self.output_dir}")
        except Exception as e:
            raise ExportError(f"Failed to create output directory: {e}")

    def export_json(
        self,
        stats: Dict[str, Dict[str, EndpointStats]],
        filename: str = None
    ) -> str:
        """
        Export results to JSON format.

        Args:
            stats: Test statistics
            filename: Optional filename (auto-generated if None)

        Returns:
            Path to saved file

        Raises:
            ExportError: If export fails
        """
        if filename is None:
            filename = f"rpc_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        filepath = self.output_dir / filename

        try:
            data = {
                "timestamp": datetime.now().isoformat(),
                "results": {}
            }

            for url, methods in stats.items():
                data["results"][url] = {}
                for method, stat in methods.items():
                    data["results"][url][method] = {
                        "total_requests": stat.total_requests,
                        "successful_requests": stat.successful_requests,
                        "failed_requests": stat.failed_requests,
                        "success_rate": round(stat.success_rate, 2),
                        "avg_latency_ms": round(stat.avg_latency, 2),
                        "min_latency_ms": round(stat.min_latency, 2),
                        "max_latency_ms": round(stat.max_latency, 2),
                        "p50_latency_ms": round(stat.p50_latency, 2),
                        "p95_latency_ms": round(stat.p95_latency, 2),
                        "p99_latency_ms": round(stat.p99_latency, 2),
                        "errors": stat.errors[:10]  # Limit errors in output
                    }

            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, sort_keys=True)

            logger.info(f"Exported JSON report to {filepath}")
            return str(filepath)

        except Exception as e:
            raise ExportError(f"Failed to export JSON: {e}")

    def export_csv(
        self,
        stats: Dict[str, Dict[str, EndpointStats]],
        filename: str = None
    ) -> str:
        """
        Export results to CSV format.

        Args:
            stats: Test statistics
            filename: Optional filename (auto-generated if None)

        Returns:
            Path to saved file

        Raises:
            ExportError: If export fails
        """
        if filename is None:
            filename = f"rpc_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        filepath = self.output_dir / filename

        try:
            with open(filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Timestamp",
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

                timestamp = datetime.now().isoformat()

                for url, methods in stats.items():
                    for method, stat in methods.items():
                        writer.writerow([
                            timestamp,
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

            logger.info(f"Exported CSV report to {filepath}")
            return str(filepath)

        except Exception as e:
            raise ExportError(f"Failed to export CSV: {e}")

    def export_html(
        self,
        stats: Dict[str, Dict[str, EndpointStats]],
        filename: str = None
    ) -> str:
        """
        Export results to enhanced HTML with charts.

        Args:
            stats: Test statistics
            filename: Optional filename (auto-generated if None)

        Returns:
            Path to saved file

        Raises:
            ExportError: If export fails
        """
        if filename is None:
            filename = f"rpc_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

        filepath = self.output_dir / filename

        try:
            html = self._generate_html_content(stats)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)

            logger.info(f"Exported HTML report to {filepath}")
            return str(filepath)

        except Exception as e:
            raise ExportError(f"Failed to export HTML: {e}")

    def _generate_html_content(self, stats: Dict[str, Dict[str, EndpointStats]]) -> str:
        """Generate enhanced HTML content with charts."""

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Prepare data for charts
        chart_data = self._prepare_chart_data(stats)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚡ RPC Test Results - {timestamp}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}

        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        header .timestamp {{
            opacity: 0.9;
            font-size: 1.1em;
        }}

        .content {{
            padding: 30px;
        }}

        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}

        .summary-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .summary-card h3 {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .summary-card .value {{
            font-size: 2.5em;
            font-weight: bold;
        }}

        .charts-section {{
            margin: 40px 0;
        }}

        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin-top: 20px;
        }}

        .chart-container {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .chart-container h3 {{
            margin-bottom: 15px;
            color: #333;
            font-size: 1.2em;
        }}

        .endpoint-section {{
            margin: 40px 0;
        }}

        .endpoint-header {{
            background: #f8f9fa;
            padding: 20px;
            border-left: 5px solid #667eea;
            border-radius: 5px;
            margin-bottom: 20px;
        }}

        .endpoint-header h2 {{
            color: #333;
            font-size: 1.5em;
            word-break: break-all;
        }}

        .method-card {{
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .method-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}

        .method-title {{
            font-size: 1.3em;
            color: #667eea;
            margin-bottom: 15px;
            font-weight: 600;
        }}

        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}

        .metric {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }}

        .metric-label {{
            font-size: 0.85em;
            color: #666;
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .metric-value {{
            font-size: 1.5em;
            font-weight: bold;
            color: #333;
        }}

        .metric-value.success {{
            color: #4CAF50;
        }}

        .metric-value.warning {{
            color: #FF9800;
        }}

        .metric-value.error {{
            color: #f44336;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}

        th {{
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}

        td {{
            padding: 12px;
            border-bottom: 1px solid #e0e0e0;
        }}

        tr:hover {{
            background: #f8f9fa;
        }}

        details {{
            margin-top: 15px;
            padding: 15px;
            background: #fff3cd;
            border-radius: 5px;
            border-left: 4px solid #ffc107;
        }}

        details summary {{
            cursor: pointer;
            font-weight: 600;
            color: #856404;
        }}

        details ul {{
            margin-top: 10px;
            margin-left: 20px;
        }}

        details li {{
            margin: 5px 0;
            color: #856404;
        }}

        footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}

        @media (max-width: 768px) {{
            .charts-grid {{
                grid-template-columns: 1fr;
            }}

            .metrics-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚡ MegaETH RPC Test Results</h1>
            <p class="timestamp">Generated: {timestamp}</p>
        </header>

        <div class="content">
"""

        # Add summary cards
        total_endpoints = len(stats)
        total_methods = sum(len(methods) for methods in stats.values())
        total_requests = sum(
            sum(stat.total_requests for stat in methods.values())
            for methods in stats.values()
        )
        avg_success_rate = sum(
            sum(stat.success_rate for stat in methods.values()) / len(methods)
            for methods in stats.values() if methods
        ) / len(stats) if stats else 0

        html += f"""
            <div class="summary">
                <div class="summary-card">
                    <h3>Endpoints Tested</h3>
                    <div class="value">{total_endpoints}</div>
                </div>
                <div class="summary-card">
                    <h3>Methods Tested</h3>
                    <div class="value">{total_methods}</div>
                </div>
                <div class="summary-card">
                    <h3>Total Requests</h3>
                    <div class="value">{total_requests}</div>
                </div>
                <div class="summary-card">
                    <h3>Avg Success Rate</h3>
                    <div class="value">{avg_success_rate:.1f}%</div>
                </div>
            </div>

            <div class="charts-section">
                <h2 style="color: #333; margin-bottom: 20px;">📊 Performance Overview</h2>
                <div class="charts-grid">
                    <div class="chart-container">
                        <h3>Average Latency Comparison</h3>
                        <canvas id="latencyChart"></canvas>
                    </div>
                    <div class="chart-container">
                        <h3>Success Rate by Endpoint</h3>
                        <canvas id="successChart"></canvas>
                    </div>
                </div>
            </div>
"""

        # Add endpoint details
        for url, methods in stats.items():
            html += f"""
            <div class="endpoint-section">
                <div class="endpoint-header">
                    <h2>🔗 {url}</h2>
                </div>
"""

            for method, stat in methods.items():
                success_class = "success" if stat.success_rate >= 95 else "warning" if stat.success_rate >= 80 else "error"

                html += f"""
                <div class="method-card">
                    <div class="method-title">{method}</div>

                    <div class="metrics-grid">
                        <div class="metric">
                            <div class="metric-label">Total Requests</div>
                            <div class="metric-value">{stat.total_requests}</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">Success Rate</div>
                            <div class="metric-value {success_class}">{stat.success_rate:.1f}%</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">Avg Latency</div>
                            <div class="metric-value">{stat.avg_latency:.2f}ms</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">P50</div>
                            <div class="metric-value">{stat.p50_latency:.2f}ms</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">P95</div>
                            <div class="metric-value">{stat.p95_latency:.2f}ms</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">P99</div>
                            <div class="metric-value">{stat.p99_latency:.2f}ms</div>
                        </div>
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
                            <td class="{'error' if stat.failed_requests > 0 else ''}">{stat.failed_requests}</td>
                        </tr>
                        <tr>
                            <td>Min Latency</td>
                            <td>{stat.min_latency:.2f} ms</td>
                        </tr>
                        <tr>
                            <td>Max Latency</td>
                            <td>{stat.max_latency:.2f} ms</td>
                        </tr>
                    </table>
"""

                if stat.errors:
                    html += f"""
                    <details>
                        <summary>⚠️ Errors ({len(stat.errors)})</summary>
                        <ul>
"""
                    for error in stat.errors[:10]:
                        html += f"                            <li>{error}</li>\n"
                    html += """                        </ul>
                    </details>
"""

                html += """
                </div>
"""

            html += """
            </div>
"""

        # Add charts JavaScript
        html += f"""
        </div>

        <footer>
            <p>Generated by MegaETH RPC Tester | {timestamp}</p>
        </footer>
    </div>

    <script>
        // Latency Comparison Chart
        const latencyCtx = document.getElementById('latencyChart');
        new Chart(latencyCtx, {{
            type: 'bar',
            data: {chart_data['latency_chart']},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        display: true,
                        position: 'top'
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: 'Latency (ms)'
                        }}
                    }}
                }}
            }}
        }});

        // Success Rate Chart
        const successCtx = document.getElementById('successChart');
        new Chart(successCtx, {{
            type: 'doughnut',
            data: {chart_data['success_chart']},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'right'
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

        return html

    def _prepare_chart_data(self, stats: Dict[str, Dict[str, EndpointStats]]) -> Dict:
        """Prepare data for charts."""

        # Prepare latency comparison data
        labels = []
        avg_latencies = []
        p95_latencies = []
        p99_latencies = []

        for url, methods in stats.items():
            for method, stat in methods.items():
                label = f"{url[:20]}.../{method}" if len(url) > 20 else f"{url}/{method}"
                labels.append(label)
                avg_latencies.append(round(stat.avg_latency, 2))
                p95_latencies.append(round(stat.p95_latency, 2))
                p99_latencies.append(round(stat.p99_latency, 2))

        latency_chart = {
            "labels": labels,
            "datasets": [
                {
                    "label": "Avg Latency",
                    "data": avg_latencies,
                    "backgroundColor": "rgba(102, 126, 234, 0.5)",
                    "borderColor": "rgba(102, 126, 234, 1)",
                    "borderWidth": 1
                },
                {
                    "label": "P95 Latency",
                    "data": p95_latencies,
                    "backgroundColor": "rgba(255, 152, 0, 0.5)",
                    "borderColor": "rgba(255, 152, 0, 1)",
                    "borderWidth": 1
                },
                {
                    "label": "P99 Latency",
                    "data": p99_latencies,
                    "backgroundColor": "rgba(244, 67, 54, 0.5)",
                    "borderColor": "rgba(244, 67, 54, 1)",
                    "borderWidth": 1
                }
            ]
        }

        # Prepare success rate data
        success_labels = []
        success_rates = []
        colors = []

        for url, methods in stats.items():
            for method, stat in methods.items():
                label = f"{url[:15]}.../{method}" if len(url) > 15 else f"{url}/{method}"
                success_labels.append(label)
                success_rates.append(round(stat.success_rate, 2))

                if stat.success_rate >= 95:
                    colors.append('rgba(76, 175, 80, 0.7)')
                elif stat.success_rate >= 80:
                    colors.append('rgba(255, 152, 0, 0.7)')
                else:
                    colors.append('rgba(244, 67, 54, 0.7)')

        success_chart = {
            "labels": success_labels,
            "datasets": [{
                "data": success_rates,
                "backgroundColor": colors,
                "borderWidth": 2,
                "borderColor": "#fff"
            }]
        }

        return {
            "latency_chart": json.dumps(latency_chart),
            "success_chart": json.dumps(success_chart)
        }

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
