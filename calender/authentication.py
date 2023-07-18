from rest_framework.authentication import TokenAuthentication

"""Overridden the default TokenAuthentication class to change the keyword from Token to Bearer.

"""
class CustomTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'

    def authenticate(self, request):
        # Get the authorization header from the request headers
        auth_header = request.headers.get('Authorization')

        if auth_header is None:
            return None

        # Split the authorization header into keyword and token value
        keyword, token = auth_header.split(' ', 1)

        # Check if the keyword matches the expected keyword
        if keyword == self.keyword:
            # Authenticate the token and return the authenticated user
            return self.authenticate_credentials(token)

        return None