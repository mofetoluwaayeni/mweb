"""
MWEB Validation Utilities
========================
Input validation and sanitization.
"""

import re
import ipaddress
from urllib.parse import urlparse
from typing import Tuple, Optional


class ValidationError(Exception):
    """Custom validation error."""
    pass


def normalize_target(target: str) -> Tuple[str, str]:
    """Normalize and validate target input."""
    if not target or not isinstance(target, str):
        raise ValidationError("Target must be a non-empty string")
    
    # Strip whitespace and common prefixes
    target = target.strip().lower()
    
    # Extract protocol if present
    protocol = "https"
    if target.startswith("http://"):
        protocol = "http"
        target = target[7:]
    elif target.startswith("https://"):
        protocol = "https"
        target = target[8:]
    
    # Remove path, query, fragment
    target = target.split('/')[0].split('?')[0].split('#')[0]
    
    # Remove port if present
    if ':' in target:
        target = target.split(':')[0]
    
    # Validate domain format
    domain_pattern = re.compile(
        r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*'
        r'[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
    )
    
    if not domain_pattern.match(target):
        raise ValidationError(f"Invalid domain format: {target}")
    
    # Check for IP address
    try:
        ipaddress.ip_address(target)
        return target, protocol
    except ValueError:
        pass
    
    # Domain validation
    if len(target) > 253:
        raise ValidationError("Domain name exceeds maximum length")
    
    return target, protocol


def is_private_ip(ip: str) -> bool:
    """Check if IP address is private/RFC1918."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private
    except ValueError:
        return False
