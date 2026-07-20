"""
MWEB Configuration Module
========================
Central configuration management for the MWEB framework.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import os


@dataclass
class Config:
    """Configuration settings for MWEB reconnaissance."""
    
    # HTTP Settings
    timeout: int = 30
    user_agent: str = "MWEB/1.0 Security Scanner"
    follow_redirects: bool = True
    max_redirects: int = 5
    
    # SSL/TLS Settings
    ssl_verify: bool = True
    ssl_timeout: int = 10
    
    # DNS Settings
    dns_servers: List[str] = field(default_factory=lambda: [
        "8.8.8.8", "8.8.4.4", "1.1.1.1"
    ])
    
    # Rate Limiting
    request_delay: float = 0.5
    max_retries: int = 3
    
    # Output Settings
    output_dir: str = "reports"
    log_level: str = "INFO"
    
    # Security Headers to Check
    security_headers: List[str] = field(default_factory=lambda: [
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "X-XSS-Protection",
        "Referrer-Policy",
        "Permissions-Policy",
        "Cross-Origin-Embedder-Policy",
        "Cross-Origin-Opener-Policy",
        "Cross-Origin-Resource-Policy"
    ])
    
    # Crawler Settings
    crawl_paths: List[str] = field(default_factory=lambda: [
        "/robots.txt",
        "/sitemap.xml",
        "/.well-known/security.txt",
        "/crossdomain.xml",
        "/clientaccesspolicy.xml"
    ])
    
    def __post_init__(self):
        """Ensure output directory exists."""
        os.makedirs(self.output_dir, exist_ok=True)


# Global config instance
CONFIG = Config()
