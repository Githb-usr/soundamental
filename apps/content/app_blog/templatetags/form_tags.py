from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={"class": css})
    return field

@register.filter
def add_data_attr(field, args):
    """
    Ajoute des attributs data-* à un champ (ex: data-section, data-subfolder).
    Utilisation : field|add_data_attr:"section=blog,subfolder=contenu"
    """
    attrs = {}
    for pair in args.split(","):
        if "=" in pair:
            k, v = pair.split("=", 1)
            attrs[f"data-{k.strip()}"] = v.strip()
    return field.as_widget(attrs=attrs)
