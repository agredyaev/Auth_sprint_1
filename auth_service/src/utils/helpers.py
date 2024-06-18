from datetime import datetime, timezone


def get_timestamp() -> datetime:
    """Get current timestamp."""
    return datetime.now(timezone.utc)
