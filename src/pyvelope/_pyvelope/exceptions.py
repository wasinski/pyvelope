class PyvelopeError(Exception):
    """Base class for Pyvelope exceptions."""
    pass


class ConfigurationError(PyvelopeError):
    """Raised when Pyvelope is misconfigured."""

    pass
