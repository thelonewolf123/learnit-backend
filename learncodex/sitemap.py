from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from .models import FreeCourse


class StaticViewSitemap(Sitemap):
    def items(self):
        return ['index']

    def location(self, item):
        return reverse(item)

class CourseViewSitemap(Sitemap):

    changefreq = 'weekly'

    def items(self):

        return FreeCourse.objects.all()