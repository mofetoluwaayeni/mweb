"""
MWEB WHOIS Module
=================
Domain registration information gathering.
"""

import whois
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from .base import BaseModule, ModuleResult


class WhoisModule(BaseModule):
    """WHOIS reconnaissance module."""
    
    @property
    def module_name(self) -> str:
        return "whois"
    
    async def run(self, target: str) -> ModuleResult:
        """Gather WHOIS information for target."""
        start_time = datetime.utcnow()
        self.logger.info(f"Querying WHOIS for {target}")
        
        try:
            loop = asyncio.get_event_loop()
            w = await loop.run_in_executor(None, whois.whois, target)
            
            data = self._parse_whois(w)
            return self._create_result(success=True, data=data)
            
        except Exception as e:
            self.logger.error(f"WHOIS query failed: {e}")
            return self._create_result(success=False, errors=[str(e)])
    
    def _parse_whois(self, whois_data) -> Dict[str, Any]:
        """Parse and normalize WHOIS data."""
        def safe_date(date_val):
            if isinstance(date_val, list):
                date_val = date_val[0] if date_val else None
            if date_val and hasattr(date_val, 'isoformat'):
                return date_val.isoformat()
            return str(date_val) if date_val else None
        
        return {
            "domain_name": whois_data.domain_name,
            "registrar": whois_data.registrar,
            "creation_date": safe_date(whois_data.creation_date),
            "expiration_date": safe_date(whois_data.expiration_date),
            "updated_date": safe_date(whois_data.updated_date),
            "name_servers": whois_data.name_servers,
            "status": whois_data.status,
            "registrant_name": getattr(whois_data, 'name', None),
            "registrant_org": getattr(whois_data, 'org', None),
            "registrant_country": getattr(whois_data, 'country', None),
            "emails": whois_data.emails if isinstance(whois_data.emails, list) else [whois_data.emails] if whois_data.emails else [],
            "dnssec": getattr(whois_data, 'dnssec', None)
        }
