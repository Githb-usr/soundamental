from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Article

class BlogRSSFeed(Feed):
    title = "Soundamental – Blog"
    link = "/news/"
    description = "Actualités de Soundamental (nouveautés, musique, site...)"

    def items(self):
        return Article.objects.filter(est_publie=True).order_by('-date_publication')[:20]

    def item_title(self, item):
        return item.titre

    def item_description(self, item):
        return item.get_resume()

    def item_link(self, item):
        return reverse('app_blog:detail_article', args=[item.slug])
