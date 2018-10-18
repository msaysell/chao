from django.contrib import sitemaps
from django.core.urlresolvers import reverse

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView

from Darts.settings import STATIC_URL
from derby_darts.views import login_user, index, ContactFormView, PostListView, ReceiveMsgView
from Darts.api.router import router


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['derby_darts:home', 'derby_darts:league', 'Fixtures:fixtures_by_team', 'contact']

    def location(self, item):
        return reverse(item)


sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [url(r'^$', PostListView.as_view(), name='home'),
               url(r'^api/', include(router.urls, namespace='api')),
               url(r'^2s3xYDK627En3B5E/$', csrf_exempt(ReceiveMsgView.as_view()), name='receive_msg'),
               url(r'^contact$', ContactFormView.as_view(), name='contact'),
               url(r'^', include('derby_darts.urls', namespace='derby_darts')),
               url(r'^rules/', include('Rules.urls', namespace='Rules')),
               url(r'^fixtures/', include('Fixtures.urls', namespace='Fixtures')),
               url(r'^settings/', include('Dashboard.urls', namespace='Dashboard')),
               url(r'^login/$', login_user, name='login'),
               url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}),
               url(r'^xy/', include(admin.site.urls)),
               ]
