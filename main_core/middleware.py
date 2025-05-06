class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get language from session or default to English
        language = request.session.get('language', 'en')
        request.LANGUAGE = language
        
        response = self.get_response(request)
        return response 