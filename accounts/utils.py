from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    """
    Return dict object containing refresh_token and access_token for given user
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
