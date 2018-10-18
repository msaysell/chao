from derby_darts.models import League
import os
__author__ = 'Michael'


class LeagueMiddleware(object):
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
