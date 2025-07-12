import random
from apps.core.app_main.models.tags import Tag
from apps.core.app_main.models.static_pages import StaticPageMeta
from apps.core.app_main.models.dynamic_pages import DynamicPageInfo, DynamicPageTag
from apps.content.app_blog.models import Article

def assign_tags_to_existing_pages(nb_tags=2, nb_static=5, nb_dynamic=5, nb_articles=5):
    '''
    Commande à utiliser en console pour créer des tags fake : python manage.py shell
    from apps.utils.factories.tag_helpers import assign_tags_to_existing_pages

    assign_tags_to_existing_pages(
        nb_tags=10,
        nb_static=5,
        nb_dynamic=5,
        nb_articles=25
    )
    '''
    tags = list(Tag.objects.all())
    if not tags:
        print("❌ Aucun tag trouvé.")
        return

    # 🔹 Pages statiques
    static_pages = StaticPageMeta.objects.all()[:nb_static]
    for page in static_pages:
        selected_tags = random.sample(tags, min(nb_tags, len(tags)))
        page.tags.set(selected_tags)
        page.save()
        print(f"✅ Tags assignés à la page statique : {page.title}")

    # 🔹 Pages dynamiques
    dynamic_pages = DynamicPageInfo.objects.all()[:nb_dynamic]
    for page in dynamic_pages:
        selected_tags = random.sample(tags, min(nb_tags, len(tags)))
        for tag in selected_tags:
            DynamicPageTag.objects.create(
                tag=tag,
                page_name=page.page_name,
                display_name=page.display_name,
                page_info=page
            )
        print(f"✅ Tags assignés à la page dynamique : {page.display_name}")

    # 🔹 Articles
    articles = Article.objects.all()[:nb_articles]
    for article in articles:
        selected_tags = random.sample(tags, min(nb_tags, len(tags)))
        article.tags.set(selected_tags)
        article.save()
        print(f"✅ Tags assignés à l'article : {article.titre}")
