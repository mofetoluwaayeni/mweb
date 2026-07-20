"""
MWEB Base Module
================
Abstract base class for all reconnaissance modules.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging


@dataclass
class ModuleResult:
    """Standardized result container for all modules."""
    
    module_name: str
    success: bool
    data: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    execution_time: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "module": self.module_name,
            "success": self.success,
            "timestamp": self.timestamp.isoformat(),
            "execution_time": self.execution_time,
            "data": self.data,
            "errors": self.errors
        }


class BaseModule(ABC):
    """Abstract base class for reconnaissance modules."""
    
    def __init__(self, config=None):
        """Initialize module with configuration."""
        self.config = config
        self.logger = logging.getLogger(f"mweb.{self.module_name}")
    
    @property
    @abstractmethod
    def module_name(self) -> str:
        """Return module identifier."""
        pass
    
    @abstractmethod
    async def run(self, target: str) -> ModuleResult:
        """Execute module against target."""
        pass
    
    def _create_result(
        self,
        success: bool,
        data: Optional[Dict] = None,
        errors: Optional[List[str]] = None
    ) -> ModuleResult:
        """Create standardized result object."""
        return ModuleResult(
            module_name=self.module_name,
            success=success,
            data=data or {},
            errors=errors or []
        )
