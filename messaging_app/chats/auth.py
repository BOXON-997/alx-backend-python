from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication class.

    This class currently behaves exactly like DRF SimpleJWT's
    default JWTAuthentication, but exists so the project has
    a dedicated hook where custom token validation, logging,
    or user checks can be added later if needed.

    ALX requires this file to be present as part of the
    authentication implementation.
    """
    pass
