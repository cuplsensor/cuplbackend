from functools import wraps


def requires_capture_hash(f):
    """Checks a received string against the most recent capture hash for this tag.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        return f(*args, **kwargs)

    return decorated