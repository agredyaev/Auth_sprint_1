class RedisRepositoryError(Exception):
    """Base class for exceptions in this module."""

    pass


class RedisCreateError(RedisRepositoryError):
    """Exception raised for errors during the creation in Redis."""

    pass


class RedisGetError(RedisRepositoryError):
    """Exception raised for errors during the retrieval from Redis."""

    pass


class RedisUpdateError(RedisRepositoryError):
    """Exception raised for errors during the update in Redis."""

    pass


class RedisDeleteError(RedisRepositoryError):
    """Exception raised for errors during the deletion from Redis."""

    pass


class RedisListError(RedisRepositoryError):
    """Exception raised for errors during the listing keys in Redis."""

    pass


class RedisConnectionError(ConnectionError):
    """Redis connection error."""

    pass
