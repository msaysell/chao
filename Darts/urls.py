from django.contrib import sitemaps
from django.urls import reverse, path as url

from django.conf.urls import include
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

urlpatterns = [url(r'', PostListView.as_view(), name='home'),
               url(r'api/', include((router.urls, 'api'), namespace='api')),
               url(r'2s3xYDK627En3B5E/', csrf_exempt(ReceiveMsgView.as_view()), name='receive_msg'),
               url(r'contact', ContactFormView.as_view(), name='contact'),
               url(r'', include(('derby_darts.urls', 'derby_darts'), namespace='derby_darts')),
               url(r'rules/', include(('Rules.urls', 'rules'), namespace='Rules')),
               url(r'fixtures/', include(('Fixtures.urls', 'fixtures'), namespace='Fixtures')),
               url(r'settings/', include(('Dashboard.urls', 'dashboard'), namespace='Dashboard')),
               url(r'login/', login_user, name='login'),
               url(r'sitemap\.xml', sitemap, {'sitemaps': sitemaps}),
               url(r'xy/', admin.site.urls),
               ]
