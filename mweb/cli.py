"""
MWEB Command Line Interface
============================
Main entry point for the MWEB framework.
"""

import asyncio
import click
from typing import List, Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from .config import Config
from .utils.logger import setup_logger
from .utils.validators import normalize_target, ValidationError
from .core.whois_module import WhoisModule
from .core.dns_module import DNSModule
from .core.ipgeo_module import IPGeoModule
from .core.http_module import HTTPModule
from .core.ssl_module import SSLModule
from .core.crawler_module import CrawlerModule
from .reporters.markdown_reporter import MarkdownReporter
from .reporters.html_reporter import HTMLReporter


console = Console()


class MWEBScanner:
    """Main scanner orchestrator."""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.logger = setup_logger("mweb", self.config.log_level)
        self.modules = {
            "whois": WhoisModule(self.config),
            "dns": DNSModule(self.config),
            "ipgeo": IPGeoModule(self.config),
            "http": HTTPModule(self.config),
            "ssl_tls": SSLModule(self.config),
            "crawler": CrawlerModule(self.config)
        }
    
    async def scan(self, target: str, modules: Optional[List[str]] = None) -> dict:
        """Run scan against target."""
        try:
            domain, protocol = normalize_target(target)
        except ValidationError as e:
            self.logger.error(f"Invalid target: {e}")
            raise
        
        to_run = modules or list(self.modules.keys())
        results = {}
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            for module_name in to_run:
                if module_name not in self.modules:
                    continue
                
                module = self.modules[module_name]
                task = progress.add_task(f"Running {module_name}...", total=None)
                
                try:
                    if module_name == "http":
                        result = await module.run(domain, protocol)
                    elif module_name == "ssl_tls":
                        result = await module.run(domain)
                    elif module_name == "crawler":
                        result = await module.run(domain, protocol)
                    else:
                        result = await module.run(domain)
                    
                    results[module_name] = result.to_dict()
                    
                except Exception as e:
                    results[module_name] = {
                        "module": module_name,
                        "success": False,
                        "errors": [str(e)]
                    }
                
                progress.remove_task(task)
        
        return results


@click.command()
@click.argument("target")
@click.option("--modules", "-m", default=None, help="Comma-separated module list")
@click.option("--format", "-f", "output_format", default="markdown", 
              type=click.Choice(["markdown", "html", "json"]))
@click.option("--output", "-o", default="reports", help="Output directory")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
def main(target: str, modules: Optional[str], output_format: str, 
         output: str, verbose: bool):
    """MWEB - Modular Web Enumeration & Benchmarking"""
    
    config = Config()
    config.output_dir = output
    config.log_level = "DEBUG" if verbose else "INFO"
    
    console.print(f"\n[bold blue]🔒 MWEB Scanner[/bold blue]")
    console.print(f"Target: [cyan]{target}[/cyan]\n")
    
    scanner = MWEBScanner(config)
    
    module_list = None
    if modules:
        module_list = [m.strip() for m in modules.split(",")]
    
    try:
        results = asyncio.run(scanner.scan(target, module_list))
        
        if output_format == "markdown":
            reporter = MarkdownReporter(output)
        elif output_format == "html":
            reporter = HTMLReporter(output)
        else:
            import json
            from pathlib import Path
            out_file = Path(output) / f"mweb_report_{target}.json"
            out_file.write_text(json.dumps(results, indent=2))
            console.print(f"\n[green]✓ Report saved:[/green] {out_file}")
            return
        
        report_path = reporter.generate(target, results)
        console.print(f"\n[green]✓ Report generated:[/green] {report_path}")
        
        # Summary table
        table = Table(title="Scan Summary")
        table.add_column("Module", style="cyan")
        table.add_column("Status", style="green")
        
        for mod_name, result in results.items():
            status = "✓" if result.get("success") else "✗"
            style = "green" if result.get("success") else "red"
            table.add_row(mod_name, f"[{style}]{status}[/{style}]")
        
        console.print("\n")
        console.print(table)
        
    except Exception as e:
        console.print(f"\n[red]✗ Scan failed:[/red] {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
