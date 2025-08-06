from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings

# def custom_error_404(request, exception=None):
#     print("🚨 Handler 404 exécuté !")
#     return render(request, "pages/errors/error_404.html", status=404)

def custom_error_404(request, exception=None):
    status_code = "404"  # On force le type string
    # print(f"🚨 Handler 404 exécuté ! status_code = {status_code}")  # Debug console
    return render(request, "pages/errors/error_404.html", status=404)

def custom_error_500(request):
    # print("🔥 Handler 500 exécuté")
    # print("DEBUG =", settings.DEBUG)
    # print("ENV =", os.environ.get("ENVIRONMENT"))
    return render(request, "pages/errors/error_500.html", status=500)
    # return HttpResponse("<h1>🔥 500 direct sans template 🔥</h1>", status=500)
