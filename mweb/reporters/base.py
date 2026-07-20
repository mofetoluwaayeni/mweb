"""
MWEB Base Reporter
==================
Abstract base for report generators.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path


class BaseReporter(ABC):
    """Abstract base class for report generators."""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    @abstractmethod
    def generate(self, target: str, results: Dict[str, Any]) -> str:
        """Generate report from results."""
        pass
    
    def _get_timestamp(self) -> str:
        return datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    
    def _calculate_risk_score(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall risk score."""
        score = 100
        findings = []
        
        ssl_data = results.get("ssl_tls", {}).get("data", {})
        if ssl_data.get("vulnerabilities"):
            score -= len(ssl_data["vulnerabilities"]) * 10
            for vuln in ssl_data["vulnerabilities"]:
                findings.append(f"SSL/TLS: {vuln}")
        
        http_data = results.get("http", {}).get("data", {})
        for url, headers in http_data.get("security_headers", {}).items():
            missing = headers.get("missing", [])
            score -= len(missing) * 5
        
        score = max(0, min(100, score))
        
        if score >= 80:
            rating = "Good"
        elif score >= 60:
            rating = "Fair"
        elif score >= 40:
            rating = "Poor"
        else:
            rating = "Critical"
        
        return {"score": score, "rating": rating, "findings": findings[:10]}
