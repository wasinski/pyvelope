class PyvelopeError(Exception):
    """Base class for Pyvelope exceptions."""


class ConfigurationError(PyvelopeError):
    """Raised when Pyvelope is misconfigured."""
