"""
MWEB IP Geolocation Module
==========================
IP address information and geolocation.
"""

import socket
import requests
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from .base import BaseModule, ModuleResult


class IPGeoModule(BaseModule):
    """IP and geolocation module."""
    
    GEOIP_APIS = [
        "https://ipapi.co/{ip}/json/",
        "https://ip-api.com/json/{ip}"
    ]
    
    @property
    def module_name(self) -> str:
        return "ipgeo"
    
    async def run(self, target: str) -> ModuleResult:
        """Gather IP and geolocation data."""
        self.logger.info(f"Resolving IP and geolocation for {target}")
        
        results = {
            "resolved_ips": [],
            "geolocation": {},
            "asn_info": {}
        }
        errors = []
        
        try:
            # Resolve domain to IPs
            try:
                ipv4 = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: socket.getaddrinfo(target, None, socket.AF_INET)
                )
                for addr in ipv4:
                    ip = addr[4][0]
                    if ip not in results["resolved_ips"]:
                        results["resolved_ips"].append(ip)
            except socket.gaierror:
                pass
            
            # Geolocation for first IP
            if results["resolved_ips"]:
                primary_ip = results["resolved_ips"][0]
                geo_data = await self._get_geolocation(primary_ip)
                if geo_data:
                    results["geolocation"] = geo_data
            
        except Exception as e:
            errors.append(str(e))
        
        return self._create_result(
            success=len(results["resolved_ips"]) > 0,
            data=results,
            errors=errors if errors else None
        )
    
    async def _get_geolocation(self, ip: str) -> Optional[Dict[str, Any]]:
        """Fetch geolocation data for IP."""
        for api_url in self.GEOIP_APIS:
            try:
                url = api_url.format(ip=ip)
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: requests.get(url, timeout=10)
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "ip": data.get("ip") or data.get("query"),
                        "city": data.get("city"),
                        "region": data.get("region") or data.get("regionName"),
                        "country": data.get("country") or data.get("country_name"),
                        "latitude": data.get("lat") or data.get("latitude"),
                        "longitude": data.get("lon") or data.get("longitude"),
                        "isp": data.get("isp") or data.get("org")
                    }
            except Exception:
                continue
        return None
