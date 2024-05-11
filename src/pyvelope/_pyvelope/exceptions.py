class PyvelopeError(Exception):
    """Base class for Pyvelope exceptions."""


class ConfigurationError(PyvelopeError):
    """Raised when Pyvelope is misconfigured."""

    @classmethod
    def address_not_supported(cls, address: str) -> "ConfigurationError":
        return cls(f"Address {address} not supported by any transport")
