class FrameOptionsMiddleware:
    def __init__(self, get_reponse):
        self.get_reponse = get_reponse

    def __call__(self, request):
        response = self.get_reponse(request)
        response['X-Frame-Options'] = 'sameorigin'
        return response
