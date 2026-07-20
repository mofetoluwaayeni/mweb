"""
MWEB - Modular Web Enumeration & Benchmarking
=============================================
A professional web reconnaissance framework.

Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Security Engineer"
__license__ = "MIT"

from .core.base import BaseModule, ModuleResult
from .config import Config

__all__ = ["BaseModule", "ModuleResult", "Config"]
