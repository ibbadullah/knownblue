from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from adminsection.models import CategoryModel,ArticlesModel


# Static sitemap
class StaticSiteMaps(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    # builtin views for static views
    def items(self):
        return ["Home","ContactUs"]

    def location(self, item):
        return reverse(item)


#Dynamic sitemaps for category
class CategoriesSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return CategoryModel.objects.all()


# Dynamic sitemaps for category
class ArticlesSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ArticlesModel.objects.all()


