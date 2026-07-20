"""
MWEB SSL/TLS Module
===================
Certificate analysis and SSL/TLS security.
"""

import ssl
import socket
import asyncio
import certifi
from datetime import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from typing import Dict, Any, List, Optional
from .base import BaseModule, ModuleResult


class SSLModule(BaseModule):
    """SSL/TLS certificate analysis module."""
    
    @property
    def module_name(self) -> str:
        return "ssl_tls"
    
    async def run(self, target: str, port: int = 443) -> ModuleResult:
        """Analyze SSL/TLS certificate and configuration."""
        self.logger.info(f"Analyzing SSL/TLS for {target}:{port}")
        
        results = {
            "certificate": {},
            "ssl_version": None,
            "cipher_suite": None,
            "vulnerabilities": []
        }
        errors = []
        
        try:
            context = ssl.create_default_context(cafile=certifi.where())
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.config.ssl_timeout if self.config else 10)
            
            with context.wrap_socket(sock, server_hostname=target) as ssock:
                ssock.connect((target, port))
                
                results["ssl_version"] = ssock.version()
                
                cipher = ssock.cipher()
                results["cipher_suite"] = {
                    "name": cipher[0],
                    "version": cipher[1],
                    "bits": cipher[2]
                }
                
                cert_der = ssock.getpeercert(binary_form=True)
                cert = x509.load_der_x509_certificate(cert_der, default_backend())
                results["certificate"] = self._parse_certificate(cert)
                
                # Check expiration
                now = datetime.utcnow()
                if now > cert.not_valid_after:
                    results["vulnerabilities"].append("Certificate has expired")
                else:
                    days_until = (cert.not_valid_after - now).days
                    if days_until < 30:
                        results["vulnerabilities"].append(f"Certificate expires in {days_until} days")
        
        except Exception as e:
            errors.append(f"SSL analysis failed: {str(e)}")
        
        return self._create_result(
            success=len(results["certificate"]) > 0,
            data=results,
            errors=errors if errors else None
        )
    
    def _parse_certificate(self, cert: x509.Certificate) -> Dict[str, Any]:
        """Parse X.509 certificate fields."""
        def get_name_attributes(name):
            return {attr.oid._name: attr.value for attr in name}
        
        subject = get_name_attributes(cert.subject)
        issuer = get_name_attributes(cert.issuer)
        
        san_list = []
        try:
            san = cert.extensions.get_extension_for_oid(
                x509.oid.ExtensionOID.SUBJECT_ALTERNATIVE_NAME
            )
            san_list = san.value.get_values_for_type(x509.DNSName)
        except:
            pass
        
        return {
            "subject": subject,
            "issuer": issuer,
            "serial_number": str(cert.serial_number),
            "not_before": cert.not_valid_before.isoformat(),
            "not_after": cert.not_valid_after.isoformat(),
            "san": san_list
        }
