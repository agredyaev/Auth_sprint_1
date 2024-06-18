import hashlib
import uuid


def get_static_uuid(seed: str) -> uuid.UUID:
    """
    Deterministic UUID generator
    :param seed: seed string
    :return: uuid.UUID
    """
    sha = hashlib.sha256()
    sha.update(seed.encode("utf-8"))
    hash_bytes = sha.digest()[:16]
    return uuid.UUID(bytes=hash_bytes)
