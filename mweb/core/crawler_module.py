"""
MWEB Crawler Module
===================
Discovery of robots.txt, sitemap.xml, and other files.
"""

import requests
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from urllib.parse import urljoin
from xml.etree import ElementTree as ET
from .base import BaseModule, ModuleResult


class CrawlerModule(BaseModule):
    """Web crawler for discovery files."""
    
    @property
    def module_name(self) -> str:
        return "crawler"
    
    async def run(self, target: str, protocol: str = "https") -> ModuleResult:
        """Crawl for discovery files."""
        self.logger.info(f"Crawling {target} for discovery files")
        
        results = {
            "robots_txt": None,
            "sitemap_xml": None,
            "discovered_urls": [],
            "exposed_files": []
        }
        errors = []
        
        base_url = f"{protocol}://{target}"
        paths = self.config.crawl_paths if self.config else [
            "/robots.txt", "/sitemap.xml", "/.well-known/security.txt"
        ]
        
        headers = {"User-Agent": self.config.user_agent if self.config else "MWEB/1.0"}
        
        for path in paths:
            url = urljoin(base_url, path)
            try:
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: requests.get(url, headers=headers, timeout=10)
                )
                
                if response.status_code == 200:
                    if "robots.txt" in path:
                        results["robots_txt"] = response.text
                    elif "sitemap.xml" in path:
                        results["sitemap_xml"] = self._parse_sitemap(response.text)
                    
                    results["discovered_urls"].append(url)
            
            except Exception as e:
                errors.append(f"Failed to fetch {path}: {str(e)}")
        
        return self._create_result(
            success=len(results["discovered_urls"]) > 0,
            data=results,
            errors=errors if errors else None
        )
    
    def _parse_sitemap(self, content: str) -> Dict[str, Any]:
        """Parse sitemap.xml file."""
        urls = []
        try:
            root = ET.fromstring(content)
            for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
                loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                if loc is not None and loc.text:
                    urls.append(loc.text)
        except:
            pass
        
        return {"urls": urls, "url_count": len(urls)}
