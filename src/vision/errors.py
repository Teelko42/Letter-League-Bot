from __future__ import annotations

# Error code constants
INVALID_SCREENSHOT = "INVALID_SCREENSHOT"
EXTRACTION_FAILED = "EXTRACTION_FAILED"
VALIDATION_FAILED = "VALIDATION_FAILED"


class VisNError(Exception):
    """Typed error for the vision pipeline.

    Attributes:
        code: One of INVALID_SCREENSHOT, EXTRACTION_FAILED, VALIDATION_FAILED.
        message: Human-readable description of the error.
    """

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")
