class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Paths that don't require the JWT token to be added to the Authorization header
        excluded_paths = [
            '/api/swagger/',  # Swagger UI path
            '/api/swagger',
            '/api/redoc/',    # Redoc path
            '/api/redoc',
            # You can add more paths to this list as needed.
        ]

        # Extract the current path from the request
        current_path = request.path
        print(current_path)
        # Extract the token from the cookies only if the current path is not in the excluded paths
        if current_path not in excluded_paths:
            access_token = request.COOKIES.get('access_token')

            # If the token exists, add it to the Authorization header
            if access_token:
                request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

        response = self.get_response(request)
        return response
