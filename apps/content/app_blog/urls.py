from django.urls import path
from .feeds import BlogRSSFeed
from .views import (
    ArticleListView, ArticleDetailView, ArticleArchiveView,
    ArticleCategorieView, ArticleCreateView,
    media_images_view, delete_blog_image,
)

app_name = "app_blog"

urlpatterns = [
    # RSS
    path('rss/', BlogRSSFeed(), name='flux_rss'),
    
    # Archive annuelle filtrée par catégorie (navigation croisée année + catégorie)
    path('<int:annee>/categorie/<slug:slug>/', ArticleCategorieView.as_view(), name='articles_par_annee_categorie'),
    
    # Articles par catégorie toutes années confondues
    path('categorie/<slug:slug>/', ArticleCategorieView.as_view(), name='articles_par_categorie'),
    
    # Accueil des archives
    path('', ArticleListView.as_view(), name='liste_articles'),
    # Archive annuelle
    path('<int:annee>/', ArticleArchiveView.as_view(), name='archives_annee'),
    # Archive mensuelle
    path('<int:annee>/<int:mois>/', ArticleArchiveView.as_view(), name='archives_mois'),
    
    # Liste des images uploadées pour le blog
    path("medias/", media_images_view, name="blog_media_images"),
    # Suppression d’une image (admin uniquement)
    path("medias/delete/<str:filename>/", delete_blog_image, name="delete_blog_image"),

    # Formulaire de création d'article en ligne (admin, contributeurs)
    path("creer/", ArticleCreateView.as_view(), name="article_creer"),
    
    # Détail article
    path('<slug:slug>/', ArticleDetailView.as_view(), name='detail_article'),
]
