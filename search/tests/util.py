def print_url(url):
    def decorator(test_func):
        def wrapper(*args, **kwargs):
            print(f"Testing URL: {url}")
            return test_func(*args, **kwargs)
        return wrapper
    return decorator