from derby_darts.models import League
import os
__author__ = 'Michael'


class LeagueMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        short_url = os.environ.get('AWS_FEATURE', None) or request.META.get("HTTP_X_BENDER")

        if short_url is None:
            request.league = League.objects.first()
            return None

        if League.objects.filter(short_url=short_url).exists():
            league = League.objects.get(short_url=short_url)
        else:
            league = League.objects.first()

        request.league = league
        return None

    def process_request(self, request):
        short_url = os.environ.get('AWS_FEATURE', None) or request.META.get("HTTP_X_BENDER")

        if short_url is None:
            request.league = League.objects.first()
            return None

        if League.objects.filter(short_url=short_url).exists():
            league = League.objects.get(short_url=short_url)
        else:
            league = League.objects.first()

        request.league = league
        return None
