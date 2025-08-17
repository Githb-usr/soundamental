"""
Agrégateur des modèles de l'app Index.
Les classes sont définies dans models/* puis importées ici pour garder
un point d'import unique (apps.content.app_index.models).
"""

from .base_models import Category, PageType
from .index_entry import IndexEntry
from .page_existence import PageExistence
from .config_index import IndexSettings
from .aliases_index import IndexAlias

__all__ = [
    "Category",
    "PageType",
    "IndexEntry",
    "PageExistence",
    "IndexSettings",
    "IndexAlias",
]
