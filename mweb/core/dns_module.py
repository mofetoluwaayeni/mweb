"""
MWEB DNS Module
===============
DNS record enumeration and analysis.
"""

import dns.resolver
import dns.reversename
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from .base import BaseModule, ModuleResult


class DNSModule(BaseModule):
    """DNS reconnaissance module."""
    
    RECORD_TYPES = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA', 'PTR', 'SRV', 'CAA']
    
    @property
    def module_name(self) -> str:
        return "dns"
    
    async def run(self, target: str) -> ModuleResult:
        """Enumerate DNS records for target."""
        self.logger.info(f"Enumerating DNS records for {target}")
        
        results = {
            "records": {},
            "dns_servers": [],
            "zone_transfer": False
        }
        errors = []
        
        # Configure resolver
        resolver = dns.resolver.Resolver()
        if self.config and self.config.dns_servers:
            resolver.nameservers = self.config.dns_servers
        
        # Query each record type
        for record_type in self.RECORD_TYPES:
            try:
                answers = await asyncio.get_event_loop().run_in_executor(
                    None, 
                    lambda: resolver.resolve(target, record_type, lifetime=5)
                )
                
                records = []
                for rdata in answers:
                    if record_type == 'MX':
                        records.append({
                            "preference": rdata.preference,
                            "exchange": str(rdata.exchange)
                        })
                    elif record_type == 'SOA':
                        records.append({
                            "mname": str(rdata.mname),
                            "rname": str(rdata.rname),
                            "serial": rdata.serial
                        })
                    else:
                        records.append(str(rdata))
                
                if records:
                    results["records"][record_type] = records
                    
            except dns.resolver.NXDOMAIN:
                errors.append(f"Domain {target} does not exist")
            except dns.resolver.NoAnswer:
                pass
            except Exception as e:
                errors.append(f"{record_type} query failed: {str(e)}")
        
        success = len(results["records"]) > 0
        return self._create_result(
            success=success,
            data=results,
            errors=errors if errors else None
        )
