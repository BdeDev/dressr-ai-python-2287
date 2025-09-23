from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from accounts.constants import USE_HTTPS

class StaticSitemap(Sitemap):
    changefreq = 'daily'
    priority = '0.5'
    protocol = 'https' if USE_HTTPS else 'http'
    def items(self):
        return [
            'accounts:login'
        ]
    def location(self, item):
        return reverse(item)
