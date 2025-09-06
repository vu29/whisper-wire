
class InvalidCredentialsException(Exception):
    """Raised when the provided credentials are invalid."""
    pass

class InvalidRefreshTokenException(Exception):
    """Raised when the provided refresh token is invalid or expired."""
    pass