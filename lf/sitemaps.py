from django.contrib import sitemaps
from django.urls import reverse
from .models import PortfolioItem, Company
from django_distill.distill import distill_path


class StaticViewSitemap(sitemaps.Sitemap):
    def items(self):
        return ['home', 'seo-index', 'content-writing', 'portfolio-index', 'portfolio-video'] # Specify static pages.

    def location(self, item):
        return reverse(item)
    

class seoExampleSitemap(sitemaps.Sitemap):
	def items(self):
		return Company.objects.filter(is_published=True)
	