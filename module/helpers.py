"""Helper utilities."""

import uuid

def generate_id() -> str:
    """Generate a short unique ID for temporary directories."""
    return uuid.uuid4().hex[:8]
