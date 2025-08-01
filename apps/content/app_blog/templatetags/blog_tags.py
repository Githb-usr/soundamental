from django import template

register = template.Library()

MOIS_FR = {
    1: "janvier", 2: "février", 3: "mars", 4: "avril",
    5: "mai", 6: "juin", 7: "juillet", 8: "août",
    9: "septembre", 10: "octobre", 11: "novembre", 12: "décembre"
}

@register.filter
def mois_nom(numero):
    """
    Convertit un numéro de mois (1–12) en nom français.
    """
    return MOIS_FR.get(int(numero), numero)

@register.filter
def to_list(start, end):
    """
    Renvoie une liste d'entiers de start à end (inclus).
    Exemple : 1|to_list:12 → [1, 2, ..., 12]
    """
    return list(range(start, end + 1))

@register.filter
def dict_get(dictionnaire, cle):
    """
    Permet d'accéder à un dictionnaire avec une clé dans un template Django.
    Usage : {{ mon_dict|dict_get:cle }}
    """
    return dictionnaire.get(cle, set())
