"""
Rich CLI interface for RPC Tester.
"""

import argparse
import asyncio
import sys
from pathlib import Path
from typing import Dict, List

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from rich.text import Text
from rich import box

from .core import RPCTester, EndpointStats
from .config import Config
from .reporting import Reporter


console = Console()


class CLI:
    """Command-line interface for RPC Tester."""

    def __init__(self):
        """Initialize CLI."""
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser."""

        parser = argparse.ArgumentParser(
            description="⚡ MegaETH RPC Tester - Advanced Ethereum RPC endpoint testing tool",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Test multiple RPC endpoints
  python -m rpc_tester https://eth.llamarpc.com https://rpc.ankr.com/eth

  # Test with custom number of requests
  python -m rpc_tester https://eth.llamarpc.com -n 50

  # Test specific methods only
  python -m rpc_tester https://eth.llamarpc.com -m eth_blockNumber eth_gasPrice

  # Export results to multiple formats
  python -m rpc_tester https://eth.llamarpc.com --json --csv --html

  # Use configuration file
  python -m rpc_tester --config config.yaml

  # Generate example configuration
  python -m rpc_tester --generate-config example_config.yaml
            """
        )

        parser.add_argument(
            "urls",
            nargs="*",
            help="RPC URLs to test"
        )

        parser.add_argument(
            "-c", "--config",
            help="Path to configuration file (YAML or JSON)"
        )

        parser.add_argument(
            "-n", "--num-requests",
            type=int,
            default=10,
            help="Number of requests per endpoint (default: 10)"
        )

        parser.add_argument(
            "--concurrent",
            type=int,
            default=5,
            help="Number of concurrent requests (default: 5)"
        )

        parser.add_argument(
            "-m", "--methods",
            nargs="+",
            default=["eth_blockNumber", "eth_chainId", "eth_gasPrice"],
            help="RPC methods to test (default: eth_blockNumber eth_chainId eth_gasPrice)"
        )

        parser.add_argument(
            "--timeout",
            type=float,
            default=30.0,
            help="Request timeout in seconds (default: 30)"
        )

        parser.add_argument(
            "--retry",
            type=int,
            default=3,
            help="Number of retry attempts (default: 3)"
        )

        parser.add_argument(
            "--json",
            action="store_true",
            help="Export results to JSON"
        )

        parser.add_argument(
            "--csv",
            action="store_true",
            help="Export results to CSV"
        )

        parser.add_argument(
            "--html",
            action="store_true",
            help="Export results to HTML"
        )

        parser.add_argument(
            "-o", "--output-dir",
            default="results",
            help="Output directory for reports (default: results)"
        )

        parser.add_argument(
            "-v", "--verbose",
            action="store_true",
            help="Verbose output"
        )

        parser.add_argument(
            "-q", "--quiet",
            action="store_true",
            help="Quiet mode (minimal output)"
        )

        parser.add_argument(
            "--generate-config",
            metavar="FILENAME",
            help="Generate example configuration file and exit"
        )

        return parser

    def run(self, args: List[str] = None) -> int:
        """Run the CLI."""

        parsed_args = self.parser.parse_args(args)

        # Handle config generation
        if parsed_args.generate_config:
            self._generate_config(parsed_args.generate_config)
            return 0

        # Load or create configuration
        if parsed_args.config:
            try:
                config = Config.from_file(parsed_args.config)
            except Exception as e:
                console.print(f"[red]Error loading config: {e}[/red]")
                return 1
        else:
            # Create config from CLI args
            if not parsed_args.urls:
                console.print("[red]Error: No RPC URLs provided[/red]")
                console.print("Use --help for usage information")
                return 1

            config = Config(
                rpc_urls=parsed_args.urls,
                num_requests=parsed_args.num_requests,
                concurrent_requests=parsed_args.concurrent,
                test_methods=parsed_args.methods,
                timeout=parsed_args.timeout,
                retry_attempts=parsed_args.retry,
                export_json=parsed_args.json,
                export_csv=parsed_args.csv,
                export_html=parsed_args.html,
                output_dir=parsed_args.output_dir,
                verbose=parsed_args.verbose,
                quiet=parsed_args.quiet
            )

        # Run tests
        return asyncio.run(self._run_tests(config))

    async def _run_tests(self, config: Config) -> int:
        """Run RPC tests."""

        if not config.quiet:
            self._print_header(config)

        try:
            async with RPCTester(config) as tester:
                # Run tests with progress bar
                if not config.quiet:
                    await self._run_tests_with_progress(tester, config)
                else:
                    await tester.test_all_endpoints()

                # Calculate statistics
                stats = tester.get_all_statistics()

                # Display results
                if not config.quiet:
                    self._display_results(stats, config)

                # Export results
                if config.export_json or config.export_csv or config.export_html:
                    self._export_results(stats, config)

                return 0

        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
            if config.verbose:
                console.print_exception()
            return 1

    async def _run_tests_with_progress(self, tester: RPCTester, config: Config):
        """Run tests with progress bar."""

        total_tests = len(config.rpc_urls) * len(config.test_methods) * config.num_requests

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:

            task = progress.add_task(
                "[cyan]Running RPC tests...",
                total=total_tests
            )

            for url in config.rpc_urls:
                for method in config.test_methods:
                    params = tester._get_params_for_method(method)
                    await tester.test_endpoint(url, method, params)
                    progress.advance(task, config.num_requests)

    def _print_header(self, config: Config):
        """Print header information."""

        header = Text()
        header.append("⚡ MegaETH RPC Tester\n", style="bold cyan")
        header.append(f"\nTesting {len(config.rpc_urls)} endpoint(s) with {len(config.test_methods)} method(s)\n")
        header.append(f"Requests per test: {config.num_requests} | Concurrent: {config.concurrent_requests}\n")

        console.print(Panel(header, box=box.ROUNDED))
        console.print()

    def _display_results(self, stats: Dict[str, Dict[str, EndpointStats]], config: Config):
        """Display test results in a rich table."""

        console.print("\n")
        console.print("=" * 80)
        console.print("📊 [bold cyan]Test Results[/bold cyan]")
        console.print("=" * 80)
        console.print()

        for url, methods in stats.items():
            console.print(f"\n[bold]🔗 {url}[/bold]\n")

            table = Table(box=box.ROUNDED, show_header=True, header_style="bold magenta")

            table.add_column("Method", style="cyan")
            table.add_column("Requests", justify="right")
            table.add_column("Success Rate", justify="right")
            table.add_column("Avg Latency", justify="right")

            if config.show_percentiles:
                table.add_column("P50", justify="right")
                table.add_column("P95", justify="right")
                table.add_column("P99", justify="right")

            table.add_column("Min", justify="right")
            table.add_column("Max", justify="right")

            for method, stat in methods.items():
                # Color code success rate
                if stat.success_rate >= 95:
                    success_color = "green"
                elif stat.success_rate >= 80:
                    success_color = "yellow"
                else:
                    success_color = "red"

                row = [
                    method,
                    str(stat.total_requests),
                    f"[{success_color}]{stat.success_rate:.1f}%[/{success_color}]",
                    f"{stat.avg_latency:.2f}ms"
                ]

                if config.show_percentiles:
                    row.extend([
                        f"{stat.p50_latency:.2f}ms",
                        f"{stat.p95_latency:.2f}ms",
                        f"{stat.p99_latency:.2f}ms"
                    ])

                row.extend([
                    f"{stat.min_latency:.2f}ms",
                    f"{stat.max_latency:.2f}ms"
                ])

                table.add_row(*row)

            console.print(table)

            # Show errors if any
            for method, stat in methods.items():
                if stat.errors and config.verbose:
                    console.print(f"\n[yellow]⚠️  Errors for {method}:[/yellow]")
                    for error in stat.errors[:5]:
                        console.print(f"  • {error}")

        # Comparison table if multiple endpoints
        if len(stats) > 1:
            console.print("\n")
            console.print("=" * 80)
            console.print("📈 [bold cyan]Comparison[/bold cyan]")
            console.print("=" * 80)
            console.print()

            self._display_comparison(stats)

    def _display_comparison(self, stats: Dict[str, Dict[str, EndpointStats]]):
        """Display comparison table for multiple endpoints."""

        # Get all methods
        all_methods = set()
        for methods in stats.values():
            all_methods.update(methods.keys())

        table = Table(box=box.ROUNDED, show_header=True, header_style="bold magenta")
        table.add_column("Method", style="cyan")

        for url in stats.keys():
            # Truncate long URLs for display
            display_url = url if len(url) <= 30 else url[:27] + "..."
            table.add_column(display_url, justify="center")

        for method in sorted(all_methods):
            row = [method]

            # Find best latency for this method
            latencies = []
            for url in stats.keys():
                if method in stats[url]:
                    latencies.append(stats[url][method].avg_latency)

            best_latency = min(latencies) if latencies else None

            for url in stats.keys():
                if method in stats[url]:
                    stat = stats[url][method]
                    latency_str = f"{stat.avg_latency:.1f}ms"

                    # Highlight best performer
                    if best_latency and abs(stat.avg_latency - best_latency) < 0.1:
                        latency_str = f"[bold green]{latency_str} ⚡[/bold green]"

                    # Add success rate indicator
                    if stat.success_rate >= 95:
                        indicator = "✓"
                    elif stat.success_rate >= 80:
                        indicator = "⚠"
                    else:
                        indicator = "✗"

                    row.append(f"{latency_str}\n{indicator} {stat.success_rate:.0f}%")
                else:
                    row.append("N/A")

            table.add_row(*row)

        console.print(table)

    def _export_results(self, stats: Dict[str, Dict[str, EndpointStats]], config: Config):
        """Export results to files."""

        console.print("\n")
        console.print("=" * 80)
        console.print("💾 [bold cyan]Exporting Results[/bold cyan]")
        console.print("=" * 80)
        console.print()

        reporter = Reporter(config.output_dir)

        if config.export_json:
            filepath = reporter.export_json(stats)
            console.print(f"[green]✓[/green] JSON report saved: {filepath}")

        if config.export_csv:
            filepath = reporter.export_csv(stats)
            console.print(f"[green]✓[/green] CSV report saved: {filepath}")

        if config.export_html:
            filepath = reporter.export_html(stats)
            console.print(f"[green]✓[/green] HTML report saved: {filepath}")

        console.print()

    def _generate_config(self, filename: str):
        """Generate example configuration file."""

        config = Config(
            rpc_urls=[
                "https://eth.llamarpc.com",
                "https://rpc.ankr.com/eth"
            ],
            num_requests=20,
            concurrent_requests=5,
            timeout=30.0,
            retry_attempts=3,
            retry_delay=1.0,
            test_methods=[
                "eth_blockNumber",
                "eth_chainId",
                "eth_gasPrice",
                "net_version"
            ],
            test_eth_call=False,
            test_eth_getLogs=False,
            test_address=None,
            test_block_range=100,
            export_json=True,
            export_csv=True,
            export_html=True,
            output_dir="results",
            verbose=False,
            quiet=False,
            show_percentiles=True
        )

        config.to_file(filename)
        console.print(f"[green]✓[/green] Example configuration saved to: {filename}")


def main():
    """Main entry point."""
    cli = CLI()
    sys.exit(cli.run())


if __name__ == "__main__":
    main()
