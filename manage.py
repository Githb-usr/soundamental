import os
import sys
from decouple import config

def main():
    """Run administrative tasks."""
    # D'abord on lit l'env
    ENVIRONMENT = config("ENVIRONMENT", default="local")  # "local" ou "production"

    # Ensuite on configure Django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.settings.{ENVIRONMENT}")

    print(f"Django utilise : {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    print(f"ENVIRONMENT dans .env = {config('ENVIRONMENT', default='NON TROUVÉ')}")
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
