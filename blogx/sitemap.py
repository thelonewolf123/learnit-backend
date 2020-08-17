from django.contrib.sitemaps import Sitemap

from .models import Post

class BlogViewSitemap(Sitemap):

    changefreq = 'daily'

    def items(self):

        return Post.objects.all()