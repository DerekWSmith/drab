import os

class LogRequestURLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        log_file_path = '/usr/local/var/www/drrbb/_logs/url.log'
        with open(log_file_path, 'a') as file:
            file.write(f"Received URL: {request.path}\n")
        return self.get_response(request)