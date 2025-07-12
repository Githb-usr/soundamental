from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.timezone import now
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage, FileSystemStorage
from django.core.files.uploadedfile import UploadedFile
import os

# === Pagination ===
def paginate(queryset, request, per_page=None):
    """
    Gère la pagination d'un queryset ou d'une liste.
    
    Priorité pour le nombre d'éléments par page :
    1. Valeur fournie en paramètre `per_page`
    2. Valeur définie dans settings (`PAGINATION_SIZE`)
    3. Valeur par défaut (25)

    :param queryset: Liste ou queryset à paginer
    :param request: Requête HTTP pour récupérer le numéro de page
    :param per_page: Nombre d'éléments par page (priorité sur settings)
    :return: page_obj (données paginées) et paginator (objet Django Paginator)
    """
    per_page = per_page or getattr(settings, "PAGINATION_SIZE", 25)

    paginator = Paginator(queryset, per_page)
    page = request.GET.get("page")

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return page_obj, paginator

# === Anti-spam ===
def check_request_delay(request, session_key="last_request_time", delay=None):
    """
    Vérifie si une action (ex: formulaire de contact) doit attendre avant d'être répétée.
    
    :param request: Requête utilisateur (utilisée pour accéder à la session)
    :param session_key: Clé sous laquelle l'heure de la dernière action est stockée en session
    :param delay: Temps minimal entre deux actions, en secondes (priorité sur settings)
    :return: None si aucun délai, sinon un dict contenant `time_remaining`
    """
    delay = delay or getattr(settings, "DEFAULT_REQUEST_DELAY", 120)  # Utilise settings si pas fourni
    last_action_time = request.session.get(session_key)
    
    if not last_action_time:
        return None  # Aucun délai actif

    time_since_last = now().timestamp() - last_action_time
    time_remaining = max(delay - int(time_since_last), 0)

    if time_remaining > 0:
        messages.error(
            request, 
            f"Vous devez attendre encore <span id='timer'>{time_remaining}</span> secondes avant de réessayer."
        )
        return {"time_remaining": time_remaining}  # Retourne le temps restant

    return None  # Aucun délai actif
