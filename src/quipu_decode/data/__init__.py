"""
QUIPU-DECODE Framework v1.0 - Data Module
Data access, conversion, and validation utilities

This module provides tools for:
- Accessing external quipu databases (Cornell University, museums)
- Converting diverse data formats to QUIPU-DECODE standard
- Validating data quality and completeness
- Managing reference collections and comparative analysis
"""

from .cornell_dataset import CornellQuipuParser, validate_cornell_conversion

__all__ = [
    "CornellQuipuParser",
    "validate_cornell_conversion"
]
