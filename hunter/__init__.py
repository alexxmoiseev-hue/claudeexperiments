"""Minimal client for the Hunter.io API (https://hunter.io/api-documentation/v2)."""

from .client import HunterClient, HunterError

__all__ = ["HunterClient", "HunterError"]
