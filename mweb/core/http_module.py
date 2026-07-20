"""
MWEB HTTP Module
================
HTTP header analysis and security checks.
"""

import requests
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from urllib.parse import urljoin
from .base import BaseModule, ModuleResult


class HTTPModule(BaseModule):
    """HTTP reconnaissance module."""
    
    @property
    def module_name(self) -> str:
        return "http"
    
    async def run(self, target: str, protocol: str = "https") -> ModuleResult:
        """Analyze HTTP headers and security."""
        self.logger.info(f"Analyzing HTTP headers for {target}")
        
        results = {
            "urls_tested": [],
            "responses": {},
            "security_headers": {},
            "server_info": {},
            "technologies": []
        }
        errors = []
        
        base_url = f"{protocol}://{target}"
        urls_to_test = [base_url]
        if protocol == "https":
            urls_to_test.append(f"http://{target}")
        
        headers = {
            "User-Agent": self.config.user_agent if self.config else "MWEB/1.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        
        for url in urls_to_test:
            try:
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: requests.get(
                        url,
                        headers=headers,
                        timeout=self.config.timeout if self.config else 30,
                        allow_redirects=True,
                        verify=self.config.ssl_verify if self.config else True
                    )
                )
                
                results["urls_tested"].append(url)
                results["responses"][url] = {
                    "status_code": response.status_code,
                    "content_type": response.headers.get("Content-Type"),
                    "response_time": response.elapsed.total_seconds()
                }
                
                # Server info
                server = response.headers.get("Server", "")
                if server:
                    results["server_info"][url] = server
                
                # Security headers
                sec_headers = self.config.security_headers if self.config else []
                results["security_headers"][url] = self._analyze_security_headers(
                    response.headers, sec_headers
                )
                
            except Exception as e:
                errors.append(f"Request failed for {url}: {str(e)}")
        
        return self._create_result(
            success=len(results["urls_tested"]) > 0,
            data=results,
            errors=errors if errors else None
        )
    
    def _analyze_security_headers(self, headers: Dict[str, str], check_list: List[str]) -> Dict[str, Any]:
        """Analyze security headers presence."""
        result = {"present": {}, "missing": []}
        headers_lower = {k.lower(): v for k, v in headers.items()}
        
        for header in check_list:
            header_lower = header.lower()
            if header_lower in headers_lower:
                result["present"][header] = headers_lower[header_lower]
            else:
                result["missing"].append(header)
        
        return result
