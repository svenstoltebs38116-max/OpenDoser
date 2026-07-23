"""Exceptions for OpenDoser."""

from __future__ import annotations


class OpenDoserError(Exception):
    """Base exception for OpenDoser."""


class ValidationError(OpenDoserError):
    """Validation error."""


class DuplicateIdError(ValidationError):
    """Duplicate object ID."""


class ObjectNotFoundError(ValidationError):
    """Object not found."""


class ObjectInUseError(ValidationError):
    """Object is still referenced by another object."""