from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from .models import Course


class StaticViewSitemap(Sitemap):
    def items(self):
        return ['index','about','contact']

    def location(self, item):
        return reverse(item)

class CourseViewSitemap(Sitemap):

    changefreq = 'weekly'

    def items(self):

        return Course.objects.all()